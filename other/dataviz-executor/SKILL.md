---
name: dataviz-executor
type: executor
description: "Execute visualization implementations from dataviz-planner specs."
version: 0.1.0
---

# Data Visualization Executor Skill

## When to Use

**Primary triggers:**
- "generate a chart", "create a visualization", "build this chart"
- "execute this dataviz plan", "generate from this viz spec"
- "make a bar chart of this data", "plot this CSV"
- User has a dataviz-planner spec and wants an HTML visualization generated
- User has a CSV/JSON file and wants a chart produced

---

## Use When

- You have a completed dataviz-planner spec and want a self-contained HTML chart generated
- You have a CSV or JSON data file and a clear chart request (simple cases)
- You need a Plotly.js visualization with accessibility features (colorblind-safe, alt text, responsive)
- You want a chart that opens directly in the browser — no server or build step needed
- You need to produce a chart that dataviz-critic can then review

---

## Do Not Use When

- You need to **design** a visualization — use `dataviz-planner` first
- You need to **review** an existing visualization — use `dataviz-critic`
- You need a **dashboard** with multiple charts and KPI hierarchy — use `dashboard-planner` first
- You need **statistical analysis** of the data — analyze first, then visualize
- You need a **print-ready** static image — this produces interactive HTML, not PNG/PDF

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Have a dataviz-planner spec, need a chart | This skill — generates self-contained HTML |
| Need to design the visualization first | Use `dataviz-planner`, then come back |
| Have a chart, need quality review | Use `dataviz-critic` |
| Need multiple charts in a dashboard | Use `dashboard-planner` for architecture first |
| Have raw data, need quick exploratory chart | This skill — direct request mode (simple cases) |

---

## What You Get

- **Self-contained HTML file** with Plotly.js CDN, inline data, responsive layout
- **Accessibility features**: colorblind-safe palette, alt text, ARIA labels, keyboard navigation
- **Deviation log** documenting any places the output differs from the planner spec
- **Critic handoff command** — ready to run `/dataviz-critic` on the output

---

## Input Modes

### Mode 1: Planner Spec (Preferred)
Provide the output from `dataviz-planner`. The executor parses the structured plan (Question & Audience, Chart Type Selection, Design Specifications, Equity Review) and generates an HTML visualization matching the spec.

### Mode 2: Direct Request (Simple Cases)
Provide a data file path (CSV/JSON) and describe the chart: "Create a bar chart of sales by region from sales.csv." The executor generates the chart using sensible defaults. For complex multi-variable visualizations or equity-sensitive data, redirects to `dataviz-planner`.

---

## Supported Chart Types

| Chart Type | Use Case | Plotly.js Trace |
|-----------|----------|----------------|
| Bar (vertical/horizontal) | Category comparison | `bar` |
| Grouped/Stacked bar | Multi-series comparison | `bar` with `barmode` |
| Line | Trends over time | `scatter` mode lines |
| Multi-series line | Group trends | `scatter` mode lines (multiple traces) |
| Scatter | Relationship between variables | `scatter` |
| Scatter with regression | Correlation analysis | `scatter` + trendline |
| Histogram | Distribution | `histogram` |
| Box plot | Distribution comparison | `box` |
| Heatmap | Matrix relationships | `heatmap` |
| Treemap | Hierarchical composition | `treemap` |
| Choropleth | Geographic data | `choropleth` / `choroplethmapbox` |
| Pie/Donut | Part-to-whole (≤5 categories) | `pie` |

---

## Companion Skills

- **dataviz-planner** (upstream): Designs the visualization plan this executor implements
- **dataviz-critic** (downstream): Reviews the generated visualization for encoding honesty, accessibility, audience fit
- **dashboard-planner** (upstream, multi-chart): Designs dashboard architecture when multiple charts are needed

---

## meta-router Registry Note

Listed under the **Executors** table.
Trigger signals: `generate chart, create visualization, build chart, plot data, generate dataviz, create plotly chart, visualize this data`
