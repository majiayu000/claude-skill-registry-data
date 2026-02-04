---
name: chartjs-developers
description: This skill should be used when the user asks "Chart.js plugin", "custom Chart.js plugin", "Chart.js plugin hooks", "Chart.js beforeDraw", "Chart.js afterDraw", "custom chart type", "extend Chart.js", "Chart.js API", "Chart.js update", "Chart.js destroy", "Chart.js methods", "Chart.js events", "Chart.js canvas", "Chart.js TypeScript", "custom scale", "Chart.js DatasetController", "Chart.js Scale", or needs help creating custom Chart.js v4.5.1 plugins, extensions, custom chart types, custom scales, or using the API.
---

# Chart.js Developer Guide (v4.5.1)

Advanced guide for creating custom plugins, extending Chart.js, and using the API.

## Chart Instance API

### Creating a Chart

```javascript
const chart = new Chart(ctx, {
  type: 'bar',
  data: { /* ... */ },
  options: { /* ... */ }
});
```

### Chart Methods

```javascript
// Update chart
chart.update();                      // With animation
chart.update('none');                // Without animation
chart.update('active');              // Only animate active elements

// Data manipulation
chart.data.datasets[0].data.push(newValue);
chart.data.labels.push(newLabel);
chart.update();

// Resize
chart.resize();
chart.resize(width, height);

// Reset to original state
chart.reset();

// Destroy chart instance
chart.destroy();

// Convert to image
const base64Image = chart.toBase64Image();
const base64Image = chart.toBase64Image('image/png', 1.0);

// Show/hide datasets
chart.hide(datasetIndex);
chart.show(datasetIndex);
chart.isDatasetVisible(datasetIndex);
chart.setDatasetVisibility(datasetIndex, visible);

// Toggle data visibility (pie, doughnut, polar, bar)
chart.toggleDataVisibility(index);
chart.getDataVisibility(index);

// Animation control
chart.stop();                        // Stop current animation
chart.render();                      // Redraw without updating data
chart.clear();                       // Clear canvas

// Active elements
chart.setActiveElements([{ datasetIndex: 0, index: 1 }]);

// Dataset info
chart.getVisibleDatasetCount();
chart.getSortedVisibleDatasetMetas();

// Get elements at position
const elements = chart.getElementsAtEventForMode(
  event,
  'nearest',
  { intersect: true },
  true
);

// Get dataset metadata
const meta = chart.getDatasetMeta(datasetIndex);
```

## Creating Custom Plugins

Plugins extend Chart.js functionality through lifecycle hooks.

### Basic Plugin Structure

```javascript
const myPlugin = {
  id: 'myPlugin',

  // Called when plugin is installed
  install(chart, args, options) {},

  // Called when plugin is started
  start(chart, args, options) {},

  // Called when plugin is stopped
  stop(chart, args, options) {},

  // Called when plugin is uninstalled
  uninstall(chart, args, options) {},

  // Lifecycle hooks
  beforeInit(chart, args, options) {},
  afterInit(chart, args, options) {},
  beforeUpdate(chart, args, options) {},
  afterUpdate(chart, args, options) {},
  beforeDraw(chart, args, options) {},
  afterDraw(chart, args, options) {},
  beforeDatasetsDraw(chart, args, options) {},
  afterDatasetsDraw(chart, args, options) {},
  beforeDatasetDraw(chart, args, options) {},
  afterDatasetDraw(chart, args, options) {},
  beforeEvent(chart, args, options) {},
  afterEvent(chart, args, options) {},
  beforeDestroy(chart, args, options) {},
  afterDestroy(chart, args, options) {},

  // Default options
  defaults: {
    color: 'red'
  }
};
```

### Using Plugins

```javascript
// Per-chart (inline plugin)
new Chart(ctx, {
  plugins: [myPlugin],
  options: {
    plugins: {
      myPlugin: {
        color: 'blue'
      }
    }
  }
});

// Global registration
Chart.register(myPlugin);

// Disable for specific chart
options: {
  plugins: {
    myPlugin: false
  }
}
```

### Example: Canvas Background Plugin

```javascript
const canvasBackgroundPlugin = {
  id: 'canvasBackground',

  beforeDraw(chart, args, options) {
    const { ctx, chartArea: { left, top, width, height } } = chart;

    ctx.save();
    ctx.fillStyle = options.color || 'white';
    ctx.fillRect(left, top, width, height);
    ctx.restore();
  },

  defaults: {
    color: 'white'
  }
};

// Usage
new Chart(ctx, {
  plugins: [canvasBackgroundPlugin],
  options: {
    plugins: {
      canvasBackground: {
        color: '#f0f0f0'
      }
    }
  }
});
```

### Example: Chart Area Border Plugin

```javascript
const chartAreaBorderPlugin = {
  id: 'chartAreaBorder',

  beforeDraw(chart, args, options) {
    const { ctx, chartArea: { left, top, width, height } } = chart;

    ctx.save();
    ctx.strokeStyle = options.borderColor || 'black';
    ctx.lineWidth = options.borderWidth || 1;
    ctx.setLineDash(options.borderDash || []);
    ctx.strokeRect(left, top, width, height);
    ctx.restore();
  },

  defaults: {
    borderColor: 'black',
    borderWidth: 1,
    borderDash: []
  }
};
```

### Example: Crosshair Plugin

