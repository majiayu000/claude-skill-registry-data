---
name: motion-engine
description: Use when a web project needs animation or motion-tool selection across native CSS/WAAPI/View Transitions, Motion, Anime.js, GSAP, Lenis, scroll choreography, SVG/text animation, or synchronized motion systems.
metadata:
  short-description: Route native motion, Motion, Anime.js, GSAP and Lenis
---

# Motion Engine

## Rule: intent first, engine second

Read `references/tool-router.md` and `references/capability-matrix-2026.md` and choose the smallest engine that cleanly implements the interaction.

### Native first
Use CSS transitions/keyframes, WAAPI, CSS Scroll-Driven Animations or View Transitions when they cover the behavior cleanly.

### Motion
Prefer for React state/layout/shared-layout, presence, gestures, springs and common scroll-linked UI motion. Read `references/motion.md`.

### Anime.js
Prefer for precise lightweight timelines, staggered choreography, SVG/text/value animation and deterministic sequencing. Read `references/animejs.md`.

### GSAP
Prefer for advanced multi-part timelines, ScrollTrigger pin/scrub, Flip, SplitText, MotionPath and complex scroll/DOM/3D orchestration. Read `references/gsap-lenis.md`.

### Lenis
Use only when smooth scrolling or a normalized scroll signal is an intentional part of the experience. Native scroll remains the default.

## Cross-engine discipline

- Do not install two engines that solve the same job unless distinct capabilities are actively used.
- If multiple systems animate in the same frame, coordinate update loops rather than creating uncontrolled RAF competition.
- Preserve logical state when motion is disabled.
- Keep transform/opacity animation compositor-friendly where possible; avoid layout thrash in scroll handlers.
- Pause offscreen or nonessential animation.

## Output

For notable motion, record: `Intent → Engine → Why → Reduced-motion behavior → Performance risk`.
