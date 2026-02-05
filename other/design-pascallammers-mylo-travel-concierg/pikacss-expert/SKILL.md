---
name: pikacss-expert
description: Expert guidance for using PikaCSS—an Atomic CSS-in-JS engine that combines CSS-in-JS syntax with Atomic CSS output. Use when users ask about PikaCSS styling, configuration, plugins, shortcuts, selectors, TypeScript integration, or need help writing PikaCSS code.
license: MIT
metadata:
  version: 0.0.38
  category: css-in-js
  framework: agnostic
allowed-tools: read
---

## Purpose
Use this skill to assist users with PikaCSS, an Atomic CSS-in-JS engine that transforms CSS-in-JS code into atomic CSS at build time. This skill provides expert guidance on syntax, configuration, plugins, best practices, and troubleshooting.

## When to Use This Skill
- User asks about PikaCSS features, concepts, or usage
- User needs help writing `pika()` style declarations
- User wants to configure PikaCSS (config file, plugins, shortcuts, etc.)
- User needs TypeScript autocomplete or type safety guidance
- User asks about selectors, nested styles, or special properties
- User wants to use or create plugins (icons, reset, typography, custom)
- User needs integration help (Vite, Nuxt, Webpack, Rspack, esbuild, Farm)
- Troubleshooting PikaCSS-related issues

## Core Concepts

### What is PikaCSS?
PikaCSS is an **Atomic CSS-in-JS engine** that lets you:
- **Write** styles in familiar CSS-in-JS syntax (no utility class memorization)
- **Output** atomic CSS classes for optimal performance
- **Transform** styles at build time (zero runtime overhead)
- **Support** any framework (framework-agnostic)
- **Get** TypeScript autocomplete and type safety

**⚠️ Zero Runtime Constraint**: Because PikaCSS transforms styles at build time, all arguments to `pika()` functions must be **statically analyzable**. Runtime variables, dynamic expressions, or function calls are **not supported**.

**Key Benefits:**
- Zero learning curve (just use CSS property names)
- Zero runtime (build-time transformation)
- Small CSS bundle size (atomic CSS deduplication)
- Excellent DX (TypeScript support, style preview)

## Basic Usage

### The `pika()` Function

The main API is the `pika()` function with three variants:

```ts
// pika.str(...) - Returns space-separated class names (default)
const classes = pika.str({ color: 'red', fontSize: '16px' })
// Returns: "a b"

// pika.arr(...) - Returns array of class names
const classList = pika.arr({ color: 'red', fontSize: '16px' })
// Returns: ["a", "b"]

// pika.inl(...) - Returns inline class string (unquoted)
const inline = `class="${pika.inl({ color: 'red' })}"`
// Returns: "class=a"

// Short form defaults to .str
const shorthand = pika({ color: 'red' })
// Same as pika.str({ color: 'red' })
```

**⚠️ Build-Time Evaluation**: All `pika()` arguments are evaluated at build time:

```ts
// ✅ VALID - Static values
const classes = pika({ color: 'red', fontSize: '16px' })

// ✅ VALID - String literals
const primary = pika({ color: '#3b82f6' })

// ❌ INVALID - Runtime variables
const userColor = getUserColor() // Runtime function
const classes = pika({ color: userColor }) // ERROR: Cannot evaluate at build time

// ❌ INVALID - Dynamic expressions
const size = props.size // Runtime prop
const classes = pika({ fontSize: size }) // ERROR: Dynamic value

// ✅ SOLUTION - Use CSS variables for runtime values
const classes = pika({ color: 'var(--user-color)' })
// Then set the variable at runtime: style={{ '--user-color': userColor }}
```

### Style Objects

```ts
pika({
  // Standard CSS properties
  display: 'flex',
  alignItems: 'center',
  padding: '1rem',
  
  // camelCase or kebab-case both work
  backgroundColor: '#fff',
  'background-color': '#fff',
  
  // Numbers or strings
  margin: 0,
  fontSize: '16px',
})
```

## Selectors and Nesting

### The `$` Symbol
Use `$` to represent the current element's selector (the atomic class):

