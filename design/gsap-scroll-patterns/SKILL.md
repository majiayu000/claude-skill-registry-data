---
name: gsap-scroll-patterns
description: Complete GSAP and ScrollTrigger patterns for scroll-driven animations. Use when building scroll storytelling, section pinning, parallax effects, or timeline-based choreography.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# GSAP & ScrollTrigger Patterns

## Purpose
Production-ready GSAP patterns for scroll-driven animation. Every example is complete and copy-pasteable. After reading this skill, you can build a full scroll storytelling page from these patterns alone.

## When to Use This Skill
Use when:
- Scroll-driven animations (section reveals, parallax, pinning)
- Timeline choreography (sequenced multi-element animations)
- Text splitting animations (character/word reveals)
- Any animation that must sync to scroll position

Do NOT use when:
- High performance animations are not required, or for basic component-level triggers that can be handled via Framer Motion.

**CRITICAL**: Never use GSAP and Framer Motion in the same component tree. If a section uses GSAP, every animation in that section must be GSAP.

## Phase 1: GSAP Animation Strategy

## 1. Core API

### gsap.to() — Animate TO target values
```tsx
// Move element 100px right and fade in over 1 second
gsap.to(".element", {
  x: 100,
  opacity: 1,
  duration: 1,
  ease: "power2.out",
});
```

### gsap.from() — Animate FROM starting values (element snaps to its CSS position at end)
```tsx
// Element starts 50px below and invisible, animates to its natural position
gsap.from(".element", {
  y: 50,
  opacity: 0,
  duration: 0.8,
  ease: "power3.out",
});
```

### gsap.fromTo() — Explicit start AND end values
```tsx
// Full control: define both start and end states
gsap.fromTo(".element",
  { y: 30, opacity: 0, scale: 0.95 },        // FROM
  { y: 0, opacity: 1, scale: 1, duration: 1 } // TO
);
```

### Property Shorthands
```
x, y           → translateX, translateY (GPU-accelerated)
scale          → scale transform
rotation       → rotate in degrees
scaleX, scaleY → directional scale
xPercent       → translateX in percent of element width
yPercent       → translateY in percent of element height
```

**RULE**: Only animate `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`, `margin`, or `padding`. These trigger layout recalculation and kill 60fps.

### Easing Reference
```
"none"            → Linear (robotic, avoid for UI)
"power1.out"      → Subtle deceleration (buttons, micro-interactions)
"power2.out"      → Standard deceleration (most UI animations)
"power3.out"      → Pronounced deceleration (entrance reveals)
"power4.out"      → Dramatic deceleration (hero elements)
"back.out(1.7)"   → Slight overshoot (playful, bouncy)
"elastic.out(1, 0.3)" → Elastic spring (celebrations, success states)
"expo.out"        → Extreme deceleration (premium, Apple-style)

// For scroll-scrubbed animations, easing is irrelevant — scroll position
// directly controls progress. Use "none" or omit ease entirely.
```

---

## 2. Timelines

Timelines chain animations in sequence. Without a timeline, animations fire simultaneously.

```tsx
const tl = gsap.timeline();

tl.from(".hero-title", { y: 40, opacity: 0, duration: 0.8, ease: "power3.out" })
  .from(".hero-subtitle", { y: 30, opacity: 0, duration: 0.6, ease: "power3.out" }, "-=0.4")
  .from(".hero-cta", { y: 20, opacity: 0, duration: 0.5, ease: "power2.out" }, "-=0.3");

// Position parameter (3rd argument):
// "-=0.4"   → start 0.4s BEFORE previous animation ends (overlap)
// "+=0.2"   → start 0.2s AFTER previous animation ends (gap)
// "<"       → start at same time as previous animation
// "<0.2"    → start 0.2s after previous animation STARTS
```

### Timeline Defaults
```tsx
// Set shared defaults to reduce repetition
const tl = gsap.timeline({
  defaults: { duration: 0.8, ease: "power3.out" },
});

tl.from(".line-1", { y: 40, opacity: 0 })
  .from(".line-2", { y: 40, opacity: 0 }, "-=0.5")
  .from(".line-3", { y: 40, opacity: 0 }, "-=0.5");
```

---

## 3. ScrollTrigger Fundamentals

### Installation
```tsx
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);
```

