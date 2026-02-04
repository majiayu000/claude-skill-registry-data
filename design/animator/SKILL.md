---
name: animator
description: Animation and micro-interaction patterns for web interfaces. Use when adding transitions, animations, hover effects, loading states, or any motion to UI components.
---

# Motion Design

Create meaningful, performant animations that enhance user experience.

## Core Principles

### Purpose of Motion
- **Feedback** - Confirm user actions (button press, form submit)
- **Orientation** - Show where elements come from/go to
- **Focus** - Direct attention to important changes
- **Delight** - Add personality without slowing users down

### When NOT to Animate
- User has `prefers-reduced-motion` enabled
- Animation would delay critical actions
- Motion doesn't add meaning
- On low-powered devices

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Timing & Easing

### Duration Guidelines

| Type | Duration | Use Case |
|------|----------|----------|
| Micro | 100-150ms | Button states, toggles, small feedback |
| Standard | 200-300ms | Most UI transitions, modals, dropdowns |
| Complex | 300-500ms | Page transitions, large reveals |
| Emphasis | 500ms+ | Onboarding, celebrations (use sparingly) |

### Easing Functions

```css
/* Natural motion - use for most UI */
--ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);      /* Decelerate */
--ease-in: cubic-bezier(0.4, 0.0, 1, 1);          /* Accelerate */
--ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);   /* Both */

/* Expressive motion - entrances/exits */
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);  /* Overshoot */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);   /* Playful */

/* Quick reference */
ease-out: Elements entering (coming to rest)
ease-in: Elements exiting (accelerating away)
ease-in-out: Elements moving between states
```

### Tailwind Defaults
```html
<!-- Duration -->
duration-75 duration-100 duration-150 duration-200 duration-300 duration-500

<!-- Easing -->
ease-linear ease-in ease-out ease-in-out
```

## Common Patterns

### Button Interactions

```css
.button {
  transition: transform 150ms ease-out,
              box-shadow 150ms ease-out,
              background-color 150ms ease-out;
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.button:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

```tsx
// Tailwind
<button className="transition-all duration-150 ease-out
  hover:-translate-y-0.5 hover:shadow-lg
  active:translate-y-0 active:scale-[0.98]">
  Click me
</button>
```

### Fade & Scale Enter

```css
/* Modal/Dialog entrance */
@keyframes fadeScaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal {
  animation: fadeScaleIn 200ms ease-out;
}
```

### Slide Transitions

```css
/* Slide from bottom */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Slide from side (for drawers) */
@keyframes slideInRight {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}
```

### Staggered List Animation

```tsx
// Framer Motion
<motion.ul>
  {items.map((item, i) => (
    <motion.li
      key={item.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: i * 0.05 }}
    />
  ))}
</motion.ul>
```

```css
/* CSS stagger with animation-delay */
.list-item {
  opacity: 0;
  animation: fadeSlideIn 300ms ease-out forwards;
}

.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 50ms; }
.list-item:nth-child(3) { animation-delay: 100ms; }
/* ... or use CSS custom properties */

.list-item {
  animation-delay: calc(var(--index) * 50ms);
}
```

### Loading States

```css
/* Pulse (skeleton loading) */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton {
  animation: pulse 2s ease-in-out infinite;
}

/* Spinner */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}

/* Progress bar shimmer */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

### Hover Reveals

```css
/* Image zoom on hover */
.image-container {
  overflow: hidden;
}

.image-container img {
  transition: transform 300ms ease-out;
}

.image-container:hover img {
  transform: scale(1.05);
}

/* Underline grow */
.link {
  position: relative;
}

.link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 250ms ease-out;
}

.link:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}
```

## Framer Motion Patterns

### Basic Animation
```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.2, ease: 'easeOut' }}
>
  Content
</motion.div>
```

### Variants for Complex Animations
```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  {items.map((item) => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

### Layout Animations
```tsx
// Animate layout changes automatically
<motion.div layout>
  {isExpanded ? <ExpandedContent /> : <CollapsedContent />}
</motion.div>

// Shared layout animation (element morphing)
<motion.div layoutId="shared-element">
  {/* This element animates between positions */}
