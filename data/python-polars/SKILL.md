---
name: python-polars
description: This skill should be used when the user asks to "work with polars", "create a dataframe", "use lazy evaluation", "migrate from pandas", "optimize data pipelines", "read parquet files", "group by operations", or needs guidance on Polars DataFrame operations, expression API, performance optimization, or data transformation workflows.
---

# Python Polars

Polars is a lightning-fast DataFrame library for Python built on Apache Arrow. It provides an expression-based API, lazy evaluation framework, and automatic parallelization for high-performance data processing.

## Quick start

### Installation

```python
uv pip install polars
```

### Basic operations

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

## Core concepts

### Expressions

Expressions are composable units describing data transformations. Use `pl.col("column_name")` to reference columns and chain methods for complex operations:

```python
df.select(
    pl.col("name"),
    (pl.col("age") * 12).alias("age_in_months")
)
```

Expressions execute within contexts: `select()`, `with_columns()`, `filter()`, `group_by().agg()`.

### Lazy vs eager evaluation

**Eager (DataFrame)**: Operations execute immediately.

```python
df = pl.read_csv("file.csv")  # Reads immediately
result = df.filter(pl.col("age") > 25)
```

**Lazy (LazyFrame)**: Operations build an optimized query plan.

```python
lf = pl.scan_csv("file.csv")  # Doesn't read yet
result = lf.filter(pl.col("age") > 25).select("name", "age")
df = result.collect()  # Executes optimized query
```

Use lazy mode for large datasets, complex pipelines, and when performance is critical. Benefits include automatic query optimization, predicate pushdown, projection pushdown, and parallel execution.

For detailed concepts including data types, type casting, null handling, and parallelization, see `references/core-concepts.md`.

## Common operations

### Select and with_columns

```python
# Select specific columns
df.select("name", "age")

# Select with expressions
df.select(
    pl.col("name"),
    (pl.col("age") * 2).alias("double_age")
)

# Add new columns (preserves existing)
df.with_columns(
    age_doubled=pl.col("age") * 2,
    name_upper=pl.col("name").str.to_uppercase()
)
```

### Filter

```python
# Single condition
df.filter(pl.col("age") > 25)

# Multiple conditions (AND)
df.filter(
    pl.col("age") > 25,
    pl.col("city") == "NY"
)

# OR conditions
df.filter(
    (pl.col("age") > 25) | (pl.col("city") == "LA")
)
```

### Group by and aggregations

```python
df.group_by("city").agg(
    pl.col("age").mean().alias("avg_age"),
    pl.len().alias("count")
)
```

### Window functions

Apply aggregations while preserving row count:

```python
df.with_columns(
    avg_age_by_city=pl.col("age").mean().over("city"),
    rank_in_city=pl.col("salary").rank().over("city")
)
```

For comprehensive operations including sorting, conditionals, string/date operations, and list handling, see `references/operations.md`.

## Data I/O

### CSV

```python
# Eager
df = pl.read_csv("file.csv")
df.write_csv("output.csv")

# Lazy (preferred for large files)
lf = pl.scan_csv("file.csv")
result = lf.filter(...).select(...).collect()
```

### Parquet (recommended for performance)

```python
df = pl.read_parquet("file.parquet")
df.write_parquet("output.parquet")

# Lazy with predicate pushdown
lf = pl.scan_parquet("file.parquet")
```

For comprehensive I/O including JSON, Excel, databases, cloud storage, and streaming, see `references/io-guide.md`.

## Transformations

### Joins

```python
# Inner join
df1.join(df2, on="id", how="inner")

# Left join
df1.join(df2, on="id", how="left")

# Different column names
df1.join(df2, left_on="user_id", right_on="id")
```

### Concatenation

```python
# Vertical (stack rows)
pl.concat([df1, df2], how="vertical")

# Horizontal (add columns)
pl.concat([df1, df2], how="horizontal")
```

### Pivot and unpivot

```python
# Pivot (wide format)
df.pivot(values="sales", index="date", columns="product")

# Unpivot (long format)
df.unpivot(index="id", on=["col1", "col2"])
```

For detailed transformation patterns including asof joins, exploding, and transposing, see `references/transformations.md`.

## Best practices

### Performance optimization

1. **Use lazy evaluation for large datasets**:

   ```python
   lf = pl.scan_csv("large.csv")  # Not read_csv
   result = lf.filter(...).select(...).collect()
   ```

2. **Avoid Python functions in hot paths** - stay within the expression API for parallelization:

   ```python
   # Good: Native expression (parallelized)
   df.with_columns(result=pl.col("value") * 2)

   # Avoid: Python function (sequential)
   df.with_columns(result=pl.col("value").map_elements(lambda x: x * 2))
   ```

3. **Select only needed columns early**:

   ```python
   lf.select("col1", "col2").filter(...)  # Good
   lf.filter(...).select("col1", "col2")  # Less optimal
   ```

4. **Use streaming for very large data**:

   ```python
   lf.collect(streaming=True)
   ```

5. **Use appropriate data types** - Categorical for low-cardinality strings, appropriate integer sizes.

### Conditional operations

```python
pl.when(condition).then(value).otherwise(other_value)
```

### Null handling

```python
pl.col("x").fill_null(0)
pl.col("x").is_null()
pl.col("x").drop_nulls()
```

For comprehensive best practices including anti-patterns, memory management, testing, and code organization, see `references/best-practices.md`.

## Pandas migration

Polars offers significant performance improvements over pandas with a cleaner API. Key differences:

- **No index**: Polars uses integer positions only
- **Strict typing**: No silent type conversions
- **Lazy evaluation**: Available via LazyFrame
- **Parallel by default**: Operations parallelized automatically

### Common operation mappings

| Operation | pandas | Polars |
|-----------|--------|--------|
| Select | `df["col"]` | `df.select("col")` |
| Filter | `df[df["col"] > 10]` | `df.filter(pl.col("col") > 10)` |
| Add column | `df.assign(x=...)` | `df.with_columns(x=...)` |
| Group by | `df.groupby("col").agg(...)` | `df.group_by("col").agg(...)` |
| Window | `df.groupby("col").transform(...)` | `df.with_columns(...).over("col")` |

For comprehensive migration guide including operation mappings, migration patterns, and anti-patterns to avoid, see `references/pandas-migration.md`.

## References

This skill includes comprehensive reference documentation:

- `references/core-concepts.md` - Expressions, data types, lazy evaluation, parallelization
- `references/operations.md` - Selection, filtering, grouping, window functions, string/date operations
- `references/best-practices.md` - Performance optimization, anti-patterns, memory management
- `references/io-guide.md` - CSV, Parquet, JSON, Excel, databases, cloud storage
- `references/transformations.md` - Joins, concatenation, pivots, reshaping operations
- `references/pandas-migration.md` - Migration guide from pandas to Polars

Load these references as needed for detailed information on specific topics.
