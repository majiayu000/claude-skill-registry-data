---
name: creative-web
description: Use when the design concept calls for Three.js or React Three Fiber 3D, WebGL/WebGPU, Rive, Spline, Theatre.js, SVG, canvas, shaders, particle systems, or other immersive creative-web techniques.
metadata:
  short-description: Route 3D, WebGL, Rive, Spline and creative effects
---

# Creative Web

## Entry criterion

Creative technology must communicate product meaning, spatial information, material character, or memorable brand identity. Decorative complexity alone is not sufficient.

## Router

Read `references/capability-matrix-2026.md` first. Read `references/three-r3f.md` for programmable 3D and `references/rive-spline-theatre.md` for authored interactive assets/timelines.

- Three.js: low-level scene/render/shader control.
- React Three Fiber: React-native Three.js scene architecture.
- Rive: interactive vector animation and state machines.
- Spline: designer-authored 3D scenes and web integration.
- Theatre.js: timeline authoring and synchronized scene/property animation.
- SVG: first choice for many crisp illustrative/mask/path effects.
- Canvas/shader: custom computation when visual behavior cannot be expressed cleanly in DOM/SVG.

## Progressive enhancement contract

- Essential text, navigation and controls stay in semantic DOM.
- Define a still/static fallback for 3D/canvas/vector scenes.
- Degrade particle count, DPR, post-processing, shadows and continuous loops on constrained devices.
- Lazy-load heavy scenes below the fold or behind interaction.
- Stop or reduce rendering when offscreen.
- Respect reduced motion.

## Acceptance

The creative layer must strengthen the design POV enough to justify load, runtime and QA cost.
