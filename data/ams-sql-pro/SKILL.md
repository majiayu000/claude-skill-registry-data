---
name: sql-pro
description: Expert SQL patterns for complex queries, optimization, and cross-database portability — use when writing, tuning, or debugging SQL.
category: database
---

## Overview

SQL is the lingua franca of data work, but writing SQL that is both correct and fast
requires more than knowing `SELECT`. This skill covers advanced querying techniques,
portability across dialects (PostgreSQL, MySQL, SQLite, SQL Server), and the
optimization habits that keep queries quick as data grows.

## When to use

- Writing multi-table joins, subqueries, or window functions
- Debugging a query that returns wrong results or runs slowly
- Migrating queries between database dialects (e.g. MySQL → PostgreSQL)
- Reviewing generated or hand-written SQL for correctness and performance
- Building reports, aggregations, or data pipelines in SQL

## Core concepts

**Set thinking, not loop thinking.** SQL operates on sets of rows. Prefer set
operations (`JOIN`, `UNION`, `GROUP BY`) over row-by-row logic. If you find yourself
"iterating" mentally, look for a set-based formulation — it will be both shorter and
faster.

**CTEs for readability.** Common table expressions (`WITH ... AS`) turn nested
subqueries into named, testable steps. Prefer CTEs over deeply nested subqueries,
and prefer `EXISTS` over `IN` when testing membership against large sets.

**Window functions.** `ROW_NUMBER()`, `RANK()`, `LAG()`, `LEAD()`, and running
`SUM() OVER (...)` answer questions like "top N per group" or "change from the
previous row" without self-joins:

```sql
WITH ranked AS (
  SELECT customer_id, order_date, total,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
  FROM orders
)
SELECT * FROM ranked WHERE rn = 1;  -- latest order per customer
```

**Dialect portability.** String functions, date arithmetic, and quoting differ across
engines. Stick to standard SQL (`||` or `CONCAT` sparingly, `CAST`, `EXTRACT`) where
portable, and isolate dialect-specific code (e.g. `DATE_TRUNC` in Postgres,
`LIMIT` vs `TOP`) behind clearly marked sections when porting.

**Read the execution plan.** `EXPLAIN` / `EXPLAIN ANALYZE` shows how the engine
executes your query. Learn to spot full table scans, unindexed nested loops, and
misestimated row counts — these are where 90% of slowdowns come from.

## Practical workflow

1. **Restate the question in plain language** — "per customer, their most recent
   order" maps directly to a window function, not a correlated subquery.
2. **Write the smallest correct version first.** Verify results on a small sample
   (`WHERE ... LIMIT 100`) before scaling to full tables.
3. **Check row counts at each step.** A join that multiplies rows silently is the
   most common source of wrong aggregates — add `COUNT(*)` probes while building.
4. **Add filtering early.** Push `WHERE` predicates as deep as possible so the engine
   filters before joining and aggregating.
5. **Handle NULLs explicitly.** `NULL = NULL` is false; use `IS NULL` / `COALESCE`
   deliberately, and know that `NOT IN` with a NULL in the set returns nothing.
6. **Run EXPLAIN** on the final query; add or reorder indexes only after seeing the
   actual plan, not by guessing.
7. **Test edge cases:** empty tables, ties in `ORDER BY` for `TOP 1` patterns,
   duplicate keys in joins, and timezone-naive vs aware timestamps.

**Quick index checklist:** index foreign keys, columns in `WHERE` equality filters,
and leading columns of `ORDER BY` in paginated queries. Avoid indexing every
column — each index costs write speed and disk.

## Common pitfalls

- **`SELECT *` in production queries** — breaks silently when columns are added and
  drags unnecessary data. List columns explicitly.
- **Aggregating before deduplicating** — joining one-to-many tables before `SUM()`
  inflates totals. Aggregate first, join after.
- **Implicit type casts** — comparing a timestamp column to a string, or an
  integer column to text, can silently disable index use. Match types exactly.
- **Correlated subqueries in the SELECT list** — run once per row; rewrite as a
  single join or window function.
- **Non-deterministic `LIMIT 1`** without `ORDER BY` — returns an arbitrary row,
  and different runs can differ.
- **Forgetting transaction isolation** — long reporting queries on a live database
  can see inconsistent snapshots; use a read replica or an explicit isolation
  level when consistency matters.
