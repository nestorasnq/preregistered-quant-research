"""Cost modelling, break-even win rate, and slippage sensitivity.

The distinction that matters
----------------------------
Commissions, spreads and rolls are fees. They appear on a schedule, a broker will quote
them in advance, and they can be modelled before a single trade is placed.

Slippage is not a fee. It is the gap between the price that triggered an order and the
price that filled it, and it is an execution outcome. No schedule contains it.

For a strategy that enters on a resting stop and exits on a stop, both sides are adversely
selected by construction: a stop fills while price is moving through the level, in the
direction that hurts. The functions here exist to quantify how much of a measured edge
survives that, because for a 1:1 target on a tight stop the answer is often "not much".
"""

from __future__ import annotations

import pandas as pd


def breakeven_win_rate(cost_r: float, be_fraction: float = 0.0) -> float:
    """Win rate over decisive trades at which expectancy is zero, for a 1:1 target.

    With no cost and no break-evens this is 50%. Cost moves it up twice as fast as the
    cost itself, because a fee is paid on winners and losers alike.

    Break-even trades make it worse again: they realise no R but still pay cost, so the
    decisive trades have to carry them. `be_fraction` is the share of *resolved* trades
    that scratch.

        E = (1 - b)(2p - 1 - c) - bc = 0
        p = [1 + c + bc / (1 - b)] / 2
    """
    if not 0.0 <= be_fraction < 1.0:
        raise ValueError("be_fraction must be in [0, 1)")
    drag = be_fraction * cost_r / (1.0 - be_fraction)
    return (1.0 + cost_r + drag) / 2.0


def slippage_cost_r(ticks_per_side: float, tick_value: float, stop_distance: float) -> float:
    """Slippage expressed in R, given ticks lost per side.

    One R is the stop distance. Slipping `t` ticks on entry and `t` on exit costs
    2 * t * tick_value in price terms, which is 2 * t * tick_value / stop_distance in R.
    """
    if stop_distance <= 0:
        raise ValueError("stop_distance must be positive")
    return 2.0 * ticks_per_side * tick_value / stop_distance


def sensitivity_table(
    measured_win_rate: float,
    base_cost_r: float,
    be_fraction: float,
    tick_value: float,
    stop_distance: float,
    ticks_grid=(0.0, 0.5, 1.0, 1.5, 2.0),
) -> pd.DataFrame:
    """How much edge survives at each level of per-side slippage.

    `edge_pp` is the measured win rate minus the break-even win rate, in percentage
    points. Where it crosses zero is the honest answer to "what execution quality does
    this strategy require in order to exist".
    """
    rows = []
    for t in ticks_grid:
        added = slippage_cost_r(t, tick_value, stop_distance)
        total = base_cost_r + added
        be = breakeven_win_rate(total, be_fraction)
        rows.append({
            "ticks_per_side": t,
            "added_cost_R": added,
            "total_cost_R": total,
            "breakeven_win_rate": be,
            "edge_pp": 100.0 * (measured_win_rate - be),
        })
    return pd.DataFrame(rows).set_index("ticks_per_side")


def breakeven_ticks(
    measured_win_rate: float,
    base_cost_r: float,
    be_fraction: float,
    tick_value: float,
    stop_distance: float,
) -> float:
    """Per-side slippage, in ticks, at which the edge reaches exactly zero.

    Solves p = [1 + c + bc/(1-b)] / 2 for c, then converts c back to ticks.
    """
    k = 1.0 + be_fraction / (1.0 - be_fraction)
    cost_at_zero = (2.0 * measured_win_rate - 1.0) / k
    added = cost_at_zero - base_cost_r
    if added <= 0:
        return 0.0
    return added * stop_distance / (2.0 * tick_value)
