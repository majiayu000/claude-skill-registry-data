---
name: notebook-creator
description: Create Jupyter notebooks for FF Analytics following project conventions. Use this skill when the user requests analysis notebooks for player evaluation, roster health, trade scenarios, market trends, or projection quality analysis. Guides through notebook structure, DuckDB connections, mart queries, visualization standards, and freshness banner patterns.
---

# Notebook Creator

Create analysis Jupyter notebooks for the Fantasy Football Analytics project following established conventions for data access, visualization, and documentation.

## When to Use This Skill

Use this skill proactively when:

- User requests "create a notebook for {analysis type}"
- User wants to analyze data using Jupyter
- User mentions player analysis, roster evaluation, or market trends
- User needs to explore marts, validate projections, or evaluate trades
- Creating deliverables for strategic planning (referenced from strategic-planner skill)

## Notebook Types

The FF Analytics project uses notebooks for several common analysis patterns:

1. **Player Analysis** - Deep dive on individual player performance, projections vs actuals
2. **Roster Health** - Team composition analysis, position depth, age curves
3. **Waiver/FA Analysis** - Available player evaluation using FASA marts (from Sprint 1)
4. **Trade Analysis** - Multi-asset trade scenario evaluation with KTC valuations
5. **Market Analysis** - Dynasty value trends over time from Keep Trade Cut data
6. **Projection Quality** - Model performance evaluation (projections vs actuals)

## Notebook Creation Workflow

### Step 1: Setup Notebook Structure

Use `assets/notebook_template.ipynb` as the starting point:

1. **Header cells**: Title, purpose, author, date, objectives
2. **Setup cell**: Imports (duckdb, pandas/polars, matplotlib, seaborn)
3. **Connection cell**: DuckDB database connection with EXTERNAL_ROOT
4. **Analysis cells**: Data loading, transformation, visualization
5. **Conclusion cell**: Findings and recommendations

**Naming convention**: `{topic}_{action}.ipynb`

- `roster_health_analysis.ipynb`
- `trade_scenario_evaluation.ipynb`
- `market_trends_ktc.ipynb`

### Step 2: Connect to Data

**DuckDB Connection Pattern:**

```python
import os
from pathlib import Path
import duckdb

# Set EXTERNAL_ROOT for parquet file access
external_root = os.environ.get("EXTERNAL_ROOT", str(Path.cwd().parent / "data" / "raw"))

# Connect to dbt database
db_path = Path.cwd().parent / "dbt" / "ff_data_transform" / "target" / "dev.duckdb"

if db_path.exists():
    conn = duckdb.connect(str(db_path), read_only=True)
    print(f"Connected to: {db_path}")
else:
    conn = duckdb.connect()  # In-memory fallback
    print("Using in-memory database")
```

**For Google Colab** (cloud data access):

```python
# Cloud GCS access pattern
conn = duckdb.connect()
conn.execute("INSTALL httpfs")
conn.execute("LOAD httpfs")

# Query External Parquet directly
query = """
SELECT * FROM read_parquet('gs://ff-analytics/mart/*/data.parquet')
"""
```

### Step 3: Query Marts

**Common mart query patterns:**

**Fantasy Actuals (2x2 Model - Actuals + Fantasy Scoring):**

```sql
SELECT
    player_name,
    season,
    week,
    SUM(fantasy_points) as total_points,
    COUNT(DISTINCT week) as games_played
FROM main.mart_fantasy_actuals_weekly
WHERE season = 2024
  AND position = 'RB'
GROUP BY player_name, season, week
ORDER BY total_points DESC
```

**Real-World Actuals:**

```sql
SELECT *
FROM main.mart_real_world_actuals_weekly
WHERE season = 2024
  AND stat_name IN ('rushing_yards', 'rushing_tds')
```

**FASA Targets (Free Agent / Still Available):**

```sql
SELECT
    player_name,
    position,
    age,
    ktc_value,
    fasa_status
FROM main.mart_fasa_targets
WHERE fasa_status = 'available'
  AND position IN ('RB', 'WR', 'TE')
ORDER BY ktc_value DESC
```

**Trade Values:**

```sql
SELECT *
FROM main.vw_trade_value_default  -- 1QB default view
WHERE player_name IN ('Player A', 'Player B')
```

### Step 4: Apply Visualization Standards

