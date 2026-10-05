---
name: market-regime
description: Use when characterizing the current market environment. Covers trend and volatility regimes, risk-on versus risk-off signals, macro context, and matching strategy to regime rather than fighting it.
metadata:
  category: finance
  version: 1.0.0
  tags: [regime, macro, volatility, risk-on, environment]
---

# Market Regime

## Purpose

Characterize the environment before selecting a strategy. A strategy that works in a trending, low-volatility regime frequently loses money in a choppy, high-volatility one — and the most common cause of a strategy "stopping working" is a regime change it was never designed to survive.

## When to Use

- Setting overall exposure and strategy selection.
- Explaining why a strategy that worked has stopped.
- Assessing whether conditions favor trend-following or mean-reversion.
- Periodic review of the environment.

## Capabilities

- Trend regime: trending versus range-bound.
- Volatility regime: expanding, contracting, and the level.
- Risk appetite: credit spreads, defensive versus cyclical leadership.
- Macro context: rates, the dollar, inflation expectations.
- Regime-appropriate strategy selection.

## Inputs

- Index price and volatility history.
- Cross-asset data: credit spreads, rates, currencies, commodities.
- Sector and factor performance.

## Outputs

- A regime characterization.
- Which strategies the regime favors and which it punishes.
- An exposure recommendation.

## Workflow

1. **Establish the trend regime** — Is the index above a rising long-term average, or chopping around a flat one? Trend-following requires a trend; in a range it bleeds.
2. **Establish the volatility regime** — The level and, more importantly, the direction. Expanding volatility from a low base is the most dangerous configuration for leveraged and short-volatility positions.
3. **Read the risk appetite** — Credit spreads widening while equities hold is a warning that the bond market disagrees. Defensive sectors leading in an advance is the same message.
4. **Note the macro backdrop** — Rates, the dollar, and inflation expectations set the constraint within which everything else operates.
5. **Match the strategy to the regime** — Do not run a mean-reversion strategy in a strong trend, and do not run a breakout strategy in a range. This is the entire point of the exercise.
6. **Re-assess on a schedule, not on impulse** — Weekly. Regimes change slowly; reacting to daily noise is the failure mode this is meant to prevent.

## Best Practices

- The most common cause of a strategy failing is a regime change, not a broken strategy. Diagnose the environment before you rewrite the code.
- Volatility clusters. A high-volatility day is followed by more high-volatility days far more often than chance. Expanding volatility means reduce size, immediately.
- Credit markets lead equity markets more often than the reverse. Widening high-yield spreads with equities at a high is a disagreement worth respecting.
- No regime lasts. The strategy that has worked for eighteen months is the one most at risk when conditions change, and it will have attracted the most capital by then.
- Do not predict the regime change. Observe it and adapt. Positioning for a change that has not happened is expensive.
- Reduce exposure when the regime is ambiguous. Ambiguity is itself information.

## Examples

**A regime read across dimensions:**

```python
def regime(market: MarketData) -> RegimeReport:
    spx, vix = market.spx, market.vix

    trend = (
        "trending_up"   if spx.close.iloc[-1] > spx.ma200.iloc[-1] and spx.ma200.diff(20).iloc[-1] > 0 else
        "trending_down" if spx.close.iloc[-1] < spx.ma200.iloc[-1] and spx.ma200.diff(20).iloc[-1] < 0 else
        "range"
    )

    vix_now, vix_avg = vix.close.iloc[-1], vix.close.rolling(63).mean().iloc[-1]
    vol = (
        "expanding" if vix_now > vix_avg * 1.25 else
        "contracting" if vix_now < vix_avg * 0.80 else
        "stable"
    )
    vol_level = "low" if vix_now < 15 else "elevated" if vix_now < 25 else "high"

    # Cross-asset risk appetite: does the credit market agree with the equity market?
    credit_stress = market.hy_spread.iloc[-1] > market.hy_spread.rolling(126).quantile(0.75).iloc[-1]
    defensive_leading = (
        market.sector_returns_63d[["utilities", "staples", "healthcare"]].mean()
        > market.sector_returns_63d[["tech", "discretionary", "financials"]].mean()
    )

    return RegimeReport(
        trend=trend,
        volatility=f"{vol_level}_{vol}",
        risk_appetite="off" if (credit_stress or defensive_leading) else "on",

        favors=STRATEGY_FIT[(trend, vol)],
        punishes=STRATEGY_ANTI_FIT[(trend, vol)],
    )


STRATEGY_FIT = {
    ("trending_up", "contracting"):  ["trend-following", "momentum", "breakouts"],
    ("trending_up", "expanding"):    ["reduce size", "tighten stops"],
    ("range", "contracting"):        ["mean-reversion", "premium selling"],
    ("range", "expanding"):          ["cash", "wait"],
    ("trending_down", "expanding"):  ["cash", "defensive", "hedges"],
}
```

**A read that explains a strategy's failure:**

```text
Regime, as of this week:

Trend         : range. SPX has oscillated in a 6% band for 11 weeks. The 200-day
                is flat.
Volatility    : elevated and expanding. VIX 24, up from a 63-day average of 17.
Risk appetite : OFF. High-yield spreads at the 82nd percentile of the last six
                months. Utilities and staples leading over 63 days.
Macro         : 10-year yield +80bp over the quarter. Dollar strengthening.

Favors  : mean-reversion at the range extremes, reduced size, cash.
Punishes: breakout strategies (every breakout has failed — that IS the range),
          trend-following (there is no trend), short volatility (expanding).

This explains the drawdown. The breakout strategy has not stopped working; it is
being run in the one regime that is designed to defeat it. Every breakout in a
range is a false breakout by definition — that is what makes it a range.

Action: reduce breakout allocation until the index closes outside the range on
above-average volume. Do not rewrite the strategy.
```

## Notes

- The insight in the example is the practically valuable one: a strategy in a drawdown is more often in the wrong regime than broken. Changing the strategy at that point usually means optimizing it for a regime that is about to end.
- Volatility clustering is one of the most robust empirical findings in finance. Expanding volatility genuinely predicts more volatility, which makes it the most actionable regime input.
- This is educational material about regime-analysis methodology, not financial advice or a market forecast.
