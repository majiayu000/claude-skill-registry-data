---
name: pikacss-expert
description: Comprehensive user guidance for PikaCSS API, configuration, style definition, plugin usage, and best practices for building with atomic CSS.
license: MIT
metadata:
  author: PikaCSS Team
  version: "2.0.0"
compatibility: Works with all PikaCSS setups - Vite, Nuxt, or other bundlers
---

# PikaCSS User & API Expert Guide

This skill provides comprehensive guidance for using PikaCSS, understanding its API, configuring projects, and implementing styles effectively.

## Quick Start

### Basic Usage

```typescript
import { pika } from '@pikacss/core'

// Define styles
const styles = pika({
  display: 'flex',
  gap: '1rem',
  padding: '2rem',
  backgroundColor: 'white',
  borderRadius: '0.5rem'
})

// Use generated class names
console.log(styles.className)
```

### In Your Framework

**Vue/Nuxt:**
```vue
<template>
  <div :class="styles.className">
    Content here
  </div>
</template>

<script setup>
import { pika } from '@pikacss/core'

const styles = pika({
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem'
})
</script>
```

**React:**
```typescript
import { pika } from '@pikacss/core'

const styles = pika({
  padding: '1rem',
  borderRadius: '0.25rem'
})

export function MyComponent() {
  return <div className={styles.className}>Hello</div>
}
```

## Core Concepts

### Static Evaluation Requirement

All `pika()` arguments must be statically determinable at build time:

```typescript
// ✅ Allowed (static values)
const styles = pika({ color: 'red' })
const COLOR = 'blue'
const styles2 = pika({ color: COLOR })

// ❌ Not allowed (runtime variables)
function Component({ color }) {
  const styles = pika({ color }) // Error!
}

// ✅ Solution: Use CSS variables for dynamic values
const styles = pika({ color: 'var(--user-color)' })
function Component({ color }) {
  return <div style={{ '--user-color': color }} className={styles.className} />
}
```

### Generated Output

PikaCSS generates:
1. **Atomic CSS** (`pika.gen.css`) - Tiny, reusable style rules
2. **TypeScript definitions** (`pika.gen.ts`) - Full autocomplete and type safety

```css
/* pika.gen.css - atomic rules */
.display-flex { display: flex; }
.gap-1rem { gap: 1rem; }
.padding-2rem { padding: 2rem; }
```

### Atomic CSS Advantage

Each utility generates a single CSS rule:
- **No duplication** - `.display-flex` appears once, shared by all uses
- **Tiny output** - Compound 100 styles = 100 rules, not larger files
- **Tree-shakable** - Unused styles don't make it to production
- **Predictable** - Same input always generates same class

## Style Definition API

### Basic Properties

Define styles using CSS property names:

```typescript
pika({
  // Layout
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem',
  
  // Sizing
  width: '100%',
  minHeight: '500px',
  
  // Colors
  color: 'white',
  backgroundColor: '#1a1a1a',
  
  // Spacing
  padding: '2rem',
  margin: '1rem',
  
  // Borders
  border: '1px solid #ddd',
  borderRadius: '0.5rem'
})
```

### Pseudo-Elements

Use `$` prefix for pseudo-elements:

```typescript
pika({
  color: 'blue',
  $before: {
    content: '"→ "',
    color: 'gray'
  },
  $after: {
    content: ' ←"',
    color: 'gray'
  },
  $firstLine: {
    fontWeight: 'bold'
  }
})
```

### Pseudo-Classes

Use `&` or state selectors:

```typescript
pika({
  backgroundColor: 'white',
  '&:hover': {
    backgroundColor: '#f5f5f5'
  },
  '&:active': {
    transform: 'scale(0.95)'
  },
  '&:focus-visible': {
    outline: '2px solid blue'
  }
})
```

### Responsive Design

Use media query syntax:

```typescript
pika({
  display: 'grid',
  gridTemplateColumns: '1fr',
  
  // Mobile-first
  '@media (min-width: 768px)': {
    gridTemplateColumns: '1fr 1fr'
  },
  '@media (min-width: 1024px)': {
    gridTemplateColumns: '1fr 1fr 1fr'
  }
})
```

### Dark Mode

Support dark mode with system preference:

```typescript
pika({
  backgroundColor: 'white',
  color: 'black',
  
  '@media (prefers-color-scheme: dark)': {
    backgroundColor: '#1a1a1a',
    color: 'white'
  }
})
```

## Shortcuts & Utilities

### Using Built-in Shortcuts

Shortcuts provide quick access to common patterns:

```typescript
// Icon shortcut from @pikacss/plugin-icons
pika({
  icon: {
    name: 'chevron-right',
    size: '24px',
    color: 'blue'
  }
})

// Typography shortcuts from @pikacss/plugin-typography
pika({
  h1: true,
  // Applies: fontSize, fontWeight, lineHeight for h1
})

// Button shortcut (if configured)
pika({
  btn: {
    variant: 'primary',
    size: 'md'
  }
})
```

### Shortcut Resolution

Shortcuts resolve to full style definitions:

```typescript
// Icon shortcut resolves to:
// {
//   display: 'inline-block',
//   width: '24px',
//   height: '24px',
//   backgroundColor: 'blue',
//   maskImage: 'url(...)'
// }
```

## Configuration

### Engine Configuration

Configure the core engine:

