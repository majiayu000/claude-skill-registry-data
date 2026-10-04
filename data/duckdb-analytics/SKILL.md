---
name: duckdb-analytics
description: 'Use when running analytical SQL over Parquet/CSV/JSON without a warehouse, replacing pandas for data wrangling, joining S3 data in-place, building local data marts, or embedding OLAP into an app. Triggers: read_parquet/read_csv setup, partitioned dataset queries, hive partitioning, glob patterns for S3, COPY TO export, attach Postgres/MySQL, UDFs in Python/R, MotherDuck cloud sync, columnar performance vs row stores. NOT for OLTP workloads (concurrent writes), distributed analytics at petabyte scale (use Spark/Trino), or vector search (use pgvector/Lance).'
category: Data & Analytics
tags:
  - duckdb
  - analytics
  - parquet
  - olap
  - sql
  - data-engineering
---

# DuckDB Analytics

DuckDB is an embedded analytical database — SQLite for OLAP. It reads Parquet/CSV directly, runs columnar vectorized SQL, and ships as a single binary. For most "I'd reach for pandas" or "I'd spin up a warehouse for this" tasks, DuckDB is faster and simpler.

## When to use

- Querying Parquet/CSV/JSON without loading into a database first.
- A pandas pipeline that's slow or won't fit in memory.
- Local data marts for dashboards (read-heavy, single-writer).
- Joining S3 data in place without ETL.
- Embedding analytical SQL into an app (CLI tool, Jupyter, Electron).

## Core capabilities

### Read Parquet directly

```sql
-- Single file
SELECT * FROM read_parquet('/data/events.parquet') LIMIT 10;

-- Glob over many files (single dataset)
SELECT count(*) FROM read_parquet('/data/events/*.parquet');

-- Hive-partitioned dataset
SELECT region, count(*) AS n
FROM read_parquet('/data/events/year=2026/month=*/day=*/*.parquet',
                  hive_partitioning = true)
GROUP BY region;
```

DuckDB pushes predicates and column projections into the Parquet reader — only the columns and row groups you need are read off disk.

### Read S3

```sql
INSTALL httpfs;
LOAD httpfs;

SET s3_region='us-west-2';
SET s3_access_key_id='...';
SET s3_secret_access_key='...';
-- Or for IAM roles in EC2/ECS, AWS_PROFILE works.

SELECT * FROM read_parquet('s3://my-bucket/events/*.parquet') LIMIT 10;
```

For Cloudflare R2, use the S3-compatible endpoint: `SET s3_endpoint='<account>.r2.cloudflarestorage.com';`.

### CSV with type inference

```sql
SELECT * FROM read_csv_auto('/data/exports/*.csv', sample_size = 100000);

-- Or explicit
CREATE TABLE orders AS
SELECT * FROM read_csv('/data/orders.csv',
  header = true,
  delim = ',',
  columns = {'id': 'BIGINT', 'created_at': 'TIMESTAMP', 'total': 'DECIMAL(10,2)'}
);
```

`read_csv_auto` is great for exploration; lock down types in `read_csv` for production pipelines.

### JSON

```sql
SELECT * FROM read_json_auto('/data/events.ndjson') LIMIT 10;

-- Specific path inside nested JSON
SELECT json_extract(payload, '$.user.id') AS user_id, count(*)
FROM read_json_auto('/data/events.ndjson')
GROUP BY 1;
```

### Attach Postgres/MySQL/SQLite

```sql
INSTALL postgres;
LOAD postgres;
ATTACH 'host=db.example.com user=ro password=... dbname=app' AS pg (TYPE postgres);

-- Now query Postgres tables alongside Parquet.
SELECT u.name, count(*) AS events
FROM read_parquet('s3://events/*.parquet') e
JOIN pg.public.users u ON u.id = e.user_id
GROUP BY u.name;
```

This is a common pattern: production data in Postgres, log/event data in S3 Parquet, joins for analytics.

### Export

```sql
COPY (SELECT * FROM big_query)
TO '/data/output/result.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);

-- Partitioned
COPY (SELECT *, date_trunc('day', ts) AS day FROM events)
TO '/data/events_partitioned'
(FORMAT PARQUET, PARTITION_BY (day), OVERWRITE_OR_IGNORE);
```

ZSTD is the right default — better compression than snappy, similar speed.

### Python integration

