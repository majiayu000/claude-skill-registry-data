---
name: responsive-helper
description: Responsive design assistance including breakpoint generation, fluid typography, container queries, and mobile-first/desktop-first strategy guidance. Use when creating responsive layouts or adapting designs for multiple screen sizes.
allowed-tools: Read, Write, Edit
---

# Responsive Helper Skill

This skill helps you create responsive designs that work beautifully across all devices. I'll guide you through responsive patterns, breakpoint strategies, and modern techniques like container queries and fluid typography.

## What I Can Help With

### Breakpoint Design
- Define appropriate breakpoints
- Mobile-first vs desktop-first strategies
- Custom breakpoint systems
- Content-based breakpoints

### Fluid Typography
- Responsive font sizing with clamp()
- Modular scale systems
- Viewport-based sizing
- Accessible responsive text

### Container Queries
- Component-responsive layouts
- Container-based breakpoints
- Intrinsic responsive design
- Container query units

### Responsive Patterns
- Grid systems
- Navigation patterns
- Image handling
- Table responsiveness
- Form layouts

## Standard Breakpoint System

### Common Device Breakpoints
```css
/* Mobile-first approach (recommended) */
/* Base styles: Mobile (< 640px) */

@media (min-width: 640px) {
  /* Small tablet / Large phone (sm) */
}

@media (min-width: 768px) {
  /* Tablet (md) */
}

@media (min-width: 1024px) {
  /* Desktop (lg) */
}

@media (min-width: 1280px) {
  /* Large desktop (xl) */
}

@media (min-width: 1536px) {
  /* Extra large desktop (2xl) */
}
```

### Custom Property Breakpoints
```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Can't use in media queries directly, but useful for JavaScript */
```

## Mobile-First vs Desktop-First

### Mobile-First (Recommended)
```css
/* Base: Mobile styles (< 640px) */
.container {
  padding: 1rem;
  font-size: 1rem;
}

.grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Add complexity as screen grows */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    font-size: 1.125rem;
  }

  .grid {
    flex-direction: row;
    gap: 2rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 3rem;
    font-size: 1.25rem;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3rem;
  }
}
```

### Desktop-First
```css
/* Base: Desktop styles (> 1024px) */
.container {
  padding: 3rem;
  font-size: 1.25rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3rem;
}

/* Simplify as screen shrinks */
@media (max-width: 1024px) {
  .container {
    padding: 2rem;
    font-size: 1.125rem;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
    font-size: 1rem;
  }

  .grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
}
```

## Fluid Typography

### Using clamp()
```css
/* Modern fluid typography */
.heading-1 {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
  /* Min: 2rem (32px)
   * Preferred: 5% of viewport + 1rem
   * Max: 4rem (64px)
   */
}

.heading-2 {
  font-size: clamp(1.5rem, 4vw + 0.5rem, 3rem);
}

.body {
  font-size: clamp(1rem, 2vw + 0.5rem, 1.25rem);
}
```

### Fluid Scale System
```css
:root {
  /* Fluid type scale */
  --font-size-xs: clamp(0.75rem, 1.5vw, 0.875rem);
  --font-size-sm: clamp(0.875rem, 2vw, 1rem);
  --font-size-base: clamp(1rem, 2.5vw, 1.125rem);
  --font-size-lg: clamp(1.125rem, 3vw, 1.5rem);
  --font-size-xl: clamp(1.25rem, 4vw, 2rem);
  --font-size-2xl: clamp(1.5rem, 5vw, 3rem);
  --font-size-3xl: clamp(2rem, 6vw, 4rem);

  /* Fluid spacing */
  --spacing-xs: clamp(0.5rem, 2vw, 1rem);
  --spacing-sm: clamp(0.75rem, 3vw, 1.5rem);
  --spacing-md: clamp(1rem, 4vw, 2rem);
  --spacing-lg: clamp(1.5rem, 5vw, 3rem);
  --spacing-xl: clamp(2rem, 6vw, 4rem);
}
```

### Viewport Units
```css
/* Using viewport units */
.hero-title {
  font-size: 8vw;  /* Scales with viewport width */
}

/* With constraints */
.hero-title {
  font-size: min(8vw, 5rem);  /* Max 5rem */
  font-size: max(8vw, 2rem);  /* Min 2rem */
}
```

## Container Queries

### Basic Container Query
```css
/* Define container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query the container, not viewport */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 200px 1fr;
  }
}
```

### Container Query Units
```css
.card-container {
  container-type: inline-size;
}

.card-title {
  /* 5% of container width */
  font-size: clamp(1rem, 5cqi, 2rem);
}

.card-padding {
  /* 2% of container width */
  padding: 2cqi;
}

/* Container query units:
 * cqi: inline size (width in horizontal writing)
 * cqb: block size (height in horizontal writing)
 * cqw: container width
 * cqh: container height
 * cqmin: min(cqi, cqb)
 * cqmax: max(cqi, cqb)
 */
```

### Responsive Component Pattern
```css
/* Component is responsive to its container, not viewport */
.sidebar-container,
.main-container {
  container-type: inline-size;
}

/* Works in sidebar (narrow) and main (wide) */
.widget {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@container (min-width: 400px) {
  .widget {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 2rem;
  }
}
```

