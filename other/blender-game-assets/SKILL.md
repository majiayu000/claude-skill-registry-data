---
name: blender-game-assets
description:
  "Build, texture, rig and export editable 3D game assets with local Blender CLI and bpy from references or a project
  brief. Use for game models and 3D sources for rendered sprites, in GameGen projects or as standalone asset work that
  does not require GameGen setup."
---

# Build Blender game assets

In a GameGen project, or when the task is part of GameGen production, read
[shared context](../../references/shared-context.md), the ready preferences and
[repository contracts](../../references/repository.md). For a standalone Blender asset request outside a GameGen
project, do not start `game-bootstrap` or create preferences: resolve the brief, target engine and export contract from
the request and existing files, and report provenance and review evidence instead of writing a manifest. Use the
[local Blender workflow](../../references/blender-cli.md) for executable discovery, background Python, the macOS startup
workaround, renders and export checks. Use the supplied asset references, intended gameplay camera and project-specific
budgets.

## Establish the source and export contract

Inspect references and existing sources before building. Match their silhouette, proportions, feature placement, palette
and material response as closely as the delivery allows. Infer concealed forms consistently and record consequential
assumptions. When no references are supplied, work from the brief and saved art direction; do not require a new
reference-generation round unless it is needed or requested.

Own a dedicated collection, source file or isolated build and preserve unrelated objects and unsaved work. Resolve
units, forward/up axes, origin, ground contact, bounds, material/texture budgets, collision ownership and
animation/root-motion expectations from the existing contract and task. In a GameGen project, ask only about
consequential asset-contract details that preferences, the manifest and the task leave open, and record the answers in
the asset manifest. Route changes to saved preferences through the coordinating agent and `game-bootstrap` instead of
asking production choices again. For standalone work, ask the user directly. Run Blender locally through repeatable
`bpy` scripts; a third-party Blender MCP is not a dependency.

## Model and surface workflow

1. Start with primitives, curves or simple custom meshes for the major forms. Render front, side, rear and intended
   gameplay views and compare against available references before fine detail. Preserve simple primitive construction
   where it fits the design; join, reshape or retopologize organic forms where the reference requires smooth anatomical
   transitions.
2. Use parameterized builders, modifiers, Geometry Nodes or supported particle/simulation systems when procedural
   construction makes the asset easier to author or revise. Keep meaningful dimensions and variation editable, and
   follow the shared cache and export rules for stateful results.
3. Build topology that supports the intended deformation around joints, face and attachment points. Close exposed
   surfaces, including eyes and mouths, and inspect them from multiple angles. Remeshing can unify a sculpt, but its
   topology and density still need review for deformation and export.
4. Create usable UVs and materials that match the reference. Add base-color, roughness, normal and other texture maps
   where needed for markings and surface detail. Solid-color materials are appropriate when the art calls for them.
   Inspect texel density, seams, stretching, normals and tangent behavior under representative lighting.
5. Treat base-color paint as color data and normal/roughness maps as non-color data. Avoid applying gamma conversion
   twice. Verify exported vertex colors are enabled and not unintentionally multiplied by a tinted material. Bake
   unsupported procedural shading to suitable maps on the final UV layout and keep texture dependencies portable.
6. Reduce material splits and geometry against the configured budgets while retaining silhouette and articulation.
   Reinspect the textured and deformed result after optimization. For Blender-rendered sprites, keep camera, projection,
   lighting and framing fixed across directions and animation frames; coordinate with game-sprites.

## Rig and animate when required

Give characters a usable rest pose, skeleton and skin. Place joints for the anatomy and required motion, including
fingers, tails or other movable appendages where relevant. Separate authoring controls from deform bones; provide IK, FK
and facial shape keys or controls appropriate to the task. For other articulated assets, choose bone, object or
constraint controls that suit their construction. Static props do not need a character rig.

Bind the visible geometry and follow the
[skin and animation export checks](../../references/blender-cli.md#skin-and-animation-export-checks) for weights and
baking. Inspect extreme poses for collapsed joints, stretching, disconnected surfaces and face/appendage clipping.
Verify vertex movement and facial deformation, not only bone transforms. Retain the editable rig in the source.

Use [game-animation](../game-animation/SKILL.md) for requested clips, readable timing, planted contacts, secondary
motion, loop behavior and animation preview review.

## Export and review

Save the editable `.blend`, builder and required textures. Export an engine-supported format such as glTF/GLB with the
actual selected asset objects, required textures, skin and clips. Exclude the review studio unless it is part of the
requested asset. Apply transforms deliberately; record orientation after import instead of assuming Blender and Godot
agree. Verify the selected export mode preserves named clips, baked constraints and facial morphs without accidentally
combining unrelated actions.

Run the bundled `scripts/asset_audit.py` for structural GLB metadata when useful. Follow the shared fresh-import checks,
then perform a Godot import and actual visual review for game delivery. Check texture/material response, eyes/face
readability, ground contact and articulated deformation. A rotating skeleton is not enough if vertices are not weighted
to it.

Keep `.blend` sources and builders outside the engine import tree. Record output hash, dimensions, triangles, surfaces,
rig/clip metadata and review evidence. Do not call a source render an in-engine capture, or call an export optimized for
mobile before profiling the target workload.