### Basic Trigger
```tsx
gsap.from(".feature-card", {
  y: 60,
  opacity: 0,
  duration: 1,
  ease: "power3.out",
  scrollTrigger: {
    trigger: ".feature-card",     // Element that triggers the animation
    start: "top 80%",             // "trigger-position viewport-position"
    end: "top 20%",               // When to end (for scrub)
    toggleActions: "play none none none",
    // toggleActions: "onEnter onLeave onEnterBack onLeaveBack"
    // Values: "play", "pause", "resume", "reset", "restart", "complete", "reverse", "none"
  },
});
```

### Start/End Syntax
```
"top 80%"      → when the TOP of trigger hits 80% from viewport top
"top center"   → when the TOP of trigger hits the viewport center
"top top"      → when the TOP of trigger hits the viewport top
"bottom top"   → when the BOTTOM of trigger reaches the viewport top
"center center" → when the CENTER of trigger is at viewport center

// Pixel offsets:
"top 80%-=100" → 100px above the 80% mark
```

### Scrub — Link Animation to Scroll Position
```tsx
gsap.to(".progress-bar", {
  scaleX: 1,
  ease: "none",     // Linear for scroll-linked — easing feels wrong with scrub
  scrollTrigger: {
    trigger: ".content-section",
    start: "top top",
    end: "bottom bottom",
    scrub: true,      // Direct 1:1 scroll-to-progress mapping
    // scrub: 0.5,    // 0.5 second smoothing lag (feels polished)
    // scrub: 1,      // 1 second lag (smooth, cinematic)
    // scrub: 3,      // 3 second lag (lazy, dramatic)
  },
});
```

### Pin — Lock Element During Scroll
```tsx
ScrollTrigger.create({
  trigger: ".pinned-section",
  start: "top top",
  end: "+=1000",           // Pin for 1000px of scroll distance
  pin: true,               // Lock the trigger element in place
  pinSpacing: true,        // Push content below down (default, usually correct)
  anticipatePin: 1,        // iOS Safari: pre-calculate pin position to prevent jump
});
```

### Debug Markers
```tsx
scrollTrigger: {
  markers: true,  // DEVELOPMENT ONLY — shows start/end markers on screen
}
// ALWAYS remove markers before shipping.
```

---

## 4. Battle-Tested Patterns

### Pattern 1: Section Reveal on Scroll
```tsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger);

export function SectionReveal({ children }: { children: React.ReactNode }) {
  const sectionRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const elements = sectionRef.current?.querySelectorAll("[data-animate]");
    if (!elements) return;

    elements.forEach((el, i) => {
      gsap.from(el, {
        y: 40,
        opacity: 0,
        duration: 0.8,
        delay: i * 0.1,
        ease: "power3.out",
        scrollTrigger: {
          trigger: el,
          start: "top 85%",
          toggleActions: "play none none none",
        },
      });
    });
  }, { scope: sectionRef });

  return <div ref={sectionRef}>{children}</div>;
}

// Usage:
// <SectionReveal>
//   <h2 data-animate>Title</h2>
//   <p data-animate>Description</p>
//   <button data-animate>CTA</button>
// </SectionReveal>
```

### Pattern 2: Pinned Section with Timeline
```tsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger);

export function PinnedFeatureShowcase() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: containerRef.current,
        start: "top top",
        end: "+=3000",        // 3000px of scroll to complete the timeline
        pin: true,
        scrub: 1,
        anticipatePin: 1,
      },
    });

    tl.from(".feature-1", { opacity: 0, y: 30 })
      .to(".feature-1", { opacity: 0, y: -30 }, "+=0.3")
      .from(".feature-2", { opacity: 0, y: 30 })
      .to(".feature-2", { opacity: 0, y: -30 }, "+=0.3")
      .from(".feature-3", { opacity: 0, y: 30 });
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="relative h-screen overflow-hidden">
      <div className="feature-1 absolute inset-0 flex items-center justify-center">
        <h2>Feature One</h2>
      </div>
      <div className="feature-2 absolute inset-0 flex items-center justify-center">
        <h2>Feature Two</h2>
      </div>
      <div className="feature-3 absolute inset-0 flex items-center justify-center">
        <h2>Feature Three</h2>
      </div>
    </section>
  );
}
```