```ts
pika({
  'color': 'black',
  
  // Pseudo-classes
  '$:hover': {
    color: 'blue',
  },
  '$:active': {
    transform: 'scale(0.98)',
  },
  
  // Pseudo-elements
  '$::before': {
    content: '"*"',
    color: 'red',
  },
  '$::after': {
    content: '""',
    display: 'block',
  },
  
  // Combinators
  '$ > span': {
    fontWeight: 'bold',
  },
  '$ + div': {
    marginTop: '1rem',
  },
  '$ ~ p': {
    color: 'gray',
  },
  
  // Class combinations
  '$.active': {
    backgroundColor: 'yellow',
  },
  '$.disabled:hover': {
    cursor: 'not-allowed',
  },
  
  // Parent selectors
  'div > $': {
    margin: '1rem',
  },
  '.container $': {
    padding: '1rem',
  },
})
```

**Output:** Each selector gets transformed to CSS:
- `$:hover` → `.xxx:hover`
- `$::before` → `.xxx::before`
- `$ > span` → `.xxx > span`
- `$.active` → `.xxx.active`
- `div > $` → `div > .xxx`

### Nested Structures

```ts
pika({
  'display': 'grid',
  'gap': '1rem',
  
  // Media query with selectors
  '@media (min-width: 768px)': {
    '$:hover': {
      transform: 'scale(1.05)',
    },
  },
  
  // Selector with media query
  '$:hover': {
    '@media (prefers-reduced-motion)': {
      transition: 'none',
    },
  },
  
  // Complex nesting
  '$.active::before': {
    'content': '"✓"',
    '@media (max-width: 768px)': {
      display: 'none',
    },
  },
  
  // Feature queries
  '@supports (display: grid)': {
    '$ > *': {
      gridColumn: 'span 2',
    },
  },
})
```

**Limit:** Nesting is limited to 5 levels (sufficient for most use cases).

## Special Properties

### `__important`
Adds `!important` to all properties:

```ts
pika({
  __important: true,
  color: 'red',
  fontSize: '16px'
})
// Output: color: red !important; font-size: 16px !important;
```

### `__shortcut`
Apply shortcuts within style objects:

```ts
// Single shortcut
pika({
  __shortcut: 'btn',
  color: 'blue'
})

// Multiple shortcuts
pika({
  __shortcut: ['btn', 'text-center']
})
```

## Shortcuts

Shortcuts are reusable style combinations defined in `pika.config.ts`:

### Static Shortcuts

```ts
export default defineEngineConfig({
  shortcuts: {
    shortcuts: [
      ['flex-center', {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }],
      ['card', {
        padding: '1rem',
        borderRadius: '0.5rem',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
      }],
    ]
  }
})
```

### Dynamic Shortcuts

```ts
shortcuts: [
  // Pattern matching with transform function
  [/^m-(\d+)$/, m => ({ margin: `${m[1]}px` }), ['m-4', 'm-8', 'm-16']],
  [/^p-(\d+)$/, m => ({ padding: `${m[1]}px` }), ['p-4', 'p-8']],
  [/^grid-cols-(\d+)$/, m => ({
    display: 'grid',
    gridTemplateColumns: `repeat(${m[1]}, minmax(0, 1fr))`
  }), ['grid-cols-2', 'grid-cols-3', 'grid-cols-4']],
]
```

**Third parameter** provides autocomplete suggestions.

### Using Shortcuts

```ts
// Direct string usage
pika('flex-center')
pika('flex-center', 'card')
pika('m-4')

// Combine with style objects
pika('flex-center', { color: 'blue' })

// Using __shortcut property
pika({
  __shortcut: 'flex-center',
  color: 'blue',
})
```

## Configuration

Create `pika.config.ts` in your project root:

```ts
/// <reference path="./src/pika.gen.ts" />

import { defineEngineConfig } from '@pikacss/core'
// Or from integration packages:
// import { defineEngineConfig } from '@pikacss/unplugin-pikacss'

export default defineEngineConfig({
  // Register plugins
  plugins: [
    icons(),
    reset(),
  ],
  
  // Prefix for atomic class IDs
  prefix: 'pika-',
  
  // Default selector format (% = atomic ID)
  defaultSelector: '.%',
  // Or use attribute selector: '[data-pika~="%"]'
  
  // Global CSS (CSS variables, animations, resets)
  preflights: [
    ':root { --color-primary: #3b82f6; }',
    // Or function:
    ({ engine, isFormatted }) => {
      return '/* Generated preflight */'
    }
  ],
  
  // Shortcuts configuration
  shortcuts: {
    shortcuts: [
      ['flex-center', { display: 'flex', alignItems: 'center', justifyContent: 'center' }],
    ]
  },
  
  // Other plugin options...
  icons: {
    prefix: 'i-',
    scale: 1,
  },
})
```

