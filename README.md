# Pre-registered Quantitative Research

**A multi-instrument backtesting campaign on a systematic intraday strategy, run with the validation discipline of a production system.**

Sixteen years of market data, seven instruments, thirteen pre-registered studies, and a validation protocol that verified every build byte-for-byte against a reference implementation. Every primary hypothesis was rejected, and every filter with them. This repository documents how, and why that is the interesting part.

The strategy implementation is not published. The methodology, the tooling, the pre-registrations, the results and the trade-level outcome data are.

---

## The campaign in numbers

| | |
|---|---|
| Period covered | August 2011 – August 2026 (14.96 years) |
| Instruments tested | 7 — index futures from CME, Eurex, Osaka and ICE, plus two retail feeds |
| Final book | ES1!, NQ1!, NK2251! — **2,030 resolved trades** |
| Pre-registered studies | **13** — 4 primaries, 8 filters, 3 parameters |
| Hypotheses confirmed | **0** across all primaries and filters |
| Inference | ISO-week-clustered block bootstrap, 10,000 resamples, 3-year horizon |
| Build verification | Byte-level reversal match on every build, without exception |
| Python-to-reference parity | 26 / 86 / 28 cases, exact |
| Engine under test | ~4,800 lines, stateful from bar 0, three simultaneous timeframes |

---

## What makes this unusual: it mostly failed

Every hypothesis in this campaign was registered before data collection, with the significance threshold and the decision rule fixed in advance. The register is in [`prereg/`](prereg/). The outcomes are in [`results/`](results/).

**Four primary hypotheses. Zero confirmed.**

| Study | Outcome |
|---|---|
| ES/NQ correlation filter | Failed. +2.76 pp, p = 0.172. Applying it *costs* 31.5% of annual return |
| DX1! inverse confirmation | Passed the primary at p = 0.0312, then **reversed on replication**. Retired |
| D1/H4 timeframe robustness | Failed. 896 trades, pooled 53.39% against a 51.45% break-even, p = 0.168, 95% LCB 50.07% |
| GC1! gold as a portfolio addition | Failed. 999 trades. Best weight returns −0.04%/yr against a required +1.00 |

**Eight filter hypotheses. Zero confirmed.**

Four of them are attempts at the same underlying idea — that *when* a trade fires predicts *how* it resolves. So the family was also closed as a family, with an omnibus test, because testing enough members of a family guarantees one will clear a threshold. The full register is in [`prereg/filters/`](prereg/filters/).

Two entries there are worth the click. The hour study's best of twenty-three hours came back **below the median of the noise distribution** — pure chance typically hands you a better one. And the only filter in the campaign that cleared its pre-registered block bar, a scheduled gold benchmark fix positive in 4 of 4 blocks, turned out to have **54 of its 55 trades inside a prior that had already failed**. Naming a hypothesis in advance does not immunise it against being a subset of another one.

The DX1! result is the one worth reading in full. It cleared the pre-registered threshold at p = 0.0312 — a publishable number in most settings. Replication across five host instruments reversed it: FDAX1! at −8.04 pp, Z1! at −5.03 pp, a five-host weighted mean of −0.19 pp. It was retired.

A related secondary result failed for a reason worth recording: the measured effect **peaked at five days stale**, which no market mechanism can produce. A random coin-flip subset reproduced the same effect 11.72% of the time. The statistics said "significant." The mechanism said "artifact." The mechanism won.

Eleven closed hypotheses is not a failed campaign. It is the campaign doing what pre-registration exists to do. A strategy that survives twelve honest attempts to break it is a different object from a strategy that was never attacked.

---

## The two findings that survived

### 1. The parameter island is flat

The entry timeframe was chosen *a priori* — an hour, because an hour is a unit market participants act on — rather than selected by grid search. Testing the neighbourhood afterwards:

| Configuration | Trades (W+L) | Win rate |
|---|---|---|
| M60 (the book) | 223 | 56.05% |
| M48 | 312 | 54.17% |
| M50 | 337 | 56.97% |

Three timeframes clustered inside **2.8 percentage points across 872 trades**. The result does not sit on a knife edge, which is the standard failure mode of a curve-fitted parameter.

### 2. The retail data feed reproduces exchange data

The campaign used one non-exchange price feed. Whether that feed was trustworthy was a genuinely open question, so the full engine was re-run on CME gold futures — a different provider, and a different instrument carrying a basis and a contract roll.

| Source | Trades | Win rate |
|---|---|---|
| Retail aggregator, spot metal | 959 | 54.55% |
| CME futures | 958 | 54.49% |

**Within 0.06 percentage points on 1,013 trades, 2011–2026.** At trade level, 63.0% of futures entries coincide with a spot entry to the minute, and 94.5% of those resolve identically. The 37% that do not coincide are the basis and the roll behaving exactly as they should.

This arrived as a by-product of a study whose own hypothesis failed. That is what pre-registered nulls are for: you keep the data even when the answer is no.