### Pattern 3: Horizontal Scroll Section
```tsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalScroll() {
  const containerRef = useRef<HTMLDivElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const track = trackRef.current;
    if (!track) return;

    const totalWidth = track.scrollWidth - window.innerWidth;

    gsap.to(track, {
      x: -totalWidth,
      ease: "none",
      scrollTrigger: {
        trigger: containerRef.current,
        start: "top top",
        end: () => `+=${totalWidth}`,
        pin: true,
        scrub: 0.5,
        anticipatePin: 1,
        invalidateOnRefresh: true,  // Recalculate on resize
      },
    });
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="overflow-hidden">
      <div ref={trackRef} className="flex gap-8 w-max px-8">
        {/* Horizontal scroll panels */}
        <div className="w-screen h-screen flex-shrink-0">Panel 1</div>
        <div className="w-screen h-screen flex-shrink-0">Panel 2</div>
        <div className="w-screen h-screen flex-shrink-0">Panel 3</div>
      </div>
    </section>
  );
}
```

### Pattern 4: Parallax Layer Stack
```tsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger);

export function ParallaxHero() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // Foreground moves fast, background moves slow
    gsap.to(".parallax-bg", {
      yPercent: -20,
      ease: "none",
      scrollTrigger: {
        trigger: containerRef.current,
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });

    gsap.to(".parallax-mid", {
      yPercent: -40,
      ease: "none",
      scrollTrigger: {
        trigger: containerRef.current,
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });

    gsap.to(".parallax-fg", {
      yPercent: -60,
      ease: "none",
      scrollTrigger: {
        trigger: containerRef.current,
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="relative h-[150vh] overflow-hidden">
      <div className="parallax-bg absolute inset-0">Background Layer</div>
      <div className="parallax-mid absolute inset-0">Midground Layer</div>
      <div className="parallax-fg absolute inset-0">Foreground Layer</div>
    </section>
  );
}
```

### Pattern 5: Batch Stagger for Repeated Elements
```tsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger);

export function StaggeredCards() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    ScrollTrigger.batch(".stagger-card", {
      onEnter: (elements) => {
        gsap.from(elements, {
          y: 40,
          opacity: 0,
          duration: 0.8,
          ease: "power3.out",
          stagger: 0.1,
        });
      },
      start: "top 85%",
      once: true,      // Only animate once, don't reverse
    });
  }, { scope: containerRef });

  return (
    <div ref={containerRef} className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="stagger-card">Card 1</div>
      <div className="stagger-card">Card 2</div>
      <div className="stagger-card">Card 3</div>
      <div className="stagger-card">Card 4</div>
      <div className="stagger-card">Card 5</div>
      <div className="stagger-card">Card 6</div>
    </div>
  );
}
```

---

## 5. Next.js Integration

### The useGSAP Hook (Required for All GSAP in React)

```tsx
// Install: npm install @gsap/react
import { useGSAP } from "@gsap/react";

// useGSAP replaces useEffect + useLayoutEffect for GSAP.
// It automatically creates a gsap.context() and cleans up on unmount.

export function AnimatedComponent() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // All GSAP code goes inside this callback.
    // Selectors are scoped to containerRef automatically.
    gsap.from(".child-element", { y: 30, opacity: 0 });
  }, { scope: containerRef }); // Scope limits selectors to this container

  // DEPENDENCY ARRAY (optional, 2nd arg after config):
  // useGSAP(() => { ... }, { scope: ref, dependencies: [someState] });
  // Re-runs when dependencies change, cleaning up previous animations.

  return <div ref={containerRef}>...</div>;
}
```

**RULE**: Every GSAP animation in a React component MUST use `useGSAP`. Never use raw `useEffect` with GSAP — cleanup is unreliable.

### ScrollTrigger.refresh() After Dynamic Content
```tsx
useGSAP(() => {
  // After images load or dynamic content renders, recalculate positions
  ScrollTrigger.refresh();
}, { dependencies: [dataLoaded] });

// Also refresh on window resize (automatic, but manual trigger if layout shifts):
// ScrollTrigger.addEventListener("refreshInit", () => { ... });
```

---

## 6. Responsive Scroll Animations

```tsx
useGSAP(() => {
  const mm = gsap.matchMedia();

  mm.add("(min-width: 768px)", () => {
    // Desktop-only: horizontal scroll
    gsap.to(".track", {
      x: -totalWidth,
      scrollTrigger: { trigger: ".container", pin: true, scrub: 1 },
    });
  });

  mm.add("(max-width: 767px)", () => {
    // Mobile: vertical stack, simple reveals
    gsap.from(".track > *", {
      y: 30,
      opacity: 0,
      stagger: 0.1,
      scrollTrigger: { trigger: ".container", start: "top 80%" },
    });
  });

  // Reduced motion — CRITICAL for accessibility
  mm.add("(prefers-reduced-motion: reduce)", () => {
    // Kill all scroll animations. Show content immediately.
    ScrollTrigger.getAll().forEach(st => st.kill());
    gsap.set("[data-animate]", { opacity: 1, y: 0, x: 0 });
  });
}, { scope: containerRef });
```

