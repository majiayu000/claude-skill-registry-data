---
name: kpi-delta
description: Configure KPI delta displays in drizzle-cube dashboards for showing metrics with change indicators and trends. Use when displaying KPIs with trends, growth rates, or comparison to previous period.
---

# KPI Delta Configuration

Configure KPI delta displays for drizzle-cube dashboards. KPI delta shows a metric value with its change/delta from a previous period, including visual trend indicators.

## Chart Type

```typescript
chartType: 'kpiDelta'
```

## Basic Configuration

```typescript
{
  id: 'kpi-delta-1',
  title: 'Monthly Revenue',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue'],
    timeDimensions: [{
      dimension: 'Sales.date',
      granularity: 'month',
      dateRange: 'last 2 months'
    }]
  }),
  chartType: 'kpiDelta',
  chartConfig: {
    yAxis: ['Sales.totalRevenue'],
    xAxis: ['Sales.date']
  },
  displayConfig: {
    prefix: '$',
    decimals: 2,
    showHistogram: true
  },
  x: 0, y: 0, w: 3, h: 2
}
```

## Chart Configuration (`chartConfig`)

### yAxis (Value)
- **Type**: `string[]`
- **Required**: Yes
- **Max Items**: 1
- **Purpose**: The measure to display and calculate delta for
- **Example**: `['Sales.totalRevenue']`

### xAxis (Optional - Ordering)
- **Type**: `string[]`
- **Optional**: Yes
- **Max Items**: 1
- **Purpose**: Dimension for ordering data points (typically time dimension)
- **Example**: `['Sales.date']`

## Display Configuration (`displayConfig`)

### prefix
- **Type**: `string`
- **Default**: `''`
- **Purpose**: Text before number
- **Example**: `'$'`, `'€'`

### suffix
- **Type**: `string`
- **Default**: `''`
- **Purpose**: Text after number
- **Example**: `'%'`, `' users'`

### decimals
- **Type**: `number`
- **Default**: `0`
- **Purpose**: Decimal places

### positiveColorIndex
- **Type**: `number`
- **Default**: `2` (green)
- **Purpose**: Color for positive delta

### negativeColorIndex
- **Type**: `number`
- **Default**: `0` (red)
- **Purpose**: Color for negative delta

### showHistogram
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Show mini trend chart

## Examples

### Revenue Growth

```typescript
{
  id: 'revenue-growth',
  title: 'Monthly Revenue',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue'],
    timeDimensions: [{
      dimension: 'Sales.date',
      granularity: 'month',
      dateRange: 'last 2 months'
    }]
  }),
  chartType: 'kpiDelta',
  chartConfig: {
    yAxis: ['Sales.totalRevenue'],
    xAxis: ['Sales.date']
  },
  displayConfig: {
    prefix: '$',
    decimals: 2,
    showHistogram: true
  },
  x: 0, y: 0, w: 3, h: 2
}
```

### User Growth

```typescript
{
  id: 'user-growth',
  title: 'Active Users',
  query: JSON.stringify({
    measures: ['Users.activeCount'],
    timeDimensions: [{
      dimension: 'Activity.date',
      dateRange: 'last 2 weeks',
      granularity: 'week'
    }]
  }),
  chartType: 'kpiDelta',
  chartConfig: {
    yAxis: ['Users.activeCount'],
    xAxis: ['Activity.date']
  },
  displayConfig: {
    suffix: ' users',
    decimals: 0,
    showHistogram: true
  },
  x: 3, y: 0, w: 3, h: 2
}
```

### Conversion Rate

```typescript
{
  id: 'conversion-delta',
  title: 'Conversion Rate',
  query: JSON.stringify({
    measures: ['Analytics.conversionRate'],
    timeDimensions: [{
      dimension: 'Analytics.date',
      dateRange: 'last 2 months',
      granularity: 'month'
    }]
  }),
  chartType: 'kpiDelta',
  chartConfig: {
    yAxis: ['Analytics.conversionRate'],
    xAxis: ['Analytics.date']
  },
  displayConfig: {
    suffix: '%',
    decimals: 1,
    positiveColorIndex: 2,
    negativeColorIndex: 0
  },
  x: 6, y: 0, w: 3, h: 2
}
```

## Use Cases

- **Growth Tracking**: Show metric growth over time
- **Performance Monitoring**: Track KPI changes
- **Trend Indicators**: Display up/down trends
- **Comparison Metrics**: Compare to previous periods

## Best Practices

1. **Use 2 time periods** - Query should return current and previous period
2. **Consistent time ranges** - Use same granularity for comparison
3. **Meaningful deltas** - Choose appropriate comparison period
4. **Color consistency** - Green for positive, red for negative (or reverse if lower is better)
5. **Show histogram** - Provides visual trend context

## Related Skills

- Use `kpi-number` for simple metrics
- Use `line-chart` for detailed trends
- Use `queries` skill for time-based comparisons
