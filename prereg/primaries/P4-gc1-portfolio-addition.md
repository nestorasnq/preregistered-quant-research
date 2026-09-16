# P4 — CME gold as a portfolio addition

**Verdict: FAILED.** And it produced the campaign's most useful by-product.

## Hypothesis

Adding GC1! to the three-index book improves the portfolio on a drawdown-adjusted basis by at least
1.00 percentage point of annual return at the 10% drawdown limit.

**Why it was worth testing.** The book is three equity index futures, which are correlated by
construction. Gold is the obvious diversifier: a different driver, a different session profile, and
a history of moving against risk assets when it matters most. If the rules work on gold, the
portfolio effect should be larger than the standalone edge, because the correlation is lower.

**Why the threshold was +1.00 and not zero.** A new instrument costs data, monitoring, execution
complexity and one more thing to get wrong. An improvement inside the noise is not worth that.
Setting the bar above zero before collection is what stops a marginal result from being argued into
the book afterwards.

## Fixed before collection

| | |
|---|---|
| requirement | **≥ +1.00%/yr** drawdown-adjusted improvement |
| weights tested | a declared grid, fixed in advance |
| drawdown | ISO-week blocks, 10,000 resamples, 95th percentile of maximum drawdown over a 3-year horizon |
| sizing | `risk% = 10 / DD95`, then `%/yr = risk% × R/yr` |
| data | CME futures, not the retail spot feed |

## Result

**999 resolved trades on CME data, 2011–2026.**

| weight | drawdown-adjusted improvement |
|---|---|
| 0.25 (best of the declared grid) | **−0.04%/yr** |
| 95% lower bound at that weight | **−2.96%/yr** |
| 0.15 (post-hoc optimal) | +0.03%/yr |

Against a requirement of +1.00.

## Ruling

Closed. Gold is not added to the book.

The post-hoc optimal weight is recorded because leaving it out would be dishonest, and it changes
nothing: +0.03%/yr is inside the noise, it was found by searching the grid after seeing the
outcomes, and it still misses the threshold by a factor of thirty.

## The by-product

This study's hypothesis failed. Its data produced the campaign's strongest positive finding.

Running the engine on CME gold futures required a second, independent price source for an
instrument the campaign already had retail data on. That comparison had never been possible before,
and one non-exchange feed was load-bearing across the whole campaign.

| source | trades | win rate |
|---|---|---|
| retail aggregator, spot metal | 959 | 54.55% |
| CME futures | 958 | 54.49% |

**Within 0.06 percentage points.** At trade level, 63.0% of futures entries coincide with a spot
entry to the minute, and 94.5% of those resolve identically — the remainder being the basis and the
contract roll behaving as they should.

This is the argument for keeping data from studies whose hypotheses fail. The question the study
was asked returned no. The data answered a different question that mattered more.
