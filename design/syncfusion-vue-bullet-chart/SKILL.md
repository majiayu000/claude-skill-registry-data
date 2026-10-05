---
name: syncfusion-vue-bullet-chart
description: Comprehensive guide for implementing the Syncfusion Vue Bullet Chart component in Vue 2 and Vue 3 applications. Always use this skill when the user needs to implement, configure, or customize a Syncfusion Bullet Chart component, display performance metrics with target comparison, create quality range bands, enable tooltips, or needs troubleshooting for Bullet Chart setup and features. Immediately trigger for any Syncfusion Vue Bullet Chart requirement.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue Bullet Chart

A comprehensive guide for implementing the Syncfusion Essential JS 2 Bullet Chart component in Vue 2 and Vue 3 applications.

## When to Use This Skill

Use this skill when the user needs to:
- **Set up Syncfusion Bullet Chart** in a Vue project (Vue 2 or Vue 3)
- **Display performance metrics** with actual vs target comparison bars
- **Configure data binding** - map value, target, and category fields
- **Customize titles & subtitles** - positioning (Left, Right, Top, Bottom) and styling
- **Create quality ranges** - define performance bands (Good, Satisfactory, Bad) with colors
- **Enable interactive features** - tooltips on hover, keyboard navigation, print support
- **Customize appearance** - orientation (horizontal/vertical), dimensions, animations
- **Implement accessibility** - WCAG 2.2 compliance, screen readers, keyboard shortcuts
- **Troubleshoot Bullet Chart issues** - module injection, styling, data mapping, rendering problems

## Component Overview

The **Bullet Chart** is a data visualization component designed to compare a measure (actual value) against a target bar within quality range bands. It's ideal for KPIs, performance dashboards, and goal tracking.

**Key Characteristics:**
- Horizontal or vertical orientation
- Actual value bar vs target comparative bar
- Customizable quality ranges (colors/opacity)
- Built-in tooltips and keyboard navigation
- Supports multiple bullets with categories
- Responsive design and RTL support
- Full accessibility compliance (WCAG 2.2)

## Documentation & Navigation Guide

Choose the reference file based on your task:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Vue 2 vs Vue 3 project setup
- Installation and package requirements
- Component registration and import
- Module injection (BulletTooltip)
- Basic bullet chart implementation
- Troubleshooting setup issues

### Data Binding & Configuration
📄 **Read:** [references/data-binding-configuration.md](references/data-binding-configuration.md)
- Mapping data source fields (value, target, category)
- Scaling configuration (minimum, maximum, interval)
- Single vs multiple bullet charts
- Local and remote data sources
- Common data patterns and edge cases

### Title & Subtitle Customization
📄 **Read:** [references/title-and-subtitle.md](references/title-and-subtitle.md)
- Adding title and subtitle text
- Positioning titles (Left, Right, Top, Bottom)
- Title styling (font, color, size, weight)
- Subtitle styling and label formatting
- Best practices for chart titles

### Ranges & Color Bands
📄 **Read:** [references/ranges-and-colors.md](references/ranges-and-colors.md)
- Understanding quality ranges (Good, Satisfactory, Bad)
- Defining range end points
- Color and opacity customization
- Multiple ranges and performance bands
- Dynamic range configuration

### Tooltip & Interaction
📄 **Read:** [references/tooltip-interaction.md](references/tooltip-interaction.md)
- Enable and configure tooltips
- Custom tooltip templates
- Tooltip formatting and styling
- Module injection for tooltip feature
- Hover behavior and user interaction

### Customization & Orientation
📄 **Read:** [references/customization-and-orientation.md](references/customization-and-orientation.md)
- Horizontal vs vertical orientation
- Chart dimensions (height, width, responsive)
- Animation settings
- Data label configuration
- Comparative bar and value bar styling
- RTL support

### Accessibility & Advanced Features
📄 **Read:** [references/accessibility-and-advanced.md](references/accessibility-and-advanced.md)
- WCAG 2.2 and Section 508 compliance
- Keyboard navigation (Tab, Shift+Tab, Ctrl+P)
- Screen reader support
- ARIA attributes and semantics
- Right-to-left (RTL) layout
- Print functionality
- Performance optimization tips

## Quick Start Example

**Basic Bullet Chart (Vue 3 Composition API):**

