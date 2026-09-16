# F3 — Position inside the higher-timeframe candle

**Verdict: FAILED.** The most error-prone study in the campaign, and the one that produced the most
durable procedural lesson.

## Hypothesis

Entries firing in the **first** hourly candle of a fresh four-hour candle (`h4_pos = 0`) outperform
those firing in the other three positions.

**Why it was worth testing.** A fresh higher-timeframe candle is where the previous candle's range
becomes a reference level and where the structure the engine reads is newest. If the engine keys on
higher-timeframe structure, the moment that structure refreshes is a plausible place for its edge to
concentrate.

## The variable was mis-defined twice, and both were caught

**ES1! used `utc_hour mod 4`.** ES1!'s four-hour candles anchor to the 17:00 Chicago CME rollover,
not to UTC midnight. The variable was **wrong on 694 of 694 rows** — roughly half the dataset
mislabelled in a way that no statistic could detect. The verdict was **withdrawn**, not corrected,
and the hypothesis reopened.

**Gold's first batch was off by one position** for the same class of reason.

The rule written afterwards: **build the anchor from each instrument's own measured
higher-timeframe boundaries, never from a clock you assume.** Gold anchors at 18:00 New York, ES1!
at 17:00 Chicago — the same instant, the CME rollover. For any new instrument the boundary must be
**measured from timestamp logs before the variable is built.**

This is a data-definition failure, not a statistical one, and it is the kind that produces a
confident wrong answer rather than an error.

## A blocking gate that preceded the statistics

`h4_pos = 0` is the first hour of a fresh candle — **exactly where a look-ahead defect would bite.**

A real early-candle edge and an engine seeing its own future produce **the same signature**. Two
instruments showed that signature. So a targeted simulation was made blocking:

> The targeted sim must run and clear **before any position rule is frozen or traded**, regardless
> of what the statistics show. If the edge is an artefact of the engine seeing its own future, no
> amount of out-of-sample confirmation makes it tradeable — it will not exist live.

A statistical pass cannot clear a mechanism you suspect. That ordering — mechanism gate first,
statistics second — is the point.

## Results

**Gold, P2:** blocks +16.1 / +14.6 / +0.9 / −12.0 → **3 of 4**, short of the 4-of-5 bar.
p = 0.173, confidence interval spanning zero. **Failed Holm.** A later re-analysis against the rest
of the book found the differential **essentially zero**.

**EURUSD + NQ1!, H2:**

| | cell 0 | rest | difference | bootstrap 95% | beats its null? |
|---|---|---|---|---|---|
| EURUSD | n=198, **46.97%** | n=709, 56.70% | **−9.73 pp** | [−17.49, −2.19] | **yes**, p = 0.015 |
| NQ1! | n=162, **67.28%** | n=453, 59.38% | **+7.90 pp** | [−0.77, +16.33] | **no**, p = 0.097 |
| pooled | | | −1.76 pp | [−7.51, +3.98] | |

**On EURUSD the first hour is nearly ten points worse. On NQ1! it is nearly eight points better.**
The pre-registered sign-consistency requirement fails 1 of 2.

And the second rule kills it independently: NQ1!'s +7.90 pp **does not beat its own null.** The 95th
percentile of 5,000 random re-labellings is 7.90 pp — the observed value sits exactly on it.

**Only EURUSD's effect beats its null, and it points the wrong way.**

## Ruling

Closed. No position filter.

## The lesson worth more than the verdict

A variable you did not measure is a variable you do not have. Two studies assumed a clock, and one
of them produced a full set of statistics on a column that was wrong on every row.

The defence was not more care. It was a rule: **measure the anchor from the instrument's own
timestamps before building the variable**, and treat an assumed definition as an untested assumption
rather than as background knowledge.
