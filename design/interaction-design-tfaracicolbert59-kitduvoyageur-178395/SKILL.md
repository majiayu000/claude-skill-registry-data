---
name: interaction-design
description: Design and implement microinteractions, motion design, transitions, and user feedback patterns. Use when adding polish to UI interactions, implementing loading states, or creating delightful user experiences.
---

# Aura Interaction Design Skill

Create engaging, intuitive interactions through motion, feedback, and thoughtful state transitions that enhance usability, performance, and delight users across desktop and mobile.

---

## When to Use This Skill

Activate this skill automatically for any task concerning:
- **UX & Ergonomics**: User journeys, interactive hierarchy, form validation, step-by-step onboarding.
- **Micro-interactions**: Button press states, toggle switches, counter increments, reactive icons.
- **Motion & Transitions**: Page/view transitions, modal sheets, drawer slides, accordion expands.
- **Loading & Feedback**: Skeleton screens, progressive progress bars, toast alerts, tactile haptics.
- **Mobile Gestures**: Pull-to-refresh, swipe-to-dismiss, sheet dragging, carousel panning.
- **States & Continuity**: Empty states, error boundaries, partial network recovery, optimistic UI updates.

---

## LKDV Integration & Architectural Rules

When applying interaction design to **LKDV (Le Kit du Voyageur)**:

1. **Design System Consistency**:
   - **Palette**: Use `#0B1F17` (Foreground 900), `#17402C` (Foreground 800 - primary CTAs & active states), `#2D6B4A` (Foreground 700), `#A3C4A3` (Sage 500), `#FBFAF6` (Stone 50/100).
   - **Prohibition**: Never introduce `#E4501C` (orange) into new or modified code.
   - **Typography**: Söhne/Inter for UI, Georgia italic (`#17402C`) for emphasis, JetBrains Mono for metrics/numbers.
2. **Mobile-First & Shell Awareness**:
   - Respect `MobilePageShell`, `BottomTabBar`, and `HamburgerMenu`.
   - Preserve safe areas (`env(safe-area-inset-bottom)`, `safe-area-inset-top`).
   - Do not obscure floating navigation with bottom sheets or persistent toasts without proper z-index and spacing (`pb-24` on mobile).
3. **Performance First**:
   - Only animate GPU-accelerated properties: `transform` (scale, translate) and `opacity`.
   - Never animate layout properties like `width`, `height`, `top`, `left`, `margin`, or `padding` directly.
   - Avoid heavy continuous JS loops on mobile devices.
4. **Accessibility (a11y)**:
   - Always honor `prefers-reduced-motion`.
   - Provide non-visual feedback (ARIA live regions, accessible names, focus states).
   - Ensure touch targets are at least `44x44px` on mobile.

---

## Core Principles

### 1. Purposeful Motion
Motion must communicate, not decorate:
- **Feedback**: Confirm user actions instantaneously (< 100ms).
- **Orientation**: Clarify spatial origins (modals slide from trigger or bottom on mobile).
- **Focus**: Direct user attention to crucial state changes without disorienting them.
- **Continuity**: Maintain context during transitions (shared layout animations, persistent headers).

### 2. Timing Scale
| Duration | Use Case |
| :--- | :--- |
| **100 – 150ms** | Micro-feedback (button tap, hover, radio selection, icon morph) |
| **200 – 300ms** | Small transitions (toggles, dropdown menus, tooltips, accordion items) |
| **300 – 450ms** | Medium transitions (bottom sheets, dialog modals, drawer navigation, page enters) |
| **500ms+** | Choreographed multi-step animations (onboarding steps, celebration flows) |

### 3. Easing Curves & Springs
```css
/* Standard CSS Easings */
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);      /* Decelerate - entering elements */
--ease-in: cubic-bezier(0.55, 0, 1, 0.45);      /* Accelerate - exiting elements */
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);  /* Symmetrical - layout reordering */
--spring-snappy: cubic-bezier(0.34, 1.56, 0.64, 1); /* Bouncy micro-feedback */
```

In Framer Motion:
```typescript
export const springTransition = {
  type: "spring" as const,
  stiffness: 400,
  damping: 30,
  mass: 0.8,
};

export const snappySpring = {
  type: "spring" as const,
  stiffness: 500,
  damping: 25,
};
```

---

## Standard Interaction Patterns

