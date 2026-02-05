---
name: kpi-number
description: Configure KPI number displays in drizzle-cube dashboards for showing single metric values with formatting. Use when displaying KPIs, single numbers, metrics, totals, or key performance indicators.
---

# KPI Number Configuration

Configure KPI number displays for drizzle-cube dashboards. KPI numbers show a single metric value prominently with optional formatting like prefixes, suffixes, and decimal places.

## Chart Type

```typescript
chartType: 'kpiNumber'
```

## Basic Configuration

```typescript
{
  id: 'kpi-1',
  title: 'Total Revenue',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue']
  }),
  chartType: 'kpiNumber',
  chartConfig: {
    yAxis: ['Sales.totalRevenue']
  },
  displayConfig: {
    prefix: '$',
    suffix: '',
    decimals: 2
  },
  x: 0, y: 0, w: 3, h: 2
}
```

## Chart Configuration (`chartConfig`)

### yAxis (Value)
- **Type**: `string[]`
- **Required**: Yes
- **Max Items**: 1
- **Purpose**: The measure to display
- **Example**: `['Sales.totalRevenue']`

## Display Configuration (`displayConfig`)

### prefix
- **Type**: `string`
- **Default**: `''`
- **Purpose**: Text before the number
- **Example**: `'$'`, `'€'`, `'#'`

### suffix
- **Type**: `string`
- **Default**: `''`
- **Purpose**: Text after the number
- **Example**: `'%'`, `' users'`, `' GB'`

### decimals
- **Type**: `number`
- **Default**: `0`
- **Purpose**: Number of decimal places
- **Example**: `0`, `2`, `4`

### valueColorIndex
- **Type**: `number`
- **Default**: `0`
- **Purpose**: Color index from palette for the number

## Examples

### Currency KPI

```typescript
{
  id: 'total-revenue',
  title: 'Total Revenue',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue']
  }),
  chartType: 'kpiNumber',
  chartConfig: {
    yAxis: ['Sales.totalRevenue']
  },
  displayConfig: {
    prefix: '$',
    decimals: 2
  },
  x: 0, y: 0, w: 3, h: 2
}
```

### Count KPI

```typescript
{
  id: 'total-users',
  title: 'Total Users',
  query: JSON.stringify({
    measures: ['Users.count']
  }),
  chartType: 'kpiNumber',
  chartConfig: {
    yAxis: ['Users.count']
  },
  displayConfig: {
    suffix: ' users',
    decimals: 0
  },
  x: 3, y: 0, w: 3, h: 2
}
```

### Percentage KPI

```typescript
{
  id: 'conversion-rate',
  title: 'Conversion Rate',
  query: JSON.stringify({
    measures: ['Analytics.conversionRate']
  }),
  chartType: 'kpiNumber',
  chartConfig: {
    yAxis: ['Analytics.conversionRate']
  },
  displayConfig: {
    suffix: '%',
    decimals: 1
  },
  x: 6, y: 0, w: 3, h: 2
}
```

### Average KPI

```typescript
{
  id: 'avg-order-value',
  title: 'Average Order Value',
  query: JSON.stringify({
    measures: ['Orders.avgValue']
  }),
  chartType: 'kpiNumber',
  chartConfig: {
    yAxis: ['Orders.avgValue']
  },
  displayConfig: {
    prefix: '$',
    decimals: 2
  },
  x: 9, y: 0, w: 3, h: 2
}
```

### Filtered KPI

```typescript
{
  id: 'active-users',
  title: 'Active Users (Last 30 Days)',
  query: JSON.stringify({
    measures: ['Users.activeCount'],
    timeDimensions: [{
      dimension: 'Activity.date',
      dateRange: 'last 30 days'
    }]
  }),
  chartType: 'kpiNumber',
  chartConfig: {
    yAxis: ['Users.activeCount']
  },
  displayConfig: {
    suffix: ' active',
    decimals: 0,
    valueColorIndex: 2
  },
  x: 0, y: 2, w: 4, h: 2
}
```

### Data Size KPI

```typescript
{
  id: 'storage-used',
  title: 'Storage Used',
  query: JSON.stringify({
    measures: ['Files.totalSize']
  }),
  chartType: 'kpiNumber',
  chartConfig: {
    yAxis: ['Files.totalSize']
  },
  displayConfig: {
    suffix: ' GB',
    decimals: 1
  },
  x: 0, y: 0, w: 3, h: 2
}
```

## Use Cases

- **Key Metrics**: Display primary business metrics
- **Summary Values**: Show totals at dashboard top
- **Quick Insights**: Provide at-a-glance numbers
- **Current Status**: Display current metric values
- **Goal Tracking**: Show progress toward targets

## Best Practices

1. **Keep titles short** - Clear, concise titles
2. **Use appropriate decimals** - 0 for counts, 2 for currency
3. **Add context in title** - Include time period if relevant
4. **Group related KPIs** - Place similar metrics together
5. **Use consistent formatting** - Same prefix/suffix for similar metrics
6. **Size appropriately** - Usually 2-4 grid units high

## Common Patterns

```typescript
// Dashboard header pattern (4 KPIs across top)
[
  { x: 0, y: 0, w: 3, h: 2, title: 'Revenue', prefix: '$' },
  { x: 3, y: 0, w: 3, h: 2, title: 'Orders', suffix: ' orders' },
  { x: 6, y: 0, w: 3, h: 2, title: 'Customers', suffix: ' users' },
  { x: 9, y: 0, w: 3, h: 2, title: 'Conversion', suffix: '%' }
]

// Currency pattern
{
  prefix: '$',
  decimals: 2
}

// Count pattern
{
  suffix: ' items',
  decimals: 0
}

// Percentage pattern
{
  suffix: '%',
  decimals: 1
}
```

## Related Skills

- Use `kpi-delta` for showing change/trends
- Use `kpi-text` for text-based KPIs
- Use `queries` skill for KPI calculations
