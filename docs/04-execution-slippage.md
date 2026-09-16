# Execution and Slippage

## In plain words

Every number in this repository assumes I got the price I asked for. In real trading, you often
don't.

**Slippage is the difference between the price that triggered your order and the price you actually
got.** You wanted to buy at 100. By the time your order reached the exchange, the market was at
100.25. You paid a quarter more than the plan.

This matters here more than it does for most strategies, for a reason built into how the strategy
works. It gets in on a **stop order** and gets out of losers on a **stop order**. A stop order fires
*while price is moving through your level* — which means it fills at whatever is available on the
other side, and the other side is moving away from you. **Both ends are working against you by
design.**

Nobody can tell you this number in advance. Your broker will quote you commissions and spreads,
because those are on a price list. Slippage is not on any price list. It is a thing that happens to
you and you find out afterwards.

**So I built the tool to measure it, and I have not measured it yet. That is the biggest hole in
this entire project and I am not going to pretend otherwise.**

---

## The distinction that gets glossed over

| | what it is | can you know it in advance? |
|---|---|---|
| Commission | a fee per contract | **Yes** — the broker publishes it |
| Spread | the gap between buy and sell price | **Yes** — observable |
| Roll | cost of moving to the next contract month | **Yes** — observable |
| **Slippage** | the gap between trigger price and fill price | **No** — an outcome, not a fee |

The first three are modelled at **0.048 R**. The fourth is not modelled, because it cannot be
modelled from a fee schedule. Saying "costs are included" while omitting slippage is the most common
way a backtest overstates itself.

## R, ticks, and why the unit matters

**One R is the distance from the entry to the stop.** It is the unit of risk. Every result here is
in R, so a win is +1 R and a loss is −1 R.

**A tick is the smallest amount a price can move.** On NQ it is 0.25 index points, and it has been
0.25 forever.

So the real question is: **how big a bite does one tick take out of one R?**

That depends entirely on how many ticks wide the stop is. And that has changed by an order of
magnitude.

| Year | NQ price | Median stop | Stop in ticks | One tick costs |
|---|---|---|---|---|
| 2011 | ~2,300 | 12.00 pts | 48 | **2.08% of R** |
| 2014 | ~4,000 | 9.62 pts | 38 | 2.60% of R |
| 2017 | ~6,000 | 16.00 pts | 64 | 1.56% of R |
| 2020 | ~11,000 | 87.50 pts | 350 | 0.29% of R |
| 2023 | ~15,000 | 66.50 pts | 266 | 0.38% of R |
| 2026 | ~25,000 | 230.00 pts | 920 | **0.11% of R** |

The instrument went up roughly tenfold. The stop scaled with it, because a stop is a distance in the
market. **The tick did not scale.** It is still 0.25 points.

**So the same one tick of slippage does about nineteen times less damage in 2026 than it did in
2011.** Nothing about the strategy improved. The ruler stayed the same size while the thing being
measured grew.

## The correction this project had to make to itself

The headline figure carried for most of this campaign was: **the entire edge disappears at 1.5 ticks
per side.**

Every number behind that was arithmetically correct. The 2011–2017 median stop is 12.75 points —
exactly 51 ticks — and that is the table the figure came from.

**The label was wrong.** It described the strategy *in 2011–2017* and was carried as though it
described the strategy. Recomputing it from the published ledger is what surfaced it.

This is the same mistake as two earlier errors in the campaign, where a figure computed on one slice
of time was compared against a baseline from another. It is in the [defect register](06-defect-register.md)
for that reason. All three are the same failure: **a number measured on one subset, carried as a
property of the whole.**

## Where it actually breaks

**2011–2017** — stop 51 ticks, win rate 56.84%:

| Ticks/side | Total cost | Break-even | Edge remaining |
|---|---|---|---|
| 0.0 | 0.0480 R | 52.84% | **+4.00 pp** |
| 1.0 | 0.0872 R | 55.16% | +1.68 pp |
| 1.5 | 0.1068 R | 56.32% | +0.51 pp |
| **2.0** | 0.1264 R | 57.48% | **−0.65 pp — gone** |

**2022–2026** — stop 396 ticks, win rate 66.15%:

| Ticks/side | Total cost | Break-even | Edge remaining |
|---|---|---|---|
| 0 | 0.0480 R | 52.83% | **+13.32 pp** |
| 10 | 0.0986 R | 55.81% | +10.34 pp |
| **19** | 0.1441 R | 58.50% | **+7.66 pp — the planning point** |
| **45** | 0.2756 R | 66.25% | **−0.10 pp — gone** |

**Break-even win rate** is the win rate at which you make exactly nothing. On a 1:1 target with no
costs it is 50%. Costs push it up twice as fast as the cost itself, because you pay on winners and
losers alike. Break-even trades push it up further — they realise nothing but still pay the fee.

## What to plan against

**Nineteen ticks per side, not forty-five.** The lower confidence bound, not the point estimate.

**And stop thinking in ticks.** The tick count is not stable — it will drift again as the instrument
moves. The stable unit is fraction of R: today one tick per side costs about 0.5% of R.

## Three things this does not fix

**The measurement still does not exist.** More tolerance is not a measured fill.

**Some of the extra room is illusory.** Stops widened because volatility rose, and fast markets fill
stops worse. Part of the additional tolerance is consumed by the very thing it protects against.

**No return figure anywhere in this repository is net of slippage.** Every one is a ceiling.

## The instrument that was built to close it

An intrabar alert layer that fires the moment price crosses the trigger, naming the exact entry,
stop and target levels **at the moment of the event**. The difference between those levels and a
real broker fill *is* the number.

It reaches 94.9% of trades with advance warning, up from 68.7%.

**The instrumentation is complete. The measurement is not.** Two weeks of live alert validation
produces it, and that is the next step in the plan — not as a precursor to a slippage study, but
*as* the slippage study.
