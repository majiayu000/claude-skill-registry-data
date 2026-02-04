---
name: vanilla-extract
description: Implements zero-runtime CSS using vanilla-extract with type-safe styles, themes, recipes, and sprinkles. Use when wanting type-safe CSS, static extraction at build time, or building design system utilities.
---

# vanilla-extract

Zero-runtime CSS-in-TypeScript with static extraction at build time.

## Quick Start

**Install:**
```bash
npm install @vanilla-extract/css
# Framework integrations
npm install @vanilla-extract/vite-plugin    # Vite
npm install @vanilla-extract/next-plugin    # Next.js
```

**Configure (Vite):**
```typescript
// vite.config.ts
import { vanillaExtractPlugin } from '@vanilla-extract/vite-plugin';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [vanillaExtractPlugin()],
});
```

**Create styles:**
```typescript
// button.css.ts
import { style } from '@vanilla-extract/css';

export const button = style({
  padding: '12px 24px',
  border: 'none',
  borderRadius: 8,
  fontSize: 16,
  cursor: 'pointer',
  backgroundColor: '#3b82f6',
  color: 'white',
  ':hover': {
    backgroundColor: '#2563eb',
  },
});
```

**Use in component:**
```tsx
// Button.tsx
import { button } from './button.css';

export function Button({ children }: { children: React.ReactNode }) {
  return <button className={button}>{children}</button>;
}
```

## Style API

### Basic Styles

```typescript
import { style } from '@vanilla-extract/css';

export const container = style({
  maxWidth: 1200,
  margin: '0 auto',
  padding: 16,
});

// Numbers become pixels (except unitless properties)
export const box = style({
  padding: 16,        // 16px
  margin: 8,          // 8px
  opacity: 0.5,       // unitless
  flexGrow: 1,        // unitless
  lineHeight: 1.5,    // unitless
});
```

### Pseudo-Selectors

```typescript
export const link = style({
  color: '#3b82f6',
  textDecoration: 'none',

  ':hover': {
    textDecoration: 'underline',
  },

  ':focus-visible': {
    outline: '2px solid #3b82f6',
    outlineOffset: 2,
  },

  '::before': {
    content: '">"',
    marginRight: 4,
  },
});
```

### Complex Selectors

```typescript
export const card = style({
  padding: 16,

  selectors: {
    // Target self with conditions
    '&:first-child': {
      marginTop: 0,
    },

    // Adjacent sibling
    '& + &': {
      marginTop: 16,
    },

    // Parent hover (& must appear in selector)
    '.dark-mode &': {
      backgroundColor: '#1f2937',
    },

    // Direct child - use globalStyle instead
    // '& > div': { } // Invalid!
  },
});
```

### Media Queries

```typescript
export const responsiveBox = style({
  padding: 16,

  '@media': {
    '(min-width: 768px)': {
      padding: 24,
    },
    '(min-width: 1024px)': {
      padding: 32,
    },
    '(prefers-color-scheme: dark)': {
      backgroundColor: '#1f2937',
    },
  },
});
```

### Container Queries

```typescript
export const containerParent = style({
  containerType: 'inline-size',
});

export const responsiveChild = style({
  padding: 16,

  '@container': {
    '(min-width: 400px)': {
      padding: 24,
    },
  },
});
```

## CSS Variables

### createVar

```typescript
import { style, createVar } from '@vanilla-extract/css';

const accentColor = createVar();
const spacing = createVar();

export const container = style({
  vars: {
    [accentColor]: '#3b82f6',
    [spacing]: '16px',
  },
  padding: spacing,
  borderColor: accentColor,
});

export const altContainer = style({
  vars: {
    [accentColor]: '#10b981', // Override
  },
});
```

### Fallback Values

```typescript
import { fallbackVar } from '@vanilla-extract/css';

export const box = style({
  color: fallbackVar(accentColor, 'blue'),
});
```

## Style Variants

```typescript
import { styleVariants } from '@vanilla-extract/css';

// Simple variants
export const color = styleVariants({
  primary: { backgroundColor: '#3b82f6', color: 'white' },
  secondary: { backgroundColor: '#e5e7eb', color: '#1f2937' },
  danger: { backgroundColor: '#ef4444', color: 'white' },
});

// With composition
const base = style({
  padding: '12px 24px',
  borderRadius: 8,
  border: 'none',
});

export const button = styleVariants({
  primary: [base, { backgroundColor: '#3b82f6', color: 'white' }],
  secondary: [base, { backgroundColor: '#e5e7eb', color: '#1f2937' }],
});

// Usage
<button className={button.primary}>Primary</button>
<button className={color['secondary']}>Secondary</button>
```

## Global Styles

```typescript
import { globalStyle, style } from '@vanilla-extract/css';

// Global reset
globalStyle('*, *::before, *::after', {
  boxSizing: 'border-box',
});

globalStyle('body', {
  margin: 0,
  fontFamily: 'system-ui, sans-serif',
});

// Reference scoped classes
const card = style({ padding: 16 });

globalStyle(`${card} > h2`, {
  margin: 0,
  fontSize: 24,
});

globalStyle(`${card} p`, {
  color: '#6b7280',
});
```

## Theming

### Create Theme

```typescript
// theme.css.ts
import { createTheme } from '@vanilla-extract/css';

export const [themeClass, vars] = createTheme({
  colors: {
    primary: '#3b82f6',
    secondary: '#6b7280',
    background: '#ffffff',
    text: '#1f2937',
  },
  spacing: {
    sm: '8px',
    md: '16px',
    lg: '24px',
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '16px',
  },
});
```

### Use Theme Variables

