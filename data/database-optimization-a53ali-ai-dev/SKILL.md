---
name: database-optimization
description: Analyse and fix slow database queries using EXPLAIN ANALYZE, index strategy, N+1 detection, connection pooling, and query rewriting patterns — with clear trade-off guidance on when to escalate to a DBA
triggers:
  - "database optimization"
  - "slow query"
  - "EXPLAIN ANALYZE"
  - "index strategy"
  - "N+1 query"
  - "connection pooling"
  - "query rewrite"
  - "database performance"
  - "slow query log"
  - "pagination performance"
  - "SELECT *"
  - "covering index"
audience: engineer
---

# Database Optimization

## Context
Database performance problems account for a disproportionate share of application latency. A single missing index can turn a 1ms query into a 30-second table scan at scale. Yet adding too many indexes degrades write throughput — every insert, update, or delete must maintain each index.

The governing principle: **indexes are a write tax paid for a read benefit.** Understanding this trade-off prevents the two most common mistakes: no indexes (slow reads) and too many indexes (slow writes).

Use this skill when:
- A query is identified as slow via APM traces, slow query logs, or `EXPLAIN ANALYZE`
- A table is growing and previously fast queries are degrading
- An ORM is generating suspicious SQL (N+1, missing joins, `SELECT *`)
- You are designing a schema and want to choose indexes deliberately
- A migration is adding or removing columns on a large table

**This skill is PostgreSQL-primary** with notes where MySQL/SQLite differ materially.

---

## Instructions / Steps

### Step 1: Find the Slow Queries

Before tuning, identify which queries actually need it.

**Enable slow query logging (PostgreSQL):**
```sql
-- Log queries taking more than 100ms
ALTER SYSTEM SET log_min_duration_statement = 100;
SELECT pg_reload_conf();

-- View current setting
SHOW log_min_duration_statement;
```

**Find slow queries in pg_stat_statements (extension must be enabled):**
```sql
-- Top 10 queries by total execution time
SELECT
  query,
  calls,
  round(total_exec_time::numeric, 2) AS total_ms,
  round(mean_exec_time::numeric, 2) AS avg_ms,
  round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS percent_total
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

**Find missing indexes (queries doing sequential scans on large tables):**
```sql
SELECT
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  n_live_tup
FROM pg_stat_user_tables
WHERE seq_scan > 0
  AND n_live_tup > 10000
ORDER BY seq_tup_read DESC;
```

### Step 2: Run EXPLAIN ANALYZE

Always run `EXPLAIN (ANALYZE, BUFFERS)` — never `EXPLAIN` alone (which doesn't execute the query).

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT
  o.id,
  o.total_amount,
  u.email
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending'
  AND o.created_at > now() - interval '7 days'
ORDER BY o.created_at DESC
LIMIT 50;
```

### Step 3: Interpret EXPLAIN ANALYZE Output

**Node types and what they mean:**

| Node Type | Meaning | Action |
|---|---|---|
| `Seq Scan` | Full table scan | Almost always add an index if table is large |
| `Index Scan` | Reads index, then heap | Good for selective (<5%) queries |
| `Index Only Scan` | Reads index only, skips heap | Optimal — consider covering indexes to achieve this |
| `Bitmap Heap Scan` | Batched index lookup | Good for 5-20% selectivity |
| `Bitmap Index Scan` | Builds bitmap from index | Precedes Bitmap Heap Scan |
| `Hash Join` | Hashes smaller table, probes larger | Good for large unsorted sets |
| `Merge Join` | Merge of two sorted sets | Requires sorted input or sort step |
| `Nested Loop` | Per-row lookup of inner side | Fast only if inner side is indexed and small |
| `Sort` | In-memory or on-disk sort | On-disk sort (`Sort Method: external`) = add index to avoid |

**Cost and timing:**

```
->  Seq Scan on orders  (cost=0.00..15420.00 rows=320000 width=48)
                         (actual time=0.012..183.4 rows=320000 loops=1)
    Buffers: shared hit=1820 read=2640
```

| Field | Meaning |
|---|---|
| `cost=X..Y` | Estimated cost: X = startup, Y = total (arbitrary units) |
| `actual time=X..Y` | Measured ms: X = first row, Y = all rows |
| `rows=N` (estimated) vs `rows=M` (actual) | Huge discrepancy → stale statistics → run `ANALYZE` |
| `shared hit=N` | Pages served from buffer cache (good) |
| `shared read=N` | Pages read from disk (slow, consider larger `shared_buffers`) |
| `loops=N` | Node executed N times — multiply `actual time` by loops for true total |

**Identify the bottleneck node:** look for the node with the highest `actual time` and widest row estimate discrepancy. That's where to focus.

### Step 4: Index Strategy

#### B-tree Index (default — covers most cases)
```sql
-- Single column index for equality and range queries
CREATE INDEX CONCURRENTLY idx_orders_status ON orders(status);

-- Always use CONCURRENTLY on production tables to avoid locking
CREATE INDEX CONCURRENTLY idx_orders_created_at ON orders(created_at DESC);
```

