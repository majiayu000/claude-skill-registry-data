---
name: postgres-query-optimization
description: PostgreSQL query optimization and performance tuning reference. Use when analyzing slow queries, interpreting EXPLAIN output, optimizing indexes, or troubleshooting database performance issues.
---

# PostgreSQL Query Optimization

## EXPLAIN Basics

### Running EXPLAIN
```sql
-- Basic plan (no execution)
EXPLAIN SELECT * FROM orders WHERE customer_id = 123;

-- With actual execution times and row counts
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123;

-- With buffer/IO statistics
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE customer_id = 123;

-- Full verbose output with all options
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON) SELECT * FROM orders WHERE customer_id = 123;
```

### Key Metrics to Watch
- **actual time**: First row time..last row time in milliseconds
- **rows**: Estimated vs actual row counts (large differences indicate stale statistics)
- **loops**: How many times the node executed (important for nested loops)
- **Buffers**: shared hit (cache) vs shared read (disk)—high read count = slow
- **Planning Time**: Query planning overhead
- **Execution Time**: Actual query execution time

## Scan Types

### Sequential Scan (Seq Scan)
Reads every row in the table. Acceptable for:
- Small tables (<10K rows typically)
- Queries returning large % of table (>5-10%)
- No suitable index exists

**Red flag**: Seq Scan on large table with highly selective WHERE clause.

### Index Scan
Uses B-tree index to find rows, then fetches from heap. Best for:
- Highly selective queries (<5% of rows)
- Sorted output matching index order

### Index Only Scan
Answers query entirely from index (no heap fetch). Requires:
- All needed columns in index (via INCLUDE or as key columns)
- Table's visibility map is up-to-date (run VACUUM)

**Goal**: Convert Index Scan → Index Only Scan for read-heavy queries.

### Bitmap Index Scan
Combines multiple index conditions or handles medium selectivity. Pattern:
1. Bitmap Index Scan: Build bitmap of matching pages
2. Bitmap Heap Scan: Fetch pages and recheck conditions

Good for OR conditions and medium selectivity (5-20% of rows).

## Join Types

### Nested Loop
For each row in outer table, scan inner table. Best when:
- Inner table has good index
- Outer table is small
- Join returns few rows

### Hash Join
Builds hash table from smaller table, probes with larger. Best for:
- Larger joins without useful indexes
- Equality joins only

Watch for: `Batches > 1` means hash table spilled to disk (increase `work_mem`).

### Merge Join
Both inputs sorted, merge together. Best for:
- Large sorted datasets
- Indexes provide sort order
- Multiple equality conditions

## Common Performance Issues

### N+1 Query Problem
**Symptom**: Many small queries instead of one efficient join.
```sql
-- Bad: N+1 pattern (in application)
SELECT * FROM orders WHERE id = 1;
SELECT * FROM order_items WHERE order_id = 1;
SELECT * FROM orders WHERE id = 2;
SELECT * FROM order_items WHERE order_id = 2;
-- ... repeated N times

-- Good: Single query with JOIN
SELECT o.*, oi.*
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
WHERE o.customer_id = 123;
```

### Missing Index on FK
**Symptom**: Slow deletes on parent table, slow joins.
```sql
-- Check for missing FK indexes
SELECT
    c.conrelid::regclass AS table_name,
    a.attname AS column_name,
    c.confrelid::regclass AS referenced_table
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid
    AND a.attnum = ANY(i.indkey)
);
```

### Over-Indexing
**Symptom**: Slow inserts/updates, excessive disk usage.
```sql
-- Find unused indexes
SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    pg_size_pretty(pg_relation_size(i.indexrelid)) AS size,
    idx_scan AS scans
FROM pg_stat_user_indexes i
JOIN pg_index USING (indexrelid)
WHERE idx_scan = 0
AND NOT indisunique
AND NOT indisprimary
ORDER BY pg_relation_size(i.indexrelid) DESC;
```

