---
name: motion-accessibility
description: WCAG 2.2 AA motion compliance, reduced-motion handling, ARIA patterns, focus management, and keyboard navigation. Use when auditing web animations, styling reduced-motion variants, or setting up keyboard navigation flows for legal compliance.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# Motion Accessibility & WCAG Compliance

## Purpose
Make every animation in the OS legally and ethically compliant. This skill is an enforcement layer — it applies on top of `gsap-scroll-patterns`, `framer-motion-patterns`, `microinteractions`, and any 3D animation skill.

## When to Use This Skill
- Always. Every page with animation must pass these checks.
- This skill is NOT optional. WCAG 2.2 AA is a legal requirement in the EU (European Accessibility Act 2025) and increasingly enforced in the US (ADA).

## Output Format / Delivery
Provide highly accessible, compliant CSS reset patterns, React dynamic reduced-motion hook checks, focus traps, and screen-reader tags.

## Behavior Rules
1. **Never build hover transitions that trigger layout shifts without a keyboard equivalent**.
2. **Always support vestibular safety by replacing fast translation animation sweeps with cross-fading opacities**.
3. **Never trap focus inside unclosable animated containers**.
4. **Always verify tab index orders flow logically**.

## Maintenance Notes
This skill is locked for WCAG 2.2 compliance features.

---

## Phase 1: Reduced Motion — Global CSS Reset

Place this in your global stylesheet. It is the safety net — if nothing else works, this catches all CSS animations and transitions.