```vue
<template>
  <div class="bullet-chart-container">
    <ejs-bulletchart
      id="bulletChart"
      :dataSource="chartData"
      valueField="value"
      targetField="target"
      :minimum="0"
      :maximum="300"
      :interval="50"
      title="Revenue Performance"
      height="300px"
    >
      <e-bullet-range-collection>
        <e-bullet-range end="100" color="red"></e-bullet-range>
        <e-bullet-range end="200" color="yellow"></e-bullet-range>
        <e-bullet-range end="300" color="green"></e-bullet-range>
      </e-bullet-range-collection>
    </ejs-bulletchart>
  </div>
</template>

<script setup>
import { BulletChartComponent as EjsBulletchart, BulletRangeCollectionDirective, BulletRangeDirective } from '@syncfusion/ej2-vue-charts';

const chartData = [{ value: 270, target: 250 }];
</script>

<style scoped>
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-charts/styles/material.css";
@import "../node_modules/@syncfusion/ej2-vue-charts/styles/material.css";
</style>
```

## Common Patterns

### Pattern 1: Multiple Metrics Dashboard
Display multiple bullet charts for different KPIs:

```vue
<template>
  <div class="dashboard">
    <ejs-bulletchart
      v-for="metric in metrics"
      :key="metric.id"
      :dataSource="[metric]"
      valueField="actual"
      targetField="target"
      :minimum="metric.min"
      :maximum="metric.max"
      :interval="metric.interval"
      :title="metric.name"
    ></ejs-bulletchart>
  </div>
</template>
```

### Pattern 2: Tooltip Enabled with Custom Format
Add interactive tooltips with formatted values:

```vue
<template>
  <ejs-bulletchart
    :dataSource="data"
    valueField="value"
    targetField="target"
    :tooltip="{ enable: true, format: 'Value: {value}, Target: {target}' }"
  ></ejs-bulletchart>
</template>

<script setup>
// Remember to inject BulletTooltip module in provide
</script>
```

### Pattern 3: Category-Based Comparison
Compare multiple items across the same scale:

```vue
<template>
  <ejs-bulletchart
    :dataSource="categoryData"
    valueField="actual"
    targetField="target"
    categoryField="product"
    :minimum="0"
    :maximum="100"
  ></ejs-bulletchart>
</template>

<script setup>
const categoryData = [
  { product: 'Product A', actual: 55, target: 75 },
  { product: 'Product B', actual: 70, target: 70 },
  { product: 'Product C', actual: 85, target: 75 },
];
</script>
```

## Key Props Reference

| Prop | Type | Purpose | Common Values |
|------|------|---------|----------------|
| `dataSource` | Array | Data to display | `[{ value: 270, target: 250 }]` |
| `valueField` | String | Actual value field name | `'value'`, `'actual'` |
| `targetField` | String | Target value field name | `'target'`, `'comparativeMeasure'` |
| `categoryField` | String | Category field (for multiple bullets) | `'category'`, `'product'` |
| `minimum` | Number | Scale minimum | `0`, `100` |
| `maximum` | Number | Scale maximum | `100`, `300` |
| `interval` | Number | Scale interval | `10`, `50` |
| `title` | String | Chart title | `'Revenue'`, `'Performance'` |
| `subtitle` | String | Chart subtitle | `'(in dollars)'` |
| `orientation` | String | Horizontal or vertical | `'Horizontal'`, `'Vertical'` |
| `height` | String | Chart height | `'300px'`, `'100%'` |
| `width` | String | Chart width | `'100%'`, `'400px'` |
| `tooltip` | Object | Tooltip configuration | `{ enable: true, format: '...' }` |

## Common Use Cases

### Use Case 1: Sales Performance Dashboard
Track actual vs target sales for each sales rep:
```
Rep A: Actual $270K vs Target $250K ✓ Exceeded
Rep B: Actual $150K vs Target $250K ✗ Below target
```

### Use Case 2: Manufacturing KPI Tracking
Monitor production efficiency, defect rates, delivery times against targets.

### Use Case 3: Goal Progress Visualization
Display student progress, project completion, or fitness goals vs targets with quality bands.

### Use Case 4: Service Level Agreement (SLA) Monitoring
Track uptime, response time, resolution time metrics against SLA targets.

## Important Notes

- **Module Injection Required:** Must inject `BulletTooltip` module to enable tooltips
- **CSS Imports Mandatory:** Include Syncfusion theme CSS files in your component or main.js
- **Data Mapping Critical:** Ensure `valueField` and `targetField` match your data object keys
- **Responsive Design:** Use `height="100%"` and `width="100%"` for responsive charts
- **Performance:** For 50+ bullet charts, consider pagination or lazy loading

---

**Next Steps:** Select a reference file above based on your task, or read "Getting Started" first if you're new to Bullet Chart.
