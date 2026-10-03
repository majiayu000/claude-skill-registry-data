---
name: stop-loss-strategies
description: |
  Stop-loss placement strategies for NSE/BSE equity trades. Covers structure-based, ATR-based,
  support/resistance-based, and moving average-based stops with buffer rules and hard limits.

  Use when the user asks: "where to set stop-loss", "stop-loss for [stock]", "how to protect
  this trade", "what's a good stop level", "risk management for [position]", or any question
  about initial stop-loss placement for Indian equity trades.
---

# Stop-Loss Strategies

A stop-loss is not optional. Every position needs one before entry. The purpose is to cap your maximum loss — not to predict where price will go.

## Prerequisites

No dependencies required. Provide entry price and key levels manually. Enhanced with Groww MCP (candles, ATR, MAs) or yfinance (`pip install yfinance`).

## Data Needed

1. **Entry price**: Known or planned
2. **Recent candles**: `fetch_historical_candle_data` (daily, last 60 days) or user-provided levels
3. **ATR(14)**: `get_historical_technical_indicators` from Groww, or calculate manually
4. **Key S/R levels**: From technical-analysis skill or swing highs/lows
5. **Moving averages**: SMA20, SMA50, SMA200

## Stop Type Selection

| Method | Best For | How to Calculate |
|--------|----------|-----------------|
| Structure-based | Swing trades, clear chart patterns | Below recent swing low (long) or above swing high (short) |
| ATR-based | Volatile stocks, no clear structure | Entry - ATR(14) × 1.5 to 2.0 |
| Support/Resistance | Range-bound markets, clear levels | Below key support level + buffer |
| Moving Average | Trend-following trades | Below SMA20 (aggressive) or SMA50 (conservative) |

### Structure-Based (Preferred)
Find the most recent swing low (for longs) that, if broken, would invalidate your trade thesis.
```
Stop = Recent swing low - buffer
Buffer = 0.5% for large-caps, 1% for mid/small-caps
```

### ATR-Based
Adapts to the stock's natural volatility:
```
Stop (long) = Entry - ATR(14) × multiplier
Stop (short) = Entry + ATR(14) × multiplier

Multiplier: 1.5 (tight) to 2.0 (standard) to 2.5 (loose)
```

### Support/Resistance-Based
Place stop just below a confirmed support level:
```
Stop = Support level × (1 - buffer%)
Buffer: 0.5% large-cap, 1.0% mid/small-cap
```
Only use levels with at least 2 historical touches.

### Moving Average-Based
For trend-following positions:
```
Aggressive: Stop below SMA20 (for short-term trends)
Moderate: Stop below SMA50 (for medium-term trends)
Conservative: Stop below SMA200 (for long-term holds)
```
Best when MA is clearly sloping in your direction.

## Buffer Rules

- Round stop to nearest Rs.5 or Rs.10 for cleaner levels
- Use **closing price** as trigger, not intraday wicks (unless day trading)
- Add extra buffer if the stock has a history of stop-hunting wicks
- For illiquid stocks (avg volume < 50K/day), use wider buffers (1.5-2%)

## Hard Rules

These are non-negotiable:

1. **Max loss per trade**: 2% of capital (1% if using leverage)
2. **Never move stop further away** — only tighten or leave unchanged
3. **If stop hits**: exit immediately at next open. No "let me wait for close"
4. **Pre-set the stop**: Decide before entering. Don't adjust based on emotions after entry
5. **No mental stops**: Use actual stop-loss orders on Groww if possible, or set hard price alerts

## Stop Validation

Before finalizing, check:
- [ ] Is the stop beyond normal noise? (At least 1× ATR away from entry)
- [ ] Does the position size at this stop keep risk within limits?
- [ ] Is the R:R ratio still acceptable? (→ check with risk-reward-ratio skill)
- [ ] Is the stop below a meaningful technical level, not just a round number?
