---
name: data-source-priority
description: "Ensure Alpaca API is used for quality data, not yfinance fallback. Trigger when: (1) crypto volume filter fails unexpectedly, (2) zero-volume bars in data, (3) API key configuration issues."
author: Claude Code
date: 2024-12-28
---

# Data Source Priority - Alpaca vs yfinance (v2.5.0)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-28 |
| **Goal** | Fix crypto selection failing due to poor data quality |
| **Environment** | alpaca_trading/data/fetcher.py, training notebook |
| **Status** | Success - v2.5.0 now fails early |

## Context

User reported ALL 18 crypto symbols failing selection filters:
```
BTCUSD: failed price (max_price $10k but BTC is $87k)
ETHUSD: failed data_quality (51% zero-volume bars)
Others: failed volume, trading_status
```

**Root Cause**: Alpaca API keys weren't configured, so DataFetcher fell back to yfinance. yfinance crypto data has:
- ~50% zero-volume bars (data gaps)
- Missing volume data on many bars
- Causes ALL filters to fail

## v2.5.0 Solution: Fail Fast

**OLD BEHAVIOR (v2.4.x)**: Warned about yfinance but continued anyway, wasting time debugging filter failures.

**NEW BEHAVIOR (v2.5.0)**: Training notebook FAILS IMMEDIATELY if crypto is enabled without Alpaca API:

```python
# In training notebook cell-16
alpaca_enabled = data_fetcher._use_alpaca_data

if not alpaca_enabled and selection_config.crypto.enabled:
    raise ValueError(
        'CRYPTO TRAINING REQUIRES ALPACA API. '
        'yfinance crypto data has ~50% missing volume. '
        'Set API keys or disable crypto training.'
    )
```

## Clear Error Message

When crypto is enabled without Alpaca API:
```
======================================================================
ERROR: CRYPTO TRAINING REQUIRES ALPACA API
======================================================================

yfinance crypto data is unusable for training:
  - ~50% zero-volume bars
  - Causes all symbols to fail volume/data_quality filters
  - Training on bad data produces bad models

FIX OPTIONS:
  1. Set Alpaca API keys in Colab Secrets:
     - APCA_API_KEY_ID = your_key
     - APCA_API_SECRET_KEY = your_secret

  2. Set API_KEYS_FILE in previous cell:
     API_KEYS_FILE = "/content/Alpaca_trading/API_key_500Paper.txt"

  3. Disable crypto and train only equities:
     selection_config.crypto.enabled = False
     selection_config.equities.enabled = True
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Lower volume consistency to 30% | Masks real problem, still fails | Fix data source, not thresholds |
| Skip data quality filter for crypto | Still fails price/trading_status | Garbage in = garbage out |
| Simplify all crypto filters | Works but produces bad models | Use quality data, not workarounds |
| Just warn about yfinance | User ignores warning, wastes time | FAIL FAST is better |

## Data Quality Comparison

| Data Source | Volume Data | Zero-Volume Bars | Crypto Support |
|-------------|-------------|------------------|----------------|
| **Alpaca API** | Complete | <1% | Excellent |
| yfinance | 50% missing | ~50% | Unusable |

## API Key Configuration

### For Google Colab (RECOMMENDED)
1. Go to Colab Secrets (key icon in left sidebar)
2. Add `APCA_API_KEY_ID` = your API key
3. Add `APCA_API_SECRET_KEY` = your secret key
4. Enable access to notebook

### For Training Notebook
```python
# Cell 14: Option 1 - Environment variables (recommended)
# Keys are read from Colab Secrets automatically

# Cell 15: Option 2 - Keys file (after unzipping repo)
API_KEYS_FILE = '/content/Alpaca_trading/API_key_500Paper.txt'
```

### For Local Development
```bash
# Add to ~/.bashrc or ~/.zshrc
export APCA_API_KEY_ID="your_key"
export APCA_API_SECRET_KEY="your_secret"
```

## Diagnostic Check

```python
from alpaca_trading.data.fetcher import DataFetcher
fetcher = DataFetcher(keys_file=API_KEYS_FILE)

# This is checked BEFORE selection in v2.5.0
if not fetcher._use_alpaca_data:
    print('Alpaca API: NOT AVAILABLE')
    # Notebook will fail here if crypto enabled
else:
    print('Alpaca API: ENABLED')
```

## Key Insights

1. **Don't work around bad data** - Fix the data source
2. **Fail fast, fail loud** - Silent fallbacks waste debugging time
3. **yfinance is equities-only** - Acceptable for stocks, unusable for crypto
4. **Environment variables are best** - Work everywhere, no path issues
5. **Check logs for "yfinance fetched"** - This means you're using bad data

## Files Modified (v2.5.0)

```
notebooks/training.ipynb:
  - Cell 16: Added fail-fast check before symbol selection
  - Cell 0: Updated header to v2.5.0 with changelog

alpaca_trading/selection/filters/hard_filters.py:
  - apply_hard_filters(): Simplified crypto path (skip yfinance-specific checks)
```

## References
- `alpaca_trading/data/fetcher.py`: DataFetcher implementation
- `notebooks/training.ipynb`: Training notebook with fail-fast check
- Alpaca API docs: https://docs.alpaca.markets/docs/
- Skill: `reward-function-hold-bias` - Related v2.5.0 fix
