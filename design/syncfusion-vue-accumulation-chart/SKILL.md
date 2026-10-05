---
name: syncfusion-vue-accumulation-chart
description: Master Syncfusion Vue Accumulation Charts for building pie, doughnut, funnel, and pyramid visualizations. Always includes data binding, legend configuration, data labels, and accessibility features. Immediately implement any chart type, customize styling, configure legends, format data labels, and add drill-down interactivity using ALWAYS comprehensive examples and patterns.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Accumulation Chart in Vue

Accumulation Chart is a powerful data visualization component for displaying hierarchical data as pie, doughnut, funnel, or pyramid charts. Master setup, chart types, data labels, legends, and advanced features.

## When to Use This Skill

Use this skill when you need to:
- Build pie or doughnut charts displaying categorical data
- Create funnel or pyramid charts for hierarchical visualization
- Customize chart appearance, colors, and styling
- Configure legend positioning, sizing, and interaction
- Add data labels with formatting and templates
- Implement drill-down or multi-level chart interactions
- Ensure keyboard accessibility and screen reader support
- Bind dynamic data and update charts in real-time

## Chart Types Overview

The Accumulation Chart component supports:
- **Pie Charts:** Standard circular pie with 360° visualization
- **Doughnut Charts:** Pie with inner radius creating a ring effect
- **Funnel Charts:** Hierarchical data flow visualization
- **Pyramid Charts:** Hierarchical pyramid visualization
- **Semi-Pie Charts:** Customizable start/end angles

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)


- Properties
- Data Models
- Events
- Methods
- Enums
- Child Directives
- Modules / Services
- Common Usage Patterns
- Additional Resources

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Vue 2 project configuration
- Component registration
- Module injection and dependencies
- Basic chart implementation
- CSS imports and styling

### Chart Types and Customization
📄 **Read:** [references/chart-types.md](references/chart-types.md)
- Pie chart basics and variants
- Radius customization and sizing
- Doughnut charts (innerRadius property)
- Center positioning and rotation
- Start/End angles (semi-pie charts)
- Border radius for modern appearance
- Multiple series in one chart
- Size mapping and dynamic sizing

### Data Labels Configuration
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enable and position data labels
- Label formatting and customization
- Smart label placement
- Rotation and text wrapping
- Connector lines configuration
- Template-based labels
- Display percentages and custom content
- Label events and rendering

### Legend Configuration
📄 **Read:** [references/legend-configuration.md](references/legend-configuration.md)
- Display and position legends
- Alignment options (Top, Bottom, Left, Right)
- Sizing and item sizing
- Legend shapes and icons
- Paging and navigation
- Text wrapping and maximum width
- Animation on legend click
- Custom legend templates
- Item padding and layout

### Advanced Features and Interactions
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Multi-level drill-down implementation
- Point and series events
- Tooltip configuration
- Annotations and markers
- Color mapping and styling
- Dynamic data updates
- Print functionality
- Export options

### Accessibility and Keyboard Support
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- Keyboard navigation shortcuts
- Screen reader support (ARIA attributes)
- Right-to-left (RTL) support
- Color contrast standards
- Mobile device accessibility

---

## Quick Start Example

```vue
<template>
  <div id="app">
    <ejs-accumulationchart id="chart-container">
      <e-accumulation-series-collection>
        <e-accumulation-series :dataSource="chartData" xName="category" yName="percentage">
        </e-accumulation-series>
      </e-accumulation-series-collection>
    </ejs-accumulationchart>
  </div>
</template>

<script>
import { AccumulationChartComponent, AccumulationSeriesCollectionDirective, AccumulationSeriesDirective, PieSeries } from "@syncfusion/ej2-vue-charts";

export default {
  name: "App",
  components: {
    'ejs-accumulationchart': AccumulationChartComponent,
    'e-accumulation-series-collection': AccumulationSeriesCollectionDirective,
    'e-accumulation-series': AccumulationSeriesDirective
  },
  data() {
    return {
      chartData: [
        { category: 'Chrome', percentage: 37 },
        { category: 'Firefox', percentage: 28 },
        { category: 'Safari', percentage: 19 },
        { category: 'Others', percentage: 16 }
      ]
    };
  },
  provide: {
    accumulationchart: [PieSeries]
  }
};
</script>

<style>
#chart-container {
  height: 400px;
}
</style>
```

