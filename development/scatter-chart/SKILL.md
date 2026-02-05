---
name: scatter-chart
description: Configure scatter plots in drizzle-cube dashboards for correlation and distribution analysis. Use when creating scatter plots, correlation charts, or distribution visualizations.
---

# Scatter Chart Configuration

Configure scatter plots for drizzle-cube dashboards. Scatter charts show relationships between two variables, revealing correlations and distributions.

## Chart Type

```typescript
chartType: 'scatter'
```

## Basic Configuration

```typescript
{
  id: 'scatter-1',
  title: 'Salary vs Experience',
  query: JSON.stringify({
    dimensions: [
      'Employees.yearsOfService',
      'Employees.salary',
      'Employees.name'
    ]
  }),
  chartType: 'scatter',
  chartConfig: {
    xAxis: ['Employees.yearsOfService'],
    yAxis: ['Employees.salary']
  },
  x: 0, y: 0, w: 8, h: 5
}
```

## Chart Configuration (`chartConfig`)

### xAxis (X Variable)
- **Type**: `string[]`
- **Purpose**: Dimension/measure for X axis
- **Example**: `['Employees.yearsOfService']`

### yAxis (Y Variable)
- **Type**: `string[]`
- **Purpose**: Dimension/measure for Y axis
- **Example**: `['Employees.salary']`

### series (Grouping)
- **Type**: `string[]`
- **Purpose**: Dimension for color grouping
- **Example**: `['Departments.name']`

## Examples

### Correlation Analysis

```typescript
{
  id: 'price-demand',
  title: 'Price vs Demand',
  query: JSON.stringify({
    dimensions: [
      'Products.price',
      'Products.unitsSold',
      'Products.name'
    ]
  }),
  chartType: 'scatter',
  chartConfig: {
    xAxis: ['Products.price'],
    yAxis: ['Products.unitsSold']
  },
  x: 0, y: 0, w: 8, h: 5
}
```

### Multi-Category Scatter

```typescript
{
  id: 'performance-scatter',
  title: 'Performance by Department',
  query: JSON.stringify({
    dimensions: [
      'Employees.productivity',
      'Employees.satisfaction',
      'Employees.name',
      'Departments.name'
    ]
  }),
  chartType: 'scatter',
  chartConfig: {
    xAxis: ['Employees.productivity'],
    yAxis: ['Employees.satisfaction'],
    series: ['Departments.name']
  },
  displayConfig: {
    showLegend: true
  },
  x: 0, y: 0, w: 10, h: 6
}
```

## Use Cases

- **Correlation Analysis**: Find relationships between variables
- **Distribution Patterns**: Identify clustering
- **Outlier Detection**: Spot anomalies
- **Multi-Variable Comparison**: Compare multiple factors

## Related Skills

- Use `bubble-chart` for three-variable analysis
- Use `line-chart` for trend analysis
