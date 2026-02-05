---
name: ui-theme
description: |
  Design token system using Style Dictionary with Tailwind CSS v4 integration.
  Centralizes design tokens in JSON format, outputs CSS variables mapped to @theme block.
  Reference for implementing consistent theming across UI components.
---

# UI Theme Skill

## Architecture Overview

```
design-tokens/                   # Design token source of truth
├── src/
│   ├── build.ts                 # Style Dictionary build script (TypeScript)
│   └── tokens/                  # Token definitions (JSON)
│       ├── colors/
│       │   ├── base.json        # Color palette (gray, blue, cyan, etc.)
│       │   └── semantic.json    # Semantic color aliases
│       ├── spacing/index.json
│       ├── typography/index.json
│       ├── radius/index.json
│       ├── shadow/index.json
│       └── animation/index.json
└── dist/
    ├── tokens.css               # Plain CSS variables (:root)
    └── tailwind-theme.css       # Tailwind CSS v4 @theme block
```

## Design Token Workflow

### 1. Define Tokens in JSON

Tokens are defined using Style Dictionary format:

```json
// colors/base.json - Raw color values
{
  "color": {
    "base": {
      "gray": {
        "50": { "value": "#f8fafc" },
        "500": { "value": "#64748b" },
        "900": { "value": "#0f172a" }
      },
      "cyan": {
        "500": { "value": "#06b6d4" },
        "600": { "value": "#0891b2" }
      }
    }
  }
}

// colors/semantic.json - Semantic aliases
{
  "color": {
    "semantic": {
      "background": { "value": "{color.base.gray.50}" },
      "foreground": { "value": "{color.base.gray.900}" },
      "primary": { "value": "{color.base.cyan.600}" },
      "primary-hover": { "value": "{color.base.cyan.700}" }
    }
  }
}
```

### 2. Build Tokens

Run the Style Dictionary build script to generate CSS output:

```bash
pnpm build  # Runs: tsx src/build.ts
```

Output generates:
- `dist/tokens.css` - Plain `:root { --color-primary: #0891b2; }`
- `dist/tailwind-theme.css` - Tailwind v4 `@theme { --color-primary: #0891b2; }`

### 3. Import in Application

```css
/* Import generated theme */
@import "design-tokens/tailwind-theme.css";

/* Global base styles (html, body, scrollbar, etc.) */
```

### 4. Use in Components

```tsx
// Tailwind utility classes work with tokens
<div className="bg-background text-foreground border-border" />

// Or CSS variables directly
<div style={{ backgroundColor: 'var(--color-primary)' }} />
```

## Style Dictionary Configuration

### Custom Format for Tailwind CSS v4

The build script registers a custom format that outputs `@theme` blocks:

```typescript
import StyleDictionary from "style-dictionary"
import type { FormatFn } from "style-dictionary/types"

const tailwindThemeFormat: FormatFn = ({ dictionary }) => {
  // Groups tokens by category (color, spacing, font, etc.)
  // Outputs @theme block with simplified names:
  //   color-semantic-primary → --color-primary
  //   color-base-gray-500 → --color-gray-500
  return `@import "tailwindcss";

@theme {
  --color-primary: #0891b2;
  --spacing-4: 1rem;
  ...
}`;
};

StyleDictionary.registerFormat({
  name: "css/tailwind-theme",
  format: tailwindThemeFormat,
});
```

### Adding New Tokens

1. Add token to appropriate JSON file in `src/tokens/`
2. Run build command
3. Token is automatically available as CSS variable and Tailwind utility

## Design Methodology

### 1. Define Design Direction

Before implementing, establish a clear aesthetic direction:

- **Purpose**: What problem does this UI solve? Who uses it?
- **Tone**: Professional/Industrial, Playful, Minimal, Editorial, etc.
- **Color Philosophy**: Choose a hue family (e.g., cool slate ~260, warm gray ~45)
- **Differentiation**: What makes this design memorable?

### 2. Color System

Define colors in base tokens then create semantic aliases:

```json
// Base colors - Raw palette values
{
  "color": {
    "base": {
      "gray": {
        "50": { "value": "#f8fafc" },
        "100": { "value": "#f1f5f9" },
        "200": { "value": "#e2e8f0" },
        "500": { "value": "#64748b" },
        "600": { "value": "#475569" },
        "900": { "value": "#0f172a" }
      },
      "cyan": {
        "500": { "value": "#06b6d4" },
        "600": { "value": "#0891b2" },
        "700": { "value": "#0e7490" }
      }
    }
  }
}

// Semantic colors - UI-specific aliases
{
  "color": {
    "semantic": {
      "background": { "value": "{color.base.gray.50}" },
      "foreground": { "value": "{color.base.gray.900}" },
      "muted": { "value": "{color.base.gray.100}" },
      "muted-foreground": { "value": "{color.base.gray.500}" },
      "primary": { "value": "{color.base.cyan.600}" },
      "primary-foreground": { "value": "{color.base.white}" },
      "primary-hover": { "value": "{color.base.cyan.700}" },
      "border": { "value": "{color.base.gray.200}" },
      "ring": { "value": "{color.base.cyan.600}" },
      "ring-offset": { "value": "{color.base.white}" }
    }
  }
}
```