### 1. Interactive Button (with Press & Haptic Feedback)
```tsx
import { motion } from "framer-motion";

interface InteractiveButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary" | "ghost";
  className?: string;
  disabled?: boolean;
}

export function InteractiveButton({
  children,
  onClick,
  variant = "primary",
  className = "",
  disabled = false,
}: InteractiveButtonProps) {
  const baseStyles =
    "relative inline-flex items-center justify-center font-medium rounded-xl transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#17402C] focus-visible:ring-offset-2";
  
  const variantStyles = {
    primary: "bg-[#17402C] text-white hover:bg-[#0B1F17] shadow-sm",
    secondary: "bg-[#EDF3ED] text-[#17402C] hover:bg-[#A3C4A3]/20 border border-[#A3C4A3]/30",
    ghost: "text-[#0B1F17] hover:bg-[#0B1F17]/5",
  };

  return (
    <motion.button
      type="button"
      disabled={disabled}
      onClick={onClick}
      whileHover={{ scale: disabled ? 1 : 1.015 }}
      whileTap={{ scale: disabled ? 1 : 0.97 }}
      transition={{ type: "spring", stiffness: 450, damping: 25 }}
      className={`${baseStyles} ${variantStyles[variant]} ${className} ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
    >
      {children}
    </motion.button>
  );
}
```

### 2. Skeleton Loading Screen
Preserve layout stability and prevent Content Layout Shift (CLS):
```tsx
export function CardSkeleton() {
  return (
    <div className="bg-[#FBFAF6] border border-[#0B1F17]/10 rounded-2xl p-4 shadow-sm animate-pulse space-y-3">
      <div className="h-44 bg-[#0B1F17]/5 rounded-xl w-full" />
      <div className="h-5 bg-[#0B1F17]/10 rounded w-3/4" />
      <div className="h-4 bg-[#0B1F17]/5 rounded w-1/2" />
      <div className="flex gap-2 pt-2">
        <div className="h-6 bg-[#0B1F17]/5 rounded-full w-16" />
        <div className="h-6 bg-[#0B1F17]/5 rounded-full w-20" />
      </div>
    </div>
  );
}
```

### 3. Smooth Animated Switch Toggle
```tsx
import { motion } from "framer-motion";

interface ToggleProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
}

export function Toggle({ checked, onChange, label }: ToggleProps) {
  return (
    <label className="inline-flex items-center gap-3 cursor-pointer select-none">
      <button
        role="switch"
        type="button"
        aria-checked={checked}
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 shrink-0 rounded-full transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-[#17402C] ${
          checked ? "bg-[#17402C]" : "bg-neutral-300"
        }`}
      >
        <motion.span
          className="pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0"
          animate={{ x: checked ? 22 : 2 }}
          transition={{ type: "spring", stiffness: 600, damping: 35 }}
        />
      </button>
      {label && <span className="text-sm font-medium text-[#0B1F17]">{label}</span>}
    </label>
  );
}
```

### 4. Page & Route Transitions (Framer Motion)
```tsx
import { AnimatePresence, motion } from "framer-motion";

export function PageTransition({
  children,
  routeKey,
}: {
  children: React.ReactNode;
  routeKey: string;
}) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={routeKey}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
        className="w-full"
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### 5. Mobile Bottom Sheet / Modal Entry
```tsx
export const bottomSheetVariants = {
  hidden: { y: "100%", opacity: 0.5 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { type: "spring", damping: 30, stiffness: 350 },
  },
  exit: {
    y: "100%",
    opacity: 0,
    transition: { duration: 0.2, ease: [0.55, 0, 1, 0.45] },
  },
};
```

---

## Accessibility & Reduced Motion

Always respect user preferences for reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

In React hooks / components:
```typescript
import { useReducedMotion } from "framer-motion";

export function useMotionSafe() {
  const shouldReduceMotion = useReducedMotion();
  return {
    duration: shouldReduceMotion ? 0 : 0.25,
    spring: shouldReduceMotion ? { duration: 0 } : { type: "spring", stiffness: 400, damping: 25 },
  };
}
```

---

## Quality Checklist Before Shipping Interactions

- [ ] **Frame Rate**: Runs smoothly at 60fps/120fps on mobile without dropped frames.
- [ ] **Safe Hardware Acceleration**: Only `transform` and `opacity` are animated.
- [ ] **Instant Touch Feedback**: Visual active/tap response is triggered immediately on pointer down.
- [ ] **Clean Unmounts**: Timers, requestAnimationFrame loops, and listeners are properly garbage collected.
- [ ] **Keyboard & Screen Reader Accessible**: Focus styles are clearly distinguishable and not removed.
- [ ] **No Content Shifting**: Loading skeletons match the true dimensions of incoming data.
- [ ] **Respects LKDV Tokens**: Uses `#17402C` and forest/sage accents, zero orange `#E4501C`.
