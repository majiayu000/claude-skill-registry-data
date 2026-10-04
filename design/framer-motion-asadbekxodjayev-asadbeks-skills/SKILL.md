---
name: framer-motion
description: Best practices for Framer Motion / Motion (motion for React) animations — variants, AnimatePresence, layout animations, gestures, performance (transform/opacity, LazyMotion), reduced-motion accessibility, and "use client" in Next.js RSC. Auto-activates when adding or reviewing animations, transitions, motion components, whileHover/whileInView, or page/exit transitions.
---

# Framer Motion / Motion (React)

Animation library for React. **Package note:** Framer Motion was rebranded to **Motion**. New projects: `npm i motion`, import from `motion/react`. Existing projects on `framer-motion` (v11/v12): import from `framer-motion` — same API. Use whichever the project already has; don't mix both.

```tsx
import { motion, AnimatePresence } from 'motion/react'   // or 'framer-motion'
```

## Core patterns

**Animate with `motion.*` + variants** (named states keep markup clean and enable orchestration):
```tsx
const list = { show: { transition: { staggerChildren: 0.06 } } }
const item = { hidden: { opacity: 0, y: 8 }, show: { opacity: 1, y: 0 } }

<motion.ul variants={list} initial="hidden" animate="show">
  {items.map((i) => <motion.li key={i.id} variants={item}>{i.label}</motion.li>)}
</motion.ul>
```

**Exit animations need `AnimatePresence`** + a stable `key`; the exiting element must be a direct child:
```tsx
<AnimatePresence mode="wait">
  {open && <motion.div key="panel" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />}
</AnimatePresence>
```

**Scroll-triggered:** `whileInView={{ opacity: 1 }} viewport={{ once: true, margin: '-10%' }}`.
**Gestures:** `whileHover`, `whileTap`, `whileFocus`, `drag`.
**Shared/layout:** add `layout` for auto-animated layout changes; `layoutId="x"` for shared-element morphs between components. Use sparingly — layout animations are the most expensive.

## Accessibility — respect reduced motion (required)

```tsx
import { useReducedMotion } from 'motion/react'
const reduce = useReducedMotion()
const variants = reduce ? { hidden: { opacity: 0 }, show: { opacity: 1 } } : fullVariants
```
Or wrap with `<MotionConfig reducedMotion="user">`. Never ship motion that ignores `prefers-reduced-motion`. Keep motion **subtle** (small distances, short durations, spring or ease-out) — no gratuitous bounce.

## Performance

- Animate **`transform` and `opacity` only** (GPU-composited). Avoid animating `width`/`height`/`top`/`left`/`margin` (layout thrash) — use `scale`/`x`/`y` or `layout`.
- **Reduce bundle:** use `LazyMotion` + `domAnimation` and the lightweight `m` component instead of `motion` where you don't need the full feature set:
```tsx
import { LazyMotion, domAnimation, m } from 'motion/react'
<LazyMotion features={domAnimation}><m.div animate={{ opacity: 1 }} /></LazyMotion>
```
- Springs (`type: 'spring'`) feel natural; tweens (`duration`, `ease`) for precise timing. Stagger lists rather than animating dozens of springs independently.
- On constrained devices (Smart TV, low-end mobile) prefer CSS transitions or minimal opacity/transform; heavy `layout`/spring work can jank.

## Next.js App Router (RSC)

`motion`/`m` components are interactive → they require **`"use client"`**. Put them in client components; don't import `motion` into a Server Component. A common pattern is a small `MotionDiv` client wrapper re-exported for use inside server pages.

## Don'ts

- Don't animate layout-triggering CSS props for transitions.
- Don't forget `key` + `AnimatePresence` for exit animations (they silently won't run otherwise).
- Don't ignore reduced-motion.
- Don't import the full `motion` everywhere when `LazyMotion`+`m` would cut bundle size.
- Don't mix `framer-motion` and `motion` packages in one app.
