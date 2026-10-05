---
name: syncfusion-vue-3d-circular-chart
description: Create interactive 3D pie and donut charts using Syncfusion Vue components. Use this skill whenever the user needs to visualize data as circular/pie charts with 3D perspective, create donut visualizations, add data labels to charts, customize chart legends, tooltips, empty points and animations. Trigger when user mentions 3D charts, pie charts, donut charts, circular visualizations, 3D pie, data visualization, chart rotation, chart interactivity, or circular types.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue 3D Circular Chart

The Syncfusion Vue 3D Circular Chart is a powerful component for visualizing hierarchical and proportional data through interactive pie and donut charts with 3D perspective effects. It supports customizable data labels, legends, tooltips, and advanced interactive features perfect for reports, dashboards, and data analysis applications.

## When to Use This Skill

- **Pie Chart Visualization**: When you need to display parts of a whole using pie charts
- **Donut Charts**: For ring-style visualizations with optional center content
- **Data Labels**: Adding contextual information directly on chart segments
- **Interactive Elements**: Tooltips, click handlers, and selection behaviors
- **Chart Customization**: Legends, colors, sizes, and 3D rotation effects
- **Data Binding**: Dynamic data sources with Vue reactivity
- **Advanced Features**: Empty point handling, animations, export to PDF/PNG

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Module registration and Vue 2 vs Vue 3 syntax
- Basic pie chart creation
- Your first 3D circular chart

### Pie & Donut Charts
📄 **Read:** [references/pie-and-donut.md](references/pie-and-donut.md)
- Pie chart rendering and configuration
- Donut charts with inner radius
- Radius customization and dynamic radii
- Color and text mapping

### Data Labels & Formatting
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling and positioning data labels
- Text formatting and templates
- Connector lines and styling
- Custom formatting with events

### Legend & Navigation
📄 **Read:** [references/legend-and-navigation.md](references/legend-and-navigation.md)
- Legend visibility and positioning
- Legend alignment and wrapping
- Click events and selection
- Legend customization

### Tooltips & Interactivity
📄 **Read:** [references/tooltips-and-interactivity.md](references/tooltips-and-interactivity.md)
- Tooltip enabling and customization
- Custom tooltip templates
- Point selection and events
- Point render and customization

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Empty point handling
- 3D view rotation (tilt angle)
- Animation configuration
- Print and export functionality

## Quick Start

### Basic Pie Chart (Vue 2)
```vue
<template>
  <div id="app">
    <ejs-circularchart3d id="container" title="Sales Data">
      <e-circularchart3d-series-collection>
        <e-circularchart3d-series :dataSource="seriesData" xName="x" yName="y"></e-circularchart3d-series>
      </e-circularchart3d-series-collection>
    </ejs-circularchart3d>
  </div>
</template>

<script>
import { CircularChart3DComponent, CircularChart3DSeriesCollectionDirective, CircularChart3DSeriesDirective, PieSeries3D } from '@syncfusion/ej2-vue-charts';

export default {
  components: {
    'ejs-circularchart3d': CircularChart3DComponent,
    'e-circularchart3d-series-collection': CircularChart3DSeriesCollectionDirective,
    'e-circularchart3d-series': CircularChart3DSeriesDirective
  },
  data() {
    return {
      seriesData: [
        { x: 'Product A', y: 35 },
        { x: 'Product B', y: 28 },
        { x: 'Product C', y: 34 },
        { x: 'Product D', y: 32 }
      ]
    };
  },
  provide: {
    circularchart3d: [PieSeries3D]
  }
};
</script>

<style>
#container {
  height: 350px;
}
</style>
```

### Basic Pie Chart (Vue 3)
```vue
<template>
  <div id="app">
    <ejs-circularchart3d id="container" title="Sales Data">
      <e-circularchart3d-series-collection>
        <e-circularchart3d-series :dataSource="seriesData" xName="x" yName="y"></e-circularchart3d-series>
      </e-circularchart3d-series-collection>
    </ejs-circularchart3d>
  </div>
</template>

<script setup>
import { provide } from 'vue';
import { CircularChart3DComponent as EjsCircularchart3d, CircularChart3DSeriesCollectionDirective as ECircularchart3dSeriesCollection, CircularChart3DSeriesDirective as ECircularchart3dSeries, PieSeries3D } from '@syncfusion/ej2-vue-charts';

const seriesData = [
  { x: 'Product A', y: 35 },
  { x: 'Product B', y: 28 },
  { x: 'Product C', y: 34 },
  { x: 'Product D', y: 32 }
];

provide('circularchart3d', [PieSeries3D]);
</script>

<style>
#container {
  height: 350px;
}
</style>
```

### Donut Chart with Labels
```vue
<template>
  <div id="app">
    <ejs-circularchart3d id="container" title="Market Share">
      <e-circularchart3d-series-collection>
        <e-circularchart3d-series 
          :dataSource="seriesData" 
          xName="x" 
          yName="y" 
          innerRadius="40%"
          :dataLabel="{ visible: true, position: 'Outside' }">
        </e-circularchart3d-series>
      </e-circularchart3d-series-collection>
    </ejs-circularchart3d>
  </div>
</template>
```

## Common Patterns

### Pattern 1: Enable Legend and Tooltip
```javascript
// In data() or setup
const legendSettings = {
  visible: true,
  position: 'Right'
};

const tooltip = {
  enable: true,
  format: '${point.x}: ${point.y}%'
};

// Register modules
provide('circularchart3d', [PieSeries3D, CircularChartLegend3D, CircularChartTooltip3D]);
```

### Pattern 2: Dynamic Data with Reactivity
```javascript
// Vue 2
data() {
  return {
    seriesData: [
      { x: 'Q1', y: 45, fill: '#498fff' },
      { x: 'Q2', y: 52, fill: '#ffa060' }
    ]
  };
}

// Update data
this.seriesData.push({ x: 'Q3', y: 38, fill: '#ff68b6' });
```

### Pattern 3: Point Customization Event
```javascript
pointRender(args) {
  // Customize individual points
  if (args.point.x === 'Q1') {
    args.fill = '#ff0000'; // Highlight specific segment
  }
}

// Provide event handler to chart
<ejs-circularchart3d :pointRender="pointRender">
```

### Pattern 4: Format Data Labels
```javascript
const dataLabel = {
  visible: true,
  name: 'text',
  format: 'n2', // 2 decimal places
  position: 'Inside'
};
```

## Key Modules & Series

### Essential Module: PieSeries3D
```javascript
import { PieSeries3D } from '@syncfusion/ej2-vue-charts';
provide('circularchart3d', [PieSeries3D]);
```

### Additional Modules (As Needed)
| Module | Purpose |
|--------|---------|
| `CircularChartDataLabel3D` | Enable data labels |
| `CircularChartLegend3D` | Display legend |
| `CircularChartTooltip3D` | Show tooltips on hover |

## Core Props Quick Reference

| Property | Type | Purpose |
|----------|------|---------|
| `dataSource` | Array | Data points for the chart |
| `xName` | String | Data field for x values (category) |
| `yName` | String | Data field for y values (numeric) |
| `radius` | String | Pie radius (e.g., '80%') |
| `innerRadius` | String | Donut hole size (e.g., '40%') |
| `dataLabel` | Object | Label configuration |
| `tilt` | Number | 3D rotation angle (-90 to 90) |
| `legendSettings` | Object | Legend configuration |
| `tooltip` | Object | Tooltip configuration |