---

## The number that dominates everything: execution slippage

Commissions, spreads and rolls are broker-sourced and known. **Slippage is not one of them.** It is the gap between the price that triggered an order and the price that filled it, and it is an execution outcome, not a fee schedule.

This strategy enters on a resting stop and exits on a stop. **Both sides are adversely selected by construction** — a stop fills while price is moving through the level, against you. No cost model captures that.

### The unit was wrong, and finding that out is part of the result

The original analysis reported a tolerance of **1.5 ticks per side**, and treated it as a property of the strategy. Re-deriving it from the published ledger showed it is a property of the *era*.

One R is the stop distance. On NQ a tick is 0.25 index points and has been permanently. So what one tick costs depends entirely on how many ticks wide the stop is — and NQ went from roughly 2,300 to roughly 25,000 while the tick did not move.

| Year | Median stop | In ticks | One tick/side costs |
|---|---|---|---|
| 2011 | 12.00 pts | 48 | **2.08% of R** |
| 2014 | 9.62 pts | 38 | 2.60% of R |
| 2017 | 16.00 pts | 64 | 1.56% of R |
| 2020 | 87.50 pts | 350 | 0.29% of R |
| 2023 | 66.50 pts | 266 | 0.38% of R |
| 2026 | 230.00 pts | 920 | **0.11% of R** |

The same tick of slippage does roughly **nineteen times less damage in 2026 than in 2011**. The 2011–2017 median stop is 12.75 points — exactly 51 ticks, exactly the figure the original table was built on. The arithmetic was never wrong. The scope label was.

### Both regimes, stated

**2011–2017** — stop 51 ticks, win rate 56.84% over 234 decisive trades:

| Ticks/side | Total cost | Break-even | Edge remaining |
|---|---|---|---|
| 0.0 | 0.0480 R | 52.84% | **+4.00 pp** |
| 1.0 | 0.0872 R | 55.16% | +1.68 pp |
| 1.5 | 0.1068 R | 56.32% | +0.51 pp |
| **2.0** | 0.1264 R | 57.48% | **−0.65 pp — gone** |

**2022–2026** — stop 396 ticks, win rate 66.15% over 195 decisive trades:

| Ticks/side | Total cost | Break-even | Edge remaining |
|---|---|---|---|
| 0 | 0.0480 R | 52.83% | **+13.32 pp** |
| 10 | 0.0986 R | 55.81% | +10.34 pp |
| **19** | 0.1441 R | 58.50% | **+7.66 pp — the 95% LCB planning point** |
| 25 | 0.1744 R | 60.29% | +5.87 pp |
| **45** | 0.2756 R | 66.25% | **−0.10 pp — gone** |

In the early regime the edge died inside two ticks per side. In the current one it survives about **45 ticks on the point estimate and about 19 at the 95% lower confidence bound** on the win rate.

### What to actually plan against

**Nineteen, not forty-five.** A lower confidence bound is what a risk limit is set against, not a point estimate.

**And not in ticks at all.** The tick count is not invariant — it will drift again as the instrument moves. The invariant is the fraction of R lost: today one tick per side costs about 0.5% of R, and four ticks about 2%.

Three things this does not fix:

- **The measurement still does not exist.** Wider tolerance is not a measured fill. Nothing here has traded
- **The extra room is partly illusory.** Stops widened because volatility rose, and fast markets fill stops worse. Some of the additional tolerance is consumed by the thing it protects against
- **No return figure in this repository is net of slippage.** Every one is a ceiling

An intrabar alert layer was built specifically to close this: it timestamps and names the exact trigger, stop and target levels at the moment of the event, so the difference against a broker fill *is* the number. The instrumentation is complete. The measurement is not.

---

## The performance record

Reported because a research campaign should report its results, not because performance is the claim.

**2,030 resolved trades, 2011-08-31 to 2026-08-17, at 0.048 R modelled cost.**

- **15 of 16 years positive.** One losing year: 2017, −8.16 R on a 50.0% win rate
- +236.6 R total, +15.81 R/yr
- Realised maximum drawdown on the historical path: 19.1 R

At the book's 0.50% risk per trade, block-bootstrapped over a 3-year horizon:

| Risk per trade | Return/yr | Expected max drawdown (95th pct) | 99th pct |
|---|---|---|---|
| **0.50%** (the book) | +7.91% | **10.9%** | ~14.2% |
| 1.00% | +15.81% | 21.7% | ~28.3% |

Three things belong with those numbers:

**The claim is return per unit of drawdown, not return.** At book sizing that ratio is roughly 0.73, against roughly 0.50 for a typical S&P bear cycle and roughly 0.18 through 2008 — **1.5× to 4×**, from an intraday, both-directions book carrying little equity beta. The worst drawdown in fifteen years was 9.6%, smaller than the S&P's drawdown in 2022, 2020, 2018 and 2008. That sentence does more work than any return figure, and it does not require pretending 8% beats 10%.

