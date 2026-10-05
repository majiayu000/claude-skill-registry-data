---
name: shaders-and-vfx
description: Use when authoring shaders/materials or building visual effects in ANY engine — the shader model (vertex/fragment/compute, what each reads and writes), node-graph material thinking, procedural texturing (noise, SDFs, triplanar, vertex-color/splat masks) vs. baked textures, the VFX toolkit (CPU vs GPU particles, trails/ribbons, decals, distortion/refraction, dissolve/hit-flash/rim effects), stylized rendering (toon/cel shading, outline rendering via inverted hull or post-process edge detection), and VFX performance. Also use to diagnose shader compilation stutter, overdraw/fill-rate collapse, an unreadable "particle storm", or generated materials that all look the same. Triggers on "shader", "material", "shader graph", "procedural texture", "noise", "SDF", "triplanar", "particles", "VFX", "visual effects", "trail", "decal", "distortion", "dissolve", "hit flash", "rim light", "fresnel", "toon shader", "cel shading", "outline", "stylized rendering", "shader stutter", "overdraw", "particle storm", "fill rate".
---

# Shaders & VFX

How to author shader-driven materials and visual effects that are parametric, readable, and cheap — across any engine. A shader is a data-flow contract (each stage reads and writes specific things); a material is a bounded parameter surface a generator can vary safely; VFX is the rendering substrate for game-feel's feedback channels, and the single biggest fill-rate risk if left unbudgeted.

> **Tier:** technical craft (→ `gamestack-core`). Engine-agnostic shading/VFX principles, the technical substrate for game-feel-and-juice's feedback channels.

## When to use this

- Authoring shaders/materials as a parametric, generator-safe system (node-graph thinking, procedural texturing, baked vs. procedural)
- Building VFX — particles, trails, decals, distortion, dissolve/hit-flash/rim — and choosing the technique by its cost model
- Implementing a stylized look: toon/cel shading, outline rendering, flat shading for cheaper + more readable rendering
- Diagnosing shader compilation stutter, overdraw collapse, a particle storm, or procedurally-generated materials that read as samey

## Scope

This skill owns **shader, material, and particle technical implementation** — what each shader stage reads/writes, how a material parameterizes, how each VFX primitive is built and what it costs. Adjacent concerns live in sibling skills:
- *When/why/how-much* feedback to fire, and the inverted-U budget ceiling → `game-feel-and-juice` (this skill is its rendering substrate; cite *up* to it for "should it fire and how big")
- Rendering pipeline (forward/deferred), lighting, GI, shadows, post-processing order, overall performance-budget framing → `3d-graphics-and-rendering` (sibling, same tier — this skill lives inside its pipeline)
- Visual readability, silhouette, signal-color language, art direction → `art-direction-and-readability` (owns the language; this skill realizes it as technique)
- The meshes/terrain these materials texture and outline → `procedural-geometry` (sibling — its UV-less runtime geometry is why triplanar/vertex-color paths exist here)

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in five sub-domains: the shader model (data-flow contract), material authoring patterns (node-graph thinking · procedural texturing · baked-vs-procedural), the VFX toolkit (particles · trails · decals · distortion · screen-space effects, each mapped to a feedback channel), stylization techniques (cel shading · outline rendering · stylized-as-performance-decision), and performance & failure modes (variant explosion · overdraw · the particle storm). Each rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as validators in a generation loop.

## The two ideas to anchor on

> **1. The shader stages are a contract; vary parameters, not plumbing.** A vertex shader transforms and emits interpolated outputs; a fragment shader reads them and writes one pixel; a compute shader reads/writes arbitrary buffers. A generator's authoring surface is **uniforms, textures, and parameters** fed into a small set of hand-authored master materials — never new shader code. That single rule caps shader-variant explosion at the source.

> **2. VFX is feedback made of fill rate — budget it or it fails twice.** Every particle, trail, and distortion effect is *how* a feedback channel is built; layered transparency is the #1 fill-rate cost. The "particle storm" fails twice at once — it tanks frame rate *and* obscures the gameplay state the VFX was meant to communicate. Cap concurrent emitters and overdraw the same way `game-feel-and-juice` caps the juice budget.

> **Why this matters doubly for a generator:** a human technical artist *sees* the overdraw, the variant count, the particle storm, the samey materials. An autonomous generator does not. Hand-author the master materials, the VFX recipe palette (each effect a bounded template), and the signal-color palette as inviolable contracts; let generation select and parameterize within them; run a variant/PSO validator, an overdraw/fill-rate validator, and a concurrent-VFX validator before any content is committed.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
</content>
