# Engine Architecture

## In plain words

The thing being tested is a program that watches price and decides when the setup it is looking for
has appeared.

It is about 4,800 lines long. To give a sense of what that means: it is not a formula. It is not
"buy when the moving average crosses." It is a program that **remembers** — it tracks where
important price levels are, which ones have been taken out, what the current market bias is, and
where price has travelled — and it updates all of that on every single bar, from the very first bar
of history onwards.

**The source code is not published**, because I still intend to trade this. Everything used to test
it, and everything learned by testing it, is published.

This document describes the shape of the thing without giving away what it does.

---

## The size and shape

| | |
|---|---|
| Lines | ~4,800, Pine Script v6 |
| Custom data types | 15 |
| Persistent arrays | 66 |
| Functions | 104 |
| Timeframes read simultaneously | 3 |
| State | **Stateful from bar 0** |

## "Stateful from bar 0" — what that actually means

This is the single most important property, and it drives most of the project's practical problems.

**The engine's answer today depends on everything it has seen since the beginning.** It is not
computing a formula over the last N bars. It is carrying an accumulated picture forward.

Two consequences that shaped the whole campaign:

**You cannot start in the middle.** Ask the engine about 2019 and it needs to have watched 2011
through 2018 first to know what state it is in. Data collection therefore had to run in overlapping
chunks with a warm-up period in front of each, and "how much of this chunk is warm?" became a
tracked quantity with its own tooling.

**A small code change can alter distant results.** Change how one level is recorded and every
downstream decision that depended on it may shift, years later. This is why the validation protocol
is as heavy as it is — not perfectionism, but the fact that a stateful engine hides the consequences
of a change.

## The four state machines

A **state machine** is a program that is always in one of a fixed set of conditions and moves between
them on defined events. A traffic light is a state machine.

Four run at once:

| | what it tracks |
|---|---|
| **Path** | where price has actually travelled, as a sequence of turning points |
| **Liquidity** | price levels where orders are likely resting, and whether they have been taken out |
| **Structure** | whether the market is making higher highs or lower lows, and which way the bias points |
| **Order flow** | a separate read on participant behaviour that can override the structural bias |

They run across three timeframes at once — a slow one for context, a middle one for the setup, and a
fast one for the entry. The slow timeframes decide *whether to look*; the fast one decides *when*.

## Where the idea came from

**Market-structural, not statistical.**

The originating observation: price pushes past a level where many orders are resting, takes them out,
and then reverses. The breakout fails and the participants who chased it are trapped.

That behaviour was **observed first and formalised into rules afterwards.** The rules were not found
by searching data for patterns that would have made money.

This matters for how you read every result here. A strategy mined from historical data comes with a
story invented to fit it. A strategy built from an observed mechanism can be *wrong*, but it can be
wrong in ways you can check — which is what thirteen pre-registered studies were for.

## Python first, always

**Every concept was written and validated in Python before it was written in the engine.**

The Python version is the specification. The engine is the implementation. Three independent
harnesses then prove the two agree case by case: **26 / 86 / 28 cases, exact.**

This is standard model-validation practice and it is unusual in retail trading. The value is that a
disagreement between the two means something specific — one of them misread the specification — and
you find out at build time rather than from a live account.

## Why the source stays private

The research continues and I intend to trade this.

Published: the methodology, the pre-registrations, the results, the validation tooling, and the
trade-level outcome data. Not published: the entry and exit logic, the signal specifications, and
price-level data.

**The honest cost of that choice**, stated in [`LIMITATIONS.md`](../LIMITATIONS.md): the results here
cannot be independently replicated from source. They can be recomputed from the published ledger,
which is a weaker guarantee. A reader is being asked to accept that the ledger is an honest record of
what the engine produced.

## What was published instead

The Python simulations that reproduce the engine's logic are **not** published either — they are the
strategy in a different language.

What is published is the layer that has nothing to do with the strategy: build verification, data
pipeline, coverage auditing, and a general-purpose statistical inference library that works on any
trade ledger. See [`../tooling/`](../tooling/).
