---
name: uefn-create-use-remove-one-script
description: Create, use, read back and remove actors/assets in ONE execute_tool_script (or one Python process), with cleanup guaranteed by the caller.
last_reviewed: 2026-10-16
sources: [original]
---
# uefn-create-use-remove-one-script

## Rule
Create + use + read back + cleanup in ONE `ProgrammaticToolset/execute_tool_script`, because:
1. the guard allows writes only to objects created by the same process;
2. errors from internal tools cannot be caught in the script and there is no rollback: a script that aborts leaves what it created, so the CALLER cleans up after a failed script (`AssetTools/delete`, `SceneTools/remove_from_scene`);
3. `exists` right after `delete` may return true (materials trap 12): verify with `find_assets` o `exists` in `.Name` form.
Re-read every write: `add_rows`, `set_rows`, `add_tag` return null, not true.

## Verified recipes
- `execute_tool_script#create_widget_chain` (CreateWidgetBlueprint, AddWidget, ReplaceWidgetWithTemplate, set_properties, get_properties; cleanup `AssetTools/delete` of the folder `{lab_mount}/...`).
- `execute_tool_script#batch_reads` (multiple reads in one call).
- `execute_tool_script#verse_edit_build`.
- Script shape: `def ex(n,a): return execute_tool(n, json.dumps(a))["returnValue"]` e `def run():` that returns a dict.

## Paths
Always GUID: `{lab_mount}` = `/<guid>/<project>`. `values` of set_properties is a JSON STRING with camelCase names; `delete` takes the path without `.Name`.

## Don't
Leaving an actor in the level (a leftover `T008_Cube` cost a whole task); placing actors that simulate physics; `run()` returning a non-dict; bypassing a guard refusal; improvising if it fails (exact error, caller cleanup, stop).

## To try (not verified)
- `recipe/apply_material_instance_to_actor (ONE script)`: unverified.
- `collision_set_and_revert`: unverified (`reset_properties` goes to the class default, not the original: explicitly restore the original values).
- `recipe/animate_owner_actor_with_script_and_restore`: unverified.
