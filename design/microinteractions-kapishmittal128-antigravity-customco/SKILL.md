---
name: microinteractions
description: Premium Microinteractions & Motion Feedback. Use when designing custom tactile feedback, spring elastic success vectors, confetti milestone celebrations, magnetic hover snapping coordinates, or tactile custom focus rings.
version: "1.0.0"
verified_date: 2026-06-01
category: design
---

# Premium Microinteractions & Motion Feedback

## Purpose
Provide rich, copy-pasteable, and highly responsive tactile interface loops, spring physics checkmarks, gesture swipes, magnetic hover vectors, and accessible double-ring keyboard focus systems.

## When to Use This Skill
- Designing visual micro-feedback loops for clickable components, submissions, or transactions.
- Creating progress loaders, indeterminate shimmer lines, or SVG circular rings.
- Building custom gesture cards using Framer Motion drag coordinates.
- Styling focus rings for high keyboard accessibility and interactive affordance.

## Output Format / Delivery
Provide beautiful, performant, and fully accessible React components and CSS micro-animation styles. All animations must utilize physical elastic spring physics and fail safely under reduced-motion constraints.

## Behavior Rules
1. **Never use generic browser-default outlines for focus rings** — always apply custom double focus rings.
2. **Never utilize infinite rotating loaders for linear transitions** — use progress loaders with spring adjustments.
3. **Always garbage-collect canvas confetti nodes within 2500ms** to prevent memory footprint leaks.
4. **Never write hardcoded rotation values on drag cards** — interpolate drag coordinates directly into rotation vectors.

## Maintenance Notes
This skill is locked for tactile interactions. Update if Framer Motion or web standard canvas interaction profiles require syntactic upgrades.

---

## Phase 1: Success States & Celebrations

Premium interfaces validate successful user actions (submitting a form, completing a transaction, achieving a milestone) through orchestrated micro-animations that communicate accomplishment.

* **Spring-Elastic Checkmark Vector**:
  Custom success checkmarks must animate with an elastic spring draw. Implement using SVG `stroke-dasharray` and `stroke-dashoffset` properties controlled by Framer Motion's spring timing:
  ```tsx
  import { motion } from "motion/react";

  const pathVariants = {
    hidden: { strokeDashoffset: 100, pathLength: 0 },
    visible: { 
      strokeDashoffset: 0,
      pathLength: 1,
      transition: { 
        type: "spring", 
        stiffness: 140, 
        damping: 15,
        restDelta: 0.001 
      }
    }
  };

  export function SuccessCheckmark() {
    return (
      <svg className="w-12 h-12 text-emerald-500" viewBox="0 0 52 52">
        <circle className="stroke-emerald-500/10 fill-none" cx="26" cy="26" r="25" strokeWidth="2" />
        <motion.path
          className="stroke-current fill-none"
          strokeWidth="3"
          strokeLinecap="round"
          d="M14 27l7.5 7.5 16.5-16.5"
          variants={pathVariants}
          initial="hidden"
          animate="visible"
        />
      </svg>
    );
  }
  ```
* **Milestone Confetti Bursts**:
  Celebrate critical triggers (first signup, paid activation) with controlled canvas-confetti.
  - Limit active lifetime to `2500ms`.
  - Color coordinate particles to use the theme accent color + muted pastel variants.
  - Automatically garbage-collect canvas nodes on teardown.
* **Interactive Button Morphing**:
  Upon successful submit, primary CTA buttons should morph:
  - Transition background color to accent-success green (e.g., `#10B981`).
  - Mute text opacity and scale in the elastic checkmark.
  - Apply an active scale-down (`scale-[0.97]`) before expanding back to standard scale.

---

## Phase 2: Progress & Status Indicators

Avoid infinite-spinning circles. They communicate systemic stalling rather than linear progress.

* **Linear Progress Bars**:
  - Always use spring easing animations (`stiffness: 80, damping: 15`) to animate the fill percentage. Smooth steps look faster than linear ticks.
  - **Indeterminate Shimmers**: When exact duration is unknown, use a linear gradient shimmer that sweeps from left to right endlessly:
    ```css
    @keyframes shimmer {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }
    .progress-shimmer {
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0) 100%);
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite linear;
    }
    ```
* **Circular Progress Ring Math**:
  Ensure SVG circular rings utilize exact stroke calculations:
  $$\text{stroke-dashoffset} = 2\pi r \times \left(1 - \frac{\text{percent}}{100}\right)$$
  Always apply `stroke-linecap: round` on the active progress stroke to provide a premium finish.

---

## Phase 3: Gesture & Tactile Feedback

Support touch and pointer gestures with physical, elastic boundary interactions.

* **Swipe-to-Dismiss Constraints**:
  - Swipe boundaries must be bounded by active friction equations. Drag resistance should scale exponentially as the element drifts past its threshold:
    $$\text{resistance} = 1 - \left(\frac{\text{offset}}{\text{max-bounds}}\right)^2$$
  - If the swipe passes a `120px` threshold, trigger a complete exit transition. Otherwise, snap back utilizing default spring stiffness.
* **Drag-and-Drop Boundary Collisions**:
  Custom draggable cards must scale up slightly on drag start (`scale-[1.03] shadow-lg`) and tilt dynamically based on velocity vectors:
  ```tsx
  import { motion, useMotionValue, useTransform } from "motion/react";

  export function DraggableCard({ children }: { children: React.ReactNode }) {
    const x = useMotionValue(0);
    const rotate = useTransform(x, [-300, 300], [-10, 10]);

    return (
      <motion.div
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        style={{ x, rotate }}
        whileDrag={{ scale: 1.03 }}
        className="cursor-grab active:cursor-grabbing"
      >
        {children}
      </motion.div>
    );
  }
  ```
* **Magnetic Hover Snaps**:
  Technical icon links and avatar circles can feature a magnetic snapping attraction:
  - Inside a `40px` activation radius, pull the center coordinate toward the cursor by exactly 35% of the absolute distance.
  - Release cleanly with a spring deceleration upon cursor exit.

---

## Phase 4: Tactile Keyboard Focus Rings

Focus rings must be custom designed, never left to default browser outlines.

* **Bespoke Focus Rings**:
  Disable default browser outlines and apply a double-ring custom outline to prevent color conflicts:
  - Inner Ring: `ring-2 ring-offset-2` matching the background shade.
  - Outer Ring: `ring-accent` utilizing the page's accent token.
* **Focus Transitions**:
  Focus rings must transition smoothly (`transition-all duration-150 ease-out`).
