---
name: "control panel"
description: "Creates a control panel that allows runtime modification of values. When Claude needs to expose controls for the user to adjust variables and values."
license: Proprietary
---

# Leva Control Panel Skill

You are a specialized expert in creating interactive control panels using **Leva** - a React GUI library for building powerful, real-time controls for prototyping and debugging.

## Available Tools in This Repo

### Leva
Already installed via `leva@^0.10.1`. Import as:
```tsx
import { useControls, button, folder, buttonGroup, LevaPanel } from 'leva'
```

## Core Concepts

1. **useControls Hook** - Primary hook for creating controls
2. **Automatic Type Detection** - Leva infers control types from initial values
3. **Folders & Organization** - Group related controls for better UX
4. **Real-time Updates** - Controls update React state automatically
5. **Transient Mode** - Performance optimization for smooth interactions

## Control Types Reference

### 1. Number Controls

**Basic number:**
```tsx
const { count } = useControls({
  count: 42
})
```

**Number with constraints:**
```tsx
const { value } = useControls({
  value: { value: 50, min: 0, max: 100, step: 5 }
})
```

**With suffix/prefix:**
```tsx
const { temperature } = useControls({
  temperature: { value: 72, min: 32, max: 100, suffix: '°F' }
})
```

### 2. String/Text Controls

**Basic text:**
```tsx
const { name } = useControls({
  name: 'Default Name'
})
```

**Multiline text:**
```tsx
const { description } = useControls({
  description: { value: 'Long text...', rows: 3 }
})
```

### 3. Boolean Controls

**Simple checkbox:**
```tsx
const { enabled } = useControls({
  enabled: true
})
```

### 4. Color Controls

**Supports hex, rgb, hsl:**
```tsx
const { color } = useControls({
  background: '#4c9aff',
  textColor: { value: '#ffffff', label: 'Text' },
  accent: 'rgb(255, 100, 150)'
})
```

### 5. Select/Dropdown Controls

**Array options:**
```tsx
const { size } = useControls({
  size: { value: 'medium', options: ['small', 'medium', 'large'] }
})
```

**Object options (custom labels):**
```tsx
const { theme } = useControls({
  theme: {
    value: 'dark',
    options: {
      'Light Mode': 'light',
      'Dark Mode': 'dark',
      'Auto': 'auto'
    }
  }
})
```

### 6. Vector Controls

**2D vectors:**
```tsx
const { position } = useControls({
  position: { value: { x: 0, y: 0 }, step: 1 }
})
```

**3D vectors:**
```tsx
const { position3D } = useControls({
  position3D: { value: { x: 0, y: 0, z: 0 }, step: 1 }
})
```

**With constraints:**
```tsx
const { scale } = useControls({
  scale: { value: { x: 1, y: 1 }, min: 0.1, max: 3, step: 0.1 }
})
```

### 7. Interval/Range Controls

**Range slider:**
```tsx
const { range } = useControls({
  range: { value: [20, 80], min: 0, max: 100 }
})
```

### 8. Button Controls

**Single button:**
```tsx
const controls = useControls({
  'Click Me': button(() => {
    console.log('Clicked!')
  })
})
```

**Button group:**
```tsx
import { buttonGroup } from 'leva'

const controls = useControls({
  'Actions': buttonGroup({
    Save: () => handleSave(),
    Load: () => handleLoad(),
    Delete: () => handleDelete()
  })
})
```

### 9. Image/File Controls

```tsx
const { image } = useControls({
  image: { image: undefined }
})
```

### 10. Monitor (Read-only Display)

```tsx
const { fps } = useControls({
  'Current FPS': { value: currentFps, disabled: true }
})
```

## Organization Patterns

### Grouped Controls
```tsx
const controls = useControls('Settings', {
  width: 400,
  height: 300,
  color: '#ff0000'
})
```

### Nested Folders
```tsx
import { folder } from 'leva'

const controls = useControls('Advanced', {
  'Animation': folder({
    duration: { value: 1000, min: 100, max: 5000, step: 100 },
    easing: { value: 'easeOut', options: ['linear', 'easeIn', 'easeOut'] },
    loop: false
  }),
  'Performance': folder({
    fps: { value: 60, min: 24, max: 120 },
    quality: { value: 'high', options: ['low', 'medium', 'high'] }
  }, { collapsed: true }) // Start collapsed
})
```

## Advanced Features

### 1. Transient Mode (Performance)

Use for smooth real-time updates without re-renders:
```tsx
const { value } = useControls({
  value: {
    value: 50,
    min: 0,
    max: 100,
    transient: false // Set to true for onChange-only updates
  }
})
```

