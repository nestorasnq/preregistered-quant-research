"""Block-bootstrap inference over clustered trade outcomes.

Why blocks
----------
Trades are not independent draws. A strategy that keys on higher-timeframe structure will
take several trades off the same market condition within a few days, and those outcomes
are correlated. Resampling individual trades treats each one as fresh information, which
understates the variance and narrows every confidence interval. The interval is then
wrong in the direction that flatters the strategy.

Resampling whole ISO weeks preserves the within-week dependence and lets it propagate
into the interval. The week is the natural unit here because the clustering comes from
market regime, and market regime persists over days rather than hours.

This is a moving-block bootstrap with the block boundaries fixed to calendar weeks rather
than to a chosen block length. Fixing them to the calendar costs a little efficiency and
removes a free parameter, which is the right trade when the free parameter would be
chosen by the person reporting the result.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .ledger import net_r

WEEKS_PER_YEAR = 52


def _week_blocks(df: pd.DataFrame, cost_r: float) -> list[np.ndarray]:
    """Split a ledger into one array of per-trade net R per ISO week, in calendar order."""
    g = df.assign(net=net_r(df, cost_r))
    return [sub["net"].to_numpy() for _, sub in g.groupby("iso_week", sort=True)]


def _max_drawdown(path: np.ndarray) -> float:
    """Maximum peak-to-trough decline of a cumulative equity curve, in R."""
    if path.size == 0:
        return 0.0
    equity = np.cumsum(path)
    peak = np.maximum.accumulate(equity)
    return float(np.max(peak - equity))


def realised_max_drawdown(df: pd.DataFrame, cost_r: float) -> float:
    """Maximum drawdown along the actual historical path, in R."""
    g = df.sort_values("date", kind="stable")
    return _max_drawdown(net_r(g, cost_r).to_numpy())


def drawdown_distribution(
    df: pd.DataFrame,
    cost_r: float,
    horizon_years: float = 3.0,
    n_resamples: int = 10_000,
    seed: int = 20260909,
) -> dict:
    """Distribution of maximum drawdown over a forward horizon.

    Draws `horizon_years * 52` ISO-week blocks with replacement, concatenates them into a
    synthetic path, and records that path's maximum drawdown. The percentiles answer the
    question a risk limit actually asks: over the next three years, how bad does this get?

    Returns drawdowns in R. Multiply by risk-per-trade to convert to percent of equity.
    """
    blocks = _week_blocks(df, cost_r)
    if not blocks:
        raise ValueError("ledger contains no resolved trades")

    rng = np.random.default_rng(seed)
    n_blocks = int(round(horizon_years * WEEKS_PER_YEAR))
    idx = rng.integers(0, len(blocks), size=(n_resamples, n_blocks))

    draws = np.empty(n_resamples)
    for i in range(n_resamples):
        draws[i] = _max_drawdown(np.concatenate([blocks[j] for j in idx[i]]))

    return {
        "horizon_years": horizon_years,
        "n_resamples": n_resamples,
        "n_week_blocks": len(blocks),
        "median": float(np.percentile(draws, 50)),
        "dd95": float(np.percentile(draws, 95)),
        "dd99": float(np.percentile(draws, 99)),
        "max": float(draws.max()),
    }


def _week_stats(df: pd.DataFrame, cost_r: float) -> dict:
    """Per-ISO-week sufficient statistics: wins, losses, trade count, summed net R.

    Resampling reduces to indexing these four arrays, which is what makes 10,000
    resamples cheap. Any statistic expressible from (wins, losses, n, sum_net) can be
    bootstrapped without reassembling a DataFrame per draw.
    """
    g = df.assign(net=net_r(df, cost_r)).groupby("iso_week", sort=True)
    return {
        "wins": g.apply(lambda s: int((s["outcome"] == "W").sum()), include_groups=False).to_numpy(),
        "losses": g.apply(lambda s: int((s["outcome"] == "L").sum()), include_groups=False).to_numpy(),
        "n": g.size().to_numpy(),
        "sum_net": g["net"].sum().to_numpy(),
    }


def bootstrap_ci(
    df: pd.DataFrame,
    statistic: str = "win_rate",
    cost_r: float = 0.0,
    n_resamples: int = 10_000,
    alpha: float = 0.05,
    seed: int = 20260909,
) -> dict:
    """Percentile confidence interval, resampling whole ISO weeks with replacement.

    `statistic` is 'win_rate' (wins over decisive trades) or 'mean_net_r' (mean net R per
    resolved trade). Both are computed from per-week sufficient statistics, so the whole
    bootstrap is a handful of vectorised operations rather than a Python loop.
    """
    st = _week_stats(df, cost_r)
    k = len(st["n"])
    if k == 0:
        raise ValueError("ledger contains no resolved trades")

    rng = np.random.default_rng(seed)
    idx = rng.integers(0, k, size=(n_resamples, k))

    if statistic == "win_rate":
        w = st["wins"][idx].sum(axis=1)
        d = w + st["losses"][idx].sum(axis=1)
        draws = w / np.where(d > 0, d, 1)
        point = st["wins"].sum() / max(st["wins"].sum() + st["losses"].sum(), 1)
    elif statistic == "mean_net_r":
        draws = st["sum_net"][idx].sum(axis=1) / np.maximum(st["n"][idx].sum(axis=1), 1)
        point = st["sum_net"].sum() / max(st["n"].sum(), 1)
    else:
        raise ValueError("statistic must be 'win_rate' or 'mean_net_r'")

    return {
        "statistic": statistic,
        "point": float(point),
        "lcb": float(np.percentile(draws, 100 * alpha / 2)),
        "ucb": float(np.percentile(draws, 100 * (1 - alpha / 2))),
        "alpha": alpha,
        "n_resamples": n_resamples,
        "n_week_blocks": k,
    }


def win_rate(df: pd.DataFrame) -> float:
    """Win rate over decisive trades. Break-evens are excluded from the ratio."""
    w = int((df["outcome"] == "W").sum())
    loss = int((df["outcome"] == "L").sum())
    return w / (w + loss) if (w + loss) else float("nan")


def mean_net_r(df: pd.DataFrame, cost_r: float = 0.0):
    """Mean net R per resolved trade."""
    return float(net_r(df, cost_r).mean())
