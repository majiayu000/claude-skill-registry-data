---
name: capital-proportional-limits
description: "Use percentage-based capital limits, not hard-coded dollar amounts. Trigger when: (1) trades blocked on small accounts, (2) min_cash_buffer is absolute dollars, (3) capital allocation doesn't scale with account size, (4) fixed dollar thresholds in risk code."
author: Claude Code
date: 2024-12-24
---

# Capital Manager Proportional Limits

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-24 |
| **Goal** | Fix capital manager blocking trades with hard-coded dollar amounts |
| **Environment** | scripts/live_trader.py, alpaca_trading/risk/capital_manager.py |
| **Status** | Success |

## Context

The capital manager was initialized with `min_cash_buffer=1000.0` - a fixed dollar amount that:
1. **Blocked 20% of a $5,000 account** - Leaving only $4,000 for trading
2. **Blocked 10% of a $10,000 account** - Still significant
3. **Blocked only 1% of a $100,000 account** - Negligible

The 30% safety buffer (percentage-based) already provides proportional protection. The extra $1,000 was redundant and harmful for smaller accounts.

## Verified Workflow

### Problem Pattern

```python
# WRONG: Hard-coded dollar amount
capital_mgr = CapitalManager(
    safety_buffer_pct=0.30,
    trading_allocation_pct=0.70,
    max_position_pct=0.20,
    min_cash_buffer=1000.0  # <-- Blocks 20% of $5k account!
)
```

### Solution: Use Percentage-Based Limits

```python
# CORRECT: Let percentage-based safety buffer handle it
capital_mgr = CapitalManager(
    safety_buffer_pct=0.30,       # 30% safety buffer (proportional)
    trading_allocation_pct=0.70,  # 70% available for trading
    max_position_pct=0.20,        # 20% max per position
    # min_cash_buffer defaults to 0.0 - safety buffer is proportional
)
```

### Capital Manager Design

The `CapitalManager` class is correctly designed with percentage-based defaults:

```python
class CapitalManager:
    def __init__(
        self,
        safety_buffer_pct: float = 0.30,      # 30% reserved
        trading_allocation_pct: float = 0.70,  # 70% for trading
        max_position_pct: float = 0.20,        # 20% max per position
        min_cash_buffer: float = 0.0,          # Additional cash buffer (default: none)
        min_trade_value: float = 1.0           # Supports fractional shares
    ):
```

The `min_cash_buffer` parameter exists for edge cases but should rarely be used since the percentage-based safety buffer already scales with account size.

### Impact Analysis

| Account Size | Old (with $1,000 buffer) | New (0% buffer) | Improvement |
|-------------|--------------------------|-----------------|-------------|
| $5,000 | $4,000 available | $5,000 available | +25% |
| $10,000 | $9,000 available | $10,000 available | +11% |
| $50,000 | $49,000 available | $50,000 available | +2% |
| $100,000 | $99,000 available | $100,000 available | +1% |

Note: The 30% safety buffer still applies to all accounts, so actual trading capital is 70% of these values.

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Hard-coded $1,000 min_cash_buffer | Disproportionately hurt small accounts | Use percentage-based limits only |
| Hard-coded $50 in strategies | Same problem at smaller scale | Remove absolute dollar amounts |
| Fixed confidence thresholds | Didn't adapt to volatility regimes | Consider adaptive thresholds |
| Hard-coded stop-loss percentages | Didn't account for asset volatility | Consider asset-specific thresholds |

## Key Insights

### Percentage-Based vs Dollar-Based

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **Percentage-based** | Scales with account, fair to all sizes | May allow tiny trades on small accounts | Default - almost always |
| **Dollar-based** | Prevents dust trades | Unfair to small accounts, doesn't scale | Only for minimum trade value |

### Other Hard-Coded Values to Watch

These were identified during investigation (not fixed yet):

```python
# In live_trader.py - consider making configurable:
confidence = 0.6       # Default fallback confidence
rl_confidence < 0.4    # Minimum RL confidence threshold
confidence < 0.70      # Extreme volatility threshold
base_breakeven = 0.02  # 2% breakeven stop
base_trailing = 0.05   # 5% trailing stop

# In harmonized.py:
min_cash_buffer = 50.0  # Should also be removed
```

### The 30% Safety Buffer

The existing safety buffer provides strong protection:

```python
# How it works:
conservative_value = account_value - unrealized_profits + unrealized_losses
safety_buffer = conservative_value * 0.30  # 30% reserved
available_capital = conservative_value * 0.70  # 70% for trading

# For a $10,000 account:
# - Safety buffer: $3,000 (never touched)
# - Trading capital: $7,000
# - Max per position: $1,400 (20% of $7,000)
```

### Files Modified

```
scripts/live_trader.py:
  - Line 1751-1756: Removed min_cash_buffer=1000.0
  - Added comment explaining proportional protection
```

## References
- `alpaca_trading/risk/capital_manager.py`: Lines 74-100 (class design)
- `scripts/live_trader.py`: Lines 1750-1757 (initialization)
- CLAUDE.md: Risk Controls section
