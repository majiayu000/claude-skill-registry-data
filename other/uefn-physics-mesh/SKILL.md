---
name: uefn-physics-mesh
description: Read mesh, skeletal mesh, physics asset and texture data and add primitives via the UEFN MCP (50/63 tools ok, read-only skill). Use for mesh/physics reads; only `verified` recipes, rest listed as not verified.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-physics-mesh (MVP experimental, B10)

Source: `Claude/docs/mcp/physics-mesh.md`, `recipes.json`, `SKILLS-PROPOSAL.md` B10. Read first: skills `uefn-mcp-lab-guard` and `uefn-create-use-remove-one-script`.

## Rules
- Paths in GUID form: `/09e4e8d3-83f9-4ee0-9777-072ed3984380/root_ai_lab`. Run from PowerShell.
- The guard is never bypassed; a refusal is reported verbatim. If a recipe fails: report the exact error and STOP.
- Must NOT: write to `/AnimToTexture` or `/FigureCosmetics` meshes, place simulating actors.

## Status: 50/63 ok, 13 tools without ok
- StaticMesh not available in the project (0 StaticMesh; `duplicate` of an engine mesh is rejected by the editor: outside valid asset roots): StaticMeshTools set_nanite_enabled, remove_collisions, generate_convex_collisions, generate_lods, remove_lods, set_lod_thresholds, set_material, get_vertex_count, get_triangle_count.
- `import_file` (Static/Skeletal/Texture) and `TextureTools/export_png`: refused by the guard rule on disk paths (drive-letter path, even inside the project). Not circumvented; owner decision.
- Unblock (owner): import/copy one StaticMesh into the lab by hand, or allow project-folder paths for `import_file`.

## Recipes `tool-ok` or `proven` (recipes.json)
- StaticMeshTools (`editor_toolset.toolsets.static_mesh.StaticMeshTools`): `get_bounds {mesh}` (e.g. `/Engine/BasicShapes/Cube.Cube`, returns {min,max,isValid}), `get_lod_thresholds`, `get_material_slots`, `is_nanite_enabled`.
- SkeletalMeshTools (`...skeletal_mesh.SkeletalMeshTools`): `get_bounds`, `get_bone_names`, `get_physics_asset`, `get_socket_transform`.
- PhysicsAssetToolset (`PhysicsToolsets.PhysicsAssetToolset`): `GetBodyNames`, `GetBodyShapes`, `GetConstraints`, `GetBodyPhysicsMode`, `GetBodyMassScale`.
- PrimitiveTools (`...primitive.PrimitiveTools`): `add_cube`, `add_sphere`, `add_cone`, `add_cylinder {actor, name, dimensions}`; the actor must be created in the SAME process; cleanup `SceneTools/remove_from_scene {actor}` in the same script.
- TextureTools: `get_size`.
- `SceneTools/get_collision_channels`.

## Traps
- `get_lod_count` returns 0 on engine meshes, so vertex/triangle counts fail.
- `reset_properties` resets to the CLASS default, not the original: restore with `set_properties` of the originals.
- `read_texture` returns a pointer string; `find_assets` for SK_/SKM_/PA_ returns 1200-1800 paths (filter).

## To try (not verified)
- `collision_set_and_revert` (ObjectTools/set_properties on StaticMeshComponent0 of a lab actor): unverified in recipes.json (worked in physics-mesh.md, not promoted).
- SkeletalMeshTools sockets add/rename/transform/remove, set_material, assign_physics_asset; PhysicsAssetToolset CreateFromMesh, AddBody, RemoveBody, AddConstraint, RemoveConstraint, SetBodyPhysicsMode, SetBodyMassScale, SetConstraintLimits, SetSphere/SetBox/SetCapsule, RemoveShape: all `unverified` (recipes in recipes.json, no lab-owned skeletal mesh/physics asset to run on).
