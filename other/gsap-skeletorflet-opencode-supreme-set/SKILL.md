---
name: gsap
description: GSAP — high-performance animation library for the web with timelines, tweens, ScrollTrigger, and utility plugins.
---

### tweens
`gsap.to(el, { x: 100, duration: 1 })` — animate FROM current state TO target. `gsap.from()` — animate FROM a state TO current. `gsap.fromTo()` — explicit start/end. All return a Tween instance.

### timeline
`gsap.timeline({ defaults: { duration: 0.5 } })`. Chain `.to()`, `.from()`, `.fromTo()`. Position parameter: `"+=0.2"` (after), `"-=0.1"` (overlap), `"<"` (at start), `">"` (at end).

### easing
Built-in: `"power2.out"`, `"back.inOut"`, `"elastic.out(1, 0.5)"`, `"bounce.out"`. Custom: `"M0,0 C0.25,0.1 0.25,1 1,1"` (cubic bezier). `SlowMo`, `SteppedEase` via utils.

### ScrollTrigger
`scrollTrigger: { trigger: ".el", start: "top center", end: "bottom top", scrub: true }`. Pin elements, toggle classes, snap to sections. `ScrollTrigger.create()` for manual control. `matchMedia()` for responsive.

### MotionPath
Plugin: `gsap.to(el, { motionPath: { path: "#path", align: true, autoRotate: true } })`. Animate along SVG path or array of points. Control offset, align, rotation.

### staggers
`gsap.to(".box", { y: 50, stagger: 0.1 })`. Options: `each`, `from` ("start"/"end"/"center"), `grid` (auto, auto), `amount` (total). Eased staggers with `ease: "power1.inOut"`.

### Draggable
`Draggable.create(".el", { type: "x,y", bounds: ".container" })`. Inertia snapping, liveSnap, onDrag callbacks. Combine with ThrowProps for momentum.

### performance
Use `will-change: transform` on animated elements. Animate `transform`/`opacity` only. Cache selector results. Use `gsap.quickTo()` for mouse-driven perf. `gsap.ticker.lagSmoothing()`.
