# Defect Register

Every defect the validation protocol caught, including the two that were errors of analysis rather
than of code, and the one whose reasoning was wrong despite being carefully argued.

This document exists because a validation protocol with no recorded catches is decoration. The
catches are the evidence that the gates were load-bearing.

---

## 1. The paren-balance check that looked like ceremony

**Gate:** code-only paren balance, in `pineflight.py`
**Status:** caught three real defects in three consecutive builds

For eleven consecutive builds this check found nothing. It was the most obviously pointless gate in
the protocol — a balanced-parenthesis count over a file that the platform's own compiler would reject
if it were unbalanced.

Then it caught three defects in a row:

1. **A line-splitter eating the last line of every inserted block.** The insertion tooling was
   dropping the final line of each block it wrote. Every block. Silently
2. **An orphaned `group=` argument** left behind by an edit that removed the call it belonged to
3. **Two unterminated `input.string(` calls**

The first is the one that matters. A tool that drops the last line of every insertion produces a
file that is *usually* still valid — and would have produced results indistinguishable from correct
ones until something downstream broke.

**What it cost to keep:** a few seconds per build for eleven builds.
**What it caught:** a systematic tooling defect affecting every insertion made.

A gate's value cannot be assessed from its recent hit rate. That is the entire lesson.

---

## 2. `CE10198` — fourteen lines inside a type body

**Gate:** none existed. This defect is why `blockcheck.py` was written
**Status:** caught by compiler error, then made structurally impossible

A fourteen-line block was inserted inside an indented body — specifically inside a type declaration
— which terminated the declaration early and **orphaned its last two fields**.

The compiler caught this one, which was luck. A block landing at the wrong nesting depth does not
reliably produce an error. It can produce a type that is missing fields, or a function whose body
silently ends early, and in a stateful engine either would change results rather than fail.

`blockcheck.py` now verifies the nesting depth of every insertion and that no type or function body
terminates early. Its docstring records the failure it was written for, so the next person to read
it knows why it exists.

**Pattern:** the fix was not "be more careful with insertions." The fix was a tool that makes the
failure mode detectable.

---

## 3. The `alert.freq_all` bug — careful reasoning, wrong premise

**Gate:** field testing. Build killed
**Status:** the most instructive defect in the project

A build departed from the file's own convention on alert frequency. The departure was
**documented and reasoned** — an argument was written for why the convention did not apply in that
case, and the argument was internally coherent.

The premise was wrong. **Script-state latches do not survive realtime tick rollback.** When the
platform rolls back and replays a bar, the latch that was supposed to suppress repeat notifications
has been reset, so it suppresses nothing.

Result: roughly **seventy duplicate notifications in a single session**. The build was killed.

This is the defect worth dwelling on, because every other entry here is a mistake. This one was a
*decision* — considered, written down, justified, and wrong at the level of a factual premise about
platform behaviour that had never been tested.

**What would have caught it earlier:** treating "script state persists across ticks" as an assumption
requiring a test, rather than as background knowledge. It was neither documented as an assumption
nor tested.

---

## 4. Two era-mismatch errors in the analysis

**Gate:** review. Both caught before reaching a result document
**Status:** both would have flipped a conclusion

Two comparisons were drawn against baselines computed over **different time windows** than the thing
being compared — M50 and M48 measured over one period, the baseline over another.

Both were errors of analysis, not of code. No gate in the validation protocol could have caught
them, because the software was working perfectly and computing exactly what it was asked to compute.

**Both flipped a conclusion.** In both cases the corrected comparison reversed the sign of the
finding.

This is the failure mode that validation protocols do not address and that pre-registration only
partly addresses: the code is right, the statistics are right, and the *question* is wrong.

---

## 5. The slippage headline was anchored to a dead regime

**Gate:** independent reconstruction of published figures during repository preparation
**Status:** corrected. See `README.md` and `LIMITATIONS.md` §2

The project carried, as a headline figure, that the entire measured edge disappeared at
**1.5 ticks per side**. Every number in the supporting table was arithmetically correct and
reproduced exactly from the ledger.

The scope label was wrong. The table describes NQ1! **in the 2011–2017 regime**, when the median
stop was 12.75 points — exactly 51 ticks. It was carried as though it described the strategy.

One R is the stop distance; a tick on NQ is fixed at 0.25 points. NQ rose roughly tenfold over the
sample, so the stop grew about eightfold in ticks, and the same tick of slippage does roughly
**nineteen times less damage in 2026 than in 2011**. Current-regime tolerance is about 45 ticks per
side on the point estimate and about 19 at the 95% lower bound.

**Pattern, and the reason this sits in the same register as the era-mismatch errors:** a figure
computed on a subset was carried as a property of the whole. Same failure, different year, found by
recomputing a published claim from scratch rather than by any gate.

---

## 6. Data defects found during ledger preparation

**Gate:** column-semantics verification before publication
**Status:** confirmed, documented, excluded from publication

In the campaign export:

- **`entry` is blank on all 694 ES1! rows.** ES1! stop geometry cannot be derived from it at all
- **`entry` on NQ1! holds 29 distinct small integers, not prices.** The column is corrupt
- `sl1R` was confirmed to be the **stop distance in price units** rather than a price level, by
  testing `|entry − sl| == sl1R` against a separate export carrying all three columns:
  **1,013 of 1,013 rows matched, zero mismatches**

None of these columns are published, so no published figure is affected. The verification is
recorded because an earlier draft of this analysis computed a stop distance as `|entry − sl1R|` on
the corrupt column and produced a result that was wrong by a factor of three before being caught.

---

## Open, untraced

**Two ES1! `MISMATCH` exits** in the provisional measurement layer. NQ1! has zero across 184 exits,
so the exit walk itself is sound and the cause is ES1!-specific. Untraced.

**Shadow seed root cause.** The arm layer quotes a stop that is **too tight on 6.0% of trigger
alerts** — 10 of 166 on ES1!, 11 of 183 on NQ1!. The rate being identical across two instruments
means it is systematic, not noise. Median severity is 17–19% of the engine's stop distance. A
correction exists but applies at resync rather than preventing the condition.

A stop quoted too tight knocks you out of trades the rules would have kept. Recorded as open.

---

## What the register shows

Six defects, from six different sources: a tool, a structural invariant, a reasoned decision with a
false premise, two analysis errors, and a scope label on a published figure.

Only three were caught by automated gates. The other three were caught by review, by field testing,
and by recomputing a published claim from scratch — which is an argument for doing all three, not
for building more gates.

The two most consequential entries, **§4 and §5**, were both the same error: a figure computed on
one subset being carried as a property of another. No amount of software validation addresses that.