#### Composite Index (multi-column)
```sql
-- Column order matters: put equality columns first, range column last
-- This serves: WHERE status = 'pending' AND created_at > X
CREATE INDEX CONCURRENTLY idx_orders_status_created
ON orders(status, created_at DESC);

-- Rule: the leading column must appear in the WHERE clause for the index to be used
-- This index does NOT serve: WHERE created_at > X (without status filter)
```

#### Partial Index (indexes only rows matching a condition)
```sql
-- Only index pending orders — index stays small even as completed orders grow
CREATE INDEX CONCURRENTLY idx_orders_pending
ON orders(created_at DESC)
WHERE status = 'pending';

-- Query must use the exact filter condition to use this index:
-- WHERE status = 'pending' AND created_at > ...  ✓
-- WHERE status = 'completed' AND created_at > ... ✗ (won't use this index)
```

#### Covering Index (include all selected columns to enable Index Only Scan)
```sql
-- If your query selects user_id and amount, include them in the index
-- to avoid the heap fetch entirely
CREATE INDEX CONCURRENTLY idx_orders_status_covering
ON orders(status, created_at DESC)
INCLUDE (user_id, total_amount);
```

#### Index Creation Checklist

Before creating an index, answer:
- [ ] Is the column used in a `WHERE`, `JOIN ON`, or `ORDER BY` clause in a slow query?
- [ ] Is the table large enough for an index to help? (Rule of thumb: > 1,000 rows)
- [ ] What is the selectivity? (Low cardinality columns like booleans rarely benefit)
- [ ] What is the write volume on this table? (High-write tables: count indexes carefully)
- [ ] Does a composite index already exist with this column as the second position? (May already be covered)
- [ ] Are you using `CONCURRENTLY` to avoid locking?

**Check existing indexes before creating new ones:**
```sql
SELECT
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename = 'orders'
ORDER BY indexname;

-- Also check index usage — drop unused indexes
SELECT
  indexrelname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname = 'orders'
ORDER BY idx_scan ASC;  -- Low idx_scan = possibly unused
```

### Step 5: Fix N+1 Queries

N+1 occurs when ORM lazy loading fires one query per object in a loop.

**Detecting N+1:**
```bash
# PostgreSQL: watch for repetitive queries with different parameter values
tail -f /var/log/postgresql/postgresql.log | grep -E 'SELECT.*users.*WHERE id'

# In Node.js, use sequelize-log or enable query logging:
# sequelize = new Sequelize({ logging: console.log })

# In Rails:
# Use the bullet gem — it auto-detects N+1 and alerts in development
```

**Fixing N+1 — use a JOIN instead of a loop:**
```sql
-- BAD: one query per order
SELECT * FROM orders WHERE user_id = ?;  -- runs N times

-- GOOD: one query for all users with their orders
SELECT
  u.id,
  u.email,
  o.id AS order_id,
  o.total_amount,
  o.created_at
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.id = ANY($1::int[])  -- pass all user IDs at once
ORDER BY u.id, o.created_at DESC;
```

**Or use a subquery / IN clause for independent lookups:**
```sql
SELECT * FROM products
WHERE id IN (
  SELECT DISTINCT product_id FROM order_items WHERE order_id = ANY($1::int[])
);
```

### Step 6: Query Rewriting Patterns

#### Avoid SELECT *
```sql
-- BAD: fetches all columns, including large text/blob fields
SELECT * FROM articles WHERE author_id = 42;

-- GOOD: fetch only what you need
SELECT id, title, published_at, slug FROM articles WHERE author_id = 42;
```

#### Push Predicates Down (filter early)
```sql
-- BAD: join first, filter later — more rows in the join
SELECT o.*, p.name
FROM orders o
JOIN products p ON o.product_id = p.id
WHERE o.created_at > now() - interval '30 days';

-- GOOD: filter orders before joining (if the planner isn't doing it already)
WITH recent_orders AS (
  SELECT * FROM orders WHERE created_at > now() - interval '30 days'
)
SELECT ro.*, p.name
FROM recent_orders ro
JOIN products p ON ro.product_id = p.id;
```

#### CTEs — Use Wisely (PostgreSQL 12+ materialisation change)
```sql
-- In PostgreSQL < 12, CTEs were always materialised (optimisation fence)
-- In PostgreSQL >= 12, planner can inline them unless you add MATERIALIZED
-- Use MATERIALIZED only when you need to prevent re-evaluation:
WITH MATERIALIZED expensive_calc AS (
  SELECT user_id, COUNT(*) AS order_count FROM orders GROUP BY user_id
)
SELECT u.email, ec.order_count FROM users u JOIN expensive_calc ec ON u.id = ec.user_id;
```

#### Pagination — Keyset over OFFSET

