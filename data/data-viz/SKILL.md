---
name: data-viz
description: |
  Data visualization dashboard with multiple chart types — line, bar, pie,
  scatter, heatmap. All inline SVG. Use for "data viz", "charts", "graphs",
  "analytics".
triggers:
  - "data viz"
  - "charts"
  - "graphs"
  - "data visualization"
  - "analytics chart"
df:
  mode: prototype
  platform: desktop
  scenario: analytics
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Data Viz Skill

Produce a data visualization page with multiple chart types.

## Chart types available
- **Line chart**: time series, single or multi-line.
- **Bar chart**: categorical comparison, vertical or horizontal.
- **Pie / Donut**: part-to-whole, 2–8 segments.
- **Scatter**: correlation, with trend line.
- **Heatmap**: matrix of values, color intensity.
- **Area chart**: stacked or single, with gradient fill.

## Rules
- All charts inline SVG. No JS charting libraries.
- Axes: light gray lines, small mono labels.
- Tooltips: CSS-only via `:hover` on data points.
- Legend: color swatch + label, positioned near chart.
- `data-df-id` on each chart.
- Responsive: charts scale via `viewBox`, not fixed widths.

## Output
Single `index.html`, inline CSS.
