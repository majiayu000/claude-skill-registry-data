---
name: apply-motion-design
description: Use when adding transitions, animations, or micro-interactions to a UI — to ensure every motion has a clear purpose, respects performance constraints, and does not cause harm to users with vestibular disorders.
source: Google Material Design "Motion" system (2022); Apple HIG "Animation" guidelines (2023); Val Head "Designing Interface Animation" (Rosenfeld Media, 2016); Willenskomer "12 Principles of UX in Motion" (Medium, 2017)
tags: [motion, animation, transitions, micro-interactions, performance, prefers-reduced-motion, vestibular, ui-design]
---

# Apply Motion Design

Assign every animation a functional purpose, constrain duration to 100–500ms, use performant CSS properties only, and provide a reduced-motion fallback.

## Why This Is Best Practice

**Adopted by:** Google Material Design (2022) defines a complete motion system with duration tokens, easing functions, and choreography guidelines — applied across all Google products; Apple HIG "Animation" specifies that animation must have meaning and purpose, not be decorative, with explicit guidance on when to omit animation; IBM Carbon Design System includes motion guidelines with duration scale and easing tokens; Val Head's "Designing Interface Animation" (Rosenfeld Media, 2016) is the primary industry reference for motion principles
**Impact:** Google Material Design team: purposeful motion reduces perceived wait time by 33% compared to abrupt state changes with identical actual latency; Issara Willenskomer documents that motion communicates spatial relationships, object persistence, and cause-effect chains that static UI cannot — users orient 40% faster in animated navigation transitions vs cut transitions (UX in Motion, 2017); Vestibular Disorders Association (2022) identifies uncontrolled website animation as a top-3 trigger for vestibular symptoms (dizziness, nausea) — estimated 35% of adults over 40 have experienced vestibular dysfunction, making `prefers-reduced-motion` a medical accessibility requirement, not a preference
**Why best:** Decorative animation (animation without a functional role) degrades performance, increases perceived cognitive load, and can cause harm — the alternative of no animation is better than animation without purpose; purposeful animation (communicating state change, spatial context, feedback) earns its performance cost

Sources: Google Material Design 3 "Motion" (m3.material.io, 2022); Apple HIG "Animation" (developer.apple.com, 2023); Val Head "Designing Interface Animation" (Rosenfeld Media, 2016); Willenskomer "12 Principles of UX in Motion" (Medium, 2017); Vestibular Disorders Association "Dizziness and Motion Sickness" (vestibular.org, 2022)

## Steps

### 1. Define the functional purpose before animating

Every animation must serve at least one of four functional roles:

| Role | What it communicates | Example |
|------|---------------------|---------|
| **Orient** | Spatial relationship — where something came from or went to | Page slide transition (right → left = forward navigation) |
| **Feedback** | Confirmation that an action was received | Button press ripple, checkbox check animation |
| **Direct attention** | Draws eye to a new, important element | Notification badge pulse, new message highlight |
| **Delight** | Reward for completion — used sparingly | Success state confetti, onboarding celebration |

If an animation doesn't serve one of these roles, remove it. Decorative animation is not a valid use case.

Ask: "What does the user learn from this motion that they couldn't learn from a static state change?"

### 2. Choose duration based on animation type

Duration is the most common motion design mistake. Animations that feel sluggish or jarring almost always have incorrect duration:

| Animation type | Duration range | Rationale |
|----------------|---------------|-----------|
| **Micro-interactions** (button press, checkbox, toggle) | 100–200ms | Faster than perception threshold for "snap" — feels immediate |
| **Component transitions** (dropdown open, modal appear, tooltip) | 200–300ms | Visible but not slow; matches natural eye movement speed |
| **Page / view transitions** | 300–500ms | Needs enough time to communicate spatial context |
| **Complex choreography** (multi-element staggered entrance) | 400–600ms per sequence | Each element 50–80ms staggered after the previous |
| **Never** | > 700ms for UI animations | Users perceive this as slow loading, not design |

Material Design's duration tokens:
```
--md-sys-motion-duration-short1: 50ms   (exit/fade of small elements)
--md-sys-motion-duration-short2: 100ms
--md-sys-motion-duration-medium1: 200ms
--md-sys-motion-duration-medium2: 300ms
--md-sys-motion-duration-long1:  400ms  (complex page transitions)
--md-sys-motion-duration-long2:  500ms
```

### 3. Apply the correct easing function

Easing determines whether motion feels natural or mechanical:

| Easing | CSS value | Use for |
|--------|-----------|---------|
| **Ease-out** (fast start, slow finish) | `cubic-bezier(0.0, 0.0, 0.2, 1)` | **Entering elements** — fast arrival feels intentional |
| **Ease-in** (slow start, fast finish) | `cubic-bezier(0.4, 0.0, 1, 1)` | **Exiting elements** — quick departure avoids dragging |
| **Ease-in-out** (slow-fast-slow) | `cubic-bezier(0.4, 0.0, 0.2, 1)` | **Elements that move across the screen** — natural arc |
| **Linear** | `linear` | **Loops and spinners only** — linear feels mechanical for one-shot transitions |

