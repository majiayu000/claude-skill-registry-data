---
name: motion-dev
description: Use when React animation library — spring physics, gesture animations, layout animations, scroll effects, SVG path drawing. Successor to Framer Motion. Use when building UI animations, micro-interactions, page transitions, shared element transitions, parallax effects.
domain: content
author: oyi77
license: MIT
subdomain: animation
tags:
- animation
- react
- motion
- spring
- gesture
- layout
- scroll
- svg
- transition
- micro-interaction
version: 1.0.0
category: content
---
## Overview

This skill is the motion development playbook for HyperFrames compositions — timeline choreography, easing, and animation primitives in HTML/CSS. Use it when building any animated video surface in code. It covers the animation techniques that make compositions feel designed rather than static.


# Motion.dev — React Animation Library

Motion (formerly Framer Motion) is a production-ready React animation library. Hybrid engine uses Web Animations API + ScrollTimeline for 120fps performance, with JavaScript fallback for spring physics, interruptible keyframes, and gesture tracking.

Source: [motion.dev](https://motion.dev) | GitHub: [motiondivision/motion](https://github.com/motiondivision/motion)

## When to Use

- Building UI animations (enter/exit, hover, tap, drag)
- Layout animations (reorder, resize, shared element transitions)
- Scroll-triggered and scroll-linked effects (parallax, progress)
- SVG path drawing animations
- Micro-interactions (button feedback, loading states)
- Page transitions and route animations
- Gesture-driven interactions (drag, pan, pinch)
- Complex animation orchestration (stagger, sequence)

## Install

```bash
npm install motion
```

Import from `"motion/react"`:
```tsx
import { motion } from "motion/react"
```

## Core API

### Motion Component

Prefix any HTML/SVG tag with `motion.` to unlock animation props:

```tsx
<motion.div animate={{ opacity: 1, scale: 1 }} />
<motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }} />
<motion.circle animate={{ pathLength: 1 }} />
```

### Animation Props

| Prop | Purpose | Example |
|------|---------|---------|
| `animate` | Target values | `{ x: 100, opacity: 1 }` |
| `initial` | Starting values | `{ opacity: 0, scale: 0 }` |
| `exit` | Exit animation (with AnimatePresence) | `{ opacity: 0 }` |
| `whileHover` | Hover state | `{ scale: 1.1 }` |
| `whileTap` | Tap/press state | `{ scale: 0.95 }` |
| `whileFocus` | Focus state | `{ scale: 1.05 }` |
| `whileDrag` | Drag state | `{ scale: 1.1 }` |
| `whileInView` | Scroll-triggered | `{ opacity: 1 }` |
| `layout` | Auto-layout animation | `true` or `"position"` or `"size"` |

### Transition Types

```tsx
// Spring physics (default for physical properties)
<motion.div animate={{ x: 100 }} transition={{ type: "spring", stiffness: 300, damping: 30 }} />

// Tween easing (default for visual properties)
<motion.div animate={{ opacity: 1 }} transition={{ duration: 0.3, ease: "easeOut" }} />

// Keyframes
<motion.div animate={{ x: [0, 100, 0] }} transition={{ duration: 2, repeat: Infinity }} />
```

### Gesture Animations

```tsx
// Hover & tap
<motion.button
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.95 }}
  onHoverStart={() => console.log('hover started')}
/>

// Drag
<motion.div drag dragConstraints={{ left: 0, right: 100, top: 0, bottom: 100 }} />

// Pan
<motion.div onPan={(e, info) => console.log(info.offset)} />

// Pinch
<motion.div onPinch={(e, info) => console.log(info.offset)} />
```

### Layout Animation

```tsx
// Auto-animate layout changes
<motion.div layout />

// Shared element transition
<motion.div layoutId="underline" />

// Layout animation with spring
<motion.div layout transition={{ type: "spring", stiffness: 500, damping: 30 }} />
```

### Scroll Animations

```tsx
// Scroll-triggered
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
/>

// Scroll-linked (progress)
const { scrollYProgress } = useScroll()
<motion.div style={{ scaleX: scrollYProgress }} />

// Parallax
const { scrollYProgress } = useScroll()
const y = useTransform(scrollYProgress, [0, 1], [0, 200])
<motion.div style={{ y }} />
```

### Exit Animations (AnimatePresence)

```tsx
<AnimatePresence>
  {show && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
    />
  )}
</AnimatePresence>
```

### SVG Path Drawing

```tsx
<motion.circle
  initial={{ pathLength: 0 }}
  animate={{ pathLength: 1 }}
  transition={{ duration: 2, ease: "easeInOut" }}
/>
```

### Stagger & Orchestration

```tsx
const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => <motion.li key={i} variants={item} />)}
</motion.ul>
```

## Performance Best Practices

1. **Prefer CSS properties**: `transform` and `opacity` are GPU-accelerated
2. **Avoid animating `width`/`height`**: Use `scale` or `layout` instead
3. **Use `layoutId` for shared elements**: Smooth transitions between components
4. **Set `viewport={{ once: true }}`**: Prevent re-triggering scroll animations
5. **Use `AnimatePresence` for exit animations**: Required for exit transitions
6. **Tree-shaking**: Only import what you use
7. **Spring over tween for physical properties**: More natural feel

## Common Patterns

### Page Transition
```tsx
<motion.div
  initial={{ opacity: 0, x: 20 }}
  animate={{ opacity: 1, x: 0 }}
  exit={{ opacity: 0, x: -20 }}
  transition={{ duration: 0.3 }}
/>
```

### Modal/Dialog
```tsx
<AnimatePresence>
  {isOpen && (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="backdrop"
      />
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.9, y: 20 }}
        transition={{ type: "spring", damping: 25, stiffness: 300 }}
      >
        {children}
      </motion.div>
    </>
  )}
</AnimatePresence>
```

### Staggered List
```tsx
const list = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.07, delayChildren: 0.2 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

<motion.ul variants={list} initial="hidden" animate="show">
  {items.map(item => (
    <motion.li key={item.id} variants={item}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

### Drag-to-Reorder
```tsx
<motion.div
  drag
  dragConstraints={constraints}
  dragElastic={0.2}
  whileDrag={{ scale: 1.05, boxShadow: "0 5px 20px rgba(0,0,0,0.2)" }}
/>
```

### Scroll Progress Indicator
```tsx
const { scrollYProgress } = useScroll()
<motion.div
  className="fixed top-0 left-0 h-1 bg-blue-500 z-50"
  style={{ scaleX: scrollYProgress }}
/>
```

## Integration with Other Skills

- **ui-ux-pro-max** — Use motion.dev to implement the animations recommended by ui-ux-pro-max design system
- **21st-dev** — Many 21st components include motion.dev animations; customize with this skill
- **tailwind-advanced** — Combine motion.dev with Tailwind for animated utility-first UIs
- **frontend-design** — Use motion.dev for interactive prototypes and micro-interactions
- **shadcn/ui** — Animate shadcn/ui components with motion.dev for polished UX

## When NOT to Use

- Simple CSS transitions suffice (hover color change, basic fades)
- Non-React projects (use GSAP or vanilla WAAPI instead)
- Complex timeline animations (GSAP is better for orchestration)
- Canvas/WebGL animations (use Three.js or Pixi.js)
- Pure backend logic (no UI involved)

## Red Flags

- **Animating width/height**: Causes layout thrashing — use `scale` or `layout`
- **Too many simultaneous springs**: Performance degradation — stagger or reduce
- **Missing AnimatePresence**: Exit animations won't work without it
- **Ignoring prefers-reduced-motion**: Accessibility violation — always respect user preference
- **Over-animating**: Not everything needs animation — use motion with purpose

## Verification

- [ ] Animations run at 60fps+ (check with Chrome DevTools Performance)
- [ ] `prefers-reduced-motion` respected
- [ ] Exit animations wrapped in AnimatePresence
- [ ] Layout animations use `layout` prop (not animating width/height)
- [ ] Scroll animations use `viewport={{ once: true }}` where appropriate
- [ ] Spring physics feel natural (not too bouncy, not too stiff)

## Process

1. Identify animation requirements (enter/exit, hover, scroll, layout)
2. Choose animation type (spring, tween, keyframes)
3. Implement with motion components
4. Add gesture handlers if needed
5. Test performance (60fps target)
6. Verify accessibility (reduced-motion)
7. Polish timing and easing

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "CSS transitions are enough" | Motion scales from simple to complex with one API — CSS can't do layout animations or gestures |
| "I'll add animations later" | Animations designed in from the start feel intentional; retrofitted ones feel tacked on |
| "More animation = better UX" | Purposeful animation guides attention; excessive animation distracts |
| "Spring physics everywhere" | Springs are great for physical properties; tween is better for visual properties |
| "prefers-reduced-motion is optional" | It's an accessibility requirement — always respect user preference |
