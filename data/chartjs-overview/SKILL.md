---
name: chartjs-overview
description: This skill should be used when the user asks "how to install Chart.js", "Chart.js setup", "getting started with Chart.js", "Chart.js CDN", "Chart.js npm install", "tree-shaking Chart.js", "Chart.js bundle optimization", "import Chart.js", "Chart.js module loaders", "Chart.js CommonJS", "Chart.js RequireJS", "chart.js/auto vs manual registration", "Chart.js defaults", "update chart data", "chart instance methods", "destroy chart", "Chart.js helpers", "resize chart", "responsive chart configuration", "Chart.js global configuration", "getRelativePosition", or needs help with initial Chart.js v4.5.1 project setup, configuration, and chart manipulation.
---

# Chart.js Overview (v4.5.1)

Guidance for installing, configuring, and optimizing Chart.js v4.5.1 in web applications.

## Installation

### npm Installation

Install Chart.js via npm:

```bash
npm install chart.js
```

### CDN Installation

Include Chart.js via CDN in HTML:

```html
<!-- jsDelivr -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- CDNJS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.1/chart.umd.min.js"></script>
```

## Basic Chart Creation

Create a chart with minimal configuration:

```html
<div>
  <canvas id="myChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
</script>
```

Key requirements:
- A `<canvas>` element with an id
- Wrap canvas in a container `<div>` for responsive sizing
- Instantiate `new Chart(ctx, config)` with type, data, and options

## Module Bundlers (Webpack, Rollup, Vite, Parcel)

### Quick Start (All Components)

Import everything for rapid prototyping:

```javascript
import Chart from 'chart.js/auto';

new Chart(ctx, {
  type: 'bar',
  data: { /* ... */ }
});
```

**Warning**: `chart.js/auto` disables tree-shaking. Use manual registration for production.

### Bundle Optimization (Tree-Shaking)

Register only needed components for smaller bundles:

```javascript
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Legend,
  Tooltip
} from 'chart.js';

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Legend,
  Tooltip
);

new Chart(ctx, {
  type: 'bar',
  data: { /* ... */ }
});
```

See `references/tree-shaking.md` for complete component lists per chart type.

## Module Loader Support

### CommonJS

Use dynamic import in CommonJS modules:

```javascript
const { Chart } = await import('chart.js');
```

### RequireJS (AMD)

Require the UMD build:

```javascript
require(['path/to/chartjs/dist/chart.umd.min.js'], function(Chart) {
  const myChart = new Chart(ctx, { /* ... */ });
});
```

### ES Modules (Script Tag)

Use type="module" with ESM CDN for modern browsers:

```html
<script type="module">
  import Chart from 'https://cdn.jsdelivr.net/npm/chart.js/+esm';

  new Chart(ctx, {
    type: 'bar',
    data: { /* ... */ }
  });
</script>
```

**Tree-shaking with ES Modules:**

```html
<script type="module">
  import {
    Chart,
    BarController,
    BarElement,
    CategoryScale,
    LinearScale
  } from 'https://cdn.jsdelivr.net/npm/chart.js/+esm';

  Chart.register(BarController, BarElement, CategoryScale, LinearScale);

  new Chart(ctx, {
    type: 'bar',
    data: { /* ... */ }
  });
</script>
```

See `examples/production-bundle.html` for complete working examples.

## Configuration Structure

Every Chart.js configuration follows this structure:

```javascript
const config = {
  type: 'line',           // Chart type
  data: {                 // Data and datasets
    labels: [],
    datasets: [{ data: [] }]
  },
  options: {},            // Chart options
  plugins: []             // Inline plugins
};

new Chart(ctx, config);
```

## Global Configuration

Set defaults for all charts using `Chart.defaults`:

```javascript
// Set font defaults globally
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 14;

// Set interaction mode globally
Chart.defaults.interaction.mode = 'nearest';
Chart.defaults.interaction.intersect = false;

// Set default for all line charts
Chart.defaults.datasets.line.showLine = false;
Chart.defaults.datasets.line.tension = 0.4;

// Set default for linear scales
Chart.defaults.scales.linear.min = 0;

// Plugin defaults
Chart.defaults.plugins.legend.position = 'bottom';
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(0, 0, 0, 0.8)';
```

**Important:** Changes to `Chart.defaults` only affect charts created **after** the change.

