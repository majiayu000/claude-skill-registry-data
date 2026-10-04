---
name: animation
description: Add scroll animations, micro-interactions, or page transitions to a component using GSAP. Use when a section needs motion design or interactive polish.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Add animation/interaction to a component or section.

Target: $ARGUMENTS

## Before Starting

1. Read the target component to understand its structure
2. Check if GSAP is already imported/used in the file or nearby components
3. Read `src/app/globals.css` for any existing animation tokens or keyframes

## Animation Recipes

Choose the appropriate pattern based on what's needed:

### Scroll Reveal (most common)
```tsx
// Staggered fade-up entrance
useGSAP(() => {
  gsap.from('.reveal-item', {
    y: 20,
    opacity: 0,
    duration: 0.6,
    stagger: 0.1,
    ease: 'power2.out',
    scrollTrigger: {
      trigger: containerRef.current,
      start: 'top 80%',
    },
  });
}, { scope: containerRef });
```

### Card Hover (use Tailwind when possible)
```
hover:-translate-y-0.5 hover:shadow-lg transition-all duration-200
```
Only use GSAP for complex hover effects (tilt, glow, border beam).

### Page/Route Transitions
Coordinate with Next.js App Router. Use layout-level animation wrappers, not per-page.

### Loading States
Use shadcn Skeleton component. Only add shimmer via CSS keyframes if the default isn't sufficient.

### Hero Animations
- Text reveal: Split text, stagger character/word entrance
- Background: Subtle parallax or gradient shift (60s+ cycle for gradients)
- CTA: Delayed entrance (300-500ms after hero text)

## Implementation Rules

- ALWAYS wrap in `prefers-reduced-motion` check:
  ```tsx
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) return; // skip all animations
  ```
- Use `useGSAP` hook (not raw useEffect + gsap) for proper cleanup
- Only animate `transform` and `opacity` — never width, height, top, left
- Durations: micro-interactions 150-300ms, scroll reveals 400-600ms, page transitions 200-300ms
- Easing: `power2.out` for entrances, `power2.inOut` for transitions
- Debounce/throttle any scroll-linked animations
- Test on low-end devices — if janky, simplify or remove
- If the component is a Server Component, it needs "use client" to use GSAP. Consider extracting the animated part into a client child component instead of converting the whole page.
- Maximum simultaneous animations: 3-4 elements. More causes jank.

## Anti-Patterns

- No animations on page load that delay content visibility
- No infinite animations except subtle background effects
- No bounce/elastic easing on UI elements (feels cheap)
- No animation that moves content the user is trying to read
- No GSAP for things Tailwind `transition-*` can handle
