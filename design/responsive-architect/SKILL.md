---
name: responsive-architect
description: Expert in mobile-first responsive design, breakpoint systems, container queries, fluid typography, touch interactions, viewport optimization, and cross-device testing
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Responsive Architect

Expert skill for building mobile-first responsive applications. Specializes in breakpoint systems, container queries, fluid typography, touch interactions, and performance optimization across all devices.

## Core Capabilities

### 1. Mobile-First Design
- **Mobile-First Strategy**: Design for mobile, enhance for desktop
- **Progressive Enhancement**: Core experience works everywhere
- **Breakpoint Strategy**: 320px, 768px, 1024px, 1440px
- **Content Priority**: Most important content first
- **Touch Targets**: Minimum 44×44px hit areas
- **Performance**: Optimize for mobile networks

### 2. Breakpoint Systems
- **CSS Media Queries**: min-width approach
- **Tailwind Breakpoints**: sm, md, lg, xl, 2xl
- **Custom Breakpoints**: Project-specific sizes
- **Container Queries**: Component-level responsiveness
- **Aspect Ratio**: Maintain proportions
- **Orientation**: Portrait vs landscape

### 3. Fluid Typography
- **clamp()**: Min, preferred, max sizing
- **rem/em Units**: Scalable typography
- **Viewport Units**: vw, vh, vmin, vmax
- **Modular Scale**: Consistent type hierarchy
- **Line Height**: Readable text at all sizes
- **Letter Spacing**: Adjust for screen size

### 4. Responsive Layouts
- **CSS Grid**: Two-dimensional layouts
- **Flexbox**: One-dimensional layouts
- **Multi-Column**: Automatic columns
- **Subgrid**: Nested grid alignment
- **CSS Container Queries**: Component responsiveness
- **Intrinsic Sizing**: Content-based sizing

### 5. Touch & Gestures
- **Touch Events**: touchstart, touchmove, touchend
- **Pointer Events**: Unified mouse/touch API
- **Swipe Gestures**: Pan, swipe detection
- **Pinch Zoom**: Multi-touch gestures
- **Tap vs Click**: 300ms delay elimination
- **Hover States**: Touch-friendly alternatives

### 6. Images & Media
- **Responsive Images**: srcset, sizes
- **Art Direction**: Different images per breakpoint
- **Picture Element**: Format selection
- **Lazy Loading**: Native loading="lazy"
- **Aspect Ratio**: aspect-ratio CSS property
- **Video**: Responsive video embeds

### 7. Performance
- **Critical CSS**: Above-the-fold styles
- **Code Splitting**: Load what's needed
- **Image Optimization**: WebP, AVIF formats
- **Prefetching**: Anticipate user actions
- **Service Workers**: Offline support
- **Bundle Size**: Mobile-optimized bundles

## Breakpoint System

```typescript
// breakpoints.ts
export const breakpoints = {
  xs: '320px',   // Small phone
  sm: '640px',   // Large phone
  md: '768px',   // Tablet
  lg: '1024px',  // Laptop
  xl: '1280px',  // Desktop
  '2xl': '1536px', // Large desktop
} as const

export const mediaQueries = {
  xs: `@media (min-width: ${breakpoints.xs})`,
  sm: `@media (min-width: ${breakpoints.sm})`,
  md: `@media (min-width: ${breakpoints.md})`,
  lg: `@media (min-width: ${breakpoints.lg})`,
  xl: `@media (min-width: ${breakpoints.xl})`,
  '2xl': `@media (min-width: ${breakpoints['2xl']})`,
} as const

// CSS-in-JS usage
const styles = {
  container: {
    width: '100%',
    padding: '1rem',

    [mediaQueries.md]: {
      padding: '2rem',
    },

    [mediaQueries.lg]: {
      maxWidth: '1200px',
      margin: '0 auto',
    },
  },
}
```

## Fluid Typography

```css
/* Fluid typography with clamp() */
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
  /* Min: 2rem (32px)
     Preferred: 5vw + 1rem (scales with viewport)
     Max: 4rem (64px) */
}

h2 {
  font-size: clamp(1.5rem, 3vw + 1rem, 3rem);
}

p {
  font-size: clamp(1rem, 2vw + 0.5rem, 1.25rem);
  line-height: 1.6;
}

/* Modular scale */
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.3rem + 1vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.6rem + 1.375vw, 2.5rem);
  --text-4xl: clamp(2.25rem, 1.9rem + 1.75vw, 3rem);
}
```

## Responsive Component

```tsx
// ResponsiveCard.tsx
import { useMediaQuery } from './hooks/useMediaQuery'

export function ResponsiveCard({ children }: { children: React.ReactNode }) {
  const isMobile = useMediaQuery('(max-width: 768px)')
  const isTablet = useMediaQuery('(min-width: 769px) and (max-width: 1024px)')
  const isDesktop = useMediaQuery('(min-width: 1025px)')

  return (
    <div
      className="card"
      style={{
        padding: isMobile ? '1rem' : isTablet ? '1.5rem' : '2rem',
        gridTemplateColumns: isMobile ? '1fr' : isDesktop ? '1fr 1fr' : '1fr',
      }}
    >
      {children}
    </div>
  )
}

// useMediaQuery hook
import { useState, useEffect } from 'react'

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const media = window.matchMedia(query)

    if (media.matches !== matches) {
      setMatches(media.matches)
    }

    const listener = () => setMatches(media.matches)
    media.addEventListener('change', listener)

    return () => media.removeEventListener('change', listener)
  }, [matches, query])

  return matches
}
```

