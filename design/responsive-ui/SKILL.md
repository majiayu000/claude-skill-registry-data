---
name: responsive-ui
description: Build truly responsive SPA, MPA, or landing pages that adapt gracefully from foldable phones (280px) to ultra-wide desktops (2560px+). Use when the user asks to create responsive websites, landing pages, mobile-first designs, or any web interface requiring broad device support. Generates semantic HTML5, mobile-first CSS with fluid typography, CSS Grid/Flexbox layouts, accessible navigation with hamburger menus, and responsive images with srcset/lazy loading.
---

# Responsive UI Architecture

Build production-ready responsive web interfaces that work on every screen size without compromise.

## Core Principles

1. **Mobile-first CSS**: Start with smallest viewport, layer complexity upward
2. **Content-driven breakpoints**: Break when content breaks, not at device widths
3. **Fluid everything**: Typography, spacing, and containers scale smoothly
4. **No horizontal scroll**: Ever. Test at 280px minimum.
5. **Equal experience**: Every device gets full functionality

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│  Semantic HTML5 (accessibility layer)                       │
├─────────────────────────────────────────────────────────────┤
│  CSS Custom Properties (design tokens)                      │
├─────────────────────────────────────────────────────────────┤
│  CSS Grid (macro layout) + Flexbox (component alignment)    │
├─────────────────────────────────────────────────────────────┤
│  Fluid Typography clamp() + Container Queries (optional)    │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Workflow

### Step 1: Set Up Design Tokens

```css
:root {
  /* Fluid typography: min, preferred (vw-based), max */
  --fs-sm: clamp(0.875rem, 0.8rem + 0.25vw, 1rem);
  --fs-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --fs-lg: clamp(1.25rem, 1rem + 1vw, 1.5rem);
  --fs-xl: clamp(1.5rem, 1rem + 2vw, 2.5rem);
  --fs-2xl: clamp(2rem, 1.5rem + 2.5vw, 3.5rem);
  
  /* Fluid spacing */
  --space-xs: clamp(0.5rem, 0.4rem + 0.25vw, 0.75rem);
  --space-sm: clamp(0.75rem, 0.6rem + 0.5vw, 1rem);
  --space-md: clamp(1rem, 0.8rem + 1vw, 1.5rem);
  --space-lg: clamp(1.5rem, 1rem + 2vw, 2.5rem);
  --space-xl: clamp(2rem, 1.5rem + 3vw, 4rem);
  
  /* Layout */
  --content-width: min(90vw, 1200px);
  --narrow-width: min(90vw, 65ch);
}
```

### Step 2: Base Reset & Typography

```css
*, *::before, *::after { box-sizing: border-box; }

html {
  font-size: 100%; /* Respect user preferences */
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: var(--fs-base);
  line-height: 1.6;
  overflow-x: hidden; /* Prevent horizontal scroll */
}

img, video, svg {
  max-width: 100%;
  height: auto;
  display: block;
}
```

### Step 3: Layout with CSS Grid

**Macro layout** (full-page structure):

```css
.page {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

/* Responsive grid for content sections */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
  gap: var(--space-md);
}
```

### Step 4: Flexbox for Components

```css
.header-inner {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
}
```

### Step 5: Content-Driven Breakpoints

Only add breakpoints when content genuinely breaks:

```css
/* Nav collapses when it can't fit horizontally */
@media (max-width: 600px) {
  .nav-list { display: none; }
  .nav-toggle { display: block; }
}

/* Hero text needs more space on larger screens */
@media (min-width: 800px) {
  .hero { padding-block: var(--space-xl); }
}
```

### Step 6: Accessible Hamburger Navigation

Key requirements:
- `aria-expanded` toggles on button
- `aria-controls` links button to nav
- `aria-label` for screen readers
- Keyboard accessible (Enter/Space)
- Focus management

See `references/accessible-nav.md` for complete implementation.

### Step 7: Responsive Images

```html
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
  sizes="(max-width: 600px) 100vw, 80vw"
  alt="Descriptive alt text"
  loading="lazy"
  decoding="async"
  width="1200"
  height="600"
>
```

## Responsive Component Patterns

See `references/component-patterns.md` for responsive implementations of:

- **Navigation**: Hamburger menu, mega menu, off-canvas drawer, sticky header
- **Forms**: Text fields, dropdowns, date pickers, switches, autocomplete
- **Feedback**: Modals, dialogs, toasts, snackbars, tooltips
- **Content**: Cards, carousels, accordions, tabs, masonry grids
- **Progress**: Steppers, skeleton loaders, spinners
- **Actions**: FAB, ghost buttons, CTAs, chips/pills

Key responsive rules:
1. **Touch targets**: All interactive elements ≥44×44px on mobile
2. **Modals**: Full-screen on mobile, centered overlay on desktop
3. **Dropdowns**: Native `<select>` on mobile, custom on desktop (optional)
4. **Tooltips**: Tap-to-show on touch devices, hover on desktop
5. **Carousels**: Swipe gestures + visible arrows on desktop
6. **Mega menus**: Collapse to accordion on mobile

## Resources

- **Testing checklist**: `references/testing-checklist.md`
- **Accessible nav pattern**: `references/accessible-nav.md`
- **Component patterns**: `references/component-patterns.md`
- **Complete template**: `assets/responsive-landing.html`

## Critical Reminders

1. **Test at 280px** — Foldable phones exist
2. **Test at 2560px+** — Ultra-wide monitors exist
3. **Keyboard navigation** — Tab through everything
4. **Screen reader** — Test with VoiceOver/NVDA
5. **Lighthouse** — Target ≥95 Performance, ≥95 Accessibility
