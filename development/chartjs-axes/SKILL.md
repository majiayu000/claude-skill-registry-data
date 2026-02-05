---
name: chartjs-axes
description: This skill should be used when the user asks "Chart.js axes", "Chart.js scales", "Chart.js x-axis", "Chart.js y-axis", "Chart.js time axis", "Chart.js logarithmic scale", "Chart.js axis labels", "Chart.js ticks", "Chart.js grid lines", "Chart.js multiple axes", "Chart.js dual axis", "Chart.js axis title", "Chart.js axis range", "Chart.js min max", "stacked axes", "Chart.js radial axis", or needs help configuring Chart.js v4.5.1 axes and scales.
---

# Chart.js Axes Configuration (v4.5.1)

Comprehensive guide to configuring axes, scales, ticks, and grid lines in Chart.js.

## Axis Types

### Cartesian Axes (x/y)

| Type | Use Case | Import |
|------|----------|--------|
| `category` | String labels | `CategoryScale` |
| `linear` | Numeric data | `LinearScale` |
| `logarithmic` | Exponential data | `LogarithmicScale` |
| `time` | Date/time data | `TimeScale` |
| `timeseries` | Time series data | `TimeSeriesScale` |

### Radial Axes (r)

| Type | Use Case | Import |
|------|----------|--------|
| `radialLinear` | Radar/polar charts | `RadialLinearScale` |

## Basic Axis Configuration

Namespace: `options.scales`

```javascript
options: {
  scales: {
    x: {
      type: 'category',          // Scale type
      position: 'bottom',        // bottom, top, left, right
      display: true,             // Show axis
      title: {
        display: true,
        text: 'X Axis Label'
      }
    },
    y: {
      type: 'linear',
      position: 'left',
      beginAtZero: true,
      title: {
        display: true,
        text: 'Y Axis Label'
      }
    }
  }
}
```

## Linear Scale

For numeric data:

```javascript
scales: {
  y: {
    type: 'linear',
    min: 0,                      // Minimum value
    max: 100,                    // Maximum value
    suggestedMin: 0,             // Suggested min (can be exceeded by data)
    suggestedMax: 100,           // Suggested max
    beginAtZero: true,           // Force zero origin
    grace: '5%',                 // Extra space beyond min/max
    ticks: {
      stepSize: 10,              // Fixed step size
      count: 11,                 // Approximate number of ticks
      precision: 0               // Decimal places
    }
  }
}
```

## Category Scale

For string labels:

```javascript
scales: {
  x: {
    type: 'category',
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    offset: true,                // Add padding to edges
    ticks: {
      autoSkip: true,            // Skip labels if crowded
      maxRotation: 45,           // Max label rotation
      minRotation: 0             // Min label rotation
    }
  }
}
```

## Time Scale

Requires a date adapter. Install one:

```bash
npm install chartjs-adapter-date-fns date-fns
# or
npm install chartjs-adapter-moment moment
# or
npm install chartjs-adapter-luxon luxon
```

```javascript
import 'chartjs-adapter-date-fns';

scales: {
  x: {
    type: 'time',
    time: {
      unit: 'day',               // millisecond, second, minute, hour, day, week, month, quarter, year
      displayFormats: {
        day: 'MMM d'             // Format string
      },
      tooltipFormat: 'PP',       // Tooltip format
      parser: 'yyyy-MM-dd'       // Parse format
    },
    min: '2024-01-01',
    max: '2024-12-31',
    ticks: {
      source: 'auto'             // auto, data, labels
    }
  }
}
```

### Time Data Formats

```javascript
// ISO 8601 strings
data: ['2024-01-15', '2024-02-15', '2024-03-15']

// Date objects
data: [new Date(2024, 0, 15), new Date(2024, 1, 15)]

// Timestamps
data: [1705276800000, 1707955200000, 1710460800000]

// Object format
data: [
  { x: '2024-01-15', y: 10 },
  { x: '2024-02-15', y: 20 }
]
```

## Logarithmic Scale

For exponential data:

```javascript
scales: {
  y: {
    type: 'logarithmic',
    min: 1,                      // Must be > 0
    max: 1000000,
    ticks: {
      callback: (value) => {
        if (value === 10 || value === 100 || value === 1000) {
          return value.toLocaleString();
        }
        return '';
      }
    }
  }
}
```

## Multiple Axes

### Dual Y-Axis

```javascript
data: {
  datasets: [
    {
      label: 'Revenue',
      data: [1000, 2000, 3000],
      yAxisID: 'y'               // Left axis
    },
    {
      label: 'Units',
      data: [10, 20, 30],
      yAxisID: 'y1'              // Right axis
    }
  ]
},
options: {
  scales: {
    y: {
      type: 'linear',
      position: 'left',
      title: { display: true, text: 'Revenue ($)' }
    },
    y1: {
      type: 'linear',
      position: 'right',
      title: { display: true, text: 'Units' },
      grid: {
        drawOnChartArea: false   // Hide grid for this axis
      }
    }
  }
}
```

### Multiple X-Axes

```javascript
scales: {
  x: {
    position: 'bottom',
    title: { display: true, text: 'Months' }
  },
  x2: {
    position: 'top',
    title: { display: true, text: 'Quarters' },
    grid: { drawOnChartArea: false }
  }
}
```

## Axis Title

