---
name: pie-chart
description: Configure pie and doughnut charts in drizzle-cube dashboards for part-to-whole relationships and proportions. Use when creating pie charts, doughnut charts, or percentage visualizations.
---

# Pie Chart Configuration

Configure pie and doughnut charts for drizzle-cube dashboards. Pie charts display proportions and percentages, showing how parts contribute to a whole.

## Chart Type

```typescript
chartType: 'pie'
```

## Basic Configuration

```typescript
{
  id: 'pie-chart-1',
  title: 'Sales by Category',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue'],
    dimensions: ['Products.category']
  }),
  chartType: 'pie',
  chartConfig: {
    xAxis: ['Products.category'],  // Slices
    yAxis: ['Sales.totalRevenue']   // Size of slices
  },
  displayConfig: {
    showLegend: true
  },
  x: 0, y: 0, w: 6, h: 4
}
```

## Chart Configuration (`chartConfig`)

### xAxis (Categories)
- **Type**: `string[]`
- **Required**: Yes
- **Max Items**: 1
- **Purpose**: Dimension creating pie slices
- **Example**: `['Products.category']`

### yAxis (Values)
- **Type**: `string[]`
- **Required**: Yes
- **Max Items**: 1
- **Purpose**: Measure determining slice size
- **Example**: `['Sales.revenue']`

## Display Configuration (`displayConfig`)

### showLegend
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Display slice labels

### showTooltip
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Show values on hover

### colors
- **Type**: `string[]`
- **Purpose**: Custom slice colors

## Examples

### Simple Pie Chart

```typescript
{
  id: 'employee-distribution',
  title: 'Employees by Department',
  query: JSON.stringify({
    measures: ['Employees.count'],
    dimensions: ['Departments.name']
  }),
  chartType: 'pie',
  chartConfig: {
    xAxis: ['Departments.name'],
    yAxis: ['Employees.count']
  },
  displayConfig: {
    showLegend: true
  },
  x: 0, y: 0, w: 6, h: 4
}
```

### Market Share

```typescript
{
  id: 'market-share',
  title: 'Market Share by Product',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue'],
    dimensions: ['Products.name'],
    order: { 'Sales.totalRevenue': 'desc' },
    limit: 5  // Top 5 products
  }),
  chartType: 'pie',
  chartConfig: {
    xAxis: ['Products.name'],
    yAxis: ['Sales.totalRevenue']
  },
  displayConfig: {
    showLegend: true,
    colors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
  },
  x: 0, y: 0, w: 6, h: 5
}
```

### Status Distribution

```typescript
{
  id: 'order-status',
  title: 'Order Status Distribution',
  query: JSON.stringify({
    measures: ['Orders.count'],
    dimensions: ['Orders.status']
  }),
  chartType: 'pie',
  chartConfig: {
    xAxis: ['Orders.status'],
    yAxis: ['Orders.count']
  },
  displayConfig: {
    showLegend: true
  },
  x: 6, y: 0, w: 6, h: 4
}
```

## Use Cases

- **Proportions**: Show relative sizes of categories
- **Market Share**: Display competitive positions
- **Budget Allocation**: Visualize spending distribution
- **Status Distribution**: Show status breakdown
- **Category Composition**: Display categorical makeup
- **Simple Percentages**: When you have 3-7 categories

## Best Practices

1. **Limit slices** - Use 3-7 slices for best readability
2. **Order by size** - Largest to smallest for clarity
3. **Combine small slices** - Group tiny slices into "Other"
4. **Use contrasting colors** - Make slices distinguishable
5. **Include legend** - Show category names clearly
6. **Avoid for trends** - Use line charts instead

## Related Skills

- Use `queries` skill for aggregation queries
- Use `bar-chart` for comparing categories
- Use `treemap-chart` for hierarchical proportions