</motion.div>
```

### Gestures
```tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: 'spring', stiffness: 400, damping: 17 }}
>
  Press me
</motion.button>
```

### AnimatePresence for Exit Animations
```tsx
import { AnimatePresence, motion } from 'framer-motion';

<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

## GSAP Patterns

### Basic Animation
```tsx
import gsap from 'gsap';

// Simple tween
gsap.to('.element', {
  x: 100,
  opacity: 1,
  duration: 0.3,
  ease: 'power2.out'
});

// From animation
gsap.from('.element', {
  y: 20,
  opacity: 0,
  duration: 0.3,
  ease: 'power2.out'
});
```

### Timeline for Sequences
```tsx
const tl = gsap.timeline();

tl.from('.header', { y: -50, opacity: 0 })
  .from('.content', { y: 20, opacity: 0 }, '-=0.2')
  .from('.footer', { y: 20, opacity: 0 }, '-=0.2');

// Control the timeline
tl.play();
tl.pause();
tl.reverse();
```

### Stagger Animations
```tsx
gsap.from('.list-item', {
  y: 20,
  opacity: 0,
  duration: 0.3,
  stagger: 0.05,
  ease: 'power2.out'
});
```

### ScrollTrigger
```tsx
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

gsap.from('.section', {
  scrollTrigger: {
    trigger: '.section',
    start: 'top 80%',
    end: 'bottom 20%',
    toggleActions: 'play none none reverse'
  },
  y: 50,
  opacity: 0,
  duration: 0.6
});
```

### GSAP Easing
```tsx
// Power easings (1-4, higher = more dramatic)
ease: 'power1.out'  // Subtle
ease: 'power2.out'  // Standard (like ease-out)
ease: 'power3.out'  // Pronounced
ease: 'power4.out'  // Dramatic

// Special easings
ease: 'back.out(1.7)'   // Overshoot
ease: 'elastic.out(1, 0.3)'  // Bouncy
ease: 'bounce.out'      // Bounce at end
```

### React Integration
```tsx
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';

function Component() {
  const containerRef = useRef(null);

  useGSAP(() => {
    gsap.from('.item', {
      y: 20,
      opacity: 0,
      stagger: 0.1
    });
  }, { scope: containerRef });

  return (
    <div ref={containerRef}>
      <div className="item">Item 1</div>
      <div className="item">Item 2</div>
    </div>
  );
}
```

## Performance Tips

### Use Transform & Opacity
```css
/* Good - GPU accelerated */
transform: translateX(100px);
transform: scale(1.1);
transform: rotate(45deg);
opacity: 0.5;

/* Avoid animating - triggers layout */
width, height, top, left, margin, padding
```

### will-change Hint
```css
/* Use sparingly - only for known animations */
.animated-element {
  will-change: transform, opacity;
}

/* Remove after animation */
.animated-element.done {
  will-change: auto;
}
```

### Reduce Motion Query
```tsx
// React hook
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

// Framer Motion
<motion.div
  animate={{ x: 100 }}
  transition={{
    duration: prefersReducedMotion ? 0 : 0.3
  }}
/>
```

## Quick Reference

| Element | Duration | Easing | Properties |
|---------|----------|--------|------------|
| Button hover | 150ms | ease-out | transform, shadow, bg |
| Toggle switch | 200ms | ease-out | transform |
| Dropdown open | 200ms | ease-out | opacity, transform |
| Modal enter | 250ms | ease-out | opacity, scale |
| Modal exit | 200ms | ease-in | opacity, scale |
| Page transition | 300ms | ease-in-out | opacity, transform |
| Toast enter | 300ms | spring | transform |
| Skeleton pulse | 2000ms | ease-in-out | opacity |

## Motion Checklist

- [ ] Animation has clear purpose (feedback, orientation, focus)
- [ ] Duration feels snappy (not sluggish)
- [ ] Easing matches motion type (ease-out for enters)
- [ ] Respects prefers-reduced-motion
- [ ] Only animates transform/opacity when possible
- [ ] Exit animations are faster than enters
- [ ] Stagger delays are subtle (30-50ms)
- [ ] No animation blocks user interaction
