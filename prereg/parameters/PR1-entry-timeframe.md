# PR1 — Entry-timeframe neighbourhood

**Verdict: the island is flat.** One of the campaign's two positive findings, and it says something
the headline numbers cannot.

## Why this study exists

The entry timeframe was chosen ***a priori*** — an hour, because an hour is a unit market
participants act on — rather than selected by searching a grid for the best value.

That is the right way to choose a parameter, but it leaves a question open. A result sitting on a
sharp peak is a fitted artefact whether or not you fitted it deliberately. **The neighbourhood has
to be tested, and it has to be tested after the fact, or the choice proves nothing.**

## Hypothesis

Neighbouring entry timeframes produce materially different results. If they do, the chosen value is
a peak and the edge is a fitting artefact.

Two tests were registered, and they are different claims:

1. **M48 against its own break-even** — is M48 profitable?
2. **M48 against M60, paired** — is M48 *better*?

Only the second bears on what to do next.

## Result — fresh windows, pilot excluded

| | n (W+L) | rate/yr | win rate | break-even | edge | block-boot p | DD95 | DD-adj %/yr |
|---|---|---|---|---|---|---|---|---|
| M60 | 159 | 43.6 | 55.97% | 52.82% | +3.15 pp | 0.2237 | 19.5 R | +1.18 |
| **M48** | 225 | 59.7 | 58.67% | 52.90% | **+5.77 pp** | **0.0479** | 17.2 R | +3.46 |
| paired | | | **+2.69 pp** | | | **z = 0.53** | | |

**The two registered tests disagree.**

- M48 against its own break-even: **p = 0.0479.** A pass at α = 0.05 — by 0.0021, which is one trade
- M48 against M60, paired: **z = 0.53.** Nowhere near

*"M48 is profitable"* and *"M48 is better than M60"* are different claims. The first passed. Only the
second matters, and it failed.

## Result — the full span, which goes the other way

| | n (W+L) | win rate | edge | p | DD95 | DD-adj %/yr |
|---|---|---|---|---|---|---|
| M60 | 223 | **56.05%** | +3.22 pp | 0.171 | 18.1 R | +1.28 |
| M48 | 312 | **54.17%** | +1.22 pp | 0.349 | **25.2 R** | +0.48 |
| paired | | **−1.89 pp** | | z = −0.43 | **39% deeper** | −0.79 |

On all 312 decisive trades, **M48 is worse than M60** — lower win rate, lower drawdown-adjusted
return, and a 39% deeper 95th-percentile drawdown.

### The gap between the two tables, stated plainly

The only difference is the pilot window (2014-09 → 2016-07), where M48 ran 42.53%. It was excluded
because those outcomes had already been seen — **methodologically correct for a confirmatory test,
and it also happens to remove M48's worst stretch.**

Both tables are published for that reason. A confirmatory test on fresh windows is the right design;
a reader is entitled to see what the excluded window does to the answer.

## The island

| configuration | trades (W+L) | win rate |
|---|---|---|
| M60 — the book | 223 | 56.05% |
| M48 | 312 | 54.17% |
| M50 | 337 | 56.97% |

**Three neighbouring timeframes inside 2.8 percentage points across 872 decisive trades.**

## Ruling

**M60 stays.** Not because it won — on the paired test nothing won — but because nothing beat it,
and the incumbent keeps the position when a challenger fails to displace it.

**The flatness is the finding.** A curve-fitted parameter sits on a spike: move one notch and the
edge collapses. This one does not. Three values within 2.8 points across 872 trades is what a real
effect looks like when you probe around it, and it is the strongest available evidence that the
headline result is not an artefact of parameter selection.

## What it does not establish

A flat neighbourhood is **evidence against overfitting, not proof of its absence.** A broad but
spurious effect would also produce a flat island. This result rules out the sharpest failure mode.
It does not rule out all of them.
