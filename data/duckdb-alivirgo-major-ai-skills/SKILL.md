---
name: duckdb
description: "Query local CSV and Parquet files with DuckDB SQL, aggregate and join datasets, export analytical results, and troubleshoot schema drift or memory limits."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["duckdb", "sql", "parquet", "analytics", "olap", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# DuckDB Analytical SQL AI Skill Guide

## Overview & Engine Architecture

DuckDB is an embedded OLAP database: columnar storage/execution, vectorized operators, and direct scans of Parquet/CSV/JSON without a server. Agents write SQL against files or attached databases, push filters into scans, and export results via `COPY` or DataFrame APIs instead of reinventing aggregations in Python.

```
Parquet/CSV/HTTP
      -> DuckDB engine (in-process)
          -> SQL (joins, window, aggregate)
          -> result / COPY / DataFrame
```

## When to use this skill

- Ad-hoc SQL on local or lake files
- Replacing heavy pandas groupbys with SQL
- Lightweight warehouses for notebooks and CI checks

## Operational directives

1. Query files with `read_parquet` / `read_csv_auto` (or glob paths) before inventing loaders.
2. Create views for repeated logic; persist only when you need indexes/reuse.
3. Prefer `COPY ... TO 'out.parquet'` for large exports.
4. Set memory/thread limits for shared CI runners.
5. Never embed production secrets in attached remote extensions without review.

## Query Parquet example

```sql
INSTALL httpfs; LOAD httpfs;  -- only if remote paths needed

SELECT
  customer_id,
  date_trunc('month', created_at) AS month,
  sum(amount) AS revenue,
  count(*) AS orders
FROM read_parquet('data/orders/*.parquet')
WHERE created_at >= DATE '2025-01-01'
GROUP BY 1, 2
ORDER BY revenue DESC;
```

## Python usage

```python
import duckdb

con = duckdb.connect("analytics.duckdb")
con.execute("CREATE OR REPLACE VIEW orders AS SELECT * FROM read_parquet('data/orders/*.parquet')")
df = con.execute("""
  SELECT customer_id, sum(amount) AS revenue
  FROM orders
  GROUP BY 1
  ORDER BY 2 DESC
  LIMIT 20
""").fetchdf()
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| Type mismatch on UNION | schema drift across files | `union_by_name` / cast |
| Slow scan | reading all columns | select subset; predicate early |
| OOM | huge hash join | filter; spill settings; sample |
| Lock error | second writer on same file DB | one writer; use read_only |

## Best practices

- Keep a `.duckdb` file for curated views; keep raw lake files immutable.
- Use `EXPLAIN ANALYZE` for unexpected runtime.
- `PRAGMA threads=N` and `PRAGMA memory_limit='4GB'` in shared envs.
- Hand off to `@pandas` / `@polars` only for the final slim result.

## Limitations

- Single-node; not a substitute for Snowflake/BigQuery at fleet scale.
- Extension availability differs offline vs CI images.
- Concurrent multi-writer patterns are limited compared to server DBs.

## Related skills

- `@polars` - expression DataFrames on the same files
- `@spark` - distributed SQL when DuckDB no longer fits
- `@dbt` - versioned SQL models wrapping DuckDB or warehouses
