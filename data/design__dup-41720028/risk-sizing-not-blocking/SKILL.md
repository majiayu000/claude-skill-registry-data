---
name: risk-sizing-not-blocking
description: "Risk managers should SIZE trades, not BLOCK them. Trigger when: (1) capital manager blocks trades, (2) risk manager rejects orders, (3) trades fail due to 'exceeds limit', (4) components don't work in harmony."
author: Claude Code
date: 2024-12-24
---

# Risk Sizing Not Blocking

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-24 |
| **Goal** | Refactor risk/capital managers from blocking trades to sizing them correctly |
| **Environment** | scripts/live_trader.py, alpaca_trading/risk/ |
| **Status** | Success |

## Context

The trading system had multiple components that could BLOCK trades:
1. **Capital Manager**: `check_trade_allowed()` returned False if trade exceeded limits
2. **Portfolio Risk Manager**: `check_position_limits()` returned False for VaR/concentration violations

This caused problems:
- Trades were rejected after signal generation
- Components didn't work in harmony
- Orders sized upstream were blocked downstream

**Architectural Principle**: All trading system components should work in harmony. There should never be an order that is sized too large for capital management.

## Verified Workflow

### The Wrong Pattern (Blocking)

```python
# WRONG: Check if arbitrary size is allowed, block if not
estimated_qty = cash_available * alloc / price
allowed, reason = capital_mgr.check_trade_allowed(allocation, estimated_qty * price, symbol)
if not allowed:
    logger.warning(f"{symbol}: Capital Manager BLOCKED trade: {reason}")
    return state, {"skip_reason": "capital_limit"}  # Trade rejected!
```

### The Correct Pattern (Sizing)

```python
# CORRECT: Get max allowed size, use it as constraint
max_qty_from_capital = capital_mgr.get_max_trade_size(
    allocation=capital_allocation,
    symbol=symbol,
    current_price=price,
    positions=positions_dict
)

# Later, during GARCH sizing:
qty = garch_mgr.calculate_position_size(...)
qty = min(qty, max_qty_from_capital)  # Apply constraint
# Order executes with correct size - no blocking needed
```

### Complete Sizing Flow

```python
# 1. Capital Manager provides max qty from allocation
if capital_allocation is not None and capital_mgr is not None:
    max_qty_from_capital = capital_mgr.get_max_trade_size(
        allocation=capital_allocation,
        symbol=symbol,
        current_price=price,
        positions=positions_dict
    )
    if max_qty_from_capital <= 0:
        return state, {"skip_reason": "no_capacity"}  # Only skip if truly zero
else:
    max_qty_from_capital = float('inf')

# 2. Risk Manager provides max qty from position limits
if portfolio_risk_mgr is not None:
    max_value_from_risk = portfolio_metrics.total_value * 0.20  # 20% max
    max_qty_from_risk = max_value_from_risk / price
    max_qty_from_capital = min(max_qty_from_capital, max_qty_from_risk)

# 3. GARCH calculates initial size
qty = garch_mgr.calculate_position_size(symbol, account_value, signal_strength, price, returns)

# 4. Apply all constraints
qty = min(qty, max_qty_from_alloc)      # Allocation limit
qty = min(qty, max_qty_from_capital)     # Capital + risk limits
qty = qty * position_scale               # Drawdown scaling

# 5. Execute with correct size
executor.submit(symbol, qty=qty, side=entry_side, type="limit")
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| `check_trade_allowed()` blocking | Rejected trades after signal generation | Use `get_max_trade_size()` for constraints |
| `check_position_limits()` blocking | Portfolio risk rejected sized trades | Apply limits as max position value constraint |
| Estimate size then check | Estimated size != final size, caused false blocks | Get max size first, use as constraint |
| Hard-coded $1000 min_cash_buffer | Blocked trades on small accounts | Use percentage-based limits only |

## Key Insights

### Harmony Principle

All trading system components should work together:

```
Signal Generation → Sizing → Risk Constraints → Execution
      ↓               ↓            ↓              ↓
   Direction      Initial qty   Apply limits   Correct size
```

NOT:

```
Signal Generation → Sizing → Risk Check → BLOCKED!
```

### When to Skip vs When to Size

| Situation | Action |
|-----------|--------|
| No capacity at all (max_qty = 0) | Skip with "no_capacity" |
| Low confidence signal | Reject signal (not a blocking issue) |
| Size exceeds limit | Reduce size to limit (don't block) |
| Risk limit exceeded | Reduce size to risk limit (don't block) |

### Methods That Size vs Methods That Block

| Method | Purpose | Use For |
|--------|---------|---------|
| `get_max_trade_size()` | Returns max qty | Sizing constraints |
| `calculate_allocation()` | Returns capacity info | Sizing constraints |
| `check_trade_allowed()` | Returns bool | **AVOID** - causes blocking |
| `check_position_limits()` | Returns bool | **AVOID** - causes blocking |

### Files Modified

```
scripts/live_trader.py:
  - Lines 1375-1391: Capital manager sizing (removed check_trade_allowed)
  - Lines 1393-1411: Risk manager sizing (removed check_position_limits)
  - Lines 1466-1467: Apply max_qty_from_capital constraint
```

## References
- `alpaca_trading/risk/capital_manager.py`: `get_max_trade_size()` at lines 284-350
- `alpaca_trading/risk/portfolio_risk.py`: RiskLimits at lines 20-35
- `scripts/live_trader.py`: Sizing flow at lines 1375-1505