---

## Common Patterns

### Pattern 1: Chart Type Selection
**User Intent:** Choose between different chart types (pie, doughnut, funnel)

```vue
// For Pie Chart
provide: {
  accumulationchart: [PieSeries]
}

// For Doughnut with innerRadius
<e-accumulation-series :dataSource="data" innerRadius="40%" xName="x" yName="y">
</e-accumulation-series>

// For Funnel Chart (requires FunnelSeries)
provide: {
  accumulationchart: [FunnelSeries]
}
```

### Pattern 2: Data Label Positioning
**User Intent:** Position labels inside or outside the chart with smart placement

```vue
dataLabel: {
  visible: true,
  position: 'Outside',  // 'Inside' or 'Outside'
  name: 'label_field',
  connectorStyle: { type: 'Curve', length: '50px' }
}
```

### Pattern 3: Legend and Data Integration
**User Intent:** Show legend with positioning and animation

```vue
legendSettings: {
  visible: true,
  position: 'Right',
  alignment: 'Center'
}
```

### Pattern 4: Custom Styling and Colors
**User Intent:** Map data properties to colors and styling

```vue
<e-accumulation-series 
  :dataSource="data" 
  xName="x" 
  yName="y"
  :pointColorMapping="color"
  :dataLabel="dataLabel">
</e-accumulation-series>
```

---

## Key Props Reference

| Property | Type | Purpose |
|----------|------|---------|
| `dataSource` | Array | Series data binding |
| `xName` | String | X-axis data field name |
| `yName` | String | Y-axis data field name |
| `radius` | String | Pie/doughnut radius (e.g., '70%', '100px') |
| `innerRadius` | String | Doughnut hole size (e.g., '40%') |
| `startAngle` | Number | Starting angle (0-360) |
| `endAngle` | Number | Ending angle (0-360) |
| `borderRadius` | Number | Rounded corner radius for slices |
| `pointColorMapping` | String | Map data field to colors |
| `dataLabel` | Object | Data label configuration |
| `legendSettings` | Object | Legend positioning and styling |
| `tooltip` | Object | Tooltip on hover |
| `center` | Object | Chart center position {x, y} |
| `enableSmartLabels` | Boolean | Auto-arrange labels to avoid overlap |

---

## Common Use Cases

### Use Case 1: Market Share Pie Chart
Display categorical data (browser market share, sales by region, etc.)

**Key features:** Simple pie, legend, percentage labels, interactive tooltip

### Use Case 2: Funnel Analysis
Show progression through stages (sales pipeline, user conversion funnel)

**Key features:** Funnel series, hierarchical data, stage-by-stage comparison

### Use Case 3: Multi-Level Drill-Down
Click pie slices to drill into subcategories

**Key features:** Point click event, dynamic data binding, navigation UI

### Use Case 4: Dashboard KPI Visualization
Visualize part-to-whole relationships in dashboards

**Key features:** Doughnut center label, color mapping, responsive sizing

---

## Quick API Reference

### Essential Component Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `dataSource` | Array/Object | `''` | Series data binding |
| `title` | String | `null` | Chart title |
| `theme` | String | `'Material'` | Visual theme |
| `legendSettings` | Object | `{}` | Legend configuration |
| `tooltip` | Object | `{}` | Tooltip on hover |
| `enableSmartLabels` | Boolean | `true` | Auto-arrange labels |
| `selectionMode` | String | `'None'` | Point selection: 'None', 'Point' |
| `enableExport` | Boolean | `true` | Export to PNG/PDF/SVG/XLSX/CSV |
| `enableRtl` | Boolean | `false` | Right-to-left rendering |

### Essential Series Properties