```sql
-- BAD: OFFSET pagination scans all prior rows — gets slower as page number grows
SELECT id, title, created_at FROM posts
ORDER BY created_at DESC
OFFSET 10000 LIMIT 20;

-- GOOD: keyset pagination — always fast regardless of page depth
-- Pass the created_at and id of the last item on the previous page
SELECT id, title, created_at FROM posts
WHERE (created_at, id) < ($last_created_at, $last_id)  -- tuple comparison
ORDER BY created_at DESC, id DESC
LIMIT 20;
-- Requires composite index: CREATE INDEX ON posts(created_at DESC, id DESC)
```

### Step 7: PostgreSQL Maintenance (VACUUM / ANALYZE)

```sql
-- Check table bloat and dead tuples (high dead_tup_ratio → needs VACUUM)
SELECT
  schemaname,
  relname,
  n_live_tup,
  n_dead_tup,
  round(100 * n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
  last_vacuum,
  last_autovacuum,
  last_analyze,
  last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Manual vacuum on a specific table
VACUUM ANALYZE orders;

-- Aggressive vacuum (reclaims space, use outside peak hours)
VACUUM FULL ANALYZE orders;  -- CAUTION: takes exclusive lock

-- Update statistics so planner has accurate row estimates
ANALYZE orders;
```

### Step 8: Connection Pooling

Never open a new database connection per request. Use a connection pool:

| Pooler | When to use |
|---|---|
| Application-level (pg-pool, HikariCP, SQLAlchemy pool) | Single-service, simple setup |
| PgBouncer | Multiple services, high concurrency, PostgreSQL |
| RDS Proxy | AWS RDS/Aurora, serverless functions |

**PgBouncer key settings:**
```ini
[pgbouncer]
pool_mode = transaction         ; transaction pooling — best for stateless apps
max_client_conn = 1000
default_pool_size = 20          ; size per database/user pair
reserve_pool_size = 5
server_idle_timeout = 600
```

**Check connection exhaustion:**
```sql
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
SELECT max_conn, used, res_for_super FROM
  (SELECT count(*) used FROM pg_stat_activity) t,
  (SELECT setting::int res_for_super FROM pg_settings WHERE name='superuser_reserved_connections') t2,
  (SELECT setting::int max_conn FROM pg_settings WHERE name='max_connections') t3;
```

---

## Common Anti-Patterns

| Anti-Pattern | Impact | Fix |
|---|---|---|
| `SELECT *` in application queries | Fetches unnecessary data; breaks if schema changes | Select only needed columns |
| Index on low-cardinality column alone | Index ignored by planner | Combine with high-cardinality column in composite index |
| OFFSET pagination on large tables | O(n) scan; gets slower every page | Keyset (cursor-based) pagination |
| `LIKE '%term%'` on large text columns | Forces sequential scan | Full-text search (`to_tsvector` + GIN index) |
| No index on foreign keys | Slow JOIN and cascade deletes | Index all FK columns |
| Function on indexed column in WHERE | Index cannot be used | Rewrite predicate or use function-based index |
| `OR` instead of `UNION ALL` for disjoint sets | Prevents index use | Use `UNION ALL` for disjoint conditions |
| Implicit type cast in WHERE | Index not used | Ensure column type matches parameter type |
| Auto-commit in batch inserts | Each row is a transaction | Wrap batch inserts in explicit transaction |

---

## When to Escalate to a DBA

Escalate when:
- You need `VACUUM FULL` on a very large table in production (requires lock planning)
- Bloat is > 30% and autovacuum cannot keep up
- You need to add a column with a non-null default on a table with millions of rows
- `max_connections` is routinely exhausted and connection pooler tuning hasn't helped
- Query plans change unexpectedly after a PostgreSQL version upgrade
- You need to partition a large table that is already in production

---

## Output Format
When applying this skill, the agent should:
- Run `EXPLAIN (ANALYZE, BUFFERS)` and interpret the output with specific findings
- Identify the bottleneck node (highest actual time, largest row estimate discrepancy)
- Propose a specific index with justification (type, column order, partial condition if applicable)
- Show the `CREATE INDEX CONCURRENTLY` statement ready to run
- Rewrite any N+1-generating code with the batched equivalent
- Flag `SELECT *`, OFFSET pagination, and function-on-indexed-column anti-patterns
- Include a `VACUUM ANALYZE` recommendation if dead tuple ratio is high
- Note write-throughput trade-off for any new index suggested

---

## References
- [Using EXPLAIN — PostgreSQL Documentation](https://www.postgresql.org/docs/current/using-explain.html)
- [Indexes — PostgreSQL Documentation](https://www.postgresql.org/docs/current/indexes.html)
- [pg_stat_statements — PostgreSQL Documentation](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [Data Patterns — Martin Fowler](https://martinfowler.com/books/eaa.html)
- [Use the Index, Luke (SQL performance guide)](https://use-the-index-luke.com/)
- [PgBouncer Documentation](https://www.pgbouncer.org/config.html)
- [Keyset Pagination — Markus Winand](https://use-the-index-luke.com/no-offset)
