---
name: lumen-dashboards
description: Master declarative, no-code data dashboards with Lumen YAML specifications. Use this skill when building standard data exploration dashboards, connecting multiple data sources (files, databases, APIs), creating interactive filters and cross-filtering, designing responsive layouts with indicators and charts, or enabling rapid dashboard prototyping without writing code.
compatibility: Requires lumen >= 0.10.0, panel >= 1.3.0, holoviews >= 1.18.0, param >= 2.0.0. Supports PostgreSQL, DuckDB, SQLite, CSV, Parquet, Excel, and REST API data sources.
---

# Lumen Dashboards Skill

## Overview

Master building declarative, no-code data dashboards with Lumen's YAML-based specification system. This skill covers creating interactive data exploration dashboards through configuration rather than programming, enabling rapid development of data applications with sources, transforms, views, and layouts.

## Dependencies

- lumen >= 0.10.0
- panel >= 1.3.0
- holoviews >= 1.18.0
- param >= 2.0.0

## What is Lumen?

Lumen is a declarative framework built on Panel for creating data dashboards and exploration interfaces through YAML specifications or Python API. It provides:

- **Declarative approach**: Define dashboards in YAML without writing code
- **Data pipelines**: Connect sources → transforms → views in reproducible workflows
- **Interactive exploration**: Built-in filters, cross-filtering, and drill-down
- **Component library**: Reusable sources, transforms, and visualization views
- **Live updates**: Auto-reload during development, real-time data updates in production

### Lumen vs Panel

**Use Lumen when**:
- Building standard data exploration dashboards
- Working with non-programmers who need to modify dashboards
- Want rapid prototyping with configuration
- Need reproducible, shareable dashboard specifications
- Working with common data patterns (load → filter → visualize)

**Use Panel when**:
- Building custom application logic
- Need fine-grained control over every component
- Creating novel interactions not covered by Lumen
- Developing libraries or reusable components

**Key difference**: Lumen is *declarative* (describe what you want), Panel is *imperative* (specify how to build it).

## Core Capabilities

### 1. Data Sources

Lumen supports multiple source types for loading data:

#### File Sources

```yaml
sources:
  local_csv:
    type: file
    tables:
      data: ./data/penguins.csv

  remote_data:
    type: file
    tables:
      sales: https://example.com/sales.parquet
      inventory: https://example.com/inventory.csv

  excel_source:
    type: file
    tables:
      sheet1: ./workbook.xlsx
```

**Supported formats**: CSV, Parquet, Excel, JSON, Feather

#### Database Sources

```yaml
sources:
  postgres_db:
    type: postgres
    connection_string: postgresql://user:password@localhost:5432/mydb
    tables:
      - customers
      - orders
      - products

  duckdb_source:
    type: duckdb
    uri: ./analytics.duckdb
    tables:
      - events
      - metrics
```

**Supported databases**: PostgreSQL, DuckDB, SQLite, and SQLAlchemy-compatible databases

#### REST API Sources

```yaml
sources:
  api_source:
    type: rest
    url: https://api.example.com/data
    tables:
      metrics: /v1/metrics
```

#### Intake Catalog Sources

```yaml
sources:
  catalog:
    type: intake
    uri: ./catalog.yml
```

### 2. Data Transforms

Transform and process data in pipelines:

#### Column Selection

```yaml
transforms:
  - type: columns
    columns: ['name', 'age', 'city', 'revenue']
```

#### Filtering

```yaml
transforms:
  - type: query
    query: "age > 18 and city == 'NYC'"

  - type: filter
    conditions:
      age: {'>': 18}
      status: ['active', 'pending']
```

#### Aggregation

```yaml
transforms:
  - type: aggregate
    by: ['category', 'region']
    aggregate:
      revenue: sum
      customers: count
      avg_order: mean
```

#### Sorting

```yaml
transforms:
  - type: sort
    by: ['date']
    reverse: true
```

#### SQL Transforms

```yaml
transforms:
  - type: sql
    query: |
      SELECT
        category,
        SUM(revenue) as total_revenue,
        COUNT(*) as count
      FROM table
      WHERE date >= '2024-01-01'
      GROUP BY category
      ORDER BY total_revenue DESC
```