```vue
<e-accumulation-series
  type="Pie"                           <!-- 'Pie', 'Doughnut', 'Funnel', 'Pyramid' -->
  :dataSource="data"                   <!-- Series data -->
  xName="category"                     <!-- Category field name -->
  yName="value"                        <!-- Value field name -->
  radius="80%"                      <!-- Pie/doughnut radius -->
  innerRadius="40%"                 <!-- Doughnut hole (doughnut only) -->
  :dataLabel="dataLabel"       <!-- Show data labels -->
  :pointColorMapping="color"         <!-- Map color from data field -->
></e-accumulation-series>
```

### Essential Methods

```vue
// Export chart
this.$refs.chart.value.export('PNG', 'chart.png');
this.$refs.chart.value.export('PDF', 'chart.pdf');

// Print chart
this.$refs.chart.value.print();

// Update annotation
this.$refs.chart.value.setAnnotationValue(0, '<p>New Content</p>');

// Calculate bounds
this.$refs.chart.value.calculateBounds();
```

### Essential Events

```vue
<!-- Lifecycle -->
:load="onChartLoad"                    <!-- Before chart loads -->
:loaded="onChartLoaded"                <!-- After chart loads -->

<!-- Rendering -->
:seriesRender="onSeriesRender"         <!-- Before series renders -->
:pointRender="onPointRender"           <!-- Before point renders -->
:textRender="onTextRender"             <!-- Before labels render -->

<!-- User Interaction -->
:chartMouseClick="onChartClick"        <!-- Chart clicked -->
:pointClick="onPointClick"             <!-- Point clicked -->
:selectionComplete="onSelectionComplete" <!-- Selection done -->
:legendClick="onLegendClick"           <!-- Legend item clicked -->

<!-- Display -->
:tooltipRender="onTooltipRender"       <!-- Before tooltip renders -->
:animationComplete="onAnimationComplete" <!-- Animation finished -->

<!-- Export -->
:beforeExport="onBeforeExport"         <!-- Before export starts -->
:afterExport="onAfterExport"           <!-- After export completes -->
```

### Common Configurations

**Enable Data Labels with Percentages:**
```vue
<template>
  <e-accumulation-series :dataSource='seriesData' xName='x' yName='y' :dataLabel='dataLabel'>
  </e-accumulation-series>
</template>

<script>
export default {
  data() {
    return {
      dataLabel: {
          visible: true,
          position: 'Outside',
          format: '${x}: ${y}%',
          connectorStyle: { type: 'Curve', length: '50px' }
      }
    };
  }
};
</script>
```

**Configure Legend:**
```vue
<template>
  <ejs-accumulationchart id="container" :legendSettings='legendSettings'>
  </ejs-accumulationchart>
</template>

<script>
export default {
  data() {
    return {
      legendSettings: {
          visible: true,
          position: 'Right',
          alignment: 'Center'
      }
    };
  }
};
</script>
```

**Tooltip with Custom Format:**
```vue
<template>
  <ejs-accumulationchart id="container" :tooltip='tooltip'>
  </ejs-accumulationchart>
</template>

<script>
export default {
  data() {
    return {
      tooltip: {
          enable: true,
          format: '<b>${x}</b>: ${y} units',
          fill: '#f5f5f5'
      }
    };
  }
};
</script>
```

**Point Selection:**
```vue
<template>
  <ejs-accumulationchart id="container" selectionMode="Point" isMultiSelect="true" :selectedDataIndexes="selectedDataIndexes">
  </ejs-accumulationchart>
</template>

<script>
export default {
  data() {
    return {
      selectedDataIndexes: [
          { series: 0, point: 0 },
          { series: 0, point: 2 }
      ]
    };
  }
};
</script>
```

---

## Next Steps

1. **Explore APIs:** [references/api-reference.md](references/api-reference.md) to understand all available properties, methods, and events
2. **Start with:** [references/getting-started.md](references/getting-started.md) to set up your project
3. **Choose your chart:** [references/chart-types.md](references/chart-types.md) for pie, doughnut, or funnel
4. **Enhance display:** [references/data-labels.md](references/data-labels.md) and [references/legend-configuration.md](references/legend-configuration.md)
5. **Add interactivity:** [references/advanced-features.md](references/advanced-features.md) for drill-down and events
6. **Ensure accessibility:** [references/accessibility.md](references/accessibility.md) for WCAG compliance
