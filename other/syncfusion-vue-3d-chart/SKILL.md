---
name: syncfusion-vue-3d-chart
description: Implementing Syncfusion Vue 3D Chart component for interactive 3D data visualization. Use this skill ALWAYS when user needs to create 3D charts, visualize data in 3D columns/bars, customize 3D chart axes, configure 3D chart types, style 3D chart appearance, implement user interactions like tooltips and selection, or export/print 3D charts. Essential for displaying multidimensional data with rotation, perspective, and enhanced visual appeal.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue 3D Chart Component

The Syncfusion Vue 3D Chart component enables developers to create interactive, immersive 3D data visualizations. Perfect for displaying complex datasets with enhanced spatial awareness through 3D columns, bars, and stacked variations.

## When to Use This Skill

Use this skill when the user needs to:
- **Create 3D visualizations**: Build interactive 3D column charts, bar charts, or stacked variants
- **Visualize multidimensional data**: Display data across multiple axes with depth perception
- **Customize appearance**: Configure colors, legends, labels, and chart dimensions
- **Handle user interactions**: Implement tooltips, selection, rotation, and perspective controls
- **Configure axes**: Set up category, numeric, date-time, or logarithmic axes with customization
- **Export or print**: Generate PNG, JPEG, SVG, or PDF outputs of 3D charts

## Component Overview

The 3D Chart component transforms standard 2D charts into immersive 3D visualizations, providing:
- **Multiple 3D Chart Types**: Column, Bar, and Stacked variants
- **Advanced Axis Configuration**: Category, Numeric, Date-Time, and Logarithmic axes
- **Rich Customization**: Colors, themes, legends, tooltips, labels, and dimensions
- **User Interactions**: Rotation, selection, hover effects, and perspective control
- **Export Capabilities**: Multi-format export (PNG, JPEG, SVG, PDF) and printing

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and dependencies
- Basic 3D chart setup and component registration
- Data binding and minimal example
- CSS imports and theme setup
- **When:** Start here to set up your first 3D chart

### Chart Types
📄 **Read:** [references/chart-types.md](references/chart-types.md)
- Column 3D, Bar 3D chart implementation
- Stacked Column 3D and Stacked Bar 3D variants
- Comparing different chart type use cases
- Code examples with sample data
- **When:** Need to choose or implement a specific 3D chart type

### Axis Configuration
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)
- Configuring category, numeric, and date-time axes
- Adding axis titles and customizing labels
- Multiple panes and axis positioning
- Logarithmic axis setup
- **When:** Customizing axes for specific data requirements

### Appearance and Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Theming and color schemes
- Legend styling and positioning
- Chart dimensions and sizing
- Label and tooltip formatting
- **When:** Styling the chart appearance and visual behavior

### Interactions and Features
📄 **Read:** [references/interactions-features.md](references/interactions-features.md)
- Tooltip configuration and styling
- Selection functionality and events
- User interaction modes (rotation, perspective)
- Handling chart events
- **When:** Implementing user interactions or advanced features

### Print and Export
📄 **Read:** [references/print-export.md](references/print-export.md)
- Export to image formats (PNG, JPEG, SVG)
- PDF export functionality
- Print chart directly
- **When:** Users need to export or print chart data

---

## Quick Start Example

Here's a minimal setup to create a 3D Column Chart:

```vue
<template>
  <div id="app">
    <ejs-chart3d id="chart">
      <e-chart3d-series-collection>
        <e-chart3d-series :dataSource="chartData" type="Column" xName="month" yName="sales" name="Sales">
        </e-chart3d-series>
      </e-chart3d-series-collection>
    </ejs-chart3d>
  </div>
</template>

<script>
import { 
  Chart3DComponent, 
  Chart3DSeriesCollectionDirective, 
  Chart3DSeriesDirective,
  ColumnSeries3D,
  Category3D
} from '@syncfusion/ej2-vue-charts';

export default {
  components: {
    'ejs-chart3d': Chart3DComponent,
    'e-chart3d-series-collection': Chart3DSeriesCollectionDirective,
    'e-chart3d-series': Chart3DSeriesDirective
  },
  data() {
    return {
      chartData: [
        { month: 'Jan', sales: 35 },
        { month: 'Feb', sales: 28 },
        { month: 'Mar', sales: 34 },
        { month: 'Apr', sales: 32 },
        { month: 'May', sales: 40 }
      ]
    };
  },
  provide: {
    chart3d: [ColumnSeries3D, Category3D]
  }
};
</script>

<style>
#chart {
  width: 100%;
  height: 400px;
}
</style>
```

