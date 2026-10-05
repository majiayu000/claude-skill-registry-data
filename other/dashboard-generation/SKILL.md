---
name: dashboard-generation
displayName: Dashboard Generation
tagline: Generate custom analytics dashboards with KPIs, charts, and automated data refreshes.
description: |
  Creates custom analytics dashboards with key performance indicators,
  interactive charts, and automated data refresh schedules. Connects to
  data sources, designs metric visualizations, and sets up alerting for
  KPI thresholds. Supports executive dashboards, team dashboards, and
  operational monitoring views.
department:
  - Data & Analytics
  - Product
  - Engineering
use_cases:
  - Business Intelligence
  - Data Visualization
  - KPI Tracking
tools_required:
  - PostgreSQL MCP
  - Mixpanel MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Build a product metrics dashboard with:
  - Daily/weekly active users
  - Feature adoption rates
  - Revenue per user
  - NPS score trend
exampleOutput: |
  Product Metrics Dashboard

  PANELS
  Row 1: Overview KPIs
    DAU: 2,840  |  WAU: 8,200  |  MAU: 18,400  |  DAU/MAU: 15.4%

  Row 2: Active Users Trend
    Line chart: DAU/WAU/MAU over last 90 days
    Trendline: +3.2% weekly growth

  Row 3: Feature Adoption
    Bar chart: Top 10 features by weekly active users
    Heatmap: Feature usage by user segment

  Row 4: Revenue Metrics
    ARPU: $42/month  |  LTV: $504  |  Expansion Revenue: +12% MoM
    Line chart: MRR trend with cohort breakdown

  Row 5: NPS Trend
    Current NPS: 42  |  Promoters: 58%  |  Detractors: 16%
    Line chart: NPS over last 6 months

  DATA REFRESH: Every 4 hours
  ALERTS: KPI drops >10% WoW
---

# Dashboard Generation

Generate custom analytics dashboards with KPIs, charts, and automated data refreshes.

**Integrations:** PostgreSQL, Mixpanel

## When to Use

- The user needs a custom dashboard for business or product metrics
- KPIs need to be visualized and tracked over time
- The user mentions "dashboard", "KPI tracking", or "data visualization"

## Steps

### Step 1: Define Metrics

Identify the KPIs and metrics to display on the dashboard.

### Step 2: Design Layout

Arrange panels and charts in a logical visual hierarchy.

### Step 3: Connect Data Sources

Set up queries and data connections for each metric.

### Step 4: Configure Refresh and Alerts

Set data refresh schedules and threshold-based alerts.

## Output

Deliver:
- Dashboard layout with configured panels
- Data source queries
- Refresh schedule and alert rules
