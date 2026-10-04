---
name: polars
description: "Build Polars expression and LazyFrame pipelines for CSV or Parquet analytics with selective and streaming scans."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["polars", "dataframe", "lazy", "parquet", "python", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Polars DataFrame AI Skill Guide

## Overview & Engine Architecture

Polars is a Rust-backed DataFrame library with eager `DataFrame` and deferred `LazyFrame` plans. Expressions (`pl.col`, `pl.when`) describe column work; the optimizer pushes projections and predicates into scans. Agents default to lazy + `collect()` (or streaming) for multi-file Parquet pipelines and keep joins/filters as expressions, not Python loops.

```
scan_parquet / scan_csv
      -> LazyFrame plan
          -> filter / select / group_by / join
          -> collect() or sink_parquet()
```

## When to use this skill

- Faster local ETL than pandas on medium/large files
- Columnar pipelines that stay on Parquet
- Expression-heavy transforms before export to DuckDB/Spark

## Operational directives

1. Prefer `scan_*` + LazyFrame over `read_*` when files are large.
2. Put filters early so predicate pushdown can skip row groups.
3. Select only needed columns before wide joins.
4. Use `collect(streaming=True)` / `sink_parquet` for bigger-than-RAM paths (API varies by version).
5. Avoid `.map_elements` unless no expression alternative exists.

## Lazy groupby example

```python
import polars as pl

q = (
    pl.scan_parquet("data/orders/*.parquet")
    .filter(pl.col("created_at") >= pl.datetime(2025, 1, 1))
    .group_by("customer_id")
    .agg(
        pl.col("amount").sum().alias("revenue"),
        pl.len().alias("n_orders"),
    )
    .sort("revenue", descending=True)
)

top = q.collect()
```

## Join with explicit coalesce

```python
result = (
    orders_lf.join(customers_lf, on="customer_id", how="left")
    .select("order_id", "customer_id", "segment", "amount")
    .collect()
)
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| Schema mismatch on concat | differing dtypes/names | `cast` / align schemas |
| Slow collect | materializing too early | keep lazy until end |
| OOM | wide joins + full collect | project columns; streaming sink |
| Wrong null join | null keys | filter or coalesce intentionally |

## Best practices

- Write Parquet with snappy/zstd; partition by date when scans are date-filtered.
- Use `explain(optimized=True)` when plans surprise you.
- Prefer `pl.Expr` over UDFs for SIMD-friendly execution.
- Pin Polars version in lockfiles - expression APIs move quickly.

## Limitations

- Not a distributed cluster engine (use `@spark` for that).
- Some pandas idioms (heavy index semantics) do not translate 1:1.
- Streaming support and collect flags differ across minor versions.

## Related skills

- `@pandas` - ecosystem compatibility and small-frame UX
- `@duckdb` - SQL analytics over the same files
- `@spark` - multi-node scale-out
