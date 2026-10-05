---
name: syncfusion-vue-smith-chart
description: Implement Smith Chart visualization for high-frequency circuit analysis. Use this skill whenever the user needs to create Smith Charts, visualize transmission lines, plot impedance/admittance, configure series data, add markers/tooltips, or work with RF (radio frequency) and microwave engineering visualizations using Syncfusion Vue Smith Chart component.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Smith Chart Component

The Smith Chart is a specialized data visualization tool for high-frequency circuit applications. It uses two sets of concentric circles to plot transmission line parameters, impedance, and admittance values. This skill guides you through implementing, configuring, and customizing the Syncfusion Vue Smith Chart component.

## When to Use This Skill

- Creating Smith Charts for RF circuit analysis
- Visualizing transmission line data (impedance, admittance)
- Plotting resistance and reactance values
- Adding interactive features (markers, tooltips, legends)
- Implementing data visualization for microwave engineering applications
- Customizing chart appearance (colors, dimensions, titles)
- Handling multiple series with different configurations

## What Smith Chart Does

The Smith Chart component:
- Plots complex impedance and admittance data on circular grid
- Supports multiple series with different line styles
- Provides interactive markers and data labels
- Includes legend and tooltip features
- Renders impedance or admittance visualizations
- Exports charts to image or print formats
- Supports both Vue 2 and Vue 3

## Navigation Guide
### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

Headings:

- Overview
- Properties
- Data Models
- Events
- Methods
- Enums
- Child Directives
- Modules/Services
- Common Usage Patterns
- Additional Resources

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Vue 2 & Vue 3 project configuration
- Basic Smith Chart implementation
- CSS imports and theme setup
- Module injection for optional features

### Series and Data Binding
📄 **Read:** [references/series-and-data-binding.md](references/series-and-data-binding.md)
- Series configuration structure
- Using dataSource vs points
- Resistance and reactance data mapping
- Adding multiple series
- Series customization (colors, width, opacity)

### Markers, Labels, and Tooltips
📄 **Read:** [references/markers-labels-and-tooltips.md](references/markers-labels-and-tooltips.md)
- Enabling markers on data points
- Displaying data labels on markers
- Configuring tooltip interaction
- Tooltip formatting and templates
- Handling marker events

### Axis, Legend, and Printing
📄 **Read:** [references/axis-legend-and-printing.md](references/axis-legend-and-printing.md)
- Axis customization and formatting
- Legend configuration and positioning
- Print functionality
- Print events and lifecycle
- Export options

### Dimensions, Title, and Accessibility
📄 **Read:** [references/dimensions-title-and-accessibility.md](references/dimensions-title-and-accessibility.md)
- Setting chart dimensions (width, height)
- Adding titles and subtitles
- Responsive sizing
- WCAG accessibility compliance
- Keyboard navigation support

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Impedance vs Admittance rendering modes
- Vue 3 Composition API examples
- Data transformation patterns
- Performance optimization techniques
- Real-world transmission line scenarios

## Quick Start

### Basic Smith Chart Implementation

```vue
<template>
  <div class="control_wrapper">
    <ejs-smithchart id="smithchart" :title='title'>
      <e-seriesCollection>
        <e-series 
          :dataSource='dataSource' 
          :name='name' 
          :reactance='reactance' 
          :resistance='resistance'>
        </e-series>
      </e-seriesCollection>
    </ejs-smithchart>
  </div>
</template>

<script>
import { SmithchartComponent, SeriesDirective, SeriesCollectionDirective } from '@syncfusion/ej2-vue-charts';

export default {
  components: {
    'ejs-smithchart': SmithchartComponent,
    'e-seriesCollection': SeriesCollectionDirective,
    'e-series': SeriesDirective
  },
  data: function () {
    return {
      title: { text: 'Transmission Lines - Impedance Chart' },
      dataSource: [
        { resistance: 10, reactance: 25 }, { resistance: 8, reactance: 6 },
        { resistance: 6, reactance: 4.5 }, { resistance: 4.5, reactance: 2 },
        { resistance: 3.5, reactance: 1.6 }, { resistance: 2.5, reactance: 1.3 },
        { resistance: 2, reactance: 1.2 }, { resistance: 1.5, reactance: 1 },
        { resistance: 1, reactance: 0.8 }, { resistance: 0.5, reactance: 0.4 },
        { resistance: 0.3, reactance: 0.2 }, { resistance: 0, reactance: 0.15 }
      ],
      name: 'Transmission1',
      reactance: 'reactance',
      resistance: 'resistance'
    }
  }
}
</script>
```

