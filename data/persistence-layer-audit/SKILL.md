---
name: persistence-layer-audit
description: "Audit SQLite persistence layer for unused tables and broken integrations. Trigger when: (1) checking database usage, (2) cleaning up schema, (3) finding missing methods."
author: Claude Code
date: 2024-12-29
---

# Persistence Layer Audit Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-29 |
| **Goal** | Audit and clean up SQLite persistence to match actual codebase usage |
| **Environment** | db_manager.py, trading_db.sql, live_trader.py |
| **Status** | Success |

## Context

SQLite databases can accumulate unused tables over time as the codebase evolves. This skill documents how to audit the persistence layer and align it with actual usage.

## Verified Workflow

### 1. Find Database Files

```bash
# Search for SQLite databases
find . -name "*.db" -o -name "*.sqlite" 2>/dev/null

# Common locations:
# - data/trading.db (main database)
# - data_cache/cache.sqlite (OHLCV cache)
# - data_cache/market_data.db (historical data)
```

### 2. Analyze Table Usage

```bash
# Check which tables have data
sqlite3 data/trading.db "SELECT name, (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=m.name) FROM sqlite_master m WHERE type='table';"

# Check row counts per table
sqlite3 data/trading.db "SELECT 'predictions', COUNT(*) FROM predictions UNION ALL SELECT 'prediction_outcomes', COUNT(*) FROM prediction_outcomes;"
```

### 3. Find Methods Called But Not Implemented

```bash
# Search for method calls in codebase
grep -r "tracker\\.get_recent_accuracy\\|db\\.some_method" --include="*.py"

# Check if method exists
grep -n "def get_recent_accuracy" alpaca_trading/**/*.py
```

### 4. Find Unused Table Methods

```bash
# Search for table name usage across codebase
grep -r "equity_symbols\\|symbol_features" --include="*.py" | grep -v "db_manager\\|trading_db"

# If no results outside schema/manager, table is unused
```

### 5. Clean Up Schema

Remove unused tables from SQL schema file:
```sql
-- REMOVED (dynamically computed or unused):
--   equity_symbols     - Alpaca API provides dynamically
--   symbol_features    - Computed in-memory during selection
--   universe_selections - Console logging sufficient
--   portfolio_performance - Redundant with other tracking
```

### 6. Remove Unused Methods

After confirming no callers exist:
```python
# Remove entire method sections that reference removed tables
# - upsert_symbol()
# - get_active_symbols()
# - mark_symbol_delisted()
# - upsert_symbol_features()
# - get_latest_features()
# - log_universe_selection()
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Assuming empty tables are unused | Some tables are used but just not populated yet | Check method calls, not just row counts |
| Removing tables without checking FK | Foreign key constraints break schema | Check FK references before removal |
| Removing methods before checking callers | Broke live_trader.py | Always grep for method usage first |
| Schema changes without db migration | Old databases don't update | CREATE TABLE IF NOT EXISTS handles this |

## Final Parameters

```yaml
# Tables to keep (v2.6)
predictions: true          # Core - all predictions
prediction_outcomes: true  # Core - actual results
prediction_metrics: true   # Aggregated daily metrics
rl_models: true           # Model registry
timeframe_selections: true # Multi-timeframe tracking
backtest_results: true    # Backtest history

# Tables removed (v2.6)
equity_symbols: false     # Alpaca API provides
symbol_features: false    # Computed in-memory
universe_selections: false # Console logging sufficient
portfolio_performance: false # Redundant
```

## Key Insights

- **Schema drift is normal**: As code evolves, some tables become obsolete
- **Grep before delete**: Always search for method/table usage before removal
- **CREATE IF NOT EXISTS**: Makes schema changes safe for existing databases
- **Foreign keys may reference removed tables**: Remove FK constraints too
- **Document what was removed**: Future maintainers need to know why

## Audit Checklist

1. [ ] List all database files and their sizes
2. [ ] Check row counts for each table
3. [ ] Search for method calls that might not exist
4. [ ] Identify unused tables (no callers outside schema/manager)
5. [ ] Remove unused tables from schema
6. [ ] Remove corresponding methods from db_manager
7. [ ] Update module docstrings
8. [ ] Document removed tables in schema comments

## References
- `alpaca_trading/data/db_manager.py`: Database manager class
- `alpaca_trading/data/trading_db.sql`: SQL schema definition
- `docs/persistence.md`: Persistence layer documentation
