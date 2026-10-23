---
name: web-3d-asset-pipeline
description: Source or generate a 3D asset, clean it in Blender, export and optimize GLB, select model-viewer or a 3D runtime, and create mobile fallbacks and provenance.
---

# Web 3D Asset Pipeline

Read:

- `creative-production/pipelines/web-3d-assets.md`
- `creative-production/sources/3d-assets.md`
- `creative-production/standards/asset-budgets.md`

## Start with the interaction

Write what the visitor must do. If the answer is only “look at it,” a video or still may be better.

## Produce

1. Source, generate, or model under clear terms.
2. Set scale, orientation, and pivot in Blender.
3. Remove hidden geometry and unused materials.
4. repair normals
5. simplify topology
6. trim animation clips
7. resize and consolidate textures
8. export GLB
9. optimize with glTF Transform
10. inspect after compression

## Select runtime

Use `model-viewer` for:

- one model
- orbit
- hotspots
- AR
- camera presets

Use Three.js for:

- custom shaders
- material configuration
- multiple coordinated objects
- procedural state
- scene-level camera and scroll behavior

Use Spline when visual authoring is the primary need and its export constraints fit.

## Fallbacks

Deliver:

- optimized desktop GLB
- mobile GLB or static fallback
- poster
- loading state
- error state
- reduced-motion state
- manifest

## Verify

Measure download, decode, GPU cost, memory, focus, touch behavior, and offscreen pause. A model that renders on a desktop workstation is not automatically a web asset.
