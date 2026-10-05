---
name: syncfusion-vue-circular-gauge
description: Guide to implementing Syncfusion Vue Circular Gauge component. Use when users need to create circular gauges, progress indicators, speedometers, or status displays. Includes setup, configuration of axes, ranges, pointers, legends, animations, accessibility, print/export, and customization. Essential for data visualization, real-time monitoring, and interactive gauge-based dashboards.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "data-visualization"
---

# Implementing Syncfusion Vue Circular Gauge

The Syncfusion Vue Circular Gauge component is a powerful, feature-rich control for creating circular gauges, progress bars, speedometers, and status indicators. It supports multiple axes, pointers, ranges, annotations, legends, and extensive customization options.

## When to Use This Skill

- Setting up a new Circular Gauge component in a Vue application
- Configuring axes, ranges, and pointers for data visualization
- Implementing interactive features (pointer dragging, tooltips, value updates)
- Creating styled gauges with custom colors, gradients, and themes
- Building real-time monitoring dashboards with animated values
- Implementing gauges with legends, annotations, and labels
- Adding print, export, and accessibility features
- Supporting multiple languages and RTL layouts

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Vue 2 and Vue 3 project configuration
- Importing and registering CircularGaugeComponent
- Basic component initialization
- CSS imports and theme configuration
- First working example

### Axes and Ranges Configuration
📄 **Read:** [references/axes-and-ranges.md](references/axes-and-ranges.md)
- Axis configuration and properties
- Multiple axes support
- Range creation and styling
- Range colors and gradients
- Setting minimum and maximum values
- Configuring axis labels and ticks

### Pointers, Animations, and Interactions
📄 **Read:** [references/pointers-animations-interactions.md](references/pointers-animations-interactions.md)
- Pointer types (needle, marker, range bar)
- Pointer configuration and styling
- Enabling pointer dragging
- Animation settings and transitions
- Drag events and value change handling
- Tooltips and user feedback

### Styling, Appearance, and Themes
📄 **Read:** [references/styling-appearance-themes.md](references/styling-appearance-themes.md)
- Component sizing and dimensions
- Label styling and positioning
- Color customization and gradients
- Theme selection (Light, Dark, Bootstrap, etc.)
- CSS class customization
- Responsive design patterns

### Legend, Annotations, and Labels
📄 **Read:** [references/legend-annotations-labels.md](references/legend-annotations-labels.md)
- Legend configuration and visibility
- Legend alignment and positioning
- Adding annotations to gauges
- Custom labels and text elements
- Annotation positioning and styling
- Dynamic annotation updates

### Print, Export, and Advanced Features
📄 **Read:** [references/print-export-advanced.md](references/print-export-advanced.md)
- Print functionality and configuration
- Export to image formats (PNG, SVG, PDF)
- RTL (Right-to-Left) layout support
- Accessibility (WCAG compliance, ARIA attributes, keyboard navigation)
- Internationalization and localization
- Multi-language support

### Real-Time Data and Advanced Use Cases
📄 **Read:** [references/realtime-and-use-cases.md](references/realtime-and-use-cases.md)
- Updating gauge values in real-time
- Creating dashboards with multiple gauges
- Performance optimization techniques
- Common patterns for monitoring applications
- Building custom gauges beyond defaults
- Responsive gauge sizing and adaptation

## Quick Start Example

Here's a minimal working example to get started with the Circular Gauge component:

```vue
<template>
  <div id="app">
    <ejs-circulargauge id="container" :axes="axes">
    </ejs-circulargauge>
  </div>
</template>

<script>
import { CircularGaugeComponent } from '@syncfusion/ej2-vue-circulargauge';

export default {
  components: {
    'ejs-circulargauge': CircularGaugeComponent
  },
  data() {
    return {
      axes: [{
        minimum: 0,
        maximum: 100,
        startAngle: 0,
        endAngle: 360,
        ranges: [{
          start: 0,
          end: 25,
          color: '#3FB9E3'
        }, {
          start: 25,
          end: 50,
          color: '#33E9F6'
        }, {
          start: 50,
          end: 75,
          color: '#52F0A7'
        }, {
          start: 75,
          end: 100,
          color: '#A4D600'
        }],
        pointers: [{
          value: 65,
          radius: '60%'
        }]
      }]
    };
  }
};
</script>

<style>
#container {
  height: '450px';
}
</style>
```

This example creates:
- A circular gauge with 0-100 range
- Four color-coded ranges
- A pointer showing the value 65

## Common Patterns

### Pattern 1: Creating a Status Gauge
Display real-time status with multiple ranges representing different states:

```javascript
// In data()
axes: [{
  minimum: 0,
  maximum: 100,
  ranges: [
    { start: 0, end: 33, color: '#E74C3C' },    // Critical
    { start: 33, end: 66, color: '#F39C12' },   // Warning
    { start: 66, end: 100, color: '#27AE60' }   // Healthy
  ],
  pointers: [{
    value: this.systemStatus
  }]
}]
```

### Pattern 2: Performance Speedometer
Build a speedometer-style gauge with multiple pointers:

```javascript
axes: [{
  minimum: 0,
  maximum: 200,
  pointers: [
    { value: 120, name: 'Actual Speed', radius: '55%' },
    { value: 180, name: 'Max Speed', radius: '50%' }
  ]
}]
```

### Pattern 3: Responsive Multiple Gauges
Create a dashboard with multiple gauges that adapt to screen size:

```vue
<template>
  <div class="gauge-container">
    <div class="gauge-item">
      <ejs-circulargauge :axes="cpuAxes"></ejs-circulargauge>
    </div>
    <div class="gauge-item">
      <ejs-circulargauge :axes="memoryAxes"></ejs-circulargauge>
    </div>
    <div class="gauge-item">
      <ejs-circulargauge :axes="diskAxes"></ejs-circulargauge>
    </div>
  </div>
</template>

<style>
.gauge-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}
</style>
```

## Key Props and Configuration

- **minimum/maximum**: Set the gauge value range
- **startAngle/endAngle**: Define gauge arc (0-360 degrees)
- **ranges**: Array of value ranges with colors
- **pointers**: Array of pointer configurations
- **legends**: Legend display and positioning
- **annotations**: Custom text and content overlays
- **enableAnimation**: Enable smooth transitions
- **enablePointerDrag**: Allow user interaction
- **theme**: Select predefined color scheme

## Common Use Cases

1. **Monitoring Dashboards**: Track CPU, memory, disk, and network metrics
2. **Performance Indicators**: Display application performance, response times
3. **Progress Tracking**: Show completion percentage or status progress
4. **Speedometers**: Visualize speed, velocity, or rate metrics
5. **Temperature Gauges**: Monitor system or environmental temperature
6. **Quality Indicators**: Display quality scores or ratings
7. **Real-Time Analytics**: Update gauges with live data feeds

