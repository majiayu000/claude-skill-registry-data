---
name: design-system-manager
description: Create and manage design systems with design tokens, theming (light/dark mode), standardized spacing, colors, typography, and component registry
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Design System Manager

Expert skill for creating and maintaining scalable design systems. Specializes in design tokens, theming systems, color palettes, typography scales, spacing systems, and component documentation.

## Core Capabilities

### 1. Design Tokens
- Color tokens (primitive, semantic, component-specific)
- Spacing tokens (scale system)
- Typography tokens (font families, sizes, weights, line heights)
- Shadow tokens (elevation system)
- Border radius tokens
- Animation tokens (duration, easing)
- Z-index tokens (layering system)

### 2. Theming System
- Light/dark mode support
- Custom theme creation
- Theme switching mechanism
- CSS variables strategy
- Scoped theming
- Theme inheritance
- RTL (Right-to-Left) support

### 3. Color System
- Color palette generation
- Semantic color naming
- Accessibility compliance (WCAG contrast)
- Color scales (50-900)
- Alpha variants
- State colors (hover, active, disabled)
- Status colors (success, warning, error, info)

### 4. Typography System
- Type scale generation
- Font stack management
- Line height ratios
- Letter spacing
- Font weight system
- Responsive typography
- Web font loading strategies

### 5. Spacing System
- Spacing scale (4pt/8pt grid)
- Consistent padding/margin
- Component spacing
- Layout spacing
- Responsive spacing
- Negative spacing

### 6. Component Registry
- Component catalog
- Variant documentation
- Usage guidelines
- Prop documentation
- Anatomy diagrams
- Do's and Don'ts

## Workflow

### Phase 1: Foundation Setup
1. **Define Design Principles**
   - Visual identity
   - Brand personality
   - Design philosophy
   - Constraints and guidelines

2. **Create Token Structure**
   - Primitive tokens (base values)
   - Semantic tokens (meaningful names)
   - Component tokens (specific usage)
   - Decision tree for token usage

3. **Set Up Tooling**
   - Token management (Style Dictionary)
   - CSS-in-JS solution
   - Build pipeline
   - Documentation platform

### Phase 2: Token Creation
1. **Color Tokens**
   - Define color palette
   - Create semantic mappings
   - Generate scales
   - Ensure accessibility

2. **Spacing Tokens**
   - Define spacing scale
   - Create consistent system
   - Document usage patterns

3. **Typography Tokens**
   - Define type scale
   - Set font families
   - Create text styles
   - Define responsive behavior

4. **Other Tokens**
   - Shadows and elevation
   - Border radius
   - Animation timing
   - Breakpoints

### Phase 3: Theme Implementation
1. **Create Theme System**
   - Define theme structure
   - Implement switching mechanism
   - Set up CSS variables
   - Handle SSR (Server-Side Rendering)

2. **Build Theme Variants**
   - Light mode
   - Dark mode
   - Custom themes
   - Brand variations

3. **Test Themes**
   - Visual consistency
   - Accessibility in all themes
   - Performance impact
   - Cross-browser compatibility

## Design Token Patterns

### Token Naming Convention
```typescript
// Primitive tokens (base values)
const primitive = {
  color: {
    blue: {
      50: '#eff6ff',
      100: '#dbeafe',
      // ... through 900
      900: '#1e3a8a',
    },
  },
}

// Semantic tokens (meaningful names)
const semantic = {
  color: {
    primary: primitive.color.blue[600],
    'primary-hover': primitive.color.blue[700],
    'primary-active': primitive.color.blue[800],
    background: primitive.color.white,
    'background-subtle': primitive.color.gray[50],
    text: primitive.color.gray[900],
    'text-subtle': primitive.color.gray[600],
  },
}

// Component tokens (specific usage)
const component = {
  button: {
    primary: {
      background: semantic.color.primary,
      text: primitive.color.white,
      border: semantic.color.primary,
    },
  },
}
```

### Style Dictionary Configuration
```javascript
// style-dictionary.config.js
module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [
        {
          destination: 'variables.css',
          format: 'css/variables',
        },
      ],
    },
    js: {
      transformGroup: 'js',
      buildPath: 'dist/js/',
      files: [
        {
          destination: 'tokens.js',
          format: 'javascript/es6',
        },
      ],
    },
    ts: {
      transformGroup: 'js',
      buildPath: 'dist/ts/',
      files: [
        {
          destination: 'tokens.ts',
          format: 'typescript/es6-declarations',
        },
      ],
    },
  },
}
```

