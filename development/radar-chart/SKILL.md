---
name: radar-chart
description: Configure radar (spider) charts in drizzle-cube dashboards for multi-dimensional comparison. Use when creating radar charts, spider charts, or comparing multiple metrics across categories.
---

# Radar Chart Configuration

Configure radar (spider) charts for drizzle-cube dashboards. Radar charts display multivariate data on a radial grid, ideal for comparing multiple dimensions or categories.

## Chart Type

```typescript
chartType: 'radar'
```

## Basic Configuration

```typescript
{
  id: 'radar-1',
  title: 'Product Comparison',
  query: JSON.stringify({
    dimensions: ['Products.feature'],
    measures: ['Products.rating']
  }),
  chartType: 'radar',
  chartConfig: {
    xAxis: ['Products.feature'],
    yAxis: ['Products.rating']
  },
  x: 0, y: 0, w: 6, h: 5
}
```

## Chart Configuration (`chartConfig`)

### xAxis (Dimensions)
- **Type**: `string[]`
- **Purpose**: Dimension for radar axes
- **Example**: `['Skills.name']`

### yAxis (Values)
- **Type**: `string[]`
- **Purpose**: Measures to plot
- **Example**: `['Employees.proficiency']`

### series (Multiple Radars)
- **Type**: `string[]`
- **Purpose**: Dimension to create multiple overlaid radars
- **Example**: `['Employees.name']`

## Examples

### Skill Assessment

```typescript
{
  id: 'skill-radar',
  title: 'Team Skill Assessment',
  query: JSON.stringify({
    dimensions: ['Skills.name', 'Employees.name'],
    measures: ['Assessment.avgScore']
  }),
  chartType: 'radar',
  chartConfig: {
    xAxis: ['Skills.name'],
    yAxis: ['Assessment.avgScore'],
    series: ['Employees.name']
  },
  displayConfig: {
    showLegend: true
  },
  x: 0, y: 0, w: 8, h: 6
}
```

### Product Features

```typescript
{
  id: 'product-features',
  title: 'Product Feature Ratings',
  query: JSON.stringify({
    dimensions: ['Features.category'],
    measures: ['Ratings.avgScore']
  }),
  chartType: 'radar',
  chartConfig: {
    xAxis: ['Features.category'],
    yAxis: ['Ratings.avgScore']
  },
  x: 6, y: 0, w: 6, h: 5
}
```

## Use Cases

- **Multi-Dimensional Comparison**: Compare items across multiple attributes
- **Skill Assessment**: Visualize competency levels
- **Product Comparison**: Compare product features
- **Performance Metrics**: Show balanced scorecard data

## Related Skills

- Use `bar-chart` for simpler comparisons
- Use `bubble-chart` for three-variable analysis
