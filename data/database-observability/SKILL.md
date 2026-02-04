---
name: database-observability
description: "Instrument database queries, connection pools, and detect N+1 queries"
triggers:
  - "instrument database"
  - "trace queries"
  - "database metrics"
  - "connection pool monitoring"
  - "slow query detection"
priority: 2
---

# Database Observability

Database is often the bottleneck. Track queries, pools, and patterns.

## Query Span Attributes

| Attribute | Example | Required |
|-----------|---------|----------|
| `db.system` | postgresql, mysql | Yes |
| `db.operation` | SELECT, INSERT | Yes |
| `db.name` | orders_db | Yes |
| `db.sql.table` | users | Recommended |
| `db.statement` | SELECT * FROM users WHERE id = ? | **Parameterized only!** |

## Connection Pool Metrics (USE)

| Metric | Type | Description |
|--------|------|-------------|
| `db.connections.active` | Gauge | In use |
| `db.connections.idle` | Gauge | Available |
| `db.connections.max` | Gauge | Pool limit |
| `db.connections.wait_count` | Counter | Had to wait |
| `db.connections.wait_duration` | Histogram | Wait time |

## Issues to Detect

| Issue | Detection | Fix |
|-------|-----------|-----|
| **N+1 queries** | >10 identical queries per request | Use eager loading |
| **Slow queries** | Duration > p95 threshold | Add indexes, optimize |
| **Pool exhaustion** | wait_count increasing | Increase pool, fix leaks |

## Query Wrapper Pattern

```
Before: Start span (db.system, db.operation, db.sql.table), start timer
After:  Record duration, set db.rows_affected, record errors, end span
```

## Pool Monitor Pattern

```
Every 10s: Record active, idle, wait_count, wait_duration from pool stats
```

## Anti-Patterns

- **Full SQL with values** → PII risk, use parameterized only
- **No pool metrics** → Can't detect saturation
- **Missing slow query alerts** → Problems go unnoticed

## References

- `references/methodology/use-methodology.md`
- `references/platforms/{platform}/database.md`
