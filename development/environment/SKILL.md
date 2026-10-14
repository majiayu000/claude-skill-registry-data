---
name: environment
description: Godot environment developer — use when building game worlds, terrain, navigation meshes, occlusion, or GridMap levels.
type: implementation
---

# Godot Environment

> Expert Godot 4.x environment developer specializing in navigation meshes, terrain, occlusion, procedural placement, and large-world streaming.

## Overview

This skill handles the construction and runtime management of game environments: baking and querying navigation meshes, populating worlds with `MultiMeshInstance3D`, building 2D tile maps, projecting decals, streaming large scenes asynchronously, and authoring grid-based levels with `GridMap`. All code targets GDScript 4.7.

## Key Nodes & APIs

| Node / Class | Purpose | Key Properties / Methods |
|---|---|---|
| `NavigationRegion3D` | Defines walkable surface; owns the baked nav mesh | `navigation_mesh`, `bake_navigation_mesh()` |
| `NavigationMesh` | Config for nav mesh shape and agent constraints | `agent_radius`, `agent_height`, `agent_max_slope`, `cell_size` |
| `NavigationServer3D` | Singleton; offline path queries, map inspection | `map_get_path()`, `get_maps()` |
| `NavigationAgent3D` | Per-actor pathfinding; drives movement each frame | `target_position`, `get_next_path_position()` |
| `GridMap` | Voxel-style level from a `MeshLibrary` | `set_cell_item()`, `get_used_cells()`, `mesh_library` |
| `MultiMeshInstance3D` | GPU-instanced mesh for foliage, rocks, debris | `multimesh`, `instance_count`, `set_instance_transform()` |
| `FastNoiseLite` | Procedural noise for placement density masks | `get_noise_2d()`, `noise_type`, `frequency` |
| `TileMap` | 2D tile world | `set_cell()`, `get_used_cells()`, `get_surrounding_cells()` |
| `Decal3D` | Projects textures (blood, scorch, mud) onto surfaces | `texture_albedo`, `size`, `upper_fade`, `lower_fade` |
| `OccluderInstance3D` | Occlusion geometry for GPU culling | `occluder` (set to `ArrayOccluder3D` or `QuadOccluder3D`) |
| `StaticBody3D` | Non-moving collision geometry | — |
| `HeightMapShape3D` | Efficient terrain collision for large landscapes | `map_data`, `map_width`, `map_depth` |
| `ResourceLoader` | Async scene/resource loading for large worlds | `load_threaded_request()`, `load_threaded_get_status()` |
| `CSGShape3D` (subclasses) | Prototype-only constructive geometry | **Never ship; bake to mesh first** |

## Core Patterns

### Pattern 1 — Runtime Navigation Mesh Bake

Bake after any geometry change (spawned obstacles, destructibles, terrain edits). The bake is synchronous on the main thread; for large meshes call it from a thread or use `bake_navigation_mesh(on_thread: true)` (Godot 4.3+).

```gdscript
# environment/nav_region.gd
extends NavigationRegion3D

func configure_agent(radius: float, height: float, max_slope_deg: float) -> void:
    # agent_radius — clearance on each side of the agent; keep >= character capsule radius
    navigation_mesh.agent_radius = radius
    # agent_height — vertical clearance; set to full character height
    navigation_mesh.agent_height = height
    # agent_max_slope — steepest walkable angle in degrees; 45.0 is a typical default
    navigation_mesh.agent_max_slope = max_slope_deg
    # cell_size — voxel resolution of the bake; smaller = more accurate but slower
    navigation_mesh.cell_size = 0.25

func rebuild_nav_mesh() -> void:
    # Pass true to bake on a background thread (Godot 4.3+)
    bake_navigation_mesh(true)
    await bake_finished
```

### Pattern 2 — Offline Path Query Without an Agent

Use `NavigationServer3D.map_get_path()` when you need a path outside of per-frame `NavigationAgent3D` logic — e.g. AI planning, debug visualization, cost estimation.

