---
name: postgres
description: Use when working with PostgreSQL specifically. Covers indexing, MVCC and vacuum, connection pooling, partitioning, JSONB, replication, and the operational realities that separate Postgres from generic SQL.
metadata:
  category: data
  version: 1.0.0
  tags: [postgres, database, indexing, vacuum, replication]
---

# PostgreSQL

## Purpose

Operate PostgreSQL well: understand what MVCC costs you, why the table is bloated, why the connection count matters more than you think, and how to change a large table without locking it.

## When to Use

- Designing schemas or indexes for Postgres.
- Diagnosing bloat, slow queries, or lock contention.
- Configuring connection pooling and replication.
- Running a migration on a large table without downtime.

## Capabilities

- Index types: B-tree, GIN, GiST, BRIN, partial, expression, covering.
- MVCC, dead tuples, autovacuum tuning, and transaction ID wraparound.
- Connection pooling with PgBouncer and the pooling modes.
- Partitioning: declarative range and list partitions.
- JSONB indexing and query patterns.
- Streaming replication, replicas, and replication lag.

## Inputs

- The schema, the table sizes, and the query patterns.
- `pg_stat_statements` output for the slow-query question.
- Server configuration and Postgres version.

## Outputs

- Indexes that match the access patterns, with no unused ones.
- Autovacuum settings appropriate to the write volume.
- Migrations that acquire only brief locks.

## Workflow

1. **Find the real slow queries** — `pg_stat_statements` ordered by total time, not by mean. A 30ms query executed a million times costs more than a 4-second query run once.
2. **Index for the access pattern** — Equality columns first in a composite index, then the range or sort column. Add partial indexes for the filters that dominate.
3. **Watch the dead tuples** — Every `UPDATE` writes a new row version and leaves the old one dead. A hot table with default autovacuum settings will bloat and slow down.
4. **Pool the connections** — Each Postgres connection is a process with real memory cost. Beyond a few hundred, performance degrades. PgBouncer in transaction mode is the standard answer.
5. **Migrate without locking** — `CREATE INDEX CONCURRENTLY`. Add columns nullable, backfill in batches, then set defaults and constraints with `NOT VALID` followed by `VALIDATE`.
6. **Set a lock timeout** — Before any DDL: `SET lock_timeout = '3s'`. A migration that waits behind a long transaction will queue every subsequent query behind itself.

## Best Practices

- `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT <value>` is safe on Postgres 11+ (no table rewrite). Adding a `CHECK` constraint or a foreign key still requires a scan — use `NOT VALID`, then `VALIDATE CONSTRAINT` separately.
- An unused index is a write-amplification tax paid on every insert and update. `pg_stat_user_indexes` shows which have never been scanned. Drop them.
- Autovacuum defaults are tuned for a small database. On a high-write table, lower `autovacuum_vacuum_scale_factor` for that table specifically.
- `idle in transaction` connections hold locks and block vacuum indefinitely. Set `idle_in_transaction_session_timeout`.
- PgBouncer in transaction mode breaks prepared statements, `LISTEN/NOTIFY`, and session-level `SET`. Know this before adopting it, not after.
- Replicas serve read traffic but lag. A read-after-write on a replica will see stale data — route the read to the primary or accept it.

## Examples

**A migration on a large table that takes no meaningful lock:**

```sql
-- Adding a NOT NULL column with a default: safe and instant on PG 11+.
ALTER TABLE orders ADD COLUMN currency text NOT NULL DEFAULT 'USD';

-- A foreign key normally takes a lock and scans the whole table. Split it:
ALTER TABLE orders
  ADD CONSTRAINT orders_customer_fk
  FOREIGN KEY (customer_id) REFERENCES customers(id)
  NOT VALID;                              -- instant: only new rows are checked

ALTER TABLE orders VALIDATE CONSTRAINT orders_customer_fk;
                                          -- scans, but takes only a SHARE UPDATE
                                          -- EXCLUSIVE lock: writes continue.

-- An index without blocking writes:
SET lock_timeout = '3s';                  -- do not queue behind a long transaction
CREATE INDEX CONCURRENTLY idx_orders_customer_created
  ON orders (customer_id, created_at DESC)
  WHERE deleted_at IS NULL;
```

**Finding the queries and the indexes that matter:**

```sql
-- The queries that actually consume the database, by total time.
SELECT
  substring(query, 1, 80) AS query,
  calls,
  round(total_exec_time::numeric, 0) AS total_ms,
  round(mean_exec_time::numeric, 2) AS mean_ms,
  rows / GREATEST(calls, 1) AS avg_rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 15;

-- Indexes that have never been used: pure write overhead.
SELECT relname AS table, indexrelname AS index,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelid NOT IN (
  SELECT conindid FROM pg_constraint WHERE contype IN ('p','u')
)
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Notes

- `CREATE INDEX CONCURRENTLY` cannot run inside a transaction block, and it can fail leaving an invalid index behind. Check `pg_index.indisvalid` afterwards and drop any invalid index before retrying.
- Transaction ID wraparound is the failure mode that takes a Postgres cluster fully offline. It only happens when autovacuum has been failing for a long time and being ignored — monitor `age(datfrozenxid)`.
- JSONB is excellent for genuinely schemaless data and a poor substitute for columns. A JSONB field that every query filters on should be a column with an index.
