---
name: chartjs-configuration
description: This skill should be used when the user asks "Chart.js options", "Chart.js animations", "Chart.js legend", "Chart.js tooltip", "Chart.js title", "disable Chart.js animation", "customize Chart.js tooltip", "Chart.js responsive", "Chart.js aspect ratio", "Chart.js interactions", "Chart.js hover", "Chart.js click events", "Chart.js layout", "Chart.js padding", "Chart.js font", "Chart.js colors", "Chart.js external tooltip", "Chart.js custom legend", "Chart.js transitions", or needs help configuring Chart.js v4.5.1 options, plugins, and styling.
---

# Chart.js Configuration (v4.5.1)

Comprehensive guide to configuring Chart.js options, animations, legends, tooltips, and interactions.

## Configuration Structure

```javascript
const config = {
  type: 'line',
  data: { /* datasets, labels */ },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 2,
    events: ['mousemove', 'mouseout', 'click', 'touchstart', 'touchmove'],
    onClick: (event, elements, chart) => { /* handle click */ },
    onHover: (event, elements, chart) => { /* handle hover */ },
    plugins: {
      legend: { /* legend options */ },
      tooltip: { /* tooltip options */ },
      title: { /* title options */ }
    },
    scales: { /* axis options */ },
    animation: { /* animation options */ },
    interaction: { /* interaction options */ },
    layout: { /* layout options */ }
  },
  plugins: []  // Inline plugins
};
```

## Responsive Configuration

Namespace: `options`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `responsive` | `boolean` | `true` | Resize with container |
| `maintainAspectRatio` | `boolean` | `true` | Keep aspect ratio |
| `aspectRatio` | `number` | `2` (radial: `1`) | Width/height ratio |
| `resizeDelay` | `number` | `0` | Debounce resize (ms) |
| `onResize` | `function` | `null` | Callback on resize |

### Container Requirements

Chart.js requires the container to be **relatively positioned** and **dedicated to the chart canvas only**:

```html
<div class="chart-container" style="position: relative; height: 40vh; width: 80vw">
  <canvas id="chart"></canvas>
</div>
```

### Flexbox/Grid Layout

To prevent overflow in flexbox/grid layouts, set `min-width: 0` on the container:

```html
<div class="grid-container" style="display: grid">
  <div class="chart-container" style="min-width: 0">
    <canvas id="chart"></canvas>
  </div>
</div>
```

For fixed-size charts, set `responsive: false` and define canvas dimensions directly.

See `examples/responsive-chart.html` for complete responsive setup including print handling.

## Legend Configuration

Namespace: `options.plugins.legend`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `display` | `boolean` | `true` | Show legend |
| `position` | `string` | `'top'` | `top`, `bottom`, `left`, `right`, `chartArea` |
| `align` | `string` | `'center'` | `start`, `center`, `end` |
| `reverse` | `boolean` | `false` | Reverse order |
| `maxHeight` | `number` | - | Maximum height (px) |
| `maxWidth` | `number` | - | Maximum width (px) |
| `fullSize` | `boolean` | `true` | Take full canvas width/height |
| `rtl` | `boolean` | - | Right-to-left rendering |
| `onClick` | `function` | - | Click handler |
| `onHover` | `function` | - | Hover handler |
| `onLeave` | `function` | - | Mouse leave handler |

### Legend Labels

```javascript
labels: {
  boxWidth: 40,
  boxHeight: 12,
  color: '#666',
  font: { size: 12 },
  padding: 10,
  usePointStyle: false,
  pointStyle: 'circle',
  filter: (item, data) => item.text !== 'Hidden',  // Filter items
  sort: (a, b, data) => a.text.localeCompare(b.text)  // Sort items
}
```

### Hide Legend

```javascript
plugins: { legend: { display: false } }
```

For custom click handlers and Legend Item Interface, see `references/legend-customization.md`.

## Tooltip Configuration