## Container Queries

```css
/* Container query - component responds to its own size */
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: grid;
  gap: 1rem;
}

/* When container is > 400px, use 2 columns */
@container card (min-width: 400px) {
  .card {
    grid-template-columns: 1fr 1fr;
  }
}

/* When container is > 600px, use 3 columns */
@container card (min-width: 600px) {
  .card {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Touch Interactions

```tsx
// SwipeableCard.tsx
import { useState } from 'react'

export function SwipeableCard({ onSwipeLeft, onSwipeRight }: {
  onSwipeLeft?: () => void
  onSwipeRight?: () => void
}) {
  const [touchStart, setTouchStart] = useState(0)
  const [touchEnd, setTouchEnd] = useState(0)

  const minSwipeDistance = 50

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(0)
    setTouchStart(e.targetTouches[0].clientX)
  }

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX)
  }

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return

    const distance = touchStart - touchEnd
    const isLeftSwipe = distance > minSwipeDistance
    const isRightSwipe = distance < -minSwipeDistance

    if (isLeftSwipe && onSwipeLeft) {
      onSwipeLeft()
    }

    if (isRightSwipe && onSwipeRight) {
      onSwipeRight()
    }
  }

  return (
    <div
      onTouchStart={onTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
      className="swipeable-card"
    >
      Swipe me!
    </div>
  )
}
```

## Responsive Images

```tsx
// ResponsiveImage.tsx
export function ResponsiveImage({
  src,
  alt,
  sizes = '100vw',
}: {
  src: string
  alt: string
  sizes?: string
}) {
  return (
    <img
      src={src}
      alt={alt}
      srcSet={`
        ${src}?w=400 400w,
        ${src}?w=800 800w,
        ${src}?w=1200 1200w,
        ${src}?w=1600 1600w
      `}
      sizes={sizes}
      loading="lazy"
      style={{ width: '100%', height: 'auto' }}
    />
  )
}

// Art direction with Picture
export function ArtDirectedImage() {
  return (
    <picture>
      <source media="(min-width: 1024px)" srcSet="desktop.jpg" />
      <source media="(min-width: 768px)" srcSet="tablet.jpg" />
      <img src="mobile.jpg" alt="Responsive image" />
    </picture>
  )
}
```

## Mobile-First CSS

```css
/* ✅ GOOD - Mobile-first (min-width) */
.container {
  padding: 1rem;           /* Mobile default */
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;         /* Tablet and up */
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 3rem;         /* Desktop and up */
  }
}

/* ❌ BAD - Desktop-first (max-width) */
.container {
  padding: 3rem;           /* Desktop default */
}

@media (max-width: 1023px) {
  .container {
    padding: 2rem;         /* Tablet and down */
  }
}

@media (max-width: 767px) {
  .container {
    padding: 1rem;         /* Mobile */
  }
}
```

## Responsive Grid

```css
/* Auto-responsive grid */
.grid {
  display: grid;
  gap: 1rem;

  /* Mobile: 1 column */
  grid-template-columns: 1fr;
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: Auto-fit columns */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}
```

## Performance Optimization

```tsx
// LazyLoad component
import { Suspense, lazy } from 'react'

const DesktopNav = lazy(() => import('./DesktopNav'))
const MobileNav = lazy(() => import('./MobileNav'))

export function ResponsiveNav() {
  const isMobile = useMediaQuery('(max-width: 768px)')

  return (
    <Suspense fallback={<div>Loading...</div>}>
      {isMobile ? <MobileNav /> : <DesktopNav />}
    </Suspense>
  )
}

// Critical CSS extraction
// Load above-the-fold CSS inline
// Defer below-the-fold CSS
```

## Best Practices

### Touch Targets
```css
/* Minimum 44x44px touch targets */
button, a {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}
```

### Viewport Meta
```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

### Hover Alternatives
```css
/* Don't rely on hover for mobile */
@media (hover: hover) {
  .button:hover {
    background: blue;
  }
}

/* Touch-friendly alternative */
.button:active,
.button:focus {
  background: blue;
}
```

## When to Use This Skill

Activate this skill when you need to:
- Build mobile-first responsive layouts
- Implement breakpoint systems
- Create fluid typography
- Add touch gesture support
- Optimize for different screen sizes
- Implement responsive images
- Use container queries
- Test cross-device compatibility
- Improve mobile performance

## Output Format

When creating responsive components, provide:
1. **Mobile-First Component**: Works on all devices
2. **Breakpoint System**: Consistent across project
3. **Fluid Typography**: Scalable text
4. **Touch Support**: Gesture-friendly interactions
5. **Performance Notes**: Optimization strategies
6. **Testing Guide**: Cross-device testing

Always build interfaces that work beautifully on every device, from phones to desktops.
