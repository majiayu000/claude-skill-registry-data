---
name: lenis
description: Use when implementing Lenis smooth scroll or integrating Lenis with GSAP ScrollTrigger. Applies Lenis best practices for setup and performance.
version: "1.2.0"
---

# Lenis Smooth Scroll Best Practices

Apply when implementing Lenis smooth scrolling.

**Documentation:** https://lenis.darkroom.engineering/

## Required CSS

Always include this CSS for proper functionality:

```css
html.lenis, html.lenis body {
  height: auto;
}

.lenis.lenis-smooth {
  scroll-behavior: auto !important;
}

.lenis.lenis-smooth [data-lenis-prevent] {
  overscroll-behavior: contain;
}

.lenis.lenis-stopped {
  overflow: hidden;
}

.lenis.lenis-scrolling iframe {
  pointer-events: none;
}
```

## Basic Setup

### Standalone (Simple)
```javascript
import Lenis from 'lenis';

const lenis = new Lenis({
  autoRaf: true,  // Uses built-in RAF loop
});
```

### With GSAP ScrollTrigger (Recommended)
```javascript
import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

let lenisInstance: Lenis | null = null;
let tickerCallback: ((time: number) => void) | null = null;

function init() {
  lenisInstance = new Lenis();

  // Sync Lenis scroll position with ScrollTrigger
  lenisInstance.on('scroll', ScrollTrigger.update);

  // Store callback reference for cleanup
  tickerCallback = (time) => lenisInstance?.raf(time * 1000);
  gsap.ticker.add(tickerCallback);

  // Disable GSAP lag smoothing for precise sync
  gsap.ticker.lagSmoothing(0);
}

function destroy() {
  // Remove ticker callback first (prevents memory leak!)
  if (tickerCallback) {
    gsap.ticker.remove(tickerCallback);
    tickerCallback = null;
  }

  if (lenisInstance) {
    lenisInstance.destroy();
    lenisInstance = null;
  }
}
```

**Critical:** Store the ticker callback reference. Without `gsap.ticker.remove()`, callbacks accumulate on each init, causing memory leaks and performance issues.

## Configuration Options

```javascript
const lenis = new Lenis({
  duration: 1.2,              // Scroll animation duration
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // Ease out expo
  orientation: 'vertical',    // or 'horizontal'
  gestureOrientation: 'vertical',
  smoothWheel: true,          // Smooth wheel scrolling
  syncTouch: false,           // Don't smooth touch (usually unwanted)
  touchMultiplier: 2,         // Touch scroll speed
});
```

### Recommended Defaults
- `duration: 1.2` — Smooth but responsive
- `smoothWheel: true` — Essential for smooth feel
- `syncTouch: false` — Native touch usually better

## Preventing Scroll on Elements

```html
<!-- Prevent Lenis on scrollable containers -->
<div data-lenis-prevent>
  <div class="scrollable-content">
    <!-- This scrolls normally, Lenis ignores it -->
  </div>
</div>

<!-- Prevent only wheel events -->
<div data-lenis-prevent-wheel>
  <!-- Touch still uses Lenis -->
</div>

<!-- Prevent only touch events -->
<div data-lenis-prevent-touch>
  <!-- Wheel still uses Lenis -->
</div>
```

## Scroll Methods

```javascript
// Scroll to element
lenis.scrollTo('#section', {
  offset: -100,           // Offset from target
  duration: 2,            // Override default duration
  easing: (t) => t,       // Custom easing
  immediate: false,       // Skip animation
  lock: true,             // Prevent user scroll during animation
});

// Scroll to position
lenis.scrollTo(500);      // Scroll to 500px
lenis.scrollTo('top');    // Scroll to top
lenis.scrollTo('bottom'); // Scroll to bottom

// Control
lenis.stop();             // Pause scrolling
lenis.start();            // Resume scrolling
```

## Event Handling

```javascript
lenis.on('scroll', ({ scroll, velocity, direction, progress }) => {
  // scroll: current scroll position
  // velocity: scroll speed
  // direction: 1 (down) or -1 (up)
  // progress: 0-1 scroll progress
});
```

## Cleanup

```javascript
// On component unmount:
lenis.destroy();
```

## Known Limitations

1. **Iframes** — Smooth scroll stops over iframes (they don't forward wheel events)
2. **Safari pre-M1** — `position: fixed` may lag slightly
3. **Nested scroll containers** — Use `data-lenis-prevent` on them
4. **Browser smooth scroll** — Disable any built-in smooth scrolling

## Troubleshooting

### Scroll not smooth
- Check required CSS is included
- Verify `autoRaf: true` or GSAP ticker integration
- Check for conflicting scroll libraries

### ScrollTrigger not syncing
- Ensure `lenis.on('scroll', ScrollTrigger.update)` is set
- Call `ScrollTrigger.refresh()` after Lenis init
- Check `gsap.ticker.lagSmoothing(0)` is set

### Elements not receiving scroll
- Check for `data-lenis-prevent` on parent elements
- Verify Lenis is initialized after DOM ready

## Common Patterns

### Anchor Links
```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    e.preventDefault();
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      lenis.scrollTo(target, { offset: -80 });
    }
  });
});
```

### Stop During Modal
```javascript
function openModal() {
  lenis.stop();
  // show modal
}

function closeModal() {
  lenis.start();
  // hide modal
}
```

## Avoid
- Forgetting required CSS (causes jittery scroll)
- Using `syncTouch: true` (native touch is usually better)
- Multiple Lenis instances on the same page
- Forgetting to call `lenis.destroy()` on unmount
- Using both `autoRaf` and GSAP ticker (pick one)
- Missing `ScrollTrigger.update` sync when using GSAP
- Animating scroll position directly (use `lenis.scrollTo()`)
- Setting `duration` too high (>2s feels sluggish)