Namespace: `options.plugins.tooltip`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | `boolean` | `true` | Enable on-canvas tooltips |
| `external` | `function` | `null` | External (HTML) tooltip handler |
| `mode` | `string` | `interaction.mode` | `point`, `index`, `dataset`, `nearest` |
| `intersect` | `boolean` | `interaction.intersect` | Require intersection |
| `position` | `string` | `'average'` | `average`, `nearest`, or custom |
| `backgroundColor` | `Color` | `'rgba(0,0,0,0.8)'` | Background color |
| `padding` | `number` | `6` | Padding inside tooltip |
| `cornerRadius` | `number` | `6` | Border radius |
| `displayColors` | `boolean` | `true` | Show color boxes |

### Tooltip Callbacks

```javascript
callbacks: {
  title: (items) => items[0].label,
  label: (context) => `${context.dataset.label}: ${context.parsed.y}`,
  footer: (items) => `Total: ${items.reduce((a, b) => a + b.parsed.y, 0)}`
}
```

Additional callbacks: `beforeTitle`, `afterTitle`, `beforeBody`, `afterBody`, `beforeLabel`, `afterLabel`, `labelColor`, `labelTextColor`, `labelPointStyle`, `beforeFooter`, `afterFooter`.

### Disable Tooltips

```javascript
plugins: { tooltip: { enabled: false } }
```

For external HTML tooltips, custom positioners, and the full Tooltip Model, see `references/tooltip-customization.md` and `examples/custom-tooltip.html`.

## Title Configuration

Namespace: `options.plugins.title`

```javascript
plugins: {
  title: {
    display: true,
    text: 'Chart Title',
    color: '#666',
    font: { size: 16, weight: 'bold' },
    padding: { top: 10, bottom: 10 },
    align: 'center',      // start, center, end
    position: 'top',      // top, bottom, left, right
    fullSize: true        // Take full canvas width
  },
  subtitle: {
    display: true,
    text: 'Chart Subtitle',
    color: '#999',
    font: { size: 12 }
  }
}
```

## Animation Configuration

Chart.js animation has three configuration levels:

| Key | Namespace | Purpose |
|-----|-----------|---------|
| `animation` | `options.animation` | Base animation settings |
| `animations` | `options.animations` | Per-property animations |
| `transitions` | `options.transitions` | Mode-specific animations |

### Base Animation

```javascript
animation: {
  duration: 1000,
  easing: 'easeOutQuart',
  delay: 0,
  loop: false,
  onProgress: (animation) => { /* during animation */ },
  onComplete: (animation) => { /* when complete */ }
}
```

### Per-Property Animations

```javascript
animations: {
  tension: {
    duration: 1000,
    easing: 'linear',
    from: 1,
    to: 0,
    loop: true
  },
  colors: {
    type: 'color',
    duration: 500,
    from: 'transparent'
  }
}
```

### Transitions

Control animations for specific modes (`active`, `hide`, `show`, `reset`, `resize`):

```javascript
transitions: {
  active: { animation: { duration: 400 } },
  resize: { animation: { duration: 0 } },
  show: {
    animations: {
      colors: { from: 'transparent' },
      visible: { type: 'boolean', duration: 0 }
    }
  }
}
```

### Disable Animations

```javascript
animation: false  // Disable all
// Or per-mode:
transitions: { active: { animation: { duration: 0 } } }
```

### Easing Functions

`linear`, `easeInQuad`, `easeOutQuad`, `easeInOutQuad`, `easeInCubic`, `easeOutCubic`, `easeInOutCubic`, `easeInQuart`, `easeOutQuart`, `easeInOutQuart`, `easeInQuint`, `easeOutQuint`, `easeInOutQuint`, `easeInSine`, `easeOutSine`, `easeInOutSine`, `easeInExpo`, `easeOutExpo`, `easeInOutExpo`, `easeInCirc`, `easeOutCirc`, `easeInOutCirc`, `easeInElastic`, `easeOutElastic`, `easeInOutElastic`, `easeInBack`, `easeOutBack`, `easeInOutBack`, `easeInBounce`, `easeOutBounce`, `easeInOutBounce`

For animation callbacks and advanced patterns, see `references/advanced-animations.md`.

## Interaction Configuration

Namespace: `options.interaction`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `'nearest'` | How to find elements |
| `intersect` | `boolean` | `true` | Must intersect element |
| `axis` | `string` | `'x'` | `x`, `y`, `xy`, or `r` |
| `includeInvisible` | `boolean` | `false` | Include hidden elements |