```javascript
const crosshairPlugin = {
  id: 'crosshair',

  afterDraw(chart, args, options) {
    if (chart._active && chart._active.length) {
      const activePoint = chart._active[0];
      const { ctx } = chart;
      const { x, y } = activePoint.element;
      const { top, bottom, left, right } = chart.chartArea;

      ctx.save();
      ctx.beginPath();
      ctx.setLineDash([5, 5]);
      ctx.strokeStyle = options.color || 'gray';
      ctx.lineWidth = options.width || 1;

      // Vertical line
      ctx.moveTo(x, top);
      ctx.lineTo(x, bottom);

      // Horizontal line
      ctx.moveTo(left, y);
      ctx.lineTo(right, y);

      ctx.stroke();
      ctx.restore();
    }
  }
};
```

## Plugin Lifecycle Hooks

### Initialization Hooks

| Hook | When Called |
|------|-------------|
| `beforeInit` | Before chart initializes |
| `afterInit` | After chart initializes |

### Update Hooks

| Hook | When Called |
|------|-------------|
| `beforeUpdate` | Before chart updates |
| `afterUpdate` | After chart updates |
| `beforeLayout` | Before layout calculations |
| `afterLayout` | After layout calculations |
| `beforeDataLimits` | Before data limits are determined |
| `afterDataLimits` | After data limits are determined |
| `beforeBuildTicks` | Before ticks are built |
| `afterBuildTicks` | After ticks are built |

### Render Hooks

| Hook | When Called |
|------|-------------|
| `beforeRender` | Before rendering starts |
| `afterRender` | After rendering completes |
| `beforeDraw` | Before chart draws |
| `afterDraw` | After chart draws |
| `beforeDatasetsDraw` | Before all datasets draw |
| `afterDatasetsDraw` | After all datasets draw |
| `beforeDatasetDraw` | Before each dataset draws |
| `afterDatasetDraw` | After each dataset draws |

### Event Hooks

| Hook | When Called |
|------|-------------|
| `beforeEvent` | Before event is processed |
| `afterEvent` | After event is processed |

### Destruction Hooks

| Hook | When Called |
|------|-------------|
| `beforeDestroy` | Before chart is destroyed |
| `afterDestroy` | After chart is destroyed |

## Accessing Chart Internals

```javascript
// Chart instance
const chart = Chart.getChart('myChart');  // By canvas ID
const chart = Chart.getChart(canvasElement);  // By element

// Static methods
Chart.register(plugin);              // Register globally
Chart.unregister(plugin);            // Unregister globally

// Chart area bounds
const { left, top, right, bottom, width, height } = chart.chartArea;

// Canvas context
const ctx = chart.ctx;

// Scales
const xScale = chart.scales.x;
const yScale = chart.scales.y;

// Convert between pixel and data values
const xPixel = xScale.getPixelForValue(dataValue);
const xValue = xScale.getValueForPixel(pixelPosition);

// Dataset metadata
const meta = chart.getDatasetMeta(0);
const elements = meta.data;  // Array of visual elements
```

## TypeScript Support

### Basic Types

```typescript
import { Chart, ChartConfiguration, ChartType } from 'chart.js';

const config: ChartConfiguration<'bar'> = {
  type: 'bar',
  data: {
    labels: ['A', 'B', 'C'],
    datasets: [{
      label: 'Dataset',
      data: [1, 2, 3]
    }]
  }
};

const chart = new Chart(canvas, config);
```

### Custom Plugin Types

```typescript
import { Plugin, ChartType } from 'chart.js';

interface MyPluginOptions {
  color: string;
  enabled: boolean;
}

const myPlugin: Plugin<ChartType, MyPluginOptions> = {
  id: 'myPlugin',
  beforeDraw(chart, args, options) {
    // options is typed as MyPluginOptions
  },
  defaults: {
    color: 'red',
    enabled: true
  }
};

// Extend Chart.js types
declare module 'chart.js' {
  interface PluginOptionsByType<TType extends ChartType> {
    myPlugin?: MyPluginOptions;
  }
}
```

## Working with Canvas

```javascript
const myPlugin = {
  id: 'customDraw',

  afterDraw(chart) {
    const { ctx, chartArea } = chart;

    ctx.save();

    // Draw custom shape
    ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
    ctx.beginPath();
    ctx.arc(
      chartArea.left + chartArea.width / 2,
      chartArea.top + chartArea.height / 2,
      50,
      0,
      Math.PI * 2
    );
    ctx.fill();

    // Draw text
    ctx.font = '16px Arial';
    ctx.fillStyle = 'black';
    ctx.textAlign = 'center';
    ctx.fillText('Custom Text', chart.width / 2, chart.height / 2);

    ctx.restore();
  }
};
```

## Event Handling in Plugins

```javascript
const eventPlugin = {
  id: 'eventHandler',

  beforeEvent(chart, args, options) {
    const event = args.event;

    if (event.type === 'click') {
      console.log('Click at:', event.x, event.y);
    }

    // Return false to stop event propagation
    // return false;
  },

  afterEvent(chart, args, options) {
    if (args.changed) {
      // Chart needs to re-render
    }
  }
};
```

## Cancelling Plugin Execution

Return `false` from `before*` hooks to cancel:

```javascript
const conditionalPlugin = {
  id: 'conditional',

  beforeDraw(chart, args, options) {
    if (someCondition) {
      return false;  // Cancel draw
    }
  }
};
```

## Extending Chart.js

### Custom Chart Types

Extend `Chart.DatasetController` to create new chart types. See `references/custom-chart-types.md` for:

- DatasetController interface and required methods
- Extending built-in controllers (BarController, LineController, etc.)
- TypeScript typings for custom chart types

### Custom Scales

Extend `Chart.Scale` to create custom axis types. See `references/custom-scales.md` for:

- Scale interface and required methods
- Scale properties available during fitting
- Utility methods for pixel/value conversion

### Updating Charts

Charts can be updated dynamically after creation. See `references/updating-charts.md` for:

- Adding and removing data
- Mutating vs replacing options
- Update modes and animation control
