#!/usr/bin/env python3
"""Regenerate every published table from data/ledger.csv.

    python reproduce.py

Writes markdown tables to results/tables/ and prints a reconciliation summary. Bootstrap
seeds are fixed, so output is deterministic. Far-tail percentiles — the 99th percentile of
the drawdown distribution in particular — carry resampling noise of a few tenths of an R
and should not be read to three significant figures.

Nothing here knows anything about the strategy. It operates on a trade-outcome ledger and
a table of summary geometry, both published.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "tooling"))

from inference import (  # noqa: E402
    load, resolved, summary, by_year, realised_max_drawdown,
    drawdown_distribution, bootstrap_ci, breakeven_win_rate,
    sensitivity_table, breakeven_ticks,
)

BOOK = ["ES1!", "NQ1!", "NK2251!"]
COST_R = 0.048
RISK_PER_TRADE = 0.005
SEED = 20260909
OUT = Path("results/tables")


def write(name: str, title: str, lines: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(f"# {title}\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote results/tables/{name}")


def table_year(book) -> None:
    yt = by_year(book, COST_R)
    lines = ["| year | trades | win rate | net R |", "|---|---|---|---|"]
    for year, r in yt.iterrows():
        lines.append(f"| {year} | {int(r.n)} | {100 * r.win_rate:.1f}% | {r.net_R:+.2f} |")
    pos = int((yt.net_R > 0).sum())
    lines += ["", f"**{pos} of {len(yt)} years positive.** Total {yt.net_R.sum():+.2f} R "
                  f"over {int(yt.n.sum())} resolved trades, at {COST_R} R modelled cost."]
    write("01-year-by-year.md", "Book performance by year", lines)
    return yt


def table_instruments(df) -> None:
    lines = ["| set | resolved | win rate | 95% CI | break-even | edge | edge at 95% LCB |",
             "|---|---|---|---|---|---|---|"]
    for name, instruments in [("ES1!", ["ES1!"]), ("NQ1!", ["NQ1!"]),
                              ("NK2251!", ["NK2251!"]), ("book", BOOK)]:
        sub = resolved(df, instruments)
        s = summary(sub, COST_R)
        ci = bootstrap_ci(sub, "win_rate", seed=SEED)
        be = breakeven_win_rate(COST_R, s["be_fraction"])
        lines.append(
            f"| {name} | {s['n_resolved']} | {100 * s['win_rate']:.2f}% | "
            f"[{100 * ci['lcb']:.2f}, {100 * ci['ucb']:.2f}] | {100 * be:.2f}% | "
            f"{100 * (s['win_rate'] - be):+.2f} pp | {100 * (ci['lcb'] - be):+.2f} pp |"
        )
    lines += ["", "Win rate is computed over decisive trades only. Confidence intervals are "
                  "percentile bootstrap over whole ISO weeks, which preserves within-week "
                  "dependence between trades taken off the same market condition.",
              "", "**ES1! does not clear break-even at 95% confidence on its own.** The pooled "
                  "book does. See LIMITATIONS.md §3."]
    write("02-by-instrument.md", "Per-instrument edge with clustered intervals", lines)


def table_drawdown(book) -> None:
    realised = realised_max_drawdown(book, COST_R)
    dd = drawdown_distribution(book, COST_R, horizon_years=3.0, n_resamples=10_000, seed=SEED)
    net_r_total = summary(book, COST_R)["net_R"]
    years = (book["date"].max() - book["date"].min()).days / 365.25
    r_per_year = net_r_total / years

    lines = [f"Realised maximum drawdown on the historical path: **{realised:.1f} R**.", "",
             f"Block-bootstrapped over a {dd['horizon_years']:.0f}-year forward horizon, "
             f"{dd['n_resamples']:,} resamples drawn from {dd['n_week_blocks']} ISO-week blocks:", "",
             "| percentile | drawdown (R) |", "|---|---|",
             f"| 50th | {dd['median']:.1f} |",
             f"| 95th | {dd['dd95']:.1f} |",
             f"| 99th | ~{dd['dd99']:.1f} |", "",
             "Converted to percent of equity by risk per trade:", "",
             "| risk/trade | return/yr | max DD (95th) | max DD (99th) |", "|---|---|---|---|"]
    for risk in (0.005, 0.010):
        lines.append(f"| {100 * risk:.2f}% | {100 * r_per_year * risk:+.2f}% | "
                     f"{dd['dd95'] * 100 * risk:.1f}% | ~{dd['dd99'] * 100 * risk:.1f}% |")
    lines += ["", "Return and drawdown scale together. Doubling risk is the same strategy at "
                  "twice the leverage, not a better one."]
    write("03-drawdown.md", "Drawdown: realised and bootstrapped", lines)


def table_slippage(df) -> None:
    geometry = list(csv.DictReader(open("data/instrument_geometry.csv", encoding="utf-8")))
    lines = []
    for g in geometry:
        if not g["median_stop"] or g["instrument"] != "NQ1!":
            continue
        lo, hi = int(g["era_start"]), int(g["era_end"])
        if (lo, hi) not in [(2011, 2017), (2022, 2026)]:
            continue
        stop, tick = float(g["median_stop"]), float(g["tick_size"])
        sub = resolved(df, ["NQ1!"])
        sub = sub[(sub["date"].dt.year >= lo) & (sub["date"].dt.year <= hi)]
        s = summary(sub, COST_R)
        lcb = bootstrap_ci(sub, "win_rate", seed=SEED)["lcb"]
        grid = (0, 0.5, 1.0, 1.5, 2.0) if hi == 2017 else (0, 10, 19, 25, 45)
        t = sensitivity_table(s["win_rate"], COST_R, s["be_fraction"], tick, stop, grid)

        lines += [f"## NQ1! {lo}–{hi}", "",
                  f"Median stop {stop:.2f} points = {stop / tick:.0f} ticks. "
                  f"Win rate {100 * s['win_rate']:.2f}% over {s['wins'] + s['losses']} decisive trades.", "",
                  "| ticks/side | total cost | break-even | edge remaining |", "|---|---|---|---|"]
        for ticks, r in t.iterrows():
            lines.append(f"| {ticks} | {r.total_cost_R:.4f} R | "
                         f"{100 * r.breakeven_win_rate:.2f}% | {r.edge_pp:+.2f} pp |")
        lines += ["", f"Edge reaches zero at **{breakeven_ticks(s['win_rate'], COST_R, s['be_fraction'], tick, stop):.1f} "
                      f"ticks per side** on the point estimate, "
                      f"**{breakeven_ticks(lcb, COST_R, s['be_fraction'], tick, stop):.1f}** at the 95% "
                      f"lower bound on the win rate.", ""]

    lines += ["---", "",
              "Tick tolerance is a property of the era, not of the strategy: NQ's tick is fixed "
              "at 0.25 points while the instrument rose roughly tenfold, so the stop grew about "
              "eightfold in ticks. The invariant unit is fraction of R lost. **Plan against the "
              "lower bound.**", "",
              "No figure in this repository is net of slippage. The fill remains unmeasured."]
    write("04-slippage-sensitivity.md", "Cost sensitivity by regime", lines)


def main() -> int:
    df = load("data/ledger.csv")
    book = resolved(df, BOOK)
    s = summary(book, COST_R)

    print(f"ledger: {len(df):,} rows, {df['instrument'].nunique()} instruments, "
          f"{df['iso_week'].nunique()} ISO weeks")
    print(f"book:   {s['n_resolved']:,} resolved ({s['wins']}W / {s['losses']}L / "
          f"{s['breakevens']}BE), {s['first']} to {s['last']}\n")

    yt = table_year(book)
    table_instruments(df)
    table_drawdown(book)
    table_slippage(df)

    print(f"\nreconciliation: {s['net_R']:+.2f} R total, "
          f"{int((yt.net_R > 0).sum())}/{len(yt)} years positive, "
          f"realised max DD {realised_max_drawdown(book, COST_R):.1f} R")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
