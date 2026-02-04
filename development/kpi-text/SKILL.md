---
name: kpi-text
description: Configure KPI text displays in drizzle-cube dashboards for showing metric values with custom text templates. Use when displaying KPIs with custom formatting, labels, or contextual text around numeric values.
---

# KPI Text Configuration

Configure KPI text displays for drizzle-cube dashboards. KPI text shows a measure value embedded within a custom text template, allowing you to create formatted status messages and labeled metrics.

## Chart Type

```typescript
chartType: 'kpiText'
```

## Basic Configuration

```typescript
{
  id: 'kpi-text-1',
  title: 'Active Users',
  query: JSON.stringify({
    measures: ['Users.activeCount']
  }),
  chartType: 'kpiText',
  chartConfig: {
    yAxis: ['Users.activeCount']
  },
  displayConfig: {
    template: 'Currently ${value} active users online'
  },
  x: 0, y: 0, w: 4, h: 2
}
```

## Chart Configuration (`chartConfig`)

### yAxis (Value)
- **Type**: `string[]`
- **Required**: Yes
- **Max Items**: 1
- **Purpose**: The measure to display in the template
- **Example**: `['Sales.totalRevenue']`

## Display Configuration (`displayConfig`)

### template
- **Type**: `string`
- **Default**: `'${value}'`
- **Purpose**: Text template with `${value}` placeholder for the metric
- **Example**: `'Total Revenue: ${value}'`, `'${value} users online'`

### decimals
- **Type**: `number`
- **Default**: `0`
- **Purpose**: Number of decimal places for the value
- **Example**: `0`, `2`

### valueColorIndex
- **Type**: `number`
- **Default**: `0`
- **Purpose**: Color index from palette for the value
- **Example**: `0`, `2`, `4`

### hideHeader
- **Type**: `boolean`
- **Default**: `false`
- **Purpose**: Hide the chart title header

## Examples

### Status with Count

```typescript
{
  id: 'online-users',
  title: 'Online Status',
  query: JSON.stringify({
    measures: ['Users.onlineCount']
  }),
  chartType: 'kpiText',
  chartConfig: {
    yAxis: ['Users.onlineCount']
  },
  displayConfig: {
    template: '${value} users currently online',
    decimals: 0
  },
  x: 0, y: 0, w: 4, h: 2
}
```

### Revenue with Currency

```typescript
{
  id: 'revenue-status',
  title: 'Revenue Status',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue']
  }),
  chartType: 'kpiText',
  chartConfig: {
    yAxis: ['Sales.totalRevenue']
  },
  displayConfig: {
    template: 'Total revenue today: $${value}',
    decimals: 2,
    valueColorIndex: 2
  },
  x: 4, y: 0, w: 4, h: 2
}
```

### Percentage Status

```typescript
{
  id: 'completion-status',
  title: 'Project Status',
  query: JSON.stringify({
    measures: ['Projects.completionRate']
  }),
  chartType: 'kpiText',
  chartConfig: {
    yAxis: ['Projects.completionRate']
  },
  displayConfig: {
    template: 'Project is ${value}% complete',
    decimals: 1
  },
  x: 0, y: 2, w: 4, h: 2
}
```

### Inventory Alert

```typescript
{
  id: 'stock-alert',
  title: 'Inventory Alert',
  query: JSON.stringify({
    measures: ['Inventory.lowStockCount'],
    filters: [{
      member: 'Inventory.quantity',
      operator: 'lt',
      values: ['10']
    }]
  }),
  chartType: 'kpiText',
  chartConfig: {
    yAxis: ['Inventory.lowStockCount']
  },
  displayConfig: {
    template: '⚠️ ${value} items low in stock',
    decimals: 0,
    valueColorIndex: 3
  },
  x: 8, y: 0, w: 4, h: 2
}
```

### System Health

```typescript
{
  id: 'health-score',
  title: 'System Health',
  query: JSON.stringify({
    measures: ['System.healthScore']
  }),
  chartType: 'kpiText',
  chartConfig: {
    yAxis: ['System.healthScore']
  },
  displayConfig: {
    template: 'System health score: ${value}/100',
    decimals: 0,
    valueColorIndex: 2
  },
  x: 0, y: 0, w: 4, h: 2
}
```

### Time-based Metric

```typescript
{
  id: 'avg-response',
  title: 'Response Time',
  query: JSON.stringify({
    measures: ['API.avgResponseTime'],
    timeDimensions: [{
      dimension: 'API.timestamp',
      dateRange: 'last 1 hour'
    }]
  }),
  chartType: 'kpiText',
  chartConfig: {
    yAxis: ['API.avgResponseTime']
  },
  displayConfig: {
    template: 'Average response: ${value}ms',
    decimals: 0
  },
  x: 0, y: 0, w: 4, h: 2
}
```

## Use Cases

- **Status Messages**: Create formatted status text with embedded values
- **Contextual Metrics**: Show numbers with descriptive text
- **Custom Labels**: Add units, context, or explanations to metrics
- **Alert Text**: Display warning/info messages with dynamic values
- **Summary Text**: Create readable summary statements

## Template Formatting

The `${value}` placeholder will be replaced with the formatted measure value:

```typescript
// Input measure: 1234.567

template: '${value} items'          // → "1,234.567 items" (default decimals: 0 → "1,235 items")
template: 'Total: $${value}'        // → "Total: $1,234.57" (decimals: 2)
template: '${value}% complete'      // → "1,234.57% complete" (decimals: 2)
template: 'Score: ${value}/100'     // → "Score: 1,235/100" (decimals: 0)
```

## Best Practices

1. **Keep templates short** - One or two sentences maximum
2. **Use clear language** - Make the text self-explanatory
3. **Position ${value} logically** - Where users expect to see the number
4. **Match decimals to data** - 0 for counts, 1-2 for percentages, 2 for currency
5. **Use colors meaningfully** - valueColorIndex for status indication
6. **Consider context** - Include units, timeframes, or qualifiers

## Common Patterns

```typescript
// Count pattern
{
  template: '${value} active users',
  decimals: 0
}

// Currency pattern
{
  template: 'Revenue: $${value}',
  decimals: 2
}

// Percentage pattern
{
  template: '${value}% uptime',
  decimals: 1
}

// Status pattern
{
  template: '⚠️ ${value} alerts pending',
  decimals: 0,
  valueColorIndex: 3
}

// Score pattern
{
  template: 'Quality score: ${value}/10',
  decimals: 1
}
```

## Related Skills

- Use `kpi-number` for standalone numeric values without text template
- Use `kpi-delta` for showing trends and changes
- Use `queries` skill for calculated measures
