---
name: open-props
description: Use Open Props CSS custom properties for consistent design tokens. Use when setting up design systems, choosing spacing/color values, or wanting battle-tested CSS variables without heavy dependencies.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Open Props Skill

Use Open Props for battle-tested CSS custom properties without build-time dependencies.

## Philosophy

Open Props aligns with minimalist, dependency-light principles:

| Principle | Open Props Approach |
|-----------|---------------------|
| No build step | Just CSS custom properties |
| Pick what you need | Import only used modules |
| Copy-paste friendly | Use as reference, copy values |
| Progressive | Works in all modern browsers |

## Installation Options

### Option 1: NPM (Full Control)

```bash
npm install open-props
```

```css
/* Import specific modules */
@import 'open-props/colors.min.css';
@import 'open-props/sizes.min.css';
@import 'open-props/shadows.min.css';
```

### Option 2: CDN (Quick Start)

```html
<link rel="stylesheet" href="https://unpkg.com/open-props"/>
```

### Option 3: Copy Values (Zero Dependencies)

Copy specific values you need into your own tokens file:

```css
/* tokens.css - Copied from Open Props */
:root {
  /* Spacing - from sizes */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;

  /* Colors - from colors */
  --blue-5: oklch(51.1% 0.262 276.97);
  --gray-2: oklch(92% 0 0);
  --gray-8: oklch(27.8% 0 0);
}
```

## Core Modules

### Sizes (Spacing & Typography)

```css
@import 'open-props/sizes.min.css';
```

```css
/* Usage */
.container {
  padding: var(--size-3);      /* 1rem */
  gap: var(--size-2);          /* 0.5rem */
  max-width: var(--size-content-3); /* 60ch */
}

/* Size scale: 1-15 */
/* --size-1: 0.25rem (4px) */
/* --size-2: 0.5rem (8px) */
/* --size-3: 1rem (16px) */
/* --size-4: 1.25rem (20px) */
/* ... */
/* --size-15: 64rem (1024px) */
```

### Colors

```css
@import 'open-props/colors.min.css';
```

```css
/* Usage */
.button {
  background: var(--blue-7);
  color: var(--gray-0);
}

.button:hover {
  background: var(--blue-8);
}

/* Color scales: 0-12 (light to dark) */
/* Available colors: gray, stone, red, pink, purple, violet, */
/* indigo, blue, cyan, teal, green, lime, yellow, orange */
```

### Shadows

```css
@import 'open-props/shadows.min.css';
```

```css
/* Usage */
.card {
  box-shadow: var(--shadow-2);
}

.card:hover {
  box-shadow: var(--shadow-4);
}

/* Shadow scale: 1-6 (subtle to dramatic) */
```

### Gradients

```css
@import 'open-props/gradients.min.css';
```

```css
/* Usage */
.hero {
  background: var(--gradient-1);
}

/* 30 pre-built gradients */
```

### Animations

```css
@import 'open-props/animations.min.css';
```

```css
/* Usage */
.fade-in {
  animation: var(--animation-fade-in);
}

.slide-in {
  animation: var(--animation-slide-in-up);
}

/* Available: fade-in, fade-out, scale-up, scale-down, */
/* slide-in-*, slide-out-*, shake-*, spin, ping, blink */
```

### Easings

```css
@import 'open-props/easings.min.css';
```

```css
/* Usage */
.transition {
  transition: transform 0.3s var(--ease-3);
}

/* Easing scale: 1-5 (subtle to dramatic) */
/* Types: ease, ease-in, ease-out, ease-in-out, */
/* ease-elastic, ease-squish, ease-bounce */
```

### Borders

```css
@import 'open-props/borders.min.css';
```

```css
/* Usage */
.card {
  border-radius: var(--radius-2);
}

.pill {
  border-radius: var(--radius-round);
}

/* Border radius scale: 1-6 + round, blob, conditional */
```

### Aspect Ratios

```css
@import 'open-props/aspects.min.css';
```

```css
/* Usage */
.video {
  aspect-ratio: var(--ratio-widescreen); /* 16/9 */
}

.square {
  aspect-ratio: var(--ratio-square); /* 1 */
}
```

## Integration with @layer

Combine with CSS cascade layers:

