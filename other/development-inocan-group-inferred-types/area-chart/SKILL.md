---
name: area-chart
description: Configure area charts in drizzle-cube dashboards for cumulative trends and stacked time series. Use when creating area charts, stacked area graphs, or cumulative visualizations.
---

# Area Chart Configuration

Configure area charts for drizzle-cube dashboards. Area charts display quantitative data over time with filled regions, ideal for showing cumulative trends and volume.

## Chart Type

```typescript
chartType: 'area'
```

## Basic Configuration

```typescript
{
  id: 'area-chart-1',
  title: 'Revenue Over Time',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue'],
    timeDimensions: [{
      dimension: 'Sales.date',
      granularity: 'month',
      dateRange: 'last 12 months'
    }]
  }),
  chartType: 'area',
  chartConfig: {
    xAxis: ['Sales.date'],
    yAxis: ['Sales.totalRevenue']
  },
  displayConfig: {
    stacked: false
  },
  x: 0, y: 0, w: 8, h: 4
}
```

## Chart Configuration (`chartConfig`)

### xAxis (Time)
- **Type**: `string[]`
- **Purpose**: Time dimension
- **Example**: `['Sales.createdAt']`

### yAxis (Values)
- **Type**: `string[]`
- **Purpose**: Measures to display as filled areas
- **Example**: `['Sales.revenue', 'Sales.costs']`

### series (Multiple Areas)
- **Type**: `string[]`
- **Purpose**: Dimension for separate areas
- **Example**: `['Products.category']`

## Display Configuration (`displayConfig`)

### stacked
- **Type**: `boolean`
- **Default**: `false`
- **Purpose**: Stack areas on top of each other

### showLegend
- **Type**: `boolean`
- **Default**: `true`

### showGrid
- **Type**: `boolean`
- **Default**: `true`

### colors
- **Type**: `string[]`
- **Purpose**: Custom area colors

## Examples

### Simple Area Chart

```typescript
{
  id: 'cumulative-sales',
  title: 'Cumulative Sales',
  query: JSON.stringify({
    measures: ['Orders.totalRevenue'],
    timeDimensions: [{
      dimension: 'Orders.createdAt',
      granularity: 'week',
      dateRange: 'last 90 days'
    }]
  }),
  chartType: 'area',
  chartConfig: {
    xAxis: ['Orders.createdAt'],
    yAxis: ['Orders.totalRevenue']
  },
  x: 0, y: 0, w: 12, h: 4
}
```

### Stacked Area Chart

```typescript
{
  id: 'revenue-by-source',
  title: 'Revenue by Source',
  query: JSON.stringify({
    measures: ['Revenue.total'],
    dimensions: ['Revenue.source'],
    timeDimensions: [{
      dimension: 'Revenue.date',
      granularity: 'month',
      dateRange: 'this year'
    }]
  }),
  chartType: 'area',
  chartConfig: {
    xAxis: ['Revenue.date'],
    yAxis: ['Revenue.total'],
    series: ['Revenue.source']
  },
  displayConfig: {
    stacked: true,
    showLegend: true
  },
  x: 0, y: 0, w: 12, h: 5
}
```

## Use Cases

- **Cumulative Trends**: Show accumulation over time
- **Volume Visualization**: Display magnitude/volume
- **Multiple Streams**: Stacked sources or categories
- **Trend Emphasis**: Emphasize overall direction

## Related Skills

- Use `line-chart` for non-cumulative trends
- Use `bar-chart` for discrete comparisons
