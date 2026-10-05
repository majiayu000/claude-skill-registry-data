---
name: css-performance-optimization
description: "Every visual change enters the pipeline at one of four stages, and the stage"
---

# CSS Performance Optimization (Verbose)

## Core Patterns

### The Rendering Pipeline

Every visual change enters the pipeline at one of four stages, and the stage
determines the cost:

```
Style  →  Layout  →  Paint  →  Composite
```

| Change | Enters at | Frame budget impact |
|---|---|---|
| `transform`, `opacity` | Composite | Cheapest; can run off main thread |
| `background-color`, `color`, `box-shadow`, `border-radius` | Paint | Moderate — repaints the layer |
| `width`, `height`, `top`, `margin`, `padding`, `font-size` | Layout | Expensive — reflows the subtree |
| Adding/removing DOM, changing `display` | Style | Most expensive |

At 60fps you have 16.7ms per frame, part of which the browser needs for
compositing and JS. A layout-triggering animation recomputes geometry for a whole
subtree on every one of those frames, on the main thread, competing with your
JavaScript. Transform and opacity changes on a promoted layer are handed to the
compositor, which is why they keep animating smoothly even while the main thread
is blocked.

```css
/* ❌ animates layout 60×/second */
.panel { transition: left 250ms ease, height 250ms ease; }
.panel.open { left: 0; height: 400px; }

/* ✅ same visual result, composite-only */
.panel { transition: transform 250ms ease; transform: translateX(-100%); }
.panel.open { transform: translateX(0); }
```

FLIP covers the cases where you genuinely need a geometry change: measure First
and Last positions, apply an Invert transform, then Play by transitioning it away
— the visible motion is pure transform even though layout changed once.

### Layer Promotion and Its Cost

```css
/* Promote just before the interaction, release afterwards. */
.sheet { transition: transform 200ms; }
.sheet-container:hover .sheet { will-change: transform; }
```

A composited layer costs GPU memory on the order of `width × height × 4` bytes.
A full-screen layer at 1440×900 is roughly 5 MB; applying `will-change` to 200
list items is hundreds of megabytes and regresses worse than the problem it was
meant to fix. Treat it as a short-lived hint, never a permanent property in a
base class — removing it after the animation lets the browser discard the layer.

### Containment

`contain` tells the browser that a subtree's effects do not escape, letting it
skip work outside: `.widget { contain: layout style paint; }` keeps geometry,
counters, and paint inside the widget.

For long lists, `content-visibility` is the bigger lever:

```css
.feed-item {
  content-visibility: auto;
  contain-intrinsic-size: auto 320px;
}
```

Off-screen items skip layout, paint, and hit-testing entirely, rendering lazily as
they approach the viewport. `contain-intrinsic-size` supplies a placeholder height
so the scrollbar and page height stay stable — omit it and unrendered items
collapse to zero, causing scroll jumps. The `auto` keyword makes the browser
remember each element's last rendered size, so the estimate improves after first
paint.

Note the trade-off: skipped subtrees affect in-page find and anchor scrolling in
ways worth testing against your actual content.

### Layout Thrashing

```js
// ❌ each read after a write forces synchronous layout — O(n) reflows
function grow(elements) {
  elements.forEach((el) => {
    el.style.height = `${el.getBoundingClientRect().height * 1.5}px`;
  });
}

// ✅ one layout for all reads, then all writes
function grow(elements) {
  const heights = elements.map((el) => el.getBoundingClientRect().height);
  requestAnimationFrame(() => {
    elements.forEach((el, i) => { el.style.height = `${heights[i] * 1.5}px`; });
  });
}
```

Layout-forcing reads include `offsetTop/Width/Height`, `clientWidth/Height`,
`scrollTop/Height`, `getBoundingClientRect()`, and `getComputedStyle()`. When a
profile shows "Forced reflow" warnings this pattern is nearly always the cause —
a JS bug dressed up as a CSS problem.

### Delivery: Blocking, Size, and Fonts

