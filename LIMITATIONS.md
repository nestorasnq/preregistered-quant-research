# Limitations

Everything this research does not establish, in one place, stated as plainly as the findings are.

A backtest is a claim about the past made under assumptions. The assumptions are listed here so a
reader does not have to reconstruct them.

---

## 1. Nothing here has traded

No live execution. No paper execution. No broker connection. Every figure in this repository is the
output of a simulation over historical data.

This is research, and it is described as research throughout. Where the word "book" appears it means
the three-instrument set the campaign settled on, not a funded account.

---

## 2. No return figure is net of execution slippage

The largest single uncertainty in the project, and it is unmeasured.

Commissions, spreads and rolls are modelled at **0.048 R** and are broker-sourced. Slippage is not a
fee — it is the difference between the price that triggered an order and the price that filled it.
This strategy enters on a resting stop and exits on a stop, so **both sides are adversely selected
by construction**: a stop fills while price is moving through the level, against you.

**Every return, win rate and drawdown here is therefore a ceiling.**

Tolerance is regime-dependent and this was itself a correction to the project's own headline figure:
in the 2011–2017 regime the edge died inside **two ticks per side**; in the 2022–2026 regime it
survives roughly **45 ticks on the point estimate and 19 at the 95% lower confidence bound**. The
difference is not improvement in the strategy — NQ's tick stayed at 0.25 points while the instrument
rose roughly tenfold, so the stop grew about eightfold in ticks. See the README for the full
derivation.

The correct unit is fraction of R lost, not tick count. The measurement remains outstanding.

---

## 3. ES1! is not distinguishable from break-even on its own

Block-bootstrapped over ISO-week clusters, 20,000 resamples, stable across four seeds:

| Instrument | Resolved | Win rate | 95% CI | Break-even | Edge at 95% LCB |
|---|---|---|---|---|---|
| ES1! | 694 | 56.65% | [52.14, 61.04] | 53.00% | **−0.86 pp** |
| NQ1! | 721 | 61.46% | [57.16, 65.75] | 52.81% | +4.35 pp |
| NK2251! | 615 | 61.00% | [56.67, 65.29] | 52.73% | +3.94 pp |
| **Book** | **2,030** | **59.75%** | **[57.20, 62.29]** | **52.85%** | **+4.36 pp** |

The pooled book clears break-even at 95% confidence. **ES1! individually does not.** It is carried
by the other two legs. Any reading of the headline consistency figures should carry this: the
smoothness is a portfolio property, not a property of each instrument.

---

## 4. Returns and drawdowns scale together

A sizing figure quoted without its drawdown is meaningless. Doubling risk per trade does not produce
a better strategy, it produces the same strategy at twice the leverage.

| Risk/trade | Return/yr | Expected max DD (95th pct, 3-yr) | 99th pct |
|---|---|---|---|
| 0.50% | +7.91% | 10.9% | ~14.2% |
| 1.00% | +15.81% | 21.7% | ~28.3% |

The 99th percentile figures carry resampling noise of a few tenths of an R and should not be read to
three significant figures. Across five seeds at 10,000 resamples the 99th percentile ranges 28.3 to
28.8 R; at 50,000 resamples it is 28.3 R.

---

## 5. The consistency record is a pooled result

Fifteen of sixteen years positive is a property of the three-instrument book. Individual instruments
have sub-break-even years. Pooling across correlated-but-not-identical index futures is what
produces the smoothness — which is a real finding about diversification, not a claim that each leg
is independently robust.

---

## 6. Every result is conditioned on a fixed chart timeframe

The engine is stateful from bar 0 and reads three timeframes simultaneously. The chart timeframe on
which it is evaluated is part of the specification, and changing it changes the trade set. Results
are not timeframe-invariant and are not claimed to be.

The parameter-island finding tests the neighbourhood of the *entry* timeframe specifically —
three values inside 2.8 percentage points across 872 trades — and does not generalise to arbitrary
chart configurations.

---

## 7. The era win-rate gap is unexplained

NQ1! returned 56.84% over 2011–2017 and 64.30% over 2018–2026: a difference of +7.47 pp, **95% CI
[−1.20, +16.13], P(difference ≤ 0) = 0.046.**

One-sided this is marginal; two-sided the interval crosses zero. It is **suggestive, not
established**, and nothing in this repository is built on it. It does mean the full-sample estimate
blends two visibly different regimes, which is worth knowing when reading any single pooled number.

---

## 8. The dataset carries known gaps

The published ledger is the campaign's own record. It is short approximately **27 book trades**
against the engine's full output, from chunk-boundary reconstruction during data assembly.

Those absences are **not random** — they cluster at chunk boundaries, which are specific moments in
time. Spread across 2,030 trades and sixteen years this has no material effect, and the year table
reproduces exactly. **On small subsets it does.** An earlier tier comparison on this data showed
+14.43 against +1.93 and collapsed to +10.35 against +6.29 (p = 0.604) once the gaps were closed.

**Aggregate figures here are sound. Any future subset analysis on this ledger is not, without
re-export.**

Separately, in the source export the `entry` column is blank for all ES1! rows and corrupt for NQ1!.
Neither column is published. ES1! stop geometry cannot be derived from the current export at all.

---

## 9. Statistical caveats

**Block bootstrap is not a significance test for every question.** ISO-week clustering handles
within-week dependence. It does not handle longer-horizon regime persistence, and a strategy whose
edge varies by market regime will have intervals that are still somewhat optimistic.

**Twelve hypotheses were tested.** Each was pre-registered with its threshold fixed in advance, and
none was confirmed, so no multiple-comparison correction is load-bearing here. Had one passed, it
would have needed one — which is precisely what happened to the DX1! result at p = 0.0312, where
replication rather than correction is what retired it.

**The parameter island is evidence against overfitting, not proof of its absence.** Three
neighbouring values clustering tightly is consistent with a genuine effect and also consistent with
a broad but spurious one.

---

## 10. What is not published

The strategy implementation, its entry and exit logic, its signal specifications and all price-level
data. The research continues and the implementation remains private.

This means the central claims here **cannot be independently replicated from source**. They can be
recomputed from the published ledger, which is a weaker guarantee and is stated as such. A reader is
being asked to accept that the ledger is an honest record of what the engine produced. The
validation protocol in `docs/02-validation-protocol.md` describes how that record was verified
internally; it is not a substitute for open source.

---

## 11. This was a solo project

One researcher, self-imposed discipline, no independent reviewer. The pre-registration protocol
exists specifically to substitute for external oversight, and the defect register records what it
caught — including two analysis errors that flipped conclusions and were found in self-review.

That is a real substitute, not an equivalent one.
