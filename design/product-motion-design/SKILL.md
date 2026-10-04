---
name: product-motion-design
description: Design, implement, audit, or repair purposeful motion for React and web interfaces, including GSAP timelines, scroll choreography, micro-interactions, and optional Three.js scenes, with cleanup, responsive behavior, reduced-motion support, and browser verification.
---

# Product Motion Design

Use motion to explain hierarchy, causality, state, and spatial relationships. Do not animate a page merely to make it look expensive.

## Workflow

1. Identify the user task, focal action, state changes, and moments where motion can improve comprehension.
2. Define a motion hierarchy: page entrance, section reveal, component transition, feedback, and ambient motion.
3. Choose the lightest mechanism that fits: CSS for simple states, the existing React animation library for component lifecycle, GSAP for coordinated timelines or scroll, and Three.js only for a real 3D requirement.
4. Establish duration, easing, distance, stagger, interruption, and reduced-motion rules before implementation.
5. Scope animation selectors to component roots. Register plugins once and clean timelines, observers, listeners, frames, geometries, materials, textures, and renderers on teardown.
6. Keep layout stable. Animate transform and opacity where possible; avoid perpetual main-thread work and broad `transition: all`.
7. Adapt density and choreography for touch, narrow containers, low-power devices, and hidden tabs.
8. Verify real pixels, interaction, resize behavior, and nonblank canvas output at mobile and desktop widths.

## Motion Rules

- Interaction feedback is immediate; decorative motion yields to input.
- Scroll animation must preserve reading order and usable content without JavaScript.
- Repeated lists use restrained stagger and a cap; they do not replay on every tiny scroll.
- 3D scenes cap pixel ratio, pause when hidden, resize from the actual container, and provide a static reduced-motion frame.
- Theme changes must update 3D materials and backgrounds without making the focal object disappear.
- Do not add cursor-following effects to touch-only experiences or controls requiring precision.

## Delivery Contract

Return or implement:

1. **Motion intent** - what each animation communicates.
2. **Choreography** - triggers, sequence, timings, and interruption behavior.
3. **Implementation** - scoped code using the existing stack.
4. **Performance contract** - cleanup, device adaptation, and rendering budget.
5. **Accessibility** - reduced-motion and no-JavaScript behavior.
6. **Proof** - browser observations or screenshots at relevant states and viewports.

## Reference

Read [references/motion-checklist.md](references/motion-checklist.md) before shipping GSAP, scroll-linked, or Three.js work.