See `references/configuration-patterns.md` for advanced global configuration patterns.

## Helper Functions

Import helpers separately from the helpers package for event handling and utilities:

```javascript
import Chart from 'chart.js/auto';
import { getRelativePosition } from 'chart.js/helpers';

const chart = new Chart(ctx, {
  type: 'line',
  data: data,
  options: {
    onClick: (e) => {
      // Convert event position to chart coordinates
      const canvasPosition = getRelativePosition(e, chart);

      // Get data values at click position
      const dataX = chart.scales.x.getValueForPixel(canvasPosition.x);
      const dataY = chart.scales.y.getValueForPixel(canvasPosition.y);

      console.log(`Clicked at: (${dataX}, ${dataY})`);
    }
  }
});
```

**Available helpers:** `getRelativePosition`, `isNullOrUndef`, `isArray`, `isObject`, `valueOrDefault`, `uid`

See `references/configuration-patterns.md` for complete helper function reference.

## Chart Instance Methods

Common methods available on chart instances for dynamic updates and manipulation:

```javascript
const chart = new Chart(ctx, config);

// Update chart with new data
chart.data.datasets[0].data = [1, 2, 3, 4, 5];
chart.update();              // Default animation
chart.update('none');        // No animation (faster)
chart.update('active');      // Only active elements animate

// Resize chart
chart.resize();              // Auto-detect from container
chart.resize(800, 400);      // Set specific dimensions

// Reset to original state
chart.reset();

// Destroy chart instance (important for cleanup)
chart.destroy();

// Export chart as image
const image = chart.toBase64Image();                    // PNG
const jpeg = chart.toBase64Image('image/jpeg', 0.8);   // JPEG 80% quality

// Get elements at event position
const elements = chart.getElementsAtEventForMode(
  event,
  'nearest',
  { intersect: true },
  true
);

// Toggle dataset visibility
chart.hide(datasetIndex);
chart.show(datasetIndex);
chart.isDatasetVisible(datasetIndex);
```

**Performance tip:** Use `update('none')` for frequent updates to disable animation.

See `references/instance-methods.md` for complete method documentation and patterns.

## Responsiveness

Charts are responsive by default, automatically resizing with their container:

```javascript
new Chart(ctx, {
  type: 'bar',
  data: data,
  options: {
    responsive: true,           // Resize with container (default: true)
    maintainAspectRatio: true,  // Keep aspect ratio (default: true)
    aspectRatio: 2,             // Width/height ratio (default: 2, radial: 1)
    resizeDelay: 0,             // Debounce resize updates in ms (default: 0)

    // Callback when chart resizes
    onResize: (chart, size) => {
      console.log(`Resized to ${size.width}x${size.height}`);
    }
  }
});
```

**Container-based sizing:** Chart.js gets dimensions from the canvas's parent container:

```html
<div style="width: 80%; max-width: 1200px;">
  <canvas id="myChart"></canvas>
</div>
```

**Flexbox/Grid containers:** Set `min-width: 0` on flex/grid children to prevent overflow:

```html
<div style="display: grid; grid-template-columns: 1fr 1fr;">
  <div style="min-width: 0;"><canvas id="chart1"></canvas></div>
  <div style="min-width: 0;"><canvas id="chart2"></canvas></div>
</div>
```

**Custom aspect ratios:**

```javascript
options: {
  aspectRatio: 1    // Square (radar, polar area)
  aspectRatio: 3    // Wide (timelines)
  aspectRatio: 0.5  // Tall (rankings)
}
```

**Fixed-size charts:**

```javascript
options: {
  responsive: false,
  maintainAspectRatio: false
}
```

```html
<canvas id="myChart" width="600" height="400"></canvas>
```

See `references/configuration-patterns.md` for responsive patterns and media query-like behavior.

## Additional Resources

**Reference Documentation:**
- `references/tree-shaking.md` - Complete component registration guide for all chart types
- `references/instance-methods.md` - Chart instance methods, animation modes, and patterns
- `references/configuration-patterns.md` - Global defaults, helpers, responsive patterns

**Working Examples:**
- `examples/basic-bar-chart.html` - Bar chart examples (simple, horizontal, stacked)
- `examples/multi-dataset-line.html` - Multi-dataset and area charts with real-time updates
- `examples/production-bundle.html` - Tree-shaken builds with ESM imports