#### Custom Python Transforms

```yaml
transforms:
  - type: custom
    module: mymodule.transforms
    transform: normalize_data
    kwargs:
      method: 'z-score'
```

### 3. Filters (Interactive Widgets)

Add interactive filtering to dashboards:

#### Widget Filters

```yaml
filters:
  - type: widget
    field: category
    label: Product Category

  - type: widget
    field: date_range
    widget: date_range_slider
    start: '2024-01-01'
    end: '2024-12-31'

  - type: widget
    field: price
    widget: range_slider
    start: 0
    end: 1000
    step: 10
```

#### Constant Filters

```yaml
filters:
  - type: constant
    field: status
    value: 'active'
```

#### Cross-filtering

```yaml
# Enable cross-filtering across views
config:
  cross_filter: true

layouts:
  - title: Dashboard
    cross_filter_group: 'main'
    views: [...]
```

### 4. Views (Visualizations)

Display data with various view types:

#### Table View

```yaml
views:
  - type: table
    title: Raw Data
    show_index: false
    pagination: front
    page_size: 20
    sorters: [name, date]
    editors:
      status: ['active', 'inactive']
```

#### hvPlot Views

```yaml
views:
  # Scatter plot
  - type: hvplot
    kind: scatter
    x: bill_length_mm
    y: bill_depth_mm
    color: species
    size: body_mass_g
    responsive: true
    height: 400

  # Line chart
  - type: hvplot
    kind: line
    x: date
    y: revenue
    by: category
    responsive: true

  # Bar chart
  - type: hvplot
    kind: bar
    x: product
    y: sales
    rot: 45

  # Histogram
  - type: hvplot
    kind: hist
    y: age
    bins: 20
    alpha: 0.7
```

#### Plotly Views

```yaml
views:
  - type: plotly
    x: category
    y: revenue
    kind: bar
    color: region
    barmode: group
```

#### Altair Views

```yaml
views:
  - type: altair
    spec:
      mark: point
      encoding:
        x: {field: x, type: quantitative}
        y: {field: y, type: quantitative}
        color: {field: category, type: nominal}
```

#### Indicator Views

```yaml
views:
  - type: indicator
    field: total_revenue
    title: Total Revenue
    format: '${value:,.0f}'
    color: green

  - type: indicator
    field: avg_satisfaction
    title: Customer Satisfaction
    format: '{value:.1%}'
    color_ranges:
      - [0, 0.7, 'red']
      - [0.7, 0.85, 'orange']
      - [0.85, 1.0, 'green']
```

#### String Views (KPI Cards)

```yaml
views:
  - type: string
    template: |
      # Q4 Performance

      **Total Sales**: ${revenue:,.0f}
      **Growth**: +{growth:.1%}
      **Target**: {target_percent:.0%} achieved
    height: 200
```

### 5. Pipelines

Combine sources, transforms, filters, and views:

```yaml
sources:
  sales_db:
    type: postgres
    connection_string: ${SALES_DB_URL}
    tables: [transactions]

pipelines:
  sales_pipeline:
    source: sales_db
    table: transactions

    filters:
      - type: widget
        field: region
        label: Region

      - type: widget
        field: date
        widget: date_range_slider

    transforms:
      - type: query
        query: "status == 'completed'"

      - type: aggregate
        by: ['product_category', 'region']
        aggregate:
          revenue: sum
          quantity: sum
          avg_price: mean

      - type: sort
        by: ['revenue']
        reverse: true

layouts:
  - title: Sales Dashboard
    pipeline: sales_pipeline
    views:
      - type: indicator
        field: revenue
        title: Total Revenue
        format: '${value:,.0f}'

      - type: hvplot
        kind: bar
        x: product_category
        y: revenue
        color: region
        responsive: true

      - type: table
        title: Detailed Breakdown
```

### 6. Layouts

Organize views in responsive layouts:

#### Row/Column Layouts

