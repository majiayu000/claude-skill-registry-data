---
name: ai
description: Godot AI developer — use when implementing NPC pathfinding, NavigationAgent3D, behavior state machines, or detection systems.
type: implementation
---

# Godot AI

> Expert Godot 4.x AI programmer specializing in navigation, perception, behavior trees, and steering systems.

## Overview

Godot 4.x AI systems are built from three layers: **navigation** (`NavigationAgent3D` + `NavigationServer3D`), **perception** (vision cones, sound `Area3D`, influence maps), and **decision-making** (state machines, behavior trees). Avoidance runs on a separate thread via RVO2; behavior trees are pure GDScript. All pathfinding requires a baked `NavigationMesh` or `NavigationRegion3D`.

## Key Nodes & APIs

| Node / API | Purpose | Key Properties |
|---|---|---|
| `NavigationAgent3D` | Per-agent pathfinding + RVO avoidance | `target_position`, `avoidance_enabled`, `avoidance_priority`, `max_speed` |
| `NavigationRegion3D` | Defines walkable surface | `navigation_mesh`, `bake_navigation_mesh()` |
| `NavigationServer3D` | Singleton; baking, agent callbacks | `agent_set_callback()`, `map_force_update()` |
| `Area3D` + `CollisionShape3D` | Detection volumes (sound, proximity) | `body_entered`, `body_exited`, `monitoring` |
| `RayCast3D` | Line-of-sight verification | `target_position`, `get_collider()` |
| `CharacterBody3D` | NPC physics body | `velocity`, `move_and_slide()` |

## Core Patterns

### Pattern 1 — NavigationAgent3D Basic Chase

```gdscript
extends CharacterBody3D

@onready var nav: NavigationAgent3D = $NavigationAgent3D

var target: Node3D = null

func _ready() -> void:
    nav.velocity_computed.connect(_on_velocity_computed)

func _physics_process(_delta: float) -> void:
    if target == null:
        return
    nav.target_position = target.global_position
    if nav.is_navigation_finished():
        return
    var next: Vector3 = nav.get_next_path_position()
    var desired: Vector3 = (next - global_position).normalized() * nav.max_speed
    nav.set_velocity(desired)

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    velocity = safe_velocity
    move_and_slide()
```

### Pattern 2 — Behavior Tree (BTNode / BTSequence / BTSelector)

```gdscript
# behavior_tree.gd
class_name BehaviorTree
extends Resource

enum Status { SUCCESS, FAILURE, RUNNING }

# ── Base node ──────────────────────────────────────────────────────────────
class BTNode:
    func tick(actor: Node) -> BehaviorTree.Status:
        return BehaviorTree.Status.FAILURE

# ── Sequence: runs children in order; stops and returns FAILURE on first failure
class BTSequence extends BTNode:
    var children: Array[BTNode] = []

    func tick(actor: Node) -> BehaviorTree.Status:
        for child in children:
            var result: BehaviorTree.Status = child.tick(actor)
            if result != BehaviorTree.Status.SUCCESS:
                return result
        return BehaviorTree.Status.SUCCESS

# ── Selector: runs children in order; stops and returns SUCCESS on first success
class BTSelector extends BTNode:
    var children: Array[BTNode] = []

    func tick(actor: Node) -> BehaviorTree.Status:
        for child in children:
            var result: BehaviorTree.Status = child.tick(actor)
            if result != BehaviorTree.Status.FAILURE:
                return result
        return BehaviorTree.Status.FAILURE

# ── Leaf: check whether actor has a visible target
class HasTarget extends BTNode:
    func tick(actor: Node) -> BehaviorTree.Status:
        return BehaviorTree.Status.SUCCESS if actor.target != null else BehaviorTree.Status.FAILURE

# ── Leaf: move actor toward its target via NavigationAgent3D
class ChaseTarget extends BTNode:
    func tick(actor: Node) -> BehaviorTree.Status:
        if actor.target == null:
            return BehaviorTree.Status.FAILURE
        actor.nav.target_position = actor.target.global_position
        return BehaviorTree.Status.RUNNING

# ── Leaf: play idle animation
class Idle extends BTNode:
    func tick(actor: Node) -> BehaviorTree.Status:
        actor.animation_player.play("idle")
        return BehaviorTree.Status.SUCCESS
```

Usage in an NPC:

```gdscript
# npc.gd
extends CharacterBody3D

@onready var nav: NavigationAgent3D = $NavigationAgent3D
@onready var animation_player: AnimationPlayer = $AnimationPlayer

var target: Node3D = null
var _tree: BehaviorTree.BTNode

func _ready() -> void:
    nav.velocity_computed.connect(_on_velocity_computed)
    # Build tree: chase if target exists, otherwise idle
    var selector := BehaviorTree.BTSelector.new()
    var chase_seq := BehaviorTree.BTSequence.new()
    chase_seq.children = [BehaviorTree.HasTarget.new(), BehaviorTree.ChaseTarget.new()]
    selector.children = [chase_seq, BehaviorTree.Idle.new()]
    _tree = selector

func _physics_process(_delta: float) -> void:
    _tree.tick(self)

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    velocity = safe_velocity
    move_and_slide()
```

### Pattern 3 — Vision Cone + Raycast Line-of-Sight

```gdscript
# Returns true when `target` is inside the cone AND visible via raycast.
func can_see(target: Node3D) -> bool:
    var to_target: Vector3 = target.global_position - global_position
    var distance: float = to_target.length()
    if distance > sight_range:
        return false

    var forward: Vector3 = -global_transform.basis.z  # NPC faces -Z
    var dot: float = forward.dot(to_target.normalized())
    if dot < cos(deg_to_rad(half_fov_degrees)):
        return false

    # Raycast to verify no obstacle between NPC and target
    var space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
    var query := PhysicsRayQueryParameters3D.create(
        global_position + Vector3.UP * 0.5,
        target.global_position + Vector3.UP * 0.5
    )
    query.exclude = [self]
    var result: Dictionary = space.intersect_ray(query)
    if result.is_empty():
        return true
    return result.collider == target
```

### Pattern 4 — Sound Radius Detection with Area3D

```gdscript
# sound_detector.gd — attach to an Area3D with a SphereShape3D CollisionShape3D
extends Area3D

signal player_detected(player: Node3D)
signal player_lost(player: Node3D)

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)
    # Restrict to player physics layer only
    collision_mask = 1 << 0  # layer 1 = player

func _on_body_entered(body: Node3D) -> void:
    if body.is_in_group("player"):
        player_detected.emit(body)

func _on_body_exited(body: Node3D) -> void:
    if body.is_in_group("player"):
        player_lost.emit(body)
```

### Pattern 5 — Steering Behaviors (Seek / Arrive)

```gdscript
const SLOW_RADIUS: float = 3.0

func seek(target_pos: Vector3) -> Vector3:
    return (target_pos - global_position).normalized() * max_speed

func arrive(target_pos: Vector3) -> Vector3:
    var to_target: Vector3 = target_pos - global_position
    var distance: float = to_target.length()
    if distance < 0.01:
        return Vector3.ZERO
    var speed: float = max_speed
    if distance < SLOW_RADIUS:
        speed = max_speed * (distance / SLOW_RADIUS)
    return to_target.normalized() * speed
```

### Pattern 6 — Group Coordination (Find Nearest Ally)

```gdscript
func get_nearest_ally() -> Node3D:
    var allies: Array[Node] = get_tree().get_nodes_in_group("enemies")
    var nearest: Node3D = null
    var best_dist: float = INF
    for ally in allies:
        if ally == self:
            continue
        var d: float = global_position.distance_to((ally as Node3D).global_position)
        if d < best_dist:
            best_dist = d
            nearest = ally as Node3D
    return nearest
```

### Pattern 7 — Influence Map for Tactical Scoring

```gdscript
# influence_map.gd — singleton or component
extends Node

const CELL_SIZE: float = 2.0
var _map: Dictionary = {}  # Vector3i -> float

func add_influence(world_pos: Vector3, value: float, radius: int = 3) -> void:
    var origin: Vector3i = _to_cell(world_pos)
    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            var cell := Vector3i(origin.x + x, origin.y, origin.z + z)
            var dist: float = Vector2(x, z).length()
            var falloff: float = maxf(0.0, 1.0 - dist / radius)
            _map[cell] = _map.get(cell, 0.0) + value * falloff

func get_influence(world_pos: Vector3) -> float:
    return _map.get(_to_cell(world_pos), 0.0)

func decay(delta: float, rate: float = 0.5) -> void:
    for cell in _map.keys():
        _map[cell] *= pow(1.0 - rate, delta)
        if _map[cell] < 0.01:
            _map.erase(cell)

func _to_cell(pos: Vector3) -> Vector3i:
    return Vector3i(
        floori(pos.x / CELL_SIZE),
        floori(pos.y / CELL_SIZE),
        floori(pos.z / CELL_SIZE)
    )
```