```gdscript
# ai/path_planner.gd
extends Node

func query_path(from: Vector3, to: Vector3) -> PackedVector3Array:
    # Retrieve the default navigation map RID from the current world
    var map: RID = get_world_3d().navigation_map
    # optimize_path removes collinear intermediate points
    var path: PackedVector3Array = NavigationServer3D.map_get_path(
        map, from, to, true   # true = optimize path
    )
    return path

func estimate_travel_cost(from: Vector3, to: Vector3, speed: float) -> float:
    var path := query_path(from, to)
    if path.is_empty():
        return INF
    var dist := 0.0
    for i in range(1, path.size()):
        dist += path[i - 1].distance_to(path[i])
    return dist / speed
```

### Pattern 3 — Procedural Foliage with MultiMeshInstance3D + FastNoiseLite

Scatter thousands of meshes efficiently using GPU instancing. The noise mask controls density so that objects cluster naturally.

```gdscript
# environment/foliage_scatterer.gd
extends MultiMeshInstance3D

@export var instance_count: int = 4000
@export var area_size: float = 200.0
@export var noise_threshold: float = 0.1  # only place where noise > threshold

func _ready() -> void:
    _scatter()

func _scatter() -> void:
    var noise := FastNoiseLite.new()
    noise.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
    noise.frequency = 0.05

    multimesh = MultiMesh.new()
    multimesh.transform_format = MultiMesh.TRANSFORM_3D
    multimesh.mesh = preload("res://assets/meshes/grass_blade.mesh")

    var placements: Array[Transform3D] = []

    var attempts := instance_count * 4
    for _i in range(attempts):
        if placements.size() >= instance_count:
            break
        var x := randf_range(-area_size * 0.5, area_size * 0.5)
        var z := randf_range(-area_size * 0.5, area_size * 0.5)
        if noise.get_noise_2d(x, z) < noise_threshold:
            continue
        var y := _sample_terrain_height(x, z)
        var t := Transform3D(
            Basis.from_euler(Vector3(0.0, randf() * TAU, 0.0)),
            Vector3(x, y, z)
        )
        placements.append(t)

    multimesh.instance_count = placements.size()
    for i in range(placements.size()):
        multimesh.set_instance_transform(i, placements[i])

func _sample_terrain_height(x: float, z: float) -> float:
    var space := get_world_3d().direct_space_state
    var params := PhysicsRayQueryParameters3D.create(
        Vector3(x, 200.0, z), Vector3(x, -200.0, z)
    )
    var result := space.intersect_ray(params)
    return result.get("position", Vector3.ZERO).y
```

### Pattern 4 — 2D TileMap World Operations

Build, query, and iterate tile worlds using the `TileMap` API.

```gdscript
# world/tile_world.gd
extends TileMap

const LAYER_GROUND := 0
const SOURCE_ID := 0

func place_tile(coords: Vector2i, atlas_coords: Vector2i) -> void:
    set_cell(LAYER_GROUND, coords, SOURCE_ID, atlas_coords)

func clear_tile(coords: Vector2i) -> void:
    erase_cell(LAYER_GROUND, coords)

func get_all_floor_tiles() -> Array[Vector2i]:
    return get_used_cells(LAYER_GROUND)

func get_walkable_neighbors(coords: Vector2i) -> Array[Vector2i]:
    var neighbors: Array[Vector2i] = []
    for cell in get_surrounding_cells(coords):
        if get_cell_source_id(LAYER_GROUND, cell) != -1:
            neighbors.append(cell)
    return neighbors

func flood_fill(start: Vector2i, fill_atlas: Vector2i) -> void:
    var visited: Dictionary = {}
    var queue: Array[Vector2i] = [start]
    while not queue.is_empty():
        var current: Vector2i = queue.pop_front()
        if visited.has(current):
            continue
        visited[current] = true
        place_tile(current, fill_atlas)
        for nb in get_surrounding_cells(current):
            if not visited.has(nb) and get_cell_source_id(LAYER_GROUND, nb) != -1:
                queue.append(nb)
```

### Pattern 5 — Async Large-World Scene Streaming

Load heavy sub-scenes on a background thread to avoid frame hitches. Poll status each frame or use a timer.