```yaml
layouts:
  - title: Dashboard
    pipeline: data_pipeline
    layout: [[0, 1], [2]]  # Row 1: views 0,1 | Row 2: view 2
    sizing_mode: stretch_width
    height: 800

    views:
      - type: indicator
        field: total_sales

      - type: indicator
        field: avg_rating

      - type: hvplot
        kind: line
        x: date
        y: revenue
```

#### Tabs Layout

```yaml
layouts:
  - title: Multi-Tab Dashboard
    tabs: true

    - title: Overview
      pipeline: overview_pipeline
      views: [...]

    - title: Detailed Analysis
      pipeline: detail_pipeline
      views: [...]
```

#### Faceted Layout

```yaml
layouts:
  - title: Regional Analysis
    pipeline: regional_pipeline
    facet_by: region
    ncols: 2
    views:
      - type: hvplot
        kind: scatter
        x: x
        y: y
```

### 7. Global Configuration

Dashboard-wide settings:

```yaml
config:
  title: Sales Analytics Dashboard
  logo: ./logo.png
  favicon: ./favicon.ico

  # Theming
  theme: dark
  accent_color: '#00aa41'

  # Layout
  layout: column

  # Features
  editable: true
  show_traceback: false

  # Authentication
  auth: true
  auth_provider: okta

  # Caching
  cache: true
  cache_per_user: true
```

## Complete Dashboard Example

### Sales Analytics Dashboard

**File: `sales_dashboard.yaml`**

```yaml
config:
  title: Q4 Sales Analytics
  theme: default
  sizing_mode: stretch_width

sources:
  sales_data:
    type: file
    tables:
      transactions: https://data.company.com/q4_sales.parquet

pipelines:
  main_pipeline:
    source: sales_data
    table: transactions

    filters:
      - type: widget
        field: region
        label: Sales Region

      - type: widget
        field: product_category
        label: Product Category

      - type: widget
        field: date
        widget: date_range_slider
        label: Date Range

    transforms:
      - type: columns
        columns:
          - date
          - region
          - product_category
          - product_name
          - quantity
          - revenue
          - customer_satisfaction

      - type: query
        query: "revenue > 0"

  summary_pipeline:
    source: sales_data
    table: transactions

    transforms:
      - type: aggregate
        by: ['product_category']
        aggregate:
          total_revenue: {revenue: sum}
          total_quantity: {quantity: sum}
          avg_satisfaction: {customer_satisfaction: mean}

      - type: sort
        by: ['total_revenue']
        reverse: true

layouts:
  - title: Overview
    layout: [[0, 1, 2], [3], [4, 5]]
    height: 1200

    # KPIs
    - type: indicator
      pipeline: summary_pipeline
      field: total_revenue
      title: Total Revenue
      format: '${value:,.0f}'
      color: green

    - type: indicator
      pipeline: summary_pipeline
      field: total_quantity
      title: Units Sold
      format: '{value:,.0f}'
      color: blue

    - type: indicator
      pipeline: summary_pipeline
      field: avg_satisfaction
      title: Avg. Satisfaction
      format: '{value:.1%}'
      color_ranges:
        - [0, 0.7, 'red']
        - [0.7, 0.85, 'orange']
        - [0.85, 1.0, 'green']

    # Revenue over time
    - type: hvplot
      pipeline: main_pipeline
      kind: line
      x: date
      y: revenue
      by: product_category
      title: Revenue Trend
      responsive: true
      height: 400

    # Category breakdown
    - type: hvplot
      pipeline: summary_pipeline
      kind: bar
      x: product_category
      y: total_revenue
      title: Revenue by Category
      rot: 45
      responsive: true
      height: 400

    # Detailed table
    - type: table
      pipeline: main_pipeline
      title: Transaction Details
      page_size: 15
      show_index: false
      responsive: true
      height: 400
```

**Launch:**
```bash
lumen serve sales_dashboard.yaml --show --autoreload
```

## Best Practices

### 1. Data Source Management

**Use environment variables for credentials:**
```yaml
sources:
  production_db:
    type: postgres
    connection_string: ${DATABASE_URL}
```

**Separate configuration for environments:**
```bash
# Development
lumen serve dashboard.yaml --dev

# Production
export DATABASE_URL="postgres://..."
lumen serve dashboard.yaml
```

