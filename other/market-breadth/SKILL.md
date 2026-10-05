---
name: market-breadth
description: Use when assessing the internal health of a market advance or decline. Covers advance-decline lines, new highs versus new lows, percentage above moving averages, and divergence between the index and its constituents.
metadata:
  category: finance
  version: 1.0.0
  tags: [breadth, market-internals, divergence, participation]
---

# Market Breadth

## Purpose

Determine whether a market move is broad or narrow. An index at a new high driven by five stocks while most constituents are falling is a different market from an index at a new high with broad participation — and the index price alone cannot tell you which one you are in.

## When to Use

- Assessing whether an advance is healthy or narrowing.
- Looking for divergence between the index and its internals.
- Confirming a bottom or identifying a distribution phase.
- Setting overall exposure based on market health.

## Capabilities

- Advance-decline line and its divergence from price.
- New highs versus new lows.
- Percentage of constituents above their moving averages.
- Equal-weight versus cap-weight index comparison.
- Volume breadth: up volume versus down volume.

## Inputs

- Constituent-level data for the index, not just the index price.
- A long enough history to establish what is normal.

## Outputs

- A characterization: broadening, narrowing, or neutral.
- Any divergence between the index and its internals.
- An implication for exposure.

## Workflow

1. **Compare the index with the equal-weight version** — Cap-weighted rising while equal-weighted falls means a handful of large constituents are carrying the index. This is the fastest breadth read available and requires two data series.
2. **Track the advance-decline line** — Cumulative advancers minus decliners. When it diverges from the index — the index makes a new high, the A/D line does not — participation is narrowing.
3. **Watch new highs versus new lows** — In a healthy advance, new highs expand. New highs contracting while the index rises is deterioration.
4. **Measure the percentage above the 200-day** — A broad advance has most constituents above their long-term average. An index at a high with 45% of constituents above their 200-day is being carried.
5. **Act on the divergence, not on the level** — Breadth is a warning system, not a timing tool. Narrowing breadth can persist for months. It argues for reduced size, not for a short.

## Best Practices

- The single most useful breadth signal is the cap-weight versus equal-weight divergence. It is trivial to compute and it captures the essential question: is the index the market, or is it a few names?
- Divergences can persist far longer than seems reasonable. Breadth deterioration is a reason to reduce exposure, not a reason to bet against the index.
- Breadth improving from a washed-out level is a more reliable signal than breadth deteriorating from a strong one. Bottoms are marked by expanding participation; tops are a slow narrowing that can last a year.
- Use breadth to set exposure, not to select instruments. It is a market-level input.
- A single day's breadth reading is noise. Look at the trend over weeks.
- New lows expanding while the index is flat is the more dangerous configuration — it means damage is being done beneath a stable surface.

## Examples

**The essential breadth comparison:**

```python
def breadth_summary(constituents: pd.DataFrame, index: pd.Series) -> BreadthReport:
    ma200 = constituents.rolling(200).mean()
    ma50  = constituents.rolling(50).mean()

    pct_above_200 = (constituents.iloc[-1] > ma200.iloc[-1]).mean()
    pct_above_50  = (constituents.iloc[-1] > ma50.iloc[-1]).mean()

    # 52-week highs and lows among constituents.
    new_highs = (constituents.iloc[-1] >= constituents.rolling(252).max().iloc[-1]).sum()
    new_lows  = (constituents.iloc[-1] <= constituents.rolling(252).min().iloc[-1]).sum()

    # The core question: is the index the market, or is it a handful of names?
    equal_weight = constituents.pct_change().mean(axis=1).add(1).cumprod()
    cap_weight   = index / index.iloc[0]

    divergence_63d = (
        (cap_weight.iloc[-1] / cap_weight.iloc[-63] - 1)
        - (equal_weight.iloc[-1] / equal_weight.iloc[-63] - 1)
    )

    return BreadthReport(
        pct_above_200=pct_above_200,
        pct_above_50=pct_above_50,
        new_highs=int(new_highs),
        new_lows=int(new_lows),
        cap_vs_equal_63d=divergence_63d,
        state=(
            "narrowing" if divergence_63d > 0.03 and pct_above_200 < 0.50 else
            "broadening" if divergence_63d < -0.01 and pct_above_200 > 0.60 else
            "neutral"
        ),
    )
```

**A breadth read that changes what you do:**

```text
S&P 500, as of the close:

Index                    : at a 52-week high.
Equal-weight (RSP)       : 6.1% below ITS 52-week high.
Cap vs equal, 63 days    : +7.4%   <- the index is being carried

% above 200-day MA       : 47%     <- fewer than half of constituents are in
                                      a long-term uptrend, at an index high
% above 50-day MA        : 41%
New 52-week highs        : 22
New 52-week lows         : 38      <- more constituents at lows than at highs,
                                      with the index at a high

Read: the advance is narrow and deteriorating. Fewer than half of the index's
constituents are above their 200-day average while the index prints a new high.
More names are making new lows than new highs.

Implication: reduce gross exposure and tighten stops. NOT a short signal —
narrow advances have persisted for a year or more. This is a position-sizing
input, not a directional one.
```

## Notes

- The configuration in the example — index at a high, fewer than half of constituents above their 200-day, new lows exceeding new highs — has preceded most significant market tops. It has also occurred without one. It is a risk input, not a prediction.
- Breadth data requires constituent-level history. Index price alone cannot produce any of this, which is precisely why breadth adds information.
- This is educational material about market-internals methodology, not financial advice or a market forecast.
