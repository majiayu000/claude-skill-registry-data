---
name: responsive-design-patterns
description: "Both directions produce working layouts, but very different amounts of CSS."
---

# Responsive Design Patterns (Verbose)

## Core Patterns

### Mobile-First Is a CSS Volume Argument

Both directions produce working layouts, but very different amounts of CSS.

```css
/* ✅ mobile-first: each query ADDS */
.sidebar { display: none; }
.content { padding: 1rem; }

@media (min-width: 64rem) {
  .sidebar { display: block; width: 16rem; }
  .content { padding: 2rem 3rem; }
}

/* ❌ desktop-first: each query UNDOES */
.sidebar { display: block; width: 16rem; float: left; }
.content { padding: 2rem 3rem; margin-left: 16rem; }

@media (max-width: 64rem) {
  .sidebar { display: none; width: auto; float: none; }   /* three resets */
  .content { padding: 1rem; margin-left: 0; }             /* two more */
}
```

The desktop-first version must neutralize every property it set, and each reset
is itself a rule someone will later override. Mobile-first also leaves the
simplest layout as the unconditional base — what renders if a query never matches.

Express breakpoints in `rem`, not `px`: a `min-width: 48rem` query moves with the
user's root font size, so a user at 24px base text doesn't get a cramped
multi-column layout. And derive the values from where *your content* breaks —
resize until it looks wrong, put a breakpoint there — not from a device list that
goes out of date every year.

### Container Queries Solve What Media Queries Cannot

A media query asks "how wide is the viewport?" A component's correct layout
depends on how wide *it* is — and those are unrelated whenever the component
appears in more than one region.

```css
.card-area { container-type: inline-size; container-name: card; }

.card { display: block; }                    /* stacked by default */

@container card (min-width: 30rem) {
  .card { display: grid; grid-template-columns: 10rem 1fr; gap: 1rem; }
}
```

Now the same `.card` renders stacked in a 280px sidebar and horizontal in an
800px main column — same viewport, same moment. With media queries this needs
either a viewport-plus-region selector matrix (`.sidebar .card`, `.main .card`,
each with its own breakpoints) or duplicated components. Both scale badly and
break the moment someone drops the card in a new region.

| | Media query | Container query |
|---|---|---|
| Asks about | Viewport | Nearest container element |
| Portability | Breaks when moved | Moves intact |
| Right for | Page structure | Component internals |

Use media queries for the page shell (does the sidebar exist?) and container
queries for everything inside components. Note that `container-type: inline-size`
applies containment — apply it to a wrapper, not to an element whose height you
depend on.

Container query units (`cqi`, `cqw`) let internal sizing scale with the container
too: `font-size: clamp(1rem, 0.9rem + 1.5cqi, 1.5rem)`.

### Intrinsic Layouts

Many layouts need no breakpoints at all — let the algorithm respond.

```css
/* Responsive grid, no media queries */
.auto-grid {
  display: grid; gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(min(20rem, 100%), 1fr));
}

/* Sidebar that wraps when the main column would get too narrow */
.with-sidebar { display: flex; flex-wrap: wrap; gap: 1.5rem; }
.with-sidebar > .side { flex: 1 1 16rem; }
.with-sidebar > .main { flex: 999 1 30rem; }   /* huge grow: wins until it can't fit */
```

The `min(20rem, 100%)` matters: a bare `minmax(20rem, 1fr)` overflows whenever the
container is narrower than 20rem — exactly the mobile case. `auto-fit` collapses
empty tracks so items stretch to fill the row; `auto-fill` keeps them, preserving
column rhythm. Gallery: `auto-fit`. Dashboard: `auto-fill`.

### Fluid Typography and Spacing

```css
:root {
  --step-2: clamp(1.5rem, 1.3rem + 1vw, 2.25rem);
  --space-fluid-md: clamp(1rem, 0.8rem + 1vw, 2rem);
}
h2 { font-size: var(--step-2); }
section { padding-block: var(--space-fluid-md); }
```

The middle term must include a `rem` component. `clamp(1rem, 4vw, 2rem)` looks
fine until a user zooms: viewport units don't scale with zoom the way text does,
so the size stays pinned and fails WCAG 1.4.4 (resize text to 200%).

