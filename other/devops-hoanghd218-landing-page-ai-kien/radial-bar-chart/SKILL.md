---
name: radial-bar-chart
description: Configure radial bar charts in drizzle-cube dashboards for circular progress and gauge visualizations. Use when creating radial bars, circular progress indicators, or gauge charts.
---

# Radial Bar Chart Configuration

Configure radial bar charts for drizzle-cube dashboards. Radial bar charts display data in a circular format, useful for progress indicators and gauge-style visualizations.

## Chart Type

```typescript
chartType: 'radialBar'
```

## Basic Configuration

```typescript
{
  id: 'radial-1',
  title: 'Goal Progress',
  query: JSON.stringify({
    dimensions: ['Goals.name'],
    measures: ['Goals.completionPercentage']
  }),
  chartType: 'radialBar',
  chartConfig: {
    xAxis: ['Goals.name'],
    yAxis: ['Goals.completionPercentage']
  },
  x: 0, y: 0, w: 6, h: 5
}
```

## Chart Configuration (`chartConfig`)

### xAxis (Categories)
- **Type**: `string[]`
- **Required**: Yes
- **Max Items**: 1
- **Purpose**: Dimension for radial segments
- **Example**: `['Goals.name']`

### yAxis (Values)
- **Type**: `string[]`
- **Purpose**: Measure (typically percentage)
- **Example**: `['Goals.completion']`

## Examples

### Progress Tracking

```typescript
{
  id: 'project-progress',
  title: 'Project Completion',
  query: JSON.stringify({
    dimensions: ['Projects.name'],
    measures: ['Projects.completionRate']
  }),
  chartType: 'radialBar',
  chartConfig: {
    xAxis: ['Projects.name'],
    yAxis: ['Projects.completionRate']
  },
  displayConfig: {
    showLegend: true
  },
  x: 0, y: 0, w: 6, h: 5
}
```

## Use Cases

- **Progress Indicators**: Show completion percentages
- **Goal Tracking**: Visualize goal achievement
- **Gauges**: Display metric gauges
- **Capacity Usage**: Show resource utilization

## Related Skills

- Use `kpi-number` for simple percentages
- Use `pie-chart` for proportions
