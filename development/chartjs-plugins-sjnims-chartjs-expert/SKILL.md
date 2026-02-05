---
name: chartjs-plugins
description: This skill should be used when the user asks "Chart.js plugins", "custom Chart.js plugin", "Chart.js plugin hooks", "beforeDraw plugin", "afterDraw plugin", "Chart.js plugin API", "register Chart.js plugin", "Chart.js plugin options", "Chart.js plugin lifecycle", "Chart.js plugin TypeScript", or needs help creating custom plugins for Chart.js v4.5.1.
---

# Chart.js Custom Plugins (v4.5.1)

Complete guide to creating and using custom plugins in Chart.js.

## Plugin Basics

Plugins are the most efficient way to customize or change Chart.js default behavior. Plugins provide hooks into the chart lifecycle to execute custom code.

### Plugin Types

| Type | Scope | Use Case |
|------|-------|----------|
| **Inline** | Single chart instance | One-off customizations |
| **Shared** | Multiple charts | Reusable across specific charts |
| **Global** | All charts | Site-wide defaults |

### Inline Plugins

Define directly in chart config:

```javascript
const chart = new Chart(ctx, {
  type: 'bar',
  data: data,
  plugins: [{
    id: 'myInlinePlugin',
    beforeDraw: (chart, args, options) => {
      // Custom drawing logic
    }
  }]
});
```

**Limitations**: Cannot be registered globally, not reusable.

### Shared Plugins

Define once, use in multiple charts:

```javascript
const myPlugin = {
  id: 'mySharedPlugin',
  beforeDraw: (chart, args, options) => {
    // Custom logic
  }
};

const chart1 = new Chart(ctx1, {
  plugins: [myPlugin]
});

const chart2 = new Chart(ctx2, {
  plugins: [myPlugin]
});
```

### Global Plugins

Register once, apply to all charts:

```javascript
const myPlugin = {
  id: 'myGlobalPlugin',
  beforeDraw: (chart, args, options) => {
    // Custom logic
  }
};

Chart.register(myPlugin);

// Now all charts use this plugin automatically
const chart = new Chart(ctx, { type: 'bar', data: data });
```

## Plugin Structure

### Required Properties

```javascript
const plugin = {
  id: 'unique-plugin-id',  // Required for configuration

  // Lifecycle hooks (all optional)
  beforeInit: (chart, args, options) => {},
  afterInit: (chart, args, options) => {},
  beforeUpdate: (chart, args, options) => {},
  afterUpdate: (chart, args, options) => {},
  beforeDraw: (chart, args, options) => {},
  afterDraw: (chart, args, options) => {},
  // ... more hooks

  // Default options (optional)
  defaults: {
    color: 'red',
    lineWidth: 2
  }
};
```

### Plugin ID Naming

Follow npm package naming conventions:

- Lowercase letters, numbers, hyphens only
- No leading dot or underscore
- Should be descriptive
- Prefix with `chartjs-plugin-` for public packages

## Plugin Lifecycle Hooks

### Initialization Hooks

| Hook | When | Cancelable | Use Case |
|------|------|------------|----------|
| `beforeInit` | Before chart initialization | No | Set up data structures |
| `afterInit` | After chart initialization | No | Access initialized chart |

### Update Hooks

| Hook | When | Cancelable | Use Case |
|------|------|------------|----------|
| `beforeUpdate` | Before chart update | Yes | Modify data before update |
| `afterUpdate` | After chart update | No | React to data changes |
| `beforeLayout` | Before layout calculation | Yes | Modify layout constraints |
| `afterLayout` | After layout calculation | No | Access calculated layout |
| `beforeDatasetsUpdate` | Before datasets update | Yes | Intercept dataset updates |
| `afterDatasetsUpdate` | After datasets update | No | React to dataset changes |

### Render Hooks

| Hook | When | Cancelable | Use Case |
|------|------|------------|----------|
| `beforeRender` | Before rendering | Yes | Skip render conditionally |
| `beforeDraw` | Before drawing chart | Yes | Draw custom backgrounds |
| `afterDraw` | After drawing chart | No | Draw overlays, annotations |
| `afterRender` | After rendering complete | No | Post-render operations |

### Event Hooks

| Hook | When | Use Case |
|------|------|----------|
| `beforeEvent` | Before event processing | Intercept/modify events |
| `afterEvent` | After event processing | React to user interactions |

### Destruction Hook

| Hook | When | Use Case |
|------|------|----------|
| `afterDestroy` | After chart destroyed | Clean up resources |

## Plugin Configuration

### Defining Options

Configure plugins via `options.plugins.{plugin-id}`:

```javascript
const plugin = {
  id: 'backgroundPlugin',
  beforeDraw: (chart, args, options) => {
    const {ctx} = chart;
    ctx.save();
    ctx.fillStyle = options.color || 'white';
    ctx.fillRect(0, 0, chart.width, chart.height);
    ctx.restore();
  },
  defaults: {
    color: 'lightGreen'
  }
};

Chart.register(plugin);

const chart = new Chart(ctx, {
  options: {
    plugins: {
      backgroundPlugin: {
        color: 'lightBlue'  // Override default
      }
    }
  }
});
```

