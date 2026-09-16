"""Block-bootstrap inference and cost analysis for trade-outcome ledgers.

Strategy-agnostic. Give it any ledger in the published schema and it returns
clustered confidence intervals, drawdown distributions and cost sensitivity.
"""
from .ledger import load, resolved, net_r, summary, by_year, LedgerError
from .inference import (
    drawdown_distribution, realised_max_drawdown, bootstrap_ci, win_rate, mean_net_r,
)
from .costs import (
    breakeven_win_rate, slippage_cost_r, sensitivity_table, breakeven_ticks,
)
