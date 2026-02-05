---
name: line-chart
description: Configure line charts in drizzle-cube dashboards for time series and trend analysis with multiple series support. Use when creating line charts, trend lines, multi-line graphs, or time series visualizations.
---

# Line Chart Configuration

Configure line charts for drizzle-cube dashboards. Line charts display data trends over time or continuous variables, ideal for showing changes and patterns.

## Chart Type

```typescript
chartType: 'line'
```

## Basic Configuration

```typescript
{
  id: 'line-chart-1',
  title: 'Sales Trend',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue'],
    timeDimensions: [{
      dimension: 'Sales.createdAt',
      granularity: 'month',
      dateRange: 'last 12 months'
    }]
  }),
  chartType: 'line',
  chartConfig: {
    xAxis: ['Sales.createdAt'],
    yAxis: ['Sales.totalRevenue']
  },
  displayConfig: {
    showGrid: true,
    showTooltip: true
  },
  x: 0, y: 0, w: 8, h: 4
}
```

## Chart Configuration (`chartConfig`)

### xAxis (Time/Category)
- **Type**: `string[]`
- **Purpose**: Time dimension or continuous variable
- **Example**: `['Sales.createdAt']`

### yAxis (Values)
- **Type**: `string[]`
- **Purpose**: Measures to plot as lines
- **Example**: `['Sales.revenue', 'Sales.profit']`

### series (Multiple Lines)
- **Type**: `string[]`
- **Purpose**: Dimension to create separate lines
- **Example**: `['Products.category']`

## Display Configuration (`displayConfig`)

### showGrid
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Show background grid

### showLegend
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Display series legend

### showTooltip
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Show data point tooltips

### colors
- **Type**: `string[]`
- **Purpose**: Custom line colors

## Examples

### Simple Time Series

```typescript
{
  id: 'monthly-revenue',
  title: 'Monthly Revenue',
  query: JSON.stringify({
    measures: ['Orders.totalRevenue'],
    timeDimensions: [{
      dimension: 'Orders.createdAt',
      granularity: 'month',
      dateRange: 'this year'
    }]
  }),
  chartType: 'line',
  chartConfig: {
    xAxis: ['Orders.createdAt'],
    yAxis: ['Orders.totalRevenue']
  },
  x: 0, y: 0, w: 8, h: 4
}
```

### Multiple Measures

```typescript
{
  id: 'multi-metric',
  title: 'Revenue vs Profit Trend',
  query: JSON.stringify({
    measures: ['Sales.revenue', 'Sales.profit', 'Sales.costs'],
    timeDimensions: [{
      dimension: 'Sales.date',
      granularity: 'week',
      dateRange: 'last 90 days'
    }]
  }),
  chartType: 'line',
  chartConfig: {
    xAxis: ['Sales.date'],
    yAxis: ['Sales.revenue', 'Sales.profit', 'Sales.costs']
  },
  displayConfig: {
    showLegend: true,
    showGrid: true
  },
  x: 0, y: 0, w: 12, h: 5
}
```

### Multi-Series (Category Split)

```typescript
{
  id: 'regional-sales',
  title: 'Sales by Region',
  query: JSON.stringify({
    measures: ['Sales.revenue'],
    dimensions: ['Sales.region'],
    timeDimensions: [{
      dimension: 'Sales.date',
      granularity: 'month',
      dateRange: 'last 6 months'
    }]
  }),
  chartType: 'line',
  chartConfig: {
    xAxis: ['Sales.date'],
    yAxis: ['Sales.revenue'],
    series: ['Sales.region'] // One line per region
  },
  displayConfig: {
    showLegend: true
  },
  x: 0, y: 0, w: 10, h: 5
}
```

### Daily Active Users

```typescript
{
  id: 'daily-active-users',
  title: 'Daily Active Users',
  query: JSON.stringify({
    measures: ['Users.activeCount'],
    timeDimensions: [{
      dimension: 'Activity.date',
      granularity: 'day',
      dateRange: 'last 30 days'
    }]
  }),
  chartType: 'line',
  chartConfig: {
    xAxis: ['Activity.date'],
    yAxis: ['Users.activeCount']
  },
  displayConfig: {
    showGrid: true,
    showTooltip: true,
    colors: ['#4ECDC4']
  },
  x: 0, y: 0, w: 12, h: 4
}
```

### Growth Metrics

```typescript
{
  id: 'growth-metrics',
  title: 'User Growth Metrics',
  query: JSON.stringify({
    measures: [
      'Users.totalCount',
      'Users.newSignups',
      'Users.activeUsers'
    ],
    timeDimensions: [{
      dimension: 'Users.createdAt',
      granularity: 'week',
      dateRange: 'last 12 weeks'
    }]
  }),
  chartType: 'line',
  chartConfig: {
    xAxis: ['Users.createdAt'],
    yAxis: ['Users.totalCount', 'Users.newSignups', 'Users.activeUsers']
  },
  displayConfig: {
    showLegend: true,
    showGrid: true,
    colors: ['#45B7D1', '#FFA07A', '#98D8C8']
  },
  x: 0, y: 0, w: 12, h: 5
}
```

## Use Cases

- **Trend Analysis**: Show how metrics change over time
- **Forecasting**: Identify patterns for predictions
- **Seasonality**: Detect seasonal patterns
- **Performance Tracking**: Monitor KPIs over time
- **Comparison**: Compare multiple metrics or categories
- **Growth Metrics**: Visualize growth rates

## Best Practices

1. **Use for continuous data** - Line charts work best for time series
2. **Limit line count** - Max 5-7 lines for readability
3. **Choose appropriate granularity** - Match time grain to data density
4. **Add context with date ranges** - Show relevant time periods
5. **Use distinct colors** - Make lines easily distinguishable
6. **Include zero baseline** - Shows true scale of changes

## Related Skills

- Use `queries` skill for time dimension queries
- Use `area-chart` skill for cumulative trends
- Use `bar-chart` skill for discrete comparisons
