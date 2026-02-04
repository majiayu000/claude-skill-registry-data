---
name: multi-timeframe-training
description: "Train RL models across multiple timeframes with resampling. Trigger when: (1) multi-timeframe training, (2) resampling data, (3) creating 1Hour/4Hour models."
author: Claude Code
date: 2024-12-29
---

# Multi-Timeframe Training Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-29 |
| **Goal** | Train separate models for each timeframe using resampled data from base timeframe |
| **Environment** | training notebook, multi_timeframe.py, GPUVectorizedTradingEnv |
| **Status** | Success |

## Context

Single-timeframe training limits strategy adaptability. Different timeframes capture different market dynamics:
- 1Hour: Short-term momentum, intraday patterns
- 4Hour: Medium-term trends, reduced noise
- 1Day: Long-term trends, swing trading

**Solution**: Train separate models for each timeframe, resampling from cached 1Hour data.

## Verified Workflow

### 1. Configure Training Timeframes (notebook)

```python
# Data configuration
TIMEFRAME = '1Hour'               # Base timeframe for data fetching
TRAINING_TIMEFRAMES = ['1Hour']   # Single timeframe (default)
# TRAINING_TIMEFRAMES = ['1Hour', '4Hour']  # Multi-TF training
```

### 2. Build Training Combinations

```python
# Build training combinations (symbol x timeframe)
training_combinations = [(s, tf) for tf in TRAINING_TIMEFRAMES for s in SYMBOLS_TO_TRAIN_FINAL]
total_combinations = len(training_combinations)

print(f'TRAINING {len(SYMBOLS_TO_TRAIN_FINAL)} SYMBOLS × {len(TRAINING_TIMEFRAMES)} TIMEFRAMES = {total_combinations} models')
```

### 3. Resample Data with Proper Alignment

```python
from alpaca_trading.signals.multi_timeframe import resample_to_timeframe

# Load base data (1Hour)
df_base = PREFETCHED_DATA[symbol]

# Resample if training on different timeframe
if training_tf != TIMEFRAME:
    df = resample_to_timeframe(df_base, training_tf)
    print(f'  Resampled {len(df_base)} bars -> {len(df)} bars for {training_tf}')
else:
    df = df_base
```

### 4. Resampling Function (multi_timeframe.py)

```python
def resample_to_timeframe(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Resample OHLCV data to a different timeframe."""
    if df.empty:
        return df

    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    # Map timeframe to pandas frequency (pandas 2.2+ uses lowercase 'h')
    freq_map = {
        "1Min": "1min",
        "5Min": "5min",
        "15Min": "15min",
        "30Min": "30min",
        "1Hour": "1h",
        "2Hour": "2h",
        "4Hour": "4h",
        "1Day": "1D",
        "1Week": "1W",
    }

    freq = freq_map.get(timeframe, "1min")

    # Resample OHLCV with origin='start' to preserve alignment
    # CRITICAL: origin='start' ensures bars align with market open (9:30)
    # not clock-hour boundaries (10:00, 11:00)
    resampled = pd.DataFrame()
    resampled["open"] = df["open"].resample(freq, origin='start').first()
    resampled["high"] = df["high"].resample(freq, origin='start').max()
    resampled["low"] = df["low"].resample(freq, origin='start').min()
    resampled["close"] = df["close"].resample(freq, origin='start').last()

    if "volume" in df.columns:
        resampled["volume"] = df["volume"].resample(freq, origin='start').sum()

    return resampled.dropna()
```

### 5. Model Naming Convention

```python
# Models named with timeframe suffix
model_filename = f'{symbol}_{training_tf}.pt'
# Examples: GOOGL_1Hour.pt, GOOGL_4Hour.pt

# Save paths
local_model_path = f'models/rl_symbols/{model_filename}'
drive_model_path = f'{DRIVE_MODEL_DIR}/{model_filename}'
```

### 6. Live Trader Model Loading

```python
# Load models organized by symbol and timeframe
for model_file in model_dir.glob('*.pt'):
    filename = model_file.stem
    parts = filename.split('_')
    symbol = parts[0]
    timeframe = parts[1] if len(parts) > 1 else '1Hour'

    model = load_native_model(str(model_file))

    if symbol not in models_by_symbol:
        models_by_symbol[symbol] = {}
    models_by_symbol[symbol][timeframe] = model
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Resampling without origin='start' | Bars aligned to clock hours, not market open | Use origin='start' for equity market alignment |
| Using 'H' instead of 'h' | Deprecated in pandas 2.2+ | Use lowercase 'h' for hours |
| Training all timeframes in parallel | OOM errors | Train sequentially, clean up between |
| Mixing 1Hour and 4Hour data sources | Data inconsistency | Always resample from same base data |
| Not cleaning GPU memory between TFs | Memory accumulation, crash | Call cleanup_gpu_memory() between each |

## Final Parameters

```yaml
# Timeframe configuration
base_timeframe: '1Hour'       # Data fetched at this resolution
training_timeframes:          # Train models at these resolutions
  - '1Hour'                   # Default (single TF)
  # - '4Hour'                 # Add for multi-TF
  # - '1Day'                  # Add for swing trading

# Resampling rules
origin: 'start'               # Align to first bar (market open)
open: 'first'                 # First open in period
high: 'max'                   # Max high in period
low: 'min'                    # Min low in period
close: 'last'                 # Last close in period
volume: 'sum'                 # Total volume in period

# pandas frequency map
1Hour: '1h'
2Hour: '2h'
4Hour: '4h'
1Day: '1D'
1Week: '1W'
```

## Key Insights

- **origin='start' is CRITICAL**: Without it, 4Hour bars start at 00:00, not market open
- **Lowercase frequency strings**: pandas 2.2+ deprecated uppercase 'H'
- **Sequential training**: GPU memory doesn't allow parallel multi-TF training
- **Same base data**: All timeframes should resample from same cached data
- **Consistent naming**: `SYMBOL_TIMEFRAME.pt` enables auto-discovery

## Data Requirements

| Timeframe | Min Bars (training) | From 1Hour (4 years) |
|-----------|---------------------|----------------------|
| 1Hour     | 2000                | ~10,000 bars         |
| 4Hour     | 500                 | ~2,500 bars          |
| 1Day      | 125                 | ~1,000 bars          |

## Multi-TF Strategy (future)

Once models exist for multiple timeframes:
1. Use `MultiTimeframePricePredictor` for signal aggregation
2. Higher timeframes get more weight (filter noise)
3. Require alignment (e.g., 1Hour + 4Hour both bullish) for entries

## References
- `notebooks/training.ipynb`: TRAINING_TIMEFRAMES configuration
- `alpaca_trading/signals/multi_timeframe.py`: resample_to_timeframe()
- `scripts/live_trader.py`: Multi-TF model loading pattern
