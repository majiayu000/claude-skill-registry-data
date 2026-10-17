---
name: uefn-materials
description: Create or edit a Material, Material Instance or parameter in the lab and apply it to an actor via the UEFN MCP (39/39 tools ok). Use for materials work; only `verified` recipes, rest listed as not verified.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-materials (MVP experimental, B8)

Source: `Claude/docs/mcp/materials.md`, `recipes.json`, `SKILLS-PROPOSAL.md` B8. Read first: skills `uefn-mcp-lab-guard` (guard rules, lab mount) and `uefn-create-use-remove-one-script` (create, use and remove in ONE script).

## Rules
- Paths in GUID form: lab mount `/09e4e8d3-83f9-4ee0-9777-072ed3984380/root_ai_lab` (never `/root_ai_lab`). Run from PowerShell (Git Bash path-converts the value).
- The guard is never bypassed. A refusal is reported verbatim to the owner, not worked around. If a recipe fails: report the exact error and STOP.
- Must NOT: duplicate engine materials into the lab (refused); leave `Mat_*` assets (clean up with `AssetTools/delete`).

## Recipes `tool-ok` or `proven` (recipes.json)
MaterialTools (`editor_toolset.toolsets.material.MaterialTools`): `create_material {folder_path, asset_name}`, `add_expression`, `connect_expressions`, `connect_to_output`, `get_property_input`, `recompile`, `get_statistics`, `diff_material`.
MaterialInstanceTools (`editor_toolset.toolsets.material_instance.MaterialInstanceTools`): `create`, `list_parameters`, `set_scalar_parameter`, `set_vector_parameter`, `set_static_switch_parameter`, `set_texture_parameter`, `set_parent` (cleanup: set_parent back to the original), `clear_parameters`, `get_scalar_parameter`.
Cleanup of created assets: `AssetTools/delete {path: package path without .Name}`.

## Traps
- `ObjectTools/set_properties` on a material takes `values` as a JSON TEXT string. B-002: the guard does not inspect a string `values`, so put only lab objects and plain numbers/colors in it, never a class or asset path of a Verse script.
- Float readback 0.9 = 0.8999999761581421. One bad key in the values JSON fails the whole set.
- Each new Material adds shader compile time: prefer instances.
- `get_referencing_materials` returns `[{}]` without a path. `set_parameter_override false` returns the parent value. No MPC edit tool (asset only). No blend-mode tool (use set_properties, untried).

## Documented fix: drone (materials.md "Drone fix log", 2026-10-16)
Symptom: log `Material ... missing usage flag SkeletalMesh! Default Material will be used in game` on a skeletal mesh (mech-drone, slots Fire/Robot); instances had parent FBX Interchange phong with empty `textureParameterValues` and all `*MapWeight` 0.
Fix: (1) create lab materials with `ObjectTools/set_properties {values: '{"bUsedWithSkeletalMesh": true}'}` (key WITH the `b` prefix; `usedWithSkeletalMesh` fails); (2) wire textures (BaseColor, Normal, Gloss->OneMinus->Roughness, AO R, Emissive) and `recompile`; (3) `MaterialInstanceTools/set_parent` of each slot instance to the new material, then `save_assets`. Revert: set_parent back to the Interchange phong parent (original values untouched).
Status: recompile ok (217 / 158 instructions); `bUsedWithSkeletalMesh` reads true; NOT verified visually and no fresh in-game log line after the fix.

## To try (not verified)
- `recipe/apply_material_instance_to_actor (ONE script)`: status unverified in recipes.json.
- `MaterialInstanceTools/set_parent#drone_skeletal_fix`, `recipe/apply_lab_mi_to_owner_skeletal_actor`: unverified (no visual check; touches assets outside the lab, needs the guard roots).
- `StaticMeshTools/set_material`: not run (only an engine mesh available).
