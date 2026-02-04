---
name: chartjs-animations
description: This skill should be used when the user asks "Chart.js animations", "Chart.js easing", "Chart.js animation duration", "Chart.js animation callbacks", "Chart.js transitions", "Chart.js animation loop", "progressive line animation", "Chart.js animation delay", "disable Chart.js animation", "Chart.js onComplete", "Chart.js onProgress", or needs help configuring animations in Chart.js v4.5.1.
---

# Chart.js Animations (v4.5.1)

Complete guide to configuring and customizing animations in Chart.js.

## Animation Basics

Chart.js animates charts automatically. Animations provide visual feedback during chart initialization, data updates, and user interactions.

### Animation Configuration Structure

Three main configuration keys:

| Key | Purpose | Example Use Case |
|-----|---------|------------------|
| `animation` | Global animation settings | Duration, easing, delay |
| `animations` | Property-specific animations | Animate only x-axis values |
| `transitions` | Mode-specific animations | Custom hover behavior |

### Configuration Locations

```javascript
// Global configuration (all charts)
Chart.defaults.animation.duration = 2000;

// Chart instance configuration
const chart = new Chart(ctx, {
  options: {
    animation: {
      duration: 1500,
      easing: 'easeInOutQuart'
    }
  }
});

// Dataset-specific configuration
datasets: [{
  label: 'Sales',
  data: [10, 20, 30],
  animation: {
    duration: 3000  // This dataset animates slower
  }
}]
```

## Main Animation Options

Namespace: `options.animation`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `duration` | number | 1000 | Animation length in milliseconds |
| `easing` | string | `'easeOutQuart'` | Easing function name |
| `delay` | number | undefined | Delay before animation starts (ms) |
| `loop` | boolean | undefined | Loop animation endlessly |

### Basic Example

```javascript
const chart = new Chart(ctx, {
  type: 'bar',
  data: data,
  options: {
    animation: {
      duration: 2000,           // 2 seconds
      easing: 'easeInOutCubic', // Smooth start and end
      delay: 500                 // Wait 0.5s before starting
    }
  }
});
```

### Looping Animation

```javascript
options: {
  animation: {
    duration: 2000,
    loop: true,  // Repeat forever
    easing: 'linear'
  }
}
```

## Property-Specific Animations

Configure animations for individual properties.

Namespace: `options.animations[animationName]`

| Option | Type | Description |
|--------|------|-------------|
| `properties` | string[] | Properties to animate (defaults to key name) |
| `type` | string | `'number'`, `'color'`, or `'boolean'` |
| `from` | number\|Color\|boolean | Start value |
| `to` | number\|Color\|boolean | End value |
| `fn` | function | Custom interpolator |

### Default Property Animations

```javascript
// Chart.js default animations
animations: {
  numbers: {
    type: 'number',
    properties: ['x', 'y', 'borderWidth', 'radius', 'tension']
  },
  colors: {
    type: 'color',
    properties: ['color', 'borderColor', 'backgroundColor']
  }
}
```

### Custom Property Animation

```javascript
options: {
  animations: {
    // Animate only Y values
    y: {
      duration: 2000,
      from: 0,  // Start from bottom
      easing: 'easeOutBounce'
    },
    // Animate only colors
    colors: {
      duration: 1000,
      from: 'transparent'
    },
    // Disable X animation
    x: false
  }
}
```

### Tension Animation (Line Charts)

```javascript
options: {
  animations: {
    tension: {
      duration: 1000,
      easing: 'linear',
      from: 1,    // Very curvy
      to: 0,      // Straight lines
      loop: true  // Continuously animate
    }
  }
}
```

## Transitions

Transitions define animations for specific interaction modes.

### Built-in Transition Modes

| Mode | When Triggered | Default Duration |
|------|----------------|------------------|
| `active` | Hover/focus | 400ms |
| `resize` | Chart resize | 0ms (instant) |
| `show` | Dataset shown via legend | 1000ms |
| `hide` | Dataset hidden via legend | 1000ms |
| `reset` | Chart reset | 1000ms |

### Customizing Hover Animation

```javascript
options: {
  transitions: {
    active: {
      animation: {
        duration: 600,  // Slower hover animation
        easing: 'easeOutElastic'
      }
    }
  }
}
```

### Show/Hide Animations

```javascript
options: {
  transitions: {
    show: {
      animations: {
        x: { from: 0 },
        y: { from: 0 }
      }
    },
    hide: {
      animations: {
        x: { to: 0 },
        y: { to: 0 }
      }
    }
  }
}
```

### Custom Transition Mode

```javascript
// Trigger custom transition
chart.update('myCustomMode');

// Define custom transition
options: {
  transitions: {
    myCustomMode: {
      animation: {
        duration: 500,
        easing: 'linear'
      }
    }
  }
}
```

## Easing Functions

Chart.js provides 36 easing functions.

### Easing Categories

| Category | Functions | Visual Effect |
|----------|-----------|---------------|
| Linear | `linear` | Constant speed |
| Quad | `easeInQuad`, `easeOutQuad`, `easeInOutQuad` | Gradual acceleration/deceleration |
| Cubic | `easeInCubic`, `easeOutCubic`, `easeInOutCubic` | More pronounced curves |
| Quart | `easeInQuart`, `easeOutQuart`, `easeInOutQuart` | Strong acceleration |
| Quint | `easeInQuint`, `easeOutQuint`, `easeInOutQuint` | Very strong acceleration |
| Sine | `easeInSine`, `easeOutSine`, `easeInOutSine` | Smooth, gentle curves |
| Expo | `easeInExpo`, `easeOutExpo`, `easeInOutExpo` | Exponential growth |
| Circ | `easeInCirc`, `easeOutCirc`, `easeInOutCirc` | Circular motion |
| Elastic | `easeInElastic`, `easeOutElastic`, `easeInOutElastic` | Spring/bounce back |
| Back | `easeInBack`, `easeOutBack`, `easeInOutBack` | Overshoot then settle |
| Bounce | `easeInBounce`, `easeOutBounce`, `easeInOutBounce` | Bouncing ball effect |

