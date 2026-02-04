---
name: bar-chart
description: Configure bar and column charts in drizzle-cube dashboards with stacking, orientation, and grouping options. Use when creating bar charts, column charts, stacked bars, horizontal bars, or grouped bar visualizations.
---

# Bar Chart Configuration

Configure bar and column charts for drizzle-cube dashboards. Bar charts display categorical data with rectangular bars, supporting vertical/horizontal orientation, stacking, and grouping.

## Chart Type

```typescript
chartType: 'bar'
```

## Basic Configuration

```typescript
{
  id: 'bar-chart-1',
  title: 'Employees by Department',
  query: JSON.stringify({
    measures: ['Employees.count'],
    dimensions: ['Departments.name']
  }),
  chartType: 'bar',
  chartConfig: {
    xAxis: ['Departments.name'],  // Category axis
    yAxis: ['Employees.count']     // Value axis
  },
  displayConfig: {
    orientation: 'vertical'         // or 'horizontal'
  },
  x: 0, y: 0, w: 6, h: 4
}
```

## Chart Configuration (`chartConfig`)

### xAxis (Categories)
- **Type**: `string[]`
- **Purpose**: Dimensions to display on category axis
- **Example**: `['Departments.name']`

### yAxis (Values)
- **Type**: `string[]`
- **Purpose**: Measures to display as bar heights/lengths
- **Example**: `['Employees.count', 'Employees.avgSalary']`

### series (Grouping)
- **Type**: `string[]`
- **Purpose**: Dimension to split into multiple series/bars
- **Example**: `['Employees.isActive']`

## Display Configuration (`displayConfig`)

### orientation
- **Type**: `'vertical' | 'horizontal'`
- **Default**: `'vertical'`
- **Purpose**: Bar direction
- **Vertical**: Bars extend upward (column chart)
- **Horizontal**: Bars extend rightward

### stacked
- **Type**: `boolean`
- **Default**: `false`
- **Purpose**: Stack multiple series or measures

### showLegend
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Display chart legend

### showGrid
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Show gridlines

### showTooltip
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Show tooltips on hover

### colors
- **Type**: `string[]`
- **Default**: Uses palette colors
- **Purpose**: Custom bar colors

## Examples

### Simple Vertical Bar Chart

```typescript
{
  id: 'simple-bar',
  title: 'Sales by Region',
  query: JSON.stringify({
    measures: ['Sales.totalRevenue'],
    dimensions: ['Sales.region'],
    order: { 'Sales.totalRevenue': 'desc' }
  }),
  chartType: 'bar',
  chartConfig: {
    xAxis: ['Sales.region'],
    yAxis: ['Sales.totalRevenue']
  },
  displayConfig: {
    orientation: 'vertical',
    showLegend: false
  },
  x: 0, y: 0, w: 6, h: 4
}
```

### Horizontal Bar Chart

```typescript
{
  id: 'horizontal-bar',
  title: 'Top 10 Products by Revenue',
  query: JSON.stringify({
    measures: ['Orders.totalRevenue'],
    dimensions: ['Products.name'],
    order: { 'Orders.totalRevenue': 'desc' },
    limit: 10
  }),
  chartType: 'bar',
  chartConfig: {
    xAxis: ['Products.name'],
    yAxis: ['Orders.totalRevenue']
  },
  displayConfig: {
    orientation: 'horizontal', // Horizontal bars
    showLegend: false
  },
  x: 0, y: 0, w: 6, h: 6
}
```

### Grouped Bar Chart (Multiple Measures)

```typescript
{
  id: 'grouped-measures',
  title: 'Employee Metrics by Department',
  query: JSON.stringify({
    measures: ['Employees.count', 'Employees.avgSalary'],
    dimensions: ['Departments.name']
  }),
  chartType: 'bar',
  chartConfig: {
    xAxis: ['Departments.name'],
    yAxis: ['Employees.count', 'Employees.avgSalary'] // Multiple measures
  },
  displayConfig: {
    orientation: 'vertical',
    showLegend: true // Show which bar is which measure
  },
  x: 0, y: 0, w: 8, h: 4
}
```

