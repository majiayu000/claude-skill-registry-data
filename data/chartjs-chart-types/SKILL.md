---
name: chartjs-chart-types
description: This skill should be used when the user asks "how to create a line chart", "Chart.js bar chart", "pie chart Chart.js", "doughnut chart", "radar chart", "polar area chart", "bubble chart", "scatter chart", "mixed chart", "combo chart", "area chart", "stacked chart", "horizontal bar chart", "Chart.js chart types", "dataset properties", "chart data structure", or needs help implementing specific Chart.js v4.5.1 chart types.
---

# Chart.js Chart Types (v4.5.1)

Complete guide to all Chart.js chart types, their configuration, and dataset properties.

## Available Chart Types

| Type | Description | Use Case |
|------|-------------|----------|
| `line` | Line chart | Trends over time |
| `bar` | Bar chart | Comparing categories |
| `pie` | Pie chart | Parts of a whole |
| `doughnut` | Doughnut chart | Parts of a whole with center |
| `radar` | Radar/spider chart | Multivariate data comparison |
| `polarArea` | Polar area chart | Cyclical data |
| `bubble` | Bubble chart | Three dimensions |
| `scatter` | Scatter plot | Correlation analysis |

## Line Chart

Show trends and changes over time:

```javascript
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Sales',
      data: [65, 59, 80, 81, 56],
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1  // 0 = straight lines, 0.4 = curved
    }]
  }
});
```

### Key Line Properties

| Property | Type | Description |
|----------|------|-------------|
| `tension` | number | Bezier curve tension (0-1) |
| `fill` | boolean/string | Fill area under line |
| `stepped` | boolean/string | Stepped line interpolation |
| `borderDash` | number[] | Dashed line pattern |
| `pointRadius` | number | Data point size |
| `pointStyle` | string | Point shape (circle, rect, triangle, etc.) |
| `spanGaps` | boolean | Connect over null values |

### Vertical Line Chart

Flip axes with `indexAxis`:

```javascript
options: {
  indexAxis: 'y'  // Vertical line chart
}
```

## Bar Chart

Compare discrete categories:

```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green'],
    datasets: [{
      label: 'Votes',
      data: [12, 19, 3, 5],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)'
      ],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: { beginAtZero: true }
    }
  }
});
```

### Key Bar Properties

| Property | Type | Description |
|----------|------|-------------|
| `barThickness` | number/'flex' | Bar width in pixels |
| `barPercentage` | number | Bar width relative to category (0-1) |
| `categoryPercentage` | number | Category width (0-1) |
| `borderRadius` | number/object | Rounded corners |
| `borderSkipped` | string | Which border to skip |

### Horizontal Bar Chart

```javascript
options: {
  indexAxis: 'y'  // Makes bars horizontal
}
```

### Stacked Bar Chart

```javascript
options: {
  scales: {
    x: { stacked: true },
    y: { stacked: true }
  }
}
```

## Pie & Doughnut Charts

Show proportional data:

```javascript
// Pie chart
new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['Red', 'Blue', 'Yellow'],
    datasets: [{
      data: [300, 50, 100],
      backgroundColor: ['#ff6384', '#36a2eb', '#ffce56']
    }]
  }
});

// Doughnut chart
new Chart(ctx, {
  type: 'doughnut',
  data: { /* same as pie */ },
  options: {
    cutout: '50%'  // Size of center hole
  }
});
```

### Key Pie/Doughnut Properties

| Property | Type | Description |
|----------|------|-------------|
| `cutout` | number/string | Center hole size (doughnut) |
| `rotation` | number | Starting angle (degrees) |
| `circumference` | number | Arc sweep (degrees) |
| `offset` | number | Arc offset on hover |
| `hoverOffset` | number | Offset when hovering |

### Semi-Circle Chart

```javascript
options: {
  rotation: -90,
  circumference: 180
}
```

## Radar Chart

Compare multiple variables across categories:

```javascript
new Chart(ctx, {
  type: 'radar',
  data: {
    labels: ['Speed', 'Power', 'Defense', 'Stamina', 'Agility'],
    datasets: [{
      label: 'Player A',
      data: [65, 59, 90, 81, 56],
      fill: true,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)'
    }, {
      label: 'Player B',
      data: [28, 48, 40, 19, 96],
      fill: true,
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgb(54, 162, 235)'
    }]
  },
  options: {
    scales: {
      r: {
        angleLines: { display: true },
        suggestedMin: 0,
        suggestedMax: 100
      }
    }
  }
});
```

