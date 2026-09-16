# F2 — Session anchors

**Verdict: FAILED.** Tested on an index future, a metal and a currency pair. Same answer each time.

## Hypothesis

Trades taken in an instrument's home prime session outperform those taken in its off hours.

**Why it was worth testing, repeatedly.** This is not folklore. The London/New York overlap, the
LBMA auctions, the 16:00 WMR fix and the cash opens are documented structural features with real
volume signatures. If liquidity sweeps mean anything, they should mean more where the liquidity is.

**And a negative on one instrument was explicitly refused as a verdict.** After ES1! came back
negative, the ruling recorded was:

> ES gave a **prior**, not a verdict: hour filtering fails on a 23-hour index future with weak
> session boundaries. FX and metals are different animals.

So it was re-tested on gold, then on EURUSD, each time as a **single pre-specified hypothesis**
rather than a scan — a stronger design than the one ES1! got.

## Fixed before collection

| | |
|---|---|
| bar | beat no-filter in **≥ 4 of 5 independent blocks** |
| null control | random re-labelling, 5,000 draws. **Any result that does not beat its own null is discarded regardless of p-value** |
| sign consistency | the effect must point the same way on both instruments |
| correction | Holm across the family |

## Results

**ES1!** — Tier 1 anchored set, 10 hours, 60% of trades: **56.5% against 57.6% unanchored.**

**Gold — P1, tier-1 anchors:** blocks −9.8 / −2.9 / +1.3 / −8.6. **1 of 4.** Negative, replicating ES.

**EURUSD + NQ1! — H1, home prime vs off hours:**

| | prime | off | difference | bootstrap 95% | null p |
|---|---|---|---|---|---|
| EURUSD | n=178, 54.49% | n=416, 52.40% | +2.09 pp | [−6.50, +10.91] | 0.651 |
| NQ1! | n=76, 61.84% | n=276, 62.32% | **−0.48 pp** | [−13.32, +11.83] | **1.000** |
| pooled | | | +1.26 pp | [−5.93, +8.45] | |

NQ1!'s null p of **exactly 1.000** means every one of 5,000 random re-labellings produced a
difference at least as large as the real one.

## Ruling

Closed on three instruments across two asset classes. No session filter.

**What it is actually evidence for, stated positively:** the engine's edge is *not* concentrated in
session anchors — not on an index future, not on a metal, not on a currency pair. That is the
cleanest positive statement the study produced, and it is more useful than a filter would have been.
It means the mechanic the engine keys on is not a session-liquidity artifact.
