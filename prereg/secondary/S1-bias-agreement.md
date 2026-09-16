# S1 — Higher-timeframe bias agreement

**Verdict: FAILED.** Declared as a non-gating secondary to P3 and registered alongside it.

## Hypothesis

Entries whose direction agrees with the prevailing D1/H4 regime bias outperform the unfiltered set.

**Why it was worth testing.** "Trade with the higher-timeframe trend" is close to universal advice,
and it has a plausible mechanism: a sweep that resolves in the direction of the dominant flow should
find less opposing liquidity than one that fights it.

## Fixed before collection

| | |
|---|---|
| status | **non-gating** — the primary does not depend on it either way |
| α | **0.01**, same as the primary |
| comparison | **exactly one** — filtered versus unfiltered pooled rate. No ladder, no tiers, no per-instrument selection |
| control | **random thinning at the measured retained share**, 10,000 draws |
| clustering | ISO-week blocks |
| n floor | the join's warm-intersection sample, declared before the test ran |

Two constraints here are worth spelling out, because both exist to prevent a specific abuse:

**One comparison, declared in advance.** A bias filter admits a ladder of variants — strict
agreement, partial agreement, per-instrument thresholds. Testing several and reporting the best is
how a null becomes a finding. One comparison was fixed.

**The random-thinning control.** Any filter that removes trades changes the sample. Comparing the
filtered set against the unfiltered set therefore compares different sample sizes, and a smaller
sample is noisier in both directions. The control asks the only question that matters: does this
filter beat **randomly discarding the same number of trades**?

## Result

**+3.60 percentage points pooled, p = 0.134.**

The random-thinning control was decisive: **a random coin-flip subset matches the filter's
performance 11.72% of the time.** Roughly one time in nine, discarding trades at random does as
well as the rule.

And then the mechanism check, which is the part worth reading:

**The effect peaked at five days stale.**

The regime bias was lagged by increasing amounts and the spread re-measured:

| lag applied to the regime | spread |
|---|---|
| 0 h — fresh | +3.60 pp |
| 24 h | +4.92 pp |
| 48 h | +6.25 pp |
| **120 h — five days stale** | **+7.72 pp ← strongest** |
| 240 h | +5.38 pp |
| 720 h | −4.17 pp |

**The effect gets stronger as the information gets worse.** A regime you learned five days late
cannot predict better than the one you knew at the time. No mechanism can produce that shape.

That table is worth more than any p-value in this study. It is mechanism-free, needs no
distributional assumption, and it is unambiguous.

### One more thing the data showed about selection

Three versions were computed. The pre-registered one was the pooled test.

| version | spread | p | coin-flip subset matches it |
|---|---|---|---|
| **Pooled ES1!+NQ1! — as pre-registered** | **+3.60 pp** | 0.134 | 11.72% |
| NQ1! only | +5.71 pp | 0.086 | 8.99% |
| ES1! only | +1.83 pp | 0.340 | 36.13% |

The single-instrument version looks better than the one that was registered. **That gap is the
top-draw effect, measured: choosing the better leg after seeing it buys +2.11 pp of pure
selection.** This is exactly why the comparison was fixed to one, in advance.

## Ruling

Closed. The statistics said "not significant." The mechanism said "artifact." They agreed.

**The general lesson, recorded because it applies beyond this study:** a result that is statistically
marginal *and* mechanistically impossible is not a weak finding — it is a clean negative. Checking
whether an effect's shape is physically possible is cheap, and it settles questions that p-values
leave open. Every subsequent study in the campaign carried a mechanism check for this reason.