```typescript
import { createEngine } from '@pikacss/core'
import { iconPlugin } from '@pikacss/plugin-icons'
import { resetPlugin } from '@pikacss/plugin-reset'
import { typographyPlugin } from '@pikacss/plugin-typography'

const engine = createEngine({
  // Plugin configuration
  plugins: [
    resetPlugin(),
    iconPlugin({
      sets: ['heroicons', 'lucide']
    }),
    typographyPlugin({
      defaultFontFamily: 'system-ui'
    })
  ],
  
  // Default theme values
  theme: {
    colors: {
      primary: '#3b82f6',
      secondary: '#10b981'
    },
    spacing: {
      xs: '0.25rem',
      sm: '0.5rem',
      md: '1rem',
      lg: '1.5rem'
    }
  }
})
```

### Vite/Build Integration

In your Vite config:

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePikaCSSPlugin } from '@pikacss/vite-plugin-pikacss'

export default defineConfig({
  plugins: [
    vue(),
    VitePikaCSSPlugin({
      // Configuration
      plugins: [/* your plugins */],
      theme: {
        // Theme configuration
      }
    })
  ]
})
```

### Nuxt Integration

In your Nuxt config:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pikacss/nuxt-pikacss'],
  
  pikacss: {
    plugins: [/* your plugins */],
    theme: {
      // Theme configuration
    }
  }
})
```

## Best Practices

### 1. Use Shortcuts for Consistency

```typescript
// ❌ Avoid repeating common patterns
pika({
  padding: '0.75rem 1rem',
  borderRadius: '0.375rem',
  backgroundColor: '#3b82f6',
  color: 'white',
  fontWeight: '500'
})

// ✅ Use shortcut instead
pika({
  btn: { variant: 'primary', size: 'md' }
})
```

### 2. Compose Styles

```typescript
// Create reusable style bases
const flexCenter = pika({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center'
})

const card = pika({
  backgroundColor: 'white',
  borderRadius: '0.5rem',
  boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
})

// Combine them
const button = pika({
  ...flexCenter,
  ...card,
  gap: '0.5rem'
})
```

### 3. Use CSS Variables for Dynamic Values

```typescript
// Static definition
const styles = pika({
  color: 'var(--button-color)',
  backgroundColor: 'var(--button-bg)'
})

// Dynamic values via props
<button 
  :class="styles.className"
  :style="{
    '--button-color': isDanger ? 'red' : 'blue',
    '--button-bg': isDanger ? '#fee' : '#eff'
  }"
>
  Click me
</button>
```

### 4. Responsive Design Pattern

```typescript
const grid = pika({
  display: 'grid',
  gap: '1rem',
  gridTemplateColumns: '1fr',
  
  '@media (min-width: 640px)': {
    gridTemplateColumns: 'repeat(2, 1fr)'
  },
  '@media (min-width: 1024px)': {
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '2rem'
  }
})
```

### 5. Theme Customization

```typescript
// Define consistent theme
const theme = {
  colors: {
    primary: '#3b82f6',
    success: '#10b981',
    danger: '#ef4444',
    warning: '#f59e0b'
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem'
  },
  radius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem'
  }
}

// Use consistently
const btn = pika({
  backgroundColor: theme.colors.primary,
  borderRadius: theme.radius.md,
  padding: `${theme.spacing.sm} ${theme.spacing.md}`
})
```

### 6. Avoid These Patterns

```typescript
// ❌ DON'T: Try to use runtime values
const Component = ({ size }) => {
  const styles = pika({ 
    width: size // ERROR - size is runtime
  })
}

// ❌ DON'T: Nest pika() calls unnecessarily
pika({
  nested: pika({ color: 'red' })
})

// ❌ DON'T: Mix concerns in one pika call
pika({
  // Component state (should use CSS variables)
  opacity: isDisabled ? 0.5 : 1,
  
  // Layout (separate concern)
  display: 'flex'
})

// ✅ DO: Use CSS variables for runtime values
const styles = pika({
  width: 'var(--size)',
  opacity: 'var(--opacity)'
})

// ✅ DO: Apply runtime values separately
<div :style="{ '--size': size, '--opacity': isDisabled ? 0.5 : 1 }" />
```

## Common Patterns

### Button Component

```typescript
// Base button styles
const buttonBase = pika({
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '0.5rem',
  padding: '0.75rem 1rem',
  borderRadius: '0.375rem',
  border: 'none',
  fontWeight: '500',
  cursor: 'pointer',
  transition: 'all 0.2s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
  },
  '&:active': {
    transform: 'translateY(0)'
  },
  '&:disabled': {
    opacity: '0.5',
    cursor: 'not-allowed'
  }
})

// Variant styles
const buttonPrimary = pika({
  backgroundColor: '#3b82f6',
  color: 'white',
  '&:hover': {
    backgroundColor: '#2563eb'
  }
})
```

### Card Component

```typescript
const card = pika({
  backgroundColor: 'white',
  borderRadius: '0.5rem',
  border: '1px solid #e5e7eb',
  boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  overflow: 'hidden',
  
  '@media (prefers-color-scheme: dark)': {
    backgroundColor: '#1f2937',
    borderColor: '#374151'
  }
})

const cardHeader = pika({
  padding: '1.5rem',
  borderBottom: '1px solid #e5e7eb'
})

const cardBody = pika({
  padding: '1.5rem'
})

const cardFooter = pika({
  padding: '1rem 1.5rem',
  backgroundColor: '#f9fafb'
})
```

### Grid Layout

```typescript
const gridContainer = pika({
  display: 'grid',
  gridTemplateColumns: '1fr',
  gap: '1rem',
  
  '@media (min-width: 640px)': {
    gridTemplateColumns: 'repeat(2, 1fr)'
  },
  '@media (min-width: 1024px)': {
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '2rem'
  }
})
```

## See Also

For more details, see the reference guides:
- [references/API-REFERENCE.md](references/API-REFERENCE.md) - Complete API documentation
- [references/PLUGIN-GUIDE.md](references/PLUGIN-GUIDE.md) - Using plugins
- [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Common issues and solutions