**Seaborn Theme:**

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Set consistent theme
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10
```

**Common Visualizations:**

**Time Series (Player Performance):**

```python
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df, x='week', y='fantasy_points', hue='player_name', marker='o')
plt.title("Fantasy Points by Week")
plt.xlabel("Week")
plt.ylabel("Fantasy Points")
plt.legend(title="Player")
plt.tight_layout()
plt.show()
```

**Distribution (Position Analysis):**

```python
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x='position', y='fantasy_points')
plt.title("Fantasy Points Distribution by Position")
plt.xlabel("Position")
plt.ylabel("Fantasy Points")
plt.tight_layout()
plt.show()
```

**Market Trends (KTC Values Over Time):**

```python
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df, x='snapshot_date', y='ktc_value', hue='player_name')
plt.title("Dynasty Value Trends (Keep Trade Cut)")
plt.xlabel("Date")
plt.ylabel("KTC Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Step 5: Add Freshness Banner

Notebooks should display data freshness.

```python
# Query freshness from ops metadata
freshness_query = """
SELECT
    dataset_name,
    MAX(snapshot_date) as latest_date,
    DATEDIFF('day', MAX(snapshot_date), CURRENT_DATE) as days_old
FROM main.ops_data_freshness
WHERE dataset_name IN ('nflverse_weekly', 'ktc_assets', 'commissioner_roster')
GROUP BY dataset_name
"""

freshness_df = conn.execute(freshness_query).fetchdf()
print("=== DATA FRESHNESS ===")
print(freshness_df)
print("======================")
```

**Banner Pattern (Markdown Cell):**

```markdown
---
**📊 Data Freshness Check**

Last updated:
- NFLverse Stats: 2024-11-08 (0 days old)
- KTC Valuations: 2024-11-07 (1 day old)
- Commissioner Rosters: 2024-11-06 (2 days old)

✅ All data sources within acceptable freshness thresholds
---
```

## Best Practices

### Cell Organization

1. **Imports and Config** - Single cell at top
2. **Database Connection** - Separate cell (can be re-run if connection drops)
3. **Helper Functions** - Define reusable functions early
4. **Data Loading** - One cell per major query (with print statement for row count)
5. **Data Exploration** - Multiple cells for .head(), .info(), .describe()
6. **Analysis** - Logical sections with markdown headers
7. **Visualizations** - One visualization per cell (easier to debug)
8. **Conclusions** - Final markdown cell with findings

### Documentation

- **Markdown headers** (`##`) to separate major sections
- **Inline comments** for complex transformations
- **Docstrings** for helper functions
- **Cell outputs** - Keep representative outputs (don't clear all cells before commit)
- **Conclusions** - Always include "what did we learn?" section

### Data Access

- **Read-only connections** - Use `read_only=True` for dbt database
- **EXTERNAL_ROOT** - Always respect environment variable for raw data paths
- **Limit during development** - Use `LIMIT 1000` for initial queries, remove for final analysis
- **Freshness checks** - Query `ops_data_freshness` or check `_meta.json` files

### Export Patterns

**CSV Export:**

```python
output_dir = Path.cwd() / "output"
output_dir.mkdir(exist_ok=True)

df.to_csv(output_dir / "analysis_results.csv", index=False)
print(f"Exported to {output_dir / 'analysis_results.csv'}")
```

**HTML Report:**

```python
# For tables with styling
styled_df = df.style.highlight_max(axis=0, color='lightgreen')
styled_df.to_html(output_dir / "report.html")
```

## Integration with Other Skills

- **strategic-planner**: Notebooks are common deliverables in spec phases
- **dbt-model-builder**: Notebooks query marts created by dbt models
- **data-quality-test-generator**: Notebooks validate data quality alongside dbt tests

## Resources

### assets/

- `notebook_template.ipynb` - Base template with setup, connection, analysis structure

### references/

- `example_roster_health.ipynb` - Roster composition and depth analysis
- `example_market_trends.ipynb` - KTC valuation time series analysis
- `example_notebook.ipynb` - General reference example

## Common Patterns

### Loading Player Stats by Position

```python
query = """
SELECT
    p.player_name,
    p.position,
    f.season,
    f.week,
    f.fantasy_points
FROM main.mart_fantasy_actuals_weekly f
JOIN main.dim_player p ON f.player_id = p.player_id
WHERE p.position = 'RB'
  AND f.season = 2024
ORDER BY f.fantasy_points DESC
"""
df = conn.execute(query).fetchdf()
```

### Joining Projections vs Actuals

```python
query = """
SELECT
    a.player_name,
    a.week,
    a.actual_points,
    p.projected_points,
    (a.actual_points - p.projected_points) as delta
FROM main.mart_fantasy_actuals_weekly a
JOIN main.mart_fantasy_projections p
  ON a.player_id = p.player_id
  AND a.season = p.season
  AND a.week = p.week
WHERE a.season = 2024
"""
```

### Age Curve Analysis

```python
query = """
SELECT
    p.age,
    AVG(f.fantasy_points) as avg_points,
    COUNT(*) as sample_size
FROM main.mart_fantasy_actuals_weekly f
JOIN main.dim_player p ON f.player_id = p.player_id
WHERE p.position = 'RB'
GROUP BY p.age
HAVING COUNT(*) > 100  -- Sufficient sample size
ORDER BY p.age
"""
```