## Common Pitfalls

- **Not setting `target_position` every frame for moving targets.** `NavigationAgent3D` does not automatically track a moving target. Assign `nav.target_position = target.global_position` each `_physics_process` call.
- **Applying `nav.get_next_path_position()` velocity directly instead of routing through `set_velocity()`.** Skipping `set_velocity()` disables RVO avoidance; NPCs will overlap and clip through each other.
- **Checking `is_navigation_finished()` before the first frame path is computed.** It returns `true` on frame 0 before any path exists. Guard with a target-assigned flag or check `nav.distance_to_target() > nav.target_desired_distance`.
- **Setting `NavigationAgent3D.avoidance_enabled = true` without connecting `velocity_computed`.** Avoidance runs asynchronously; if you never consume the signal result, avoidance silently does nothing.
- **Baking `NavigationMesh` every frame or on every spawn.** Baking is expensive — bake once at scene load and again only when geometry changes, never per-frame.
- **Using per-frame `distance_to()` loops to find nearby enemies instead of `Area3D`.** Physics broadphase is far cheaper; use an `Area3D` collision shape for detection triggers.
- **Performing raycasts in `_process` for vision checks on dozens of NPCs simultaneously.** Stagger raycasts across multiple frames using a round-robin index or `call_deferred`.

## Performance

| Concern | Recommendation |
|---|---|
| Avoidance cost | Enable `avoidance_enabled` only for agents near the player; disable for distant or sleeping NPCs. Each enabled agent costs O(n) per other nearby agent per frame. |
| Navigation bake frequency | Bake once at startup (`NavigationRegion3D.bake_navigation_mesh()`) and only rebake when static geometry changes. Use `NavigationServer3D.map_force_update()` after dynamic changes. |
| Group call cost | `get_tree().get_nodes_in_group()` allocates a new `Array` each call. Cache the result or use a manager singleton for groups queried every frame. |
| `avoidance_priority` | Range 0.0–1.0; higher priority agents push others away without being pushed themselves. Use for bosses or tanks; leave at default `0.5` for generic NPCs. |
| `agent_set_callback()` | `NavigationServer3D.agent_set_callback(agent_rid, callable)` registers a low-level callback for avoidance velocity; prefer the `velocity_computed` signal on `NavigationAgent3D` unless you manage RIDs manually. |
| Influence maps | Update only cells that changed this frame; call `decay()` in `_process` with `delta` to amortize cost. Use `Vector3i` keys — faster hashing than `Vector3`. |

## Anti-Patterns

| Wrong | Right |
|---|---|
| `if pos.distance_to(player.global_position) < 10.0:` per frame in 30 NPCs | `Area3D` with radius-10 sphere; respond to `body_entered` signal |
| Nested `if/elif` for 5+ NPC states | `enum State` + `match current_state` + one function per state |
| `nav.velocity = (next - pos).normalized() * speed; move_and_slide()` | `nav.set_velocity(desired); # wait for velocity_computed signal` |
| `NavigationRegion3D.bake_navigation_mesh()` in `_process` | Bake once in `_ready()` or on level load |
| Direct state assignment from outside: `npc.state = State.FLEE` | Expose a method: `npc.request_flee(threat_position)` |
| Running vision raycasts every frame for all NPCs | Stagger across frames: `if Engine.get_process_frames() % 4 == npc_id % 4:` |

## References

- NavigationAgent3D: https://docs.godotengine.org/en/stable/classes/class_navigationagent3d.html
- NavigationServer3D: https://docs.godotengine.org/en/stable/classes/class_navigationserver3d.html
- NavigationRegion3D: https://docs.godotengine.org/en/stable/classes/class_navigationregion3d.html
- Using NavigationAgent: https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html
- RVO Avoidance: https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_avoidance.html
- Area3D: https://docs.godotengine.org/en/stable/classes/class_area3d.html
- PhysicsDirectSpaceState3D: https://docs.godotengine.org/en/stable/classes/class_physicsdirectspacestate3d.html
- GDScript exports and typing: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html

## Delegate to

| Task | Skill |
|---|---|
| GDScript implementation | `godot:coder` |
| Signal connections | `godot:signals` |
| API lookup | `godot:docs` |
