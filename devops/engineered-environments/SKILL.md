---
name: engineered-environments
description: Lay out believable large engineered environments in Three.js, as systems rather than props. Use for streets, railways, stations, buildings, bridges, utilities, industrial districts, ships and any place where infrastructure has to read as working.
---

# Engineered Environments

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`) and TSL node materials (`three/tsl`); no WebGL fallback, no GLSL.

Create a coherent engineered place, not a collection of disconnected props.

## Core idea

Everything exists because people live, travel, work, maintain and repair the place.

Think in systems:

- transport
- pedestrian circulation
- utilities
- power
- water
- waste
- ventilation
- communications
- emergency access
- maintenance
- structural support
- habitation
- commerce
- industry

## Ground and orientation

The ground is the local reference for everything built on it. When creating long structures, decide whether each should follow:

- the ground's own surface (a road, a wall, a pipe along a floor)
- a straight local tangent (a beam, a bridge span, a rail that must stay flat)
- a structural direction (a column, a mast, a hanger)
- an independent suspended structure (a cable, a gantry, a roof)

Do not flatten everything to one plane, and do not bend everything to the ground. A straight span over curved or uneven ground needs supports where it leaves the ground; a structure that follows the ground needs its pieces oriented to the local surface normal, not to a world axis.

Build in the environment's own coordinates (along, across, height) and convert to world space once, when placing. For thousands of repeated objects, compose the same basis into `InstancedMesh` matrices instead of placing separate objects.

## Infrastructure hierarchy

Large infrastructure should have:

1. primary structure
2. secondary structure
3. services
4. access/maintenance
5. visual details

For example, a bridge needs its structural members before cables, lights and signs.

## Human scale

Use doors, people, trains, stairs, handrails and vehicles as scale references.

Infrastructure should support plausible human movement.

## Futuristic design

Prefer:

- modular construction
- clean structural systems
- integrated utilities
- compact machinery
- automated maintenance
- advanced materials
- efficient space usage

Avoid generic sci-fi decoration.

## Repetition and variation

Use procedural repetition for modules, windows, railings, lights, sleepers, panels and structural members.

Introduce controlled variation so large areas do not look copy-pasted.

## Environmental storytelling

Objects should reveal function. A service hatch implies maintenance. A cable tray implies distribution. A drainage channel implies water management. A ventilation duct implies air handling.

Use these cues to make the place believable without filling every surface with detail.

## Drawing at scale

A large place is thousands of repeated meshes, most of them far away or hidden. Instance what
repeats (`InstancedMesh`), share geometries between copies, and put static blocks in a
`THREE.BundleGroup` (set `needsUpdate = true` after changing it). When the scene is vertex-bound
(towers of windows, bridges of members, a city tile repeated to the horizon), switch the renderer
to the r187 GPU-driven pipeline. It is one line, and everything it cannot draw falls back to the
standard path in the same frame:

```js
import { MeshletDrawingPipeline } from 'three/addons/pipelines/MeshletDrawingPipeline.js';
renderer.drawingPipeline = new MeshletDrawingPipeline({ lodThreshold: 1, shadowLodThreshold: 1, occlusionCulling: true });
await renderer.init();
```

- **What it does.** Splits each geometry into meshlets of 64 triangles with a chain of simplified
  levels (meshoptimizer, loaded by the addon), culls per cluster on the GPU (frustum, backface
  cone, two-phase occlusion against the previous frame's depth), picks the level whose projected
  error is under `lodThreshold` pixels (`shadowLodThreshold` texels for shadow casters) and
  issues indirect draws. `minScreenRadius` drops objects smaller than that many pixels;
  `coarseScreenRadius` forces the simplest level below it.
- **What qualifies.** `Mesh` and `InstancedMesh` with position and normal attributes and an
  opaque material: not transparent, no transmission, no alpha hash or alpha-to-coverage. Node
  materials work with `colorNode`, `normalNode`, `emissiveNode`, `opacityNode` and
  `positionNode` (bounds are fitted); `vertexNode`, `fragmentNode`, `outputNode`, `depthNode`,
  `contextNode`, backdrop and shadow nodes are not supported. Skinned and batched meshes, morph
  targets, storage-buffer instance attributes, lines and points stay on the standard path. The
  outdoor kits (grass cards, snow, the sea) are transparent or custom and stay there by
  themselves.
- **Levels and far materials.** A `THREE.LOD` whose levels are plain meshes is merged into one
  chain: `lod.addLevel(tower, 0); lod.addLevel(far, detailDistance)` with a cheaper material on
  `far`. Copies that share a geometry batch together, so build one geometry per tower type and
  place it many times rather than generating each copy.
- **Shadows.** Keep the sun's shadow map static (`sun.shadow.autoUpdate = false`, `needsUpdate =
  true` when something moves) and shrink-wrap the shadow camera to the built area.
- **When it pays.** Large gains for vertex-bound scenes with many hidden or sub-pixel triangles:
  the r187 city example draws thousands of towers this way. Fragment-bound scenes gain little;
  Sponza measured about the same (0.60 ms against 0.73 ms). Occlusion culling switches itself
  off while it culls under 30 percent of the visible clusters.
- **Checking.** `debug: true` colours each cluster (switch tone mapping off while it is on);
  `pipeline.info.clusters` and `.triangles` count what the main view drew. Await
  `renderer.compileAsync(scene, camera)` before the first frame so meshlet building and pipeline
  compilation do not land in it. Not run in this catalog; the settings are the r187 example's.
