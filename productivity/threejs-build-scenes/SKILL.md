---
name: threejs-build-scenes
description: Build Three.js scene, renderer, loading, camera and resource lifecycles for browser games using the selected host version.
engines: [THREEJS]
---

# Build Three.js Scenes

## When to use

Create or refactor a Three.js game scene, streamed world, renderer boundary, or asset-loading lifecycle.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh threejs-build-scenes`; require compatibility and honor task override scope. Read `ENGINE.md`, the project architecture, locked `three` revision, browser targets, and frame/memory/loading budgets. Use project-owned packages and decoder files; add no implicit dependency or CDN.

## Workflow

1. Give one owner the canvas, renderer, active camera, scene transitions, and frame scheduler. Choose `WebGLRenderer` or the selected `WebGPURenderer`; check initialization and material support against that revision.
2. Separate simulation entities from `Object3D` instances; synchronize transforms after simulation and bound catch-up after hidden-tab resume. Three.js provides rendering: physics, navigation, AI and networking require explicitly selected application implementations.
3. Declare world units, camera clipping, shadows, pixel-ratio caps and resize behavior. Update projection matrices and render targets together. Handle context loss and report failed restoration.
4. Load through manifests and `LoadingManager`/selected loaders. Register glTF decoders explicitly. Reject late results from cancelled transitions using a transition generation ID; release those resources instead of attaching them to the next scene.
5. Use stable world/content IDs and versioned save data rather than render UUIDs. Rebuild visual instances from validated state. Navigation adapters consume declared walkable data and return movement intent to simulation.
6. Track shared versus scene-owned geometries, materials, textures, targets, controls and observers. Release only owned resources; stop the loop on permanent teardown and dispose the renderer at canvas lifetime end.

## Output and verification

Deliver the lifecycle, asset ownership table, world adapter and budget evidence. Exercise failed loads, transition during loading, repeated enter/exit, resize, hidden-tab resume and context loss. Compare `renderer.info` and application resource counts across cycles; internal renderer caches need not reach zero. Unit fixtures cannot certify GPU behavior on target devices. Consult the [official disposal guidance](https://threejs.org/manual/pages/how-to-dispose-of-objects.html) for the selected revision.

Read `skills/build-gameplay-runtime/references/rendering-diagnostics.md` in the resolved Hephaera baseline (`.hephaera/skills/build-gameplay-runtime/references/rendering-diagnostics.md` from an installed host's root) when diagnosing conservative animated/instanced bounds, multi-camera culling/LOD, billboards, transform/rotation intent, or depth conflicts. Apply its checks through the locked Three.js APIs; retain authoritative offscreen work and refresh presentation on reentry.

For particle/VFX work use the automatically selected `threejs-build-particles` Quarks owner. Keep one scene-owned batch renderer on this presentation clock and dispose its owned effects on scene teardown; selection does not install or upgrade host dependencies.

For fullscreen effects use `threejs-build-postprocessing` and the automatically selected pmndrs `postprocessing` backend. Share the host WebGLRenderer/clock with Quarks; verify actual WebGL2 and MAUI target behavior, output color and owned composer cleanup. No implicit renderer change, package upgrade or path tracing.
