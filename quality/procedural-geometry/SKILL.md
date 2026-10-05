---
name: procedural-geometry
description: Use when generating or reviewing the GEOMETRY of a game — procedural terrain, meshes, structures, and scatter. Covers noise as the substrate (Perlin/Simplex/value noise, fractal Brownian motion, domain warping), terrain generation (heightfield vs voxel/SDF, marching cubes, dual contouring, hydraulic/thermal erosion, LOD/chunking), structural generation (L-systems, shape grammars, wave function collapse / model synthesis, constraint-based layout), mesh topology correctness (watertight/manifold meshes, inverted normals, winding order, degenerate triangles/UVs, runtime mesh performance and caching), and vegetation/scatter (Poisson-disc/blue-noise placement, slope/altitude/biome masking, GPU instancing). Also use to diagnose terrain that looks like "noise lumps", structures that read as grid-aligned or obviously generated, scatter that clumps or grids, or generated meshes with black/inverted faces and broken collision. Triggers on "procedural terrain", "terrain generation", "Perlin noise", "Simplex noise", "fBm", "domain warping", "heightmap terrain", "voxel terrain", "SDF terrain", "marching cubes", "dual contouring", "erosion simulation", "terrain LOD", "chunking", "L-system", "shape grammar", "wave function collapse", "WFC", "model synthesis", "procedural buildings", "dungeon generation", "procedural mesh", "inverted normals", "manifold mesh", "watertight", "degenerate UVs", "winding order", "vegetation scatter", "foliage placement", "Poisson disc", "blue noise", "GPU instancing", "my terrain looks fake", "it looks generated".
---

# Procedural Geometry

How to generate the *geometry* of a game — terrain, meshes, structures, and scatter — so it is **correct** (watertight, manifold, properly wound, performant) and **varied** (perceptually distinct, not parametric oatmeal). Geometry generation is engineerable math: noise as a substrate, modulation and erosion for believability, constraints and hand-placed anchors for "designed-looking" structure, blue-noise for scatter, and topology validators as the non-negotiable correctness floor.

> **Tier:** technical craft (→ `gamestack-core`). Engine-agnostic geometry-generation math underneath generated terrain, structures, and meshes.

## When to use this

- Generating terrain (heightfield or voxel/SDF), and deciding which representation the design actually needs
- Choosing and wiring a mesh-extraction (marching cubes vs dual contouring), erosion, and LOD/chunking pipeline
- Generating structures with L-systems, shape grammars, or wave function collapse / model synthesis
- Authoring the **mesh topology validator** (winding/normals, manifold, degenerates, watertight)
- Scattering vegetation/props with blue-noise placement, environmental masking, and instancing
- Diagnosing terrain that looks like "noise", structures that read as generated, or meshes with black faces / broken collision

## Scope

This skill owns **the math and algorithms that produce geometry** — meshes, terrain, structures, scatter. It is deliberately narrow. Adjacent concerns live in sibling skills:

- *What content means and whether it's perceptually varied at scale* (quests, lore, items, the oatmeal problem for **content**) → `procedural-generation`. This skill is the geometric statement of the same hybrid (hand-anchor + constrained fill); that skill is the narrative one.
- *Making a generated level legible, navigable, gated, and paced* → `level-design`. This skill is the **geometry engine underneath** it — grammars/WFC produce the rooms; `level-design`'s principles make them readable. Geometry serves legibility; it does not replace it.
- *Gating generated output for perceptual sameness and intentionality* → `procgen-review`. Its **oatmeal test** runs on the geometry this skill emits; the topology validator here is the *correctness* floor below that *quality* gate.
- *Rendering, culling, and draw-call budgets for the meshes produced* → `3d-graphics-and-rendering`. *Texturing/shading them* → `shaders-and-vfx`.
- *Macro/world spatial layout, biomes as places, exploration pull* → `open-world-design` (this skill is the terrain math underneath that layer).

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in five sub-domains: noise as the substrate (Perlin/Simplex/value, fBm, multifractal/ridged, domain warping, Worley/3D-noise caves); terrain generation (heightfield vs voxel/SDF, marching cubes vs dual contouring, erosion, LOD/chunking); structural generation (L-systems, shape grammars, WFC/model synthesis, hybrid hand-anchor); mesh topology correctness (winding/normals, manifold/watertight, degenerates, runtime threading/caching); and vegetation/scatter (blue-noise, masking, instancing). Each rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as validators in a generation loop.

## The two ideas to anchor on

> **1. A single noise field is oatmeal; structure comes from modulation, not octaves.** Plain fractal Brownian motion is the canonical "fake terrain" look — equal roughness everywhere, no ridgelines, no drainage. Believability comes from *modulating* it (multifractal/ridged noise, domain warping) and from **erosion simulation** that carves the connected valleys and ridges a process would. More octaves add detail, not structure.

> **2. "Looks designed, not random" is a constraint problem.** Grammar- and constraint-based methods (L-systems, shape grammars, wave function collapse / model synthesis) get their authored quality from **hand-authored rules and tilesets**, not from the algorithm. The designer's craft moves into the constraint set — and the most reliable path at scale is **hybrid**: hand-place the silhouette landmarks and set pieces, let the generator fill between them under constraints.

> **Why this matters doubly for a generator:** a human sees a black inside-out face, a grid-aligned forest, or 10,000 identical buildings and feels "off." An autonomous generator has no eyes. Author the **mesh topology validator** (winding/manifold/degenerate/watertight) and the **representation, erosion, crack-free, and instancing contracts** as inviolable; let generation vary inputs *inside* them (frequency, octaves, density masks, seeds); and gate every batch through `procgen-review`'s oatmeal test for *geometric* sameness — because parametric variation of one formula produces perceptually identical results.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