## Responsive Layout Patterns

### Responsive Grid (No Media Queries)
```css
/* Auto-responsive grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

/* With breakout */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
  gap: 1rem;
}
```

### Responsive Sidebar
```css
/* Sidebar that switches to column layout */
.layout {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.sidebar {
  flex: 1 1 300px;
}

.main {
  flex: 3 1 600px;
}

/* Or with Grid */
.layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
```

### Responsive Navigation
```css
/* Horizontal on desktop, vertical on mobile */
.nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

@media (min-width: 768px) {
  .nav {
    flex-direction: row;
    gap: 2rem;
  }
}

/* Hamburger menu on mobile */
.nav-toggle {
  display: block;
}

.nav-menu {
  display: none;
}

.nav-menu.open {
  display: flex;
  flex-direction: column;
}

@media (min-width: 768px) {
  .nav-toggle {
    display: none;
  }

  .nav-menu {
    display: flex;
    flex-direction: row;
  }
}
```

### Responsive Images
```css
/* Fluid images */
img {
  max-width: 100%;
  height: auto;
}

/* Responsive background images */
.hero {
  background-image: url('hero-small.jpg');
  background-size: cover;
  background-position: center;
}

@media (min-width: 768px) {
  .hero {
    background-image: url('hero-medium.jpg');
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('hero-large.jpg');
  }
}

/* Or use picture element with CSS */
.responsive-img {
  width: 100%;
  height: auto;
  object-fit: cover;
}
```

### Responsive Tables
```css
/* Stacked on mobile */
@media (max-width: 640px) {
  table, thead, tbody, th, td, tr {
    display: block;
  }

  thead tr {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }

  tr {
    margin-bottom: 1rem;
    border: 1px solid #ddd;
  }

  td {
    border: none;
    position: relative;
    padding-left: 50%;
  }

  td::before {
    content: attr(data-label);
    position: absolute;
    left: 6px;
    font-weight: bold;
  }
}
```

## Useful Media Query Features

### Orientation
```css
@media (orientation: landscape) {
  .content {
    flex-direction: row;
  }
}

@media (orientation: portrait) {
  .content {
    flex-direction: column;
  }
}
```

### Hover Capability
```css
/* Only add hover effects on devices that support hover */
@media (hover: hover) {
  .button:hover {
    background: #0056b3;
    transform: translateY(-2px);
  }
}

/* For touch devices */
@media (hover: none) {
  .button:active {
    background: #0056b3;
  }
}
```

### Aspect Ratio
```css
/* For wide screens */
@media (min-aspect-ratio: 16/9) {
  .video-container {
    max-width: 1200px;
  }
}
```

### Color Scheme
```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1a;
    --text: #ffffff;
  }
}
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Responsive Units

```css
/* Viewport units */
.full-height {
  height: 100vh;      /* 100% of viewport height */
  height: 100dvh;     /* Dynamic viewport height (accounts for mobile browsers) */
}

.full-width {
  width: 100vw;       /* 100% of viewport width */
}

.responsive-text {
  font-size: 5vw;     /* 5% of viewport width */
  font-size: 5vh;     /* 5% of viewport height */
  font-size: 5vmin;   /* 5% of smaller dimension */
  font-size: 5vmax;   /* 5% of larger dimension */
}

/* Relative units */
.text {
  font-size: 1rem;    /* Relative to root font size */
  padding: 1em;       /* Relative to element's font size */
}

/* Percentage */
.container {
  width: 100%;        /* 100% of parent width */
  max-width: 1200px;
}
```

## Best Practices

### ✓ Do
- Use mobile-first approach (min-width queries)
- Design content-based breakpoints
- Use relative units (rem, em, %)
- Test on real devices
- Use container queries for components
- Provide fluid typography
- Optimize images for different sizes
- Consider touch target sizes (44px min)

### ❌ Don't
- Use fixed pixel widths everywhere
- Design for specific devices
- Ignore content at breakpoint edges
- Use too many breakpoints
- Forget about landscape orientation
- Hide content on mobile (if important)
- Use horizontal scroll
- Rely only on viewport units

## Complete Responsive Example

```css
/* Responsive card component */
.card-container {
  container-type: inline-size;
  width: 100%;
}

.card {
  /* Mobile: vertical layout */
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border-radius: 0.25rem;
}

.card-title {
  font-size: clamp(1.25rem, 4cqi, 1.75rem);
  line-height: 1.2;
}

.card-description {
  font-size: clamp(0.875rem, 3cqi, 1rem);
  line-height: 1.5;
  color: #666;
}

/* Container query: horizontal layout when space allows */
@container (min-width: 500px) {
  .card {
    flex-direction: row;
    gap: 1.5rem;
  }

  .card-image {
    width: 200px;
    flex-shrink: 0;
  }

  .card-content {
    flex: 1;
  }
}

/* Viewport query: increase padding on larger screens */
@media (min-width: 1024px) {
  .card {
    padding: 1.5rem;
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
}
```

## Just Ask!

Tell me what responsive behavior you need:
- "Make this layout responsive"
- "Create mobile navigation"
- "Add fluid typography"
- "Use container queries"
- "Design breakpoint system"
- "Make table responsive"

I'll help you create responsive designs that work everywhere!
