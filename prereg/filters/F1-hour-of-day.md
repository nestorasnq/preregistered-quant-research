# F1 — Hour of day

**Verdict: FAILED.** Three independent methods agree, and the pre-registration predicted the failure
mode before the data was seen.

## Hypothesis

Trades that fire in particular hours outperform. Some hours carry structurally different flow —
scheduled data releases, cash opens, session handovers — and a liquidity sweep at 08:30 New York is
a different event from one at 03:00.

## Fixed before collection

The design here is the one worth reading, because the multiplicity problem was anticipated rather
than discovered.

**Hours were split into two tiers in advance.** Tier 1 was ten hours named for a stated mechanism —
cash opens, the 08:30 ET macro slot, London close, FOMC. Tier 2 was the full 23-hour scan, reported
in full, nothing hidden.

**Tier 2 hours had to clear four criteria, not one.** The first was a permutation test on the **max
statistic**: shuffle the hour labels across trades, recompute the best hour's expectancy, 10,000
times. That asks the right question — not "is this hour good?" but "is the best of 23 better than
the best of 23 random relabellings?"

**And the pre-registration wrote down what a null result would look like:**

> With 23 buckets at ~30 trades each and no edge anywhere, the best hour still shows ~61% and
> roughly one clears p < 0.05.

That sentence was written before the scan ran.

## Result

**Tier 2, the max statistic:**

```
observed best hour       13:00 CT, +0.5500 R (n = 20)
null best-of-23          median +0.6000   95th pct +1.0000
corrected p              0.6288
```

**The observed best hour is below the median of the noise distribution.** Pure chance typically
hands you a best hour of +0.60 R across 23 small buckets. The data produced +0.55 R. Restricted to
the five hours with n ≥ 30, corrected p = 0.7340.

**And the prediction landed exactly.** Among the 13 unanchored hours, **exactly one cleared
p < 0.05 uncorrected** — 21:00 CT at p = 0.0461 — against an expectation of 13 × 0.05 = 0.65.

**Tier 1, the anchored set:** 10 hours, 60% of trades. **56.5% against 57.6% for the unanchored
hours.** The named mechanisms did worse than the hours with no story attached.

**The fold experiment:** ten train/test splits, selecting the best hour in-sample and testing it
out-of-sample. The selected hour beat no-filter in **2 of 10 folds**. Median out-of-fold expectancy
**−0.1203 R against +0.0462 for no filter**. Median in-fold to out-of-fold decay: **+0.4730 R per
trade.** Every fold picked an hour worth +0.28 to +0.47 in training that returned roughly −0.12.

**Replication on gold:** omnibus across all hours, **p = 0.237**. Nothing.

## Ruling

Closed on three instruments and three methods. No hour filter.

## Two things recorded against the study's own interest

**The anchor list contained its own biggest loser.** NY 2 — the 09:30 ET cash open, as *a priori*
justifiable as any hour on the list — came back at **n = 63, 42.6%, −0.127 R**, the largest bucket
in the study. A list assembled by looking at the data would not contain that. The Tier 1 prior was
honestly specified, which is the only reason its one surviving member was allowed to skip the
max-statistic penalty.

**One stability criterion was untestable and was scored as a failure anyway.** Criterion 3 required
an hour to be positive in a majority of years with n ≥ 5. **Seventeen of 23 hours have no such year
at all.** A criterion most hours cannot attempt does not discriminate between them. It was scored
`0/0` as fail, not pass — a hypothesis that cannot demonstrate stability has not demonstrated it —
and it was not relaxed, because it was frozen before the numbers.
