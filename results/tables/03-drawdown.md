# Drawdown: realised and bootstrapped

Realised maximum drawdown on the historical path: **19.1 R**.

Block-bootstrapped over a 3-year forward horizon, 10,000 resamples drawn from 682 ISO-week blocks:

| percentile | drawdown (R) |
|---|---|
| 50th | 12.2 |
| 95th | 21.7 |
| 99th | ~28.3 |

Converted to percent of equity by risk per trade:

| risk/trade | return/yr | max DD (95th) | max DD (99th) |
|---|---|---|---|
| 0.50% | +7.91% | 10.9% | ~14.2% |
| 1.00% | +15.81% | 21.7% | ~28.3% |

Return and drawdown scale together. Doubling risk is the same strategy at twice the leverage, not a better one.
