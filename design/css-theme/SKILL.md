---
name: css-theme
description: >-
  Build theming systems with modern CSS. Covers custom properties architecture
  (primitive, semantic, component tokens), oklch/oklab color spaces, color-mix()
  for tints and shades, light-dark() for automatic dark mode, @property for
  typed custom properties, multiple theme support, contrast themes, and
  forced-colors mode. Use when building a theme, adding dark mode, creating
  color systems, setting up design tokens, or implementing color schemes.
disable-model-invocation: true
license: MIT
---

# css-theme — Modern CSS Theming Systems

You are a CSS theming specialist. Your job is to design and implement complete theming systems using modern CSS — no JavaScript theme toggling, no CSS-in-JS, no preprocessor variables. Pure CSS custom properties, `color-mix()`, `light-dark()`, and `@property`.

For the full pattern catalog, see the css-expert skill's [modern-patterns.md](../css-expert/references/modern-patterns.md). For browser support details on `light-dark()`, `@property`, and color functions, see [browser-compat.md](../css-expert/references/browser-compat.md).

## Workflow

```
Theme Build Progress:
- [ ] Step 1: Define primitive color tokens (oklch palette)
- [ ] Step 2: Create semantic token layer
- [ ] Step 3: Wire up light/dark mode
- [ ] Step 4: Add component-level tokens
- [ ] Step 5: Register animated properties with @property
- [ ] Step 6: Add contrast and forced-colors support
- [ ] Step 7: (Optional) Add extra themes beyond light/dark
```

## Step 1: Primitive Color Tokens

Build the raw color palette using `oklch()`. Every color starts here.

```css
:root {
  /* Primary */
  --primary-50: oklch(95% 0.05 250);
  --primary-100: oklch(90% 0.08 250);
  --primary-200: oklch(80% 0.12 250);
  --primary-300: oklch(70% 0.18 250);
  --primary-400: oklch(60% 0.22 250);
  --primary-500: oklch(55% 0.25 250);
  --primary-600: oklch(48% 0.22 250);
  --primary-700: oklch(40% 0.18 250);
  --primary-800: oklch(32% 0.14 250);
  --primary-900: oklch(25% 0.10 250);

  /* Neutral */
  --neutral-0: oklch(100% 0 0);
  --neutral-50: oklch(97% 0.005 250);
  --neutral-100: oklch(93% 0.005 250);
  --neutral-200: oklch(87% 0.01 250);
  --neutral-300: oklch(78% 0.01 250);
  --neutral-400: oklch(65% 0.01 250);
  --neutral-500: oklch(55% 0.01 250);
  --neutral-600: oklch(44% 0.01 250);
  --neutral-700: oklch(35% 0.01 250);
  --neutral-800: oklch(25% 0.01 250);
  --neutral-900: oklch(18% 0.01 250);
  --neutral-1000: oklch(10% 0.005 0);
}
```

### Why oklch?

- **Perceptually uniform**: equal lightness steps look visually equal (unlike HSL)
- **Wide gamut**: access colors outside sRGB on capable displays
- **Predictable**: adjusting L changes brightness without hue shift

### Generating Tints and Shades with color-mix()

Instead of hardcoding every shade, derive them:

```css
:root {
  --primary: oklch(55% 0.25 250);
  --primary-light: color-mix(in oklch, var(--primary), white 40%);
  --primary-dark: color-mix(in oklch, var(--primary), black 30%);
  --primary-muted: color-mix(in oklch, var(--primary), transparent 60%);
  --primary-subtle: color-mix(in oklch, var(--primary), var(--color-surface) 85%);
}
```

Use `color-mix()` for hover/active states, overlays, and surface tints rather than separate hardcoded values.

## Step 2: Semantic Token Layer

Map primitives to purpose-driven names. These are the tokens components actually consume.

```css
:root {
  color-scheme: light dark;

  /* Surfaces */
  --color-surface: light-dark(var(--neutral-0), var(--neutral-900));
  --color-surface-raised: light-dark(var(--neutral-0), var(--neutral-800));
  --color-surface-sunken: light-dark(var(--neutral-50), var(--neutral-1000));
  --color-surface-overlay: light-dark(
    oklch(100% 0 0 / 0.8),
    oklch(15% 0 0 / 0.8)
  );

  /* Text */
  --color-text: light-dark(var(--neutral-900), var(--neutral-100));
  --color-text-muted: light-dark(var(--neutral-600), var(--neutral-400));
  --color-text-subtle: light-dark(var(--neutral-500), var(--neutral-500));

  /* Borders */
  --color-border: light-dark(var(--neutral-200), var(--neutral-700));
  --color-border-strong: light-dark(var(--neutral-400), var(--neutral-500));

  /* Interactive */
  --color-primary: light-dark(var(--primary-500), var(--primary-400));
  --color-primary-hover: light-dark(var(--primary-600), var(--primary-300));
  --color-primary-text: light-dark(var(--neutral-0), var(--neutral-900));

  /* Status */
  --color-success: light-dark(oklch(50% 0.18 150), oklch(70% 0.18 150));
  --color-warning: light-dark(oklch(55% 0.18 85), oklch(75% 0.18 85));
  --color-error: light-dark(oklch(50% 0.22 25), oklch(70% 0.20 25));
  --color-info: light-dark(oklch(50% 0.15 250), oklch(70% 0.15 250));
}
```

### Naming Rules

- Primitives: `--{color}-{shade}` (e.g., `--primary-500`)
- Semantics: `--color-{purpose}` (e.g., `--color-surface`, `--color-text`)
- Component: `--_{property}` with underscore prefix (e.g., `--_bg`, `--_border`)

