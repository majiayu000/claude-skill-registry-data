---
name: persistent-cache-gap-filling
description: "Persistent data cache with gap-filling for historical market data. Trigger when: (1) cache re-downloads complete data unnecessarily, (2) time-based cache expiry wastes API calls, (3) historical data needs incremental updates only."
author: Claude Code
date: 2026-01-01
---

# Persistent Cache with Gap-Filling (v2.8.0)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-01 |
| **Goal** | Eliminate redundant downloads of historical data by removing time-based cache expiry |
| **Environment** | alpaca_trading/data/ modules |
| **Status** | Success |

## Context

User noticed that re-running the training notebook caused complete re-downloads of historical data even though:
- Data was downloaded earlier the same day
- Historical data is immutable (past candles never change)
- Only new bars since the last download were needed

The root cause was time-based cache expiry:
- SQLite cache (`cache.py`): 12-hour TTL via `PERSISTED_TTL_HOURS`
- Pickle cache (`caching_fetcher.py`): 3-7 day expiry via `cache_expiry_days`

## v2.8.0 Solution: Persistent Cache + Gap-Filling

### Core Principle
Historical market data is immutable. Once downloaded and validated, it should persist indefinitely. Only fetch new bars to fill the gap between cache end and current time.

### Changes Made

#### 1. cache.py - SQLite Cache
```python
# Before: TTL always checked
def get(self, ..., ttl_hours: int = 24):
    if created_at < ttl_cutoff or expires_at < now_ts:
        self._remove_entry(cache_key)
        return None

# After: TTL is optional (None = no expiry)
def get(self, ..., ttl_hours: Optional[int] = None):
    # Only check TTL if explicitly specified
    if ttl_hours is not None:
        # ... TTL check
    # Otherwise return cached data regardless of age
```

#### 2. fetcher.py - DataFetcher
```python
# Removed
PERSISTED_TTL_HOURS = 12
self._cache_ttl_hours = PERSISTED_TTL_HOURS

# Updated _load_persisted - no TTL check
def _load_persisted(self, symbol: str, timeframe: str) -> pd.DataFrame:
    # No TTL - historical data is immutable
    cached = self._cache.get(symbol, timeframe, start="", end="")
    return cached
```

#### 3. caching_fetcher.py - CachingDataFetcher
```python
class CachingDataFetcher:
    def get_bars(self, symbol, timeframe, lookback_days, **kwargs):
        cached_df = load_from_cache(symbol, timeframe, cache_dir=self._cache_dir)

        if cached_df is not None:
            cache_end = cached_df.index.max()

            # Check if cache covers requested range
            if cache_start <= start_dt and cache_end >= end_dt - tolerance:
                return cached_df  # Complete - no API call

            # Gap-fill: only fetch new bars
            fetch_start = cache_end + timedelta(hours=1)
            new_df = self._fetcher.get_bars(symbol, start=fetch_start, ...)

            # Merge and save
            combined = pd.concat([cached_df, new_df])
            save_to_cache(symbol, combined, ...)
            return combined
```

## Behavior Comparison

### Before (Time-Based Expiry)
```
Run 1 (10:00 AM): Fetch 4 years of data [API] -> Cache (12h TTL)
Run 2 (10:30 AM): Cache valid -> [CACHE] instant
Run 3 (11:00 PM): Cache expired -> [API] Fetch 4 years AGAIN
```

### After (Persistent + Gap-Fill)
```
Run 1 (10:00 AM): Fetch 4 years of data [API] -> Cache (persistent)
Run 2 (10:30 AM): Cache complete -> [CACHE] instant
Run 3 (11:00 PM): Cache + gap-fill -> [GAP-FILL] Fetch 13 new bars only
```

## Output Messages

| Message | Meaning |
|---------|---------|
| `[CACHE] AAPL: 35,040 bars (complete)` | Cache covers full range, no API call |
| `[GAP-FILL] AAPL: Fetching 2026-01-01 to 2026-01-01...` | Fetching only new bars |
| `[UPDATED] AAPL: 35,038 + 2 = 35,040 bars` | Merged new bars with cache |
| `[API] AAPL: Fetching 1460 days...` | No cache, full download |

## Cache Statistics

New `gap_fills` counter added:
```python
stats = fetcher.get_cache_stats()
# {
#   'cache_hits': 8,      # Returned cached data unchanged
#   'cache_misses': 2,    # No cache, full download
#   'gap_fills': 5,       # Merged new bars with cache
#   'hit_rate': 0.87      # (hits + gap_fills) / total
# }
```

## Failed Attempts

| Approach | Result | Why It Failed |
|----------|--------|---------------|
| Increase TTL to 30 days | Worked but fragile | Still expires eventually, arbitrary cutoff |
| Check file modification time | Partial | Doesn't verify data completeness |

## Key Insights

1. **Historical data is immutable** - Past candles never change, so there's no reason to re-fetch them
2. **Only the edge needs updating** - New bars appear at the end of the series
3. **Time-based expiry is wrong model** - For mutable data (news, weather) TTL makes sense; for historical OHLCV it's waste
4. **Completeness > freshness** - Check if cache covers the requested date range, not how old the file is

## Files Modified

```
alpaca_trading/data/cache.py:
  - get(): ttl_hours now Optional[int] = None (no expiry by default)

alpaca_trading/data/fetcher.py:
  - Removed PERSISTED_TTL_HOURS constant
  - _load_persisted(): No TTL check
  - _save_persisted(): Uses 10-year TTL (effectively infinite)

alpaca_trading/data/caching_fetcher.py:
  - DEFAULT_*_CACHE_EXPIRY_DAYS = None (no expiry)
  - is_cache_valid(): Just checks file exists
  - get_bars(): Gap-filling logic added
  - get_cache_stats(): Added gap_fills counter
```

## Backward Compatibility

- Existing `.pkl` cache files work unchanged
- `cache_expiry_days` parameter still accepted but ignored
- Old caches are automatically upgraded (no migration needed)

## References

- Skill: `selection-data-caching` - Original caching implementation (v2.5.1)
- Skill: `data-source-priority` - Data fetching hierarchy
- `alpaca_trading/data/caching_fetcher.py`: Gap-filling implementation
