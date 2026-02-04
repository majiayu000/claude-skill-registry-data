---
name: bubble-chart
description: Configure bubble charts in drizzle-cube dashboards for three-variable analysis with size and color dimensions. Use when creating bubble charts, multi-variable visualizations, or comparing three metrics simultaneously.
---

# Bubble Chart Configuration

Configure bubble charts for drizzle-cube dashboards. Bubble charts display three dimensions of data: X position, Y position, and bubble size (optionally color).

## Chart Type

```typescript
chartType: 'bubble'
```

## Basic Configuration

```typescript
{
  id: 'bubble-1',
  title: 'Product Performance',
  query: JSON.stringify({
    dimensions: [
      'Products.name',
      'Products.price',
      'Products.rating'
    ],
    measures: ['Products.salesVolume']
  }),
  chartType: 'bubble',
  chartConfig: {
    xAxis: ['Products.price'],
    yAxis: ['Products.rating'],
    sizeField: ['Products.salesVolume'],
    series: ['Products.name']  // Required for bubble labels
  },
  x: 0, y: 0, w: 10, h: 6
}
```

## Chart Configuration (`chartConfig`)

### xAxis (X Position)
- **Type**: `string[]`
- **Purpose**: Dimension/measure for X axis
- **Example**: `['Products.price']`

### yAxis (Y Position)
- **Type**: `string[]`
- **Purpose**: Dimension/measure for Y axis
- **Example**: `['Products.rating']`

### series (Bubble Labels)
- **Type**: `string[]`
- **Required**: Yes
- **Max Items**: 1
- **Purpose**: Dimension for bubble labels
- **Example**: `['Products.name']`

### sizeField (Bubble Size)
- **Type**: `string[]`
- **Required**: Yes
- **Max Items**: 1
- **Purpose**: Measure determining bubble size
- **Example**: `['Products.salesVolume']`

### colorField (Bubble Color)
- **Type**: `string[]`
- **Optional**: Yes
- **Max Items**: 1
- **Purpose**: Dimension for color grouping
- **Example**: `['Products.category']`

## Display Configuration (`displayConfig`)

### minBubbleSize
- **Type**: `number`
- **Default**: `5`
- **Purpose**: Minimum bubble radius

### maxBubbleSize
- **Type**: `number`
- **Default**: `20`
- **Purpose**: Maximum bubble radius

### showLegend
- **Type**: `boolean`
- **Default**: `true`

## Examples

### Simple Bubble Chart

```typescript
{
  id: 'market-analysis',
  title: 'Market Position Analysis',
  query: JSON.stringify({
    dimensions: [
      'Products.name',
      'Products.marketShare',
      'Products.growthRate'
    ],
    measures: ['Products.revenue']
  }),
  chartType: 'bubble',
  chartConfig: {
    xAxis: ['Products.marketShare'],
    yAxis: ['Products.growthRate'],
    sizeField: ['Products.revenue'],
    series: ['Products.name']
  },
  displayConfig: {
    minBubbleSize: 10,
    maxBubbleSize: 50
  },
  x: 0, y: 0, w: 12, h: 7
}
```

### Bubble Chart with Color

```typescript
{
  id: 'employee-analysis',
  title: 'Employee Performance & Satisfaction',
  query: JSON.stringify({
    dimensions: [
      'Employees.name',
      'Employees.performance',
      'Employees.satisfaction',
      'Departments.name'
    ],
    measures: ['Employees.tenure']
  }),
  chartType: 'bubble',
  chartConfig: {
    xAxis: ['Employees.performance'],
    yAxis: ['Employees.satisfaction'],
    sizeField: ['Employees.tenure'],
    series: ['Employees.name'],
    colorField: ['Departments.name']
  },
  displayConfig: {
    showLegend: true,
    minBubbleSize: 8,
    maxBubbleSize: 40
  },
  x: 0, y: 0, w: 12, h: 8
}
```

## Use Cases

- **Multi-Variable Analysis**: Compare 3-4 dimensions
- **Portfolio Analysis**: Evaluate product/project portfolios
- **Performance Quadrants**: Map performance vs satisfaction
- **Market Positioning**: Analyze competitive position

## Related Skills

- Use `scatter-chart` for two-variable analysis
- Use `queries` skill for complex data queries
