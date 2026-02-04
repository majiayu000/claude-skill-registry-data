---
name: activity-grid
description: Configure activity grid heatmaps in drizzle-cube dashboards for GitHub-style contribution visualizations. Use when creating activity grids, heatmaps, contribution calendars, or daily activity patterns.
---

# Activity Grid Configuration

Configure activity grid (heatmap) charts for drizzle-cube dashboards. Activity grids display daily values in a calendar-like grid, similar to GitHub contribution graphs.

## Chart Type

```typescript
chartType: 'activityGrid'
```

## Basic Configuration

```typescript
{
  id: 'activity-1',
  title: 'Daily Contributions',
  query: JSON.stringify({
    measures: ['Activity.count'],
    timeDimensions: [{
      dimension: 'Activity.date',
      granularity: 'day',
      dateRange: 'last 12 months'
    }]
  }),
  chartType: 'activityGrid',
  chartConfig: {
    dateField: 'Activity.date',
    valueField: 'Activity.count'
  },
  displayConfig: {
    showLabels: true,
    fitToWidth: true
  },
  x: 0, y: 0, w: 12, h: 4
}
```

## Chart Configuration (`chartConfig`)

### dateField
- **Type**: `string`
- **Purpose**: Time dimension field
- **Example**: `'Activity.date'`

### valueField
- **Type**: `string`
- **Purpose**: Measure to display as cell intensity
- **Example**: `'Activity.count'`

## Display Configuration (`displayConfig`)

### showLabels
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Show month labels

### fitToWidth
- **Type**: `boolean`
- **Default**: `true`
- **Purpose**: Scale grid to container width

## Examples

### Developer Activity

```typescript
{
  id: 'dev-activity',
  title: 'Development Activity',
  query: JSON.stringify({
    measures: ['Commits.count'],
    timeDimensions: [{
      dimension: 'Commits.date',
      granularity: 'day',
      dateRange: 'last 365 days'
    }]
  }),
  chartType: 'activityGrid',
  chartConfig: {
    dateField: 'Commits.date',
    valueField: 'Commits.count'
  },
  displayConfig: {
    showLabels: true
  },
  x: 0, y: 0, w: 12, h: 3
}
```

### Sales Activity

```typescript
{
  id: 'sales-activity',
  title: 'Daily Sales Activity',
  query: JSON.stringify({
    measures: ['Orders.count'],
    timeDimensions: [{
      dimension: 'Orders.createdAt',
      granularity: 'day',
      dateRange: 'last 180 days'
    }]
  }),
  chartType: 'activityGrid',
  chartConfig: {
    dateField: 'Orders.createdAt',
    valueField: 'Orders.count'
  },
  x: 0, y: 4, w: 12, h: 3
}
```

## Use Cases

- **Contribution Tracking**: Developer/team activity
- **Habit Tracking**: Daily habit completion
- **Sales Patterns**: Identify busy/slow days
- **User Engagement**: Daily active users
- **Workload Visualization**: Task completion patterns

## Related Skills

- Use `line-chart` for trend analysis
- Use `queries` skill for daily aggregations
