# F4 — Liquidity window

**Verdict: CONTRADICTED.** Not merely unconfirmed — the data points the other way.

## Hypothesis

Trades firing in the deepest-liquidity block of the day, 12:00–16:00 UTC, outperform. That window
spans the London/New York overlap, the highest-volume hours in index futures.

**Why it was worth testing.** The strategy keys on liquidity sweeps and failed breakouts. Both are
liquidity events. It is close to self-evident that they should work best where liquidity is
deepest — there is more resting size to sweep, and a failed breakout means more when more
participants were positioned for it.

The mechanism is stronger here than in any other filter in the family. Which is what makes the
result interesting.

## Result

| | win rate |
|---|---|
| 12:00–16:00 UTC, the liquid window | **57.61%** |
| book average | **59.04%** |
| best-performing blocks | **16:00–23:00 UTC — the illiquid hours** |

The filter is **below the unfiltered book**, and the strongest blocks are the ones the hypothesis
predicted would be weakest.

## Ruling

Closed, and recorded as a contradiction rather than a null.

## Why this one is worth publishing

A contradicted hypothesis carries information a null does not.

The most plausible reading is that the engine is not finding its edge where participation is
heaviest, but where a level can be swept without immediately attracting opposing size. That is a
different mechanic from the one assumed, and it is consistent with the whole family's result: the
edge is not concentrated in time-of-day structure at all.

**It is not a finding.** It was not pre-registered as a directional hypothesis in its own right and
no correction was applied to it. It is recorded as an observation that cuts against an assumption
that would otherwise have gone untested — which is the reason to write down contradicted hypotheses
rather than only failed ones.
