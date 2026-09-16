# Statistical Inference

## In plain words

Imagine you want to know whether a coin is fair. You flip it 100 times and get 55 heads. Is the coin
biased, or did you get lucky?

The honest answer is a range: "somewhere between 45% and 65% heads." Not a single number.

This document is about how those ranges were computed, and about one specific mistake that makes
them **look much more precise than they really are**.

The mistake is treating trades as if they were independent coin flips. They are not. And if you
pretend they are, every range you produce is too narrow — which makes every result look more solid
than it is, in the direction that flatters you.

---

## Why trades are not coin flips

A coin has no memory. Trade outcomes do.

This strategy keys on higher-timeframe market structure. When the market is in a particular
condition, it takes several trades off that same condition over the following days. If the condition
is a good one, those trades tend to win together. If it is a bad one, they tend to lose together.

So a week with eight trades is **not** eight independent pieces of information. It is closer to one
piece of information, observed eight times.

**If you resample individual trades, you are pretending each one is fresh news.** That understates
how much the results bounce around, so the confidence interval comes out too narrow and the strategy
looks more certain than it is.

## The fix: resample whole weeks

The block bootstrap works like this:

1. Cut the trade history into **ISO calendar weeks** — each week is a block
2. Draw weeks at random, with replacement, until you have as many weeks as a three-year stretch
3. Glue those weeks together into one fake three-year history
4. Compute whatever you care about on it — win rate, drawdown, return
5. Do that 10,000 times
6. Look at the spread of the 10,000 answers

Because whole weeks move together, the clustering inside a week is preserved and flows into the
answer. The range you get is honest.

**Verified rather than assumed.** Running both versions on each instrument, the week-clustered
intervals come out wider than naive ones every time — 8.98 against 8.27 percentage points, 8.51
against 7.64, 8.56 against 8.13. Modest, consistent, and in the correct direction. If clustering had
made no difference, it would mean the clustering assumption was doing nothing and should be dropped.

## Why weeks, and not some other block length

Most block bootstraps make you choose a block length. That is a free parameter, and a free parameter
chosen by the person reporting the result is a place where a result can be tuned.

**Fixing the blocks to calendar weeks removes the choice.** It costs a little statistical efficiency.
It buys the guarantee that nobody picked the block length after seeing which one gave a nicer answer.

The week is also the natural unit here: the clustering comes from market regime, and market regime
persists over days rather than hours.

## Drawdown, and the error that inflated it

**The question a drawdown estimate answers:** over the next three years, how bad does this get?

**The wrong way — and this campaign did it wrong once.** Slide a moving window along the one
historical path and record the worst decline in each window. That sounds reasonable and it is not:
a single bad stretch gets counted again and again as the window slides over it. **It turned a real
0.592% into 0.936%** — a 58% overstatement — before it was caught.

**The right way.** Build 10,000 *different* three-year histories out of resampled weeks, measure the
worst decline in each, and read the percentiles. Each path contributes one observation.

| percentile | meaning in plain words |
|---|---|
| 50th | a typical three years |
| 95th | a bad three years — 1 in 20 |
| 99th | a very bad three years — 1 in 100 |

Those are the numbers a risk limit is set against, and the 95th percentile is what the sizing rule
uses.

## Confidence bounds are what you plan against

A **point estimate** is the single best guess. A **lower confidence bound** is roughly the worst
case consistent with the data.

You report the point estimate. You **plan against the lower bound**, because the point estimate is
right about half the time and a strategy sized off it is under-capitalised exactly when it matters.

This is not conservatism for its own sake. It changed a real number in this project: the strategy's
tolerance for execution costs is 45 ticks per side on the point estimate and **19 at the lower
bound**. Nineteen is the number that governs.

## The mechanism check

The cheapest test in the campaign, and it settled a question that p-values left open.

**Ask whether the effect's shape is physically possible.**

One filter appeared to work — until the effect was measured using regime information of increasing
age. It got **stronger as the information got older, peaking at five days stale.**

No market mechanism can do that. Information you learned five days late cannot predict better than
what you knew at the time. The statistics said "marginal." The mechanism said "impossible."

A result that is statistically marginal **and** mechanistically impossible is not a weak finding. It
is a clean negative. This check needs no distributional assumption, costs one extra computation, and
every study after this one carried it.

## What the inference does not fix

**Week-clustering handles within-week dependence. It does not handle regime persistence over
months.** A strategy whose edge varies by market regime will still have intervals that are somewhat
optimistic.

**Twelve studies were run.** None was confirmed, so no multiple-comparison correction is
load-bearing in the final result. Had one passed, it would have needed one — which is exactly what
happened to the study that passed at p = 0.0312, where replication rather than correction is what
retired it.