### Grouped Bar Chart (Series Split)

```typescript
{
  id: 'grouped-series',
  title: 'Active vs Inactive Employees',
  query: JSON.stringify({
    measures: ['Employees.count'],
    dimensions: ['Departments.name', 'Employees.isActive']
  }),
  chartType: 'bar',
  chartConfig: {
    xAxis: ['Departments.name'],
    yAxis: ['Employees.count'],
    series: ['Employees.isActive'] // Split by active status
  },
  displayConfig: {
    orientation: 'vertical',
    showLegend: true
  },
  x: 0, y: 0, w: 8, h: 4
}
```

### Stacked Bar Chart

```typescript
{
  id: 'stacked-bar',
  title: 'Employee Distribution',
  query: JSON.stringify({
    measures: ['Employees.count'],
    dimensions: ['Departments.name', 'Employees.seniorityLevel']
  }),
  chartType: 'bar',
  chartConfig: {
    xAxis: ['Departments.name'],
    yAxis: ['Employees.count'],
    series: ['Employees.seniorityLevel']
  },
  displayConfig: {
    orientation: 'vertical',
    stacked: true, // Stack series
    showLegend: true
  },
  x: 0, y: 0, w: 8, h: 4
}
```

### Time-Based Bar Chart

```typescript
{
  id: 'monthly-signups',
  title: 'Monthly User Signups',
  query: JSON.stringify({
    measures: ['Users.count'],
    timeDimensions: [{
      dimension: 'Users.createdAt',
      granularity: 'month',
      dateRange: 'last 12 months'
    }]
  }),
  chartType: 'bar',
  chartConfig: {
    xAxis: ['Users.createdAt'],
    yAxis: ['Users.count']
  },
  displayConfig: {
    orientation: 'vertical',
    showGrid: true
  },
  x: 0, y: 0, w: 12, h: 4
}
```

### Custom Colors

```typescript
{
  id: 'custom-colors',
  title: 'Department Performance',
  query: JSON.stringify({
    measures: ['Employees.count'],
    dimensions: ['Departments.name']
  }),
  chartType: 'bar',
  chartConfig: {
    xAxis: ['Departments.name'],
    yAxis: ['Employees.count']
  },
  displayConfig: {
    orientation: 'vertical',
    colors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
  },
  x: 0, y: 0, w: 6, h: 4
}
```

## Use Cases

- **Category Comparisons**: Compare values across different categories
- **Rankings**: Show top/bottom performers
- **Distribution**: Display data distribution across groups
- **Time Series**: Visualize data over time periods
- **Multi-Metric Comparison**: Compare multiple measures side-by-side
- **Composition**: Show part-to-whole relationships (stacked)

## Best Practices

1. **Limit categories** - Too many bars make charts hard to read (max 15-20)
2. **Use horizontal for long labels** - Easier to read category names
3. **Sort data** - Order by value for better insights
4. **Choose stacked vs grouped wisely** - Stacked for totals, grouped for comparison
5. **Keep colors consistent** - Use same colors for same categories across charts
6. **Add meaningful titles** - Clear title explains what's being shown

## Common Patterns

```typescript
// Top N pattern
{
  query: JSON.stringify({
    measures: ['Metric'],
    dimensions: ['Category'],
    order: { 'Metric': 'desc' },
    limit: 10
  })
}

// Comparison pattern
{
  query: JSON.stringify({
    measures: ['Metric1', 'Metric2'],
    dimensions: ['Category']
  }),
  chartConfig: {
    yAxis: ['Metric1', 'Metric2']
  }
}

// Time series pattern
{
  query: JSON.stringify({
    measures: ['Metric'],
    timeDimensions: [{
      dimension: 'Date',
      granularity: 'month'
    }]
  })
}
```

## Related Skills

- Use `queries` skill to build complex bar chart queries
- Use `dashboard` skill to add bar charts to dashboards
- Consider `line-chart` for continuous data trends
- Consider `pie-chart` for part-to-whole relationships