### 3. Token Categories

| Category | File | Variables |
|----------|------|-----------|
| Colors | `colors/base.json`, `colors/semantic.json` | `--color-*` |
| Spacing | `spacing/index.json` | `--spacing-*` |
| Typography | `typography/index.json` | `--font-*` |
| Border Radius | `radius/index.json` | `--radius-*` |
| Shadows | `shadow/index.json` | `--shadow-*` |
| Animation | `animation/index.json` | `--duration-*`, `--easing-*` |

## Typography

```css
@theme {
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

## Animation Tokens

```css
@theme {
  --duration-instant: 50ms;
  --duration-fast: 100ms;
  --duration-normal: 150ms;
  --duration-slow: 250ms;

  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
  --easing-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

## Modern Color Features

### OKLCH Color Space (Recommended)

Perceptually uniform color space for predictable color manipulation:

```css
@theme {
  /* OKLCH: lightness (0-100%), chroma (0-0.4), hue (0-360) */
  --color-primary: oklch(55% 0.2 240);        /* Vibrant blue */
  --color-primary-light: oklch(75% 0.15 240);
  --color-primary-dark: oklch(35% 0.2 240);

  /* Consistent gray scale */
  --color-gray-50: oklch(97% 0.005 240);
  --color-gray-100: oklch(93% 0.005 240);
  --color-gray-500: oklch(55% 0.005 240);
  --color-gray-900: oklch(15% 0.005 240);
}
```

**Benefits:**
- Consistent perceived brightness across hues
- Predictable lightness modifications
- Better for accessibility contrast calculations
- Wider gamut support (P3 displays)

### color-mix() Function

Generate color variations dynamically:

```css
.button {
  --base: var(--color-primary);

  background: var(--base);

  &:hover {
    /* Mix with white for lighter */
    background: color-mix(in oklch, var(--base), white 20%);
  }

  &:active {
    /* Mix with black for darker */
    background: color-mix(in oklch, var(--base), black 20%);
  }
}

/* Semi-transparent variations */
.overlay {
  background: color-mix(in oklch, var(--color-primary) 50%, transparent);
}
```

### @property for Animated Variables

Enable CSS variable animations:

```css
@property --gradient-angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

@property --glow-opacity {
  syntax: "<number>";
  initial-value: 0;
  inherits: false;
}

.animated-border {
  background: conic-gradient(
    from var(--gradient-angle),
    var(--color-primary),
    var(--color-secondary),
    var(--color-primary)
  );
  animation: spin 3s linear infinite;
}

@keyframes spin {
  to { --gradient-angle: 360deg; }
}
```

### light-dark() for Theme Switching

Single-declaration dark mode:

```css
:root {
  color-scheme: light dark;
}

.card {
  background: light-dark(var(--color-gray-50), var(--color-gray-900));
  color: light-dark(var(--color-gray-900), var(--color-gray-50));
  border-color: light-dark(var(--color-gray-200), var(--color-gray-700));
}
```

## Dark Mode Strategy

### CSS-Only Approach

```css
/* Semantic tokens with light-dark() */
:root {
  color-scheme: light dark;

  --background: light-dark(oklch(98% 0 0), oklch(12% 0 0));
  --foreground: light-dark(oklch(12% 0 0), oklch(98% 0 0));
  --muted: light-dark(oklch(95% 0 0), oklch(20% 0 0));
  --border: light-dark(oklch(90% 0 0), oklch(25% 0 0));
}
```

### Token-Based Approach (Style Dictionary)

```json
// tokens/colors/semantic-light.json
{
  "color": {
    "semantic": {
      "background": { "value": "{color.base.gray.50}" },
      "foreground": { "value": "{color.base.gray.900}" }
    }
  }
}

// tokens/colors/semantic-dark.json
{
  "color": {
    "semantic": {
      "background": { "value": "{color.base.gray.900}" },
      "foreground": { "value": "{color.base.gray.50}" }
    }
  }
}
```

## A11y Checklist

- [ ] Contrast ratios: 4.5:1 text, 3:1 UI components
- [ ] Focus visible: 2px+ ring on all interactive elements
- [ ] Touch targets: min 24x24 CSS pixels
- [ ] Reduced motion: respect `prefers-reduced-motion`

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## References

- [Style Dictionary Documentation](https://amzn.github.io/style-dictionary/)
- [Tailwind CSS v4 Theme](https://tailwindcss.com/docs/theme)
- [Design Tokens W3C](https://www.w3.org/community/design-tokens/)