**Important:** Always add `/// <reference path="./src/pika.gen.ts" />` at the top for TypeScript support.

## Plugin System

### Core Plugins (Built-in)
- `variables`: CSS custom properties management
- `keyframes`: @keyframes animations
- `selectors`: Custom selector transformations
- `shortcuts`: Style shortcuts
- `important`: !important declarations

### Official Plugins

#### Icons Plugin
```bash
npm install -D @pikacss/plugin-icons
```

```ts
import { icons } from '@pikacss/plugin-icons'

export default defineEngineConfig({
  plugins: [icons()],
  icons: {
    prefix: 'i-',
    scale: 1.2,
    collections: ['mdi', 'carbon'],
  }
})
```

#### Reset Plugin
```bash
npm install -D @pikacss/plugin-reset
```

```ts
import { reset } from '@pikacss/plugin-reset'

export default defineEngineConfig({
  plugins: [reset()],
  reset: 'modern-normalize' // 'modern-normalize' | 'normalize' | 'andy-bell' | 'eric-meyer' | 'the-new-css-reset'
})
```

#### Typography Plugin
```bash
npm install -D @pikacss/plugin-typography
```

**pika.config.ts**:
```ts
import { defineEngineConfig } from '@pikacss/core'
import { typography } from '@pikacss/plugin-typography'

export default defineEngineConfig({
  plugins: [
    typography({
      variables: {
        '--pk-prose-color-body': '#374151',
        '--pk-prose-color-headings': '#111827',
      }
    })
  ]
})
```

**Usage:**
```ts
// Complete prose (all typography styles)
pika('prose')

// Modular shortcuts - each automatically includes prose-base
pika('prose-headings prose-paragraphs')
pika('prose-headings prose-code prose-lists')

// Common combinations
pika('prose-headings prose-paragraphs prose-links prose-emphasis prose-lists') // Blog post
pika('prose-headings prose-paragraphs prose-code prose-lists prose-links') // Technical docs
pika('prose-headings prose-paragraphs prose-links prose-quotes prose-media') // News article
pika('prose-headings prose-paragraphs prose-tables') // Data page

// Size modifiers (includes full prose styles)
pika('prose-sm')  // Small
pika('prose-lg')  // Large
pika('prose-xl')  // Extra large
pika('prose-2xl') // 2X large
```

**Available modular shortcuts (each includes `prose-base` automatically):**
- `prose-base` - Base container styles (color, max-width, font-size, line-height)
- `prose-paragraphs` - Paragraph and lead text styles (includes `prose-base`)
- `prose-links` - Link styles (includes `prose-base`)
- `prose-emphasis` - Strong/em styles (includes `prose-base`)
- `prose-kbd` - Keyboard input styles (includes `prose-base`)
- `prose-lists` - List styles (ul, ol, li, dl, dt, dd) (includes `prose-base`)
- `prose-hr` - Horizontal rule (includes `prose-base`)
- `prose-headings` - h1-h4 styles (includes `prose-base`)
- `prose-quotes` - Blockquote styles (includes `prose-base`)
- `prose-media` - Image/video/figure styles (includes `prose-base`)
- `prose-code` - Code/pre styles (includes `prose-base`)
- `prose-tables` - Table styles (includes `prose-base`)
- `prose` - Combines all modular shortcuts (not `prose-base` directly, but includes it through modular shortcuts)

**Modular benefits:**
- ✅ Smaller CSS bundle (only load what you need)
- ✅ Better performance (less CSS to parse)
- ✅ More flexible (combine exactly what you need)
- ✅ Easier debugging (know exactly which styles are applied)
- ✅ Automatic deduplication (engine removes duplicate prose-base)

### Plugin Configuration Pattern
```ts
export default defineEngineConfig({
  // 1. Register plugin in plugins array
  plugins: [icons()],
  
  // 2. Configure at root level
  icons: {
    prefix: 'i-',
    scale: 1,
  }
})
```

**Common mistake:** Don't forget to call the plugin function: `plugins: [icons()]` not `plugins: [icons]`

## Framework Integration

### Vite
```bash
npm install -D @pikacss/unplugin-pikacss
```

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import pikacss from '@pikacss/unplugin-pikacss/vite'

