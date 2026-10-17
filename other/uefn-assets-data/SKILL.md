---
name: uefn-assets-data
description: Create, search, copy, move, delete and tag assets, and work with DataTable and CurveTable via MCP in the lab. Verified recipes in recipes.json.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-assets-data

Sources: `Claude/docs/mcp/assets.md`, entry B2 of `SKILLS-PROPOSAL.md`, `recipes.json`.
Cross-cutting skills to always follow: `uefn-mcp-lab-guard` e `uefn-create-use-remove-one-script` (create, use, remove in ONE script).

## Rules
- Paths always in GUID form: `{lab}` = `/<guid>/<progetto>` (e.g. `/09e4e8d3-.../root_ai_lab`). Never `/root_ai_lab/...`.
- AssetTools: package path (without `.Name`); DataTable/CurveTable: `{"refPath":"<pkg>.<Name>"}`; `diff`: plain strings.
- The guard is not bypassed: a refusal is reported. If a recipe fails: exact error and STOP.
- `add_rows`, `set_rows`, `remove_rows` return null: re-read (`get_rows`/`list_rows`) to confirm.
- `find_assets` always with a filter (`folder_path`, `name`, `asset_type`): without arguments ~120 MB.

## Verified recipes
Toolset: `editor_toolset.toolsets.asset.AssetTools`, `editor_toolset.toolsets.data_table.DataTableTools`, `editor_toolset.toolsets.curve_table.CurveTableTools`.
Assets:
1. `create_folder {"path":"{lab}/Assets_X"}`
2. `find_assets {"folder_path":"{lab}/Assets_X","asset_type":{"refPath":"/Script/Engine.DataTable"},"recursive":true}`
3. `exists {"path":..}`, `get_asset_class {"asset_path":..}`, `get_asset_tags`, `is_dirty`, `get_dependencies`, `get_referencers`, `load_asset`, `reload_asset` (discards unsaved changes), `list_folders {"root_path":..,"recursive":false}`
4. `duplicate {"path":..,"new_path":..}` (false if it exists), `move {"path":..,"new_path":..}`, `delete {"path":..}` (folder included)
5. `save_assets {"asset_paths":["{lab}/Assets_X/DT_X"]}`
6. `update_metadata_tags {"asset_path":..,"set_tags":{"MyTag":"v1"}}` poi `get_metadata_tags` (metadata is NOT the registry tags of the `tags` filter).

DataTable:
7. `search_row_structs {"struct_name":"*Table*"}`; `create {"folder_path":"{lab}/Assets_X","asset_name":"DT_X","schema":{"refPath":"/Script/GameplayTags.GameplayTagTableRow"}}` -> refPath `{dt}`
8. `get_schema`, `add_rows {"data_table":{"refPath":"{dt}"},"row_names":["RowA","RowB"]}`, `set_rows {..,"values":"{\"RowA\":{\"devComment\":\"hello\"}}"}` (JSON TEXT, existing row), `get_rows {..,"row_names":["RowA"]}`, `list_rows`, `rename_rows {..,"renames":{"RowA":"RowAA"}}`, `remove_rows`, `diff {"old_asset_path":..,"new_asset_path":..}`

CurveTable:
9. `create {"folder_path":..,"asset_name":"CT_X"}` (already has a `Curve` row); `add_row {"curve_table":{"refPath":"{ct}"},"row_name":"Speed","default_value":1.0}`; `set_keys {..,"keys":[{"time":0,"value":0},{"time":1,"value":10}]}`; `add_key {..,"key":{"time":5.0,"value":9.0}}`; `get_keys`, `list_rows`, `rename_row {..,"row_name":"Speed","new_row_name":"Velocity"}`, `remove_row`, `diff`.

Cleanup: `AssetTools/delete {path:"{lab}/Assets_X"}`.

## To try (not verified)
- `DataTableTools/import_file`, `CurveTableTools/import_file`: guard-refused (disk path). Do not bypass.
- `AssetTools/update_metadata_tags` con `remove_tags`: rejected (3 attempts); no known way to remove a tag except deleting the asset.
- `AssetTools/exists` right after `delete`: unreliable as proof of deletion (unverified).
- `find_assets` without filters, `ListTags`: deliberately not run (120 MB / 2.8 MB).

## Don't
`find_assets` without filters; import from disk; treating null as success; writing outside the lab folder.