### Interaction Modes

| Mode | Description |
|------|-------------|
| `'point'` | Elements at same position |
| `'index'` | Elements at same index |
| `'dataset'` | Elements in same dataset |
| `'nearest'` | Nearest element |
| `'x'` | Elements at same x-axis value |
| `'y'` | Elements at same y-axis value |

## Event Handling

Namespace: `options`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `events` | `string[]` | `['mousemove', 'mouseout', 'click', 'touchstart', 'touchmove']` | Browser events to listen for |
| `onClick` | `function` | `null` | Click handler over chart area |
| `onHover` | `function` | `null` | Hover handler over chart area |

```javascript
options: {
  events: ['click'],  // Only respond to clicks
  onClick: (event, elements, chart) => {
    if (elements.length > 0) {
      const { datasetIndex, index } = elements[0];
      console.log(chart.data.datasets[datasetIndex].data[index]);
    }
  },
  onHover: (event, elements, chart) => {
    chart.canvas.style.cursor = elements.length ? 'pointer' : 'default';
  }
}
```

### Convert Event to Data Values

```javascript
onClick: (e) => {
  const position = Chart.helpers.getRelativePosition(e, chart);
  const dataX = chart.scales.x.getValueForPixel(position.x);
  const dataY = chart.scales.y.getValueForPixel(position.y);
}
```

## Layout Configuration

Namespace: `options.layout`

```javascript
layout: {
  padding: { top: 20, right: 20, bottom: 20, left: 20 },
  autoPadding: true  // Auto-adjust for labels
}
```

## Font Configuration

Global defaults:

```javascript
Chart.defaults.font.family = "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.font.weight = 'normal';
Chart.defaults.font.lineHeight = 1.2;
Chart.defaults.color = '#666';
```

Per-element font:

```javascript
font: { family: 'Arial', size: 18, weight: 'bold', style: 'italic', lineHeight: 1.2 }
```

## Color Configuration

Supported formats: named (`'red'`), hex (`'#ff0000'`), RGB (`'rgb(255,0,0)'`), RGBA (`'rgba(255,0,0,0.5)'`), HSL (`'hsl(0,100%,50%)'`), HSLA.

Global color defaults:

```javascript
Chart.defaults.backgroundColor = 'rgba(0, 0, 0, 0.1)';
Chart.defaults.borderColor = 'rgba(0, 0, 0, 0.1)';
Chart.defaults.color = '#666';
```

## Element Configuration

Default styles for chart elements:

```javascript
// Points (line, radar, scatter)
Chart.defaults.elements.point.radius = 3;
Chart.defaults.elements.point.hoverRadius = 4;

// Lines
Chart.defaults.elements.line.tension = 0;
Chart.defaults.elements.line.borderWidth = 3;

// Bars
Chart.defaults.elements.bar.borderWidth = 0;
Chart.defaults.elements.bar.borderRadius = 0;

// Arcs (pie, doughnut, polar)
Chart.defaults.elements.arc.borderWidth = 2;
```

## Global Defaults

```javascript
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = true;
Chart.defaults.interaction.mode = 'nearest';
Chart.defaults.plugins.legend.position = 'bottom';
Chart.defaults.datasets.line.tension = 0.4;
```

## Additional Configuration

Other configuration topics not covered in detail here:

- **Decimation**: Reduce data points for large datasets (`options.plugins.decimation`)
- **Locale**: Number/date formatting (`options.locale`)
- **Device Pixel Ratio**: Canvas resolution (`options.devicePixelRatio`)
- **Canvas Background**: Background color plugin for exports

## References

- `references/advanced-animations.md` - Transitions, callbacks, animation object
- `references/tooltip-customization.md` - External tooltips, Tooltip Model, custom positioners
- `references/legend-customization.md` - Legend Item Interface, custom handlers

## Examples

- `examples/responsive-chart.html` - Proper container setup, flexbox, print handling
- `examples/custom-tooltip.html` - External HTML tooltip implementation
- `examples/interactive-legend.html` - Custom legend click behavior
