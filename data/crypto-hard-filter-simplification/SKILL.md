---
name: crypto-hard-filter-simplification
description: "Simplify crypto hard filters to essential checks only. Trigger when: (1) crypto symbols fail multiple filters, (2) data_quality/spread/trading_status fail for crypto, (3) yfinance data gaps causing false failures."
author: Claude Code
date: 2024-12-28
---

# Crypto Hard Filter Simplification (v2.5.0)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-28 |
| **Goal** | Stop crypto symbols from failing irrelevant filters |
| **Environment** | alpaca_trading/selection/filters/hard_filters.py |
| **Status** | Success |

## Context

User reported ALL 18 crypto symbols failing selection with different filter failures:
```
BTCUSD: failed price (max_price $10k but BTC is $87k)
ETHUSD: failed data_quality (51% zero-volume but 5% max allowed)
SOLUSD: failed trading_status (50% activity but 80% required)
DOGEUSD: failed volume (consistency 28% but 70% required)
```

Each filter had different asset-type assumptions that didn't apply to crypto.

## Root Cause Analysis

| Filter | Problem for Crypto | Reality |
|--------|-------------------|---------|
| `price` | max_price=$10,000 | BTC is $87k+, no upper limit |
| `data_quality` | max 5% zero-volume | yfinance has 50% gaps |
| `trading_status` | 80% activity required | yfinance gaps cause 50% |
| `spread` | 0.5% max spread | Crypto volatility is higher |
| `volume` | 70% consistency | yfinance has ~30% consistency |

**Key Insight**: These filters were designed to catch BAD ASSETS, but they were flagging BAD DATA from yfinance. When using Alpaca API with quality data, these filters would pass.

## v2.5.0 Solution: Separate Crypto Path

Instead of patching each filter, we created a **separate code path** for crypto that only checks essentials:

```python
def apply_hard_filters(symbol, df, ..., is_crypto=False):
    result = HardFilterResult(symbol=symbol, passed=True)

    # v2.5.0: For crypto, only check essential filters
    # Skip spread/data_quality/trading_status - they just flag yfinance gaps
    if is_crypto:
        # Essential: Has enough data?
        if df is None or len(df) < min_bars:
            result.add_result("min_bars", False, {...})
            return result
        result.add_result("min_bars", True, {"n_bars": len(df)})

        # Essential: Price above minimum? (filter dead coins)
        current_price = df['close'].iloc[-1] if 'close' in df.columns else 0
        passed = current_price >= min_price
        result.add_result("price", passed, {...})

        # Essential: Has reasonable volume? (relaxed for yfinance gaps)
        passed, details = check_volume_filter(df, min_daily_volume_usd, is_crypto=True)
        result.add_result("volume", passed, details)

        return result  # Skip spread, data_quality, trading_status

    # Equities: Apply full filter chain
    # ... existing code ...
```

## Filter Changes for Crypto

| Filter | Equities | Crypto | Reason |
|--------|----------|--------|--------|
| `min_bars` | Check | Check | Essential for training |
| `price` | min/max | min only | No upper limit (BTC $87k+) |
| `volume` | 70% consistency | 30% consistency | yfinance gaps |
| `spread` | Check | **SKIP** | Flags yfinance volatility |
| `data_quality` | Check | **SKIP** | Flags yfinance gaps |
| `trading_status` | Check | **SKIP** | Flags yfinance gaps |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Patch max_price check for crypto | Still fails data_quality | Whack-a-mole approach |
| Lower data_quality thresholds | Still fails trading_status | Same problem |
| Add is_crypto to each filter | Complex, hard to maintain | Separate code path is cleaner |
| Remove all filters for crypto | No quality control | Keep essential checks |

## volume_filter Adjustments for Crypto

```python
def check_volume_filter(df, min_daily_volume_usd, min_volume_consistency=0.7, is_crypto=False):
    # v2.5.0: Cap consistency requirement for crypto (yfinance has many zero-volume bars)
    if is_crypto:
        min_volume_consistency = min(min_volume_consistency, 0.30)  # Cap at 30%

    # ... rest of calculation ...
```

## Key Insights

1. **Separate code paths are cleaner** - Don't patch each filter individually
2. **Filters should catch bad assets, not bad data** - Use quality data source instead
3. **Keep essential checks** - min_bars, min_price, volume still matter
4. **Skip irrelevant checks** - spread/data_quality/trading_status flag data issues, not asset issues
5. **With Alpaca API, these filters would pass** - The real fix is quality data

## Files Modified

```
alpaca_trading/selection/filters/hard_filters.py:
  - Line 362-378: New crypto-specific path in apply_hard_filters()
  - Line 66-68: Volume consistency cap for crypto
```

## Best Practice

**Prefer Alpaca API over filter simplification.**

The simplified filters are a fallback for when yfinance must be used. With Alpaca API:
- Volume data is complete
- All filters pass naturally
- No special crypto handling needed

See skill `data-source-priority` for ensuring Alpaca API is used.

## References
- `alpaca_trading/selection/filters/hard_filters.py`: Filter implementations
- Skill: `data-source-priority` - Ensure quality data source
- Skill: `symbol-selection-asset-filters` - Asset-type filter patterns