```gdscript
# world/chunk_loader.gd
extends Node

signal chunk_ready(chunk_path: String, instance: Node)

var _pending: Dictionary = {}  # path -> bool

func request_chunk(chunk_path: String) -> void:
    if _pending.has(chunk_path):
        return
    _pending[chunk_path] = true
    ResourceLoader.load_threaded_request(chunk_path)

func _process(_delta: float) -> void:
    for path in _pending.keys():
        var status := ResourceLoader.load_threaded_get_status(path)
        match status:
            ResourceLoader.THREAD_LOAD_LOADED:
                var res: PackedScene = ResourceLoader.load_threaded_get(path)
                _pending.erase(path)
                var instance := res.instantiate()
                add_child(instance)
                chunk_ready.emit(path, instance)
            ResourceLoader.THREAD_LOAD_FAILED:
                push_error("Chunk load failed: %s" % path)
                _pending.erase(path)
```

### Pattern 6 — Decal Projection for Surface Detail

Spawn `Decal3D` nodes at runtime to mark surfaces with impacts, blood, scorch marks, or mud.

```gdscript
# effects/decal_spawner.gd
extends Node3D

@export var decal_scene: PackedScene  # scene root = Decal3D

func spawn_decal(
    hit_position: Vector3,
    hit_normal: Vector3,
    texture: Texture2D,
    size: Vector3 = Vector3(0.5, 0.5, 0.5),
    lifetime: float = 30.0
) -> void:
    var decal: Decal3D = decal_scene.instantiate()
    get_tree().current_scene.add_child(decal)

    decal.texture_albedo = texture
    decal.size = size
    decal.upper_fade = 0.3
    decal.lower_fade = 0.3

    # Orient decal so its -Y axis aligns with the surface normal
    decal.global_position = hit_position + hit_normal * 0.01
    decal.global_basis = Basis.looking_at(-hit_normal, Vector3.UP)

    if lifetime > 0.0:
        var timer := get_tree().create_timer(lifetime)
        await timer.timeout
        if is_instance_valid(decal):
            decal.queue_free()
```

## Common Pitfalls

- **Forgetting to rebake after geometry changes.** `bake_navigation_mesh()` must be called every time walkable surfaces are added, removed, or moved. A stale nav mesh silently produces wrong or absent paths.
- **`GridMap` cell size mismatch.** If the `MeshLibrary` collision shapes do not exactly match `GridMap.cell_size`, gaps or overlaps appear in collision. Author all library meshes on a grid unit that equals `cell_size`.
- **`NavigationMesh.cell_size` too large.** A coarse cell size (e.g. `1.0` for a corridor with 0.8 m clearance) causes the nav mesh to miss narrow passages entirely. Keep `cell_size` at most half the narrowest corridor width.
- **Blocking the main thread with synchronous bakes.** `bake_navigation_mesh(false)` (synchronous) freezes gameplay for large meshes. Always pass `true` for the `on_thread` argument in scenes larger than a few hundred square metres, and await `bake_finished`.
- **Polling `load_threaded_get_status()` without checking `THREAD_LOAD_FAILED`.** Silently ignoring failed loads leaves `_pending` populated forever, causing repeated status checks on a dead resource every frame.
- **Placing `Decal3D` without `upper_fade`/`lower_fade`.** Without fade, decals clip sharply at the bounding box edges and look artificial. Always set both values.
- **`NavigationAgent3D` target set before the nav map is ready.** If `target_position` is set before the map is baked (e.g. in `_ready()`), the agent returns an empty path. Wait for `NavigationServer3D`'s `map_changed` signal or the region's `bake_finished` signal first.

## Performance

### Streaming

Use `ResourceLoader.load_threaded_request()` to load chunk scenes in the background (see Pattern 5). Unload distant chunks by calling `queue_free()` on their root node and removing the path from tracking. Keep chunk boundaries aligned to a power-of-two grid so visibility checks are O(1) lookups.

### GridMap Cell Size

`GridMap.cell_size` directly controls the number of draw calls and collision bodies. Larger cells reduce draw calls but require bulkier library meshes. Profile with `rendering/debug/draw_call_debug_enabled` and aim for fewer than 1000 unique `GridMap` draw calls per visible region.

### Occlusion Strategy

