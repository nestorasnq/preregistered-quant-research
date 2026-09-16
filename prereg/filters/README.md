# Filter Studies — eight hypotheses, zero confirmed

A **filter** evaluates a condition at entry time and discards trades from a set the engine already
produced. It thins an existing trade list. That is different from a **parameter**, which changes
what the engine finds in the first place — see [`../parameters/`](../parameters/).

The distinction is not pedantic. It determines which prior record applies to a new idea, and it is
the test for whether a proposal has quietly become a filter while being described as something else.

## The record

| ID | Filter | Verdict |
|---|---|---|
| [F1](F1-hour-of-day.md) | Hour of day | **FAILED** — three independent methods agree |
| [F2](F2-session-anchors.md) | Session anchors | **FAILED** — replicated on three instruments |
| [F3](F3-h4-position.md) | Position inside the higher-timeframe candle | **FAILED** — signs split, and the variable was mis-defined twice |
| [F4](F4-liquidity-window.md) | Liquidity window | **CONTRADICTED** — the illiquid blocks are the good ones |
| [F5](F5-scheduled-events.md) | Scheduled-event anchors | **FAILED** — the best result was a subset of a failed one |
| [P1](../primaries/P1-esnq-correlation.md) | ES/NQ correlation state | **FAILED** |
| [P2](../primaries/P2-dx1-inverse-confirmation.md) | DX1! inverse confirmation | **FAILED on replication** |
| [S1](../secondary/S1-bias-agreement.md) | Higher-timeframe bias agreement | **FAILED** |

## Why the family was closed at the family level

F1 through F4 are four separate attempts at the same underlying idea: that **when** a trade fires
predicts **how** it resolves. Testing them one at a time and reporting a tally invites a
multiplicity problem — test enough members of a family and one will clear any threshold.

So the family was also closed as a family, with an omnibus test that asks whether *any* time
structure exists rather than whether a particular hour does.

| omnibus | p |
|---|---|
| all hours, gold | 0.237 |
| family, coarse granularity | 0.070 |
| family, medium granularity | 0.046 |
| family, fine granularity | 0.483 |

The middle row is the one worth dwelling on. At one granularity out of three the family clears 0.05.
That is what a family-level test is *for*: a member clearing a threshold is not evidence when the
family as a whole does not, and a family that clears at one of three granularities and fails at the
other two has not shown anything.

**No member of this family was ever frozen into a rule.** The standing verdict, frozen 2026-08-19 on
in-sample data with the out-of-sample block untouched:

> **FROZEN RULE: NO FILTER.** Trade the engine as-is. No hour filter, no position filter, no
> session-anchor filter.

## The bar, fixed before any of it

> Beat no-filter in **≥ 4 of 5 independent blocks**, then survive Holm correction across the family.

One filter cleared the block bar. It is documented in [F5](F5-scheduled-events.md), and it died on a
containment check rather than on a p-value.
