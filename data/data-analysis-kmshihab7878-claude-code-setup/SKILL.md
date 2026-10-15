---
name: data-analysis
description: >
  AI-powered data analysis patterns. Natural language to SQL/pandas, visual data exploration,
  ETL pipeline design, database modeling, and automated insights generation. Use when
  analyzing datasets, building dashboards, designing databases, or processing CSV/Excel data.
---

# Data Analysis

AI-powered data analysis and exploration patterns.

## how to use

- `/data-analysis`
  Apply data analysis best practices to the current task.

- `/data-analysis <task>`
  Guide for: explore, clean, visualize, model, etl, dashboard.

## when to apply

Reference these guidelines when:
- exploring or analyzing datasets
- writing SQL queries or pandas code
- designing database schemas
- building ETL pipelines
- creating dashboards or reports
- processing CSV/Excel files
- generating automated insights from data

## natural language to code (PandasAI concepts)

### Query Pattern
```python
import pandas as pd

# Pattern: Structured approach to natural language data queries
def nl_to_pandas(df: pd.DataFrame, question: str) -> str:
    """Convert natural language question to pandas code."""
    # 1. Understand the schema
    schema = {
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "shape": df.shape,
        "sample": df.head(3).to_dict(),
    }

    # 2. Generate appropriate pandas/SQL code
    # 3. Execute and validate
    # 4. Format result for user
    ...

# Common pandas patterns for data exploration
def quick_explore(df: pd.DataFrame) -> dict:
    """Quick dataset exploration."""
    return {
        "shape": df.shape,
        "dtypes": df.dtypes.value_counts().to_dict(),
        "missing": df.isnull().sum()[df.isnull().sum() > 0].to_dict(),
        "numeric_summary": df.describe().to_dict(),
        "categorical_columns": df.select_dtypes(include="object").columns.tolist(),
        "unique_counts": {col: df[col].nunique() for col in df.select_dtypes(include="object").columns},
        "duplicates": int(df.duplicated().sum()),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1e6, 2),
    }
```

## data cleaning patterns

```python
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standard data cleaning pipeline."""
    df = df.copy()

    # 1. Remove duplicates
    df = df.drop_duplicates()

    # 2. Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # 3. Handle missing values
    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    # Fill numeric with median, categorical with mode
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    for col in categorical_cols:
        if df[col].isnull().any():
            mode = df[col].mode()
            df[col] = df[col].fillna(mode[0] if len(mode) > 0 else "unknown")

    # 4. Fix data types
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                pass

    return df

def detect_outliers(
    series: pd.Series,
    method: str = "iqr",
    threshold: float = 1.5,
) -> pd.Series:
    """Detect outliers using IQR or Z-score method."""
    if method == "iqr":
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        return (series < q1 - threshold * iqr) | (series > q3 + threshold * iqr)
    elif method == "zscore":
        z = (series - series.mean()) / series.std()
        return z.abs() > threshold
    raise ValueError(f"Unknown method: {method}")
```

## SQL query patterns

### Window Functions
```sql
-- Running totals
SELECT date, revenue,
    SUM(revenue) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) as cumulative_revenue
FROM sales;

-- Year-over-year growth
SELECT month, revenue,
    LAG(revenue, 12) OVER (ORDER BY month) as prev_year_revenue,
    (revenue - LAG(revenue, 12) OVER (ORDER BY month)) /
        NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0) * 100 as yoy_growth_pct
FROM monthly_revenue;

-- Percentile ranking
SELECT product, revenue,
    PERCENT_RANK() OVER (ORDER BY revenue) as revenue_percentile
FROM products;

-- Moving averages
SELECT date, value,
    AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as ma_7d
FROM metrics;
```

### Pivot / Unpivot
```sql
-- Pivot: rows to columns (PostgreSQL crosstab)
SELECT * FROM crosstab(
    'SELECT region, quarter, revenue FROM sales ORDER BY 1,2',
    'SELECT DISTINCT quarter FROM sales ORDER BY 1'
) AS ct(region text, q1 numeric, q2 numeric, q3 numeric, q4 numeric);

-- Unpivot: columns to rows
SELECT date, metric_name, metric_value
FROM metrics
CROSS JOIN LATERAL (
    VALUES ('cpu', cpu), ('memory', memory), ('disk', disk)
) AS t(metric_name, metric_value);
```

### Performance Optimization
```sql
-- Index strategy
CREATE INDEX idx_sales_date ON sales(date);
CREATE INDEX idx_sales_customer ON sales(customer_id) INCLUDE (amount);

-- EXPLAIN ANALYZE for query optimization
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- Partial indexes for common filters
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Materialized views for expensive queries
CREATE MATERIALIZED VIEW monthly_stats AS
SELECT date_trunc('month', created_at) as month, COUNT(*), SUM(amount)
FROM orders GROUP BY 1;
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_stats;
```

