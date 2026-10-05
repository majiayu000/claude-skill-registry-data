---
name: duckdb-polars-boundaries
description: >-
  Use when Python analytical code crosses between DuckDB SQL/relations and
  Polars DataFrame/LazyFrame objects, especially for Arrow transfer, lazy versus
  eager execution, registration lifetime, schema conversion, result ownership,
  or deciding which engine owns a stage. Do not use for DuckDB-only SQL or
  Polars-only transformations.
argument-hint: "[source, stage ownership, transfer format, and consumer]"
---

# DuckDB and Polars execution boundary

Choose one engine to own each stage. DuckDB owns relational SQL, multi-source
joins, and file scans that SQL expresses clearly. Polars owns reusable typed
expression pipelines and dataframe-native transformations. Cross once at a
deliberate consumer boundary rather than alternating after every operation.

## Workflow

1. Inspect DuckDB and Polars versions, source size/format, desired output grain,
   schema, null/timestamp/nested types, ordering, and final consumer.
2. Decide whether files remain the shared boundary or whether an in-memory
   Arrow-compatible transfer is justified. Prefer Parquet for reusable or
   process-crossing artifacts.
3. Keep source objects alive while DuckDB replacement scans or registered views
   refer to them. Use explicit registration when lifetime or naming must be
   obvious; unregister when a long-lived connection would retain stale state.
4. Materialize exactly once when crossing to an eager consumer. Do not call
   `.collect()`, `.pl()`, `.arrow()`, or dataframe conversion repeatedly in a
   loop merely to continue the pipeline in the other engine.
5. Validate row count, grain, column names/order, dtypes, nulls, timestamps,
   nested values, dictionary/categorical semantics, and ordering after transfer.

## Decision rules

- If DuckDB SQL can scan the original files and produce the final relational
  result, keep the work there and convert only for the Polars consumer.
- If Polars transformation is the reusable product, scan/transform in Polars
  and expose Arrow/Parquet to DuckDB only for a SQL stage that adds value.
- Treat conversion as potentially copying or coercing unless current APIs and
  buffers prove otherwise. Zero-copy is an optimization claim, not a default.
- SQL result order is undefined without `ORDER BY`; dataframe transfer does not
  create a durable ordering guarantee.

```python
import duckdb
import polars as pl

source = pl.scan_parquet("events/*.parquet")
prepared = source.filter(pl.col("status") == "ok").collect()

with duckdb.connect() as connection:
    connection.register("prepared", prepared)
    result = connection.sql(
        "select customer_id, count(*) as n from prepared group by customer_id"
    ).pl()
```

Verify the installed conversion APIs and add a round-trip contract test. Read
[ownership and lifetime](references/ownership.md), [schema transfer](references/schema.md),
and [verification](references/verification.md).
