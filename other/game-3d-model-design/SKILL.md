---
name: game-3d-model-design
description: Design, build, repair, and review 3D models for games. Use when Codex is asked about mesh construction, topology, retopology, UV unwrapping, normals, bevels, baking, hard-surface modeling, organic modeling, sculpt-to-low-poly workflows, deformation, rig-readiness, or model cleanup.
license: MIT
---

# Game 3D Model Design

## Core Workflow

1. Identify the model purpose, target engine, camera distance, animation/deformation needs, platform budget, and art style.
2. Start with silhouette and primary forms before topology detail. The model should read in untextured clay or flat color.
3. Choose a modeling route: direct low-poly, high-poly to retopo, sculpt to retopo, CAD/scan cleanup, kitbash cleanup, or procedural base plus manual finish.
4. Build topology to support the next task: shading, UVs, baking, rigging, deformation, destruction, customization, or modular reuse.
5. UV with visible seams, texel density, texture reuse, baking needs, and material boundaries in mind.
6. Validate normals, smoothing, triangulation, scale, transforms, nonmanifold geometry, hidden faces, overlapping surfaces, and export/import behavior.

## Modeling Priorities

- Silhouette: spend geometry where outline changes matter at the gameplay camera distance.
- Topology: use clean loops for deformation areas, controlled support edges for hard surfaces, and avoid long thin triangles where they cause shading or lighting artifacts.
- Retopology: rebuild high-density sculpt, scan, or CAD geometry into an optimized low-poly mesh when the source is not suitable for real-time use.
- UVs: minimize stretching, keep texel density intentional, split islands along logical seams, and avoid overlap unless mirrored/stacked UVs are intended.
- Normals and baking: decide where detail belongs in geometry, normal maps, trim sheets, decals, or material noise.
- Deformation: place loops around shoulders, elbows, knees, jaw, mouth, eyes, fingers, cloth bends, and other articulation zones.
- Cleanup: apply transforms, remove doubles/loose geometry, name objects, freeze/reset as required by the pipeline, and test export.

## Review Stance

When reviewing a model, lead with production blockers:

- Broken scale, transforms, orientation, or pivot
- Bad topology for deformation or shading
- Unusable UVs or inconsistent texel density
- Too many materials, objects, bones, or polygons for the target
- Missing collision, LOD, bake, or engine import needs
- Visual design that relies on texture detail instead of readable form

## Deliverable Shape

For 3D model work, provide:

- Model purpose and target constraints
- Form/silhouette assessment
- Topology, UV, normals, bake, and deformation notes
- Engine import risks
- Fix plan or modeling brief
- Verification checklist

## References

- Read `references/model-quality-checklist.md` when auditing a mesh, planning retopology, or preparing a model for engine import.
