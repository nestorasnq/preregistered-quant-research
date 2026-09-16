# Pre-registration Register

Thirteen studies. One file each. Every one records what was predicted, what was fixed **before**
data collection, and what the data returned.

## The tally

| | studies | confirmed |
|---|---|---|
| **Primary hypotheses** | 4 | **0** |
| **Filters** | 8 | **0** |
| **Parameters** | 3 | 1 positive, 1 closed, 1 unanswerable |

Two studies produced positive findings. Neither was the finding its own hypothesis predicted.

## Primaries — [`primaries/`](primaries/)

| ID | Hypothesis | Type | Verdict |
|---|---|---|---|
| [P1](primaries/P1-esnq-correlation.md) | ES/NQ correlation state predicts outcome | filter | **FAILED** — +2.76 pp, p = 0.172, and applying it costs 31.5% of annual return |
| [P2](primaries/P2-dx1-inverse-confirmation.md) | DX1! inverse state confirms index entries | filter | **FAILED on replication** — passed at p = 0.0312, then reversed across five hosts |
| [P3](primaries/P3-d1h4-robustness.md) | The rules survive a timeframe change to D1/H4 | parameter | **FAILED** — 896 trades, p = 0.168, +0.58%/yr against the book's ~8.7 |
| [P4](primaries/P4-gc1-portfolio-addition.md) | CME gold improves the book per unit of drawdown | portfolio | **FAILED** — −0.04%/yr against a required +1.00 |

## Secondary — [`secondary/`](secondary/)

| ID | Hypothesis | Verdict |
|---|---|---|
| [S1](secondary/S1-bias-agreement.md) | Entries agreeing with higher-timeframe regime outperform | **FAILED** — and the effect *peaked at five days stale*, which no mechanism can produce |

## Filters — [`filters/`](filters/)

Eight hypotheses, zero confirmed. Four of them are attempts at the same underlying idea, so the
family was **also closed at the family level with an omnibus**, because testing enough members of a
family guarantees one will clear a threshold.

| ID | Filter | Verdict |
|---|---|---|
| [F1](filters/F1-hour-of-day.md) | Hour of day | **FAILED** — best hour sits *below* the median of the noise distribution |
| [F2](filters/F2-session-anchors.md) | Session anchors | **FAILED** — three instruments, two asset classes |
| [F3](filters/F3-h4-position.md) | Position in the higher-timeframe candle | **FAILED** — signs split, and the variable was mis-defined twice |
| [F4](filters/F4-liquidity-window.md) | Liquidity window | **CONTRADICTED** — the illiquid blocks are the good ones |
| [F5](filters/F5-scheduled-events.md) | Scheduled-event anchors | **FAILED** — the only filter to clear the bar was 98% contained in one that hadn't |
| P1, P2, S1 | *(listed above — filters by type, primaries and secondary by status)* | |

## Parameters — [`parameters/`](parameters/)

| ID | Study | Verdict |
|---|---|---|
| [PR1](parameters/PR1-entry-timeframe.md) | Entry-timeframe neighbourhood, M48 / M50 / M60 | **Flat island — a positive finding.** Three values inside 2.8 pp across 872 trades |
| [PR2](parameters/PR2-target-geometry.md) | Wider-than-1:1 targets | Unanswerable on censored data, then **closed** |
| P3 | *(listed above)* | |

## Filter or parameter?

A **filter** evaluates a condition at entry and discards trades from a set the engine already
produced. A **parameter** changes what the engine finds.

The distinction decides which prior record applies to a new idea, and it is the test for whether a
proposal has quietly become something already closed. A management rule that lets winners run past
the target is not a management rule — it is a wider target, which is closed.

## The protocol

Written down before a single chunk was collected, and unchangeable afterwards:

- the hypothesis, stated so that it could fail
- the significance threshold, and for filters a **null calibration**: random thinning at the measured
  retained share. *Any result that does not beat its own null is discarded regardless of p-value*
- the test statistic and the clustering unit
- the decision rule, including what a pass would and would not authorise
- a **minimum sample floor**, below which the verdict is INCONCLUSIVE rather than FAIL
- handling of ambiguous outcomes, declared in advance
- a **look ledger** — every outcome-touching query counted, so the final claim can be corrected for
  all of them. One look at each out-of-sample block, ever

Two of these did real work that a threshold alone would not have.

**The floor** keeps *"we could not tell"* separate from *"it does not work."* One study closed on
cost rather than evidence and is recorded that way; another had 896 trades against a floor of 353
and its failure is a real answer.

**The null calibration** is what killed the bias-agreement filter — a +3.60 pp effect that random
subsetting matches 11.72% of the time — and what killed the position filter's surviving leg, whose
observed value sat *exactly* on the 95th percentile of 5,000 random re-labellings.

## What a rejection means here

Nothing in this register was abandoned because it looked unpromising. Each was specified, collected,
tested against a threshold fixed in advance, and closed with the result on record.

The standing verdict, frozen 2026-08-19 on in-sample data with the out-of-sample block untouched:

> **FROZEN RULE: NO FILTER.** Trade the engine as-is.
