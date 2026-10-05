---
name: data-viz-recharts
description: |
  Data visualization design using Recharts or comparable charting libraries.
  Enforces brand-consistent colors, readable axes, accessible chart patterns.
  Use for charts, dashboards, analytics views, or any data-driven UI.
triggers:
  - "recharts"
  - "chart"
  - "data viz"
  - "dashboard chart"
  - "analytics chart"
df:
  mode: utility
  platform: desktop
  scenario: analytics
  design_system:
    requires: true
---

# Data Viz with Recharts

## Color Palette

Never use Recharts defaults (`#8884d8`, `#82ca9d`, `#ffc658`).
Define a custom palette:

```js
const CHART_COLORS = [
  'oklch(55% 0.22 260)',  // brand primary
  'oklch(65% 0.18 30)',   // warm accent
  'oklch(60% 0.15 155)',  // success green
  'oklch(55% 0.20 350)',  // alert red
  'oklch(70% 0.10 260)',  // primary muted
];
```

## Chart Type Selection

- **Comparison over time**: `<AreaChart>` with `fillOpacity={0.15}`
- **Part-to-whole (≤4 categories)**: `<BarChart layout="vertical">`
- **Correlation**: `<ScatterChart>` with domain-appropriate dot size
- **Single KPI trend**: `<LineChart>` + `<ReferenceLine>` for target
- **Never a pie chart with > 4 slices**

## Axes and Labels

Always show `<XAxis>` and `<YAxis>`:
```jsx
tick={{ fontSize: 12, fill: 'var(--color-text-muted)' }}
```

Use `tickFormatter` to abbreviate large numbers (1.2M, 34K).
Never show a chart without axis context.

## Tooltip Design

Override with `content={<CustomTooltip />}`. Match the app's design system:
rounded corners, subtle shadow, brand font.

## Grid and Borders

```jsx
<CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
```

Remove explicit chart borders. Minimal grid lines reduce cognitive noise.

## Responsive Sizing

Always wrap in `<ResponsiveContainer width="100%" height={height}>`.

Height values:
- 200px: sparkline / compact
- 300px: standard
- 400px: detailed
- 500px: focus chart

## Accessibility

- Add `aria-label` to `<ResponsiveContainer>`.
- Color is never the only differentiator — use shape or pattern fills.

## Animation

Disable default animation for frequently-updating dashboard charts:
`isAnimationActive={false}`. Use only for initial load of report-style charts.
