---
allowed-tools: Read, Write, Edit
description: 'Build performant, accessible, mobile-first web applications.

  Use when implementing responsive layouts, touch interactions, or optimizing for
  mobile devices.

  Covers modern CSS techniques, accessibility requirements, and Core Web Vitals optimization.'
name: mobile-responsive
---

# Mobile-First Responsive Design

Build performant, accessible web applications that work across all devices.

## Strategy: Mobile-First

Start with mobile styles as the default, then progressively enhance for larger screens. This approach:

- Prioritizes the most constrained environment first
- Results in cleaner, more maintainable CSS
- Aligns with how CSS cascade naturally works
- Matches Google's mobile-first indexing

```css
/* Base styles = mobile (no media query needed) */
.card {
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

/* Enhance for larger screens */
@media (min-width: 768px) {
  .card {
    flex-direction: row;
    padding: 1.5rem;
  }
}
```

## Media Queries vs Container Queries

Choose based on what should drive the layout change:

| Use Case | Approach |
|----------|----------|
| Page-level layout (sidebar, columns) | Media queries |
| Component-level adaptation (cards, widgets) | Container queries |
| Both page and component concerns | Combine both |

### Media Queries (Viewport-Based)

```css
/* Standard breakpoints */
@media (min-width: 640px) { /* sm: Large phones */ }
@media (min-width: 768px) { /* md: Tablets */ }
@media (min-width: 1024px) { /* lg: Laptops */ }
@media (min-width: 1280px) { /* xl: Desktops */ }
@media (min-width: 1536px) { /* 2xl: Large monitors */ }
```

### Container Queries (Parent-Based)

Container queries let components adapt to their container's size, not the viewport. This makes components truly portable.

```css
/* Define a containment context */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query the container's width */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}

@container card (min-width: 600px) {
  .card {
    gap: 2rem;
  }
}
```

**When to use container queries:**
- Reusable components that appear in different layouts
- Sidebar widgets that collapse/expand
- Cards in grid layouts with varying column widths
- Any component where parent size varies independently of viewport

## Fluid Design Techniques

### Fluid Typography

Scale text smoothly between minimum and maximum sizes:

```css
:root {
  /* clamp(minimum, preferred, maximum) */
  --text-sm: clamp(0.875rem, 0.8rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.4vw, 1.125rem);
  --text-lg: clamp(1.25rem, 1rem + 0.75vw, 1.5rem);
  --text-xl: clamp(1.5rem, 1.2rem + 1.25vw, 2rem);
  --text-2xl: clamp(2rem, 1.5rem + 2vw, 3rem);
  --text-3xl: clamp(2.5rem, 1.75rem + 3vw, 4rem);
}
```

### Fluid Spacing

```css
:root {
  --space-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --space-sm: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-md: clamp(1rem, 0.8rem + 0.75vw, 1.5rem);
  --space-lg: clamp(1.5rem, 1rem + 1.5vw, 2.5rem);
  --space-xl: clamp(2rem, 1.5rem + 2vw, 4rem);
}
```

### Responsive Images

Serve appropriately sized images for each device:

```html
<picture>
  <!-- Modern formats first -->
  <source
    type="image/avif"
    srcset="image-400.avif 400w, image-800.avif 800w, image-1200.avif 1200w"
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  />
  <source
    type="image/webp"
    srcset="image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w"
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  />
  <!-- Fallback -->
  <img
    src="image-800.jpg"
    alt="Description"
    loading="lazy"
    decoding="async"
    width="800"
    height="600"
  />
</picture>
```

**Key attributes:**
- `srcset`: Multiple image sizes for browser to choose
- `sizes`: Hints about rendered size at each breakpoint
- `loading="lazy"`: Defer off-screen images
- `width` & `height`: Prevent layout shift (CLS)

## Touch Accessibility

### Minimum Touch Target Sizes

WCAG 2.2 requires interactive elements to be easily tappable:

| Level | Minimum Size | Use For |
|-------|--------------|---------|
| AA (Required) | 24×24 CSS px | Inline links, small icons |
| Best Practice | 44×44 CSS px | Buttons, nav items, form controls |
| AAA (Enhanced) | 48×48 CSS px | Primary actions, accessibility-first apps |