**Note:** In Leva 0.10.1, transient mode is handled automatically - just use regular controls for smooth interactions.

### 2. Multiple Panels

```tsx
import { LevaPanel, useControls } from 'leva'

function Component() {
  const panel1 = useControls('Panel 1', { value1: 0 })
  const panel2 = useControls('Panel 2', { value2: 100 })

  return (
    <>
      <LevaPanel store={panel1} />
      <LevaPanel store={panel2} />
    </>
  )
}
```

### 3. Conditional Controls

```tsx
const { mode, detail } = useControls({
  mode: { value: 'simple', options: ['simple', 'advanced'] },
  ...(mode === 'advanced' && {
    detail: { value: 5, min: 1, max: 10 }
  })
})
```

### 4. Custom Labels

```tsx
const controls = useControls({
  bgColor: { value: '#ffffff', label: 'Background Color' }
})
```

### 5. Control Order

```tsx
const controls = useControls({
  name: 'Title',
  size: { value: 100, order: 0 }, // Appears first
  color: { value: '#fff', order: 1 }, // Appears second
  enabled: { value: true, order: 2 } // Appears third
})
```

## Common Use Cases

### 1. Visual Prototype Controls

```tsx
function PrototypeComponent() {
  const { width, height, color, opacity, rounded } = useControls('Visual', {
    width: { value: 200, min: 100, max: 800, step: 10 },
    height: { value: 200, min: 100, max: 800, step: 10 },
    color: '#4c9aff',
    opacity: { value: 1, min: 0, max: 1, step: 0.01 },
    rounded: { value: 8, min: 0, max: 50, step: 1, suffix: 'px' }
  })

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: color,
        opacity,
        borderRadius: rounded
      }}
    />
  )
}
```

### 2. Animation Controls

```tsx
import { motion } from 'framer-motion'

function AnimatedComponent() {
  const { duration, delay, x, y, scale, rotate } = useControls('Animation', {
    duration: { value: 1, min: 0.1, max: 5, step: 0.1, suffix: 's' },
    delay: { value: 0, min: 0, max: 2, step: 0.1, suffix: 's' },
    x: { value: 0, min: -200, max: 200 },
    y: { value: 0, min: -200, max: 200 },
    scale: { value: 1, min: 0.1, max: 3, step: 0.1 },
    rotate: { value: 0, min: 0, max: 360, suffix: '°' }
  })

  return (
    <motion.div
      animate={{ x, y, scale, rotate }}
      transition={{ duration, delay }}
    >
      Animated Element
    </motion.div>
  )
}
```

### 3. Theme/Style Controls

```tsx
function ThemedComponent() {
  const { theme, spacing, fontSize, fontWeight } = useControls('Theme', {
    theme: {
      value: 'light',
      options: { Light: 'light', Dark: 'dark', Auto: 'auto' }
    },
    spacing: { value: 'comfortable', options: ['compact', 'comfortable', 'spacious'] },
    fontSize: { value: 16, min: 12, max: 24, step: 1, suffix: 'px' },
    fontWeight: {
      value: 400,
      options: { Light: 300, Regular: 400, Medium: 500, Bold: 700 }
    }
  })

  return <div style={{ fontSize, fontWeight }}>Styled Content</div>
}
```

### 4. Data Visualization Controls

```tsx
function ChartComponent() {
  const { dataPoints, chartType, showGrid, showLegend, colorScheme } = useControls('Chart', {
    dataPoints: { value: 50, min: 10, max: 200, step: 10 },
    chartType: { value: 'bar', options: ['line', 'bar', 'area', 'scatter'] },
    showGrid: true,
    showLegend: true,
    colorScheme: {
      value: 'default',
      options: ['default', 'vibrant', 'pastel', 'monochrome']
    }
  })

  // Render chart with these controls
}
```

### 5. Interactive Actions

```tsx
import { button, buttonGroup } from 'leva'

function InteractiveComponent() {
  const [state, setState] = useState('idle')

  const controls = useControls('Actions', {
    'Quick Actions': buttonGroup({
      Reset: () => setState('idle'),
      Start: () => setState('running'),
      Pause: () => setState('paused'),
      Stop: () => setState('stopped')
    }),
    'Export': button(() => {
      // Export logic
      console.log('Exporting...')
    }),
    'Current State': { value: state, disabled: true }
  })

  return <div>State: {state}</div>
}
```

## Best Practices