### 2. Performance Optimization

**Pre-aggregate large datasets:**
```yaml
transforms:
  # Aggregate before filtering for better performance
  - type: aggregate
    by: ['date', 'category']
    aggregate:
      value: sum

  - type: query
    query: "date >= '2024-01-01'"
```

**Use appropriate file formats:**
- Parquet for large columnar data
- CSV for small, human-readable data
- Feather for fast I/O within Python ecosystem

**Enable caching:**
```yaml
config:
  cache: true
  cache_per_user: true  # For multi-user deployments
```

### 3. Layout and Responsiveness

**Always use responsive sizing:**
```yaml
layouts:
  - sizing_mode: stretch_width
    views:
      - type: hvplot
        responsive: true
        height: 400  # Set explicit height with responsive width
```

**Mobile-friendly layouts:**
```yaml
layouts:
  - ncols: 1  # Single column on mobile
    views: [...]
```

### 4. Filter Design

**Provide sensible defaults:**
```yaml
filters:
  - type: widget
    field: date
    widget: date_range_slider
    start: '2024-01-01'
    end: '2024-12-31'
    default: ['2024-10-01', '2024-12-31']  # Default to Q4
```

**Group related filters:**
```yaml
layouts:
  - title: Dashboard
    sidebar:
      - '## Time Period'
      - {type: widget, field: date}
      - '## Geography'
      - {type: widget, field: region}
      - {type: widget, field: country}
```

### 5. Validation

**Validate specifications before deployment:**
```bash
lumen validate dashboard.yaml
```

**Check for common issues:**
- Missing source tables
- Invalid field references
- Circular dependencies
- Unsupported transform combinations

## Python API

For programmatic dashboard creation:

```python
from lumen.sources import FileSource
from lumen.transforms import Aggregate
from lumen.filters import WidgetFilter
from lumen.views import hvPlotView, IndicatorView
from lumen.pipeline import Pipeline
from lumen.dashboard import Dashboard

# Define components
source = FileSource(tables={'sales': 'data/sales.csv'})

pipeline = Pipeline(
    source=source,
    table='sales',
    filters=[
        WidgetFilter(field='region'),
        WidgetFilter(field='category')
    ],
    transforms=[
        Aggregate(
            by=['category'],
            aggregate={'revenue': 'sum', 'quantity': 'sum'}
        )
    ]
)

# Create views
kpi = IndicatorView(
    pipeline=pipeline,
    field='revenue',
    title='Total Revenue',
    format='${value:,.0f}'
)

chart = hvPlotView(
    pipeline=pipeline,
    kind='bar',
    x='category',
    y='revenue',
    responsive=True
)

# Build dashboard
dashboard = Dashboard(
    title='Sales Dashboard',
    pipelines={'main': pipeline},
    views=[kpi, chart],
    layout=[[0], [1]]
)

# Serve
dashboard.show()
```

## Common Patterns

### Pattern 1: Multi-Source Dashboard

```yaml
sources:
  sales_db:
    type: postgres
    connection_string: ${SALES_DB}
    tables: [orders]

  inventory_api:
    type: rest
    url: https://api.inventory.com
    tables:
      stock: /v1/stock

pipelines:
  sales_pipeline:
    source: sales_db
    table: orders

  inventory_pipeline:
    source: inventory_api
    table: stock

layouts:
  - title: Sales & Inventory
    views:
      - type: hvplot
        pipeline: sales_pipeline
        kind: line
        x: date
        y: revenue

      - type: table
        pipeline: inventory_pipeline
```

### Pattern 2: Drill-Down Dashboard

```yaml
pipelines:
  overview:
    source: data_source
    table: metrics
    transforms:
      - type: aggregate
        by: ['region']
        aggregate: {revenue: sum}

  detail:
    source: data_source
    table: metrics
    filters:
      - type: widget
        field: region  # Links to selection in overview

layouts:
  - title: Drill-Down
    cross_filter: true
    views:
      - type: hvplot
        pipeline: overview
        kind: bar
        x: region
        y: revenue
        title: Click a region to drill down

      - type: table
        pipeline: detail
        title: Regional Details
```