```css
/* Ensure minimum touch target */
.button {
  min-width: 44px;
  min-height: 44px;
  padding: 0.75rem 1rem;
}

/* Expand tap area without changing visual size */
.icon-button {
  position: relative;
  width: 24px;
  height: 24px;
}

.icon-button::before {
  content: '';
  position: absolute;
  inset: -10px; /* Expands clickable area */
}
```

### Touch Target Spacing

Ensure adequate spacing between targets to prevent accidental taps:

```css
.nav-list {
  display: flex;
  gap: 0.5rem; /* Minimum 8px between targets */
}

.nav-link {
  padding: 0.75rem 1rem;
}
```

## Device-Specific Considerations

### Safe Areas (Notch, Dynamic Island, Home Indicator)

Account for device-specific screen cutouts:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

```css
.page {
  /* Standard padding + safe area */
  padding-left: max(1rem, env(safe-area-inset-left));
  padding-right: max(1rem, env(safe-area-inset-right));
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding-bottom: max(0.5rem, env(safe-area-inset-bottom));
}

.header {
  padding-top: max(1rem, env(safe-area-inset-top));
}
```

### Orientation Handling

```css
/* Portrait-specific styles */
@media (orientation: portrait) {
  .hero {
    min-height: 60vh;
  }
}

/* Landscape-specific styles */
@media (orientation: landscape) {
  .hero {
    min-height: 80vh;
  }
}
```

### High DPI Displays

```css
/* Target retina/high-DPI displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .logo {
    background-image: url('logo@2x.png');
    background-size: 100px 50px;
  }
}
```

## Performance: Core Web Vitals

Mobile performance directly impacts user experience and SEO.

### Target Thresholds

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | ≤4s | >4s |
| INP (Interaction to Next Paint) | ≤200ms | ≤500ms | >500ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | ≤0.25 | >0.25 |

### Preventing Layout Shift (CLS)

```css
/* Always set dimensions on media */
img, video, iframe {
  max-width: 100%;
  height: auto;
}

/* Reserve space with aspect-ratio */
.video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

/* Prevent font swap shift */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;
  size-adjust: 100%;
}
```

### Improving LCP

```html
<!-- Preload critical hero image -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">

<!-- Inline critical CSS -->
<style>
  /* Above-the-fold styles only */
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

### Improving INP

```javascript
// Break up long tasks
async function processLargeDataset(items) {
  for (const chunk of chunkArray(items, 100)) {
    await new Promise(resolve => setTimeout(resolve, 0)); // Yield to main thread
    processChunk(chunk);
  }
}

// Use passive event listeners for scroll/touch
element.addEventListener('scroll', handler, { passive: true });
element.addEventListener('touchstart', handler, { passive: true });
```

## Common Patterns

### Responsive Grid

```css
.grid {
  display: grid;
  gap: var(--space-md);
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
}
```

### Mobile Navigation

```css
.nav {
  /* Mobile: bottom sheet or hamburger */
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
}

@media (min-width: 768px) {
  .nav {
    /* Desktop: horizontal bar */
    position: static;
    display: flex;
    gap: 1rem;
  }
}
```

### Collapsible Sidebar

```css
.layout {
  display: grid;
  grid-template-columns: 1fr;
}

@media (min-width: 1024px) {
  .layout {
    grid-template-columns: 250px 1fr;
  }
}
```

## Testing Checklist

- [ ] Test on real devices, not just browser DevTools
- [ ] Check both portrait and landscape orientations
- [ ] Verify touch targets are ≥44px for primary actions
- [ ] Test with slow 3G throttling enabled
- [ ] Run Lighthouse mobile audit
- [ ] Check CLS by watching for layout jumps during load
- [ ] Test with screen readers (VoiceOver, TalkBack)
- [ ] Verify safe area handling on notched devices

## Anti-Patterns to Avoid

| Problem | Better Approach |
|---------|-----------------|
| Desktop-first CSS | Start mobile, enhance up |
| `max-width` media queries | Use `min-width` for mobile-first |
| Fixed pixel breakpoints per device | Use content-based breakpoints |
| Hiding content on mobile | Prioritize and reflow instead |
| Horizontal scroll on mobile | Ensure content fits viewport |
| Tiny touch targets | Minimum 44×44px for buttons |
| Missing image dimensions | Always set width/height |
| Blocking scripts in `<head>` | Defer or async non-critical JS |
