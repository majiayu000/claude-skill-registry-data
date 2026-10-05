---
name: syncfusion-vue-linear-gauge
description: Implement and configure Syncfusion Vue Linear Gauge for displaying numerical values on a linear axis. Use this skill when building data visualization dashboards, creating gauge indicators, displaying measurements or metrics, implementing temperature/pressure sensors, speed indicators, or any linear measurement display. Covers setup, pointer management, ranges, annotations, interactions, and advanced customization.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing Linear Gauge

The Linear Gauge is a Syncfusion Vue component for visualizing numerical values along a linear axis. It renders using SVG for high performance and supports multiple pointers, ranges, annotations, and interactive features like drag-and-drop and tooltips.

## When to Use Linear Gauge

- **Measurement displays**: Temperature, pressure, speed, battery level
- **Dashboard metrics**: KPIs displayed as gauge indicators
- **Real-time monitoring**: Updates to pointer values as data changes
- **Multi-level indicators**: Multiple pointers showing different metrics on same axis
- **Annotated ranges**: Highlighting safe/warning/danger zones

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and setup
- Basic component initialization
- Vue 3 and Vue 2 compatibility
- Theming and CSS imports
- First working example

### Axis Configuration
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)
- Axis properties (min, max, interval, line style)
- Label formatting and positioning
- Axis ranges (visible range)
- RTL support
- Multiple axes

### Pointers and Ranges
📄 **Read:** [references/pointers-and-ranges.md](references/pointers-and-ranges.md)
- Marker pointers (shape, size, position)
- Bar pointers (width, offset)
- Range bars and ranges
- Color styling for different elements
- Performance with multiple elements

### Annotations and Customization
📄 **Read:** [references/annotations-and-customization.md](references/annotations-and-customization.md)
- Adding text and HTML annotations
- Annotation positioning and alignment
- CSS class customization
- Dynamic style updates
- Theme integration

### Interactions and Events
📄 **Read:** [references/interactions-and-events.md](references/interactions-and-events.md)
- Pointer drag-and-drop functionality
- Tooltip configuration
- Event handling (valueChange, drag, resize)
- Animation behavior
- Print and export functionality

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Animation configuration
- Internationalization (i18n) support
- Accessibility compliance (WCAG, ARIA)
- Component methods and references
- Performance optimization
- Browser compatibility

### Troubleshooting
📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)
- Common issues and solutions
- Data binding and updates
- Event handling gotchas
- Styling and CSS issues
- Known limitations

## Quick Start Example

```vue
<template>
  <ejs-lineargauge id="linearGauge" :axes="axes" :pointers="pointers">
  </ejs-lineargauge>
</template>

<script>
import { LinearGaugeComponent as EjsLineargauge, AxesDirective, AxisDirective, PointersDirective, PointerDirective } from '@syncfusion/ej2-vue-gauges';

export default {
  components: {
    'ejs-lineargauge': EjsLineargauge,
    'e-axes': AxesDirective,
    'e-axis': AxisDirective,
    'e-pointers': PointersDirective,
    'e-pointer': PointerDirective
  },
  data() {
    return {
      axes: [{
        minimum: 0,
        maximum: 100,
        line: { width: 2 },
        pointers: [{
          value: 60,
          type: 'Marker',
          markerType: 'Triangle',
          width: 15,
          border: { width: 2, color: '#F8F8F8' },
          color: '#F262CC'
        }],
        ranges: [{
          start: 0,
          end: 35,
          color: '#3DA58A'
        }, {
          start: 35,
          end: 70,
          color: '#FDD835'
        }, {
          start: 70,
          end: 100,
          color: '#F6464F'
        }]
      }],
      pointers: []
    };
  }
};
</script>
```

## Common Patterns

### Pattern 1: Update Pointer Value Programmatically

```javascript
// Get gauge instance and update pointer value
const gauge = document.getElementById('linearGauge').ej2_instances[0];
gauge.setPointerValue(0, 0, 75); // axis index, pointer index, new value
```

### Pattern 2: Multiple Pointers on Same Axis

```javascript
data() {
  return {
    axes: [{
      minimum: 0,
      maximum: 100,
      pointers: [
        {
          value: 45,
          type: 'Marker',
          markerType: 'Triangle',
          color: '#FF0000'
        },
        {
          value: 70,
          type: 'Bar',
          width: 8,
          color: '#00FF00'
        }
      ]
    }]
  };
}
```

### Pattern 3: Reactive Data Binding

```vue
<template>
  <div>
    <input v-model.number="pointerValue" type="range" min="0" max="100">
    <ejs-lineargauge :axes="axes"></ejs-lineargauge>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pointerValue: 50,
      axes: [{
        minimum: 0,
        maximum: 100,
        pointers: [{
          value: this.pointerValue,
          type: 'Marker'
        }]
      }]
    };
  },
  watch: {
    pointerValue(newVal) {
      const gauge = document.getElementById('linearGauge').ej2_instances[0];
      gauge.setPointerValue(0, 0, newVal);
    }
  }
};
</script>
```

## Key Props and Configuration

| Prop | Purpose | Common Values |
|------|---------|---------------|
| `minimum` | Axis lower bound | 0, -50, -100 |
| `maximum` | Axis upper bound | 100, 50, 360 |
| `interval` | Tick mark interval | 10, 20, 25, 50 |
| `type` | Pointer shape | 'Marker' \| 'Bar' |
| `markerType` | Marker appearance | 'Circle' \| 'Triangle' \| 'Diamond' \| 'Rectangle' |
| `value` | Pointer position | 0-100 (numeric) |
| `width` | Pointer thickness | 2-20 (pixels) |
| `color` | Fill color | '#FF0000', 'red' |
| `startValue` | Range start | numeric value |
| `endValue` | Range end | numeric value |