```python
import duckdb
import pandas as pd

# Inline DataFrame querying — DuckDB sees pandas DataFrames as tables.
df = pd.read_csv('orders.csv')
result = duckdb.sql("SELECT region, SUM(total) FROM df GROUP BY region").df()

# Persistent file-backed database.
con = duckdb.connect('/data/marts/sales.duckdb')
con.sql("CREATE TABLE IF NOT EXISTS daily AS SELECT date_trunc('day', ts) AS day, count(*) AS n FROM read_parquet('s3://e/*') GROUP BY 1")
```

DuckDB+pandas is the common "throw out the warehouse" combo for analyst notebooks.

### Aggregations and window functions

```sql
-- Top-3 products per region by revenue
SELECT * FROM (
  SELECT
    region, product, SUM(total) AS revenue,
    ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(total) DESC) AS rn
  FROM orders
  GROUP BY region, product
) WHERE rn <= 3;

-- 7-day moving average
SELECT
  day,
  AVG(orders) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma7
FROM daily_orders
ORDER BY day;
```

Full window-function support; same SQL works in Postgres.

### Performance — vectorized columnar

DuckDB processes data in vectors of ~1024 values at a time, columnar layout. Aggregations and projections are dramatically faster than row-store pandas equivalents on wide tables.

For a 100M-row aggregation that takes pandas 30s, DuckDB often does it in 2-5s with no special tuning.

### MotherDuck (cloud sync)

```sql
-- Hybrid local + cloud DuckDB
ATTACH 'md:my_database' AS md (TYPE motherduck);
SELECT * FROM md.events LIMIT 100;
```

MotherDuck is hosted DuckDB with cloud storage. Useful for sharing a dataset with collaborators without exporting.

## Anti-patterns

### Using DuckDB for OLTP

**Symptom:** Concurrent writes corrupt or hang.
**Diagnosis:** DuckDB is single-writer. It locks the database file for write transactions.
**Fix:** OLTP belongs in Postgres/MySQL/SQLite-WAL. DuckDB is for analytics.

### `read_csv_auto` in production

**Symptom:** Pipeline silently mistypes a column when input shape changes.
**Diagnosis:** Auto-detection is convenient but unstable across data shifts.
**Fix:** Lock types with `read_csv(..., columns = {...})` in production. Auto for exploration.

### Reading the entire file when you need one column

**Symptom:** Job slow despite Parquet being columnar.
**Diagnosis:** `SELECT *` reads all columns; predicate pushdown can't skip the columns you don't use.
**Fix:** Project only what you need: `SELECT user_id, count(*) FROM read_parquet('...')`.

### Loading 100M rows into pandas first

**Symptom:** OOM or 30+ minute runtimes.
**Diagnosis:** Pulling everything into memory before filtering.
**Fix:** Push the filter into DuckDB: `duckdb.sql("SELECT * FROM read_parquet('...') WHERE …").df()` only materializes the result.

### Forgetting `LOAD httpfs` after `INSTALL`

**Symptom:** "IO Error: Could not access HTTP" on s3:// URL.
**Diagnosis:** `INSTALL` downloads the extension; `LOAD` activates it for this session.
**Fix:** Both, in order. Or use a persistent database: extensions persist across sessions.

### Mixing CSV and Parquet without explicit casts

**Symptom:** Aggregations give wrong answers; types coerce silently.
**Diagnosis:** CSV is all strings unless you tell it otherwise; Parquet types are fixed.
**Fix:** Explicit `CAST(col AS BIGINT)` where types differ across sources.

## Quality gates

- [ ] All production reads use explicit column types (not `_auto`).
- [ ] Parquet output uses ZSTD compression.
- [ ] Partition columns chosen by query patterns (date is common; high-cardinality columns are not).
- [ ] Glob patterns tested with the actual filesystem before scheduling.
- [ ] S3 access key not in version control; use IAM roles or env vars.
- [ ] `EXPLAIN` reviewed for any query >5s on representative data.
- [ ] DuckDB version pinned; aggregations tested on upgrade (rare semantic shifts).
- [ ] No long-running concurrent writers — single producer per database file.

## NOT for

- **OLTP** — concurrent transactional workload.
- **Distributed analytics at petabyte scale** — Spark, Trino, BigQuery, Snowflake.
- **Vector search** — pgvector, Lance, Chroma; DuckDB has VSS but it's early.
- **Streaming ingestion** — DuckDB is batch-friendly; streaming requires external pipelines.
- **Real-time multi-user dashboards** — write contention; use a managed warehouse.