### Pattern 3: Custom Component Integration

```yaml
sources:
  custom_data:
    type: custom
    module: myproject.sources
    source_type: MyCustomSource
    kwargs:
      api_key: ${API_KEY}

transforms:
  - type: custom
    module: myproject.transforms
    transform: complex_calculation
    kwargs:
      parameter: value

views:
  - type: custom
    module: myproject.views
    view_type: MyCustomView
    field: result
```

## Deployment

### Development Server

```bash
# Auto-reload on changes
lumen serve dashboard.yaml --autoreload --show

# Specify port
lumen serve dashboard.yaml --port 5007

# Development mode (verbose logging)
lumen serve dashboard.yaml --dev
```

### Production Deployment

```bash
# Production server with multiple workers
panel serve dashboard.yaml \
  --port 80 \
  --num-procs 4 \
  --allow-websocket-origin=dashboard.company.com

# With authentication
panel serve dashboard.yaml \
  --oauth-provider=generic \
  --oauth-key=${OAUTH_KEY} \
  --oauth-secret=${OAUTH_SECRET}

# Behind reverse proxy
panel serve dashboard.yaml \
  --prefix=/analytics \
  --use-xheaders
```

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dashboard.yaml .
COPY data/ ./data/

CMD ["lumen", "serve", "dashboard.yaml", "--port", "5006", "--address", "0.0.0.0"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  dashboard:
    build: .
    ports:
      - "5006:5006"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./data:/app/data
```

## Troubleshooting

### Issue: Dashboard Not Loading

**Check specification syntax:**
```bash
lumen validate dashboard.yaml
```

**Common issues:**
- Incorrect indentation in YAML
- Missing required fields
- Invalid source table references

### Issue: Data Not Displaying

**Verify source connection:**
```python
from lumen.sources import FileSource
source = FileSource(tables={'test': 'data.csv'})
print(source.get('test'))
```

**Check transform chain:**
- Remove transforms one by one to isolate issue
- Verify column names match exactly
- Check for empty results after filtering

### Issue: Slow Performance

**Profile the dashboard:**
```bash
lumen serve dashboard.yaml --profiler pyinstrument
```

**Optimization strategies:**
1. Pre-aggregate data at source
2. Reduce row counts with early filtering
3. Use appropriate file formats (Parquet)
4. Enable caching
5. Limit page sizes for tables

### Issue: Filters Not Working

**Verify field names:**
- Field must exist in pipeline data
- Case-sensitive matching
- Check for spaces or special characters

**Check filter placement:**
```yaml
pipelines:
  my_pipeline:
    filters:  # Correct placement
      - type: widget
        field: category

    transforms:  # Filters applied before transforms
      - type: aggregate
        by: ['category']
```

## Resources

- [Lumen Documentation](https://lumen.holoviz.org)
- [Lumen Gallery](https://lumen.holoviz.org/gallery/)
- [GitHub Repository](https://github.com/holoviz/lumen)
- [Community Discourse](https://discourse.holoviz.org)

## Use Cases

### Business Intelligence Dashboards
- Sales performance tracking
- Financial reporting
- Inventory management
- Customer analytics

### Data Exploration Tools
- Scientific data analysis
- Research data visualization
- Quality assurance monitoring
- A/B test analysis

### Operational Dashboards
- Real-time monitoring
- System metrics
- IoT sensor data
- Log analysis

### Self-Service Analytics
- Enable business users to explore data
- Reduce analyst backlog
- Democratize data access
- Maintain governance through configuration

## Summary

Lumen provides a powerful declarative approach to building data dashboards:

**Strengths:**
- No-code dashboard creation
- Rapid prototyping
- Reproducible specifications
- Extensive component library
- Built on Panel ecosystem

**When to use:**
- Standard data exploration patterns
- Enabling non-programmers
- Rapid dashboard development
- Shareable configurations

**When not to use:**
- Highly custom interactions
- Novel visualization types
- Complex application logic
- Fine-grained control needs

For AI-powered natural language data exploration, see the **Lumen AI** skill.
