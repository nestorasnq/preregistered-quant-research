# Tooling

## In plain words

Three kinds of tool are published here. None of them knows anything about the trading strategy.

**Build verification** answers "did my edit do only what I meant it to do?" These exist because the
engine carries state forward from the very first bar, so a small change in one place can alter
results years later without producing an error. Each of these tools was written after a specific bug
got through, and each one makes that bug impossible to repeat.

**Statistical inference** answers "how confident can I actually be?" It takes a list of trade
outcomes and returns honest confidence ranges, drawdown distributions and cost sensitivity. It works
on any trade ledger, not just this one.

**What is NOT published** is everything that encodes the strategy: the engine source, and the Python
simulations that mirror its logic. Those are the strategy in a different language and publishing
them would be publishing it.

---

## `build-verification/`

| Tool | The question it answers | The bug it exists for |
|---|---|---|
| [`fn_md5.py`](build-verification/fn_md5.py) | Which functions changed between two builds? | A text diff of a 4,800-line file is too noisy to read, so you stop reading it |
| [`blockcheck.py`](build-verification/blockcheck.py) | Did my inserted block land where I meant it to? | A 14-line block landed inside a type declaration, ended it early, and orphaned its last two fields |
| [`pineflight.py`](build-verification/pineflight.py) | Will this fail on paste, for one of five known reasons? | Five mistakes that each cost a full round trip to the chart platform and back |

Each one is self-documenting: run it with no arguments and it prints its own explanation, including
why it exists.

**`fn_md5.py` is the one worth reading first.** A text diff tells you which *lines* differ. A
per-function fingerprint tells you which *behaviour* differs, and it survives reformatting and line
renumbering. It turns "please review 4,800 lines" into "90 of 91 functions are byte-identical; here
is the one that changed and why" — a claim a reviewer can verify in ten seconds.

**`pineflight.py`'s fifth check is the interesting one.** It is not a compiler error. The platform
inserts thousand separators into logged numbers, so a price of 1457.75 is written as "1,457.75" —
the comma lands inside a comma-separated log line and every downstream parser silently reads the
wrong fields. The file compiles. It runs. The data is wrong. That is the class of defect worth
building a tool for.

### Sanitisation note

These are the working tools with strategy-specific identifiers removed and hardcoded paths replaced
by command-line arguments. The logic is unchanged.

## `inference/`

A general-purpose library for trade-outcome data. Give it a ledger in the
[published schema](../data/SCHEMA.md) and it returns:

- Year-by-year performance, win rates, net R
- **Block-bootstrapped confidence intervals** clustered on ISO weeks — see
  [`../docs/03-inference.md`](../docs/03-inference.md) for why clustering by week matters and what
  goes wrong without it
- Drawdown distributions over a forward horizon
- Break-even win rate and cost sensitivity, including slippage in ticks or in fractions of R

It has no knowledge of this strategy and is reusable against any trade record.

| Module | Contents |
|---|---|
| [`ledger.py`](inference/ledger.py) | Loading, strict schema validation, yearly aggregation |
| [`inference.py`](inference/inference.py) | Block bootstrap, drawdown distribution, confidence intervals |
| [`costs.py`](inference/costs.py) | Break-even win rate, slippage sensitivity, tick tolerance |

```python
from inference import load, resolved, summary, bootstrap_ci, drawdown_distribution

book = resolved(load("data/ledger.csv"), ["ES1!", "NQ1!", "NK2251!"])
print(summary(book, cost_r=0.048))
print(bootstrap_ci(book, "win_rate"))
print(drawdown_distribution(book, cost_r=0.048, horizon_years=3.0))
```

Validation is deliberately strict. A silently malformed ledger produces numbers that look plausible,
which is the failure mode worth spending code on.
