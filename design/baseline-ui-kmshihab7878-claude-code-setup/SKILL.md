---
name: baseline-ui
description: >
  Validates animation durations, enforces typography scale, checks component accessibility, and
  prevents layout anti-patterns in Tailwind CSS projects. Mobile-first responsive design with
  breakpoints, fluid typography, container queries, and cross-device patterns. Use when building
  UI components, reviewing CSS utilities, styling React views, or enforcing design consistency.
risk: low
tags: [ui, tailwind]
created: 2026-03-07
updated: 2026-03-17
---

# Baseline UI

Enforces an opinionated UI baseline to prevent AI-generated interface slop. Includes responsive design patterns for mobile-first development.

## How to use

- `/baseline-ui`
  Apply these constraints to any UI work in this conversation.

- `/baseline-ui <file>`
  Review the file against all constraints below and output:
  - violations (quote the exact line/snippet)
  - why it matters (1 short sentence)
  - a concrete fix (code-level suggestion)

## When to use

Reference these guidelines when:
- building UI components in Tailwind CSS
- reviewing CSS utilities or styling React views
- enforcing design consistency across a project
- building responsive layouts for mobile/tablet/desktop
- implementing fluid typography or responsive navigation
- using CSS Grid, Flexbox, or container queries for layouts
- testing across screen sizes

## When NOT to use

Do NOT apply this skill when:
- the project uses a different CSS framework (Bootstrap, vanilla CSS) — adapt principles but not Tailwind-specific rules
- the task is purely creative/experimental design (use `frontend-design` skill)
- the task is about animation performance debugging (use `fixing-motion-performance` skill)

---

## Stack

- MUST use Tailwind CSS defaults unless custom values already exist or are explicitly requested
- MUST use `motion/react` (formerly `framer-motion`) when JavaScript animation is required
- SHOULD use `tw-animate-css` for entrance and micro-animations in Tailwind CSS
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic

## Components

- MUST use accessible component primitives for anything with keyboard or focus behavior (`Base UI`, `React Aria`, `Radix`)
- MUST use the project's existing component primitives first
- NEVER mix primitive systems within the same interaction surface
- SHOULD prefer [`Base UI`](https://base-ui.com/react/components) for new primitives if compatible with the stack
- MUST add an `aria-label` to icon-only buttons
- NEVER rebuild keyboard or focus behavior by hand unless explicitly requested

## Interaction

- MUST use an `AlertDialog` for destructive or irreversible actions
- SHOULD use structural skeletons for loading states
- NEVER use `h-screen`, use `h-dvh`
- MUST respect `safe-area-inset` for fixed elements
- MUST show errors next to where the action happens
- NEVER block paste in `input` or `textarea` elements

## Animation

- NEVER add animation unless it is explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD avoid animating paint properties (`background`, `color`) except for small, local UI (text, icons)
- SHOULD use `ease-out` on entrance
- NEVER exceed `200ms` for interaction feedback
- MUST pause looping animations when off-screen
- SHOULD respect `prefers-reduced-motion`
- NEVER introduce custom easing curves unless explicitly requested
- SHOULD avoid animating large images or full-screen surfaces

## Typography

- MUST use `text-balance` for headings and `text-pretty` for body/paragraphs
- MUST use `tabular-nums` for data
- SHOULD use `truncate` or `line-clamp` for dense UI
- NEVER modify `letter-spacing` (`tracking-*`) unless explicitly requested

## Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-*`)
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

## Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic

## Design

- NEVER use gradients unless explicitly requested
- NEVER use purple or multicolor gradients
- NEVER use glow effects as primary affordances
- SHOULD use Tailwind CSS default shadow scale unless explicitly requested
- MUST give empty states one clear next action
- SHOULD limit accent color usage to one per view
- SHOULD use existing theme or Tailwind CSS color tokens before introducing new ones

---

## Responsive Design

### Mobile-First Methodology

Start with mobile styles, progressively enhance for larger screens.

```css
/* Mobile-first: base styles ARE mobile styles */
.container {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    flex-direction: row;
    gap: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem;
  }
}
```

**Why mobile-first**: Forces content prioritization, smaller CSS payload for mobile, progressive enhancement is more robust than graceful degradation.

### Breakpoint System (Tailwind)

| Breakpoint | Min-width | Target |
|-----------|-----------|--------|
| `sm` | 640px | Large phones (landscape) |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large desktops |

**Prefer content-based breakpoints** over device-based when possible:
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
}
/* No media queries needed — grid adapts automatically */
```

### Shadcn-UI Responsive Patterns
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card className="p-4 md:p-6">
    <CardTitle className="text-lg md:text-xl lg:text-2xl">Title</CardTitle>
    <CardContent className="text-sm md:text-base">Content</CardContent>
  </Card>
</div>
```

