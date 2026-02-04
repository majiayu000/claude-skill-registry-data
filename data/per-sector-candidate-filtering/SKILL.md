---
name: per-sector-candidate-filtering
description: "Per-sector candidate limits using yfinance sector data. Trigger when: (1) universe selection has too many candidates, (2) need sector diversity in candidate pool, (3) downloading historical data takes too long."
author: Claude Code
date: 2026-01-03
---

# Per-Sector Candidate Filtering - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-03 |
| **Goal** | Reduce ~4k candidates to ~1.5k while maintaining sector diversity |
| **Environment** | Python 3.10/3.11, SQLite 3.25+, yfinance |
| **Status** | Success |

## Context

Universe selection was filtering 12k symbols down to ~4k candidates based on volume/price thresholds. However, downloading 4 years of hourly historical data for 4k symbols takes too long (~10s/symbol = 11+ hours).

**Requirements:**
1. Reduce candidates to ~1.5-2k (sustainable download time)
2. Maintain sector diversity (don't over-represent any single sector)
3. Cache sector data (don't re-fetch on every run)

## Verified Workflow

### 1. Database Schema Update

The sector column is automatically added via migration:

```python
# Migration in _init_db()
cursor.execute("PRAGMA table_info(symbols)")
columns = {row[1] for row in cursor.fetchall()}
if 'sector' not in columns:
    cursor.execute("ALTER TABLE symbols ADD COLUMN sector TEXT DEFAULT 'other'")
```

### 2. Fetch Sector Data (One-Time)

```python
from alpaca_trading.selection.symbol_database import SymbolDatabase

db = SymbolDatabase(db_path='data/symbol_database.db')
db.update_sectors()  # ~1-2 min for all symbols
db.print_summary()   # Shows sector breakdown
```

### 3. Get Sector-Limited Candidates

```python
candidates = db.get_candidates(
    min_volume_usd=1_000_000,
    sector_top_pct=0.30,    # Top 30% per sector by volume
    min_per_sector=50,      # Floor for small sectors
    max_per_sector=300,     # Cap for large sectors
)
print(f"Candidates: {len(candidates)}")  # ~1,300 instead of ~3,600
```

### 4. Configuration

```python
from alpaca_trading.selection.config import SelectionConfig

config = SelectionConfig()
# Access sector filter settings
print(config.sector_filter.enabled)       # True
print(config.sector_filter.sector_top_pct) # 0.30
print(config.sector_filter.min_per_sector) # 50
print(config.sector_filter.max_per_sector) # 300
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Alpaca API for sectors | Alpaca doesn't provide sector data | Use yfinance instead |
| Global top N% (no sectors) | Over-represents tech/finance | Per-sector limits needed |
| Simple SQL ORDER BY in UNION | "ORDER BY term does not match column" | Use subquery with explicit columns |
| Fixed count per sector | Small sectors wiped out | Use dynamic % with min/max bounds |

## Final Parameters

```python
# Sector filtering defaults
SECTOR_TOP_PCT = 0.30        # Top 30% of each sector
MIN_PER_SECTOR = 50          # Minimum candidates per sector
MAX_PER_SECTOR = 300         # Maximum candidates per sector

# yfinance sector mapping
YFINANCE_SECTOR_MAP = {
    'Technology': 'technology',
    'Healthcare': 'healthcare',
    'Financial Services': 'financial',
    'Consumer Cyclical': 'consumer',
    'Consumer Defensive': 'consumer',
    'Industrials': 'industrial',
    'Energy': 'energy',
    'Utilities': 'utilities',
    'Real Estate': 'real_estate',
    'Basic Materials': 'materials',
    'Communication Services': 'communication',
}

# Standard sectors (11 total)
STANDARD_SECTORS = [
    'technology', 'healthcare', 'financial', 'consumer', 'industrial',
    'energy', 'utilities', 'real_estate', 'materials', 'communication', 'other'
]
```

## SQL Window Function Query

```sql
WITH filtered AS (
    SELECT symbol, sector, daily_volume_usd, asset_type
    FROM symbols
    WHERE is_tradable = 1 AND asset_type IN ('equity', 'crypto')
      AND daily_volume_usd >= 1000000
),
ranked AS (
    SELECT
        symbol, sector, daily_volume_usd, asset_type,
        ROW_NUMBER() OVER (PARTITION BY sector ORDER BY daily_volume_usd DESC) as rank_in_sector,
        COUNT(*) OVER (PARTITION BY sector) as sector_count
    FROM filtered
    WHERE asset_type = 'equity'
),
selected_equities AS (
    SELECT symbol, daily_volume_usd FROM ranked
    WHERE rank_in_sector <= MAX(50, MIN(300, CAST(sector_count * 0.30 AS INTEGER)))
),
selected_crypto AS (
    SELECT symbol, daily_volume_usd FROM filtered
    WHERE asset_type != 'equity'
)
SELECT symbol FROM (
    SELECT symbol, daily_volume_usd FROM selected_equities
    UNION ALL
    SELECT symbol, daily_volume_usd FROM selected_crypto
) combined
ORDER BY daily_volume_usd DESC
```

## Expected Results

| Sector | Typical Count | After 30% Limit |
|--------|---------------|-----------------|
| Technology | 800 | 240 |
| Healthcare | 600 | 180 |
| Financial | 700 | 210 |
| Consumer | 500 | 150 |
| Industrial | 400 | 120 |
| Energy | 200 | 60 |
| Utilities | 150 | 50 (min) |
| Real Estate | 200 | 60 |
| Materials | 150 | 50 (min) |
| Communication | 150 | 50 (min) |
| Other | 500 | 150 |
| **Total** | **~4,350** | **~1,320** |

**Result**: ~70% reduction while maintaining proportional sector representation.

## Key Insights

- **yfinance is the only free sector source** - Alpaca doesn't provide sector data
- **Consumer sectors consolidated** - Consumer Cyclical + Consumer Defensive -> consumer
- **Dynamic limits are essential** - Fixed counts would eliminate small sectors entirely
- **SQLite 3.25+ required** - Window functions (ROW_NUMBER, PARTITION BY) need modern SQLite
- **Sector data persists** - Only fetch once, stored in database permanently
- **Crypto bypasses sector filter** - Only equities have sectors

## Files Modified

| File | Changes |
|------|---------|
| `alpaca_trading/selection/symbol_database.py` | Added sector column, `update_sectors()`, sector-aware `get_candidates()` |
| `alpaca_trading/selection/config.py` | Added `SectorFilterConfig` dataclass |

## References

- Skill: `symbol-database-selection` - Multi-stage selection pipeline
- Skill: `persistent-cache-gap-filling` - Data caching strategy
- yfinance documentation: https://pypi.org/project/yfinance/
- GICS sector classification: https://www.msci.com/gics
