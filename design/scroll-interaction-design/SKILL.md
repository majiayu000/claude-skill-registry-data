---
name: scroll-interaction-design
description: Design and implement high-quality scroll-triggered animation, parallax scrolling, smooth scroll, interactive scrolling, sticky scenes, scrollytelling.
---

# Scroll Interaction Design

## Codex Runtime Notes

Use Codex-native mechanisms, project conventions, and browser testing. Pair this skill with frontend, Figma, Three.js, native UI, or testing skills only when those skills fill separate responsibilities.

## Purpose

Build scroll and motion experiences that feel intentional, performant, accessible, and production-ready. This skill covers web and app interfaces, including scroll-triggered reveals, parallax, smooth scrolling, interactive storytelling, sticky/pinned sections, 3D canvas scenes, and native gesture-linked motion.

## Use This Skill When

- The user asks for scroll-triggered animation, parallax, smooth scroll, interactive scrolling, animated scroll storytelling, sticky scenes, or scroll progress effects.
- A web page or app should feel premium, cinematic, playful, spatial, or motion-rich.
- A 3D or WebGL scene needs to respond to scroll.
- A mobile/native app needs scroll-linked gestures, collapsing headers, animated cards, image depth, or carousel motion.
- Existing UI motion feels flat, janky, excessive, inaccessible, or visually generic.

## Routing With Other Skills

Use this skill as the motion interaction owner. Combine narrowly:

| Need | Pair With |
| --- | --- |
| Build a web app/page | frontend app or React skill |
| Audit taste and restraint | `design-motion-principles` or `design-taste-frontend` |
| Implement 3D canvas | Three.js or project frontend skill |
| Implement native/mobile | `building-native-ui`, `android-development`, or platform skill |
| Verify in browser | browser testing skill |
| Convert Figma to motion UI | Figma implementation skill plus this skill |

Do not load several broad animation or design skills together unless comparing alternatives is the explicit task.

## Decision Tree

1. Identify the product context.
   - SaaS/dashboard: quiet, fast, restrained motion.
   - Portfolio/brand/product showcase: expressive scroll scenes and depth are acceptable.
   - Game/kids/creative: playful motion can be primary.
   - Enterprise/internal tool: motion supports orientation and feedback only.

2. Choose the scroll mechanism.
   - CSS scroll-driven animations for simple progress, reveal, sticky-card, and parallax effects when browser support fits.
   - IntersectionObserver plus CSS transitions for robust reveal-on-enter effects.
   - Motion for React `useScroll` when React state, transforms, and component composition are central.
   - GSAP ScrollTrigger for complex pinned timelines, scrubbed choreography, and art-directed sequences.
   - Three.js for real 3D camera/object motion, shaders, particles, or spatial scenes.
   - React Native Reanimated or platform-native animation APIs for mobile app scroll gestures.

3. Define the motion map before coding.
   - Which section owns scroll height?
   - Which elements are pinned or sticky?
   - Which values map from progress 0 to 1?
   - Which effects are transform-only, opacity-only, or GPU-friendly?
   - What is the reduced-motion fallback?

4. Implement in layers.
   - Static layout first.
   - Scroll progress and section measurement second.
   - Motion mapping third.
   - 3D/canvas effects only after layout works.
   - Responsive and reduced-motion behavior last.

5. Verify on real viewports.
   - Desktop and mobile.
   - Reduced motion enabled.
   - Slow CPU or heavy page conditions when possible.
   - Keyboard navigation and focus through pinned/smoothed sections.

## Motion Quality Rules

- Every animation needs a job: orientation, causality, hierarchy, feedback, storytelling, or delight.
- Avoid motion that fights scroll. User drag should feel in control.
- Prefer `transform`, `opacity`, and carefully used `filter` or `clip-path`. Avoid scroll-linked layout changes such as `top`, `left`, `width`, and `height` unless necessary.
- Use fewer large movements on productivity and operational UIs.
- Use parallax depth subtly: background moves slow, foreground moves faster, text remains readable.
- Pinned sections need enough scroll distance to complete the animation without trapping the user.
- Smooth scrolling must not break native scroll, focus, anchor links, keyboard navigation, or mobile touch expectations.
- 3D scenes must have a nonblank loading/fallback state and should not block page content.
- Never rely on motion as the only way to communicate meaning.

## Required Accessibility Rules

- Always support reduced motion.
- On web, use `@media (prefers-reduced-motion: reduce)` and disable or simplify large scroll-linked transforms.
- In React/native apps, read the platform reduced-motion signal when available.
- Replace large camera moves, scale jumps, and fast parallax with fades, static states, or shorter transforms.
- Keep content reachable with keyboard and screen readers even inside pinned or smooth-scrolled sections.

## Reference Loading

Read these files only when needed:

- `references/implementation-patterns.md`: read before implementing a concrete web, React, GSAP, Three.js, or native scroll-motion feature.
- `references/validation-checklist.md`: read before finalizing or after changing motion code.
- `references/research-basis.md`: read when updating this skill, choosing between APIs, or explaining the technical basis.

## Implementation Output Expectations

When building a scroll-motion interface:

1. State the chosen mechanism in one sentence when it affects dependencies or architecture.
2. Build the actual usable screen first, not a marketing explanation page.
3. Include responsive behavior and reduced-motion fallback.
4. Test visually in browser when this is a web target and the local app can run.
5. Fix jank, overlap, clipped text, blank canvas, or mobile scroll traps before finishing.

## Anti-Patterns

- Adding parallax because the page feels empty.
- Combining smooth-scroll libraries, ScrollTrigger, and custom scroll event loops without a clear owner.
- Updating React state on every scroll frame for visual transforms.
- Pinning long sections without enough scroll distance or exit affordance.
- Putting every section in floating cards just to create depth.
- Using 3D canvas as a decorative box when it should be immersive or functional.
- Ignoring mobile touch behavior.
- Shipping without reduced-motion behavior.
- Declaring victory from code review only; scroll motion needs visual/runtime verification.

## Changelog

- [2026-05-11] Initial Codex version: added scroll, parallax, smooth scrolling, interactive scrolling, 3D/WebGL, native app motion workflow, references, accessibility rules, and validation expectations.