```typescript
// button.css.ts
import { style } from '@vanilla-extract/css';
import { vars } from './theme.css';

export const button = style({
  padding: vars.spacing.md,
  borderRadius: vars.borderRadius.md,
  backgroundColor: vars.colors.primary,
  color: '#fff',
});
```

### Multiple Themes

```typescript
import { createTheme, createThemeContract } from '@vanilla-extract/css';

// Define contract (structure only)
const themeContract = createThemeContract({
  colors: {
    background: null,
    text: null,
    primary: null,
  },
});

// Light theme
export const lightTheme = createTheme(themeContract, {
  colors: {
    background: '#ffffff',
    text: '#1f2937',
    primary: '#3b82f6',
  },
});

// Dark theme
export const darkTheme = createTheme(themeContract, {
  colors: {
    background: '#1f2937',
    text: '#f9fafb',
    primary: '#60a5fa',
  },
});

export { themeContract as vars };
```

**Apply theme:**
```tsx
function App() {
  const [isDark, setIsDark] = useState(false);

  return (
    <div className={isDark ? darkTheme : lightTheme}>
      <button onClick={() => setIsDark(!isDark)}>Toggle</button>
    </div>
  );
}
```

## Recipes

Multi-variant component styles.

**Install:**
```bash
npm install @vanilla-extract/recipes
```

```typescript
// button.css.ts
import { recipe, RecipeVariants } from '@vanilla-extract/recipes';

export const button = recipe({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer',
    fontWeight: 600,
  },

  variants: {
    color: {
      primary: {
        backgroundColor: '#3b82f6',
        color: 'white',
      },
      secondary: {
        backgroundColor: '#e5e7eb',
        color: '#1f2937',
      },
      danger: {
        backgroundColor: '#ef4444',
        color: 'white',
      },
    },
    size: {
      sm: { padding: '8px 16px', fontSize: 14 },
      md: { padding: '12px 24px', fontSize: 16 },
      lg: { padding: '16px 32px', fontSize: 18 },
    },
  },

  compoundVariants: [
    {
      variants: { color: 'primary', size: 'lg' },
      style: {
        boxShadow: '0 4px 12px rgba(59, 130, 246, 0.4)',
      },
    },
  ],

  defaultVariants: {
    color: 'primary',
    size: 'md',
  },
});

// Type extraction
export type ButtonVariants = RecipeVariants<typeof button>;
```

**Usage:**
```tsx
import { button, ButtonVariants } from './button.css';

interface ButtonProps extends ButtonVariants {
  children: React.ReactNode;
}

export function Button({ color, size, children }: ButtonProps) {
  return (
    <button className={button({ color, size })}>
      {children}
    </button>
  );
}

// Usage
<Button color="primary" size="lg">Click me</Button>
<Button color="danger">Delete</Button>
```

## Sprinkles

Build atomic CSS utilities.

**Install:**
```bash
npm install @vanilla-extract/sprinkles
```

```typescript
// sprinkles.css.ts
import { defineProperties, createSprinkles } from '@vanilla-extract/sprinkles';

const space = {
  none: '0',
  sm: '4px',
  md: '8px',
  lg: '16px',
  xl: '24px',
};

const colors = {
  primary: '#3b82f6',
  secondary: '#6b7280',
  white: '#ffffff',
  black: '#000000',
};

const responsiveProperties = defineProperties({
  conditions: {
    mobile: {},
    tablet: { '@media': '(min-width: 768px)' },
    desktop: { '@media': '(min-width: 1024px)' },
  },
  defaultCondition: 'mobile',
  properties: {
    display: ['none', 'flex', 'block', 'grid'],
    flexDirection: ['row', 'column'],
    alignItems: ['stretch', 'center', 'flex-start', 'flex-end'],
    justifyContent: ['stretch', 'center', 'flex-start', 'flex-end', 'space-between'],
    gap: space,
    padding: space,
    paddingTop: space,
    paddingBottom: space,
    paddingLeft: space,
    paddingRight: space,
    margin: space,
  },
  shorthands: {
    p: ['padding'],
    px: ['paddingLeft', 'paddingRight'],
    py: ['paddingTop', 'paddingBottom'],
    m: ['margin'],
  },
});

const colorProperties = defineProperties({
  properties: {
    color: colors,
    backgroundColor: colors,
  },
});

export const sprinkles = createSprinkles(
  responsiveProperties,
  colorProperties
);

export type Sprinkles = Parameters<typeof sprinkles>[0];
```

**Usage:**
```tsx
import { sprinkles } from './sprinkles.css';

function Box() {
  return (
    <div className={sprinkles({
      display: 'flex',
      gap: 'lg',
      p: { mobile: 'md', desktop: 'xl' },
      backgroundColor: 'white',
    })}>
      Content
    </div>
  );
}
```

## Framework Setup

### Next.js

```javascript
// next.config.js
const { createVanillaExtractPlugin } = require('@vanilla-extract/next-plugin');
const withVanillaExtract = createVanillaExtractPlugin();

module.exports = withVanillaExtract({
  // Next.js config
});
```

### Vite

```typescript
// vite.config.ts
import { vanillaExtractPlugin } from '@vanilla-extract/vite-plugin';

export default defineConfig({
  plugins: [vanillaExtractPlugin()],
});
```

## Best Practices

1. **Use `.css.ts` extension** - Required for processing
2. **Colocate styles** - Keep near components
3. **Export vars** - Share theme variables
4. **Use recipes for variants** - Type-safe component APIs
5. **Sprinkles for utilities** - Build design system primitives

## Reference Files

- [references/recipes.md](references/recipes.md) - Recipe patterns
- [references/sprinkles.md](references/sprinkles.md) - Atomic CSS utilities