- Place `OccluderInstance3D` nodes on every static mesh larger than ~1 m². Use `QuadOccluder3D` for flat walls, `ArrayOccluder3D` for convex hulls.
- Enable **Occlusion Culling** in `Project > Rendering > Occlusion Culling`.
- For `MultiMeshInstance3D` foliage, set a visibility range (`GeometryInstance3D.visibility_range_end`) to cull distant instances by distance rather than occlusion — cheaper for dense scatter fields.
- Use `NavigationRegion3D` regions per chunk rather than one global region so bakes are incremental.

## Anti-Patterns

### CSG in Production Builds

**Wrong** — shipping a level built from `CSGBox3D`, `CSGCylinder3D`, etc.:

```gdscript
# Never do this in a shipping scene
var wall := CSGBox3D.new()
wall.size = Vector3(4, 3, 0.2)
add_child(wall)
```

CSG nodes are evaluated at runtime, cannot be batched by the renderer, generate no LODs, and produce poor collision meshes. They exist **only for rapid prototyping**.

**Right** — bake CSG to a `MeshInstance3D` and replace:

1. Build the CSG layout in the editor.
2. Select the root `CSGShape3D`, choose **Mesh > Bake Mesh** (or call `bake_static_mesh()` via script).
3. Replace the CSG nodes with the resulting `MeshInstance3D` + a `StaticBody3D` with `CollisionPolygonShape3D` generated from the mesh.
4. Delete all `CSGShape3D` nodes before export.

```gdscript
# editor_tool/csg_baker.gd  (EditorScript or tool scene)
@tool
extends EditorScript

func _run() -> void:
    var csg: CSGShape3D = get_scene().find_child("PrototypeWall") as CSGShape3D
    if csg == null:
        push_error("No CSGShape3D named PrototypeWall found.")
        return
    var mesh_instance := MeshInstance3D.new()
    mesh_instance.mesh = csg.bake_static_mesh()
    mesh_instance.name = csg.name + "_Baked"
    csg.get_parent().add_child(mesh_instance)
    mesh_instance.owner = get_scene()
    csg.queue_free()
```

### Synchronous Heavy Bakes on the Main Thread

**Wrong:**
```gdscript
func _ready() -> void:
    nav_region.bake_navigation_mesh(false)  # blocks for seconds on large mesh
```

**Right:**
```gdscript
func _ready() -> void:
    nav_region.bake_navigation_mesh(true)
    await nav_region.bake_finished
```

### One Global NavigationRegion3D for the Entire World

**Wrong** — single region covering a 2 km terrain bakes everything at once.

**Right** — one `NavigationRegion3D` per chunk/streaming cell, baked independently. Set `NavigationRegion3D.enabled = false` when the chunk is unloaded.

## References

- NavigationRegion3D: https://docs.godotengine.org/en/stable/classes/class_navigationregion3d.html
- NavigationMesh: https://docs.godotengine.org/en/stable/classes/class_navigationmesh.html
- NavigationServer3D: https://docs.godotengine.org/en/stable/classes/class_navigationserver3d.html
- NavigationAgent3D: https://docs.godotengine.org/en/stable/classes/class_navigationagent3d.html
- GridMap: https://docs.godotengine.org/en/stable/classes/class_gridmap.html
- MultiMesh: https://docs.godotengine.org/en/stable/classes/class_multimesh.html
- MultiMeshInstance3D: https://docs.godotengine.org/en/stable/classes/class_multimeshinstance3d.html
- FastNoiseLite: https://docs.godotengine.org/en/stable/classes/class_fastnoiselite.html
- TileMap: https://docs.godotengine.org/en/stable/classes/class_tilemap.html
- Decal3D: https://docs.godotengine.org/en/stable/classes/class_decal3d.html
- OccluderInstance3D: https://docs.godotengine.org/en/stable/classes/class_occluderinstance3d.html
- ResourceLoader (threaded): https://docs.godotengine.org/en/stable/classes/class_resourceloader.html
- CSGShape3D: https://docs.godotengine.org/en/stable/classes/class_csgshape3d.html
- Using navigation meshes (manual): https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationmeshes.html
- Large world coordinates: https://docs.godotengine.org/en/stable/tutorials/3d/large_world_coordinates.html

## Delegate to

| Task | Skill |
|---|---|
| Scene/node manipulation | `godot:scene` |
| Architecture decisions | `godot:architect` |
| API lookup | `godot:docs` |