export default defineConfig({
  plugins: [
    pikacss({ /* options */ })
  ]
})
```

### Nuxt
```bash
npm install -D @pikacss/nuxt-pikacss
```

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pikacss/nuxt-pikacss'],
  pikacss: {
    // options
  }
})
```

### Webpack / Rspack / esbuild / Farm
All use the unplugin adapter:

```bash
npm install -D @pikacss/unplugin-pikacss
```

See integration documentation for specific bundler setup.

## TypeScript Support

PikaCSS automatically generates type definitions:

1. **Auto-generated file:** `src/pika.gen.ts` (or configured location)
2. **Autocomplete:** Get suggestions for shortcuts, selectors, CSS properties
3. **Type safety:** Catch errors at compile time
4. **Style preview:** Hover over `pikap()` function to see generated CSS

### Previewing Styles
Use `pikap()` instead of `pika()` to enable hover preview:

```ts
// Hover over pikap() to see generated CSS
const classes = pikap({
  color: 'red',
  fontSize: '16px',
})
```

## Best Practices

### 1. Organize Shortcuts Logically
```ts
// Layout shortcuts
['flex-center', ...],
['grid-cols-3', ...],

// Component shortcuts
['btn', ...],
['card', ...],

// Utility shortcuts
[/^m-(\d+)$/, ...],
[/^p-(\d+)$/, ...],
```

### 2. Use Composition
Create small, focused shortcuts and compose them:

```ts
['btn-base', { padding: '0.5rem 1rem', borderRadius: '0.25rem' }],
['btn-primary', { __shortcut: 'btn-base', backgroundColor: 'blue', color: 'white' }],
['btn-secondary', { __shortcut: 'btn-base', backgroundColor: 'gray', color: 'white' }],
```

### 3. Provide Autocomplete
Always include autocomplete array for dynamic shortcuts:

```ts
[/^m-(\d+)$/, m => ({ margin: `${m[1]}px` }), ['m-4', 'm-8', 'm-16', 'm-24']],
```

### 4. Use Semantic Names
```ts
// Good
['primary-button', ...],
['error-message', ...],

// Avoid
['blue-btn', ...],
['red-text', ...],
```

### 5. Leverage Preflights for Global Styles
Use `preflights` for CSS variables, global animations, and base styles:

```ts
preflights: [
  ':root { --primary: #3b82f6; --secondary: #64748b; }',
  '@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }',
]
```

## Common Patterns

### Responsive Design
```ts
pika({
  'width': '100%',
  '@media (min-width: 640px)': {
    width: '50%',
  },
  '@media (min-width: 1024px)': {
    width: '33.333%',
  },
})
```

### Dark Mode
```ts
pika({
  'backgroundColor': '#fff',
  'color': '#000',
  '@media (prefers-color-scheme: dark)': {
    backgroundColor: '#000',
    color: '#fff',
  },
})
```

### Component Variants
```ts
// Define shortcuts for variants
shortcuts: [
  ['btn-base', {
    display: 'inline-flex',
    padding: '0.5rem 1rem',
    borderRadius: '0.25rem',
    cursor: 'pointer',
  }],
  ['btn-sm', { __shortcut: 'btn-base', padding: '0.25rem 0.5rem', fontSize: '14px' }],
  ['btn-lg', { __shortcut: 'btn-base', padding: '0.75rem 1.5rem', fontSize: '18px' }],
]

// Usage
<button className={pika('btn-sm')}>Small</button>
<button className={pika('btn-base')}>Normal</button>
<button className={pika('btn-lg')}>Large</button>
```

## Troubleshooting

### Issue: Styles Not Applied
1. Verify the generated CSS file is imported in your entry file
2. Check `pika.gen.css` exists in the output directory
3. Ensure the build tool plugin is correctly configured
4. Check browser DevTools to see if classes are present

### Issue: TypeScript Errors
1. Add `/// <reference path="./src/pika.gen.ts" />` to config file
2. Ensure `pika.gen.ts` is generated (run dev/build once)
3. Restart TypeScript server (VS Code: "TypeScript: Restart TS Server")

### Issue: Shortcuts Not Working
1. Verify shortcut is defined in `pika.config.ts`
2. Check shortcut name matches exactly (case-sensitive)
3. For dynamic shortcuts, ensure pattern matches input
4. Rebuild to regenerate type definitions

### Issue: Build Performance
1. Use filters when working in monorepos
2. Keep shortcuts focused and avoid overly complex patterns
3. Minimize deep nesting (remember 5-level limit)

