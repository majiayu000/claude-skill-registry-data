---
name: chartjs-advanced
description: This skill should be used when the user asks "Chart.js gradients", "Chart.js linear gradient", "Chart.js radial gradient", "custom Chart.js chart type", "extend Chart.js", "derived chart type", "custom Chart.js scale", "Chart.js programmatic events", "Chart.js setActiveElements", "Chart.js custom controller", or needs help with advanced Chart.js v4.5.1 techniques.
---

# Chart.js Advanced Techniques (v4.5.1)

Guide to advanced Chart.js customization including gradients, custom chart types, and programmatic control.

## Gradients

Create visual depth with linear and radial gradients.

### Linear Gradients

```javascript
const ctx = document.getElementById('myChart').getContext('2d');

// Create gradient
const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(75, 192, 192, 1)');
gradient.addColorStop(0.5, 'rgba(75, 192, 192, 0.5)');
gradient.addColorStop(1, 'rgba(75, 192, 192, 0.1)');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Sales',
      data: [12, 19, 3, 5, 2],
      backgroundColor: gradient,
      borderColor: 'rgb(75, 192, 192)',
      fill: true
    }]
  }
});
```

### Dynamic Gradients (Responsive)

```javascript
function createGradient(ctx, chartArea) {
  const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
  gradient.addColorStop(0, 'rgba(54, 162, 235, 0)');
  gradient.addColorStop(1, 'rgba(54, 162, 235, 1)');
  return gradient;
}

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{
      label: 'Revenue',
      data: [10, 20, 30],
      backgroundColor: function(context) {
        const chart = context.chart;
        const {ctx, chartArea} = chart;
        if (!chartArea) {
          return null;  // Chart not initialized yet
        }
        return createGradient(ctx, chartArea);
      }
    }]
  }
});
```

### Radial Gradients

```javascript
function createRadialGradient(ctx, chartArea) {
  const width = chartArea.right - chartArea.left;
  const height = chartArea.bottom - chartArea.top;
  const centerX = (chartArea.left + chartArea.right) / 2;
  const centerY = (chartArea.top + chartArea.bottom) / 2;
  const r = Math.min(width, height) / 2;

  const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, r);
  gradient.addColorStop(0, 'rgba(255, 99, 132, 1)');
  gradient.addColorStop(0.5, 'rgba(255, 99, 132, 0.5)');
  gradient.addColorStop(1, 'rgba(255, 99, 132, 0)');

  return gradient;
}

// Use with pie/doughnut charts
datasets: [{
  data: [300, 50, 100],
  backgroundColor: function(context) {
    const chart = context.chart;
    const {ctx, chartArea} = chart;
    if (!chartArea) return null;
    return createRadialGradient(ctx, chartArea);
  }
}]
```

### Multi-Dataset Gradients

```javascript
const gradients = [
  { start: 'rgba(255, 99, 132, 1)', end: 'rgba(255, 99, 132, 0.1)' },
  { start: 'rgba(54, 162, 235, 1)', end: 'rgba(54, 162, 235, 0.1)' },
  { start: 'rgba(255, 206, 86, 1)', end: 'rgba(255, 206, 86, 0.1)' }
];

datasets: gradients.map((colors, i) => ({
  label: `Dataset ${i + 1}`,
  data: data[i],
  backgroundColor: function(context) {
    const chart = context.chart;
    const {ctx, chartArea} = chart;
    if (!chartArea) return null;

    const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    gradient.addColorStop(0, colors.end);
    gradient.addColorStop(1, colors.start);
    return gradient;
  }
}))
```

## Custom Chart Types

Extend existing chart types or create new ones.

### Extending Bar Controller

```javascript
import {Chart, BarController} from 'chart.js';

class CustomBarController extends BarController {
  // Override draw method
  draw() {
    super.draw();

    // Add custom drawing
    const meta = this.getMeta();
    const ctx = this.chart.ctx;

    meta.data.forEach(bar => {
      const {x, y, base, width} = bar.getProps(['x', 'y', 'base', 'width']);

      // Draw custom element
      ctx.save();
      ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
      ctx.fillRect(x - width/2, y - 5, width, 5);
      ctx.restore();
    });
  }

  // Override update method
  update(mode) {
    const meta = this.getMeta();

    // Custom update logic
    this.updateElements(meta.data, 0, meta.data.length, mode);
  }
}

CustomBarController.id = 'customBar';
CustomBarController.defaults = {
  ...BarController.defaults,
  // Add custom default options
  customOption: true
};

Chart.register(CustomBarController);

// Use custom chart type
const chart = new Chart(ctx, {
  type: 'customBar',
  data: data
});
```

### Creating Derived Bubble Chart

```javascript
import {Chart, BubbleController} from 'chart.js';

class DerivedBubble extends BubbleController {
  draw() {
    // Call parent draw
    super.draw();

    // Add custom decoration
    const meta = this.getMeta();
    const firstPoint = meta.data[0];
    const {x, y} = firstPoint.getProps(['x', 'y']);
    const {radius} = firstPoint.options;

    const ctx = this.chart.ctx;
    ctx.save();
    ctx.strokeStyle = this.options.boxStrokeStyle;
    ctx.lineWidth = 2;
    ctx.strokeRect(x - radius, y - radius, 2 * radius, 2 * radius);
    ctx.restore();
  }
}

DerivedBubble.id = 'derivedBubble';
DerivedBubble.defaults = {
  boxStrokeStyle: 'red'
};

Chart.register(DerivedBubble);
```

