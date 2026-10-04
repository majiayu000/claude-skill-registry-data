---
name: shader-web-art
description: Design or debug a GPU visual effect when shader math, textures, particles, or DOM-to-canvas synchronization is the main challenge. Use for WebGL/GLSL image and field effects; use immersive-3d-web when a navigable 3D scene is central.
---

# Shader Web Art

Create GPU effects that express the concept. Avoid generic “noise + chromatic aberration + bloom” unless those behaviors are semantically justified.

## Classify the effect

- image displacement / hover distortion
- mask reveal / dissolve / erosion
- refraction / glass / lensing
- grain / dither / halftone
- flow field / particles
- metaballs / signed-distance shapes
- feedback/trails
- DOM-aligned image/video planes
- procedural background
- text-as-texture effect
- post-processing pass
- WebGPU compute/render experiment

If the effect comes from `creative-web-studio`, preserve its thesis, scene purpose, semantic base layer, variants, budgets, and acceptance criteria. Describe the effect as a signal chain before writing shader code: inputs → coordinate transform → visual operation → composite → interaction driver → fallback.

## Choose the smallest runtime

- CSS/SVG filter if enough
- Canvas 2D for simple procedural draw
- PixiJS for sprite-heavy GPU 2D
- Curtains.js for DOM-aligned media shader treatment
- OGL for lean custom WebGL scenes
- Three.js/R3F when the effect belongs inside a broader 3D scene
- WebGPU/WGSL only with explicit capability detection and fallback

## Shader design workflow

1. Define the visual metaphor and input variables.
2. Build a static shader that renders correctly.
3. Add one time-varying dimension.
4. Add pointer/scroll/audio data only when necessary.
5. Normalize coordinates and aspect-ratio handling.
6. Clamp input ranges and avoid unstable singularities.
7. Profile fill-rate, resolution, texture samples, branches, loops, and overdraw.
8. Design reduced-motion/static fallback.

## Uniform contract

Prefer a small predictable uniform set:
- `uTime`
- `uResolution`
- `uPixelRatio` or render resolution scale
- `uPointer` normalized
- `uScroll` / `uProgress`
- `uTexture*`
- concept-specific parameters

Do not expose dozens of magic uniforms with no design system.

## DOM ↔ WebGL synchronization

For DOM-aligned planes:
- read bounding boxes at controlled times, not every frame without reason
- update on resize/scroll through a coordinated scheduler
- preserve object-fit/crop math
- match border radius/masks deliberately
- keep semantic image/text in DOM when it matters
- canvas becomes enhancement, not the only source of content

See `references/dom-webgl-sync.md`.

## Particles

Use instancing/point sprites/GPU computation where scale demands it. Particles need a story: assemble, disperse, reveal data, express atmosphere, or respond to interaction. Avoid thousands of particles as generic decoration.

## Performance rules

- cap render resolution/DPR
- reduce shader complexity on mobile tiers
- minimize full-screen multi-pass effects
- pause when offscreen/hidden
- avoid reallocating render targets each frame
- reuse textures/buffers/materials
- profile texture bandwidth and overdraw
- prefer one coordinated RAF/render loop

## WebGPU branch

Use WGSL/WebGPU when compute, storage buffers, modern pipelines, or a specific rendering technique materially benefits. Detect `navigator.gpu`; handle adapter/device failure; keep a WebGL/CSS/poster fallback. Do not assume WebGPU is Baseline.

## Reduced motion

Freeze time-based flow, remove continuous displacement, reduce pointer amplification, and switch scroll-driven full-screen effects to static/step states.

## Showcase-driven technique breakdown

When a visual reference is supplied, decompose it into input media/data → coordinate transform → shader math/mask → compositing → interaction driver → fallback. Rebuild the mechanism from first principles rather than tracing proprietary shader source.

## Output

Return effect concept, runtime choice, shader pseudocode/math, production code, uniform map, integration notes, fallback, and performance checklist as appropriate.

For build work, verify a nonblank first frame, aspect-correct resize, pointer/touch bounds, reduced-motion freeze or alternate state, capability failure, and offscreen pause. Report render scale and texture/pass counts so performance claims remain testable.

## Examples and showcase calibration

Read `references/examples.md` when translating an effect description into a rendering signal chain. Read `references/showcase.md` for public technique references. Recreate shader logic from first principles or permitted sources; do not copy proprietary shader code.

## References
- `references/examples.md`
- `references/showcase.md`
- `references/shader-recipes.md`
- `references/dom-webgl-sync.md`
- `references/webgpu-progressive.md`