## Reference Documentation

For detailed information, refer to:
- [API Reference](references/api-reference.md) - Complete API documentation
- [Plugin Hooks](references/plugin-hooks.md) - Plugin development details
- [Examples](references/examples.md) - Real-world usage patterns

## Key Reminders

1. **PikaCSS is build-time only** - No runtime overhead; all `pika()` arguments must be statically analyzable
2. **No runtime code in `pika()` calls** - Cannot use variables, function calls, or dynamic expressions that are only available at runtime
3. **Use CSS variables for dynamic values** - When you need runtime flexibility, use CSS custom properties
4. **Use `$` for selectors** - Represents current atomic class
5. **Shortcuts are powerful** - Use them for reusable patterns
6. **TypeScript is first-class** - Always configure properly
7. **Framework agnostic** - Works with any framework
8. **Atomic CSS output** - Small, optimized CSS bundles
9. **Zero learning curve** - Just CSS properties, no memorization

## Example: Complete Setup

```ts
// pika.config.ts
/// <reference path="./src/pika.gen.ts" />

import { defineEngineConfig } from '@pikacss/unplugin-pikacss'
import { icons } from '@pikacss/plugin-icons'
import { reset } from '@pikacss/plugin-reset'

export default defineEngineConfig({
  plugins: [icons(), reset()],
  
  prefix: 'pika-',
  
  preflights: [
    ':root { --primary: #3b82f6; --secondary: #64748b; }',
  ],
  
  shortcuts: {
    shortcuts: [
      // Layout
      ['flex-center', {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }],
      
      // Components
      ['btn', {
        display: 'inline-flex',
        alignItems: 'center',
        padding: '0.5rem 1rem',
        borderRadius: '0.25rem',
        cursor: 'pointer',
      }],
      
      // Utilities
      [/^m-(\d+)$/, m => ({ margin: `${m[1]}px` }), ['m-4', 'm-8', 'm-16']],
    ]
  },
  
  icons: {
    prefix: 'i-',
    scale: 1,
  },
  
  reset: 'modern-normalize',
})
```

```tsx
// App.tsx

function App() {
  return (
    <div className={pika('flex-center', { height: '100vh' })}>
      <button className={pika('btn', {
        'backgroundColor': 'var(--primary)',
        'color': 'white',
        '$:hover': {
          backgroundColor: 'var(--secondary)',
        },
      })}>
        Click Me
      </button>
    </div>
  )
}
```

## Debugging and Troubleshooting

### Quick Debug Checklist
1. Verify `pika.gen.{css,ts}` exist
2. Check `import 'pika.css'` in entry
3. Inspect element → classes → computed styles
4. Network tab → CSS loaded?
5. Console → errors?
6. Source → pika() transformed?
7. Config → plugin loaded?

### Common Fixes
- **No styles**: Import pika.css, check gen files, verify Network tab
- **pika undefined**: Add `/// <reference path="./pika.gen.ts" />`, ensure file is in `scan.include`, restart TS
- **TS errors**: Update tsconfig.json includes, restart TS server
- **No HMR**: Check scan patterns, restart dev

## Performance Tips

**Build**: Optimize scan patterns, use shortcuts for repeated styles
**Runtime**: CSS bundle 5-100KB (atomic, auto-optimized)
**Loading**: Inline critical CSS or preload, enable minification

## Migration Quick Reference

**Tailwind → PikaCSS**: `class="flex p-4"` → `pika({ display: 'flex', padding: '1rem' })`
**Styled → PikaCSS**: Replace `&` with `$`, use shortcuts for reuse
**Key**: Build-time only - use CSS variables for runtime values

## Testing Best Practice

Test computed styles, not class names:
```typescript
const styles = window.getComputedStyle(button)
expect(styles.backgroundColor).toBe('rgb(59, 130, 246)')
```

## Additional Documentation

- [Real-World Examples](/docs/examples/components.md)
- [Performance Optimization](/docs/advanced/performance.md)
- [Testing & Debugging](/docs/advanced/testing.md)
- [SSR/SSG Guide](/docs/advanced/ssr.md)
- [Plugin Development](/docs/advanced/plugin-development.md)
- [Comparison Guide](/docs/getting-started/comparison.md)
- [Migration Guide](/docs/guide/migration.md)
- [FAQ](/docs/community/faq.md)
- [Contributing](/docs/community/contributing.md)

````