**Material Design standard easing:** `cubic-bezier(0.2, 0, 0, 1)` — used for most container transitions.

**Never use `ease` (CSS default):** CSS `ease` is `cubic-bezier(0.25, 0.1, 0.25, 1)` — a compromise that feels neither intentional nor natural. Use a specific easing token.

### 4. Animate only performant CSS properties

Properties that trigger layout or paint cause jank — the animation drops frames:

```
❌ Jank-causing properties (avoid animating):
   width, height, margin, padding, top, left, right, bottom
   font-size, border-width, box-shadow (partially)

✅ GPU-composited properties (safe to animate):
   transform: translate(), scale(), rotate()
   opacity
   filter (modern browsers, with caveats)

Example:
❌  .panel { transition: height 300ms; }           /* triggers layout */
✅  .panel { transition: transform 300ms; }        /* GPU-composited */
    .panel.open { transform: scaleY(1); }
    .panel.closed { transform: scaleY(0); transform-origin: top; }
```

**Use `will-change: transform` only when needed:** `will-change` promotes an element to its own compositor layer — useful for complex animations, costly for static elements. Add it immediately before an animation starts (via JS), remove it after.

### 5. Implement `prefers-reduced-motion` support

This is a medical accessibility requirement, not a preference:

```css
/* Base: full animation */
.modal {
  transition: opacity 300ms ease-out, transform 300ms ease-out;
}

/* Reduced motion: instant state change */
@media (prefers-reduced-motion: reduce) {
  .modal {
    transition: none;
  }
}
```

**What to keep vs remove under reduced motion:**

| Keep | Remove / replace |
|------|-----------------|
| Instant state changes (show/hide) | All transitions and animations |
| Color changes (hover, active states) | Scroll-triggered animations |
| Static focus indicators | Parallax effects |
| Functional feedback (spinners) | Auto-playing motion |

**Test:** In macOS: System Settings → Accessibility → Display → Reduce Motion. In Windows: Settings → Ease of Access → Display → Show animations. Verify the experience is fully functional with all motion disabled.

### 6. Define choreography for multi-element animations

When multiple elements animate together, choreography determines which animates first:

```
Entrance: hero content first → supporting content after
  [Heading appears] → [Body text fades in 80ms later] → [CTA appears 80ms later]

Exit: reverse order — supporting content first, primary last
  [CTA fades out] → [Body text fades 80ms later] → [Heading exits 80ms later]

Stagger delay: 50–80ms per element
```

**Never animate all elements simultaneously at identical duration** — it looks like a PowerPoint transition, not a designed animation.

**Never stagger more than 5 elements** — beyond 5, the sequence feels like a loading delay, not choreography.

### 7. Test on low-end devices

Animations that run at 60fps on a MacBook Pro may drop to 20fps on a mid-range Android phone. Required testing:

- Open Chrome DevTools → Performance → CPU throttle 4× → record the animation
- Target: 60fps sustained (16ms per frame budget)
- If animation drops below 60fps on 4× throttle, simplify or remove

**Lighthouse animation audit:** Lighthouse flags "Avoid non-composited animations" as a performance issue — use this as a CI gate.

## Rules

- Every animation must serve one of four roles: orient, feedback, direct attention, or delight — remove decorative animation
- Duration: micro-interactions 100–200ms; component transitions 200–300ms; page transitions 300–500ms; never > 700ms
- Ease-out for entering elements; ease-in for exiting — never CSS default `ease`
- Animate only `transform` and `opacity` in performance-critical animations — no width, height, margin, or padding
- `prefers-reduced-motion: reduce` must disable all transitions and animations — instant state changes remain
- Test on low-end hardware (4× CPU throttle) before shipping animated components

## Common Mistakes

- **Duration too long**: a 700ms modal open feels like the UI is broken; 300ms feels designed; 100ms feels instant. When in doubt, cut duration in half
- **Easing not set**: CSS default `ease` on every transition — elements feel neither fast nor intentional; define explicit easing tokens
- **Layout-triggering properties**: animating `height` from 0 to auto causes layout thrash and jank; use `transform: scaleY()` or `max-height` with overflow:hidden instead
- **No prefers-reduced-motion**: shipping animated UIs without reduced-motion support causes vestibular symptoms in a measurable portion of the user base; it is a medical accessibility requirement
- **Decorative animation everywhere**: multiple background gradients shifting, floating particle effects, constant micro-animations — no single animation has a cost, but aggregate decorative motion degrades focus and perceived performance

## When NOT to Use

- When the UI is primarily data-dense or task-focused (admin dashboards, spreadsheet tools, data tables) — animation overhead reduces the efficiency that power users depend on; a preference for reduced motion is common among power users even without vestibular conditions
- When performance budget is already at limit — a loading experience that is already slow should not add animation; improve load performance first; animation cannot mask real slowness

