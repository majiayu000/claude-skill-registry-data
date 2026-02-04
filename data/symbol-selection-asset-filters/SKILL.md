---
name: symbol-selection-asset-filters
description: "Fix symbol selection failing due to asset-type filter mismatch. Trigger when: (1) '0/N passed hard filter' error, (2) crypto selection fails unexpectedly, (3) assets filtered by wrong price/volume thresholds."
author: Claude Code
date: 2024-12-26
---

# Symbol Selection Asset-Type Filters

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-26 |
| **Goal** | Fix symbol selection using wrong filters for asset types |
| **Environment** | alpaca_trading/selection/universe.py, config.py |
| **Status** | Success |

## Context

User reported error:
```
No symbols passed filters.
Stats: 0/30 passed hard filter
Qualified: 0
```

When running crypto-only selection with:
```python
selection_config.equities.enabled = False
selection_config.crypto.enabled = True
```

**Root Cause**: Hard filters in `universe.py` used `self.config.min_price` (equity default $5.0) for ALL assets, including crypto. Most cryptocurrencies trade below $5.

## The Bug

```python
# universe.py - BEFORE (broken)
hard_result = apply_hard_filters(
    symbol=symbol,
    df=data,
    min_daily_volume_usd=self.config.min_avg_volume,  # Global setting
    min_price=self.config.min_price,  # $5.0 - wrong for crypto!
    max_price=self.config.max_price,
    min_bars=self.config.min_data_points,
)
```

`SelectionConfig` has both:
- Global settings: `min_price = 5.0`, `min_avg_volume = 500_000`
- Asset-specific: `crypto.min_price = 0.01`, `crypto.min_daily_volume_usd = 50_000_000`

But the hard filter used GLOBAL settings, ignoring asset-specific config!

## Verified Fix

### 1. Detect Asset Type and Use Correct Config

```python
# universe.py - AFTER (fixed)
# Determine asset type and use appropriate settings
is_crypto = symbol.endswith('USD') or '/' in symbol
if is_crypto:
    asset_config = self.config.crypto
else:
    asset_config = self.config.equities

# Apply hard filters with asset-type-specific settings
hard_result = apply_hard_filters(
    symbol=symbol,
    df=data,
    min_daily_volume_usd=asset_config.min_daily_volume_usd,
    min_price=asset_config.min_price,
    max_price=self.config.max_price,
    min_bars=self.config.min_data_points,
)
```

### 2. Relax Crypto Defaults

```python
# config.py - AssetTypeConfig for crypto
crypto: AssetTypeConfig = field(default_factory=lambda: AssetTypeConfig(
    enabled=True,
    max_allocation=0.20,
    max_positions=3,
    min_volatility=0.15,   # 15% annual volatility minimum
    max_volatility=2.00,   # 200% max (crypto is volatile)
    min_daily_volume_usd=1_000_000,   # $1M (was $50M - too strict!)
    min_price=0.0001,      # Allow very low prices (was $5!)
))
```

### 3. Add Diagnostic Output

```python
# When selection fails, show WHY
print(f'Diagnostic info - Sample of failed symbols:')
for sym, analysis in list(result.analyses.items())[:10]:
    reasons = analysis.exclusion_reasons
    print(f'  {sym}: {reasons[0]}')
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Crypto min_price = $5.0 | Most cryptos trade below $5 | Use asset-type-specific settings |
| Crypto min_volume = $50M | Many valid cryptos under $50M daily volume | $1M is reasonable minimum |
| Global config.min_price | Applied equity settings to crypto | Detect asset type first |
| No diagnostic output | Users couldn't see WHY selection failed | Always show failure reasons |

## Asset-Type Detection

```python
# Simple heuristic for crypto detection
is_crypto = symbol.endswith('USD') or '/' in symbol

# Examples:
# BTCUSD  -> crypto (ends with USD)
# BTC/USD -> crypto (contains /)
# AAPL    -> equity (neither)
```

## Recommended Settings by Asset Type

### Equities
```python
selection_config.equities.min_price = 5.0             # $5 minimum
selection_config.equities.min_daily_volume_usd = 10_000_000  # $10M
selection_config.equities.min_volatility = 0.05       # 5% annual
selection_config.equities.max_volatility = 0.60       # 60% annual
```

### Crypto
```python
selection_config.crypto.min_price = 0.0001            # Allow any price
selection_config.crypto.min_daily_volume_usd = 1_000_000  # $1M
selection_config.crypto.min_volatility = 0.15         # 15% annual
selection_config.crypto.max_volatility = 2.00         # 200% annual
```

## Key Insights

### Why Crypto Needs Different Settings

| Parameter | Equity | Crypto | Why Different |
|-----------|--------|--------|---------------|
| min_price | $5.00 | $0.0001 | Many cryptos < $1 |
| min_volume | $10M | $1M | Smaller crypto market |
| max_volatility | 60% | 200% | Crypto is volatile |

### Alpaca Crypto Availability

- Alpaca has ~30 crypto pairs
- All end with `USD` (e.g., `BTCUSD`, `ETHUSD`)
- Some trade at fractions of a cent (e.g., `SHIBUSD`)

### Common Selection Errors

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| `0/N passed hard filter` | Wrong asset-type settings | Check min_price for crypto |
| `Insufficient data` | min_data_points too high | Lower to 300 for hourly data |
| `volume` filter fails | min_daily_volume_usd too high | $1M for crypto, $10M equity |

## Files Modified

```
alpaca_trading/selection/universe.py:
  - Lines 260-275: Detect asset type, use correct AssetTypeConfig

alpaca_trading/selection/config.py:
  - Lines 85-93: Relaxed crypto defaults

notebooks/VSCode_Colab_Training_NATIVE.ipynb:
  - cell-16: Added diagnostic output on failure
```

## References
- `alpaca_trading/selection/config.py`: AssetTypeConfig dataclass
- `alpaca_trading/selection/filters/hard_filters.py`: Filter implementations
- `alpaca_trading/selection/universe.py`: Selection orchestration
- `.skills/plugins/trading/symbol-selection-statistical/`: Statistical selection guide