### Stale Statistics
**Symptom**: Planner estimates wildly wrong vs actual rows.
```sql
-- Check table statistics freshness
SELECT
    schemaname,
    relname,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze,
    n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Force statistics update
ANALYZE table_name;
ANALYZE VERBOSE table_name;  -- with progress
```

### Inefficient Pagination
**Symptom**: OFFSET-based pagination gets slower for higher pages.
```sql
-- Bad: OFFSET pagination (rescans all previous rows)
SELECT * FROM orders ORDER BY created_at DESC OFFSET 10000 LIMIT 20;

-- Good: Keyset/cursor pagination
SELECT * FROM orders
WHERE created_at < '2024-01-15T10:30:00Z'
ORDER BY created_at DESC
LIMIT 20;
```

## Index Selection Strategy

### When to Create Indexes
1. **WHERE clause columns**: Frequently filtered columns
2. **JOIN columns**: Both sides of JOIN conditions
3. **ORDER BY columns**: For sorted output without extra sort
4. **Foreign keys**: Always index FK columns (PostgreSQL doesn't auto-create)
5. **Unique constraints**: Already create indexes automatically

### Index Types by Use Case

| Use Case | Index Type | Example |
|----------|------------|---------|
| Equality, range, ORDER BY | B-tree (default) | `CREATE INDEX ON orders (status)` |
| JSONB containment | GIN | `CREATE INDEX ON docs USING GIN (data)` |
| Array operations | GIN | `CREATE INDEX ON posts USING GIN (tags)` |
| Full-text search | GIN | `CREATE INDEX ON articles USING GIN (to_tsvector('english', body))` |
| Range overlap | GiST | `CREATE INDEX ON bookings USING GiST (daterange)` |
| Time-series (huge tables) | BRIN | `CREATE INDEX ON logs USING BRIN (created_at)` |
| Pattern matching (LIKE) | GIN + pg_trgm | `CREATE INDEX ON users USING GIN (name gin_trgm_ops)` |

### Partial Indexes
Index only rows matching a condition:
```sql
-- Only index active orders (common query pattern)
CREATE INDEX ON orders (customer_id) WHERE status = 'active';

-- Only index non-null values
CREATE INDEX ON users (referral_code) WHERE referral_code IS NOT NULL;
```

### Covering Indexes
Include extra columns for index-only scans:
```sql
-- Query: SELECT name, email FROM users WHERE id = ?
CREATE INDEX ON users (id) INCLUDE (name, email);
```

### Expression Indexes
Index computed values:
```sql
-- Case-insensitive email lookup
CREATE INDEX ON users (LOWER(email));

-- JSONB field extraction
CREATE INDEX ON products ((data->>'category'));

-- Date part extraction
CREATE INDEX ON events (DATE(created_at));
```

## pg_stat_statements

Essential extension for query performance monitoring.

### Enable and Configure
```sql
-- In postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all

-- Create extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

### Find Slowest Queries
```sql
-- Top 10 by total time
SELECT
    calls,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS percent_total,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Queries with high variance (inconsistent performance)
SELECT
    calls,
    round(mean_exec_time::numeric, 2) AS mean_ms,
    round(stddev_exec_time::numeric, 2) AS stddev_ms,
    query
FROM pg_stat_statements
WHERE calls > 100
ORDER BY stddev_exec_time DESC
LIMIT 10;
```

### Reset Statistics
```sql
SELECT pg_stat_statements_reset();
```

## Lock Monitoring

### Current Locks
```sql
SELECT
    pg_class.relname,
    pg_locks.mode,
    pg_locks.granted,
    pg_stat_activity.query,
    pg_stat_activity.pid
FROM pg_locks
JOIN pg_class ON pg_locks.relation = pg_class.oid
JOIN pg_stat_activity ON pg_locks.pid = pg_stat_activity.pid
WHERE pg_class.relname NOT LIKE 'pg_%'
ORDER BY pg_class.relname;
```

### Blocked Queries
```sql
SELECT
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query,
    now() - blocked.query_start AS blocked_duration
FROM pg_stat_activity blocked
JOIN pg_locks blocked_locks ON blocked.pid = blocked_locks.pid
JOIN pg_locks blocking_locks ON blocked_locks.locktype = blocking_locks.locktype
    AND blocked_locks.relation = blocking_locks.relation
    AND blocked_locks.pid != blocking_locks.pid
JOIN pg_stat_activity blocking ON blocking_locks.pid = blocking.pid
WHERE NOT blocked_locks.granted;
```

### Long-Running Transactions
```sql
SELECT
    pid,
    now() - xact_start AS duration,
    state,
    query
FROM pg_stat_activity
WHERE state != 'idle'
AND xact_start < now() - interval '5 minutes'
ORDER BY duration DESC;
```

## Connection Management

### Current Connections
```sql
SELECT
    state,
    COUNT(*) AS count,
    MAX(now() - state_change) AS max_duration
FROM pg_stat_activity
GROUP BY state;
```

### Connection Pool Sizing
Rule of thumb: `connections = (core_count * 2) + effective_spindle_count`

For most web apps with SSD: 10-20 connections per CPU core is reasonable.

### Idle Connection Cleanup
```sql
-- Terminate idle connections older than 10 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < now() - interval '10 minutes';
```

## Memory Settings

### work_mem
Memory per operation (sort, hash). Default 4MB is often too low.
```sql
-- Check current setting
SHOW work_mem;

-- Set for session (for heavy analytical queries)
SET work_mem = '256MB';

-- Check if sorts are spilling to disk
EXPLAIN (ANALYZE, BUFFERS) SELECT ... ORDER BY ...;
-- Look for: "Sort Method: external merge Disk:"
```

### shared_buffers
Main memory cache. Start with 25% of system RAM.

### effective_cache_size
Hint to planner about total cache (OS + PostgreSQL). Set to ~75% of RAM.

## Query Patterns to Avoid

### SELECT *
Fetch only needed columns for smaller data transfer and potential index-only scans.

### Functions on Indexed Columns
```sql
-- Bad: Can't use index on created_at
WHERE DATE(created_at) = '2024-01-15'

-- Good: Range query uses index
WHERE created_at >= '2024-01-15' AND created_at < '2024-01-16'
```

### OR with Different Columns
```sql
-- Bad: Often causes Seq Scan
WHERE status = 'active' OR customer_id = 123

-- Better: UNION of indexed queries
SELECT * FROM orders WHERE status = 'active'
UNION ALL
SELECT * FROM orders WHERE customer_id = 123 AND status != 'active'
```

### DISTINCT When Not Needed
DISTINCT adds sort/hash overhead. Ensure your query design eliminates duplicates naturally through proper joins.

### Correlated Subqueries
```sql
-- Bad: Executes subquery for each row
SELECT * FROM orders o
WHERE total > (SELECT AVG(total) FROM orders WHERE customer_id = o.customer_id);

-- Good: Use window function or CTE
WITH customer_avg AS (
    SELECT customer_id, AVG(total) AS avg_total
    FROM orders
    GROUP BY customer_id
)
SELECT o.*
FROM orders o
JOIN customer_avg ca ON o.customer_id = ca.customer_id
WHERE o.total > ca.avg_total;
```

## Performance Checklist

1. **EXPLAIN ANALYZE** your slow queries
2. Check estimated vs actual rows (stale stats?)
3. Look for Seq Scans on large tables
4. Verify indexes exist for WHERE/JOIN columns
5. Check for missing FK indexes
6. Review work_mem for sorts spilling to disk
7. Consider partial/covering indexes for hot queries
8. Use keyset pagination instead of OFFSET
9. Enable pg_stat_statements for ongoing monitoring
10. Regular VACUUM ANALYZE for fresh statistics