---

## Common Patterns

### Pattern 1: Multi-Series 3D Column Chart
Display multiple data series in a single 3D chart:

```vue
<e-chart3d-series-collection>
  <e-chart3d-series :dataSource="data" type="Column" xName="month" yName="sales" name="Sales"></e-chart3d-series>
  <e-chart3d-series :dataSource="data" type="Column" xName="month" yName="revenue" name="Revenue"></e-chart3d-series>
</e-chart3d-series-collection>
```

**Use when:** You need to compare multiple metrics across categories in 3D perspective.

### Pattern 2: Stacked Data Visualization
Stack multiple series to show cumulative totals:

```vue
<e-chart3d-series type="StackingColumn3D" xName="country" yName="gold"></e-chart3d-series>
```

**Use when:** Displaying parts of a whole across categories (e.g., medal counts by type).

### Pattern 3: Custom Axis Configuration
Configure axes to match specific data ranges and labels:

```vue
<ejs-chart3d :primaryXAxis="xAxis" :primaryYAxis="yAxis">
  <!-- series collection -->
</ejs-chart3d>

data() {
  return {
    xAxis: { valueType: 'Category', labelFormat: '{value}' },
    yAxis: { labelFormat: '{value}K', minimum: 0, maximum: 100 }
  };
}
```

**Use when:** Custom axis ranges, formatting, or label positioning is needed.

### Pattern 4: Dynamic Tooltip Display
Show contextual information on hover:

```vue
<ejs-chart3d :tooltip="tooltip">
  <!-- series collection -->
</ejs-chart3d>

data() {
  return {
    tooltip: { enable: true, format: '${point.x}: $${point.y}K' }
  };
}
```

**Use when:** Users need contextual data on interaction (hover over data points).

---

## Key Props

| Prop | Type | Purpose | Example |
|------|------|---------|---------|
| `type` | String | Series chart type (Column, Bar, StackingColumn3D, StackingBar3D) | `type="Column"` |
| `xName` | String | Maps x-axis data from data source | `xName="month"` |
| `yName` | String | Maps y-axis data from data source | `yName="sales"` |
| `dataSource` | Array | Chart data array | `:dataSource="chartData"` |
| `name` | String | Series display name in legend | `name="Sales"` |
| `:tooltip` | Object | Tooltip configuration | `:tooltip="{ enable: true }"` |
| `:primaryXAxis` | Object | X-axis configuration | `:primaryXAxis="xAxisConfig"` |
| `:primaryYAxis` | Object | Y-axis configuration | `:primaryYAxis="yAxisConfig"` |

---

## Common Use Cases

**Use Case 1: Sales Performance Dashboard**
Create a 3D stacked column chart showing revenue breakdown by product category and month. Users interact via tooltips and rotate the chart for better perspective.

**Use Case 2: Analytics Comparison**
Compare metrics across multiple dimensions using 3D column charts with custom axes, legends, and export capability for reports.

**Use Case 3: Financial Data Visualization**
Display financial trends with date-time axes on 3D charts, enabling users to identify patterns through rotation and perspective.

**Use Case 4: Quality Metrics**
Visualize quality metrics stacked by defect type, with tooltips showing detailed breakdown and export-to-PDF for compliance documentation.

---

## Next Steps

1. **Start here:** Read [references/getting-started.md](references/getting-started.md) to set up your first 3D chart
2. **Choose chart type:** Review [references/chart-types.md](references/chart-types.md) for available options
3. **Customize as needed:** Check other references based on your specific requirements
4. **Export:** Use [references/print-export.md](references/print-export.md) when ready to generate outputs