## Common Patterns

### Pattern 1: Multiple Series with Markers and Legend

```vue
<template>
  <ejs-smithchart id="smithchart" :title='title' :legendSettings='legendSettings'>
    <e-seriesCollection>
      <e-series 
        :dataSource='data1' 
        :name='name1' 
        :marker='marker1'
        :reactance='reactance' 
        :resistance='resistance'>
      </e-series>
      <e-series 
        :dataSource='data2' 
        :name='name2' 
        :marker='marker2'
        :reactance='reactance' 
        :resistance='resistance'>
      </e-series>
    </e-seriesCollection>
  </ejs-smithchart>
</template>

<script>
import { SmithchartComponent, SeriesDirective, SeriesCollectionDirective, SmithchartLegend } from '@syncfusion/ej2-vue-charts';
export default {
  data: function () {
    return {
      title: { text: 'Multiple Transmission Lines' },
      legendSettings: { visible: true },
      marker1: { visible: true, dataLabel: { visible: true } },
      marker2: { visible: true, dataLabel: { visible: true } },
      reactance: 'reactance',
      resistance: 'resistance',
      // ... data arrays
    }
  },
  provide: {
    smithchart: [SmithchartLegend]
  }
}
</script>
```

### Pattern 2: Interactive Chart with Tooltips

```vue
<template>
  <ejs-smithchart id="smithchart" :title='title'>
    <e-seriesCollection>
      <e-series 
        :dataSource='dataSource'
        :tooltip='tooltip'
        :name='name'
        :reactance='reactance' 
        :resistance='resistance'>
      </e-series>
    </e-seriesCollection>
  </ejs-smithchart>
</template>

<script>
import { SmithchartComponent, SeriesDirective, SeriesCollectionDirective, TooltipRender } from '@syncfusion/ej2-vue-charts';

export default {
  data: function () {
    return {
      tooltip: { visible: true },
      // ... other properties
    }
  },
  provide: {
    smithchart: [TooltipRender]
  }
}
</script>
```

## Key Props

### SmithchartComponent Props
- **title** - Chart title configuration (text, font style, visibility)
- **legendSettings** - Legend configuration (visibility, position, padding)
- **width** - Chart width in pixels or percentage
- **height** - Chart height in pixels or percentage
- **renderType** - Render mode: 'Impedance' (default) or 'Admittance'

### Series Props
- **dataSource** - Array of data objects with resistance/reactance values
- **points** - Alternative to dataSource, explicit array of points
- **name** - Series identifier (shown in legend)
- **resistance** - Field name for resistance values in data
- **reactance** - Field name for reactance values in data
- **fill** - Line color (e.g., '#FF5733')
- **width** - Line width in pixels
- **opacity** - Line transparency (0-1)
- **marker** - Marker configuration object
- **tooltip** - Tooltip configuration

### Marker Props
- **visible** - Enable/disable markers
- **width** - Marker size
- **border** - Border styling
- **dataLabel** - Data label configuration

## Common Use Cases

**Use Case 1: Basic Circuit Analysis**
Visualize a single transmission line impedance curve for circuit design analysis.

**Use Case 2: Multi-Line Comparison**
Plot multiple transmission lines with different characteristics to compare impedance behavior.

**Use Case 3: Interactive RF Dashboard**
Create an interactive dashboard with tooltips, markers, and legends for RF circuit monitoring.

**Use Case 4: Print-Ready Charts**
Generate charts formatted for printing or exporting as images for documentation.

## Related Information

- **Vue 3 Setup** - Vue 3 uses Composition API, but Smith Chart component works identically
- **Themes** - Syncfusion supports Material, Bootstrap, and custom themes
- **Module Injection** - Legend and Tooltip are optional modules that must be injected
- **Data Formats** - Resistance/reactance values are normalized numerical values
- **Performance** - Smith Chart efficiently handles 100+ data points per series

## Next Steps

1. Start with [Getting Started](references/getting-started.md) to set up your project
2. Configure your data using [Series and Data Binding](references/series-and-data-binding.md)
3. Add interactivity with [Markers and Tooltips](references/markers-labels-and-tooltips.md)
4. Enhance presentation with [Dimensions and Titles](references/dimensions-title-and-accessibility.md)
5. Explore advanced patterns in [Advanced Patterns](references/advanced-patterns.md)