### Token Files Structure
```
tokens/
├── global/
│   ├── color.json
│   ├── spacing.json
│   ├── typography.json
│   ├── shadow.json
│   └── radius.json
├── semantic/
│   ├── light.json
│   └── dark.json
└── component/
    ├── button.json
    ├── input.json
    └── card.json
```

### Color Token Example
```json
{
  "color": {
    "brand": {
      "primary": {
        "value": "#3b82f6",
        "type": "color"
      }
    },
    "gray": {
      "50": { "value": "#f9fafb", "type": "color" },
      "100": { "value": "#f3f4f6", "type": "color" },
      "200": { "value": "#e5e7eb", "type": "color" }
    }
  }
}
```

## Theming Implementation

### CSS Variables Theme
```css
/* tokens/light.css */
:root {
  /* Colors */
  --color-background: 255 255 255; /* RGB for alpha variants */
  --color-foreground: 0 0 0;
  --color-primary: 59 130 246;
  --color-secondary: 139 92 246;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-8: 2rem;

  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

  /* Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
}

/* tokens/dark.css */
[data-theme="dark"] {
  --color-background: 0 0 0;
  --color-foreground: 255 255 255;
  --color-primary: 96 165 250;
  --color-secondary: 167 139 250;
}

/* Usage with alpha */
.card {
  background-color: rgb(var(--color-background));
  color: rgb(var(--color-foreground));
  box-shadow: var(--shadow-md);
  border-radius: var(--radius-lg);
}

.overlay {
  background-color: rgb(var(--color-background) / 0.8);
}
```

### TypeScript Theme Provider
```typescript
// theme-provider.tsx
import { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'

interface ThemeContextValue {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'light' | 'dark'
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

export function ThemeProvider({
  children,
  defaultTheme = 'system',
  storageKey = 'ui-theme',
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem(storageKey) as Theme) || defaultTheme
  )

  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    const root = window.document.documentElement
    root.classList.remove('light', 'dark')

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)')
        .matches
        ? 'dark'
        : 'light'
      root.classList.add(systemTheme)
      setResolvedTheme(systemTheme)
    } else {
      root.classList.add(theme)
      setResolvedTheme(theme)
    }
  }, [theme])

  useEffect(() => {
    localStorage.setItem(storageKey, theme)
  }, [theme, storageKey])

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

### Tailwind CSS Integration
```javascript
// tailwind.config.js
module.exports = {
  darkMode: ['class'],
  theme: {
    extend: {
      colors: {
        background: 'rgb(var(--color-background) / <alpha-value>)',
        foreground: 'rgb(var(--color-foreground) / <alpha-value>)',
        primary: {
          DEFAULT: 'rgb(var(--color-primary) / <alpha-value>)',
          foreground: 'rgb(var(--color-primary-foreground) / <alpha-value>)',
        },
        secondary: {
          DEFAULT: 'rgb(var(--color-secondary) / <alpha-value>)',
          foreground: 'rgb(var(--color-secondary-foreground) / <alpha-value>)',
        },
      },
      spacing: {
        1: 'var(--spacing-1)',
        2: 'var(--spacing-2)',
        4: 'var(--spacing-4)',
        8: 'var(--spacing-8)',
      },
      fontSize: {
        xs: 'var(--text-xs)',
        sm: 'var(--text-sm)',
        base: 'var(--text-base)',
        lg: 'var(--text-lg)',
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
      },
    },
  },
}
```

## Color System

### Color Palette Generator
```typescript
// color-utils.ts
import { colord, extend } from 'colord'
import a11yPlugin from 'colord/plugins/a11y'

extend([a11yPlugin])

export function generateColorScale(baseColor: string) {
  const base = colord(baseColor)

  return {
    50: base.lighten(0.45).toHex(),
    100: base.lighten(0.4).toHex(),
    200: base.lighten(0.3).toHex(),
    300: base.lighten(0.2).toHex(),
    400: base.lighten(0.1).toHex(),
    500: baseColor,
    600: base.darken(0.1).toHex(),
    700: base.darken(0.2).toHex(),
    800: base.darken(0.3).toHex(),
    900: base.darken(0.4).toHex(),
  }
}

