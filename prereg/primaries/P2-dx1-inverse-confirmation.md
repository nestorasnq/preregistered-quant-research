# P2 — DX1! inverse confirmation

**Verdict: FAILED on replication.** The most instructive result in the campaign.

## Hypothesis

The dollar index is inversely related to risk assets. When DX1! is in a state that confirms an
index entry's direction — dollar weakening into a long, strengthening into a short — that entry
outperforms the unfiltered set.

**Why it was worth testing.** The inverse dollar/risk relationship is one of the most widely
observed regularities in macro markets, and it has a mechanism: dollar liquidity conditions drive
risk appetite, and a failed breakout at a higher-timeframe level is a liquidity event. If the
dollar is confirming, the sweep is more likely to be genuine rather than noise.

## Fixed before collection

| | |
|---|---|
| test | ISO-week-clustered resampling, filtered against unfiltered |
| α | fixed before collection |
| **replication requirement** | the effect must reproduce on hosts other than the one it was discovered on |
| drawdown rule | risk% derived from bootstrapped DD95 over a 3-year horizon |

The replication requirement is the part that matters, and it was fixed in advance rather than
added after the primary passed.

## Result

**The primary passed at p = 0.0312.**

Then it was replicated across five host instruments:

| host | effect |
|---|---|
| discovery host | positive |
| FDAX1! | **−8.04 pp** |
| Z1! | **−5.03 pp** |
| **five-host weighted mean** | **−0.19 pp** |

The effect ran from +8.31 to −8.04 across hosts. Pooled across all five it is indistinguishable
from zero.

## Ruling

**Retired.** A number that cleared its own pre-registered threshold was discarded because
replication reversed it.

## Two things this study produced beyond its own verdict

**Replication beats a tighter threshold.** A more conservative α would not have caught this — it
passed at 0.0312 and would have passed at 0.01 on a slightly different draw. What caught it was
testing it somewhere else. Every subsequent primary in the campaign was given a multi-instrument
structure because of this result.

**A drawdown methodology error was found and fixed.** The original analysis measured drawdown with
a moving window over a single realised path, which re-measures the same drawdown repeatedly and
inflates the result. It turned a real 0.592%/yr into 0.936%/yr. The block-bootstrap specification
used everywhere in this campaign was written to make that error impossible, and it is named
explicitly in the D1/H4 pre-registration so it cannot recur.
