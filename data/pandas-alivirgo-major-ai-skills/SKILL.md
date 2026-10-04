---
name: pandas
description: "Load, clean, join, and aggregate tabular data with pandas while managing data types and memory use."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["pandas", "dataframe", "etl", "python", "analytics", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# pandas DataFrame AI Skill Guide

## Overview & Engine Architecture

pandas is the default Python tabular toolkit: Series and DataFrame over NumPy (and Arrow-backed dtypes in newer builds). IO loaders materialize tables; vectorized ops and `groupby`/`merge` reshape them. Agents prefer explicit dtypes, avoid row-wise `apply` on large frames, and profile memory before chaining copies.

```
CSV/Parquet/SQL
      -> DataFrame (columns = Series)
          -> filter / assign / groupby / merge
          -> to_parquet / to_sql / plot
```

## When to use this skill

- Cleaning and joining tabular files
- Feature tables for ML (`@scikit-learn`, `@pytorch`)
- Quick exploratory aggregates before moving to Polars/DuckDB/Spark

## Operational directives

1. Set dtypes at read time (`dtype=`, `parse_dates=`) instead of fixing later.
2. Prefer boolean masks and vectorized ops over Python loops / `apply`.
3. Use `merge` with explicit `how` and validate key uniqueness when required.
4. Chain with `.copy()` only when you must break SettingWithCopy hazards.
5. For multi-GB data, switch to `@polars`, `@duckdb`, or chunked reads.

## Read + aggregate example

```python
import pandas as pd

df = pd.read_csv(
    "orders.csv",
    usecols=["order_id", "customer_id", "amount", "created_at"],
    parse_dates=["created_at"],
    dtype={"order_id": "string", "customer_id": "string"},
)

monthly = (
    df.assign(month=df["created_at"].dt.to_period("M").astype(str))
    .groupby(["customer_id", "month"], as_index=False)
    .agg(revenue=("amount", "sum"), orders=("order_id", "nunique"))
)
```

## Merge hygiene

```python
out = orders.merge(
    customers[["customer_id", "segment"]],
    on="customer_id",
    how="left",
    validate="m:1",
)
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| SettingWithCopyWarning | chained indexing | `.loc[]` assign or `.copy()` |
| object dtype bloat | mixed/unparsed columns | `astype` / `convert_dtypes` |
| merge row explosion | many-to-many keys | validate; dedupe keys |
| slow groupby | Python `apply` | built-in aggregations |

## Best practices

- Prefer Parquet over CSV for repeated pipelines.
- `df.memory_usage(deep=True)` before widening joins.
- Categoricals for low-cardinality string columns used as keys/filters.
- Keep idempotent transforms; avoid mutating global frames in notebooks without copies.

## Limitations

- Single-machine memory bound; not a Spark replacement.
- Time-zone and nullable dtypes differ across pandas majors - pin versions in prod.
- Arrow string dtype behavior depends on pandas/pyarrow versions.

## Related skills

- `@polars` - faster single-node DataFrames
- `@duckdb` - SQL over files without full materialization
- `@jupyter` - exploratory notebooks
