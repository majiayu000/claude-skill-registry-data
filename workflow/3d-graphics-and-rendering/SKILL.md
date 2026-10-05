---
name: 3d-graphics-and-rendering
description: Use when designing, choosing, or reviewing the rendering layer of any real-time 3D (or 2D-with-lighting) game — the rasterization pipeline, PBR vs stylized/NPR materials, the forward/deferred/forward+ lighting architecture, global-illumination and shadow choices, culling/LOD/draw-call/overdraw performance budgets, and the post-processing chain (tonemapping, bloom, AO, anti-aliasing). Also use to diagnose a scene that's GPU-bound or CPU-bound, shadow acne or peter-panning, pop-in, overdraw blowout, blown-out or washed-out tonemapping, or content that looks visually incoherent across generated scenes. Triggers on "rendering pipeline", "PBR", "metallic roughness", "deferred vs forward", "forward+", "global illumination", "GI", "lightmaps", "light probes", "SDFGI", "shadow maps", "cascaded shadows", "shadow acne", "peter panning", "frustum culling", "occlusion culling", "LOD", "pop-in", "draw calls", "batching", "instancing", "overdraw", "CPU bound", "GPU bound", "tonemapping", "ACES", "bloom", "SSAO", "ambient occlusion", "anti-aliasing", "MSAA", "TAA", "FXAA", "Nanite", "mesh shaders".
---

# 3D Graphics & Rendering

How a real-time engine turns geometry, materials, and lights into a frame — and which of those choices a generator can safely vary versus which must be frozen. Rendering is a pipeline of fixed stages with hard limits and hard budgets; getting the *architecture* and the *imaging contract* right up front is what keeps a 3D game both performant and visually coherent.

> **Tier:** technical craft (→ `gamestack-core`). Engine-agnostic rendering principles every real-time 3D (or 2D with lighting) game obeys.

## When to use this

- Choosing the lighting architecture (forward / deferred / forward+/clustered) and living with its constraints
- Picking a PBR workflow (metallic/roughness vs specular/glossiness) or deliberately departing into stylized/NPR
- Selecting a GI approach (baked lightmaps · light probes · voxel/SDF GI · ray-traced) by scene dynamism and budget
- Tuning shadows (slope-scaled bias, cascaded shadow maps) out of the acne↔peter-panning band
- Setting performance budgets: culling, LOD, batching/instancing, overdraw — after diagnosing CPU- vs GPU-bound
- Ordering the post chain (HDR effects → tonemap → LDR grade) and freezing the exposure/tonemap/AO/AA contract
- Deciding which rendering parameters a generator may vary vs which are a fixed pipeline contract

## Scope

This skill owns **the pipeline, lighting, performance, and imaging layer** — how the frame is assembled, not what's painted into it. Adjacent concerns live in sibling skills:
- Material & VFX *authoring*: the shader model, node-graph/procedural materials, particles, decals, screen-space effects, stylization mechanics → `shaders-and-vfx` (this skill picks deferred-vs-forward and the overdraw budget; that skill authors the materials and effects living inside it)
- Visual readability, silhouette, signal color, readability-over-fidelity → `art-direction-and-readability`
- Generated meshes, terrain, noise, marching cubes, mesh topology correctness, scatter placement → `procedural-geometry` (this skill renders what that skill generates; the mesh-validity contract is shared)
- Animation/skinning/blend systems → `animation-systems`

It does **not** own material authoring, art direction, or geometry generation — only the pipeline they run through.

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in five sub-domains: the rasterization pipeline (stages and their limits; mesh/compute shaders), PBR (energy conservation, metallic/roughness vs specular/glossiness, NPR departures), lighting & shadows (forward/deferred/clustered, GI spectrum, shadow bias, CSM), performance & culling (CPU vs GPU bound, frustum/occlusion culling, LOD, batching/instancing, overdraw), and post-processing (chain order, filmic tonemapping, AO, AA). Each rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain, written to be enforced as validators in a generation loop.

## The two ideas to anchor on

> **1. Architecture and imaging are decided once, then frozen.** The lighting architecture (forward/deferred/clustered), the PBR/NPR shading model, the shadow-bias band, and the whole imaging pipeline (exposure → tonemap → AO → bloom → AA, in that order) are *contracts*, not per-scene dials. Pick each from its real driver — light count, material variety, scene dynamism, target hardware — then hold it constant across the whole game.

> **2. "Quality" problems are usually budget problems, and the first question is CPU vs GPU.** Culling, LOD, batching/instancing, and overdraw control decide whether the frame fits at all — not just how pretty it is. CPU-bound and GPU-bound demand *opposite* fixes (fewer draw calls vs less per-pixel work), so diagnose the bound before optimizing anything.

> **Why this matters doubly for a generator:** a human team feels an incoherent imaging pipeline or an overdraw blowout as "off." An autonomous generator does not. Freeze the imaging contract, the lighting architecture, the shadow constants, and the draw-call/overdraw budget as inviolable, hand-tuned globals; let generation vary *content* (material params within vetted ranges, light placement within the architecture's budget, LOD thresholds) inside them; run a draw-call/overdraw linter and an imaging-contract guard before any scene is committed. If the imaging pipeline drifts per scene, identical content reads as visually incoherent across the world even when each asset is individually correct.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