Cap measure for readability (`.prose { max-width: 65ch; }`) rather than reaching
for another breakpoint.

### Images

```html
<img src="/hero-800.jpg"
     srcset="/hero-400.jpg 400w, /hero-800.jpg 800w, /hero-1600.jpg 1600w"
     sizes="(min-width: 64rem) 50vw, 100vw"
     width="1600" height="900" alt="..." loading="lazy" decoding="async">
```

`srcset` + `sizes` lets the browser pick by width and device pixel ratio. The
`width`/`height` attributes let it reserve the correct box before load —
omitting them is the most common source of layout shift, and CSS `aspect-ratio`
serves the same purpose for CSS-sized media. Never set `loading="lazy"` on the
LCP image; it delays the very thing being measured.

### Input Modality

```css
@media (hover: hover) and (pointer: fine) { .row:hover .row__actions { opacity: 1; } }
@media (pointer: coarse) {
  .row__actions { opacity: 1; }        /* always visible for touch */
  .btn { min-height: 2.75rem; }        /* comfortable touch target */
}
```

Screen width is not input type: touchscreen laptops are wide and coarse, a phone
with a stylus is narrow and fine. Query the capability directly, and pair it with
a `prefers-reduced-motion: reduce` block neutralizing non-essential animation.

### Viewport Units on Mobile

Use `min-height: 100dvh` for full-height panels, not `100vh`.

`100vh` is sized against the *largest* viewport — the one with browser chrome
retracted — so a full-height element is taller than the visible area while the
address bar is showing, and its bottom is cut off. `dvh` tracks the dynamic
viewport; `svh` and `lvh` give the small and large extremes when you need a stable
value. Combine with `env(safe-area-inset-*)` so content clears notches.

## Common Anti-Patterns

❌ **Device-named breakpoints** — `@media (max-width: 375px) /* iPhone */` is
obsolete on release day.
✅ Breakpoints derived from where the content stops working.

❌ **Desktop-first `max-width` chains** — every rule needs an undo.
✅ Mobile-first `min-width`, additive only.

❌ **Viewport queries for component internals** — the component works in one
region and breaks in every other.
✅ `container-type: inline-size` on the wrapper, `@container` inside.

❌ **`minmax(20rem, 1fr)` without a `min()` guard** — overflow below 20rem.
✅ `minmax(min(20rem, 100%), 1fr)`.

❌ **Pure `vw` font sizing** — text stops responding to zoom, failing WCAG 1.4.4.
✅ `clamp()` with a `rem` term in the fluid middle.

❌ **`display: none` to "make it responsive"** — mobile users lose functionality
instead of getting a different arrangement.
✅ Reflow, collapse into a disclosure, or move into a bottom sheet.

❌ **Hover-revealed actions with no coarse-pointer path** — unreachable on touch.
✅ Gate on `(hover: hover)` and provide a persistent alternative.

❌ **`100vh` full-height panels on mobile** — clipped under browser chrome.
✅ `100dvh`, plus safe-area insets.

❌ **Images without intrinsic dimensions** — layout shift on every load.
✅ `width`/`height` attributes or `aspect-ratio`.

## Responsive Design Checklist

- [ ] Base styles are the smallest layout; queries only add
- [ ] Breakpoints in `rem`, chosen from content, not devices
- [ ] Component-internal adaptation uses container queries
- [ ] `container-type` applied to a wrapper, not a height-critical element
- [ ] Grids use `auto-fit`/`auto-fill` with a `min()` overflow guard
- [ ] Fluid type via `clamp()` with a `rem` term in the middle
- [ ] Line length capped (~65ch) for prose
- [ ] Images use `srcset` + `sizes` and declare intrinsic dimensions
- [ ] LCP image not lazy-loaded
- [ ] Hover affordances gated on `(hover: hover)`; touch targets ~44px on coarse
- [ ] `100dvh` used instead of `100vh`; `env(safe-area-inset-*)` on edge UI
- [ ] `prefers-reduced-motion` honored
- [ ] No horizontal scroll at 320px; layout verified at 200% zoom
- [ ] Nothing essential removed at small widths — only rearranged