export function checkContrast(foreground: string, background: string) {
  const contrast = colord(foreground).contrast(background)

  return {
    contrast,
    passesAA: contrast >= 4.5,
    passesAAA: contrast >= 7,
    passesAALarge: contrast >= 3,
  }
}
```

### Semantic Color Mapping
```typescript
// colors.ts
export const colors = {
  // Primitive colors
  blue: generateColorScale('#3b82f6'),
  green: generateColorScale('#10b981'),
  red: generateColorScale('#ef4444'),
  gray: generateColorScale('#6b7280'),

  // Semantic colors
  primary: {
    DEFAULT: 'var(--color-primary)',
    hover: 'var(--color-primary-hover)',
    active: 'var(--color-primary-active)',
    disabled: 'var(--color-primary-disabled)',
  },

  // Status colors
  success: {
    DEFAULT: 'var(--color-success)',
    background: 'var(--color-success-bg)',
    border: 'var(--color-success-border)',
  },
  error: {
    DEFAULT: 'var(--color-error)',
    background: 'var(--color-error-bg)',
    border: 'var(--color-error-border)',
  },
  warning: {
    DEFAULT: 'var(--color-warning)',
    background: 'var(--color-warning-bg)',
    border: 'var(--color-warning-border)',
  },
  info: {
    DEFAULT: 'var(--color-info)',
    background: 'var(--color-info-bg)',
    border: 'var(--color-info-border)',
  },
}
```

## Typography System

### Type Scale
```typescript
// typography.ts
export const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },

  fontSize: {
    xs: ['0.75rem', { lineHeight: '1rem' }],
    sm: ['0.875rem', { lineHeight: '1.25rem' }],
    base: ['1rem', { lineHeight: '1.5rem' }],
    lg: ['1.125rem', { lineHeight: '1.75rem' }],
    xl: ['1.25rem', { lineHeight: '1.75rem' }],
    '2xl': ['1.5rem', { lineHeight: '2rem' }],
    '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
    '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
    '5xl': ['3rem', { lineHeight: '1' }],
  },

  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },

  letterSpacing: {
    tighter: '-0.05em',
    tight: '-0.025em',
    normal: '0',
    wide: '0.025em',
    wider: '0.05em',
  },
}
```

### Text Styles
```typescript
// text-styles.ts
export const textStyles = {
  h1: {
    fontSize: 'var(--text-5xl)',
    fontWeight: 'var(--font-bold)',
    lineHeight: '1',
    letterSpacing: 'var(--tracking-tight)',
  },
  h2: {
    fontSize: 'var(--text-4xl)',
    fontWeight: 'var(--font-bold)',
    lineHeight: '1.1',
  },
  h3: {
    fontSize: 'var(--text-3xl)',
    fontWeight: 'var(--font-semibold)',
    lineHeight: '1.2',
  },
  body: {
    fontSize: 'var(--text-base)',
    fontWeight: 'var(--font-normal)',
    lineHeight: '1.5',
  },
  caption: {
    fontSize: 'var(--text-sm)',
    fontWeight: 'var(--font-normal)',
    lineHeight: '1.25',
    color: 'var(--color-text-subtle)',
  },
}
```

### Responsive Typography
```css
/* Fluid typography using clamp() */
:root {
  --text-xs: clamp(0.69rem, 0.66rem + 0.16vw, 0.75rem);
  --text-sm: clamp(0.83rem, 0.78rem + 0.24vw, 0.94rem);
  --text-base: clamp(1rem, 0.93rem + 0.36vw, 1.19rem);
  --text-lg: clamp(1.2rem, 1.09rem + 0.53vw, 1.48rem);
  --text-xl: clamp(1.44rem, 1.29rem + 0.75vw, 1.86rem);
}
```

## Spacing System

### Spacing Scale (8pt Grid)
```typescript
// spacing.ts
export const spacing = {
  0: '0',
  0.5: '0.125rem',  // 2px
  1: '0.25rem',     // 4px
  1.5: '0.375rem',  // 6px
  2: '0.5rem',      // 8px
  2.5: '0.625rem',  // 10px
  3: '0.75rem',     // 12px
  3.5: '0.875rem',  // 14px
  4: '1rem',        // 16px
  5: '1.25rem',     // 20px
  6: '1.5rem',      // 24px
  7: '1.75rem',     // 28px
  8: '2rem',        // 32px
  9: '2.25rem',     // 36px
  10: '2.5rem',     // 40px
  12: '3rem',       // 48px
  16: '4rem',       // 64px
  20: '5rem',       // 80px
  24: '6rem',       // 96px
}
```

### Component Spacing Patterns
```typescript
// spacing-patterns.ts
export const componentSpacing = {
  button: {
    paddingX: {
      sm: 'var(--spacing-3)',
      md: 'var(--spacing-4)',
      lg: 'var(--spacing-6)',
    },
    paddingY: {
      sm: 'var(--spacing-1.5)',
      md: 'var(--spacing-2)',
      lg: 'var(--spacing-2.5)',
    },
    gap: 'var(--spacing-2)',
  },
  card: {
    padding: {
      sm: 'var(--spacing-4)',
      md: 'var(--spacing-6)',
      lg: 'var(--spacing-8)',
    },
    gap: 'var(--spacing-4)',
  },
  input: {
    paddingX: 'var(--spacing-3)',
    paddingY: 'var(--spacing-2)',
  },
}
```

## Component Registry

### Component Metadata
```typescript
// component-registry.ts
export interface ComponentMetadata {
  name: string
  category: 'form' | 'layout' | 'navigation' | 'feedback' | 'data-display'
  status: 'stable' | 'beta' | 'deprecated'
  accessibility: {
    roles: string[]
    keyboard: string[]
    screenReader: string
  }
  variants: Array<{
    name: string
    props: Record<string, any>
  }>
  examples: Array<{
    title: string
    code: string
  }>
}