```css
/* globals.css — REQUIRED on every project */
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

**What this does**: Instantly collapses all CSS animations and transitions to near-zero duration. Content appears immediately without motion.

**What this does NOT cover**: JavaScript-driven animations (GSAP, Framer Motion, Three.js). Those require explicit handling below.

---

## 2. Framer Motion — Reduced Motion Integration

### useReducedMotion Hook
```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function AnimatedSection({ children }: { children: React.ReactNode }) {
  const shouldReduce = useReducedMotion();

  return (
    <motion.div
      initial={shouldReduce ? false : { opacity: 0, y: 30 }}
      whileInView={shouldReduce ? {} : { opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.3 }}
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

### Reduced Motion Variant Pattern (Reusable)
```tsx
"use client";
import { motion, useReducedMotion, type Variants } from "motion/react";

// Define full and reduced variant sets
function useAccessibleVariants(
  full: Variants,
  reduced: Variants
): Variants {
  const shouldReduce = useReducedMotion();
  return shouldReduce ? reduced : full;
}

// Usage:
const fullVariants: Variants = {
  hidden: { opacity: 0, y: 40, scale: 0.95 },
  visible: {
    opacity: 1, y: 0, scale: 1,
    transition: { type: "spring", stiffness: 100, damping: 20 },
  },
};

const reducedVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
};

export function AccessibleCard({ children }: { children: React.ReactNode }) {
  const variants = useAccessibleVariants(fullVariants, reducedVariants);

  return (
    <motion.div variants={variants} initial="hidden" whileInView="visible" viewport={{ once: true }}>
      {children}
    </motion.div>
  );
}
```

**RULE**: Reduced-motion variants should keep `opacity` transitions (they don't cause vestibular issues). Remove `transform` animations (`x`, `y`, `scale`, `rotate`).

---

## 3. GSAP — Reduced Motion Integration

### gsap.matchMedia Pattern
```tsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger);

export function AccessibleScrollSection() {
  const ref = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const mm = gsap.matchMedia();

    mm.add("(prefers-reduced-motion: no-preference)", () => {
      // Full animations — only when user has NOT requested reduced motion
      gsap.from("[data-animate]", {
        y: 40,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: "power3.out",
        scrollTrigger: {
          trigger: ref.current,
          start: "top 80%",
        },
      });
    });

    mm.add("(prefers-reduced-motion: reduce)", () => {
      // Reduced: show content immediately, no transforms
      gsap.set("[data-animate]", { opacity: 1, y: 0 });
      // Kill any ScrollTrigger instances
      ScrollTrigger.getAll().forEach((st) => st.kill());
    });
  }, { scope: ref });

  return <div ref={ref}>{/* content with data-animate attributes */}</div>;
}
```

**RULE**: When `prefers-reduced-motion: reduce`, kill ALL ScrollTrigger pins. Pinned sections that trap the user in a scroll loop are a severe vestibular trigger.

---

## 4. Three.js / R3F — Reduced Motion Integration

### Static Fallback Pattern
```tsx
"use client";
import { useState, useEffect } from "react";

export function Hero3D() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(mq.matches);
    const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  if (prefersReducedMotion) {
    // Static fallback: high-quality image instead of 3D scene
    return (
      <div className="relative h-screen">
        <img
          src="/hero-static.webp"
          alt="Product hero"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <h1>Hero Content</h1>
        </div>
      </div>
    );
  }

  // Full 3D scene (only rendered when motion is allowed)
  return <HeroCanvas />;
}
```

### Pausing useFrame
```tsx
import { useFrame } from "@react-three/fiber";
import { useReducedMotion } from "motion/react";

export function RotatingModel() {
  const meshRef = useRef<THREE.Mesh>(null);
  const shouldReduce = useReducedMotion();

  useFrame((_, delta) => {
    if (shouldReduce || !meshRef.current) return; // Stop all animation
    meshRef.current.rotation.y += delta * 0.5;
  });

  return <mesh ref={meshRef}>...</mesh>;
}
```

---

## 5. Auto-Playing Content Rules

WCAG 2.2 SC 2.2.2 requires:

> Any auto-playing animation that lasts longer than 5 seconds MUST have a mechanism to pause, stop, or hide it.

### Implementation
```tsx
"use client";
import { useState, useEffect } from "react";
import { motion, useReducedMotion } from "motion/react";

export function AnimatedBackground() {
  const shouldReduce = useReducedMotion();
  const [isPaused, setIsPaused] = useState(false);

  // Auto-pause after 5 seconds for compliance
  useEffect(() => {
    const timer = setTimeout(() => setIsPaused(true), 5000);
    return () => clearTimeout(timer);
  }, []);

  if (shouldReduce || isPaused) {
    return <div className="bg-zinc-950">Static background</div>;
  }

  return (
    <>
      <motion.div animate={{ /* continuous animation */ }} />
      <button
        onClick={() => setIsPaused(true)}
        className="fixed bottom-4 right-4 z-50"
        aria-label="Pause background animation"
      >
        Pause Animation
      </button>
    </>
  );
}
```

---

## 6. Skip Link

Every page MUST have a skip link as the first focusable element. It allows keyboard users to bypass navigation.

```tsx
// components/SkipLink.tsx
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="
        sr-only focus:not-sr-only
        focus:fixed focus:top-4 focus:left-4 focus:z-[9999]
        focus:px-4 focus:py-2 focus:rounded-lg
        focus:bg-zinc-900 focus:text-white focus:ring-2 focus:ring-white
        focus:outline-none
      "
    >
      Skip to main content
    </a>
  );
}

// In layout.tsx:
// <body>
//   <SkipLink />
//   <nav>...</nav>
//   <main id="main-content">...</main>
// </body>
```

---

## 7. Focus Trapping (Modals & Overlays)

When a modal or overlay is open, focus MUST be trapped inside it. Tab should cycle through focusable elements within the modal, not escape to the page behind.

```tsx
"use client";
import { useEffect, useRef } from "react";

export function useFocusTrap(isOpen: boolean) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen || !containerRef.current) return;

    const container = containerRef.current;
    const focusable = container.querySelectorAll<HTMLElement>(
      'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    const firstEl = focusable[0];
    const lastEl = focusable[focusable.length - 1];

    // Focus first element on open
    firstEl?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        // Close modal on Escape — implement your close logic
        return;
      }

      if (e.key !== "Tab") return;

      if (e.shiftKey) {
        // Shift+Tab: if on first element, jump to last
        if (document.activeElement === firstEl) {
          e.preventDefault();
          lastEl?.focus();
        }
      } else {
        // Tab: if on last element, jump to first
        if (document.activeElement === lastEl) {
          e.preventDefault();
          firstEl?.focus();
        }
      }
    };

    container.addEventListener("keydown", handleKeyDown);
    return () => container.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  return containerRef;
}

// Usage:
// const modalRef = useFocusTrap(isModalOpen);
// <div ref={modalRef} role="dialog" aria-modal="true" aria-labelledby="modal-title">
//   <h2 id="modal-title">Modal Title</h2>
//   ...
// </div>
```

---

## 8. ARIA for Animated Content

### Dynamic Content Announcements
```tsx
// When content changes dynamically (e.g., after form submit, toast notification):
<div role="status" aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// aria-live values:
// "polite"     → announces when user is idle (forms, status updates)
// "assertive"  → announces immediately (errors, urgent alerts)
// "off"        → no announcement (default)
```

### Animated Tabs
```tsx
<div role="tablist" aria-label="Feature tabs">
  {tabs.map((tab) => (
    <button
      key={tab.id}
      role="tab"
      aria-selected={activeTab === tab.id}
      aria-controls={`panel-${tab.id}`}
      id={`tab-${tab.id}`}
      tabIndex={activeTab === tab.id ? 0 : -1}
      onClick={() => setActiveTab(tab.id)}
      onKeyDown={(e) => {
        // Arrow key navigation between tabs
        if (e.key === "ArrowRight") focusNextTab();
        if (e.key === "ArrowLeft") focusPrevTab();
      }}
    >
      {tab.label}
    </button>
  ))}
</div>

{tabs.map((tab) => (
  <div
    key={tab.id}
    role="tabpanel"
    id={`panel-${tab.id}`}
    aria-labelledby={`tab-${tab.id}`}
    hidden={activeTab !== tab.id}
  >
    {tab.content}
  </div>
))}
```

---

## 9. Keyboard Navigation Rules

| Component | Required Keys | Behavior |
|-----------|--------------|----------|
| Button | `Enter`, `Space` | Activate the button |
| Link | `Enter` | Navigate |
| Modal | `Escape` | Close the modal |
| Tabs | `Arrow Left/Right` | Switch between tabs |
| Menu | `Arrow Up/Down` | Navigate items, `Escape` to close |
| Accordion | `Enter`, `Space` | Toggle panel |
| Carousel | `Arrow Left/Right` | Navigate slides |

### Custom Interactive Element
```tsx
// If you build a custom interactive element (not a native <button> or <a>):
<div
  role="button"
  tabIndex={0}
  onClick={handleAction}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleAction();
    }
  }}
  aria-label="Descriptive action label"
>
  Custom clickable element
</div>

// PREFERRED: Just use <button> instead. It handles all of this natively.
```

---

## 10. Verification Checklist

### Reduced Motion
- [ ] Global CSS `prefers-reduced-motion` reset is in `globals.css`
- [ ] Every Framer Motion animation checks `useReducedMotion()`
- [ ] Every GSAP animation uses `gsap.matchMedia()` for reduced-motion
- [ ] Three.js scenes fall back to static images when reduced-motion is active
- [ ] Auto-playing animations stop or provide pause button after 5 seconds

### Focus & Keyboard
- [ ] Skip link is the first focusable element on every page
- [ ] Every modal/overlay has focus trapping
- [ ] Tab order is logical (follows visual reading order)
- [ ] All interactive elements are reachable by keyboard
- [ ] `Escape` closes modals, menus, and overlays

### ARIA
- [ ] Dynamic content changes use `aria-live` regions
- [ ] Custom interactive elements have `role`, `tabIndex`, and keyboard handlers
- [ ] Tabs use proper `role="tablist"`, `role="tab"`, `role="tabpanel"` structure
- [ ] Form errors are associated with inputs via `aria-describedby`

### Testing
- [ ] Toggle reduced-motion in Chrome DevTools: Rendering → Emulate CSS media feature `prefers-reduced-motion`
- [ ] Navigate entire page using only keyboard (Tab, Shift+Tab, Enter, Escape, Arrow keys)
- [ ] Verify no focus trap escapes in modals
- [ ] Screen reader test: enable VoiceOver (macOS) or NVDA (Windows) and verify all content is announced
