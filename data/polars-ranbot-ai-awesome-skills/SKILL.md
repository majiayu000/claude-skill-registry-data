---
name: polars
description: Fast in-memory DataFrame library for datasets that fit in RAM. Use when pandas is too slow but data still fits in memory. Lazy evaluation, parallel execution, Apache Arrow backend. Best for 1-100GB da
category: Document Processing
source: antigravity
tags: [python, api, ai, workflow, document, azure, rag, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/polars
---


# Polars

## When to Use
- You need a faster in-memory DataFrame workflow than pandas for data that still fits in RAM.
- You are building ETL, analytics, or transformation pipelines that benefit from lazy evaluation and parallel execution.
- You want expression-based tabular operations on top of Apache Arrow semantics.

## Overview

Polars is a lightning-fast DataFrame library for Python and Rust built on Apache Arrow. Work with Polars' expression-based API, lazy evaluation framework, and high-performance data manipulation capabilities for efficient data processing, pandas migration, and data pipeline optimization.

## Quick Start

### Installation and Basic Usage

Install Polars:
```python
uv pip install polars
```

Basic DataFrame creation and operations:
```python
import polars as pl

# Create DataFrame
df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NY", "LA", "SF"]
})

# Select columns
df.select("name", "age")

# Filter rows
df.filter(pl.col("age") > 25)

# Add computed columns
df.with_columns(
    age_plus_10=pl.col("age") + 10
)
```

## Core Concepts

### Expressions

Expressions are the fundamental building blocks of Polars operations. They describe transformations on data and can be composed, reused, and optimized.

**Key principles:**
- Use `pl.col("column_name")` to reference columns
- Chain methods to build complex transformations
- Expressions are lazy and only execute within contexts (select, with_columns, filter, group_by)

**Example:**
```python
# Expression-based computation
df.select(
    pl.col("name"),
    (pl.col("age") * 12).alias("age_in_months")
)
```

### Lazy vs Eager Evaluation

**Eager (DataFrame):** Operations execute immediately
```python
df = pl.read_csv("file.csv")  # Reads immediately
result = df.filter(pl.col("age") > 25)  # Executes immediately
```

**Lazy (LazyFrame):** Operations build a query plan, optimized before execution
```python
lf = pl.scan_csv("file.csv")  # Doesn't read yet
result = lf.filter(pl.col("age") > 25).select("name", "age")
df = result.collect()  # Now executes optimized query
```

**When to use lazy:**
- Working with large datasets
- Complex query pipelines
- When only some columns/rows are needed
- Performance is critical

**Benefits of lazy evaluation:**
- Automatic query optimization
- Predicate pushdown
- Projection pushdown
- Parallel execution

For detailed concepts, load `references/core_concepts.md`.

## Common Operations

### Select
Select and manipulate columns:
```python
# Select specific columns
df.select("name", "age")

# Select with expressions
df.select(
    pl.col("name"),
    (pl.col("age") * 2).alias("double_age")
)

# Select all columns matching a pattern
df.select(pl.col("^.*_id$"))
```

### Filter
Filter rows by conditions:
```python
# Single condition
df.filter(pl.col("age") > 25)

# Multiple conditions (cleaner than using &)
df.filter(
    pl.col("age") > 25,
    pl.col("city") == "NY"
)

# Complex conditions
df.filter(
    (pl.col("age") > 25) | (pl.col("city") == "LA")
)
```

### With Columns
Add or modify columns while preserving existing ones:
```python
# Add new columns
df.with_columns(
    age_plus_10=pl.col("age") + 10,
    name_upper=pl.col("name").str.to_uppercase()
)

# Parallel computation (all columns computed in parallel)
df.with_columns(
    pl.col("value") * 10,
    pl.col("value") * 100,
)
```

### Group By and Aggregations
Group data and compute aggregations:
```python
# Basic grouping
df.group_by("city").agg(
    pl.col("age").mean().alias("avg_age"),
    pl.len().alias("count")
)

# Multiple group keys
df.group_by("city", "department").agg(
    pl.col("salary").sum()
)

# Conditional aggregations
df.group_by("city").agg(
    (pl.col("age") > 30).sum().alias("over_30")
)
```

For detailed operation patterns, load `references/operations.md`.

## Aggregations and Window Functions

### Aggregation Functions
Common aggregations within `group_by` context:
- `pl.len()` - count rows
- `pl.col("x").sum()` - sum values
- `pl.col("x").mean()` - average
- `pl.col("x").min()` / `pl.col("x").max()` - extremes
- `pl.first()` / `pl.last()` - first/last values

### Window Functions with `over()`
Apply aggregations while preserving row count:
```python
# Add group statistics to each row
df.with_columns(
    avg_age_by_city=pl.col("age").mean().over("city"),
    rank_in_city=pl.col("salary").rank().over("city")
)

# Multiple grouping columns
df.with_columns(
    group_avg=pl.col("value").mean().over("category", "region")
)
```

**Mapping strategies:**
- `group_to_rows` (default): Preserves original row order
- `explode`: Faster but groups rows together
- `join`: Creates list columns

## Data I/O

### Supported Formats
Polars supports reading and writing:
- CSV, Parquet, JSON, Excel
- Databases (via connectors)
- Cloud storage (S3, Azure, GCS)
- Google BigQuery
- Multiple/partitioned files

### Common I/O Operations

**CSV:**
```python
# Eager
df = pl.read_csv("file.csv")
df.w
