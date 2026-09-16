# Results — everything, in one place

## In plain words

Twelve ideas were tested properly. **None of them worked.**

Two things came out positive anyway, and both arrived sideways — as by-products of studies whose own
question came back "no."

That is the whole campaign in three sentences. The detail follows.

---

## The scoreboard

Twelve distinct studies, each counted once by what it proposed:

| by type | studies | confirmed |
|---|---|---|
| Filters | 8 | **0** |
| Parameters | 3 | 1 positive, 1 closed, 1 unanswerable |
| Portfolio addition | 1 | **0** |
| **total** | **12** | **0** |

Four of the twelve were designated **primary** — the main question of their own study. None passed.

## The four primaries

| Study | The idea, plainly | Verdict |
|---|---|---|
| [ES/NQ correlation](../prereg/primaries/P1-esnq-correlation.md) | Two similar indices agreeing should be a better signal | **FAILED.** +2.76 pp, p = 0.172. And using it *costs* 31.5% of annual return, because it throws away too many trades |
| [DX1! confirmation](../prereg/primaries/P2-dx1-inverse-confirmation.md) | The dollar moves opposite to stocks; use it as confirmation | **FAILED on replication.** Passed at p = 0.0312, then reversed on four other instruments |
| [D1/H4 robustness](../prereg/primaries/P3-d1h4-robustness.md) | If the idea is real, it should work on slower timeframes too | **FAILED.** 896 trades, p = 0.168. Returns a fifteenth of what the book does per unit of drawdown |
| [Gold in the portfolio](../prereg/primaries/P4-gc1-portfolio-addition.md) | Gold is a different animal; adding it should smooth the book | **FAILED.** −0.04%/yr against a required +1.00 |

## The eight filters

A **filter** is a rule that says "skip this trade." All eight said skip, and none of them helped.

Four of them were attempts at the same underlying idea — that *when* a trade happens predicts *how
it ends*. Those were also closed **as a family**, with a single test asking whether any time effect
exists at all, because if you test enough individual hours one will look good by luck.

Full register: [`../prereg/filters/`](../prereg/filters/)

**The two worth reading:**

**The hour study.** Out of 23 hours of the day, the best one came back **below the median of what
pure chance produces.** Shuffle the hour labels randomly 10,000 times and the best hour is typically
*better* than the real best hour. The pre-registration had predicted, in writing, that exactly one
of thirteen hours would look significant by luck. Exactly one did.

**The gold benchmark fix.** This was the only filter in the entire campaign to clear its
pre-registered bar — positive in **4 of 4** blocks, biggest effect, lowest p-value, and a real
scheduled institutional flow behind it. Then a containment check found that **54 of its 55 trades
sat inside a different filter that had already failed.** It was not a second idea agreeing with the
first. It was the hottest fifth of the first one. Retired.

## The two positive findings

### 1. The parameter island is flat

**The worry.** If you pick a setting because it made money in testing, you have probably fitted to
noise. Move one notch and the edge collapses.

**The check.** Test the settings on either side.

| setting | trades | win rate |
|---|---|---|
| M60 — the one in use | 223 | 56.05% |
| M48 | 312 | 54.17% |
| M50 | 337 | 56.97% |

**Three neighbouring settings inside 2.8 percentage points across 872 trades.** The result does not
sit on a spike.

The setting in use was chosen *before* testing — an hour, because an hour is a unit market
participants act on — rather than picked as the winner of a search. Testing the neighbourhood
afterwards is what makes that claim checkable.

Full detail, including the table where M48 looks *better* and the one where it looks worse:
[`PR1`](../prereg/parameters/PR1-entry-timeframe.md)

### 2. The data feed is trustworthy

**The worry.** Most of this campaign ran on a retail price feed, not exchange data. If that feed was
wrong, everything built on it was wrong.

**The check.** Re-run the entire engine on real CME gold futures — a different provider, a different
instrument, carrying a basis and a contract roll that the spot feed does not have.

| source | trades | win rate |
|---|---|---|
| Retail aggregator, spot metal | 959 | 54.55% |
| CME futures | 958 | 54.49% |

**Within 0.06 percentage points, on 1,013 trades across sixteen years.**

At trade level, **63.0% of futures entries land on the same minute as a spot entry**, and **94.5% of
those end the same way.** The 37% that do not line up are the basis and the roll doing exactly what
they should.

This came out of the gold portfolio study — the one whose own hypothesis failed. The study asked
"should I add gold?" and the answer was no. The data it generated answered a more important question
that had been open the whole time.

## The performance record

Reported because a campaign should report its results, not because performance is the claim.

**2,030 resolved trades, 2011–2026, three instruments.**

- **15 of 16 years positive.** The one loser: 2017, −8.16 R
- +236.56 R total, +15.81 R/yr
- Worst drawdown actually experienced: 19.1 R — **9.6%** at the book's risk setting

| Risk per trade | Return/yr | Bad-case drawdown (1 in 20) | Very bad (1 in 100) |
|---|---|---|---|
| **0.50%** | +7.91% | **10.9%** | ~14.2% |
| 1.00% | +15.81% | 21.7% | ~28.3% |

**Read the second row as a warning, not an upgrade.** It is the same strategy with twice the
leverage. Return and drawdown both double.

### Why the claim is drawdown, not return

**Return per unit of drawdown is roughly 0.73** — against roughly 0.50 for a typical S&P bear cycle
and roughly 0.18 through 2008. **Between 1.5× and 4×.**

In plain words: this makes less money than the index, and it makes it with much smaller falls along
the way. The worst drop in fifteen years was 9.6%, smaller than the S&P's drop in 2022, 2020, 2018
and 2008.

That sentence is true and does not require pretending 8% beats 10%.

### Three caveats attached to those numbers

**Not net of slippage.** Every figure is a ceiling. See [`../docs/04-execution-slippage.md`](../docs/04-execution-slippage.md).

**Nothing has traded**, live or on paper.

**The smooth record is a portfolio effect.** Individual instruments have losing years — and one of
the three, ES1!, **does not clear break-even on its own at 95% confidence.** The consistency comes
from pooling three correlated-but-not-identical instruments, which is itself the more interesting
finding.

## Reproducing all of it

```bash
python reproduce.py
```

Regenerates every table in [`tables/`](tables/) from the published ledger. Seeds are fixed.
