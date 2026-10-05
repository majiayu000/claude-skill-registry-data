---
name: polymarket
description: Use when natural-language interface to Polymarket prediction markets.
  Ask questions about event probabilities, market odds, price movements, and betting
  strategies in plain English. event probabilities, or when user asks about Polymarket
  data. Use when working with polymarket.
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
- algorithms
- markets
- polymarket
- trading
version: 1.0.0
category: trading
---

# Polymarket

## When to Use

**Trigger phrases:**
- "polymarket"
- "Help me with polymarket"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Query prediction market data from Polymarket's public API (no auth required).


## When NOT to Use

- When you cannot afford to lose the capital at risk
- For instruments you do not understand
- When emotional state impairs judgment (revenge trading, FOMO)


## Overview

Polymarket provides market analysis capabilities with risk management.

## Workflow

```python
# Example: Position sizing (Kelly Criterion)
def kelly_size(win_rate: float, avg_win: float, avg_loss: float) -> float:
    if avg_loss == 0: return 0
    b = avg_win / abs(avg_loss)
    kelly = (win_rate * b - (1 - win_rate)) / b
    return max(0, min(kelly * 0.5, 0.02))  # Half-Kelly, max 2%
```

1. **Research** — Analyze market conditions and opportunities
2. **Plan** — Define entry, exit, and position sizing
3. **Execute** — Place trades with proper order types
4. **Monitor** — Track positions and market changes
5. **Manage risk** — Apply stop-losses and hedging
6. **Review** — Post-trade analysis and journaling

## Risk Management

- Never risk more than 1-2% of portfolio per trade
- Set stop-loss before entering any position
- Diversify across uncorrelated assets
- Size positions based on volatility (ATR)
- Have a maximum daily loss limit

## Key Metrics

- Win rate and profit factor
- Sharpe ratio and max drawdown
- Average risk-reward ratio
- Expectancy per trade
- Correlation to benchmark

## Discipline Rules

- Follow your trading plan — no impulsive trades
- Cut losses short, let winners run
- Review every trade in your journal
- Never revenge trade after a loss
- Take breaks after consecutive losses

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |


## Process

1. **Scope** — Define research questions, identify data sources, set time boundaries
1. **Gather** — Collect data from primary sources, APIs, and public records
1. **Synthesize** — Analyze findings, identify patterns, produce actionable report

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings