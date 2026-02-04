---
name: data-viz-insight
description: Interactive data exploration and visualization skill. Use when users ask to visualize data, analyze datasets, create charts, or explore data files (CSV, Excel, Parquet, JSON). This skill guides through data exploration, proposes visualization strategies based on data characteristics, creates interactive Plotly charts in marimo notebooks, and generates analytical conclusions.
---

# Data Viz Insight

This skill enables interactive data exploration, visualization planning, and automated chart generation in marimo notebooks.

## Prerequisites

Marimo server must be running with MCP support:
```bash
uv run marimo edit main.py --mcp --no-token
```

## Workflow

Follow this 5-step interactive process:

### Step 1: Data Input

If the user hasn't provided a data file path, ask for it:
- "Which data file would you like to visualize?"
- Accept: CSV, Excel (.xlsx), Parquet (.parquet), JSON files

Verify the file exists before proceeding.

### Step 2: Auto-Explore Data

**Option 1: Use the exploration script (recommended for comprehensive analysis)**
```bash
uv run python .claude/skills/data-viz-insight/scripts/explore_data.py data.csv
```

The script provides:
- Data shape and schema
- Summary statistics for numeric columns
- Value counts for categorical columns
- Missing data analysis
- Date ranges for temporal columns
- Sample rows
- Visualization recommendations

**Option 2: Use Polars directly for custom exploration**
```python
import polars as pl

# Read data (format detected automatically)
df = pl.read_csv("data.csv")  # or read_excel, read_parquet, read_json

# Gather key information
schema = df.schema  # Column names and types
shape = (df.height, df.width)  # Rows, columns
stats = df.describe()  # Summary statistics
nulls = df.null_count()  # Missing values
```

Present findings in a structured summary:
- Data shape (rows × columns)
- Column types breakdown (numeric, categorical, temporal)
- Key statistics for numeric columns
- Unique values for categorical columns
- Date ranges for temporal data
- Notable patterns or data quality issues

For detailed Polars patterns, see [references/polars-patterns.md](references/polars-patterns.md).

### Step 3: Understand User Interest

After sharing initial insights, explicitly ask what aspects interest the user:

- "What aspects of this data would you like to explore?"
- "Are you interested in trends over time, category breakdowns, or relationships between variables?"
- "Which specific fields or patterns caught your attention?"

Listen for specific interests like:
- Time-based trends
- Category comparisons
- Distribution analysis
- Correlation between variables
- Metric vs metric comparisons
- Top/bottom performers
- Anomaly detection

### Step 4: Propose Visualizations

Based on data characteristics and user interests, propose 3-5 specific charts with rationale:

**Example proposal format:**
```
Based on your data analysis, I propose these visualizations:

1. **[Metric] by [Category] (Bar Chart)** - Compare values across different groups
2. **[Metric] Over Time (Line Chart)** - Show trends and patterns
3. **[Category] Distribution (Pie Chart)** - Visualize proportions of the whole
4. **[Value] Distribution (Histogram)** - Understand the spread of values
5. **[Variable A] vs [Variable B] (Scatter)** - Explore relationships

Would you like me to create these visualizations?
```

**Adapt to data type:**
- **Sales data**: "Revenue by Region", "Monthly Sales Trend", "Product Mix"
- **Web analytics**: "Traffic by Source", "Daily Visitors", "Bounce Rate Distribution"
- **Scientific data**: "Measurements by Condition", "Temperature Over Time", "Correlation Matrix"
- **Financial data**: "Spending by Category", "Transaction Trend", "Amount Distribution"

For chart type selection guidance, see [references/plotly-charts.md](references/plotly-charts.md).

### Step 5: Execute & Conclude

Once approved, create visualizations in marimo notebook and write conclusions.

#### Adding Visualization Cells

Use marimo MCP tools to inspect the notebook:
- `mcp__marimo__get_active_notebooks` - Get session ID
- `mcp__marimo__get_lightweight_cell_map` - View structure

Add cells directly to the marimo file using the Edit tool. Each chart follows this pattern:

```python
@app.cell
def _(df, go, pl):
    import plotly.graph_objects as go

    # Group data for visualization
    category_totals = df.group_by("category").agg(
        pl.col("amount").sum().alias("total")
    ).sort("total", descending=True)

    # Create chart using Graph Objects
    fig = go.Figure(data=[
        go.Bar(
            x=category_totals["category"].to_list(),
            y=category_totals["total"].to_list(),
            marker=dict(
                color=category_totals["total"].to_list(),
                colorscale='Blues',
                showscale=False
            )
        )
    ])
    fig.update_layout(
        title="Spending by Category",
        xaxis_title="Category",
        yaxis_title="Total Amount (TWD)",
        showlegend=False
    )
    return fig
```

**Cell guidelines:**
- **ALWAYS use Plotly Graph Objects (`plotly.graph_objects`), NOT Plotly Express**
- Import `go` from plotly.graph_objects in the imports cell
- Reference data from previous cells (e.g., `df`)
- Convert Polars columns to lists using `.to_list()` before passing to plotly
- Return the figure object
- Use descriptive titles and axis labels with `update_layout()`
- One visualization per cell for reactivity

**Why Graph Objects over Express:**
- No numpy dependency required
- More control over chart customization
- Explicit data handling with `.to_list()`
- Better performance with Polars DataFrames

#### Writing Conclusions

Add a conclusion cell summarizing key findings:

```python
@app.cell
def _():
    import marimo as mo
    mo.md("""
    ## Data Analysis Summary

    **Key Findings:**
    - [Finding 1: e.g., "Category A accounts for 45% of total (12,450 units)"]
    - [Finding 2: e.g., "Peak activity occurs on [day/time] - 2.3x above average"]
    - [Finding 3: e.g., "Largest value: 3,196 in [category] on [date]"]

    **Insights:**
    - [Pattern or trend observed from the data]
    - [Notable anomaly or outlier identified]
    """)
    return
```

Keep conclusions:
- **Brief** (3-5 bullet points for findings + 2-3 insights)
- **Data-driven** (include specific numbers from analysis)
- **Actionable** (suggest patterns or next steps when relevant)

After creating visualizations, use MCP tools to verify:
- `mcp__marimo__get_cell_outputs` - View rendered charts
- `mcp__marimo__lint_notebook` - Validate notebook structure

## Marimo MCP Tools Reference

When marimo runs with MCP enabled, these tools are available:

- `mcp__marimo__get_marimo_rules` - Get marimo best practices
- `mcp__marimo__get_active_notebooks` - List active sessions and file paths
- `mcp__marimo__get_lightweight_cell_map` - Preview notebook structure
- `mcp__marimo__get_tables_and_variables` - Inspect data in session
- `mcp__marimo__get_cell_outputs` - View visualization results
- `mcp__marimo__lint_notebook` - Validate changes

## Data Format Support

Polars supports these formats natively:

**CSV:**
```python
df = pl.read_csv("data.csv")
```

**Excel:**
```python
df = pl.read_excel("data.xlsx", sheet_name="Sheet1")
```

**Parquet:**
```python
df = pl.read_parquet("data.parquet")
```

**JSON:**
```python
df = pl.read_json("data.json")
```

## Visualization Selection Guide

Quick reference for choosing chart types:

**Categorical comparisons** → Bar chart, horizontal bar
**Proportions** → Pie chart (<7 categories), treemap
**Time series** → Line chart, area chart
**Distributions** → Histogram, box plot, violin plot
**Relationships** → Scatter plot, bubble chart
**Correlations** → Heatmap
**Multi-category** → Grouped bar, stacked bar

For detailed examples and customization patterns, see [references/plotly-charts.md](references/plotly-charts.md).

## Resources

This skill includes reference documentation for detailed patterns:

- **[references/polars-patterns.md](references/polars-patterns.md)** - Complete Polars data exploration patterns, filtering, transformations, and date operations
- **[references/plotly-charts.md](references/plotly-charts.md)** - Chart type examples, customization patterns, and interactive features