## Polar Area Chart

Like pie but with equal angles, varying radius:

```javascript
new Chart(ctx, {
  type: 'polarArea',
  data: {
    labels: ['Red', 'Green', 'Yellow', 'Grey', 'Blue'],
    datasets: [{
      data: [11, 16, 7, 3, 14],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(255, 205, 86, 0.5)',
        'rgba(201, 203, 207, 0.5)',
        'rgba(54, 162, 235, 0.5)'
      ]
    }]
  }
});
```

## Scatter Chart

Show correlation between two variables:

```javascript
new Chart(ctx, {
  type: 'scatter',
  data: {
    datasets: [{
      label: 'Data Points',
      data: [
        { x: 10, y: 20 },
        { x: 15, y: 10 },
        { x: 20, y: 30 },
        { x: 25, y: 25 }
      ],
      backgroundColor: 'rgb(255, 99, 132)'
    }]
  },
  options: {
    scales: {
      x: { type: 'linear', position: 'bottom' },
      y: { type: 'linear' }
    }
  }
});
```

## Bubble Chart

Three-dimensional data visualization:

```javascript
new Chart(ctx, {
  type: 'bubble',
  data: {
    datasets: [{
      label: 'Dataset',
      data: [
        { x: 20, y: 30, r: 15 },  // r = bubble radius
        { x: 40, y: 10, r: 10 },
        { x: 30, y: 22, r: 25 }
      ],
      backgroundColor: 'rgba(255, 99, 132, 0.5)'
    }]
  },
  options: {
    aspectRatio: 1  // Square chart for bubbles
  }
});
```

## Area Chart

Line chart with filled area:

```javascript
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Revenue',
      data: [65, 59, 80, 81, 56],
      fill: true,  // Enable fill
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgb(75, 192, 192)'
    }]
  }
});
```

### Fill Options

| Value | Description |
|-------|-------------|
| `false` | No fill (default) |
| `true` | Fill to origin |
| `'origin'` | Fill to origin |
| `'start'` | Fill to bottom |
| `'end'` | Fill to top |
| `'-1'` | Fill to previous dataset |
| `'+1'` | Fill to next dataset |

## Mixed Charts

Combine multiple chart types:

```javascript
new Chart(ctx, {
  type: 'bar',  // Base type
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    datasets: [
      {
        type: 'line',  // Override type for this dataset
        label: 'Trend',
        data: [50, 60, 70, 80],
        borderColor: 'rgb(255, 99, 132)',
        fill: false
      },
      {
        type: 'bar',  // Explicit bar type
        label: 'Sales',
        data: [40, 55, 65, 75],
        backgroundColor: 'rgba(54, 162, 235, 0.5)'
      }
    ]
  }
});
```

### Drawing Order

Control which dataset renders on top:

```javascript
datasets: [
  { label: 'Bars', order: 2 },  // Drawn first (behind)
  { label: 'Line', order: 1 }   // Drawn last (on top)
]
```

## Data Structures

### Standard Format

```javascript
data: {
  labels: ['A', 'B', 'C'],
  datasets: [{
    data: [10, 20, 30]
  }]
}
```

### Object Format

```javascript
datasets: [{
  data: [
    { x: 'A', y: 10 },
    { x: 'B', y: 20 },
    { x: 'C', y: 30 }
  ]
}]
```

### Parsed Data Format

```javascript
datasets: [{
  data: [
    { id: 'Sales', value: 100 },
    { id: 'Revenue', value: 200 }
  ],
  parsing: {
    xAxisKey: 'id',
    yAxisKey: 'value'
  }
}]
```

## Additional Resources

- See `references/dataset-properties.md` for complete property reference
- See `examples/` for working HTML examples:
  - `line-area-charts.html` - Line charts with tension, area fills, stepped lines
  - `bar-charts.html` - Vertical, horizontal, stacked bars, and mixed bar+line
  - `circular-charts.html` - Pie, doughnut, semi-circle gauge, polar area, radar
