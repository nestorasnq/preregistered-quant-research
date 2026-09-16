"""Ledger loading and validation.

A ledger is a trade-outcome record with one row per trade. The schema is deliberately
minimal: everything needed to reproduce a statistical claim, and nothing that describes
how a trade was selected.

Required columns
----------------
date        ISO date, YYYY-MM-DD
instrument  free-form symbol
direction   'long' or 'short'
outcome     'W' | 'L' | 'BE' | 'AMBIG'
R_result    realised R multiple, gross of cost
iso_week     ISO year-week, 'YYYY-Wnn' — the clustering unit for block inference
sample      'in_sample' | 'OOS_RESERVED' or any free-form tag

AMBIG rows are carried in the file and excluded from resolved-trade statistics. They are
kept rather than dropped upstream so that the exclusion is visible and reproducible.
"""

from __future__ import annotations

import pandas as pd

REQUIRED = ["date", "instrument", "direction", "outcome", "R_result", "iso_week", "sample"]
RESOLVED = ("W", "L", "BE")


class LedgerError(ValueError):
    """Raised when a ledger does not satisfy the published schema."""


def load(path: str) -> pd.DataFrame:
    """Read a ledger from CSV and validate it against the schema.

    Validation is strict on purpose. A silently malformed ledger produces numbers that
    look plausible, which is the failure mode worth spending code on.
    """
    df = pd.read_csv(path, dtype={"iso_week": str, "sample": str})

    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise LedgerError(f"missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    if df["date"].isna().any():
        bad = int(df["date"].isna().sum())
        raise LedgerError(f"{bad} row(s) have an unparseable date")

    unknown = set(df["outcome"].unique()) - set(RESOLVED) - {"AMBIG"}
    if unknown:
        raise LedgerError(f"unknown outcome value(s): {sorted(unknown)}")

    bad_dir = set(df["direction"].unique()) - {"long", "short"}
    if bad_dir:
        raise LedgerError(f"unknown direction value(s): {sorted(bad_dir)}")

    if not df["iso_week"].str.match(r"^\d{4}-W\d{2}$").all():
        raise LedgerError("iso_week must be formatted 'YYYY-Wnn'")

    return df.sort_values(["date", "instrument"], kind="stable").reset_index(drop=True)


def resolved(df: pd.DataFrame, instruments: list[str] | None = None) -> pd.DataFrame:
    """Return resolved trades only (W/L/BE), optionally filtered to a set of instruments."""
    out = df[df["outcome"].isin(RESOLVED)]
    if instruments is not None:
        out = out[out["instrument"].isin(instruments)]
    return out.reset_index(drop=True)


def net_r(df: pd.DataFrame, cost_r: float) -> pd.Series:
    """Per-trade R net of a flat round-turn cost, in R units.

    Cost is applied to every resolved trade including break-evens: a trade that is
    scratched at entry still pays commission and spread.
    """
    return df["R_result"].astype(float) - cost_r


def summary(df: pd.DataFrame, cost_r: float) -> dict:
    """Headline statistics for a set of resolved trades."""
    w = int((df["outcome"] == "W").sum())
    loss = int((df["outcome"] == "L").sum())
    be = int((df["outcome"] == "BE").sum())
    decisive = w + loss
    return {
        "n_resolved": len(df),
        "wins": w,
        "losses": loss,
        "breakevens": be,
        "win_rate": w / decisive if decisive else float("nan"),
        "be_fraction": be / len(df) if len(df) else float("nan"),
        "net_R": float(net_r(df, cost_r).sum()),
        "first": df["date"].min().date().isoformat() if len(df) else None,
        "last": df["date"].max().date().isoformat() if len(df) else None,
    }


def by_year(df: pd.DataFrame, cost_r: float) -> pd.DataFrame:
    """Year-by-year table: trade count, win rate over decisive trades, net R."""
    g = df.assign(year=df["date"].dt.year, net=net_r(df, cost_r))
    rows = []
    for year, sub in g.groupby("year"):
        w = int((sub["outcome"] == "W").sum())
        loss = int((sub["outcome"] == "L").sum())
        rows.append({
            "year": int(year),
            "n": len(sub),
            "win_rate": w / (w + loss) if (w + loss) else float("nan"),
            "net_R": float(sub["net"].sum()),
        })
    return pd.DataFrame(rows).set_index("year")
