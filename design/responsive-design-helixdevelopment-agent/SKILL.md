---
name: responsive-design
description: Implement mobile-first responsive design using modern CSS techniques. Support various screen sizes and devices effectively.
triggers:
- /responsive
- /mobile first
---

# Responsive Web Design

This skill covers implementing mobile-first responsive designs that work effectively across all device sizes using modern CSS techniques.

## When to use this skill

Use this skill when you need to:
- Build responsive layouts
- Implement mobile-first designs
- Create flexible grid systems
- Handle responsive images and typography
- Support various device capabilities

## Prerequisites

- Understanding of CSS fundamentals
- Knowledge of viewport meta tags
- Familiarity with CSS Grid and Flexbox
- Testing devices or browser DevTools

## Guidelines

### Mobile-First Approach

**Philosophy**
- Design for mobile by default
- Progressive enhancement for larger screens
- Content priority drives layout decisions
- Touch-friendly interactions

**Viewport Configuration**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**CSS Strategy**
```css
/* Mobile first: Base styles for mobile */
.card {
  padding: 1rem;
  width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .card {
    padding: 1.5rem;
    width: 50%;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .card {
    padding: 2rem;
    width: 33.333%;
  }
}
```

### Breakpoint Strategy

**Standard Breakpoints**
```css
/* Mobile first breakpoints */
/* Small devices (phones) - default */

/* Medium devices (tablets) */
@media (min-width: 768px) { }

/* Large devices (desktops) */
@media (min-width: 1024px) { }

/* Extra large devices */
@media (min-width: 1280px) { }

/* 4K and ultra-wide */
@media (min-width: 1536px) { }
```

**Content-Based Breakpoints**
- Break when content breaks, not at device widths
- Use relative units (em, rem) for breakpoints
- Test with actual content

```css
/* Break when line length becomes unreadable */
.container {
  max-width: 100%;
  padding: 1rem;
}

@media (min-width: 65ch) {
  .container {
    max-width: 65ch; /* Optimal reading width */
    margin: 0 auto;
  }
}
```

### Layout Techniques

**CSS Grid**
```css
/* Responsive grid */
.grid {
  display: grid;
  gap: 1rem;
  /* Single column by default (mobile) */
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}

/* Responsive without media queries */
.grid-auto {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(100%, 300px), 1fr)
  );
}
```

**Flexbox**
```css
/* Responsive navigation */
.nav {
  display: flex;
  flex-direction: column; /* Mobile: stacked */
  gap: 0.5rem;
}

@media (min-width: 768px) {
  .nav {
    flex-direction: row; /* Desktop: horizontal */
    gap: 2rem;
  }
}

/* Responsive cards */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  flex: 1 1 300px; /* Grow, shrink, basis */
  min-width: 0; /* Allow shrinking below basis */
}
```

### Responsive Typography

**Fluid Typography**
```css
/* Clamp: minimum, preferred, maximum */
h1 {
  font-size: clamp(1.5rem, 4vw + 1rem, 3rem);
}

p {
  font-size: clamp(1rem, 0.5vw + 0.875rem, 1.25rem);
  line-height: 1.6;
}
```

**Responsive Line Height**
```css
body {
  font-size: 1rem;
  line-height: 1.5;
}

@media (min-width: 768px) {
  body {
    font-size: 1.125rem;
    line-height: 1.6;
  }
}
```

### Responsive Images

**Art Direction**
```html
<picture>
  <!-- Mobile: portrait crop -->
  <source 
    media="(max-width: 767px)" 
    srcset="hero-mobile.jpg"
  >
  <!-- Desktop: full image -->
  <source 
    media="(min-width: 768px)" 
    srcset="hero-desktop.jpg"
  >
  <img src="hero-default.jpg" alt="Description">
</picture>
```

**Resolution Switching**
```html
<img 
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="
    (max-width: 600px) 400px,
    (max-width: 1000px) 800px,
    1200px
  "
  src="image-800.jpg"
  alt="Description"
>
```

**Object Fit**
```css
.image-container {
  width: 100%;
  aspect-ratio: 16 / 9;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### Container Queries

**Modern Responsive Alternative**
```css
/* Container query instead of media query */
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (min-width: 700px) {
  .card {
    grid-template-columns: 300px 1fr;
  }
}
```

### Touch and Input Considerations

**Touch Targets**
```css
/* Minimum touch target size */
button, 
.nav-link,
.form-input {
  min-height: 44px;
  min-width: 44px;
}

/* Adequate spacing between touch targets */
.nav-list li {
  margin-bottom: 0.5rem;
}
```

**Hover Capability**
```css
/* Only apply hover styles on hover-capable devices */
@media (hover: hover) {
  .button:hover {
    background-color: #0056b3;
  }
}

/* Fallback for touch devices */
@media (hover: none) {
  .button:active {
    background-color: #0056b3;
  }
}
```

### Dark Mode Support

```css
/* Dark mode media query */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #1a1a1a;
    --text-color: #e0e0e0;
  }
}

/* Respect user preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Testing

**Device Testing Checklist**
- [ ] iPhone (Safari)
- [ ] Android (Chrome)
- [ ] iPad/Tablet
- [ ] Small laptop (1024px)
- [ ] Desktop (1920px)
- [ ] Rotated devices

**Browser DevTools**
- Responsive Design Mode
- Device emulation
- Network throttling
- Touch simulation

## Examples

See the `examples/` directory for:
- `grid-layouts/` - Responsive grid patterns
- `navigation-patterns/` - Responsive nav designs
- `typography-system/` - Fluid type scales
- `dark-mode/` - Dark mode implementation

## References

- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Every Layout](https://every-layout.dev/)
- [Responsive Web Design by Ethan Marcotte](https://alistapart.com/article/responsive-web-design/)
- [Modern CSS Solutions](https://moderncss.dev/)
- [Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries)
