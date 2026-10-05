---
name: syncfusion-vue-charts
description: Implement interactive data visualization charts in Vue applications using Syncfusion Chart component. Always guide when users need to visualize data, create dashboards, display metrics, build analytics interfaces, or render multiple data series. Immediately assists with chart types, axes, legend, tooltips, customization, interactivity, and dynamic data updates.
metadata:
  author: "Syncfusion Inc"
  category: "Data Visualization"
  version: "34.1.29"
---

# Implementing Syncfusion Vue Charts

## When to Use This Skill

This skill helps you whenever you need to:
- **Visualize data** in interactive charts (sales, metrics, performance)
- **Create dashboards** with multiple chart types and series
- **Display analytics** with real-time or dynamic data
- **Build interactive interfaces** with zooming, selection, and events
- **Customize chart appearance** with themes, colors, and styling
- **Export or print** charts from your application

## What is the Vue Chart Component?

The Syncfusion Vue Chart is a powerful, interactive data visualization component that transforms raw data into meaningful visual insights. It supports 35+ chart types (line, column, area, pie, financial, specialized), with features like legends, tooltips, data labels, annotations, zooming, and export capabilities.

**Key Strengths:**
- 35+ chart types for any data scenario
- Multi-series support with synchronized rendering
- Interactive features (zoom, pan, selection, crosshair)
- Export to PDF/PNG/SVG and print functionality
- Real-time data updates without re-rendering the entire chart
- Accessibility and localization support
- Vue 2 and Vue 3 compatibility (with Composition and Options API)

## Quick Start: Your First Chart

Here's the minimal setup to render a chart in Vue 3 (Composition API):

```vue
<template>
  <div>
    <ejs-chart id="container" :title="chartTitle">
      <e-series-collection>
        <e-series :dataSource="chartData" type="Column" xName="month" yName="sales" name="Sales">
        </e-series>
      </e-series-collection>
    </ejs-chart>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ChartComponent as EjsChart, SeriesCollectionDirective as ESeriesCollection, SeriesDirective as ESeries, ColumnSeries, Category } from "@syncfusion/ej2-vue-charts";
import { provide } from "vue";

const chartTitle = "Monthly Sales";
const chartData = [
  { month: "Jan", sales: 21 },
  { month: "Feb", sales: 28 },
  { month: "Mar", sales: 15 },
  { month: "Apr", sales: 32 }
];

provide("chart", [ColumnSeries, Category]);
</script>

<style>
#container {
  height: 350px;
}
</style>
```

## Key Concepts at a Glance

| Concept | What It Does | When You Need It |
|---------|--------------|------------------|
| **Series** | Groups of data points plotted on the chart | Always (defines what data is visualized) |
| **Chart Type** | The visual representation (line, column, pie, etc.) | Choosing how to display your data |
| **Axes** | X-axis (categories/values) and Y-axis (values) | Labeling and scaling data |
| **Legend** | Identifies each series with color/shape | Multiple series (helps users distinguish them) |
| **Tooltip** | Shows data on hover | Providing contextual information |
| **Data Label** | Text displayed on data points | Showing exact values directly on chart |
| **Annotation** | Text, shapes, or images overlaid on chart | Highlighting key insights or areas |
| **Events** | Respond to user interactions (click, hover, zoom) | Building interactive features |

## Documentation and Navigation Guide

### 🔗 API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

- Property Index
- Properties
- Data Models
- Events
- Methods
- Enums
- Child Directives
- Modules
- Common Usage Patterns
- Additional Resources

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm packages
- Vue 2 vs Vue 3 setup differences
- Module registration and imports
- First chart implementation
- Common setup troubleshooting

### Chart Types and Series Configuration
📄 **Read:** [references/chart-types-and-series.md](references/chart-types-and-series.md)
- Understanding the series concept
- Basic chart types (line, column, bar, area)
- Financial charts (candle, HLOC, renko)
- Specialized charts (pie, polar, radar, bubble)
- Multiple series on the same chart
- Dynamically changing chart types

### Axes, Labels, and Scales
📄 **Read:** [references/axes-and-scale.md](references/axes-and-scale.md)
- X-axis types (category, numeric, datetime)
- Y-axis configuration and scaling
- Axis labels, formatting, and rotation
- Multiple Y-axes on one chart
- Logarithmic and date-time scales
- Customizing axis appearance

### Legend, Tooltip, and Crosshair
📄 **Read:** [references/legend-and-tooltips.md](references/legend-and-tooltips.md)
- Legend positioning and styling
- Toggling series visibility via legend
- Tooltip templates and formatting
- Custom tooltip rendering
- Crosshair and trackball features
- Responsive legend behavior

### Data Labels and Annotations
📄 **Read:** [references/data-labels-and-annotations.md](references/data-labels-and-annotations.md)
- Data label positioning and formatting
- Label templates for custom content
- Chart annotations (text, shapes, images)
- Annotation positioning and styling
- Dynamic updates to labels and annotations

### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- Color palettes and predefined themes
- CSS variables for customization
- Font and text styling
- Chart sizing and responsive behavior
- Gradient fills and border styling
- Advanced CSS customization

### Interactions and Events
📄 **Read:** [references/interactions-and-events.md](references/interactions-and-events.md)
- Selection modes (series, point, range)
- Zooming and panning configurations
- Synchronized charts (linked interaction)
- Event system (pointRender, seriesRender, etc.)
- Drag and drop interactions
- Click and double-click handlers

