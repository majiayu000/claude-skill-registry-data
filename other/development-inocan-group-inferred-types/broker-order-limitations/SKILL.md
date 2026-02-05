---
name: broker-order-limitations
description: "Alpaca broker limitations: crypto shorts blocked (broker doesn't support), stock shorts allowed. Trigger when: (1) shorting gate blocks wrong assets, (2) SELL signals blocked, (3) order type confusion."
author: Claude Code
date: 2024-12-26
---

# Broker Order Limitations (Alpaca)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-26 |
| **Goal** | Document broker-specific order limitations |
| **Environment** | scripts/live_trader.py, Alpaca Trading API |
| **Status** | Reference |

## Context

Alpaca broker has specific limitations on order types. The most important one for this trading system:

**Crypto shorting is NOT supported by Alpaca.** Stock shorting IS allowed.

This distinction is critical because:
1. Model generates SELL signals for both crypto and equities
2. SELL signal on crypto = blocked by broker limitation
3. SELL signal on equities = allowed (short selling)

## Verified Implementation

### Crypto Short Gate (Correct)

```python
# In live_trader.py (~line 1335)
# Only block shorts for crypto, not equities
if desired_side == -1 and asset_type == AssetType.CRYPTO and state.side <= 0:
    # Trying to go short on crypto when not already long
    gate_statuses[symbol] = GateStatus(
        final_status='BLOCKED',
        blocking_gate='crypto_short',
        crypto_short_gate=False,  # Failed
    )
    continue
```

### Key Logic Points

```python
# desired_side == -1: Model wants to SELL
# asset_type == AssetType.CRYPTO: Asset is cryptocurrency
# state.side <= 0: Not currently holding a long position

# All three conditions must be true to block:
# 1. SELL signal (-1)
# 2. Is crypto (not equity)
# 3. Would be opening a short (not closing a long)
```

### What IS Allowed

| Asset Type | Buy (Long) | Sell to Close | Sell to Short |
|------------|------------|---------------|---------------|
| **Equity** | Yes | Yes | Yes |
| **Crypto** | Yes | Yes | **NO** |

### Gate Status in Dashboard

When crypto short is blocked:
```python
gate_status = {
    'final_status': 'BLOCKED',
    'blocking_gate': 'crypto_short',
    'crypto_short_gate': False,
    # ... other gates may be True
}
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Block all SELL signals for crypto | Prevented closing profitable longs | Only block new shorts |
| Block all shorts (crypto + equity) | Equity shorts are valid strategy | Check asset type |
| No short gate at all | Orders rejected by broker | Pre-filter before submission |
| Check `desired_side < 0` | Could catch rounding errors | Use `== -1` exactly |

## Alpaca Order Types Reference

### Supported Order Types

| Order Type | Equities | Crypto |
|------------|----------|--------|
| Market Buy | Yes | Yes |
| Market Sell | Yes | Yes (close only) |
| Limit Buy | Yes | Yes |
| Limit Sell | Yes | Yes (close only) |
| Stop Loss | Yes | Yes |
| Take Profit | Yes | Yes |
| Short Sell | Yes | **NO** |
| Fractional | Yes (0.001) | Yes (varies) |

### Crypto-Specific Limitations

1. **No shorting**: Cannot borrow and sell crypto
2. **24/7 trading**: No market hours restrictions
3. **Symbol format**: Ends with `USD` (e.g., `BTCUSD`, `ETHUSD`)
4. **Fractional minimum**: Varies by crypto (check API)

### Equity-Specific Features

1. **Short selling**: Allowed with margin account
2. **Market hours**: 9:30 AM - 4:00 PM ET (regular)
3. **Extended hours**: 4:00 AM - 8:00 PM ET (with flag)
4. **Pattern day trader**: Rules apply if >3 day trades in 5 days

## Key Insights

### Detecting Asset Type

```python
# Simple heuristic used in live_trader.py
def is_crypto(symbol: str) -> bool:
    return symbol.endswith('USD')

# Or use Alpaca's asset class
from alpaca.trading.enums import AssetClass
asset = api.get_asset(symbol)
is_crypto = asset.asset_class == AssetClass.CRYPTO
```

### Why Not Block at Model Level?

The model is trained on both crypto and equity data. It learns:
- When to go long (BUY = +1)
- When to go short (SELL = -1)
- When to stay out (HOLD = 0)

Blocking shorts in the model would:
- Reduce training efficiency
- Create inconsistent behavior
- Miss valid equity short signals

**Better approach**: Let model predict freely, filter at execution gate.

### Capital Shift Interaction

When equity markets close, capital shifts to crypto. During this time:
- More crypto signals generated
- All crypto SELL signals blocked
- Only crypto BUY signals executed
- Effective strategy: crypto long-only overnight

## Files Modified

```
scripts/live_trader.py:
  - Line 1335: Crypto short gate check
  - Uses AssetType enum for asset classification
  - Gate status stored in gate_statuses dict
```

## References
- [Alpaca Crypto Trading](https://alpaca.markets/docs/trading/crypto/)
- [Alpaca Short Selling](https://alpaca.markets/docs/trading/short-selling/)
- `scripts/live_trader.py`: Order execution logic (lines ~1300-1400)
- `alpaca_trading/risk/capital_shift.py`: Equity→crypto shift logic
