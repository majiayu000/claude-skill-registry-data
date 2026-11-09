---
name: godot-build-scenes
description: Build Godot scene and resource lifecycles with explicit node ownership, navigation integration, and versioned state.
engines: [GODOT]
---

# Godot Build Scenes

## When to use

Build Godot scene and resource lifecycles with explicit node ownership, navigation integration, and versioned state. Apply this feature only to Godot-owned code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh godot-build-scenes` before edits or tool launches. Continue only when the effective engine is `GODOT` and the skill is eligible. Skill selection never selects the engine. Honor validated task override evidence and its permitted isolated output scope.

Read project.godot, exact Godot version, renderer, target platforms, enabled plugins and the project's GDScript or C# choice. C# requires the matching .NET-enabled Editor and compatible SDK; do not translate the project to another language.

## Workflow

1. Map SceneTree, Node ownership, PackedScene instances, autoload services and scene transitions. Define _enter_tree, _ready and _exit_tree responsibilities, using the equivalent C# methods when selected.
2. Keep reusable authored configuration in Resources and mutable instance state separate. Shared resources are shared intentionally; duplicate or make scene-local only when per-instance mutation is required.
3. Instantiate PackedScene content and set ownership deliberately for anything intended to serialize into a scene. Preserve resource UIDs, import metadata and references instead of inventing identifiers or editing imported cache outputs.
4. Coordinate ResourceLoader loading, activation and cancellation without retaining freed nodes. Use call_deferred and queue_free where tree mutation timing requires it, and disconnect owned signals or cancel pending callbacks on teardown.
5. Integrate NavigationRegion and NavigationAgent nodes in the correct 2D/3D world. Wait for map synchronization, update path following during physics ticks and stop updates when finished; navigation suggests motion rather than moving the parent automatically.
6. Keep AI intent, avoidance safe velocity and CharacterBody movement under one authority. Define unreachable targets, map changes and cancellation; a stale path callback must not move a replacement actor.
7. Store save data with stable domain IDs, explicit schema versions and validated resource references. Use approved user-data storage, preserve failed saves/migrations and restore dependencies before signals notify HUD or gameplay consumers.

## Verification

For Blender source/export delivery, read [Blender asset handoff](references/blender-asset-handoff.md) for explicit import prerequisites, editable scene ownership, reimport and target evidence.

- Load and reload a representative scene in actual Godot; check imported resources, autoload duplication, signal lifetime and queued deletion.
- Exercise successful, unreachable and cancelled navigation plus scene removal during asynchronous loading.
- Round-trip versioned state, reject malformed or missing-content records and measure load/allocation budgets on the target surface.

## Output

Scene/resource/scripts changes, node and resource ownership map, loading/navigation/save contracts and native lifecycle fixtures. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not install plugins, alter language selection or treat imported cache artifacts as editable source. Text scene validity alone does not prove gameplay correctness. Independent services and tools retain their architecture contracts.

## References

- [Godot scene organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html). Select the documentation matching the project release.
- [Using NavigationAgents](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html). Select the documentation matching the project release.

