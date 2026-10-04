---
name: write-sql-query
description: Use when writing, reviewing, or optimizing SQL queries for correctness, performance, and maintainability
source: Joe Celko "SQL for Smarties" (5th ed., Morgan Kaufmann 2014); Use The Index, Luke (use-the-index-luke.com); PostgreSQL documentation
tags: [sql, database, performance, query-optimization, indexing, data]
verified: true
---

# Write SQL Query

Write SQL queries that are correct, index-aware, readable, and safe against injection and unintended side effects.

## Why This Is Best Practice

**Adopted by:** PostgreSQL community (Use The Index, Luke), Google (BigQuery SQL style guide), GitLab (SQL query guidelines in engineering handbook)
**Impact:** A missing index on a WHERE clause column can cause full table scans — a 10ms query becomes 10 seconds on a 10M row table. Celko's patterns and index-aware SQL are the standard in performance-critical data engineering.

**Why best:** Most SQL performance problems have the same root cause: the query does not use an available index, or no appropriate index exists. Writing index-aware SQL from the start costs nothing; retroactively optimizing a slow query in production is expensive and disruptive.

## Steps

1. **Understand the execution plan first** — For any non-trivial query: `EXPLAIN ANALYZE` (Postgres), `EXPLAIN FORMAT=JSON` (MySQL), or `EXPLAIN PLAN` (Oracle) before assuming it is efficient.
2. **Write SARGable predicates** — Ensure WHERE clause conditions can use an index: avoid wrapping indexed columns in functions (`WHERE YEAR(created_at) = 2026` → not SARGable; `WHERE created_at >= '2026-01-01'` → SARGable).
3. **Select only needed columns** — Never `SELECT *` in production queries; enumerate columns. Reduces I/O, prevents index-only scan breakage, and avoids surprises when schema changes.
4. **Use JOINs explicitly** — Always specify JOIN type (INNER, LEFT, etc.); never use implicit comma-joins in FROM clause. Explicit JOINs are readable and unambiguous.
5. **Avoid N+1 patterns** — Never execute queries inside loops; use JOIN or a subquery to batch the operation. N+1 is the #1 application-layer SQL anti-pattern.
6. **Use CTEs for readability** — Break complex queries into named CTEs (`WITH ... AS (...)`) for readability; modern optimizers inline CTEs efficiently (Postgres 12+, BigQuery).
7. **Parameterize all user inputs** — Never concatenate user input into SQL strings. Always use prepared statements or parameterized queries; SQL injection is trivially exploitable.

## Rules

- Never run an UPDATE or DELETE without a WHERE clause — add a `LIMIT 1` guard in development to prevent accidents.
- Always test queries on a representative dataset size — a query that runs in 50ms on 1,000 rows may take 50 seconds on 1,000,000.
- Wrap multi-statement data mutations in a transaction; rollback on error.
- Avoid `SELECT DISTINCT` as a band-aid — it usually signals a missing JOIN condition or a data model problem.

## Examples

Non-SARGable (bad):
```sql
SELECT * FROM orders WHERE DATE(created_at) = '2026-03-01';
-- Function on column prevents index use
```

SARGable (good):
```sql
SELECT order_id, total, status
FROM orders
WHERE created_at >= '2026-03-01' AND created_at < '2026-03-02';
-- Range scan on index; only needed columns selected
```

## Common Mistakes

- **`SELECT *` in production** — fetches unused columns, breaks index-only scans, causes hidden bugs when columns are added/dropped.
- **Implicit type coercion in WHERE** — `WHERE user_id = '42'` when `user_id` is integer triggers type cast on every row, preventing index use.
- **Correlated subqueries in SELECT** — executes the subquery once per row; replace with a JOIN or window function.
