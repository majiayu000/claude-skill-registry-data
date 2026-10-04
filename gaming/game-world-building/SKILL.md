---
name: game-world-building
description:
  "For GameGen projects, assemble game levels and presentation in Godot, including cameras, lighting, materials,
  occlusion and the spatial rules of 2D, 3D and 2.5D worlds."
---

# Assemble worlds and presentation

Read [shared context](../../references/shared-context.md), ready preferences, approved environment references and the
existing level system. Read [repository contracts](../../references/repository.md). Use the selected grid, simulation
dimension, camera and renderer.

## Establish gameplay readability

Block out traversal, interactions, obstacles and encounter space first. Compose through the intended gameplay camera and
device aspect ratio. Check actor size, face/silhouette visibility, movement direction and available space around touch
controls. Perspective or orthographic projection, camera angle and follow behavior should serve the brief. Do not
default all games to distant overhead views.

Use a small representative environment to validate the asset kit and lighting. Keep collision/navigation geometry
intentional and simpler than decorative meshes. Verify entrances, slopes, bridges, elevation changes and camera
occlusion with continuous traversal.

For Blender-authored modular assets or procedural environment sources, use
[blender-game-assets](../blender-game-assets/SKILL.md) and its local CLI workflow. Keep editable dimensions, scatter
parameters and materials in the source. Export or realize geometry as required by the target workflow, and build runtime
interaction and procedural behavior in Godot when the level needs them.

For tile-based terrain, use [game-tilesets](../game-tilesets/SKILL.md) to create tiles, adjacency metadata and coverage
maps. This skill places the validated tiles in levels and composes them with props, actors and cameras.

## Rendering paths

- 2D: align sprites/tiles to the selected pixel density and filtering, handle Y/depth ordering, parallax and occluders
  deliberately, and keep collision coordinates independent from decorative offsets.
- 3D: use coherent materials, deliberate key/fill light, grounded contact shadows and exposure. Check renderer support
  before relying on effects. Bake or simplify when it benefits the target device while preserving the art direction.
- Sprites in 3D: define billboard/facing rules, pivot and ground contact, transparent sorting, shadow/light response and
  occlusion. Preserve a stable visual scale while navigating the 3D world.
- Pre-rendered sprites: match baked lighting and projection to the environment. Avoid double shadows or incompatible
  camera angles.
- 3D visuals with constrained movement: constrain gameplay to the intended plane or axes while maintaining 3D
  presentation and clear depth cues.

## Finish and verify

Differentiate rough, satin, glossy and emissive surfaces instead of applying one finish to everything. Keep
post-processing restrained enough for readable action. Pixel art, painterly scenes and miniature 3D worlds require
different treatments.

Reuse materials and modular pieces where useful; balance variation against draw calls and memory. Use
[game-optimization](../game-optimization/SKILL.md) to profile foliage, transparency, lighting and screen-space effects
at the target workload. Capture a fixed comparison view and actual traversal footage in Godot. A beautiful Blender
environment render is not evidence that the same lighting or materials work in the engine.
