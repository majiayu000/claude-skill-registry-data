---
skill_id: trading_strategy_guidelines
name: Trading Strategy Guidelines
version: 1.0.0
description: Core trading strategy rules and guidelines for consistent execution
author: Trading System CTO
tags: [trading-strategy, rules, guidelines, momentum, macd, rsi]
---

# Trading Strategy Guidelines

Core rules and guidelines for our momentum-based trading system.

## Strategy Overview

**Type**: Momentum-based with technical indicators
**Daily Investment**: $10/day ($7 Core + $3 Growth)
**Risk Management**: 2% daily loss limit, 10% max drawdown

## Entry Rules (All Must Pass)

### 1. MACD Momentum Filter
- **Required**: MACD histogram > 0 (bullish momentum)
- **Rejection**: If MACD histogram < 0 → SKIP symbol
- **Rationale**: Only trade with the trend

### 2. RSI Overbought Filter
- **Required**: RSI < 70 (not overbought)
- **Rejection**: If RSI > 70 → SKIP symbol
- **Rationale**: Avoid buying at peaks

### 3. Volume Confirmation
- **Required**: Volume > 20-day average
- **Rejection**: If volume < average → SKIP symbol
- **Rationale**: Confirm momentum with volume

## Position Sizing

- **Tier 1 (Core)**: $7/day - SPY, QQQ, VOO
- **Tier 2 (Growth)**: $3/day - Individual stocks
- **Max Position**: 10% of portfolio per symbol
- **Risk per Trade**: 1-2% of portfolio

## Exit Rules

1. **Stop-Loss**: 5% trailing stop (Tier 1), 3% (Tier 2)
2. **Profit Target**: Take profits at 10% gain
3. **MACD Reversal**: Exit on bearish MACD crossover
4. **RSI Overbought**: Exit if RSI > 70 after entry

## Data Source Priority

1. **Cache** (if recent)
2. **Alpaca API** (primary reliable source)
3. **Polygon.io** (secondary reliable source)
4. **Disk Cache** (if < 24 hours old)
5. **yfinance** (last resort, unreliable)
6. **Alpha Vantage** (avoid - rate-limited)

## Philosophy

- **Better to sit in cash than fight the trend**
- **Only trade when all filters pass**
- **Use reliable data sources first**
- **Fail fast on API errors**

## Integration

These guidelines are enforced in:
- `src/strategies/core_strategy.py`
- `src/strategies/growth_strategy.py`
- `src/utils/market_data.py`
