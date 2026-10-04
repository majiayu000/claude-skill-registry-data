---
name: fix-web-rendering-performance
description:
  Audit and fix web rendering performance, including animations, scrolling, layout thrashing, and expensive visual
  effects. Use for janky interactions or costly CSS rendering, such as repeated background blur, backdrop filters, and
  shadows in lists or grids, even when those effects are not animated.
---

# Fix Web Rendering Performance

Diagnose and reduce expensive layout, paint, raster, and compositing work in web interfaces, including animations and
static visual effects repeated across scrolling lists or grids.

## how to use

- `/fix-web-rendering-performance` Apply these guidelines to web rendering, visual effects, and animation work in this
  conversation.

- `/fix-web-rendering-performance <file>` Review the file against the relevant guidance below and report:
  - violations (quote the exact line or snippet)
  - why it matters (one short sentence)
  - a concrete fix (code-level suggestion)

Do not migrate animation libraries unless explicitly requested. Apply rules within the existing stack.

Treat rendering guidance as performance heuristics. A CSS property can identify a risk, but a runtime profile is needed
to establish a bottleneck and verify an improvement.

## when to apply

Reference these guidelines when:

- adding or changing UI animations (CSS, WAAPI, Motion, rAF, GSAP)
- refactoring janky interactions or transitions
- implementing scroll-linked motion or reveal-on-scroll
- animating layout, filters, masks, gradients, or CSS variables
- reviewing components that use will-change, transforms, or measurement
- reviewing scrolling lists or grids with repeated filters, shadows, blur, or backdrop effects, including virtualized
  lists

## rendering steps glossary

- composite candidates: transform and opacity; verify actual layer behavior
- paint/raster: changing colors, borders, gradients, masks, images, or shadows can require redrawing pixels
- filters: filter and backdrop-filter costs depend on the effect, affected pixels, and browser acceleration
- layout: changes to size, position, or flow can require recalculating geometry

## rule categories by priority

| priority | category             | impact      |
| -------- | -------------------- | ----------- |
| 1        | never patterns       | critical    |
| 2        | choose the mechanism | critical    |
| 3        | measurement          | high        |
| 4        | scroll               | high        |
| 5        | paint                | medium-high |
| 6        | layers               | medium      |
| 7        | repeated effects     | medium-high |
| 8        | view transitions     | low         |
| 9        | tool boundaries      | critical    |

## quick reference

### 1. never patterns (critical)

- do not interleave layout reads and writes in the same frame
- do not animate layout continuously on large or meaningful surfaces
- do not drive animation from scrollTop, scrollY, or scroll events
- no requestAnimationFrame loops without a stop condition
- do not mix multiple animation systems that each measure or mutate layout

### 2. choose the mechanism (critical)

- default to transform and opacity for motion
- use JS-driven animation only when interaction requires it
- paint or layout animation is acceptable only on small, isolated surfaces
- one-shot effects are acceptable more often than continuous motion
- prefer downgrading technique over removing motion entirely

### 3. measurement (high)

- measure once, then animate via transform or opacity
- batch all DOM reads before writes
- do not read layout repeatedly during an animation
- prefer FLIP-style transitions for layout-like effects
- prefer approaches that batch measurement and writes
- profile realistic scrolling and animation on target browsers and devices; inspect frame times, dropped frames,
  paint/raster work, and compositing alongside JavaScript and framework render timings

### 4. scroll (high)

- prefer Scroll or View Timelines for scroll-linked motion when available
- use IntersectionObserver for visibility and pausing
- do not poll scroll position for animation
- pause or stop animations when off-screen
- scroll-linked motion must not trigger continuous layout or paint on large surfaces

### 5. paint (medium-high)

- paint-triggering animation is allowed only on small, isolated elements
- do not animate paint-heavy properties on large containers
- do not animate CSS variables for transform, opacity, or position
- do not animate inherited CSS variables
- scope animated CSS variables locally and avoid inheritance

### 6. layers (medium)

- compositor motion requires layer promotion, never assume it
- use will-change temporarily and surgically
- avoid many or large promoted layers
- avoid applying will-change to every list row; layer promotion does not eliminate an effect's rendering cost
- validate layer behavior with tooling when performance matters

### 7. blur, shadows, and repeated effects (medium-high)

Blur and blurred shadows can cost more to render than simple fills. The cost varies with the filter, radius, affected
area, browser, and device. See [CSS filter performance](https://web.dev/articles/understanding-css) and
[paint profiling guidance](https://web.dev/articles/animations-guide).

- assess repeated filter, backdrop-filter, blurred box-shadow, and drop-shadow effects across the rendered list or grid;
  many individually small effects can become a substantial aggregate workload
- virtualization normally reduces work by limiting rendered items; it does not remove the cost of effects on those
  items. Include visible rows, overscan, and newly entering rows in measurements, and tune overscan to avoid both
  excessive work and blank flashes. See
  [list virtualization guidance](https://web.dev/articles/virtualize-long-lists-react-window#overscanning)
- profile backdrop-filter while content behind it scrolls or animates, even if the filter value is static; the filtered
  input changes with the backdrop. See the
  [Filter Effects draft rendering model](https://drafts.csswg.org/filter-effects-2/) and
  [backdrop-filter guidance](https://web.dev/articles/backdrop-filter#basics)
- distinguish animating filter or shadow parameters from moving an item whose static rendering can be reused; evaluate
  the [rendering pipeline](https://web.dev/articles/animations-overview) before calling either a bottleneck
- prefer smaller affected areas, fewer shadow layers, and simpler fills or borders when repeated decoration is a
  measured bottleneck; preserve meaningful focus and state indicators
- prefer transform and opacity when they convey the intended motion; keep necessary blur animations brief and localized,
  and profile continuous or large-area effects explicitly
- do not prescribe a universal safe blur radius such as 8px; choose limits from measurements of the actual workload

### 8. view transitions (low)

- use view transitions only for navigation-level changes
- avoid view transitions for interaction-heavy UI
- avoid view transitions when interruption or cancellation is required
- treat size changes as potentially layout-triggering

### 9. tool boundaries (critical)

- do not migrate or rewrite animation libraries unless explicitly requested
- apply these rules within the existing animation system
- never partially migrate APIs or mix styles within the same component

## common fixes

```css
/* layout thrashing: animate transform instead of width */
/* before */
.panel {
  transition: width 0.3s;
}
/* after */
.panel {
  transition: transform 0.3s;
}

/* scroll-linked: use scroll-timeline instead of JS */
/* before */
window.addEventListener('scroll', () => el.style.opacity = scrollY / 500)
/* after */  .reveal {
  animation: fade-in linear;
  animation-timeline: view();
}
```

```js
// measurement: batch reads before writes (FLIP)
// before: layout thrash
el.style.left = el.getBoundingClientRect().left + 10 + "px"
// after: measure once, animate via transform
const first = el.getBoundingClientRect()
el.classList.add("moved")
const last = el.getBoundingClientRect()
el.style.transform = `translateX(${first.left - last.left}px)`
requestAnimationFrame(() => {
  el.style.transition = "transform 0.3s"
  el.style.transform = ""
})
```

## review guidance

- enforce critical rules first (never patterns, tool boundaries)
- choose the least expensive rendering work that matches the intent
- for any non-default choice, state the constraint that justifies it (surface size, duration, or interaction
  requirement)
- when reviewing, prefer actionable notes and concrete alternatives over theory
- verify suspected effect costs by comparing the same interaction with effects enabled and simplified or disabled;
  report the browser/device, rendered item count including overscan, and observed frame/rendering changes
- label findings from source inspection as potential hotspots until profiling confirms their impact
