---

name: leeway-3d-scene-audit

description: Deterministic inspection procedure for existing 3D scenes/assets before mutation, producing a scene passport with geometry, transforms, materials, UVs, textures, modifiers, rigs, lights, cameras, LOD/collision and performance evidence.

license: MIT

---

# LeeWay 3D Scene Audit

## Inspect

Record scene units/scale, coordinate frame, object hierarchy, names/IDs, transforms/dimensions, mesh vertex/edge/face/triangle counts, manifold state, normals, UV layers, material slots, texture files/resolutions/color spaces, modifiers, armatures, animations, lights, cameras, collections, LODs, collision and missing dependencies.

## Scene passport

Produce machine-readable asset/scene identity before editing. Hash/source references where available. Flag UNKNOWN rather than guessing measurements or texture provenance.

## Defect classes

GEOMETRY, TOPOLOGY, NORMALS, UV, MATERIAL, TEXTURE, LIGHTING, RIG, COLLISION, LOD, PERFORMANCE, DEPENDENCY, SCALE, EXPORT, VISUAL.

## Handoff

Defects route to specialized 3D skills; audit itself does not silently repair.