```css
/* main.css */
@layer tokens, reset, base, components, utilities;

@import 'open-props/colors.min.css' layer(tokens);
@import 'open-props/sizes.min.css' layer(tokens);
@import 'open-props/shadows.min.css' layer(tokens);

@layer tokens {
  /* Override or extend Open Props */
  :root {
    --color-primary: var(--blue-7);
    --color-secondary: var(--purple-7);
    --space-page: var(--size-5);
  }
}

@layer base {
  body {
    color: var(--gray-8);
    background: var(--gray-1);
  }
}
```

## Project Token Mapping

Map Open Props to semantic project tokens:

```css
/* tokens.css */
:root {
  /* Colors - Semantic mapping */
  --color-text: var(--gray-8);
  --color-text-muted: var(--gray-6);
  --color-background: var(--gray-0);
  --color-surface: var(--gray-1);
  --color-border: var(--gray-3);

  --color-primary: var(--blue-7);
  --color-primary-hover: var(--blue-8);
  --color-primary-text: var(--gray-0);

  --color-success: var(--green-7);
  --color-warning: var(--yellow-6);
  --color-error: var(--red-7);

  /* Spacing - Semantic mapping */
  --space-xs: var(--size-1);
  --space-sm: var(--size-2);
  --space-md: var(--size-3);
  --space-lg: var(--size-5);
  --space-xl: var(--size-7);

  /* Typography */
  --font-size-sm: var(--font-size-0);
  --font-size-base: var(--font-size-1);
  --font-size-lg: var(--font-size-2);
  --font-size-xl: var(--font-size-4);
  --font-size-2xl: var(--font-size-6);

  /* Effects */
  --shadow-sm: var(--shadow-1);
  --shadow-md: var(--shadow-3);
  --shadow-lg: var(--shadow-5);

  --radius-sm: var(--radius-2);
  --radius-md: var(--radius-3);
  --radius-lg: var(--radius-4);
}
```

## Dark Mode

Open Props includes HSL versions for easy dark mode:

```css
@import 'open-props/colors-hsl.min.css';

:root {
  --surface: hsl(var(--gray-0-hsl));
  --text: hsl(var(--gray-9-hsl));
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface: hsl(var(--gray-9-hsl));
    --text: hsl(var(--gray-1-hsl));
  }
}
```

Or use the OKLCH versions for better color manipulation:

```css
@import 'open-props/colors.min.css'; /* OKLCH by default */

:root {
  --text-color: var(--gray-8);
  --bg-color: var(--gray-1);
}

[data-theme="dark"] {
  --text-color: var(--gray-2);
  --bg-color: var(--gray-9);
}
```

## Responsive Typography

```css
/* Fluid type scale */
@import 'open-props/fonts.min.css';

h1 { font-size: var(--font-size-fluid-3); }
h2 { font-size: var(--font-size-fluid-2); }
h3 { font-size: var(--font-size-fluid-1); }
p { font-size: var(--font-size-fluid-0); }
small { font-size: var(--font-size-0); }
```

## Minimal Import Strategy

Import only what you use:

```css
/* Minimal setup - just essentials */
@import 'open-props/sizes.min.css';
@import 'open-props/gray.min.css';      /* Just gray colors */
@import 'open-props/blue.min.css';      /* Just blue colors */
@import 'open-props/shadows.min.css';
@import 'open-props/borders.min.css';
```

Or copy specific values (zero runtime dependency):

```css
/* Manually copied values - no import needed */
:root {
  --size-1: 0.25rem;
  --size-2: 0.5rem;
  --size-3: 1rem;
  --size-4: 1.25rem;
  --size-5: 1.5rem;

  --gray-0: oklch(99% 0 0);
  --gray-1: oklch(95% 0 0);
  --gray-8: oklch(27.8% 0 0);
  --gray-9: oklch(21% 0 0);

  --blue-7: oklch(48.8% 0.243 264.05);

  --shadow-2: 0 3px 5px -2px hsl(0 0% 0% / 0.1),
              0 7px 14px -5px hsl(0 0% 0% / 0.1);

  --radius-2: 0.5rem;
}
```

## Checklist

When using Open Props:

- [ ] Import only needed modules (not everything)
- [ ] Map to semantic project tokens
- [ ] Document which values are used
- [ ] Consider copying values for zero dependencies
- [ ] Test dark mode color combinations
- [ ] Verify animation performance

## Related Skills

- **css-author** - CSS organization and @layer
- **performance** - Minimize CSS payload
- **accessibility-checker** - Color contrast requirements
