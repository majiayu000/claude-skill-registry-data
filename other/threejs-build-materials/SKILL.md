---
name: threejs-build-materials
description: Author Three.js materials and shaders for the selected WebGL or WebGPU renderer with correct color, texture and resource budgets.
engines: [THREEJS]
---

# Build Three.js Materials

## When to use

Implement or diagnose materials, shaders, texture conventions or render cost in a Three.js game.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh threejs-build-materials`; require compatibility and honor task override scope. Read the locked core/addon revision, renderer backend, `STYLE.md`, art pipeline, lighting baseline and texture/shader budgets. Use project dependencies and authorized inputs; this skill never changes the art pipeline.

## Workflow

1. Prefer a standard/physical material where it expresses the surface. Declare metal/roughness, normals, UV channel, alpha mode, sidedness and environment light. Diagnose missing tangents or wrong texture channels before adding shader complexity.
2. Assign color textures their color space and leave data textures uncolored. Check the complete linear lighting/output path to avoid double tone mapping or conversion. Match normal-map convention and UV orientation to exports.
3. `WebGLRenderer` supports custom GLSL through `ShaderMaterial`/`RawShaderMaterial`. For `WebGPURenderer`, use that revision's supported node/TSL APIs; GLSL shader materials and `onBeforeCompile` patches are not interchangeable with this path.
4. Change uniform values without rebuilding variants each frame. Bound compile permutations, texture dimensions, transparent overdraw, shadows and targets. Use only documented project quality modes; never silently switch renderer.
5. Declare shared material ownership. Clone where per-object mutation requires isolation; dispose owned materials and textures separately after their final user leaves.

## Output and verification

Deliver parameters, texture/channel conventions, shader or node sources and GPU evidence. Compare lit/unlit surfaces, grazing angles, alpha sorting, color references and device frame cost. Record compile failures and unsupported backends. Compilation does not prove visual agreement with the art contract. Refer to [renderer compatibility](https://threejs.org/manual/pages/webgpurenderer), [ShaderMaterial](https://threejs.org/docs/pages/ShaderMaterial.html), and [color management](https://threejs.org/manual/pages/color-management.html).

Read `skills/build-gameplay-runtime/references/rendering-diagnostics.md` in the resolved Hephaera baseline (`.hephaera/skills/build-gameplay-runtime/references/rendering-diagnostics.md` from an installed host's root) for geometry/map-normal and tangent spaces, transformed billboards, scoped depth remedies, and comparable cost/visual checks. Keep renderer-supported material APIs, authored normals, and asset-production ancestry explicit.

For fullscreen effects use `threejs-build-postprocessing` and the automatically selected pmndrs `postprocessing` backend. Share the host WebGLRenderer/clock with Quarks; verify actual WebGL2 and MAUI target behavior, output color and owned composer cleanup. No implicit renderer change, package upgrade or path tracing.
