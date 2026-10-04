---
name: css-responsive
description: |
  Modern responsive design using container queries, fluid typography, responsive
  images, logical properties, viewport units, intrinsic sizing, and preference
  queries. Prioritizes container queries over media queries. Use when the user
  asks for responsive CSS, responsive design, mobile layout, fluid typography,
  responsive images, dark mode, prefers-reduced-motion, or adaptive design.
disable-model-invocation: true
license: MIT
---

# css.dev — CSS Responsive

You are a senior CSS engineer specializing in responsive design. Build responsive layouts and components using modern techniques. Always generate code. Prefer intrinsic sizing and container queries over breakpoint-driven media queries. For reference, see [modern-patterns.md](../css-expert/references/modern-patterns.md) and [browser-compat.md](../css-expert/references/browser-compat.md).

## Workflow

1. **Understand the target** — Is this a page-level layout or a component? Components use container queries. Pages use media queries.
2. **Start fluid** — Use `clamp()`, intrinsic sizing, and flexible grids so most things just work without breakpoints.
3. **Add container queries** — For components that need layout changes based on their container size.
4. **Add media queries** — Only for page-level layout shifts (sidebar collapse, navigation pattern change).
5. **Add preference queries** — Color scheme, reduced motion, contrast.
6. **Handle images** — Use `srcset`, `sizes`, and `<picture>` for responsive images.

## Responsive Strategy Hierarchy

Apply in this order — each layer reduces the need for the next:

```
1. Intrinsic sizing     → content determines size naturally
2. Fluid values         → clamp() adapts without breakpoints
3. Flexible layouts     → Grid/Flexbox auto-fill, wrap, grow
4. Container queries    → component adapts to its container
5. Media queries        → page-level layout shifts only
```

## Container Queries

### When to Use

- A component's layout should change based on **its container**, not the viewport.
- Cards, widgets, sidebars, navigation items — anything reusable.

### Setup

```css
.component-wrapper {
  container-type: inline-size;
  container-name: card;
}
```

### Responsive Component

```css
.card-wrapper {
  container-type: inline-size;
}

.card {
  display: flex;
  flex-direction: column;
  gap: var(--space-s);

  @container (inline-size >= 450px) {
    flex-direction: row;
    align-items: center;
  }

  @container (inline-size >= 700px) {
    display: grid;
    grid-template-columns: 250px 1fr auto;
  }
}
```

### Container Query Units

| Unit | Meaning |
|------|---------|
| `cqi` | 1% of container inline size |
| `cqb` | 1% of container block size |
| `cqmin` | smaller of `cqi` and `cqb` |
| `cqmax` | larger of `cqi` and `cqb` |

```css
.card-title {
  font-size: clamp(1rem, 3cqi, 1.5rem);
}
```

### Named Containers

```css
.sidebar {
  container-type: inline-size;
  container-name: sidebar;
}

@container sidebar (inline-size > 300px) {
  .widget { display: grid; grid-template-columns: 1fr 1fr; }
}
```

## Media Queries (Page Level Only)

Use media queries only for page-level layout shifts.

### Correct Usage

```css
@media (max-width: 48em) {
  .page {
    grid-template-columns: 1fr;
  }
  .sidebar { display: none; }
}
```

### Rules

- Use `em` units, never `px` — respects user font size.
- Prefer `min-width` (mobile-first) unless the desktop layout is simpler.
- Limit to 2–3 breakpoints maximum for page layout.
- Never use media queries for component-level responsiveness.

### Recommended Breakpoints (if needed)

```css
/* Compact */    @media (max-width: 48em) { }
/* Medium */     @media (min-width: 48em) and (max-width: 64em) { }
/* Expanded */   @media (min-width: 64em) { }
```

## Fluid Typography

Use `clamp()` for font sizes that scale smoothly between a minimum and maximum.

### Type Scale

```css
:root {
  --text-sm:  clamp(0.8rem, 0.75rem + 0.25vw, 0.875rem);
  --text-base: clamp(1rem, 0.925rem + 0.375vw, 1.125rem);
  --text-lg:  clamp(1.125rem, 1rem + 0.625vw, 1.375rem);
  --text-xl:  clamp(1.25rem, 1.1rem + 0.75vw, 1.625rem);
  --text-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2.25rem);
  --text-3xl: clamp(2rem, 1.5rem + 2.5vw, 3.5rem);
}
```

### How clamp() Works

```
clamp(minimum, preferred, maximum)
```

- **minimum**: smallest the value can be (in `rem`)
- **preferred**: scales with viewport (use `rem + vw`)
- **maximum**: largest the value can be (in `rem`)

### Fluid Spacing Scale

```css
:root {
  --space-xs: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-s:  clamp(0.75rem, 0.6rem + 0.75vw, 1rem);
  --space-m:  clamp(1rem, 0.8rem + 1vw, 1.5rem);
  --space-l:  clamp(1.5rem, 1.2rem + 1.5vw, 2rem);
  --space-xl: clamp(2rem, 1.6rem + 2vw, 3rem);
  --space-2xl: clamp(3rem, 2.4rem + 3vw, 4.5rem);
}
```

## Responsive Images

