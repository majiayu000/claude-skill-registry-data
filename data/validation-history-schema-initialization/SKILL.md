---
name: validation-history-schema-initialization
description: Initialize PostgreSQL schema for validation history tables
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T23:36:28.500Z"
  updated_at: "2026-01-29T23:36:28.500Z"
  version: "1"
  tags: "validation,history,database,schema,postgresql"
  compatibility: "2.1.0+"
  difficulty: "intermediate"
---
<!-- BEGIN:compound:skill-managed -->
# Validation History Schema Initialization
This skill provides guidance on initializing PostgreSQL database schema for validation history storage.

## When To Use
- Creating new ValidationHistoryStore instance
- Setting up validation history for first time
- Database migration or fresh installation

## Procedure
1. Create PostgreSQLConnector with valid config
2. Initialize ValidationHistoryStore with connector
3. Call `initialize_schema()` method
4. Verify tables created with `connector.table_exists()`

## Example
```python
from vibe_piper.connectors.postgres import PostgreSQLConnector, PostgreSQLConfig
from vibe_piper.validation.history import PostgreSQLValidationHistoryStore

config = PostgreSQLConfig(
    host='localhost',
    port=5432,
    database='vibe_piper',
    user='postgres',
    password='password'
)

connector = PostgreSQLConnector(config)
connector.connect()

store = PostgreSQLValidationHistoryStore(connector)
store.initialize_schema()

# Tables created:
# - validation_runs
# - validation_check_results
# - validation_metrics
# - Indexes for efficient querying
```

## Tables Created
- `validation_runs`: Stores validation run metadata
- `validation_check_results`: Stores individual check results
- `validation_metrics`: Stores quality metric measurements

## Indexes Created
- `idx_validation_runs_asset`: Query by asset name
- `idx_validation_runs_status`: Query by status
- `idx_validation_runs_started_at`: Query by date (descending)
- `idx_check_results_run`: Query check results by run
- `idx_metrics_asset`: Query metrics by asset
- `idx_metrics_metric`: Query metrics by name
- `idx_metrics_timestamp`: Query metrics by date

## Notes
- Schema uses ON DELETE CASCADE for referential integrity
- All tables have created_at timestamp for auditing
- Method is idempotent - safe to call multiple times
- Requires psycopg2 connector with execute_query support
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
