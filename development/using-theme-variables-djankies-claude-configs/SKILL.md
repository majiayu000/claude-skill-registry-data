---
name: using-theme-variables
description: Define and use theme variables with @theme directive, oklch() color format, semantic naming, and namespaced utilities. Use when customizing design tokens or creating design systems.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Using Theme Variables

## Purpose

Define custom design tokens using the `@theme` directive with CSS variables. Tailwind v4 uses modern color formats (oklch) and namespace-based utility generation.

## Basic Theme Variables

```css
@import 'tailwindcss';

@theme {
  --font-display: 'Satoshi', 'sans-serif';
  --font-body: 'Inter', 'sans-serif';

  --color-brand-primary: oklch(0.65 0.25 270);
  --color-brand-accent: oklch(0.75 0.22 320);

  --breakpoint-3xl: 120rem;
  --breakpoint-4xl: 160rem;

  --spacing-18: 4.5rem;
  --spacing-72: 18rem;

  --radius-4xl: 2rem;

  --shadow-brutal: 8px 8px 0 0 rgb(0 0 0);
}
```

## Color Format: oklch()

Tailwind v4 uses OkLCh color space instead of RGB for wider gamut and more vivid colors on modern displays.

**oklch() syntax:**

```
oklch(Lightness Chroma Hue)
```

- **Lightness:** 0 (black) to 1 (white)
- **Chroma:** 0 (gray) to ~0.4 (vivid)
- **Hue:** 0-360 degrees

**Examples:**

```css
@theme {
  --color-blue: oklch(0.65 0.25 270);
  --color-green: oklch(0.72 0.15 142);
  --color-red: oklch(0.65 0.22 25);
  --color-purple: oklch(0.75 0.22 320);
  --color-orange: oklch(0.78 0.18 60);
}
```

## Theme Variable Namespaces

Tailwind generates utilities based on variable name prefixes:

| Namespace         | Utilities Generated                        |
| ----------------- | ------------------------------------------ |
| `--color-*`       | bg-, text-, fill-, stroke-, border-, ring- |
| `--font-*`        | font-family utilities                      |
| `--text-*`        | font-size utilities                        |
| `--font-weight-*` | font-weight utilities                      |
| `--tracking-*`    | letter-spacing utilities                   |
| `--leading-*`     | line-height utilities                      |
| `--breakpoint-*`  | responsive breakpoint variants             |
| `--spacing-*`     | padding, margin, sizing utilities          |
| `--radius-*`      | border-radius utilities                    |
| `--shadow-*`      | box-shadow utilities                       |
| `--animate-*`     | animation utilities                        |

**Example usage:**

```css
@theme {
  --color-brand: oklch(0.65 0.25 270);
  --spacing-18: 4.5rem;
  --radius-4xl: 2rem;
}
```

Generates utilities:

```html
<div class="bg-brand text-brand border-brand"></div>
<div class="p-18 m-18 w-18"></div>
<div class="rounded-4xl"></div>
```

## Semantic Naming

Use meaningful names instead of generic scales:

```css
@theme {
  --color-primary: oklch(0.65 0.25 270);
  --color-secondary: oklch(0.75 0.22 320);
  --color-success: oklch(0.72 0.15 142);
  --color-warning: oklch(0.78 0.18 60);
  --color-error: oklch(0.65 0.22 25);

  --color-text: oklch(0.21 0 0);
  --color-text-muted: oklch(0.51 0 0);
  --color-background: oklch(0.99 0 0);
}
```

**Usage:**

```html
<button class="bg-primary text-white hover:opacity-90">Primary Button</button>
<div class="text-error">Error message</div>
<p class="text-text-muted">Muted text</p>
```

## Extending Default Theme

Add new values without removing defaults:

```css
@theme {
  --color-lagoon: oklch(0.72 0.11 221.19);
  --color-coral: oklch(0.74 0.17 40.24);
  --font-script: 'Great Vibes', cursive;
  --breakpoint-3xl: 120rem;
}
```

All default Tailwind utilities remain available (blue-500, gray-200, etc.).

## Replacing Default Theme

Remove all defaults and define only custom variables:

```css
@theme {
  --*: initial;

  --spacing: 4px;
  --font-body: 'Inter', sans-serif;
  --color-lagoon: oklch(0.72 0.11 221.19);
  --color-coral: oklch(0.74 0.17 40.24);
}
```

Only utilities based on custom variables will be generated.

## Inline Theme Variables

Reference other variables using the inline option:

```css
@theme inline {
  --font-sans: var(--font-inter);
  --color-primary: var(--color-red-500);
  --spacing-gutter: var(--spacing-4);
}
```

Variables defined in `@theme inline` can reference variables from main `@theme`.

## Static Theme Variables

Generate all CSS variables even if unused:

```css
@theme static {
  --color-primary: var(--color-red-500);
  --color-secondary: var(--color-blue-500);
}
```

Useful for runtime JavaScript access:

```javascript
const styles = getComputedStyle(document.documentElement);
const primaryColor = styles.getPropertyValue('--color-primary');
```

## Accessing Variables in JavaScript

```javascript
const styles = getComputedStyle(document.documentElement);
const shadow = styles.getPropertyValue('--shadow-xl');
const color = styles.getPropertyValue('--color-blue-500');
```

**Setting variables dynamically:**

```javascript
document.documentElement.style.setProperty('--color-primary', 'oklch(0.70 0.20 180)');
```

**In animation libraries:**

```jsx
<motion.div animate={{ backgroundColor: 'var(--color-blue-500)' }} />
```

## Sharing Themes Across Projects

**Create shared theme file:**

**packages/brand/theme.css:**

```css
@theme {
  --*: initial;

  --spacing: 4px;
  --font-body: 'Inter', sans-serif;
  --color-lagoon: oklch(0.72 0.11 221.19);
  --color-coral: oklch(0.74 0.17 40.24);
}
```

**Import in projects:**

```css
@import 'tailwindcss';
@import '@my-company/brand/theme.css';
```

## Complex Theme Example

```css
@import 'tailwindcss';

@theme {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;

  --color-white: #ffffff;
  --color-black: #000000;

  --color-gray-50: oklch(0.99 0 0);
  --color-gray-100: oklch(0.97 0 0);
  --color-gray-900: oklch(0.21 0 0);

  --color-primary: oklch(0.65 0.25 270);
  --color-secondary: oklch(0.75 0.22 320);
  --color-success: oklch(0.72 0.15 142);

  --spacing: 0.25rem;
  --spacing-px: 1px;
  --spacing-1: calc(var(--spacing) * 1);
  --spacing-4: calc(var(--spacing) * 4);

  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;

  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);

  --breakpoint-sm: 40rem;
  --breakpoint-md: 48rem;
  --breakpoint-lg: 64rem;
}
```

## Best Practices

1. **Use semantic names** instead of scales (primary vs blue-500)
2. **Use oklch()** for color definitions
3. **Define variables at :root** for performance
4. **Group related variables** (colors, spacing, typography)
5. **Reference other variables** with inline theme
6. **Share themes** across projects using imports

## See Also

- references/color-conversion.md - Hex to oklch conversion table
- references/namespace-reference.md - Complete namespace documentation