## Custom Scales

Create custom axis types.

### Logarithmic Base-2 Scale

```javascript
import {Chart, Scale} from 'chart.js';

class Log2Axis extends Scale {
  constructor(cfg) {
    super(cfg);
    this.start = undefined;
    this.end = undefined;
  }

  parse(raw, index) {
    const value = +raw;
    return isFinite(value) ? value : null;
  }

  determineDataLimits() {
    const {min, max} = this.getMinMax(true);
    this.min = min;
    this.max = max;
  }

  buildTicks() {
    const ticks = [];
    let power = Math.floor(Math.log2(this.min));
    let value = Math.pow(2, power);

    while (value < this.max) {
      ticks.push({value});
      power++;
      value = Math.pow(2, power);
    }

    return ticks;
  }

  getPixelForValue(value) {
    if (value === undefined || value === 0) {
      value = this.min;
    }

    const decimal = (Math.log2(value) - Math.log2(this.min)) / (Math.log2(this.max) - Math.log2(this.min));
    return this.getPixelForDecimal(decimal);
  }

  getValueForPixel(pixel) {
    const decimal = this.getDecimalForPixel(pixel);
    return Math.pow(2, Math.log2(this.min) + decimal * (Math.log2(this.max) - Math.log2(this.min)));
  }
}

Log2Axis.id = 'log2';
Log2Axis.defaults = {};

Chart.register(Log2Axis);

// Use custom scale
const chart = new Chart(ctx, {
  type: 'line',
  data: data,
  options: {
    scales: {
      y: {
        type: 'log2'
      }
    }
  }
});
```

## Programmatic Interactions

Control chart interactions via API.

### Trigger Hover Programmatically

```javascript
function triggerHover(chart, datasetIndex, index) {
  if (chart.getActiveElements().length > 0) {
    // Clear active elements
    chart.setActiveElements([]);
  } else {
    // Set active elements
    chart.setActiveElements([
      {datasetIndex: 0, index: 0},
      {datasetIndex: 1, index: 0}
    ]);
  }
  chart.update();
}

// Usage
triggerHover(chart, 0, 2);  // Highlight first dataset, third point
```

### Trigger Tooltip Programmatically

```javascript
function triggerTooltip(chart, datasetIndex, index) {
  const tooltip = chart.tooltip;

  if (tooltip.getActiveElements().length > 0) {
    // Hide tooltip
    tooltip.setActiveElements([], {x: 0, y: 0});
  } else {
    // Show tooltip
    const chartArea = chart.chartArea;
    tooltip.setActiveElements([
      {datasetIndex, index}
    ], {
      x: (chartArea.left + chartArea.right) / 2,
      y: (chartArea.top + chartArea.bottom) / 2
    });
  }

  chart.update();
}

// Usage
triggerTooltip(chart, 0, 3);  // Show tooltip for first dataset, fourth point
```

### Simulate Click Event

```javascript
function simulateClick(chart, x, y) {
  const event = {
    type: 'click',
    x: x,
    y: y,
    native: {
      clientX: x,
      clientY: y
    }
  };

  chart.handleEvent(event);
}

// Click center of chart
const chartArea = chart.chartArea;
const centerX = (chartArea.left + chartArea.right) / 2;
const centerY = (chartArea.top + chartArea.bottom) / 2;
simulateClick(chart, centerX, centerY);
```

## Dynamic Updates

Advanced data update patterns.

### Smooth Data Streaming

```javascript
function addDataPoint(chart, label, data) {
  chart.data.labels.push(label);
  chart.data.datasets.forEach((dataset, i) => {
    dataset.data.push(data[i]);
  });

  // Keep last 20 points
  if (chart.data.labels.length > 20) {
    chart.data.labels.shift();
    chart.data.datasets.forEach(dataset => {
      dataset.data.shift();
    });
  }

  chart.update('active');  // Use active transition for smooth updates
}

// Stream data every second
setInterval(() => {
  addDataPoint(chart, new Date().toLocaleTimeString(), [
    Math.random() * 100,
    Math.random() * 100
  ]);
}, 1000);
```

### Update Without Animation

```javascript
// No animation
chart.data.datasets[0].data = [10, 20, 30, 40];
chart.update('none');

// Or disable for single update
chart.update({duration: 0});
```

## Performance Optimization

### Data Decimation

```javascript
options: {
  plugins: {
    decimation: {
      enabled: true,
      algorithm: 'lttb',  // Largest Triangle Three Buckets
      samples: 500        // Target number of samples
    }
  }
}
```

### Disable Animations for Large Datasets

```javascript
const dataPoints = data.datasets[0].data.length;

options: {
  animation: dataPoints > 1000 ? false : {
    duration: 1000,
    easing: 'easeOutQuart'
  }
}
```

## Additional Resources

### Examples

- `examples/gradient-backgrounds.html` - Gradient pattern library (vertical, horizontal, radial, diagonal)
- `examples/custom-chart-type.html` - Complete custom controller example (DerivedBubble)

### References

- `references/controller-api.md` - Chart controller API and TypeScript declarations
- `references/scale-api.md` - Scale API for custom axis types
- `references/performance-optimization.md` - Comprehensive performance tuning guide