## visual data exploration (PyGWalker concepts)

### Interactive Exploration Pattern
```python
import pygwalker as pyg

# One-line interactive exploration
walker = pyg.walk(df)  # Opens interactive Tableau-like UI in notebook

# For specific visualizations
walker = pyg.walk(df, spec={
    "mark": "bar",
    "encoding": {
        "x": {"field": "category", "type": "nominal"},
        "y": {"field": "revenue", "type": "quantitative", "aggregate": "sum"},
    }
})
```

### Matplotlib/Seaborn Quick Patterns
```python
import matplotlib.pyplot as plt
import seaborn as sns

def create_dashboard(df: pd.DataFrame, target_col: str) -> None:
    """Quick 4-panel analysis dashboard."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Distribution
    sns.histplot(df[target_col], kde=True, ax=axes[0, 0])
    axes[0, 0].set_title(f"Distribution of {target_col}")

    # Correlation heatmap
    numeric_df = df.select_dtypes(include="number")
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=axes[0, 1])
    axes[0, 1].set_title("Correlation Matrix")

    # Box plot
    if df.select_dtypes(include="object").shape[1] > 0:
        cat_col = df.select_dtypes(include="object").columns[0]
        sns.boxplot(data=df, x=cat_col, y=target_col, ax=axes[1, 0])
        axes[1, 0].set_title(f"{target_col} by {cat_col}")
        axes[1, 0].tick_params(axis="x", rotation=45)

    # Time series (if date column exists)
    date_cols = df.select_dtypes(include="datetime").columns
    if len(date_cols) > 0:
        df.set_index(date_cols[0])[target_col].plot(ax=axes[1, 1])
        axes[1, 1].set_title(f"{target_col} Over Time")

    plt.tight_layout()
    plt.savefig("dashboard.png", dpi=150)
```

## ETL pipeline patterns (Airbyte concepts)

### ELT Architecture
```
Sources → Extract → Load (raw) → Transform (dbt) → Serve
   ↑                                                   ↓
   └──── Schedule (Airflow/Dagster/Hatchet) ◄──────────┘
```

### Pipeline Template
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PipelineConfig:
    source: str
    destination: str
    schedule: str  # cron expression
    incremental: bool = True
    watermark_column: str = "updated_at"

class ETLPipeline:
    """Standard ETL pipeline pattern."""
    async def extract(self, config: PipelineConfig, since: datetime | None = None) -> pd.DataFrame:
        """Extract data from source with optional incremental loading."""
        ...

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply business logic transformations."""
        df = clean_dataframe(df)
        # Add derived columns, aggregations, etc.
        return df

    async def load(self, df: pd.DataFrame, config: PipelineConfig) -> int:
        """Load data to destination. Returns row count."""
        ...

    async def run(self, config: PipelineConfig) -> dict:
        """Execute full ETL pipeline."""
        raw = await self.extract(config)
        transformed = self.transform(raw)
        rows = await self.load(transformed, config)
        return {"rows_processed": rows, "timestamp": datetime.now().isoformat()}
```

## database design (DrawDB concepts)

### Schema Design Checklist
- [ ] Primary keys on all tables (prefer UUID or BIGSERIAL)
- [ ] Foreign keys with appropriate ON DELETE behavior
- [ ] NOT NULL constraints where applicable
- [ ] Unique constraints for business keys
- [ ] Indexes on foreign keys and common query filters
- [ ] Timestamps: `created_at`, `updated_at` on all tables
- [ ] Soft delete (`deleted_at`) vs hard delete decision
- [ ] Enum types for fixed value sets

### Common Patterns
```sql
-- Audit timestamps
CREATE TABLE entities (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Auto-update updated_at
CREATE FUNCTION update_updated_at() RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER entities_updated_at BEFORE UPDATE ON entities
FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

## integration with the operator's environment

| Component | Integration |
|-----------|------------|
| `data-analyst` agent | Delegates statistical analysis tasks |
| `xlsx` skill | Spreadsheet I/O for tabular data |
| `database-patterns` skill | Schema design and migration patterns |
| `db-admin` agent | Database operations and tuning |
| `Docker` MCP | Deploy Metabase/Superset/Qdrant |
| `filesystem` MCP | Read/write data files |

## cross-references

- **xlsx** skill: Excel/CSV file operations
- **database-patterns** skill: Schema design, migrations, indexing
- **pdf** skill: Extract tables from PDFs
- **data-analyst** agent: Statistical analysis
- **db-admin** agent: Database administration
- **DATA_PLATFORM_GUIDE.md**: Tool comparison reference
