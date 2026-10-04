---
name: framer-motion-patterns
description: Complete Framer Motion patterns for entrance animations, exits, stagger sequences, scroll-triggered reveals, layout transitions, page transitions, and gesture interactions. Use when building any non-scroll-storytelling animation.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# Framer Motion Patterns

## Purpose
Production-ready Framer Motion patterns covering every standard web animation need. Every example is complete and copy-pasteable. After reading this skill, you can implement any standard page animation.

## When to Use This Skill
Use when:
- Entrance/exit animations
- Hover and tap interactions
- Scroll-triggered reveals (via `whileInView`)
- Page transitions (Next.js App Router)
- Layout animations and shared-element transitions
- Gesture-driven interactions (drag, swipe)

Do NOT use when:
- Using GSAP in the same component tree or for scroll storytelling.

**CRITICAL**: Import from `"motion/react"` — NOT `"framer-motion"`. The package was renamed in v11.
**CRITICAL**: Never use Framer Motion and GSAP in the same component tree.

## Phase 1: Framer Motion Strategy

## 1. Core Animation

### Basic Animate
```tsx
"use client";
import { motion } from "motion/react";

// Animate from initial state to animate state on mount
export function FadeIn({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  );
}
```

### Named Variants
```tsx
"use client";
import { motion } from "motion/react";

const cardVariants = {
  hidden: { opacity: 0, y: 30, scale: 0.97 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      type: "spring",
      stiffness: 100,
      damping: 20,
    },
  },
};

export function AnimatedCard({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
    >
      {children}
    </motion.div>
  );
}
```

### Transition Types
```tsx
// Spring (default for physical, organic feel)
transition: { type: "spring", stiffness: 100, damping: 20 }

// Spring with bounce
transition: { type: "spring", stiffness: 300, damping: 15 }

// Tween with cubic-bezier (premium, Apple-style)
transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] }

// Tween with named easing
transition: { duration: 0.4, ease: "easeOut" }

// Different properties, different transitions
transition: {
  opacity: { duration: 0.3 },
  y: { type: "spring", stiffness: 100, damping: 20 },
}
```

---

## 2. Stagger Children

Parent variant orchestrates child animation timing.

```tsx
"use client";
import { motion } from "motion/react";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,   // 80ms between each child
      delayChildren: 0.1,     // 100ms before first child starts
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 100, damping: 20 },
  },
};

export function StaggeredList({ items }: { items: string[] }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.li key={item} variants={itemVariants}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

**RULE**: Children inherit `initial` and `animate` from parent automatically when using variants. Do NOT re-specify `initial="hidden"` on children.

---

## 3. Scroll-Triggered Reveals

### whileInView — Animate When Element Enters Viewport
```tsx
"use client";
import { motion } from "motion/react";

export function ScrollReveal({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  );
}

// viewport options:
// once: true       → animate only first time (don't reverse on scroll back)
// amount: 0.3      → trigger when 30% of element is visible
// amount: "all"    → trigger when 100% is visible
// margin: "-100px" → trigger 100px before element enters viewport
```

### Staggered Section Reveal
```tsx
"use client";
import { motion } from "motion/react";

const sectionVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] },
  },
};

export function FeatureSection() {
  return (
    <motion.section
      variants={sectionVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.2 }}
    >
      <motion.h2 variants={itemVariants}>Features</motion.h2>
      <motion.p variants={itemVariants}>Subtitle text</motion.p>
      <motion.div variants={itemVariants} className="grid grid-cols-3 gap-6">
        {/* Cards */}
      </motion.div>
    </motion.section>
  );
}
```

---

## 4. Scroll-Linked Values

### useScroll + useTransform — Map Scroll Position to CSS Values
```tsx
"use client";
import { useRef } from "react";
import { motion, useScroll, useTransform } from "motion/react";

export function ParallaxImage() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
    // offset: ["when trigger starts relative to viewport", "when trigger ends"]
    // "start end" = top of element hits bottom of viewport
    // "end start" = bottom of element hits top of viewport
  });

  const y = useTransform(scrollYProgress, [0, 1], ["-10%", "10%"]);
  const opacity = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0, 1, 1, 0]);

  return (
    <div ref={ref} className="overflow-hidden h-[60vh]">
      <motion.img
        src="/hero.jpg"
        alt="Hero"
        style={{ y, opacity }}
        className="w-full h-[120%] object-cover"
      />
    </div>
  );
}
```

### useSpring — Smooth Scroll Values
```tsx
import { useScroll, useSpring, useTransform } from "motion/react";

