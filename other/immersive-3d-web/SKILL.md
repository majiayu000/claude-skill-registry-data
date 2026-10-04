---
name: immersive-3d-web
description: Build or debug a real 3D web scene when viewpoint, depth, material, or object manipulation carries the idea. Covers Three.js and React Three Fiber architecture, assets, controls, and performance; use motion-choreographer for DOM-only motion and shader-web-art for GPU image effects without a 3D scene.
---

# Immersive 3D Web

Use 3D only when depth, viewpoint, object structure, material, spatial navigation, or direct manipulation communicates something better than flat DOM.

## Intake checklist

Identify:
- framework and router
- target devices and minimum browser support
- scene purpose and user action
- model/texture assets and licensing
- camera behavior
- animation source: baked GLB clips / procedural / GSAP / Theatre.js / physics
- interaction model
- SEO/semantic DOM requirements
- performance budget and fallback

When the scene is part of a broader creative direction, inherit the handoff packet from `creative-web-studio`. Preserve the experience thesis and scene purpose; challenge the 3D choice if a lower rendering tier can satisfy them. Return any asset, browser, or performance assumption that still needs measurement.

## Architecture decision

### Three.js directly
Use for framework-agnostic or low-level control where React is not useful.

### React Three Fiber + Drei
Use in React/Next when component scene structure, hooks, ecosystem helpers, suspense/lazy loading, and declarative composition improve maintainability.

### Spline
Use when the scene is authored in Spline, fast visual authoring matters, or non-developers will iterate on 3D. Treat runtime cost honestly. Avoid stacking multiple embeds.

### Theatre.js
Use when hand-authored camera/object timelines need visual editing or creative direction iteration.

### WebGPU
Treat as progressive enhancement unless the project explicitly targets supported environments. Capability-detect. Preserve a WebGL or static fallback.

## Scene design workflow

1. Design the hero/scene as a still composition.
2. Establish world scale and coordinate conventions.
3. Choose one camera model and define camera states.
4. Build the smallest scene that communicates the concept.
5. Add lighting/material only after geometry and framing work.
6. Add interaction.
7. Add motion/camera choreography.
8. Add post-processing last.
9. Tier quality by device and test under throttling.

## R3F performance rules

- Do not mount/unmount expensive objects repeatedly; visibility or state changes may be cheaper.
- Reuse geometry and materials.
- Use instancing/batching for repeated objects.
- Avoid React `setState` inside `useFrame`; mutate refs for per-frame values.
- Avoid creating new vectors/materials/geometries every frame.
- Cap DPR; do not blindly render at full retina resolution.
- Use `frameloop="demand"` for mostly static scenes when practical.
- Lazy-load heavy models and below-fold canvases.
- Pause/reduce work when canvas is offscreen or document is hidden.
- Dispose textures, geometries, materials, render targets, and event resources when no longer needed.

See `references/performance-tiering.md`.

## Asset pipeline

Prefer GLB/glTF. Before shipping:
- remove invisible/unused geometry
- reduce polygon count where silhouette allows
- compress geometry (Draco/Meshopt when appropriate)
- resize textures to actual screen needs
- prefer modern compressed texture formats when pipeline allows
- atlas materials/textures when useful
- bake lighting/AO when dynamic lighting is unnecessary
- keep animation clips only when used
- preserve pivots/naming needed for interaction

## Camera choreography

Treat camera as a narrative instrument. Define named poses/states and interpolate between them. Avoid free-floating camera drift. Use one of:
- object moves, camera stable
- camera moves, object stable
- both only if visual reference remains clear

Scroll-driven camera motion should map to meaningful chapters. Reduced motion should switch to cuts between stable views or a static hero.

## Lighting/material rules

- Start with minimal lights.
- Prefer environment lighting where it improves realism and simplifies setup.
- Expensive shadows are optional; fake/bake when possible.
- Keep transparent layered materials under control.
- Use post-processing only after the base render is good.
- Avoid bloom as a substitute for art direction.

## Interaction

Raycast only when necessary; constrain hit targets. Provide DOM labels/instructions for essential controls. Touch targets and orbit constraints must be intentional. Do not trap page scroll inside the canvas unless the interaction explicitly requires it and there is a clear escape.

## Spline integration

Use the Spline React/Next runtime or code API when a Spline scene is supplied. Keep one primary scene, lazy-load it, test page-scroll interaction, and create a static fallback. If deeper custom rendering/performance control is needed, prefer R3F/Three over fighting the embed.

## Physics

Use Rapier or another physics engine only when physical behavior is the interaction itself. Do not simulate physics for decorative jitter.

## Showcase-driven concept check

When a reference-quality 3D direction is requested, compare the concept against 2–3 examples from `references/showcase.md`: identify the spatial idea, why 3D is justified, and how the project will differ materially.

## Output modes

Return any combination of:
- scene architecture and graph
- asset prep checklist
- camera storyboard
- R3F/Three/Spline implementation
- performance tier table
- mobile/reduced-motion fallback
- debugging plan
- AI coding prompt

For build work, provide or verify evidence at desktop and mobile framing, pointer and touch input, reduced motion, WebGL failure, and hidden/offscreen behavior. Record render resolution/DPR policy and the heaviest known asset instead of using “optimized” as an unmeasured claim.

## Examples and showcase calibration

Read `references/examples.md` for product, camera, assembly, Spline, and device-tier patterns. Read `references/showcase.md` when evaluating whether a 3D concept is strong enough to justify its runtime cost. Transfer spatial principles, not a reference site's world or assets.

## References
- `references/examples.md`
- `references/showcase.md`
- `references/r3f-architecture.md`
- `references/performance-tiering.md`
- `references/asset-pipeline.md`
- `references/3d-runtime-decisions.md`
