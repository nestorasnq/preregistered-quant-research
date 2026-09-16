# F5 — Scheduled-event anchors

**Verdict: FAILED.** Contains the only filter in the campaign that cleared its pre-registered block
bar, and the reason it died is the best thing in this register.

## Hypotheses

Two named priors, both specified for a mechanism before any data was seen:

**NY 7 — 14:00 New York.** FOMC statements and Treasury auction results. A scheduled,
market-moving, calendar-known event.

**LBMA PM — 15:00 London.** The afternoon gold benchmark fix: a real, scheduled, documented
institutional flow. On gold specifically, about as legitimate as a time hypothesis gets.

## NY 7 — statistically strong, and unfreezable

On ES1! it was the one anchor that cleared its pre-registered bar:

| | |
|---|---|
| sample | n = 20 — 12 W / 1 L / 7 BE |
| expectancy | +0.5500 R gross, +0.4869 R net |
| **p** | **0.0017, surviving Bonferroni across all ten anchors** |
| spread | 19 distinct days, 9 of 11 years |
| independent signature | **75% Tue/Wed against a 44% book baseline** — consistent with its stated mechanism |

That last row matters: the weekday concentration is what an FOMC/auction effect *should* look like,
and it was not part of the selection.

**And it was not frozen.** Projected out-of-sample sample: **≈ 10 trades.** The pre-registration's
verdict table says a sample that size can only return *"the sample cannot answer this"* unless it
collapses outright.

> Spending the only unrepeatable test in the study on a cell that cannot answer would be worse than
> not testing at all, because it would produce a number that reads like evidence.

On gold, NY 7 came back 3 of 4 blocks with **9 out-of-sample trades**. Same conclusion.

**Recorded as: failed for want of a holdout, not on evidence against it.** That distinction is kept
deliberately. It went 2 of 4 out-of-fold, which is not encouraging, but it was never given a fair
test and the register should not pretend otherwise.

## LBMA PM — the one that cleared the bar

| block | B1 | B2 | B3 | B4 | clears |
|---|---|---|---|---|---|
| P1 tier-1 anchors | −9.8 | −2.9 | +1.3 | −8.6 | 1 of 4 |
| P2 position-0 | +16.1 | +14.6 | +0.9 | −12.0 | 3 of 4 |
| P3 NY 7 | +44.8 | +42.3 | +45.6 | −10.4 | 3 of 4 |
| **P5 LBMA PM** | **+25.4** | **+8.5** | **+21.6** | **+24.0** | **4 of 4** |

Positive in every block. Lowest p in the study. Large effect. A real scheduled mechanism behind it.
By the letter of the frozen bar, it passed.

**Then it was checked for independence, before the out-of-sample look was spent:**

| | |
|---|---|
| LBMA PM trades, whole sample | 55 |
| of those with `h4_pos = 0` | **54 of 55 — 98%** |
| at New York hour 10 | 54 of 55 |
| LBMA PM as a share of all position-0 trades | **21%** |

**London 15:00 is New York 10:00, and New York 10 is a position-0 hour. P5 is a 21% slice of P2.**

So the structure of the result is: **P2 as a whole is +6.7 pp and not significant, and its
best-performing fifth is +21 pp.** That is not two priors agreeing. It is one prior, and the
sub-cell inside it that happened to run hottest.

## Ruling

Both closed. No event-anchor filter.

## Why this is the most important entry in the register

**Naming a hypothesis in advance does not immunise it.** P5 was pre-registered. It was named for a
plausible, documented mechanism. The mechanism may even be real. And the *evidence* for it was
still a subset of a prior that had already failed.

Pre-registration protects against choosing a hypothesis after seeing the data. It does not protect
against a registered hypothesis being structurally contained inside another one. Nothing catches
that except checking — and the check cost one query and was run **before** the irreversible
out-of-sample look, not after.

The omnibus made the same point from the other side: New York hour 10 was one of its cells, and
across all hours there was nothing.
