---
license: Apache-2.0
name: motion-design-web
description: Motion design and micro-animations for web interfaces — Framer Motion layout animations, CSS scroll-driven animations, View Transitions API, GSAP ScrollTrigger, spring physics tuning, loading choreography, and Disney's 12 principles applied to UI. Makes interfaces feel alive without feeling busy. Activate on 'web animation', 'Framer Motion', 'micro-interaction', 'scroll animation', 'page transition', 'View Transitions API', 'spring animation web', 'motion design', 'loading animation', 'skeleton screen', 'hover effect', 'GSAP ScrollTrigger'.
allowed-tools: Read,Write,Edit,Glob,Grep,WebSearch,WebFetch
metadata:
  category: Design & UX
  tags:
    - animation
    - motion-design
    - framer-motion
    - css-animations
    - gsap
    - micro-interactions
    - page-transitions
    - scroll-driven
  pairs-with:
    - skill: react-performance-optimizer
      reason: Animations must not compromise render performance
    - skill: web-design-expert
      reason: Motion serves the visual design, not the other way around
    - skill: hero-section-design
      reason: Hero sections rely heavily on entrance animations and scroll effects
    - skill: native-app-designer
      reason: Shared principles of spring physics and interaction feedback
category: Design & Creative
tags:
  - motion-design
  - animation
  - web
  - transitions
  - ux
---

# Motion Design for Web

Motion is the invisible layer between good design and great design. When done right, users don't notice the animations — they notice the app feels responsive, alive, intentional. When done wrong, they notice that something is bouncing and they wish it would stop.

## Decision Points

### Library Selection by Complexity/Performance
```
Project Requirements → Library Choice
├── Simple transitions (hover, fade, slide)?
│   └── Use CSS transitions/animations
│       - Low bundle size impact
│       - Hardware accelerated
│       - Good enough for 80% of needs
├── Layout animations, gesture handling, or complex sequences?
│   ├── React project?
│   │   └── Use Framer Motion
│   │       - Layout animations automatic
│   │       - AnimatePresence for mount/unmount
│   │       - Spring physics built-in
│   └── Vanilla JS or non-React?
│       └── Use GSAP
│           - Maximum control and performance
│           - ScrollTrigger for scroll effects
│           - Complex timeline orchestration
├── Scroll-driven effects only?
│   ├── Browser support modern (Chrome 115+)?
│   │   └── Use CSS scroll-driven animations
│   │       - Zero JavaScript overhead
│   │       - Runs off main thread
│   └── Need older browser support?
│       └── Use GSAP ScrollTrigger
└── Cross-page transitions?
    ├── Shared elements between pages?
    │   └── Use View Transitions API
    │       - Browser handles morphing automatically
    │       - Fallback to regular page load
    └── Simple page-level effects?
        └── CSS animations with navigation events
```

### Timing Decision Tree
```
Animation Purpose → Duration Range
├── Instant feedback (hover acknowledgment)?
│   └── 100-150ms with ease-out
├── State change confirmation (toggle, selection)?
│   └── 200-250ms with ease-in-out
├── Content reveal (dropdown, accordion)?
│   └── 300-400ms with spring physics
├── Major context change (modal, page)?
│   └── 400-600ms with anticipation + follow-through
└── Background activity (loading, progress)?
    └── 1.5-2s cycle or tied to actual progress
```

### Spring Physics Tuning
```
Interaction Type → Spring Config
├── Snappy UI controls (buttons, switches)?
│   └── stiffness: 400, damping: 28
├── Smooth panels (modals, cards)?
│   └── stiffness: 200, damping: 24
├── Playful elements (success animations)?
│   └── stiffness: 300, damping: 15 (more bounce)
├── Heavy elements (full-page sheets)?
│   └── stiffness: 120, damping: 20, mass: 1.5
└── Gesture-driven (drag, swipe)?
    └── stiffness: 300, damping: 20, velocity inheritance
```

## Failure Modes

### Layout Thrashing Jank
**Detection:** Animation drops below 60fps, DevTools Performance tab shows purple "Layout" blocks during animation
**Symptoms:** Choppy motion, especially on slower devices; scrolling feels laggy during transitions
**Root Cause:** Animating properties that trigger layout recalculation (width, height, margin, padding, top, left)
**Fix:** Only animate transform, opacity, filter, clip-path; use transform: scale() instead of width/height changes

### Spring Oscillation Hell
**Detection:** Elements bounce for >1 second after interaction; users wait for UI to settle before next action
**Symptoms:** Damping too low (<15) or stiffness too high (>500) with low damping; feels like everything is made of jello
**Root Cause:** Misunderstanding that lower damping = more bounce = longer settle time
**Fix:** Keep damping ≥20 for interactive elements; test on actual devices, not fast desktop; use duration-based transitions for predictable timing