### Fluid Typography

```css
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.825rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.5vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.2rem + 1.5vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.4rem + 2.25vw, 2.5rem);
  --text-4xl: clamp(2.25rem, 1.5rem + 3.5vw, 3.5rem);

  --space-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --space-sm: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-md: clamp(1rem, 0.8rem + 1vw, 1.5rem);
  --space-lg: clamp(1.5rem, 1.2rem + 1.5vw, 2.5rem);
  --space-xl: clamp(2rem, 1.5rem + 2.5vw, 4rem);
}
```

### Container Queries

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card-body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
}

@container card (min-width: 600px) {
  .card-body {
    grid-template-columns: 1fr 2fr;
  }
}
```

### Responsive Images

```html
<picture>
  <source media="(min-width: 1024px)" srcset="hero-desktop.webp" />
  <source media="(min-width: 640px)" srcset="hero-tablet.webp" />
  <img src="hero-mobile.webp" alt="Hero image" loading="lazy" />
</picture>

<img
  srcset="photo-400.webp 400w, photo-800.webp 800w, photo-1200.webp 1200w"
  sizes="(min-width: 1024px) 50vw, (min-width: 640px) 75vw, 100vw"
  src="photo-800.webp"
  alt="Photo"
  loading="lazy"
  decoding="async"
/>
```

### Responsive Navigation

**Hamburger menu** (mobile → desktop):
```css
.nav-links { display: none; }
.nav-toggle { display: block; }

@media (min-width: 768px) {
  .nav-links { display: flex; gap: 1.5rem; }
  .nav-toggle { display: none; }
}
```

**Bottom tab bar** (mobile only):
```css
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  padding: 0.5rem;
}

@media (min-width: 768px) {
  .bottom-nav { display: none; }
}
```

### Responsive Tables

```css
/* Horizontal scroll */
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Card layout on mobile */
@media (max-width: 640px) {
  table, thead, tbody, th, td, tr { display: block; }
  thead { display: none; }
  td {
    position: relative;
    padding-left: 50%;
  }
  td::before {
    content: attr(data-label);
    position: absolute;
    left: 0.5rem;
    font-weight: 600;
  }
}
```

### Touch-Friendly Design

- **44x44px** minimum touch target (Apple HIG)
- **48x48dp** minimum touch target (Material Design)
- **8px** minimum spacing between touch targets

```css
.btn {
  min-height: 44px;
  min-width: 44px;
  padding: 0.75rem 1.5rem;
}

.icon-btn {
  position: relative;
}
.icon-btn::after {
  content: "";
  position: absolute;
  inset: -8px; /* Expand tap area */
}
```

### Dark Mode + Responsive

```css
:root {
  --bg: #ffffff;
  --text: #1a1a1a;
  --card-bg: #f9fafb;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0a0a0a;
    --text: #f5f5f5;
    --card-bg: #1a1a1a;
  }
}
```

---

## Responsive Checklist

- [ ] Test at all Tailwind breakpoints (640, 768, 1024, 1280, 1536px)
- [ ] Test landscape orientation on mobile
- [ ] Verify touch targets are 44px+ on mobile
- [ ] Check text readability at all sizes
- [ ] Verify images don't overflow containers
- [ ] Test navigation collapse/expand
- [ ] Check form inputs are usable on mobile
- [ ] Verify no horizontal scroll at any breakpoint
- [ ] Test with browser zoom (200%, 400%)
- [ ] Check `prefers-reduced-motion` support
- [ ] Use `webapp-testing` skill for Playwright viewport testing

## Cross-references

- **frontend-design** skill: Creative UI design, bold aesthetics
- **fixing-accessibility** skill: ARIA, keyboard nav, WCAG
- **fixing-motion-performance** skill: Animation performance debugging
- **ui-ux-pro-max** skill: 50+ styles, design system generation
- **webapp-testing** skill: Playwright browser testing across viewports
- **FRONTEND_PATTERNS.md**: Component library patterns reference
