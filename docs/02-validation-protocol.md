# Validation Protocol

What was enforced on every build, why each gate exists, and what it caught.

The premise: a backtest engine is a piece of software, and a research result computed by
untrusted software is not a result. Most of this protocol is ordinary software engineering
applied somewhere it usually isn't.

---

## The problem this solves

The engine is roughly 4,800 lines, stateful from bar 0, with 15 user-defined types, 66 persistent
arrays and 104 functions reading three timeframes at once. A single misplaced line can change the
trade set silently — not by throwing an error, but by producing a slightly different, entirely
plausible set of trades.

That is the specific failure this protocol is built against: **a change that alters results without
announcing itself.**

---

## The gates

### 1. Reversal byte-match

Every build in the campaign descends from one reference file, the **reversal anchor** (3,881 lines,
md5 `43fabae1…`). For any child build, strip every inserted line and splice back any replaced parent
lines, and the result must reproduce the anchor **byte for byte**.

This is the strongest gate in the protocol, because it is binary and mechanical. There is no
judgement in it and nothing to argue about. If a child does not reverse, something entered the file
that nobody recorded — and *that* is the condition worth detecting, not the diff itself.

**Held on every build in the chain, without exception.**

### 2. Function-level hashing

`fn_md5.py` splits a Pine file on function declarations and hashes each function independently, then
diffs the digests against the parent. Every changed function has to be named and justified before
the build ships.

The collection build has **90 of its 91 functions byte-identical to the parent**. That is a
one-line claim that would otherwise require a reviewer to read 4,800 lines.

Why per-function rather than a whole-file diff: a whole-file diff tells you *what* changed as text.
A per-function digest tells you what changed as *behaviour*, which is the question, and it survives
reformatting and line renumbering.

### 3. Regression simulations

Fifteen Python simulations must exit clean on every build. They cover entry state machines,
break-even logic, cold-start behaviour, prefill, epoch handling and measurement layers.

These are regression gates, not tests of correctness. They do not prove the engine is right. They
prove it still does what it did before the edit.

### 4. Parity proofs

Three independent harnesses check that the Python specification and the Pine implementation agree
case by case: **26 / 86 / 28 cases, exact.**

The direction matters. **Every concept was specified and validated in Python before it was written
in Pine**, and every Pine build was then proven against that specification. The Python is the
reference and the Pine is the implementation under test, not the other way round.

This is model validation in the ordinary sense: an independent implementation of the same
specification, built to disagree if the specification was misread.

### 5. Static pre-flight

`pineflight.py` runs five static checks over the file before it ever reaches the platform: paren
balance on code lines only, orphaned arguments, unterminated calls, suspicious indentation depth,
and a whole-file format-directive count that must not increase between builds.

The last one is a canary. A rising format count usually means text was inserted somewhere it was
not intended to go.

### 6. Structural invariants

`blockcheck.py` verifies that an inserted block landed at the nesting depth it was supposed to land
at, and that no type or function body was terminated early by an insertion.

This tool was written **after** the failure it now prevents. See the defect register.

### 7. Isolation scan

For any instrumentation added to the engine — alert layers, measurement code — a mechanical scan
confirms zero writes to engine state: no writes to any engine field, no engine-array mutations, no
trade-record writes, and no history references, `varip`, or cross-timeframe requests in added lines.

Measurement code that changes the thing it measures is worse than no measurement, because the
output still looks like data.

### 8. Field trade check

Eight fixed anchor trades on two instruments, re-verified on every build in the chain:
**ES1! 169 trades, NQ1! 184 trades, zero outcome mismatches.**

The other gates check that the file is structurally what it claims to be. This one checks that it
still produces the same trades. It is the end-to-end gate, and it is the one that would catch a
defect that slipped past all seven others.

---

## What the protocol does not do

**It does not establish that the engine is correct.** It establishes that the engine is *stable*,
that changes are *accounted for*, and that the Pine matches a specification that was written and
tested independently. Those are different claims and the difference is worth stating.

**It was applied by one person.** The pre-registration protocol and this validation chain exist
partly to substitute for an independent reviewer. That is a real substitute, not an equivalent one.

**The reference itself is unverified against anything external.** The parity proofs establish
Python-to-Pine agreement. If the Python specification misunderstood the market mechanic it was
modelling, both implementations would be wrong together and every gate here would pass.

---

## The point

Eight gates is more than a research backtest usually carries, and the cost was real — several builds
were killed by gates that turned out to be right.

The justification is in `06-defect-register.md`. Three of these gates caught defects that would have
silently altered results, and one of them looked like pure ceremony for eleven consecutive builds
before it caught anything at all.
