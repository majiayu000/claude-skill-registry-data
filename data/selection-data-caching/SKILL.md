---
name: selection-data-caching
description: "SUPERSEDED by persistent-cache-gap-filling (v2.8.0). Cache data during symbol selection for instant repeat runs."
author: Claude Code
date: 2024-12-28
---

# Selection Data Caching (v2.5.1)

> **SUPERSEDED**: This skill documents the v2.5.1 time-based cache expiry approach.
> See **persistent-cache-gap-filling** for the v2.8.0 improvement that removes
> time-based expiry and uses gap-filling instead.

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-28 |
| **Goal** | Make universe selection use cached data like training does |
| **Environment** | notebooks/training.ipynb |
| **Status** | Superseded by v2.8.0 |

## Context

User noticed that training uses a data cache (Google Drive) but universe selection fetches fresh data every time. This meant:
- Selection took 3-5 minutes on every run (API rate limits)
- Changing selection parameters required waiting again
- Data fetched during selection was thrown away (not reused for training)

## v2.5.1 Solution: Unified Cache System

Created `CachingDataFetcher` wrapper that intercepts `get_bars()` calls and uses Google Drive cache:

```python
class CachingDataFetcher:
    """Wrapper around DataFetcher that uses Google Drive cache."""

    def __init__(self, base_fetcher: DataFetcher,
                 cache_expiry_days: int = 3,
                 verbose: bool = True):
        self._fetcher = base_fetcher
        self._cache_expiry_days = cache_expiry_days
        self._verbose = verbose
        self._cache_hits = 0
        self._cache_misses = 0

        # Expose underlying fetcher's attributes
        self._use_alpaca_data = base_fetcher._use_alpaca_data

    def get_bars(self, symbol: str, timeframe: str = '1Hour',
                 lookback_days: int = 730, **kwargs) -> pd.DataFrame:
        # Try cache first
        df = load_from_cache(symbol, timeframe, self._cache_expiry_days)

        if df is not None and len(df) >= MIN_BARS_REQUIRED:
            self._cache_hits += 1
            return df

        # Cache miss - fetch from API
        self._cache_misses += 1
        df = self._fetcher.get_bars(symbol, timeframe=timeframe,
                                    lookback_days=lookback_days, **kwargs)

        # Cache the result if valid
        if df is not None and len(df) >= MIN_BARS_REQUIRED:
            save_to_cache(symbol, df, timeframe, lookback_days)

        return df
```

## Cache Configuration

| Setting | Selection | Training | Reason |
|---------|-----------|----------|--------|
| **Expiry** | 3 days | 7 days | Selection needs fresher data for ranking |
| **Min bars** | 500 | 2000 | Training needs more data |
| **Location** | `/content/drive/MyDrive/Colab_Projects/training_data` | Same | Shared cache |

## Workflow Before vs After

### Before (v2.5.0)
```
Selection: Fetch from API (3-5 min)
     ↓
Training prefetch: Fetch from API again (3-5 min)
     ↓
Training: Load from cache (instant)
```

### After (v2.5.1)
```
Selection: Fetch from API + cache (3-5 min on first run)
     ↓         ↓ (instant on repeat runs)
Training: Load from same cache (instant)
```

## Implementation Details

### 1. Cache Cell (Added after imports)
```python
# Define cache functions and CachingDataFetcher
DRIVE_DATA_DIR = '/content/drive/MyDrive/Colab_Projects/training_data'
SELECTION_CACHE_EXPIRY_DAYS = 3
TRAINING_CACHE_EXPIRY_DAYS = 7

class CachingDataFetcher:
    ...
```

### 2. Selection Cell (Modified)
```python
# Create cached fetcher for selection
base_fetcher = DataFetcher(keys_file=API_KEYS_FILE)
data_fetcher = CachingDataFetcher(
    base_fetcher=base_fetcher,
    cache_expiry_days=SELECTION_CACHE_EXPIRY_DAYS,
    verbose=True
)

# Use cached fetcher for selection
selected_symbols, result = select_compatible_universe(
    candidates=candidates,
    data_fetcher=data_fetcher,  # Now uses cache!
    ...
)

# Show cache statistics
cache_stats = data_fetcher.get_cache_stats()
print(f'Cache hits: {cache_stats["cache_hits"]} ({cache_stats["hit_rate"]:.0%})')
```

### 3. Training Cell (Modified)
```python
# Reuse base_fetcher with longer expiry
fetcher = CachingDataFetcher(
    base_fetcher=base_fetcher,
    cache_expiry_days=TRAINING_CACHE_EXPIRY_DAYS,  # 7 days
    verbose=True
)
# Data already cached from selection - instant load!
```

## Key Insights

1. **Wrapper pattern is clean** - CachingDataFetcher wraps DataFetcher without modifying it
2. **Different expiry for different needs** - Selection wants fresh data, training wants stability
3. **Cache statistics are helpful** - Shows user that cache is working
4. **Same cache for both** - Selection caches data that training reuses
5. **Verbose mode for debugging** - Shows [CACHE] vs [API] for each symbol

## Files Modified

```
notebooks/training.ipynb:
  - New cell after imports: Cache system and CachingDataFetcher
  - cell-16: Selection uses CachingDataFetcher
  - cell-27: Training reuses same cache with longer expiry
  - cell-0: Updated header to v2.5.1
```

## Performance Improvement

| Run | Selection Time | Training Prefetch | Total |
|-----|----------------|-------------------|-------|
| **First** | 3-5 min | ~0 (already cached) | 3-5 min |
| **Repeat** | Seconds | Seconds | Seconds |

## References
- `notebooks/training.ipynb`: Implementation
- `alpaca_trading/data/fetcher.py`: Base DataFetcher
- Skill: `data-source-priority` - Related data fetching patterns
- Skill: `persistent-cache-gap-filling` - v2.8.0 replacement

---

## v2.8.0 Update: Why Time-Based Expiry Was Wrong

The v2.5.1 approach used time-based cache expiry (3-7 days), but this caused problems:

| Issue | Impact |
|-------|--------|
| Cache expired overnight | Re-downloaded complete 4-year history |
| Historical data is immutable | Past candles never change, so re-fetching wastes API calls |
| Different expiry per use case | Confusing configuration |

**v2.8.0 Solution**: Persistent cache with gap-filling
- Cache never expires (historical data is immutable)
- Only fetches new bars since last cache update
- Single cache location for both selection and training

See skill: **persistent-cache-gap-filling** for full details.
