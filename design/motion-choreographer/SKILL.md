---
name: motion-choreographer
description: Design or repair website motion such as scroll choreography, page transitions, reveals, gestures, or kinetic type. Use when timing and continuity are the main problem; use accessible-interaction-systems for component semantics and immersive-3d-web or shader-web-art for GPU-led scenes.
---

# Motion Choreographer

Build a coherent motion language whose timing, direction, continuity, and interaction all serve the content.

## Start by classifying the job

1. **Microinteraction:** hover, press, focus, toggle, menu, tooltip, cursor feedback.
2. **Entrance/reveal:** section, text, image, card, media.
3. **Layout continuity:** card-to-detail, shared element, expanding media, reordering.
4. **Scroll-triggered:** play when entering/leaving viewport.
5. **Scroll-linked:** animation progress follows scroll.
6. **Pinned narrative:** context stays fixed while content evolves.
7. **Page transition:** route/view continuity.
8. **Gesture/drag:** carousel, scrubbing, object control.
9. **Kinetic typography:** split/mask/path/scramble/type transformation.
10. **Cross-system choreography:** DOM + canvas/3D sync; hand off to a 3D/shader specialist when the GPU side dominates.

If work arrives from `creative-web-studio`, preserve its experience thesis, scene purpose, rendering boundary, variants, budgets, and acceptance criteria. Resolve missing trigger/state/cleanup details before choosing an engine. Return changed assumptions explicitly rather than silently rewriting the direction.

## Choose one primary engine

Use `references/library-decisions.md`.

Default hierarchy:
- native CSS/WAAPI/Scroll-driven Animations/View Transitions for simple effects
- Motion for React for component/layout/gesture-centric React work
- GSAP for complex deterministic timelines, ScrollTrigger, FLIP, SVG, and pinned narratives
- Lenis only as an optional scroll transport layer
- Barba.js for lifecycle/page-transition orchestration on classic multi-page/MPA sites; it is not the animation engine itself
- Rive for state-machine-driven authored vector interaction; Lottie/dotLottie for authored timeline vector playback

Do not use multiple animation libraries for the same responsibility.

## Define motion grammar before code

Create 2–4 motifs and a small timing system. Example:
- fast feedback: 120–200ms
- UI transition: 200–380ms
- editorial reveal: 450–850ms
- major scene transition: 700–1400ms
- scrubbed sequences: progress-based, not duration-based

Tune to the concept. Avoid bounce unless it belongs to the brand.

For each animation document:
`trigger → from → to → duration/progress → easing → stagger → cleanup/reverse → reduced motion`.

## Scroll choreography rules

- Use trigger when the visitor only needs an entrance/reveal.
- Use scrub when progress communicates transformation, comparison, sequence, or spatial movement.
- Use pin only when keeping context helps understanding.
- Keep pinned distance as short as the content allows.
- Make reverse scroll restore states reliably.
- Avoid reading long text while its container is moving continuously.
- Use parallax to express hierarchy/depth, not random speed offsets.

## GSAP implementation rules

- Register plugins explicitly.
- Scope selectors/contexts to the component.
- Create timelines in lifecycle-safe setup and revert/kill on cleanup.
- Avoid creating ScrollTriggers repeatedly during React renders.
- Refresh after layout/media changes that affect trigger positions.
- Use transform/opacity for continuous motion where possible.
- Use FLIP for continuity between layout states rather than manually guessing coordinates.
- Integrate Lenis with one animation ticker; avoid dueling RAF loops.

## Motion for React implementation rules

- Use variants for shared state and orchestration.
- Use `layout` / `layoutId` for structural continuity.
- Use `AnimatePresence` for exit states.
- Use MotionValues for high-frequency animated values instead of React state.
- Use `useScroll` + transforms for scroll linkage.
- Use `useReducedMotion` and design an alternate experience.
- Lazy-load motion features when bundle sensitivity matters.

## Authored animation runtimes

Use Rive when a designer-authored interactive graphic needs explicit states/data binding, hover/press/scroll-driven state changes, or richer runtime logic. Isolate the runtime in a component, clean it up correctly, and pause it when offscreen where practical.

Use Lottie/dotLottie for exported vector timeline animation when state-machine logic is unnecessary. Do not autoplay many looping animations simultaneously; lazy-load and pause offscreen.

Use Barba.js only for navigation lifecycle and page-container swapping on sites where that architecture fits. Put animation in GSAP/Anime/CSS or another chosen engine, and put page-specific setup/teardown in Barba views/hooks. In React/Next routers, prefer framework-native routing/view-transition patterns unless there is a compelling migration reason.

## Native motion rules

Prefer CSS `animation-timeline` / view-progress timelines when support and fallback requirements fit. Use View Transitions for shared navigation continuity where appropriate. Keep a non-animated fallback.

Read [modern motion support](references/modern-motion-support.md) before choosing scroll timelines or View Transitions for a public site.

## Text motion

Text must become readable quickly. Animate masks/lines/words for rhythm but do not make visitors wait through decorative sequencing. Preserve screen-reader semantics; do not convert meaningful text into canvas-only glyphs.

## Interaction states

Design idle, hover, focus-visible, press, active/selected, disabled, loading, and touch alternatives where relevant. Hover is enhancement, not the only way to discover an action.

## Reduced motion

Reduced motion must be intentionally designed. Prefer opacity/color/cut transitions, shorter distances, no continuous parallax, no large zooms, no camera-like movement, and minimal pin/scrub. See `references/reduced-motion.md`.

## Showcase-driven comparison

When inspiration is requested, compare 2–3 interaction references using trigger, start/end state, continuity object, easing character, mobile translation, and reduced-motion translation. Then recommend one pattern adapted to the project.

## Deliverables

Depending on request, output:
- motion audit + prioritized fixes
- motion tokens and grammar
- scene/interaction choreography table
- library choice with reasoning
- React/Next implementation code
- a prompt for a coding agent
- reduced-motion and mobile variants

For implementation work, include proof for the primary interaction: initial state, completed state, reverse/cleanup behavior, narrow viewport, keyboard or touch alternative, and reduced-motion result. Report observed behavior separately from unverified assumptions.

## Examples and showcase calibration

Read `references/examples.md` when selecting a choreography pattern or producing a motion specification. Read `references/showcase.md` when the user asks for inspiration or reference-quality interactions. Extract trigger/state/continuity/mobile/reduced-motion logic rather than copying surface effects.

## References
- `references/examples.md`
- `references/showcase.md`
- `references/library-decisions.md`
- `references/pattern-cookbook.md`
- `references/reduced-motion.md`
- `references/modern-motion-support.md`