CSS in `<head>` is render-blocking by design: the browser will not paint until it
has the styles, to avoid a flash of unstyled content. So the number that matters
is the size of the *critical* stylesheet, not the total.

```html
<!-- critical, inline, small -->
<style>/* above-the-fold rules only */</style>

<!-- everything else, non-blocking -->
<link rel="stylesheet" href="/rest.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="/rest.css"></noscript>
```

Never use `@import` inside a stylesheet: the browser cannot discover the imported
file until it has parsed the importer, which serializes what should be parallel
requests.

Fonts:

```html
<link rel="preload" as="font" type="font/woff2" href="/inter.woff2" crossorigin>
```
```css
@font-face {
  font-family: Inter;
  src: url(/inter.woff2) format("woff2");
  font-display: swap;
  unicode-range: U+0000-00FF;   /* subset — don't ship glyphs you never render */
}
```

`font-display: swap` renders fallback text immediately and swaps when the webfont
arrives; the default (`block`) leaves text invisible for up to about 3 seconds.
Reduce the resulting reflow with a metric-compatible fallback, tuned via
`size-adjust` / `ascent-override` on a local fallback `@font-face`.

### Selectors and Bundle Size

Selector matching is rarely the bottleneck on modern engines — total stylesheet
size and unmatched rules matter more. The exception is a large DOM with frequent
class toggles high in the tree, where `.app .sidebar .item span` forces
re-matching across a wide subtree. Flat single-class selectors (BEM, CSS Modules,
utilities) sidestep this and keep specificity flat too.

Measure unused CSS with the DevTools Coverage panel. Frameworks routinely ship
80%+ unused rules on a given route; route-level CSS splitting is usually a bigger
win than any micro-optimization above.

## Common Anti-Patterns

❌ **Transitioning `width`, `height`, `top`, or `left`** — layout on every frame.
✅ `transform: translate()` / `scale()`, with FLIP where geometry truly changes.

❌ **`will-change` on a base class or every list item** — hundreds of MB of layer
memory, and the browser loses its own optimization heuristics.
✅ Apply on hover/focus just before animating; remove when done.

❌ **`content-visibility: auto` without `contain-intrinsic-size`** — the scrollbar
jumps as items render.
✅ Always pair them with a realistic estimate.

❌ **Reading geometry inside a write loop** — forced synchronous layout per item.
✅ Batch all reads, then all writes, inside `requestAnimationFrame`.

❌ **`@import` in CSS** — serialized network requests, delayed first paint.
✅ Multiple `<link>` tags or a bundler.

❌ **One giant stylesheet for every route** — the homepage blocks on the admin
panel's CSS.
✅ Critical CSS inlined, the rest split per route and loaded non-blocking.

❌ **Default `font-display`** — invisible text during load, read as a broken page.
✅ `swap`, plus preload and subsetting for above-the-fold fonts.

❌ **Optimizing selectors before measuring** — usually noise next to bundle size.
✅ Profile first; fix the layout and paint costs the profile actually shows.

## CSS Performance Checklist

- [ ] Animations restricted to `transform` and `opacity`
- [ ] FLIP used where geometry genuinely changes
- [ ] `will-change` applied transiently, never in base styles
- [ ] Long lists use `content-visibility: auto` with `contain-intrinsic-size`
- [ ] `contain` applied to independent widgets
- [ ] DOM reads batched separately from writes
- [ ] No "Forced reflow" warnings in the performance profile
- [ ] Critical CSS inlined; remaining sheets non-blocking
- [ ] No `@import` inside stylesheets
- [ ] CSS split per route, with unused-rule coverage measured
- [ ] `font-display: swap` on all webfonts
- [ ] Above-the-fold font preloaded with `crossorigin`; subset via `unicode-range`
- [ ] Deep descendant selectors avoided in hot subtrees
- [ ] `prefers-reduced-motion` honored for non-essential animation
- [ ] Frame timing verified on a mid-range device, not a dev laptop