### Disabling Plugins

Disable global plugin for specific chart:

```javascript
const chart = new Chart(ctx, {
  options: {
    plugins: {
      myPlugin: false  // Disable this plugin
    }
  }
});
```

Disable all plugins:

```javascript
const chart = new Chart(ctx, {
  options: {
    plugins: false  // Disable all plugins
  }
});
```

## Common Plugin Patterns

### Canvas Background Color

```javascript
const canvasBackgroundColor = {
  id: 'canvasBackgroundColor',
  beforeDraw: (chart, args, options) => {
    const {ctx, chartArea} = chart;
    ctx.save();
    ctx.globalCompositeOperation = 'destination-over';
    ctx.fillStyle = options.color || 'white';
    ctx.fillRect(0, 0, chart.width, chart.height);
    ctx.restore();
  }
};
```

### Chart Area Border

```javascript
const chartAreaBorder = {
  id: 'chartAreaBorder',
  beforeDraw(chart, args, options) {
    const {ctx, chartArea: {left, top, width, height}} = chart;
    ctx.save();
    ctx.strokeStyle = options.borderColor;
    ctx.lineWidth = options.borderWidth;
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

### Custom Text Overlay

```javascript
const textOverlay = {
  id: 'textOverlay',
  afterDraw: (chart, args, options) => {
    const {ctx, chartArea: {left, right, top, bottom}} = chart;
    ctx.save();

    const centerX = (left + right) / 2;
    const centerY = (top + bottom) / 2;

    ctx.font = options.font || '20px Arial';
    ctx.fillStyle = options.color || 'black';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(options.text || '', centerX, centerY);

    ctx.restore();
  }
};
```

### Empty State Handler

```javascript
const emptyStatePlugin = {
  id: 'emptyState',
  afterDraw(chart, args, options) {
    const {datasets} = chart.data;
    let hasData = datasets.some(ds => ds.data.length > 0);

    if (!hasData) {
      const {ctx, chartArea: {left, top, right, bottom}} = chart;
      const centerX = (left + right) / 2;
      const centerY = (top + bottom) / 2;

      ctx.save();
      ctx.font = '16px Arial';
      ctx.fillStyle = 'gray';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(options.message || 'No data available', centerX, centerY);
      ctx.restore();
    }
  }
};
```

## Accessing Chart Elements

### Chart Object Properties

```javascript
beforeDraw: (chart, args, options) => {
  const {
    ctx,              // Canvas 2D context
    canvas,           // Canvas element
    width,            // Chart width
    height,           // Chart height
    chartArea,        // {left, top, right, bottom, width, height}
    scales,           // {x, y, r, ...}
    data,             // Chart data
    options,          // Chart options
    config            // Chart configuration
  } = chart;
}
```

### Scales and Coordinates

```javascript
afterDraw: (chart, args, options) => {
  const {scales: {x, y}} = chart;

  // Convert data value to pixel
  const pixelX = x.getPixelForValue(dataValue);
  const pixelY = y.getPixelForValue(dataValue);

  // Convert pixel to data value
  const dataX = x.getValueForPixel(pixelX);
  const dataY = y.getValueForPixel(pixelY);
}
```

## TypeScript Support

### Plugin Type Declaration

```typescript
import {ChartType, Plugin} from 'chart.js';

declare module 'chart.js' {
  interface PluginOptionsByType<TType extends ChartType> {
    myPlugin?: {
      color?: string;
      width?: number;
      enabled?: boolean;
    }
  }
}

const myPlugin: Plugin = {
  id: 'myPlugin',
  beforeDraw(chart, args, options) {
    // TypeScript now knows about options.color, options.width
    const color = options.color || 'red';
  }
};
```

## Best Practices

### Performance

- Use `beforeDraw`/`afterDraw` sparingly - called on every render
- Cache calculations in `afterUpdate` hooks
- Avoid heavy computations in render hooks
- Use `ctx.save()` and `ctx.restore()` to avoid side effects

### Error Handling

```javascript
const safePlugin = {
  id: 'safePlugin',
  afterDraw: (chart, args, options) => {
    try {
      // Plugin logic
    } catch (error) {
      console.error('Plugin error:', error);
    }
  }
};
```

### Conditional Rendering

```javascript
const conditionalPlugin = {
  id: 'conditionalPlugin',
  beforeDraw: (chart, args, options) => {
    if (!options.enabled) {
      return;  // Skip if disabled
    }
    // Draw logic
  }
};
```

## Additional Resources

- See `references/plugin-api.md` for complete hook reference
- See `examples/quadrants-plugin.md` for working quadrant background example
- See `examples/empty-state-plugin.md` for empty state handler example
