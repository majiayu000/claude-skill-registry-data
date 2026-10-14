---
name: polars
description: Use when working with dataframes, data wrangling, ETL pipelines, or replacing pandas with Polars; Use when the user asks about fast, memory-efficient tabular data processing in Python
risk: low
source: custom
date_added: '2026-06-11'
---
You are an expert in **Polars**, the blazing-fast DataFrame library for Python written in Rust, designed as a modern replacement for pandas.

## Use this skill when

- Loading, transforming, and analyzing tabular data with Polars
- Migrating code from pandas to Polars
- Building ETL or data pipelines
- Working with lazy evaluation and query optimization
- Reading/writing CSV, Parquet, JSON, Arrow, Excel files
- Performing aggregations, joins, pivots, and window functions

## Do not use this skill when

- The user explicitly requires pandas
- The task involves ML model training (use pandas/numpy there if needed)

## Instructions

1. Always prefer the lazy API (`pl.scan_*`, `.lazy()`, `.collect()`) for large datasets.
2. Use expression-based transforms rather than row-wise operations.
3. Avoid `.to_pandas()` unless absolutely required for interop.
4. Always type-annotate DataFrames where possible.

## Core API

### Creating DataFrames
```python
import polars as pl

df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [30, 25, 35],
    "score": [88.5, 92.1, 78.0],
})

# From list of dicts
df = pl.from_dicts([{"a": 1, "b": 2}, {"a": 3, "b": 4}])

# Schema-enforced
df = pl.DataFrame({"a": [1, 2, 3]}, schema={"a": pl.Int32})
```

### Reading & Writing Files
```python
# CSV
df = pl.read_csv("data.csv")
lf = pl.scan_csv("data.csv")           # lazy
df.write_csv("out.csv")

# Parquet (preferred for large data)
df = pl.read_parquet("data.parquet")
lf = pl.scan_parquet("data.parquet")   # lazy
df.write_parquet("out.parquet")

# JSON / NDJSON
df = pl.read_json("data.json")
df = pl.read_ndjson("data.ndjson")

# Excel
df = pl.read_excel("data.xlsx", sheet_name="Sheet1")
```

### Selecting & Filtering
```python
# Select columns
df.select(["name", "age"])
df.select(pl.col("age"), pl.col("score"))
df.select(pl.all().exclude("name"))

# Filter rows
df.filter(pl.col("age") > 28)
df.filter((pl.col("age") > 25) & (pl.col("score") >= 90))

# Slice
df.head(10)
df.tail(5)
df.slice(10, 20)   # offset, length
```

### Transformations
```python
# Add / rename / drop columns
df.with_columns(
    (pl.col("score") * 1.1).alias("adjusted_score"),
    pl.col("name").str.to_uppercase().alias("NAME"),
)
df.rename({"name": "full_name"})
df.drop(["score"])

# Type casting
df.with_columns(pl.col("age").cast(pl.Float64))

# String operations
df.with_columns(
    pl.col("name").str.contains("Ali").alias("is_ali"),
    pl.col("name").str.split(" ").alias("parts"),
    pl.col("name").str.replace("Charlie", "Chuck"),
)

# Date/time
df.with_columns(
    pl.col("date").str.to_date("%Y-%m-%d"),
    pl.col("dt").dt.year(),
    pl.col("dt").dt.strftime("%b %Y"),
)
```

### Aggregations & GroupBy
```python
df.group_by("department").agg(
    pl.col("salary").mean().alias("avg_salary"),
    pl.col("salary").max().alias("max_salary"),
    pl.len().alias("count"),
)

# Multiple group keys
df.group_by(["dept", "year"]).agg(pl.col("revenue").sum())

# Pivot
df.pivot(index="year", on="category", values="amount", aggregate_function="sum")
```

### Joins
```python
df1.join(df2, on="id", how="inner")      # inner
df1.join(df2, on="id", how="left")       # left
df1.join(df2, left_on="user_id", right_on="id", how="full")  # full outer
df1.join_asof(df2, on="timestamp", strategy="backward")     # asof/range join
```

### Lazy API (recommended for large data)
```python
result = (
    pl.scan_csv("large.csv")
    .filter(pl.col("value") > 100)
    .group_by("category")
    .agg(pl.col("value").sum())
    .sort("value", descending=True)
    .collect()  # execute the query plan
)

# Explain the query plan
lf.explain()
lf.explain(optimized=True)
```

### Window Functions
```python
df.with_columns(
    pl.col("score").rank().over("department").alias("rank_in_dept"),
    pl.col("value").sum().over("group").alias("group_total"),
    pl.col("ts").sort().over("user_id"),    # sort within group
)
```

### Expressions & Utilities
```python
# Conditional / when-then-otherwise
df.with_columns(
    pl.when(pl.col("score") >= 90)
      .then(pl.lit("A"))
      .when(pl.col("score") >= 80)
      .then(pl.lit("B"))
      .otherwise(pl.lit("C"))
      .alias("grade")
)

# Null handling
df.drop_nulls()
df.fill_null(0)
df.fill_null(strategy="forward")
df.with_columns(pl.col("x").fill_nan(None))

# Sorting
df.sort("age", descending=True)
df.sort(["dept", "salary"], descending=[False, True])
```

### Schema & Metadata
```python
df.schema          # dict of column -> dtype
df.dtypes          # list of dtypes
df.columns         # list of column names
df.shape           # (rows, cols)
df.describe()      # summary statistics
```

## pandas → Polars Migration Cheatsheet

| pandas | Polars |
|--------|--------|
| `df["col"]` | `df["col"]` or `df.get_column("col")` |
| `df[["a","b"]]` | `df.select(["a","b"])` |
| `df[df["x"]>1]` | `df.filter(pl.col("x")>1)` |
| `df.assign(c=...)` | `df.with_columns(...)` |
| `df.groupby().agg()` | `df.group_by().agg()` |
| `df.merge()` | `df.join()` |
| `df.apply(fn)` | use expressions; last resort: `df.map_rows(fn)` |
| `pd.read_csv()` | `pl.read_csv()` / `pl.scan_csv()` |
| `df.to_parquet()` | `df.write_parquet()` |

## Best Practices

- **Prefer lazy over eager** for anything beyond toy-sized data.
- **Use expressions** instead of Python-level loops or `.map_rows()`.
- **Avoid `.to_pandas()`** — interop cost is high; stay in Polars as long as possible.
- **Use Parquet** as your storage format: columnar, compressed, fast to scan.
- **Specify dtypes** explicitly when reading CSVs to avoid inference overhead.
- **Use `.sink_parquet()` / `.sink_csv()`** for streaming writes with the lazy API.
- **Partition large datasets** with `hive_partitioning=True` on Parquet reads/writes.

## Common Patterns

### Top-N per group
```python
df.sort("score", descending=True).group_by("dept").head(3)
```

### Unnesting structs / lists
```python
df.unnest("address")          # struct column → individual columns
df.explode("tags")            # list column → multiple rows
```

### Concatenation
```python
pl.concat([df1, df2])                         # vertical (same schema)
pl.concat([df1, df2], how="diagonal")        # vertical, fill missing with null
pl.concat([df1, df2], how="horizontal")      # side-by-side
```
