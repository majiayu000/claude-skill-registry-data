---
name: technical-analysis
description: |
  Systematic chart reading and technical analysis for NSE/BSE Indian equities.
  Covers trend identification, support/resistance mapping, volume analysis, indicator dashboards,
  and probabilistic scenario building. Uses Groww MCP for live data and yfinance for history.

  Use when the user asks to: read a chart, identify trends, find support/resistance levels, check
  indicators (RSI, MACD, Bollinger, ADX, Stochastic), analyze volume, or build trade scenarios.
  Triggers on: "what's the trend on [stock]", "support resistance for [stock]", "indicators for
  [stock]", "is [stock] bullish or bearish", "volume analysis", "chart analysis", or any request
  to interpret price action on Indian equities.
---

# Technical Analysis

Read the chart systematically — don't cherry-pick indicators that confirm a bias.

## Prerequisites

No hard dependencies. Works best with Groww MCP or yfinance for live data, but can analyze any stock if you provide prices manually.

## Data Collection

When data tools are available, fetch in this order:

1. **Resolve symbol**: `search_stock_and_others_symbol` on Groww
2. **Live quote**: `get_quotes_and_depth` for current price, volume, day range
3. **Indicators**: `get_historical_technical_indicators` for SMA, EMA, RSI, MACD, Bollinger, ADX
4. **Candles**: `fetch_historical_candle_data` with `interval=1d` for at least 200 days
5. **Long history** (if needed): `yf.download("SYMBOL.NS", period="2y")` via yfinance

## Step 1: Trend Identification

- **Primary trend** (weekly): Higher highs & higher lows = uptrend. Lower highs & lower lows = downtrend.
- **Secondary trend** (daily): Current swing direction within the primary trend.
- **Moving average alignment**:
  - Price > SMA20 > SMA50 > SMA200 = strong uptrend
  - Price < SMA20 < SMA50 < SMA200 = strong downtrend
  - Mixed = transitional / choppy
- **Cross signals**: Golden cross (SMA50 > SMA200) = bullish. Death cross = bearish.

## Step 2: Support & Resistance

- **Horizontal S/R**: Recent swing highs and lows with at least 2 touches
- **Round numbers**: Psychological levels (Rs.1,000, Rs.1,500, Rs.2,000)
- **Volume clusters**: Zones where heavy trading occurred (act as magnets)
- **Dynamic S/R**: SMA20 (short-term), SMA50 (medium), SMA200 (major)
- **Gap zones**: Unfilled gaps act as support (gap up) or resistance (gap down)

## Step 3: Volume Analysis

| Price Action | Volume | Interpretation |
|-------------|--------|----------------|
| Rising price | Rising volume | Strong move — trend healthy |
| Rising price | Falling volume | Weak rally — suspect, may reverse |
| Falling price | Rising volume | Strong selling — trend acceleration |
| Falling price | Falling volume | Selling exhaustion — bounce possible |
| Spike volume at support | — | Potential capitulation / reversal |
| Spike volume at resistance | — | Breakout attempt or distribution |

Compare current volume to 20-day average. >1.5x = significant.

## Step 4: Indicator Dashboard

Pull via `get_historical_technical_indicators`:

| Indicator | Bullish | Bearish | Neutral |
|-----------|---------|---------|---------|
| RSI(14) | >50, rising from <30 | <50, falling from >70 | 40-60, flat |
| MACD | Line > Signal, histogram growing | Line < Signal, histogram shrinking | Near zero line |
| Bollinger Bands | Price bouncing off lower band | Price rejected at upper band | Walking the band |
| ADX | >25 with +DI > -DI | >25 with -DI > +DI | <20 (no trend) |
| Stochastic | %K crosses above %D below 20 | %K crosses below %D above 80 | Mid-range |

Count bullish vs bearish signals to gauge overall bias.

## Step 5: Probabilistic Scenarios

Always present 2-3 scenarios with rough probabilities. Assign higher probability to the scenario with more technical evidence.

```
SCENARIO A (Bullish) — XX% probability
- Trigger: [specific price/indicator condition]
- Target: Rs.XXX (nearest resistance / Fib level)
- Invalidation: Close below Rs.XXX

SCENARIO B (Bearish) — XX% probability
- Trigger: [specific condition]
- Target: Rs.XXX (nearest support)
- Invalidation: Close above Rs.XXX

SCENARIO C (Sideways) — XX% probability
- Range: Rs.XXX to Rs.XXX
- Duration estimate: X days/weeks
- Breakout signal: [what to watch]
```

Probabilities should sum to ~100%. Base them on: trend alignment, indicator consensus, volume confirmation, and S/R proximity.
