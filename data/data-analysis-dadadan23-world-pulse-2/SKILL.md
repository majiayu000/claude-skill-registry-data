---
name: "data-analysis"
description: 'Analyze structured data across CSV, JSON, SQL, and DataFrame workflows with exploration, transformation, and visualization. Use when exploring datasets with pandas/polars, running SQL queries on files with DuckDB, transforming data pipelines, or generating data visualizations.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 languages: ["python", "sql", "typescript"]
 frameworks: ["pandas", "polars", "duckdb"]
 platforms: ["windows", "linux", "macos"]
---

# Data Analysis

> Patterns for exploring, transforming, validating, and visualizing structured data.

## Prerequisites

- Python 3.9+ with pandas, polars, or DuckDB installed

## When to Use

- Exploring CSV, JSON, Parquet, or database data
- Building data transformation pipelines
- Validating data quality and schema compliance
- Creating data visualizations and reports
- Writing ETL/ELT scripts

## Decision Tree

```
Working with data?
+- Quick exploration / ad-hoc?
| +- Small file (< 1GB)? -> Pandas / Polars
| +- SQL-like queries? -> DuckDB (in-process)
| - Interactive? -> Jupyter Notebook
+- Production pipeline?
| +- Simple transforms? -> Python script + scheduling
| +- Large scale? -> Spark / Databricks
| - Streaming? -> Kafka + Flink
+- Data validation?
| +- Schema checking? -> Pydantic / Great Expectations
| - Quality rules? -> dbt tests / custom validators
- Visualization?
 +- Static charts? -> Matplotlib / Seaborn
 +- Interactive? -> Plotly / Altair
 - Dashboard? -> Streamlit / Dash
```

## Quick Start: Pandas

```python
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Explore
print(df.shape) # (rows, cols)
print(df.dtypes) # Column types
print(df.describe()) # Summary statistics
print(df.isnull().sum()) # Missing values per column

# Transform
df["date"] = pd.to_datetime(df["date"])
df = df.dropna(subset=["required_field"])
df["category"] = df["category"].str.lower().str.strip()

# Aggregate
summary = df.groupby("category").agg(
 count=("id", "count"),
 avg_value=("value", "mean"),
 total=("value", "sum")
).reset_index()

# Export
summary.to_csv("output.csv", index=False)
```

## Quick Start: DuckDB (SQL on Files)

```python
import duckdb

# Query CSV directly - no loading step
result = duckdb.sql("""
 SELECT category, COUNT(*) as count, AVG(value) as avg_value
 FROM 'data.csv'
 WHERE date >= '2024-01-01'
 GROUP BY category
 ORDER BY count DESC
""").df() # Returns pandas DataFrame

# Query Parquet files (partitioned)
result = duckdb.sql("""
 SELECT * FROM 'data/**/*.parquet'
 WHERE region = 'US'
 LIMIT 1000
""")
```

## Quick Start: Polars (Fast Alternative)

```python
import polars as pl

# Load and transform in one chain
result = (
 pl.read_csv("data.csv")
 .filter(pl.col("value") > 0)
 .with_columns(
 pl.col("date").str.to_datetime(),
 pl.col("category").str.to_lowercase()
 )
 .group_by("category")
 .agg(
 pl.col("value").mean().alias("avg_value"),
 pl.col("id").count().alias("count")
 )
 .sort("count", descending=True)
)
```

## Core Rules

### 1. Data Loading

- **Always check shape and dtypes first**: Before any transformation
- **Handle encoding**: `pd.read_csv("file.csv", encoding="utf-8-sig")` for BOM files
- **Parse dates on load**: `parse_dates=["date_col"]` - don't post-process
- **Use chunked reading for large files**: `pd.read_csv("big.csv", chunksize=10000)`
- **Prefer Parquet for intermediate storage**: Column-oriented, compressed, typed

### 2. Data Quality

```python
# Essential quality checks
def validate_dataframe(df: pd.DataFrame) -> list[str]:
 issues = []
 
 # Null checks
 null_cols = df.columns[df.isnull().any()].tolist()
 if null_cols:
 issues.append(f"Null values in: {null_cols}")
 
 # Duplicate checks
 dup_count = df.duplicated().sum()
 if dup_count > 0:
 issues.append(f"{dup_count} duplicate rows")
 
 # Type checks
 for col in df.select_dtypes(include=["object"]):
 if df[col].str.match(r"^\d+$").all():
 issues.append(f"Column '{col}' looks numeric but is string")
 
 return issues
```

### 3. Performance

| Scenario | Recommendation |
|----------|---------------|
| < 100MB CSV | Pandas (sufficient) |
| 100MB - 10GB | Polars or DuckDB |
| > 10GB | DuckDB, Spark, or chunk processing |
| SQL-like queries | DuckDB (fastest for analytics) |
| Complex transforms | Polars (parallel, lazy evaluation) |

### 4. Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Always set figure size and style
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")

# Bar chart with annotation
ax = sns.barplot(data=summary, x="category", y="count")
ax.set_title("Items by Category", fontsize=14)
ax.set_xlabel("Category")
ax.set_ylabel("Count")

# Add value labels
for p in ax.patches:
 ax.annotate(f"{p.get_height():.0f}",
 (p.get_x() + p.get_width() / 2., p.get_height()),
 ha="center", va="bottom")

plt.tight_layout()
plt.savefig("chart.png", dpi=150)
```

### 5. Notebook Best Practices

- **One purpose per notebook**: Exploration, transformation, or reporting - not all three
- **Run cells top-to-bottom**: Notebooks must be reproducible in order
- **No hardcoded paths**: Use `pathlib.Path` or environment variables
- **Clear outputs before committing**: `jupyter nbconvert --clear-output`
- **Add markdown headers**: Document what each section does

## Anti-Patterns

- **Modifying data in-place without copy**: Unexpected side effects -> use `.copy()`
- **Chained indexing**: `df[df.a > 1]['b'] = 5` -> use `.loc[]` instead
- **Iterating rows with for loops**: Slow -> use vectorized operations or `.apply()`
- **Loading entire dataset when you need 5 columns**: Use `usecols=` parameter
- **No data validation**: Trusting input data blindly -> always validate schema + nulls
- **String concatenation for SQL**: SQL injection risk -> use parameterized queries

## Troubleshooting

| Issue | Solution |
|-------|----------|
| pandas MemoryError on large files | Use dtype optimization, chunksize parameter, or switch to polars/DuckDB |
| DuckDB file lock error | Close other connections, use read_only=True for concurrent reads |