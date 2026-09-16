# PR2 — Target geometry

**Verdict: unanswerable on the available data, then closed on gold.** The entry is here because the
analysis was corrected mid-campaign, in the direction that made the conclusion weaker.

## Hypothesis

A target wider than 1:1 improves the strategy. The engine exits at one R; the question is whether
winners would have run further.

**Why it matters more than any filter.** A filter raises expectancy by discarding trades, and total
profit falls faster than expectancy rises. Target geometry changes what every winning trade is
worth. It is the one untested parameter with the leverage to change the result rather than trim it.

## The correction

The original reading of the excursion data was that it **pointed against** a wider target: only
11.9% of wins ran to 1.5 R.

**That reading was wrong, and it was walked back.**

**Wins are censored.** A trade closes the moment price touches 1 R, so the recorded favourable
excursion is only the overshoot on the resolving bar — not how far the move would have gone. *"Only
11.9% of wins ran to 1.5 R"* is **a lower bound, not a measurement.** The true fraction that would
have reached 1.5 R is unknown and could be much higher.

**Losses are uncensored and informative.** 32.1% of losing trades ran ≥ 0.5 R favourably before
dying. That is real, and it bears on stop placement and break-even arming rather than on targets.

So the data could answer half the question — the half about losses — and the half everyone cared
about was structurally unavailable.

## Ruling

**On ES1!: the data cannot answer it.** Recorded as a limitation of the measurement, not as evidence
against wider targets.

**On gold: closed**, after a measurement build change made it answerable.

**And it stays closed.** The most likely route back in is a rule that lets winners run past 1 R
under some condition — which *is* a wider target, arriving under a different name. Moving a stop is
a different thing from moving a target, and that line has to be held deliberately or a closed
question returns through the side door.

## Two lessons recorded

**Censored data produces confident wrong answers.** The censoring was not visible in the numbers —
11.9% looks like a measurement. Recognising it required knowing how the exit worked, not how the
statistic was computed.

**Answering it needed a build change, not an analysis change.** No amount of re-analysis recovers
information the instrumentation never captured. The fix was to log favourable excursion *past* the
1 R exit as a separate uncensored field — and the instrumentation had to be proven behaviourally
inert first, with a positive control, because **a counter that reports zero is worthless until it
has fired on a known case.**
