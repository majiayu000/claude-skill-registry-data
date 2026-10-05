---
name: syncfusion-vue-heatmap
description: Create interactive heat map data visualizations using Syncfusion Vue components. Use this skill whenever users need to implement, configure, or customize HeatMap charts in Vue applications for displaying patterns in 2D tabular data, visualizing intensity across dimensions, creating sales matrices, employee performance heatmaps, or any temporal/categorical data correlation visualization.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue HeatMap Chart

## When to Use This Skill

Use this skill when you need to:
- Create a HeatMap component to visualize 2D tabular data with color-coded values
- Display intensity patterns across multiple dimensions (e.g., sales by employee and day)
- Configure axes with category, numerical, or datetime labels
- Customize cell appearance, colors, legends, and tooltips
- Handle user interactions like cell clicks and cell selection
- Apply color palettes and data-driven styling
- Build data-rich analytical dashboards in Vue applications

## Component Overview

The Syncfusion Vue HeatMap component visualizes two-dimensional data where values are represented through gradient or fixed color mappings. It's ideal for:
- **Temporal Analysis**: Showing patterns over time (hours, days, months)
- **Comparative Matrices**: Comparing performance across categories (employees, regions, products)
- **Heatmaps**: Representing intensity or magnitude with color gradients
- **Data Pattern Discovery**: Identifying correlations and anomalies in 2D datasets

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When user needs:
- Installation and npm package setup
- Vue 2 project initialization
- Component registration in Vue
- Basic HeatMap rendering with minimal configuration
- Understanding of feature modules (Legend, Tooltip)
- Running and testing the project

### Data Binding and Working with Data
📄 **Read:** [references/data-binding-and-sources.md](references/data-binding-and-sources.md)

When user needs:
- Populating HeatMap with data sources
- Understanding 2D array data format
- Binding data to dataSource property
- Working with different data structures
- Setting up sample datasets

### Axis Configuration
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)

When user needs:
- Configuring X-axis and Y-axis properties
- Understanding axis types (Category, Numerical, Datetime)
- Adding axis labels and customization
- Setting up category labels for rows and columns
- Formatting axis display

### Appearance and Styling
📄 **Read:** [references/appearance-and-styling.md](references/appearance-and-styling.md)

When user needs:
- Customizing cell borders and cell appearance
- Styling titles and text properties
- Configuring rendering modes (SVG vs Canvas)
- Cell settings (labels, borders, styling)
- Visual layout customization

### Legend and Tooltips
📄 **Read:** [references/legend-and-tooltips.md](references/legend-and-tooltips.md)

When user needs:
- Enabling and positioning legends
- Customizing legend visibility and display
- Setting up tooltips for cell information
- Creating tooltip templates
- Customizing labels and indicators

### Events and Selection
📄 **Read:** [references/events-and-selection.md](references/events-and-selection.md)

When user needs:
- Handling cell click events
- Implementing cell selection functionality
- Responding to user interactions
- Understanding event arguments and data
- Building interactive features

### Palette and Color Customization
📄 **Read:** [references/palette-and-colors.md](references/palette-and-colors.md)

When user needs:
- Configuring color palettes for cells
- Using gradient vs fixed color modes
- Creating custom color schemes
- Setting color ranges for data mapping
- Applying predefined palette types

## Quick Start Example

```vue
<template>
  <div id="app">
    <ejs-heatmap id="heatmap" 
      :dataSource='dataSource'
      :xAxis='xAxis'
      :yAxis='yAxis'
      :titleSettings='titleSettings'
      :legendSettings='legendSettings'>
    </ejs-heatmap>
  </div>
</template>

<script>
import { HeatMapComponent, Tooltip, Legend } from '@syncfusion/ej2-vue-heatmap';

export default {
  name: "App",
  components: {
    'ejs-heatmap': HeatMapComponent
  },
  data: function () {
    return {
      dataSource: [
        [73, 39, 26, 39, 94, 0],
        [93, 58, 53, 38, 26, 68],
        [99, 28, 22, 4, 66, 90],
        [14, 26, 97, 69, 69, 3],
        [7, 46, 47, 47, 88, 6],
        [41, 55, 73, 23, 3, 79]
      ],
      xAxis: {
        labels: ['Nancy', 'Andrew', 'Janet', 'Margaret', 'Steven', 'Michael']
      },
      yAxis: {
        labels: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']
      },
      titleSettings: {
        text: 'Sales Revenue per Employee (in 1000 US$)',
        textStyle: { size: '15px', fontWeight: '500' }
      },
      legendSettings: {
        visible: true,
        position: 'Right',
        showLabel: true
      }
    }
  },
  provide: {
    heatmap: [Tooltip, Legend]
  }
}
</script>
```

## Common Patterns

### Pattern 1: Basic Data Visualization
**When:** Displaying simple 2D data with minimal configuration
- Define 2D array as dataSource
- Add axis labels via xAxis and yAxis
- Enable legend and tooltip modules
- Render immediately

### Pattern 2: Interactive Dashboard
**When:** Building analytical dashboards with user interactions
- Configure cellClick events to respond to selections
- Show detailed information in tooltips
- Customize legends for data interpretation
- Apply color palettes for visual emphasis

### Pattern 3: Performance Analysis
**When:** Showing patterns over time or across categories
- Use Category axis type for both X and Y axes
- Map time/category labels to axis labels
- Use gradient palettes to represent intensity
- Add titles and legends for context

## Key Props

| Prop | Type | Purpose |
|------|------|---------|
| `dataSource` | Array | 2D array containing numerical values |
| `xAxis` | Object | Configuration for X-axis (labels, valueType) |
| `yAxis` | Object | Configuration for Y-axis (labels, valueType) |
| `titleSettings` | Object | Configures HeatMap title and text styling |
| `legendSettings` | Object | Controls legend display and positioning |
| `cellSettings` | Object | Customizes cell appearance (border, labels) |
| `paletteSettings` | Object | Defines color palette and gradient mode |
| `showTooltip` | Boolean | Enables/disables tooltip feature |
| `cellClick` | Function | Event handler for cell click interactions |

## Common Use Cases

1. **Employee Performance Matrix** - Display sales/productivity by employee and time period
2. **Weather Heatmaps** - Visualize temperature, humidity across locations/time
3. **Website Analytics** - Show page traffic by hour and day of week
4. **Correlation Matrix** - Display relationships between multiple variables
5. **Production Metrics** - Track defects or quality metrics across shifts and products