### Export and Data Management
📄 **Read:** [references/export-and-data-management.md](references/export-and-data-management.md)
- Exporting charts to PDF, PNG, SVG
- Print functionality
- Dynamic data updates and binding
- Real-time data streams
- Performance optimization with large datasets
- Troubleshooting data issues

## Common Patterns

### Pattern 1: Basic Chart with Multiple Series
```vue
<e-series-collection>
  <e-series :dataSource="data" type="Column" xName="category" yName="value1" name="Series 1"></e-series>
  <e-series :dataSource="data" type="Column" xName="category" yName="value2" name="Series 2"></e-series>
</e-series-collection>
```
**When to use:** Comparing multiple related metrics (sales vs profit, actual vs target, etc.)

### Pattern 2: Customize Appearance
```vue
<ejs-chart :palettes="customColors" :legendSettings="{ position: 'Top' }">
```
**When to use:** Matching brand colors or specific UI design requirements

### Pattern 3: Handle Events
```vue
<ejs-chart @pointRender="onPointRender" @tooltipRender="onTooltipRender">
```
**When to use:** Custom logic based on user interactions or data changes

### Pattern 4: Real-Time Data Updates
```vue
// Update series data without re-rendering entire chart
chartInstance.series[0].dataSource = newData;
chartInstance.refresh();
```
**When to use:** Live dashboards, monitoring, streaming data

## Vue 2 vs Vue 3 Comparison

| Feature | Vue 2 | Vue 3 |
|---------|-------|-------|
| **Setup** | `vue create` + Vue CLI | Vite (recommended) |
| **Composition** | Options API | Composition API or Options API |
| **Import Style** | `Vue` global or import | Named imports from packages |
| **Template** | Standard Vue 2 template | Same as Vue 2 |
| **Event Handling** | `@event="method"` | Same as Vue 2 |
| **Directives** | `v-for`, `v-if`, etc. | Same as Vue 2 |

**Recommendation:** Start with Vue 3 for new projects. Vue 2 support is maintained but reached end-of-life in Dec 2023.

## Quick API Reference

### Essential Component Properties
```vue
<!-- Main chart configuration -->
<template>
  <ejs-chart
    :title="Sales Data"
    :primaryXAxis="primaryXAxis"
    :primaryYAxis="primaryYAxis"
    :legendSettings="legendSettings"
    :tooltip="tooltip"
    :zoomSettings="zoomSettings"
    :selectionMode="Point"
    :seriesRender="onSeriesRender"
    :pointRender="onPointRender"
    :tooltipRender="onTooltipRender"
  >
  </ejs-chart>
<template>

<script setup>
const primaryXAxis = { valueType: 'Category' };
const primaryYAxis = { valueType: 'Double' };
const legendSettings = { visible: true, position: 'Top' };
const tooltip = { enable: true };
const zoomSettings = { enableMouseWheelZooming: true };
const onSeriesRender = function (args) {};
const onPointRender = function (args) {};
const onTooltipRender = function (args) {};
</script>
```

### Essential Series Properties
```vue
<template>
  <e-series
    :dataSource="data"
    type="Column"
    xName="category"
    yName="value"
    name="Sales"
    :marker="marker"
  />
<template> 

<script setup>
const data = [
  { x: 'John', y: 10000 },
  { x: 'Jake', y: 12000 },
  { x: 'Peter', y: 18000 },
  { x: 'James', y: 11000 },
  { x: 'Mary', y: 9700 }
];
const marker = { visible: true, dataLabel: { visible: true } };
</script>
```

### Essential Methods
```vue
// Get chart instance
const chart = document.getElementById("container").ej2_instances[0];

// Manage series
chart.addSeries([seriesConfig]);     // Add new series
chart.addPoint({seriesConfig});     // Add new point
chart.removeSeries(0);                // Remove by index
chart.removePoint(0);                // Remove by index
chart.clearSeries();                  // Remove all
chart.setData(newData, 1000)          // Replace entire daatsource

// Export and print
chart.exportModule.export('PNG', 'chart.png');    // Export to PNG
chart.exportModule.export('PDF', 'report.pdf');   // Export to PDF
chart.value.print();                        // Print chart

// Tooltips and crosshair
chart.showTooltip(args.x, args.y);    // Show tooltip
chart.hideTooltip();                  // Hide tooltip
chart.showCrosshair(args.x, args.y);           // Show crosshair
chart.hideCrosshair();                // Hide crosshair
```

### Essential Events
```vue
<ejs-chart
  :load="onLoad"                        // Before chart loads
  :seriesRender="onSeriesRender"       // Before series renders
  :pointRender="onPointRender"         // Before each point renders
  :tooltipRender="onTooltipRender"     // Before tooltip shows
  :pointClick="onPointClick"           // When point clicked
  :legendClick="onLegendClick"         // When legend item clicked
  :zoomComplete="onZoomComplete"       // After zoom completes
>
</ejs-chart>
```

For complete API reference, see: **[API Reference](references/api-reference.md)**

## Next Steps

1. **Start here:** [Getting Started](references/getting-started.md) - Set up your first chart
2. **Choose chart type:** [Chart Types](references/chart-types-and-series.md) - Pick the right visualization
3. **Explore APIs:** [API Reference](references/api-reference.md) - Detailed property/method/event documentation
4. **Add interactivity:** [Events & Interactions](references/interactions-and-events.md) - Respond to user actions
5. **Polish appearance:** [Customization](references/customization-and-styling.md) - Style to match your app
6. **Export or print:** [Export & Management](references/export-and-data-management.md) - Share or archive data

---

**🎯 Ready to create your chart?** Start with [Getting Started](references/getting-started.md)

**📚 Need API details?** Check [API Reference](references/api-reference.md)
