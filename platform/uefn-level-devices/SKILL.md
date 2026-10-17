---
name: uefn-level-devices
description: Place/move actors, tags, folders, components, data layers, classic devices, event bindings and entities in the UEFN level via MCP (SceneTools, ActorTools, DeviceToolset, EntityToolset). Use for level changes in the lab, always with final cleanup.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-level-devices

Source: `Claude/docs/mcp/level-devices.md`, recipes in `recipes.json`. Before every write, apply `uefn-mcp-lab-guard`; for the create -> use -> remove cycle, see `uefn-create-use-remove-one-script`.

## Rules
- Paths in GUID form `/<guid>/<project>/...`. The guard is not bypassed: a refusal is reported.
- If a recipe fails: exact error and stop.
- Do not leave actors in the level (always clean up). Do not call `create_level`/`load_level` (changes the open level). Do not use B-002.

## Verified recipes
- Scene: `SceneTools/add_to_scene_from_class` (e.g. `/Script/Engine.TargetPoint`; the `name` becomes the LABEL; returns refPath), `add_to_scene_from_asset`, `find_actors` (`collision_channels: []` required), `set_actor_folder`, `get_folders`, `get_actors_in_folder`, `rename_folder`, `delete_folder`, `set_actor_hidden`, `remove_from_scene` (cleanup), data layer (`create_data_layer_asset`, `add_actors_to_data_layer`, `get_actors_in_data_layer`, `remove_actors_from_data_layer`).
- Actors: `ActorTools/set_label`, `add_tag`, `remove_tag`, `get_tags`, `set_actor_transform`, `get_actor_transform`, `add_component`, `remove_component`, `get_components`, `get_actor_bounds`.
- Classic devices: `DeviceToolset/ListDeviceAssets`, `PlaceDevice` (catalog devices only: `/Game`, e.g. `PID_CP_Devices_Hover_Platform`; also `#catalog` `/CreativeCoreDevices/SetupAssets/PID_Device_Button`), `GetBindingOptions`, `AddEventBinding` (`sourceEvent` with spaces: `On Player Spawned`), `ListEventBindings` (lists on the TARGET), `RemoveEventBinding` (same 4 args).
- Device Verse: `PlaceDevice {assetPath:{refPath:"/<guid>/_Verse.<progetto>-<classe>"}, transform}` ok (T-011/T-015); `ListDeviceProperties`/`SetDeviceProperty` camelCase, with a verification read and restore. Events from/to Verse devices: not possible (`GetBindingOptions` empty).
- Entities: `EntityToolset/CreateEntity` (`NPCInteropEntity_C` under `/Game`; `#simulation_entity` removed via `find_actors` + `remove_from_scene`, `DeleteEntity` fails on the root), `FindEntities`, `ListEntityClasses`.

## Pitfalls
- Class of a Verse device: `/Script/VerseDevices.ScriptDevice`; to place it you need the path `/_Verse.` of the compiled class.
- Outliner folders disappear with the last actor.
- The level `diff` is not supported.
- `TargetPoint` actors make StartSession validation fail (A2): remove them first.

## To try (not verified)
- `SelectActors`/`FocusOnActors` with a real actor: refused by the guard, do not bypass.
- `create_level`/`load_level`: deliberately not tried (they change the open level).