### srcset + sizes

```html
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w,
    image-1600.jpg 1600w
  "
  sizes="
    (max-width: 48em) 100vw,
    (max-width: 64em) 50vw,
    33vw
  "
  alt="Description"
  loading="lazy"
  decoding="async"
>
```

### Art Direction with `<picture>`

```html
<picture>
  <source
    media="(min-width: 64em)"
    srcset="hero-wide.avif"
    type="image/avif"
  >
  <source
    media="(min-width: 48em)"
    srcset="hero-medium.avif"
    type="image/avif"
  >
  <img
    src="hero-narrow.jpg"
    alt="Description"
    loading="lazy"
    decoding="async"
  >
</picture>
```

### Responsive Image CSS

```css
img {
  max-inline-size: 100%;
  block-size: auto;
  display: block;
}

.hero-image {
  inline-size: 100%;
  block-size: auto;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
```

## Viewport Units

### Modern Viewport Units

| Unit | Meaning |
|------|---------|
| `dvh` | Dynamic viewport height (accounts for mobile browser chrome) |
| `svh` | Small viewport height (smallest possible viewport) |
| `lvh` | Large viewport height (largest possible viewport) |
| `dvw` | Dynamic viewport width |

### Usage

```css
.full-screen {
  min-block-size: 100dvh;
}

.hero {
  block-size: 100svh;
}
```

- Use `dvh` for full-height layouts on mobile (accounts for URL bar).
- Use `svh` when you need the element to never exceed the visible area.
- Never use `100vh` — it doesn't account for mobile browser UI.

## Intrinsic Sizing

### min(), max(), clamp()

```css
.container {
  inline-size: min(90%, 75rem);
  margin-inline: auto;
}

.card-grid {
  grid-template-columns: repeat(auto-fill, minmax(min(280px, 100%), 1fr));
}

.sidebar {
  inline-size: clamp(200px, 25%, 350px);
}
```

### fit-content

```css
.tag {
  inline-size: fit-content;
  padding-inline: var(--space-s);
}
```

### min-content / max-content

```css
.nav { inline-size: max-content; }
.label { inline-size: min-content; }
```

## Logical Properties

Use logical properties for all directional values. They support RTL/LTR automatically.

```css
.element {
  margin-block: var(--space-m);
  padding-inline: var(--space-l);
  border-inline-start: 3px solid var(--color-primary);
  max-inline-size: 65ch;
  text-align: start;
}
```

Full mapping reference in the [css-layout](../css-layout/SKILL.md) skill.

## Preference Queries

### Color Scheme

```css
:root {
  color-scheme: light dark;
  --color-surface: light-dark(white, oklch(15% 0 0));
  --color-text: light-dark(oklch(20% 0 0), oklch(90% 0 0));
  --color-border: light-dark(oklch(80% 0 0), oklch(30% 0 0));
}
```

`light-dark()` is preferred over `@media (prefers-color-scheme)` for individual values. Use the media query only for structural changes:

```css
@media (prefers-color-scheme: dark) {
  .logo { filter: brightness(1.2); }
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### High Contrast

```css
@media (prefers-contrast: more) {
  :root {
    --color-border: oklch(0% 0 0);
    --color-text: oklch(0% 0 0);
  }

  .card {
    border: 2px solid var(--color-border);
  }
}
```

### Forced Colors (Windows High Contrast)

```css
@media (forced-colors: active) {
  .button {
    border: 2px solid ButtonText;
  }

  .icon {
    forced-color-adjust: none;
  }
}
```

### Reduced Transparency

```css
@media (prefers-reduced-transparency: reduce) {
  .overlay {
    background: var(--color-surface);
    backdrop-filter: none;
  }
}
```

## Responsive Spacing Scale

Use `clamp()` for spacing that scales between viewports without breakpoints:

```css
:root {
  --space-xs: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-s:  clamp(0.75rem, 0.6rem + 0.75vw, 1rem);
  --space-m:  clamp(1rem, 0.8rem + 1vw, 1.5rem);
  --space-l:  clamp(1.5rem, 1.2rem + 1.5vw, 2rem);
  --space-xl: clamp(2rem, 1.6rem + 2vw, 3rem);
}

section { padding-block: var(--space-xl); }
.stack > * + * { margin-block-start: var(--space-m); }
```

## Checklist Before Delivering

- [ ] Container queries used for component responsiveness (not media queries)
- [ ] Media queries limited to page-level layout shifts
- [ ] Media queries use `em` units (not `px`)
- [ ] Font sizes use `clamp()` with `rem` + `vw`
- [ ] Spacing uses fluid scale with custom properties
- [ ] Logical properties used (no `left`/`right`/`top`/`bottom`)
- [ ] Images use `srcset`/`sizes` or `<picture>` where appropriate
- [ ] `100dvh` used instead of `100vh`
- [ ] `prefers-reduced-motion` handled
- [ ] `prefers-color-scheme` handled (or `light-dark()`)
- [ ] `prefers-contrast` handled for key elements
- [ ] No fixed widths — intrinsic sizing with `min()`/`max()`/`clamp()`
- [ ] Content is readable at 320px and 2560px viewports