### Easing Pattern Meanings

- **easeIn**: Slow start, fast end
- **easeOut**: Fast start, slow end (most natural)
- **easeInOut**: Slow start, fast middle, slow end

### Common Easing Choices

```javascript
// Default (smooth and natural)
easing: 'easeOutQuart'

// Bouncy entrance
easing: 'easeOutBounce'

// Elastic snap
easing: 'easeOutElastic'

// Smooth both ends
easing: 'easeInOutCubic'

// Constant speed
easing: 'linear'
```

## Animation Callbacks

Execute custom code during animations.

Namespace: `options.animation`

| Callback | When Called | Parameters |
|----------|-------------|------------|
| `onProgress` | Each animation frame | Animation state object |
| `onComplete` | Animation finishes | Animation state object |

### Callback Parameters

```javascript
{
  chart: Chart,           // Chart instance
  currentStep: number,    // Current animation step
  initial: boolean,       // True for initial chart animation
  numSteps: number        // Total animation steps
}
```

### Progress Bar Example

```javascript
const progressBar = document.getElementById('progress');

const chart = new Chart(ctx, {
  type: 'line',
  data: data,
  options: {
    animation: {
      duration: 2000,
      onProgress: (animation) => {
        const progress = (animation.currentStep / animation.numSteps) * 100;
        progressBar.style.width = progress + '%';
      },
      onComplete: (animation) => {
        console.log('Animation finished!');
        progressBar.style.width = '100%';
      }
    }
  }
});
```

### Trigger Action After Animation

```javascript
options: {
  animation: {
    onComplete: (animation) => {
      if (animation.initial) {
        // Only run after initial chart render
        showDataTable();
      }
    }
  }
}
```

## Disabling Animations

### Disable All Animations

```javascript
// Instance-level
options: {
  animation: false
}

// Global default
Chart.defaults.animation = false;
```

### Disable Specific Animations

```javascript
options: {
  animations: {
    colors: false,  // Disable color animations
    x: false        // Disable x-axis animations
  }
}
```

### Disable Transition Modes

```javascript
options: {
  transitions: {
    active: {
      animation: {
        duration: 0  // No hover animation
      }
    }
  }
}
```

## Advanced Patterns

### Progressive Line Reveal

```javascript
options: {
  animation: {
    duration: 2000,
    onProgress: function(animation) {
      const chartInstance = animation.chart;
      const ctx = chartInstance.ctx;
      const meta = chartInstance.getDatasetMeta(0);

      // Draw line progressively
      const progress = animation.currentStep / animation.numSteps;
      // Custom rendering logic here
    }
  }
}
```

### Staggered Animation

```javascript
options: {
  animation: {
    delay: (context) => {
      let delay = 0;
      if (context.type === 'data' && context.mode === 'default') {
        delay = context.dataIndex * 50;  // 50ms delay per data point
      }
      return delay;
    }
  }
}
```

### Drop Animation

```javascript
options: {
  animations: {
    y: {
      duration: 2000,
      from: (ctx) => {
        // Drop from top of chart
        return ctx.chart.scales.y.getPixelForValue(
          ctx.chart.scales.y.max
        );
      },
      easing: 'easeOutBounce'
    }
  }
}
```

### Color Fade Transition

```javascript
options: {
  animations: {
    backgroundColor: {
      type: 'color',
      duration: 1000,
      from: 'transparent',
      to: 'rgba(255, 99, 132, 0.5)',
      easing: 'easeInOutQuad'
    }
  }
}
```

## Performance Considerations

### Reduce Animation Duration for Large Datasets

```javascript
const dataPoints = data.datasets[0].data.length;

options: {
  animation: {
    duration: dataPoints > 100 ? 500 : 1000  // Faster for large datasets
  }
}
```

### Skip Animations on Updates

```javascript
// No animation for this update
chart.update('none');

// Or specific mode
chart.update('active');  // Use 'active' transition
```

### Responsive Animation Handling

```javascript
options: {
  transitions: {
    resize: {
      animation: {
        duration: 0  // Instant resize (default)
      }
    }
  }
}
```

## Framework Integration

### React (react-chartjs-2)

```jsx
import { Line } from 'react-chartjs-2';

function AnimatedChart() {
  const options = {
    animation: {
      duration: 2000,
      easing: 'easeOutQuart',
      onComplete: () => {
        console.log('Animation done!');
      }
    }
  };

  return <Line data={data} options={options} />;
}
```

### Vue (vue-chartjs)

```vue
<script setup>
import { Line } from 'vue-chartjs';

const chartOptions = {
  animation: {
    duration: 1500,
    easing: 'easeInOutCubic'
  }
};
</script>

<template>
  <Line :data="chartData" :options="chartOptions" />
</template>
```

## Additional Resources

- See `references/easing-functions.md` for visual easing function guide
- See `references/animation-patterns.md` for advanced animation patterns
- See `examples/progressive-animation.html` for progressive line reveal example
- See `examples/staggered-bars.html` for staggered bar animation example
