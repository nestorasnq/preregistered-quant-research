# P1 — ES/NQ correlation state

**Verdict: FAILED.** Effect present, not significant, and costly to apply.

## Hypothesis

The prevailing correlation state between ES1! and NQ1! predicts the outcome of entries taken on
either instrument. Trades taken while the pair is in one correlation regime outperform those
taken in the other.

**Why it was worth testing.** ES and NQ are two expressions of the same underlying risk appetite,
and they decouple in identifiable conditions — rotation between growth and value, single-name
concentration in the Nasdaq, rate-sensitivity divergence. If a liquidity sweep at a
higher-timeframe level means something different when the two indices disagree than when they
move together, the correlation state is information the entry rules do not currently see.

That is a structural argument, not a data-mining one, which is why it was the campaign's first
primary.

## Fixed before collection

| | |
|---|---|
| test | ISO-week-clustered permutation between the two correlation-state groups |
| resamples | 10,000 |
| clustering | whole ISO weeks, to preserve within-week dependence |
| decision rule | the filtered set must clear the unfiltered set, **and** the filtered configuration must improve the book on a drawdown-adjusted basis |

The second half of the decision rule was deliberate. A filter that improves the win rate while
discarding enough trades to worsen the return per unit of drawdown has not helped.

## Result

**+2.76 percentage points, p = 0.172.**

The effect pointed the right way and did not clear the threshold.

The drawdown-adjusted leg settled it independently: applying the filter costs **−31.5% of annual
return**. The trades it removes are not disproportionately losers; there are simply fewer of them,
and the compounding of a thinner trade stream loses more than the improved rate gains.

## Ruling

Closed. The correlation state is not used.

**What was learned beyond the verdict:** an effect of +2.76 pp that fails at p = 0.172 is exactly
the size and shape of thing that survives in a campaign without a pre-registered threshold. It
would have been easy to report as "a modest edge." The threshold is what stopped it.
