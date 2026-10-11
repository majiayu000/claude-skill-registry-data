---
name: mysql
description: MySQL/MariaDB — InnoDB, indexing, replication, JSON, query tuning.
---

# MySQL Reference

## When to Load
Load when the project uses MySQL or MariaDB (signal: `mysql`, `mysql2`, `mysql:` in docker-compose, `DATABASE_URL` with `mysql://`).

## CLI Connection

```bash
mysql -h "$DB_HOST" -P "${DB_PORT:-3306}" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME"
# non-interactive:
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "SELECT VERSION();"
```

Key inspection commands:
```sql
SHOW ENGINE INNODB STATUS;                        -- lock waits, undo log
SHOW FULL PROCESSLIST;                            -- running queries
EXPLAIN FORMAT=JSON SELECT ...;                   -- detailed query plan
SELECT * FROM performance_schema.events_statements_summary_by_digest
  ORDER BY sum_timer_wait DESC LIMIT 10;          -- slow query digest
```

## InnoDB Storage Engine

- Default engine since MySQL 5.5; always use InnoDB (not MyISAM) for new tables
- Row-level locking; supports foreign keys and transactions
- Clustered primary key index: all secondary indexes contain the PK value
- Large PK → large secondary indexes; prefer `INT AUTO_INCREMENT` or compact UUID

## Index Behavior

| Scenario | Recommendation |
|----------|---------------|
| Composite index | Most selective column first; match query column order |
| Covering index | Include all queried columns: `CREATE INDEX idx ON t(a, b) INCLUDE (c)` |
| Prefix index | For long VARCHAR: `CREATE INDEX ON t(col(20))` |
| `EXPLAIN` | Always run before merging slow queries; check `type` column (prefer `ref` or `range`, avoid `ALL`) |

## Transactions & Isolation

Default isolation: `REPEATABLE READ` (unlike PostgreSQL's `READ COMMITTED`).
- MVCC via undo logs (not tuple versioning like Postgres)
- Long transactions grow the undo log → monitor with `SHOW ENGINE INNODB STATUS`
- Use `READ COMMITTED` for OLAP or reporting queries to reduce lock contention

## Replication

| Type | Consistency | Use when |
|------|-------------|----------|
| Async (default) | Eventual | Most setups; risk of data loss on primary failure |
| Semi-sync | Near-sync | One replica ACKs before commit returns |
| GTID-based | Position-independent | Failover without manual binlog coordinates |

- Never write to a replica; use `read_only = ON` on replicas
- Replica lag: monitor `Seconds_Behind_Master` or `performance_schema.replication_connection_status`

## JSON Type (MySQL 5.7.8+)

- Store as `JSON` column for validation; queried with `->` (returns JSON) and `->>` (returns string)
- Index generated columns: `ALTER TABLE t ADD COLUMN col VARCHAR(255) GENERATED ALWAYS AS (json_col->>'$.key') VIRTUAL, ADD INDEX idx(col)`
- Avoid deep nesting; normalize frequently queried fields

## Common Gotchas

| Gotcha | Fix |
|--------|-----|
| Silent truncation in strict mode OFF | Enable `sql_mode = STRICT_ALL_TABLES` |
| `GROUP BY` without `ONLY_FULL_GROUP_BY` silently picks random non-aggregated values | Enable `ONLY_FULL_GROUP_BY` |
| `utf8` charset is actually 3-byte (no emoji) | Use `utf8mb4` + `utf8mb4_unicode_ci` |
| `TINYINT(1)` returned as boolean in some ORMs | Use `TINYINT(1)` deliberately for booleans |
| Deadlocks on concurrent `INSERT ... ON DUPLICATE KEY UPDATE` | Use sparingly; prefer application-level locking |

## Useful Diagnostics

```sql
SHOW ENGINE INNODB STATUS;                          -- lock waits, undo log
SHOW FULL PROCESSLIST;                              -- running queries
SELECT * FROM performance_schema.events_statements_summary_by_digest
  ORDER BY sum_timer_wait DESC LIMIT 10;            -- slow queries
EXPLAIN FORMAT=JSON SELECT ...;                     -- detailed plan
```
