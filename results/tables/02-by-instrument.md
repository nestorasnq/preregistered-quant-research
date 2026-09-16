# Per-instrument edge with clustered intervals

| set | resolved | win rate | 95% CI | break-even | edge | edge at 95% LCB |
|---|---|---|---|---|---|---|
| ES1! | 694 | 56.65% | [52.14, 61.04] | 53.00% | +3.66 pp | -0.86 pp |
| NQ1! | 721 | 61.46% | [57.16, 65.75] | 52.81% | +8.65 pp | +4.35 pp |
| NK2251! | 615 | 61.00% | [56.67, 65.29] | 52.73% | +8.27 pp | +3.94 pp |
| book | 2030 | 59.75% | [57.20, 62.29] | 52.85% | +6.91 pp | +4.36 pp |

Win rate is computed over decisive trades only. Confidence intervals are percentile bootstrap over whole ISO weeks, which preserves within-week dependence between trades taken off the same market condition.

**ES1! does not clear break-even at 95% confidence on its own.** The pooled book does. See LIMITATIONS.md §3.