---

## 7. iOS Safari Compatibility

| Issue | Fix |
|-------|-----|
| Pin jumps on scroll start | `anticipatePin: 1` on every pinned ScrollTrigger |
| Address bar resize causes layout shift | Use `min-h-[100dvh]` instead of `h-screen` |
| Overscroll bounce interferes with pin | `overscroll-behavior: none` on `<body>` |
| Momentum scroll overshoots end position | Use `scrub: 0.5` minimum (never `scrub: true`) |
| Pinned section flickers | Add `will-change: transform` to pinned element |
| Content below pin overlaps | Ensure `pinSpacing: true` (default, don't disable) |

---

## 8. Text Splitting Animation

```tsx
// Requires: npm install gsap @gsap/react
// SplitText is a GSAP Club plugin. For free alternative, split manually:

"use client";
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

export function TextReveal({ text }: { text: string }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const chars = containerRef.current?.querySelectorAll(".char");
    if (!chars) return;

    gsap.from(chars, {
      y: "100%",
      opacity: 0,
      duration: 0.6,
      ease: "power3.out",
      stagger: 0.02,
      scrollTrigger: {
        trigger: containerRef.current,
        start: "top 80%",
        toggleActions: "play none none none",
      },
    });
  }, { scope: containerRef });

  return (
    <div ref={containerRef} className="overflow-hidden">
      <span className="inline-flex flex-wrap">
        {text.split("").map((char, i) => (
          <span key={i} className="char inline-block" style={{ whiteSpace: char === " " ? "pre" : undefined }}>
            {char}
          </span>
        ))}
      </span>
    </div>
  );
}
```

---

## 9. Anti-Patterns

| ❌ Don't | ✅ Do | Why |
|---------|-------|-----|
| `gsap.to(el, { width: "100%" })` | `gsap.to(el, { scaleX: 1 })` | `width` triggers layout. `scaleX` is GPU-only. |
| `gsap.to(el, { height: 0 })` | `gsap.to(el, { scaleY: 0 })` | Same — avoid layout-triggering properties. |
| `useEffect(() => { gsap.to(...) })` | `useGSAP(() => { gsap.to(...) })` | `useGSAP` handles cleanup. `useEffect` causes memory leaks. |
| Pinning inside a flex container | Pin a wrapper around the flex container | Flex recalculates during pin, causing jitter. |
| `scrub: true` on short timelines | `scrub: 0.5` minimum | `true` = direct mapping, feels jerky on short timelines. |
| Forgetting `anticipatePin` | Always set `anticipatePin: 1` | iOS Safari jump on pin start. |
| Leaving `markers: true` in production | Remove or gate behind `process.env.NODE_ENV` | Visible debug markers in production. |
| Mixing GSAP + Framer Motion in one tree | Use one library per component tree boundary | Conflicting transform management causes unpredictable behavior. |

---

## 10. Verification Checklist

- [ ] Every GSAP call is inside `useGSAP()` with a `scope` ref
- [ ] Every ScrollTrigger has explicit `start` and `end` values
- [ ] Only `transform` and `opacity` are animated (no layout properties)
- [ ] `anticipatePin: 1` is set on every pinned ScrollTrigger
- [ ] `scrub` uses a numeric value (not bare `true`) on timelines under 2000px
- [ ] `markers: true` is removed before production
- [ ] `prefers-reduced-motion` is handled via `gsap.matchMedia()`
- [ ] `ScrollTrigger.refresh()` is called after dynamic content loads
- [ ] Mobile breakpoint has simplified or disabled scroll animations
- [ ] No GSAP and Framer Motion in the same component tree

## Output Format / Delivery
- High-fidelity scroll storytelling and timeline animations using GSAP.
- Responsive, accessible scroll-pinned structures with clean GSAP cleanup.

## Behavior Rules
- Always use useGSAP hook for proper garbage collection.
- Always check prefers-reduced-motion via gsap.matchMedia().

## Maintenance Notes
- Updated to match structural guidelines in June 2026.