### Animation Soup Chaos
**Detection:** Multiple elements animating simultaneously with no clear visual hierarchy; user doesn't know where to look
**Symptoms:** Everything moves at once on page load; competing animations fight for attention
**Root Cause:** Ignoring Disney's "staging" principle; treating each animation in isolation
**Fix:** Stagger children by 40-80ms; animate hero/primary element first; max 1-2 simultaneous animation groups

### Accessibility Violation Seizures
**Detection:** No @media (prefers-reduced-motion) styles; animations run at full intensity for all users
**Symptoms:** User reports motion sensitivity issues; fails accessibility audits
**Root Cause:** Treating reduced motion as optional nice-to-have instead of legal/safety requirement
**Fix:** Always provide crossfade or instant alternatives; test with prefers-reduced-motion: reduce enabled

### Bundle Bloat Performance Hit
**Detection:** Animation library adds >50KB to bundle; first-page animations cause layout shift or delay
**Symptoms:** Slow initial page load; animations start late after JavaScript parses
**Root Cause:** Loading heavy animation library for simple transitions; not code-splitting animation features
**Fix:** Use CSS for simple effects; lazy-load Framer Motion/GSAP; inline critical animation CSS; measure Core Web Vitals impact

## Worked Examples

### Example: Card Hover with Performance Monitoring
**Scenario:** Product card needs hover effect that feels premium but performs well on mobile.

**Novice approach:**
```css
.card:hover {
  width: 102%;
  height: 102%;
  margin-top: -4px;
  border-width: 2px;
}
```

**Expert analysis:** This will trigger layout recalculation on every frame. Width/height changes force reflow. Border-width change affects box model.

**Expert solution with decision points:**
1. **Library choice:** CSS only (simple hover state, no React needed)
2. **Properties:** Transform + box-shadow only (GPU-composited)
3. **Timing:** 200ms ease-out (quick acknowledgment, not dramatic)
4. **Accessibility:** Honor reduced motion preference

```css
.card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
  will-change: transform; /* Hint for layer promotion */
}

.card:hover {
  transform: translateY(-4px) scale(1.01); /* Lift + subtle scale */
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08); /* Depth increase */
}

@media (prefers-reduced-motion: reduce) {
  .card {
    transition: box-shadow 200ms ease-out; /* Keep depth change, remove movement */
  }
  .card:hover {
    transform: none; /* No movement for motion-sensitive users */
  }
}
```

**Performance validation:** DevTools Performance tab shows no Layout blocks during hover, maintains 60fps on mid-range mobile device.

## Quality Gates

- [ ] **FPS Target:** Animation maintains 60fps on mid-range device (test on throttled Chrome DevTools CPU)
- [ ] **Duration Range:** Interactive animations between 100-500ms; background animations <2s cycles
- [ ] **Overshoot Bounds:** Spring animations settle within 0-10% overshoot; damping ≥20 for UI controls
- [ ] **Reduced Motion:** @media (prefers-reduced-motion: reduce) provides crossfade or instant alternatives
- [ ] **GPU Properties Only:** Only transform, opacity, filter, clip-path animated; zero Layout/Paint in DevTools Performance
- [ ] **Stagger Hierarchy:** Groups use 40-80ms stagger delays; primary element animates first
- [ ] **Bundle Impact:** Animation libraries lazy-loaded or <20KB for critical path; CSS-only when sufficient
- [ ] **Focus Accessibility:** All interactive animations include focus-visible states with smooth transitions
- [ ] **Spring Settle Time:** Physics-based animations complete within 600ms for interactive elements
- [ ] **Cross-Browser Fallbacks:** Graceful degradation for unsupported features (View Transitions, scroll-driven)

## NOT-FOR Boundaries

**Do NOT use this skill for:**
- Canvas/WebGL animations → Use `threejs-expert` for 3D graphics and particle systems
- SVG illustration animation → Use After Effects + Lottie or dedicated SVG animation libraries
- Video editing or motion graphics production → Use video editing tools, not web animation APIs
- Native mobile animations → Use `ios-app-beauty` for SwiftUI or Android animation systems
- Game animations → Use game engines; web animation APIs not optimized for 60+ entity coordination

**Delegate to other skills:**
- Performance optimization → Use `react-performance-optimizer` for bundle analysis and render optimization
- Complex scroll interactions → Use `scroll-experience-designer` for scroll-jacking and custom scroll behaviors
- Design systems → Use `design-system-architect` for consistent animation tokens and guidelines