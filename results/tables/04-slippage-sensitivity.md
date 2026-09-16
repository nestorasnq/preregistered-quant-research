# Cost sensitivity by regime

## NQ1! 2011–2017

Median stop 12.75 points = 51 ticks. Win rate 56.84% over 234 decisive trades.

| ticks/side | total cost | break-even | edge remaining |
|---|---|---|---|
| 0.0 | 0.0480 R | 52.84% | +4.00 pp |
| 0.5 | 0.0676 R | 54.00% | +2.84 pp |
| 1.0 | 0.0872 R | 55.16% | +1.68 pp |
| 1.5 | 0.1068 R | 56.32% | +0.51 pp |
| 2.0 | 0.1264 R | 57.48% | -0.65 pp |

Edge reaches zero at **1.7 ticks per side** on the point estimate, **0.0** at the 95% lower bound on the win rate.

## NQ1! 2022–2026

Median stop 98.88 points = 396 ticks. Win rate 66.15% over 195 decisive trades.

| ticks/side | total cost | break-even | edge remaining |
|---|---|---|---|
| 0 | 0.0480 R | 52.83% | +13.32 pp |
| 10 | 0.0986 R | 55.81% | +10.34 pp |
| 19 | 0.1441 R | 58.50% | +7.66 pp |
| 25 | 0.1744 R | 60.29% | +5.87 pp |
| 45 | 0.2756 R | 66.25% | -0.10 pp |

Edge reaches zero at **44.7 ticks per side** on the point estimate, **18.8** at the 95% lower bound on the win rate.

---

Tick tolerance is a property of the era, not of the strategy: NQ's tick is fixed at 0.25 points while the instrument rose roughly tenfold, so the stop grew about eightfold in ticks. The invariant unit is fraction of R lost. **Plan against the lower bound.**

No figure in this repository is net of slippage. The fill remains unmeasured.