export const componentRegistry: Record<string, ComponentMetadata> = {
  Button: {
    name: 'Button',
    category: 'form',
    status: 'stable',
    accessibility: {
      roles: ['button'],
      keyboard: ['Enter', 'Space'],
      screenReader: 'Announces as button with label',
    },
    variants: [
      { name: 'primary', props: { variant: 'primary' } },
      { name: 'secondary', props: { variant: 'secondary' } },
      { name: 'outline', props: { variant: 'outline' } },
    ],
    examples: [
      {
        title: 'Primary Button',
        code: '<Button variant="primary">Click me</Button>',
      },
    ],
  },
}
```

## Best Practices

### Design Tokens
1. **Three-Tier System**: Primitive → Semantic → Component tokens
2. **Meaningful Names**: Use semantic names, not descriptive ones
   - ✅ `color-primary`, `color-error`
   - ❌ `color-blue`, `color-red`
3. **Single Source of Truth**: Define once, reference everywhere
4. **Platform Agnostic**: Export to CSS, JS, iOS, Android
5. **Versioning**: Track token changes with semantic versioning

### Theming
1. **CSS Variables**: Use for runtime theme switching
2. **SSR Support**: Handle hydration correctly
3. **System Preference**: Respect user's OS theme preference
4. **Persistence**: Save theme choice to localStorage
5. **Smooth Transitions**: Animate theme changes subtly

### Color System
1. **Accessibility First**: Ensure WCAG AA/AAA compliance
2. **Consistent Scales**: Generate color scales systematically
3. **Semantic Mapping**: Primary, secondary, success, error, etc.
4. **Alpha Variants**: Support transparency with RGB values
5. **Dark Mode**: Test all colors in both themes

### Typography
1. **Type Scale**: Use consistent ratio (1.25, 1.333, 1.5)
2. **Line Height**: Appropriate for text length (1.5 for body, 1.2 for headings)
3. **Font Loading**: Optimize web font loading (swap, preload)
4. **Responsive**: Use clamp() for fluid typography
5. **Hierarchy**: Clear visual hierarchy through size and weight

### Spacing
1. **Consistent System**: Use 4pt or 8pt grid
2. **Relative Units**: Use rem for scalability
3. **Component Spacing**: Define spacing patterns per component
4. **Responsive**: Adjust spacing for different screen sizes
5. **Negative Spacing**: Support when needed

## Tools & Resources

### Essential Tools
- **Style Dictionary**: Token transformation platform
- **colord**: Color manipulation and contrast checking
- **Radix Colors**: Accessible color system
- **Tailwind CSS**: Utility-first CSS framework
- **Figma Tokens**: Sync tokens between Figma and code

### Typography Tools
- **Modern Font Stacks**: System font stacks
- **Google Fonts**: Web font library
- **Fontsource**: Self-hosted fonts via NPM
- **Type Scale Calculator**: Generate type scales

### Color Tools
- **Coolors**: Color palette generator
- **Adobe Color**: Color wheel and schemes
- **Contrast Checker**: WCAG contrast validation
- **oklch.css**: Perceptually uniform color space

## When to Use This Skill

Activate this skill when you need to:
- Set up a new design system
- Create design tokens
- Implement theming (light/dark mode)
- Define color palettes
- Create typography system
- Set up spacing system
- Document component patterns
- Ensure design consistency
- Improve accessibility
- Migrate to design tokens
- Audit existing design system

## Output Format

When working with design systems, provide:
1. **Token Files**: Complete token definitions
2. **Theme Configuration**: CSS variables and theme provider
3. **Usage Examples**: How to use tokens in components
4. **Accessibility Report**: WCAG compliance status
5. **Documentation**: Guidelines for using the design system
6. **Migration Guide**: If updating existing system

Always prioritize consistency, accessibility, and scalability in design system implementation.