**Doubling the risk is not a better strategy.** It is the same strategy with twice the leverage: return and drawdown scale together, and a 1% sizing carries a 21.7% expected maximum drawdown with a 1-in-100 three-year path reaching roughly 28%.

**The smooth year-by-year record is a portfolio effect, not an instrument effect.** Individual instruments have sub-break-even years. Pooling across correlated-but-not-identical index futures is what produces the consistency, and that is the more interesting finding.

---

## Validation discipline

Every build in the chain, without exception:

- **Reversal byte-match.** Strip every inserted line, splice back any replaced lines, and the file must reproduce the reference anchor exactly. Held on every build
- **Function-level hashing.** Per-function digest against the reference; every changed function named and justified before shipping
- **Regression gates.** Fifteen simulations must exit clean
- **Parity proofs.** Three independent harnesses, 26 / 86 / 28 cases, exact. Every concept was specified and validated in Python *before* implementation, and every implementation was then proven against that specification case by case
- **Isolation scan.** Zero writes to engine state from any added code, verified mechanically
- **Field trade check.** Eight fixed anchors across two instruments, 169 and 184 trades, zero outcome mismatches

### What the discipline actually caught

Recorded in full in [`docs/06-defect-register.md`](docs/06-defect-register.md), because the failures are the evidence that the process was load-bearing rather than decorative.

A paren-balance check looked like ceremony for eleven consecutive builds, then caught three real defects in three consecutive builds: a line-splitter silently eating the last line of every inserted block, an orphaned argument, and two unclosed calls.

A structural check was written after a fourteen-line block was inserted inside an indented body, terminating a type declaration early and orphaning its last two fields. The tool now makes that failure impossible.

One documented, reasoned departure from the file's own convention turned out to rest on a wrong premise about state survival under realtime tick rollback, and produced roughly seventy duplicate notifications in a single session. The build was killed.

Two comparisons in the analysis were drawn against baselines from different time windows. Both errors were mine. Both flipped a conclusion. Both were caught in review before they reached a result document.

---

## The engine

The implementation is not published. What can be said accurately:

- ~4,800 lines, **stateful from bar 0**
- 15 user-defined types, 66 persistent arrays, 104 functions
- Path, liquidity, structure and order-flow state machines running across **three timeframes simultaneously**
- The originating hypothesis is **market-structural, not statistical** — liquidity sweeps, failed breakouts and order-flow context at higher-timeframe levels. These were behaviours observed first and formalised afterwards, not patterns mined from data
- Every concept was validated in Python before it was written, and every build proven against that Python case by case

The source stays private because the research continues. Everything used to test it, and everything learned from testing it, is here.

---

## What is in this repository

```
docs/        methodology, validation protocol, inference, slippage, architecture, defect register
prereg/      one file per hypothesis, threshold and decision rule fixed before collection
results/     every outcome, including all eleven rejections, with the arithmetic
tooling/     build verification · inference library
data/        trade-level outcome ledger, 2,030 rows
reproduce.py regenerates every table in results/ from data/
```

**Not included:** strategy source, entry and exit logic, price levels, signal specifications.

**The ledger is redacted by design.** It carries date, instrument, direction, outcome and R multiple. It does not carry prices, stop levels or intraday timestamps. Every statistical claim above is reproducible from it; the strategy is not recoverable from it.

`tooling/inference/` is a general-purpose library. It takes any ledger in the published schema and returns block-bootstrapped confidence intervals, drawdown distributions, break-even sensitivity and cost-adjusted edge. It has no knowledge of this strategy and is reusable against any trade record.

---

## Reproducing the results

```bash
git clone https://github.com/nestorasnq/preregistered-quant-research
cd preregistered-quant-research
pip install -r requirements.txt
python reproduce.py
```

Regenerates every table in `results/tables/` from `data/ledger.csv`. Bootstrap seeds are fixed; output should match byte-for-byte.

---

## Limitations

Stated in full in [`LIMITATIONS.md`](LIMITATIONS.md). In short:

- **No figure is net of execution slippage.** Tolerance is regime-dependent: the edge died inside two ticks per side in 2011–2017, and survives roughly 19 ticks at the 95% lower bound in the current regime. The fill itself remains unmeasured
- **Nothing here has traded live or on paper.** This is research
- Returns and drawdowns scale together; any sizing figure is meaningless without its drawdown attached
- Year-by-year consistency is a property of the pooled book, not of individual instruments
- Every result is implicitly conditioned on a fixed chart timeframe, which is known to change the trade set

---

## About

Built and run by **Dimitris Nestoras** — Financial Data Analyst, BSc Economics (University of Macedonia), MSc Applied Economics and Finance (in progress).

Interests: market risk, quantitative model validation, financial market data.

[LinkedIn](https://www.linkedin.com/in/dimitris-nestoras-86643b290/) · dimitrisnes28@gmail.com