1. **Group Related Controls** - Use folders to organize complex UIs
2. **Provide Constraints** - Always set min/max for numeric values when appropriate
3. **Use Descriptive Labels** - Make control purposes clear
4. **Add Units** - Use suffix/prefix for clarity (px, %, °, ms, etc.)
5. **Start Collapsed** - Use `{ collapsed: true }` for secondary options
6. **Monitor Important Values** - Use disabled controls to display computed values
7. **Use Button Groups** - Group related actions together for better UX
8. **Keep It Organized** - Don't create too many controls at the root level
9. **Performance** - For real-time controls, Leva is already optimized
10. **Naming** - Use clear, consistent naming conventions

## Integration with Other Libraries

### With Framer Motion
```tsx
import { motion } from 'framer-motion'
import { useControls } from 'leva'

function AnimatedBox() {
  const { x, y, rotate, scale } = useControls({
    x: { value: 0, min: -200, max: 200 },
    y: { value: 0, min: -200, max: 200 },
    rotate: { value: 0, min: 0, max: 360 },
    scale: { value: 1, min: 0.5, max: 2, step: 0.1 }
  })

  return (
    <motion.div animate={{ x, y, rotate, scale }}>
      Content
    </motion.div>
  )
}
```

### With Three.js/React Three Fiber
```tsx
import { useControls } from 'leva'

function Scene() {
  const { intensity, position, color } = useControls('Light', {
    intensity: { value: 1, min: 0, max: 5, step: 0.1 },
    position: { value: { x: 0, y: 5, z: 0 } },
    color: '#ffffff'
  })

  return (
    <pointLight
      intensity={intensity}
      position={[position.x, position.y, position.z]}
      color={color}
    />
  )
}
```

## Styling & Customization

The Leva panel appears by default in the top-right corner. It supports dark/light themes automatically based on system preferences.

For custom positioning or styling, use CSS:
```css
/* Target the Leva root */
:root {
  --leva-colors-accent1: #4c9aff;
  --leva-colors-accent2: #5c6bc0;
}
```

## Quick Reference

| Control Type | Input | Output |
|-------------|-------|--------|
| Number | `count: 42` | `{ count: number }` |
| String | `name: 'text'` | `{ name: string }` |
| Boolean | `enabled: true` | `{ enabled: boolean }` |
| Color | `color: '#fff'` | `{ color: string }` |
| Select | `size: { options: [...] }` | `{ size: string }` |
| Vector2D | `pos: { x: 0, y: 0 }` | `{ pos: {x, y} }` |
| Vector3D | `pos: { x, y, z }` | `{ pos: {x, y, z} }` |
| Range | `range: [20, 80]` | `{ range: [number, number] }` |
| Button | `button(() => {})` | `void` |
| Image | `image: { image }` | `{ image: string \| undefined }` |

## Example: Complete Control Panel

```tsx
import { useControls, folder, button, buttonGroup } from 'leva'
import { motion } from 'framer-motion'

function CompleteDemo() {
  const {
    // Basic
    name,
    count,
    enabled,

    // Visual
    color,
    size,
    opacity,

    // Position
    position,

    // Advanced
    duration,
    easing,
    quality
  } = useControls({
    // Basic group
    name: 'Demo',
    count: { value: 42, min: 0, max: 100 },
    enabled: true,

    // Visual group
    Visual: folder({
      color: '#4c9aff',
      size: { value: 'medium', options: ['small', 'medium', 'large'] },
      opacity: { value: 1, min: 0, max: 1, step: 0.01 }
    }),

    // Position
    position: { value: { x: 0, y: 0 }, step: 5 },

    // Advanced
    Advanced: folder({
      duration: { value: 1000, min: 100, max: 3000, suffix: 'ms' },
      easing: { value: 'easeOut', options: ['linear', 'easeIn', 'easeOut'] },
      quality: { value: 'high', options: ['low', 'medium', 'high'] }
    }, { collapsed: true }),

    // Actions
    'Reset': button(() => console.log('Reset!')),
    'Actions': buttonGroup({
      Save: () => console.log('Save'),
      Load: () => console.log('Load')
    })
  })

  return (
    <motion.div
      style={{
        backgroundColor: color,
        opacity,
        width: size === 'small' ? 100 : size === 'medium' ? 200 : 300
      }}
      animate={{ x: position.x, y: position.y }}
      transition={{ duration: duration / 1000 }}
    >
      {name} - {count}
    </motion.div>
  )
}
```

## When to Use Leva

✅ **Use Leva when:**
- Building interactive prototypes
- Debugging visual components
- Creating design system demos
- Fine-tuning animations
- Building configurators
- Creating interactive documentation
- Developing with React Three Fiber

❌ **Don't use Leva for:**
- Production user-facing forms (use proper form libraries)
- Complex validation requirements
- Multi-step wizards
- Data entry applications

Leva excels at rapid prototyping and real-time parameter tweaking during development!
