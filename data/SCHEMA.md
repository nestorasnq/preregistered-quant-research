# `ledger.csv` — schema and provenance

One row per trade. 5,474 rows, seven instruments, 2011-03-10 to 2026-08-20.

---

## Columns

| Column | Type | Values | Notes |
|---|---|---|---|
| `date` | ISO date | `YYYY-MM-DD` | Date the position opened. Deliberately date-level; see redaction below |
| `instrument` | string | `ES1!` `NQ1!` `NK2251!` `FDAX1!` `Z1!` `XAUUSD` `EURUSD` | |
| `direction` | string | `long` `short` | |
| `outcome` | string | `W` `L` `BE` `AMBIG` | See resolution below |
| `R_result` | integer | `1` `-1` `0` | Gross R multiple. Empty for `AMBIG`. Fixed 1:1 target throughout |
| `iso_week` | string | `YYYY-Wnn` | ISO year-week. The clustering unit for block inference |
| `sample` | string | `in_sample` `OOS_RESERVED` | Campaign designation at time of collection |

**Instrument venues.** ES1! and NQ1! — CME. FDAX1! — Eurex. NK2251! — Osaka. Z1! — ICE Europe.
XAUUSD and EURUSD — aggregated retail feeds, not exchange data. The distinction matters: the
data-feed validation study exists because one non-exchange feed was load-bearing.

---

## Resolution

`W`, `L` and `BE` are **resolved** outcomes and enter all statistics. `AMBIG` denotes a trade whose
outcome could not be determined unambiguously from the available bar data, typically where target
and stop were both touched within a single bar and the sequence is unrecoverable.

There are **78 AMBIG rows campaign-wide, 15 of them in the three-instrument book.**

They are retained in this file rather than dropped during assembly so that the exclusion is
**visible and reproducible** rather than an unstated upstream decision. Filtering to
`outcome ∈ {W, L, BE}` reproduces every published figure.

Win rate throughout is computed over **decisive** trades only — `W / (W + L)` — with break-evens
excluded from the ratio but retained in the denominator for cost purposes, since a scratched trade
still pays commission and spread.

---

## Provenance

All published figures are computed from this ledger. It is the campaign's own record and is short
approximately **27 book trades** against the engine's full output, from chunk-boundary
reconstruction during data assembly. Fifteen AMBIG outcomes are retained in the file and excluded
from resolved-trade statistics.

The gaps are **not randomly distributed** — they sit at chunk boundaries, which correspond to
specific periods. Across 2,030 book trades and sixteen years this has no material effect and the
year-by-year table reproduces exactly. On small subsets it does have an effect, documented in
`LIMITATIONS.md` §8. Treat aggregate figures as sound and subset analyses as requiring a clean
re-export.

---

## What was removed, and why

| Removed | Reason |
|---|---|
| `entry`, `sl`, `tp`, `sl1R` | Price levels. Redaction — the strategy is not published and entry geometry is the most direct route to reconstructing it |
| intraday timestamps (`utc_hour`, `opened_utc`) | Redaction. Date-level resolution preserves every statistical claim while removing the ability to locate the entry bar on a chart |
| `bars`, `mfe`, `mae` | Redaction. Not required by any published figure |
| `model`, `h4_pos`, `h4_trend`, `gate1`, `era_block` | Internal strategy state |

Two of the removed columns were also **defective** in the source export, which is worth recording
for anyone who works from the originals: `entry` is blank on all 694 ES1! rows and holds 29 distinct
small integers rather than prices on NQ1!. The `sl1R` column was verified to be the **stop distance
in price units** rather than a price level, by testing `|entry − sl| == sl1R` against the GC1!
export, which carries all three columns — 1,013 of 1,013 rows matched.

---

## Redaction principle

Everything needed to check a statistical claim is here. Nothing describing **how a trade was
selected** is.

The published inference code reproduces the year table, the pooled and per-instrument win rates with
clustered confidence intervals, the realised and bootstrapped drawdown distributions, and the
cost-sensitivity grids — all from these seven columns.

The strategy is not recoverable from them.

---

## Reproducing

```bash
python reproduce.py
```

Regenerates every table in `results/tables/` from this file. Bootstrap seeds are fixed at `20260909`.
Percentile estimates in the far tail — the 99th percentile of the drawdown distribution in
particular — carry resampling noise of a few tenths of an R and should not be read to three
significant figures.