## Step 3: Light/Dark Mode

### Automatic with light-dark()

The `light-dark()` function reads `color-scheme` and picks the correct value automatically. The `color-scheme` declaration on `:root` is required:

```css
:root {
  color-scheme: light dark;
}
```

This single declaration enables the browser's native light/dark toggle. The user's OS preference drives it via `prefers-color-scheme`.

### Manual Override

Allow users to force a theme with a data attribute:

```css
:root, [data-theme="light"] {
  color-scheme: light;
}

[data-theme="dark"] {
  color-scheme: dark;
}
```

The `light-dark()` values in semantic tokens automatically respond to the `color-scheme` change — no need to redeclare every variable.

### Theme Toggle (minimal JS)

```js
document.documentElement.dataset.theme =
  document.documentElement.dataset.theme === "dark" ? "light" : "dark";
```

Store preference in `localStorage`. On load, set the attribute before first paint to avoid flash.

## Step 4: Component-Level Tokens

Components should use internal custom properties (underscore prefix) mapped to semantic tokens:

```css
.button {
  --_bg: var(--color-primary);
  --_color: var(--color-primary-text);
  --_border: transparent;
  --_radius: var(--radius-m);

  background: var(--_bg);
  color: var(--_color);
  border: 1px solid var(--_border);
  border-radius: var(--_radius);

  &:hover {
    --_bg: var(--color-primary-hover);
  }

  &[data-variant="outline"] {
    --_bg: transparent;
    --_color: var(--color-primary);
    --_border: var(--color-primary);
  }

  &[data-variant="ghost"] {
    --_bg: transparent;
    --_color: var(--color-primary);
  }
}
```

This pattern lets variants, states, and themes override internal tokens without touching property declarations.

## Step 5: @property for Typed and Animated Custom Properties

Register custom properties to enable transitions and type checking:

```css
@property --gradient-angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

@property --color-primary-l {
  syntax: "<percentage>";
  inherits: true;
  initial-value: 55%;
}
```

### Use Cases for @property

- **Animate gradients**: transition `--gradient-angle` to spin a gradient
- **Animate colors**: transition individual oklch channels
- **Type safety**: constrain values to `<length>`, `<color>`, `<number>`, etc.
- **Fallback enforcement**: `initial-value` acts as a guaranteed fallback

### Animated Gradient Example

```css
@property --angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.gradient-border {
  background: conic-gradient(from var(--angle), var(--primary-400), var(--primary-600), var(--primary-400));
  transition: --angle 500ms ease;

  &:hover {
    --angle: 180deg;
  }
}
```

## Step 6: Contrast and Forced-Colors Support

### prefers-contrast: more

Increase visual distinction for users who request it:

```css
@media (prefers-contrast: more) {
  :root {
    --color-text: light-dark(oklch(5% 0 0), oklch(98% 0 0));
    --color-border: light-dark(oklch(30% 0 0), oklch(80% 0 0));
    --color-text-muted: light-dark(oklch(30% 0 0), oklch(80% 0 0));
  }
}
```

### forced-colors: active

Support Windows High Contrast mode. System colors replace your custom colors:

```css
@media (forced-colors: active) {
  .button {
    border: 1px solid ButtonText;
  }

  .card {
    border: 1px solid CanvasText;
  }

  .badge {
    outline: 1px solid;
  }
}
```

Key system color keywords: `Canvas`, `CanvasText`, `LinkText`, `ButtonFace`, `ButtonText`, `Highlight`, `HighlightText`, `GrayText`.

Rules in forced-colors mode:
- Custom colors are overridden — don't fight it
- Borders and outlines become the primary visual indicators
- Ensure interactive elements remain distinguishable
- `background-image` is removed — don't rely on it for meaning

## Step 7: Multiple Themes (Beyond Light/Dark)

For brand themes, seasonal themes, or user-customizable themes, use data attributes with full token overrides:

```css
[data-theme="ocean"] {
  color-scheme: dark;
  --primary-500: oklch(60% 0.20 230);
  --color-surface: oklch(18% 0.02 230);
  --color-text: oklch(90% 0.01 230);
}

[data-theme="forest"] {
  color-scheme: dark;
  --primary-500: oklch(55% 0.18 150);
  --color-surface: oklch(15% 0.02 150);
  --color-text: oklch(90% 0.01 150);
}
```

Override only the primitives — semantic tokens that reference primitives via `var()` update automatically.

### User-Customizable Themes

Expose a small set of properties for user control:

```css
:root {
  --user-hue: 250;
  --primary-500: oklch(55% 0.25 var(--user-hue));
}
```

Set `--user-hue` from JavaScript based on user preference.

## Output Format

When building a theme system, deliver:

1. **Token file** — all primitive and semantic tokens in one file (e.g., `tokens.css`)
2. **Theme variants** — separate `@layer` blocks or data-attribute overrides
3. **Component examples** — show 2-3 components using the token system
4. **Accessibility layer** — `prefers-contrast` and `forced-colors` overrides

## Rules

- Always declare `color-scheme: light dark` on `:root` when using `light-dark()`
- Never hardcode colors in components — always reference tokens
- Use `oklch()` for all color definitions, never hex/rgb/hsl
- Use `color-mix(in oklch, ...)` for derived colors, not manually computed values
- Test that contrast ratios meet WCAG: 4.5:1 for normal text, 3:1 for large
- Component tokens use underscore prefix (`--_bg`) to signal internal scope
- Semantic tokens use `--color-` prefix for discoverability
