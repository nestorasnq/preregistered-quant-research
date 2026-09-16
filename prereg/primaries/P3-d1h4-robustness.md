# P3 — D1/H4 timeframe robustness

**Verdict: FAILED.** Tested at adequate sample, closed on evidence.

## Hypothesis

The rules survive a timeframe change. Pooled win rate across ES1! and NQ1! at chart H1 /
entry TF 240 / higher TF D1 exceeds the 1:1 break-even including cost.

**Why it was worth testing.** The originating idea is structural — liquidity sweeps and failed
breakouts at higher-timeframe levels. If that description is correct, the behaviour is not a
property of any particular timeframe; it should appear wherever a higher-timeframe level exists to
be swept. A rule set that works only at one scale is more likely to be fitted to that scale than
to be describing a market mechanic.

This was the campaign's most direct test of whether the originating hypothesis was true.

## Fixed before collection

| | |
|---|---|
| test | one-sided, pooled at trade level across both instruments |
| **α** | **0.01** |
| break-even | `p* = (1 + c) / 2`, with `c = fixed_cost_points / median(stop distance)` per instrument per era — a formula, not a number |
| **binding condition** | pooled clears `p*` **AND** neither instrument's point estimate sits below `p*` |
| p-value | ISO-week block bootstrap, 10,000 resamples |
| cross-check | design-effect-corrected one-sided binomial |
| **minimum n** | **353 resolved pooled.** Below it, INCONCLUSIVE — not FAIL |
| ambiguous outcomes | excluded from the test, **also reported counted as losses**. Verdict disagreement between the two ⇒ INCONCLUSIVE |
| era split | descriptive only, never a gate |

Three details worth noting because they cut against the tester's own interest:

**The cost correction lowered the bar.** At D1/H4 the stop distance is several times larger while
commission and spread stay fixed in points, so `c` falls and the break-even falls with it —
roughly 52.4% to ~50.6%. Recomputing it cut the required sample by 38%. The bar was being held too
high, and fixing that was the single most pro-hypothesis decision in the document.

**α stayed at 0.01.** It had been pre-registered at 0.01 before anyone knew the study might
struggle to clear it. Loosening it afterwards is the exact post-hoc move that makes
pre-registration meaningless, so it stayed.

**The both-legs condition was added deliberately, at a known cost.** Roughly 2 percentage points of
power, because every failure in the campaign to that point had been carried by one instrument while
the other contributed nothing.

## Result

**896 resolved trades, 2000–2026 — comfortably above the floor.**

| | |
|---|---|
| pooled win rate | 53.39% |
| break-even | 51.45% |
| **p** | **0.168** |
| 95% lower confidence bound | 50.07% |
| drawdown-adjusted return | **+0.58%/yr** against the book's ~8.7%/yr |

## Ruling

Closed on evidence, not on cost. The sample was adequate and the answer was no.

The drawdown-adjusted figure is the decisive one. Even taking the point estimate at face value and
ignoring the p-value entirely, D1/H4 returns about a fifteenth of what the existing book returns
per unit of drawdown. There is no version of this result that puts it in the book.

**What it means for the originating hypothesis:** the rules did not transport to a four-times-slower
timeframe. That is evidence against the strongest form of the structural claim. It does not
establish that the edge is fitted — the parameter island points the other way — but it bounds how
general the mechanic can be said to be.