```javascript
scales: {
  y: {
    title: {
      display: true,
      text: 'Value',
      color: '#666',
      font: {
        size: 14,
        weight: 'bold'
      },
      padding: { top: 10, bottom: 10 }
    }
  }
}
```

## Tick Configuration

```javascript
scales: {
  y: {
    ticks: {
      display: true,
      color: '#666',
      font: { size: 11 },
      padding: 5,
      align: 'center',           // start, center, end
      crossAlign: 'near',        // near, center, far
      autoSkip: true,
      autoSkipPadding: 3,
      maxTicksLimit: 11,
      includeBounds: true,

      // Custom formatting
      callback: function(value, index, ticks) {
        return '$' + value.toLocaleString();
      }
    }
  }
}
```

### Common Tick Formats

```javascript
// Currency
callback: (value) => '$' + value.toLocaleString()

// Percentage
callback: (value) => value + '%'

// Abbreviated numbers
callback: (value) => {
  if (value >= 1000000) return (value / 1000000) + 'M';
  if (value >= 1000) return (value / 1000) + 'K';
  return value;
}

// Date formatting
callback: (value) => new Date(value).toLocaleDateString()
```

## Grid Lines

```javascript
scales: {
  x: {
    grid: {
      display: true,
      color: 'rgba(0, 0, 0, 0.1)',
      lineWidth: 1,
      drawOnChartArea: true,     // Draw grid in chart area
      drawTicks: true,           // Draw tick marks
      tickLength: 8,
      tickColor: '#666',         // Tick mark color
      offset: false,
      z: -1                      // Z-index (<= 0 under datasets)
    }
  },
  y: {
    grid: {
      // Scriptable: different color for zero line
      color: (context) => {
        if (context.tick.value === 0) {
          return 'rgba(0, 0, 0, 0.5)';  // Bold zero line
        }
        return 'rgba(0, 0, 0, 0.1)';
      }
    }
  }
}
```

### Hide Grid Lines

```javascript
grid: { display: false }
```

## Axis Border

Namespace: `options.scales[scaleId].border` - configures the axis border line (separate from grid lines).

```javascript
scales: {
  x: {
    border: {
      display: true,             // Show axis border
      color: '#666',             // Border color
      width: 2,                  // Border width in pixels
      dash: [],                  // Solid line
      dashOffset: 0,
      z: 0                       // Z-index (> 0 on top of datasets)
    }
  },
  y: {
    border: {
      display: true,
      color: 'rgba(0, 0, 0, 0.5)',
      width: 1,
      dash: [5, 5],              // Dashed border
      dashOffset: 0
    }
  }
}
```

## Stacked Axes

```javascript
scales: {
  x: {
    stacked: true
  },
  y: {
    stacked: true
  }
}
```

### Grouped Stacks

```javascript
datasets: [
  { label: 'A1', stack: 'Stack 0', data: [1, 2, 3] },
  { label: 'A2', stack: 'Stack 0', data: [2, 3, 4] },
  { label: 'B1', stack: 'Stack 1', data: [3, 4, 5] },
  { label: 'B2', stack: 'Stack 1', data: [4, 5, 6] }
]
```

## Radial Linear Scale

For radar and polar area charts:

```javascript
scales: {
  r: {
    angleLines: {
      display: true,
      color: 'rgba(0, 0, 0, 0.1)'
    },
    grid: {
      circular: true             // Circular or straight grid
    },
    pointLabels: {
      display: true,
      font: { size: 12 }
    },
    suggestedMin: 0,
    suggestedMax: 100,
    ticks: {
      stepSize: 20,
      backdropColor: 'transparent'
    }
  }
}
```

## Axis Range Settings

### Fixed Range

```javascript
scales: {
  y: {
    min: 0,
    max: 100
  }
}
```

### Suggested Range

Data can exceed these bounds:

```javascript
scales: {
  y: {
    suggestedMin: 0,
    suggestedMax: 100
  }
}
```

### Dynamic Range with Grace

```javascript
scales: {
  y: {
    grace: '5%',                 // Add 5% padding
    // or
    grace: 5                     // Add 5 units
  }
}
```

## Axis Callbacks

```javascript
scales: {
  y: {
    beforeUpdate: (axis) => { /* ... */ },
    afterUpdate: (axis) => { /* ... */ },
    beforeBuildTicks: (axis) => { /* ... */ },
    afterBuildTicks: (axis) => { /* ... */ },
    beforeDataLimits: (axis) => { /* ... */ },
    afterDataLimits: (axis) => { /* ... */ },
    beforeTickToLabelConversion: (axis) => { /* ... */ },
    afterTickToLabelConversion: (axis) => { /* ... */ },
    beforeFit: (axis) => { /* ... */ },
    afterFit: (axis) => { /* ... */ }
  }
}
```

## Axis Defaults

Set defaults for all scales:

```javascript
// Linear scale defaults
Chart.defaults.scales.linear.min = 0;

// Category scale defaults
Chart.defaults.scales.category.ticks.autoSkip = true;

// All scales
Chart.defaults.scale.grid.color = 'rgba(0, 0, 0, 0.1)';
```

## Additional Resources

- See `references/date-adapters.md` for time scale adapter setup
- See `references/advanced-axis-customization.md` for scriptable options, tick alignment, and dynamic positioning
- See `examples/dual-y-axis.html` for dual axis with mixed chart types
- See `examples/time-scale.html` for time-based charts with date-fns adapter
- See `examples/styled-axes.html` for custom axis styling (borders, grids, ticks)