const { scrollYProgress } = useScroll();
const smoothProgress = useSpring(scrollYProgress, {
  stiffness: 100,
  damping: 30,
  restDelta: 0.001,
});

// Use smoothProgress instead of scrollYProgress for buttery-smooth motion
const y = useTransform(smoothProgress, [0, 1], [0, -200]);
```

---

## 5. Exit Animations (AnimatePresence)

### Basic Exit
```tsx
"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";

export function ToggleContent() {
  const [isVisible, setIsVisible] = useState(true);

  return (
    <>
      <button onClick={() => setIsVisible(!isVisible)}>Toggle</button>
      <AnimatePresence mode="wait">
        {isVisible && (
          <motion.div
            key="content"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          >
            Content here
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

// AnimatePresence modes:
// "sync"     → new and old animate simultaneously (default)
// "wait"     → old exits completely before new enters
// "popLayout" → old exits with layout preserved, new enters immediately
```

**RULE**: Every child of `AnimatePresence` MUST have a unique `key` prop. Without it, exit animations won't fire.

---

## 6. Page Transitions (Next.js App Router)

### Using template.tsx (Recommended)

`template.tsx` remounts on every navigation, unlike `layout.tsx`. This makes it the correct place for page transitions.

```tsx
// app/template.tsx
"use client";
import { motion, AnimatePresence } from "motion/react";
import { usePathname } from "next/navigation";

export default function Template({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

**RULE**: Do NOT put page transitions in `layout.tsx`. Layouts persist across navigations and do not remount — `exit` animations will never fire.

---

## 7. Layout Animations

### Auto Layout Transition
```tsx
// Add `layout` prop — Framer Motion auto-animates position and size changes
<motion.div layout className="p-4">
  {isExpanded ? <FullContent /> : <Summary />}
</motion.div>

// layout="position" → only animate position, not size
// layout="size"     → only animate size, not position
```

### Shared Element Transition (layoutId)
```tsx
"use client";
import { useState } from "react";
import { motion, AnimatePresence, LayoutGroup } from "motion/react";

export function ExpandableCards() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <LayoutGroup>
      <div className="grid grid-cols-3 gap-4">
        {items.map((item) => (
          <motion.div
            key={item.id}
            layoutId={`card-${item.id}`}
            onClick={() => setSelected(item.id)}
            className="cursor-pointer rounded-xl p-4 bg-zinc-900"
          >
            <motion.h3 layoutId={`title-${item.id}`}>{item.title}</motion.h3>
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {selected && (
          <motion.div
            layoutId={`card-${selected}`}
            className="fixed inset-0 z-50 flex items-center justify-center"
          >
            <motion.h3 layoutId={`title-${selected}`}>
              {items.find(i => i.id === selected)?.title}
            </motion.h3>
            <p>Expanded content here</p>
            <button onClick={() => setSelected(null)}>Close</button>
          </motion.div>
        )}
      </AnimatePresence>
    </LayoutGroup>
  );
}
```

---

## 8. Gesture Patterns

### Hover & Tap
```tsx
<motion.button
  whileHover={{ scale: 1.02, boxShadow: "0 8px 30px rgba(0,0,0,0.12)" }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: "spring", stiffness: 400, damping: 25 }}
>
  Click me
</motion.button>
```

### Magnetic Hover Effect
```tsx
"use client";
import { useRef } from "react";
import { motion, useMotionValue, useSpring } from "motion/react";

export function MagneticButton({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const springX = useSpring(x, { stiffness: 200, damping: 20 });
  const springY = useSpring(y, { stiffness: 200, damping: 20 });

  const handleMouse = (e: React.MouseEvent) => {
    const rect = ref.current?.getBoundingClientRect();
    if (!rect) return;
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    // Pull toward cursor by 35% of distance
    x.set((e.clientX - centerX) * 0.35);
    y.set((e.clientY - centerY) * 0.35);
  };

  const handleLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.div
      ref={ref}
      style={{ x: springX, y: springY }}
      onMouseMove={handleMouse}
      onMouseLeave={handleLeave}
      className="inline-block"
    >
      {children}
    </motion.div>
  );
}
```

### Drag with Constraints
```tsx
<motion.div
  drag="x"
  dragConstraints={{ left: -200, right: 200 }}
  dragElastic={0.1}         // Rubber-band effect at boundaries
  dragTransition={{ bounceStiffness: 300, bounceDamping: 20 }}
  whileDrag={{ scale: 1.03, cursor: "grabbing" }}
  className="cursor-grab"
>
  Drag me
</motion.div>
```

---

## 9. Performance Rules

### Hardware Acceleration
Only animate `transform` and `opacity`. Framer Motion does this by default when you use:
- `x`, `y`, `z` (translate)
- `scale`, `scaleX`, `scaleY`
- `rotate`, `rotateX`, `rotateY`
- `opacity`

**NEVER** animate via Framer Motion:
- `width`, `height` → use `scaleX`/`scaleY`
- `top`, `left` → use `x`/`y`
- `borderRadius` → acceptable but not GPU-accelerated
- `backgroundColor` → acceptable for simple color transitions

### Reduce Renders
```tsx
// useMotionValue does NOT trigger React re-renders
const x = useMotionValue(0);

// useState DOES trigger re-renders — avoid for animation values
const [x, setX] = useState(0); // ❌ Bad for animation
```

### Reduced Motion Support
```tsx
import { useReducedMotion } from "motion/react";

export function AnimatedSection({ children }: { children: React.ReactNode }) {
  const shouldReduce = useReducedMotion();

  return (
    <motion.div
      initial={shouldReduce ? false : { opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={shouldReduce
        ? { duration: 0 }
        : { duration: 0.6, ease: [0.16, 1, 0.3, 1] }
      }
    >
      {children}
    </motion.div>
  );
}
```

---

## 10. Anti-Patterns

| ❌ Don't | ✅ Do | Why |
|---------|-------|-----|
| `import { motion } from "framer-motion"` | `import { motion } from "motion/react"` | Package renamed in v11. Old import still works but is deprecated. |
| `AnimatePresence` without `key` on children | Always add unique `key` | Exit animations require `key` to track element identity. |
| Page transitions in `layout.tsx` | Page transitions in `template.tsx` | Layout persists, template remounts. Exit animations need remount. |
| `useState` for animation values | `useMotionValue` for animation values | Motion values don't trigger re-renders. State does. |
| `whileInView` without `viewport={{ once: true }}` | Add `once: true` unless intentional | Without it, animations replay on every scroll pass — distracting. |
| Mixing GSAP and Framer Motion | One library per component tree | Conflicting transform management. |
| Animating `width`/`height` | Animate `scale`/`scaleX`/`scaleY` | Layout-triggering vs GPU-accelerated. |
| `initial={false}` without reason | Only skip `initial` for server-rendered visible content | `initial={false}` means element starts at `animate` state — no animation plays. |

---

## 11. Verification Checklist

- [ ] Importing from `"motion/react"` (not `"framer-motion"`)
- [ ] Every `AnimatePresence` child has a unique `key`
- [ ] Page transitions use `template.tsx`, not `layout.tsx`
- [ ] `whileInView` includes `viewport={{ once: true }}` unless deliberately repeating
- [ ] Only `transform` and `opacity` properties are animated
- [ ] `useReducedMotion()` is checked for all major animations
- [ ] No GSAP usage in the same component tree
- [ ] Animation values use `useMotionValue`, not `useState`
- [ ] Exit animations include `exit` prop with `AnimatePresence` wrapper
- [ ] Spring transitions use reasonable values (stiffness 80-400, damping 15-30)

## Output Format / Delivery
- High-fidelity component animation setup using Framer Motion (via motion/react).
- Smooth entrance/exit/layout animations with reduced-motion fallbacks.

## Behavior Rules
- Always check and respect useReducedMotion().
- Never animate non-GPU attributes like top/left/width/height.

## Maintenance Notes
- Updated to match structural guidelines in June 2026.
