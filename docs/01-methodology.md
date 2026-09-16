# Methodology

## In plain words

I had an idea about how markets move. I wanted to know if it was true or if I was fooling myself.

Fooling yourself is the easy outcome. If you look at fifteen years of market data for long enough,
you will always find something that looks like it works. Look at enough hours of the day and one of
them will have made money. That does not mean the hour is special. It means you looked a lot.

So before I looked at any data, I wrote down what I expected to find, and what result would make me
say "no, this doesn't work." Then I collected the data and checked. I was not allowed to change the
rules afterwards.

I did that thirteen times. Every single idea failed.

That sounds bad. It is the opposite. It means the process worked — it caught thirteen ideas that
would have cost me money, including one that looked like a winner right up until I tested it
somewhere else.

---

## Where the idea came from

Not from a computer.

The starting point was watching price behaviour and noticing something repeat: price pushes past an
obvious level where a lot of orders are sitting, takes those orders out, and then immediately
reverses. The breakout fails. The people who bought the breakout are trapped.

That is a **market-structural** hypothesis. It describes a mechanism involving real participants
doing real things. It was observed first and written down as rules afterwards.

The alternative — searching historical data for patterns that made money and then inventing a story
for them — is the standard way to produce a strategy that works beautifully on the past and fails
immediately on the future. Nothing in this campaign was found that way.

## Pre-registration, and why it is the whole thing

**Pre-registration means writing down the test before you run it, and being stuck with what you
wrote.**

For every study, fixed in advance:

| what was fixed | why it has to be fixed *before* |
|---|---|
| The hypothesis, stated so it could fail | "This helps sometimes" cannot be wrong, so it cannot be tested |
| The significance threshold | Chosen afterwards, it is always whatever the result needs |
| The test statistic and the clustering unit | There are many ways to compute a p-value and they do not agree |
| The decision rule | Including what a pass would **not** authorise |
| A minimum sample size | So "we could not tell" stays separate from "it does not work" |
| Handling of ambiguous outcomes | Otherwise the ambiguous cases become whatever helps |

### The sample floor, in plain words

If you flip a coin four times and get three heads, you have not discovered anything about the coin.
You have too little information to say.

The floor is the number of trades below which the study cannot answer its own question. Declaring it
in advance means a study that comes up short gets recorded as **"we could not tell"** instead of
**"it does not work."** Those are different, and collapsing them permanently closes questions on
evidence that never existed.

One study in this campaign had 896 trades against a floor of 353 — so its failure is a real answer.
Another was closed for want of a holdout large enough to test anything, and is recorded that way.

### The null calibration, in plain words

Any filter that removes trades changes the results, because you have fewer trades and fewer trades
are noisier. So "it did better after filtering" proves nothing on its own.

The fix: **compare the filter against throwing away the same number of trades at random.**

If your clever rule does not beat a coin flip that discards the same amount, your clever rule is a
coin flip. This killed two filters that otherwise looked promising — one whose effect random
discarding matched **11.72% of the time**, and one whose result landed *exactly* on the 95th
percentile of 5,000 random relabellings.

### The look ledger, in plain words

Every time you look at the data and see an outcome, you get a little more chance of being fooled.
Look twenty times and something will look significant.

So every look was counted. The final claim is corrected for all of them. And each out-of-sample
block — data held back and never examined — gets **exactly one look, ever.** Once spent, it is gone,
and there is no second chance to get the answer you wanted.

## Scoring: drawdown, not return

Every result in this campaign is scored on **return per unit of drawdown**, not on return.

**Drawdown is how far down you go before you come back up.** If your account falls 30% before
recovering, that is a 30% drawdown, and it is the number that decides whether you are still trading
when the recovery arrives.

Return alone can be made arbitrarily large by taking more risk per trade. That is not a better
strategy — it is the same strategy with more leverage, and the drawdown grows exactly as fast. A
return figure quoted without its drawdown is not a result.

## Replication beats a stricter threshold

The single most useful thing this campaign learned.

One hypothesis passed its pre-registered test at p = 0.0312. A tighter threshold would not have
caught it — it would have passed at 0.01 on a slightly different draw. What caught it was **testing
the same idea on four other instruments**, where it ran from +8 points to −8 points and averaged
essentially zero.

The general version: an effect that is real should show up somewhere else. An effect that is noise
will not. Testing elsewhere is a cheaper and stronger check than demanding a smaller p-value on the
same data.

## What this methodology does not do

It does not make the strategy work. Thirteen studies produced zero confirmed hypotheses.

What it produces is a set of **closed questions** — things that are now known not to help, recorded
with the evidence, so that neither I nor anyone reading this spends time on them again.

In research that is the ordinary outcome and the reason the process exists. A campaign where
everything passed would be a campaign whose tests were too easy.
