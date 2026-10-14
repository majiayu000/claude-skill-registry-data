---
name: architect
description: Design Godot project structure — use when designing autoloads, resource architecture, scene organization, or plugin layout.
type: guidance
---

# Godot Architect

> Expert Godot 4 project architect specializing in scene composition, resource systems, autoload patterns, and scalable game structure.

## Overview

This skill covers the structural layer of a Godot 4 project: how scenes relate to each other, how data flows through the node tree, when autoloads are appropriate, and how to organize code so that systems remain decoupled and independently testable.

**Domain:** Scene hierarchy design, autoload architecture, resource-based data, plugin layout, dependency management.

**Philosophy:** Prefer composition over inheritance. Each scene should own its behaviour, expose a minimal surface via signals and exported properties, and have no hard dependencies on siblings or global singletons. Data lives in `Resource` subclasses, not plain `Dictionary` objects. Communication travels up the tree via signals and down via method calls.

**When to use this skill:**
- Designing or refactoring an autoload graph
- Deciding whether to use `Node`, `RefCounted`, or `Resource` for a new class
- Laying out a scene hierarchy for a new system (inventory, dialogue, combat)
- Structuring a plugin or tool addon
- Hitting serialization bugs related to `owner`
- Concerned about active node count or scene-tree overhead

## Key Nodes & APIs

| Node / Class | Purpose | Key Properties / Methods |
|---|---|---|
| `Node` | Base scene-tree participant | `owner`, `add_child()`, `queue_free()`, `get_tree()` |
| `RefCounted` | Lightweight reference-counted object, no scene-tree | automatic ref tracking, no `_process`, no signals without `Object` cast |
| `Resource` | Serialisable data container, sharable across scenes | `@export` fields, `resource_path`, `duplicate()` |
| `PackedScene` | Compiled scene blueprint for instancing | `instantiate()`, used in object pools |
| `Autoload (Node singleton)` | Global service accessible by name from any script | Project Settings → Autoload; avoid tight coupling |
| `SceneTree` | Root controller; provides groups, timers, change_scene | `get_nodes_in_group()`, `create_timer()`, `change_scene_to_file()` |
| `MultiMeshInstance3D` | Render thousands of identical meshes in one draw call | `multimesh`, `instance_count`, `set_instance_transform()` |
| `EditorPlugin` | Entry point for editor addons | `_enter_tree()`, `add_tool_menu_item()`, `get_editor_interface()` |

## Core Patterns

### Pattern 1 — Scene Composition over Inheritance

Favour small, focused scenes assembled together rather than deep class hierarchies. Each child scene is independently runnable with F6 and has no knowledge of its parent.

```gdscript
# health_component.gd — reusable, self-contained
class_name HealthComponent
extends Node

signal died
signal health_changed(new_value: int, max_value: int)

@export var max_health: int = 100
var current_health: int

func _ready() -> void:
    current_health = max_health

func take_damage(amount: int) -> void:
    current_health = max(0, current_health - amount)
    health_changed.emit(current_health, max_health)
    if current_health == 0:
        died.emit()

func heal(amount: int) -> void:
    current_health = min(max_health, current_health + amount)
    health_changed.emit(current_health, max_health)
```

```gdscript
# enemy.gd — composes HealthComponent; no base class needed
class_name Enemy
extends CharacterBody3D

@onready var health: HealthComponent = $HealthComponent

func _ready() -> void:
    health.died.connect(_on_died)

func _on_died() -> void:
    queue_free()
```

The `Enemy` scene contains `HealthComponent` as a child node. Swapping it for a different health model requires no code change in `Enemy`.

---

### Pattern 2 — Dependency Injection via Resource Constructor Arguments

Avoid coupling systems to autoloads by passing `Resource` configuration objects at construction time. This makes every system unit-testable in isolation.

```gdscript
# weapon_config.gd
class_name WeaponConfig
extends Resource

@export var damage: int = 25
@export var fire_rate: float = 0.5
@export var projectile_scene: PackedScene
```

```gdscript
# weapon.gd — receives its config; no autoload dependency
class_name Weapon
extends Node3D

var config: WeaponConfig

static func create(cfg: WeaponConfig) -> Weapon:
    var w: Weapon = preload("res://scenes/weapon/weapon.tscn").instantiate()
    w.config = cfg
    return w

func fire() -> void:
    if config.projectile_scene == null:
        return
    var projectile := config.projectile_scene.instantiate()
    get_tree().current_scene.add_child(projectile)
    projectile.global_position = global_position
```

```gdscript
# player.gd — wires config at runtime; testable by passing a mock config
func _ready() -> void:
    var cfg := preload("res://resources/weapons/pistol.tres") as WeaponConfig
    var weapon := Weapon.create(cfg)
    add_child(weapon)
```

---

### Pattern 3 — Object Pool with PackedScene Pre-instantiation

Pre-instantiate nodes at load time to avoid per-frame allocation spikes. Return nodes to the pool rather than freeing them.

```gdscript
# object_pool.gd
class_name ObjectPool
extends Node

@export var scene: PackedScene
@export var initial_size: int = 20

var _available: Array[Node] = []

func _ready() -> void:
    for i in initial_size:
        var instance := scene.instantiate()
        instance.process_mode = Node.PROCESS_MODE_DISABLED
        add_child(instance)
        _available.append(instance)

func acquire() -> Node:
    if _available.is_empty():
        var instance := scene.instantiate()
        add_child(instance)
        return instance
    var node := _available.pop_back()
    node.process_mode = Node.PROCESS_MODE_INHERIT
    return node

func release(node: Node) -> void:
    node.process_mode = Node.PROCESS_MODE_DISABLED
    _available.append(node)
```

```gdscript
# bullet_manager.gd — uses pool instead of instantiate/free per shot
@onready var pool: ObjectPool = $BulletPool

func spawn_bullet(pos: Vector3, dir: Vector3) -> void:
    var bullet := pool.acquire()
    bullet.global_position = pos
    bullet.direction = dir
    # Bullet calls pool.release(self) when it exits the screen
```

---

### Pattern 4 — Safe Autoload Event Bus (Signals Only)

When a true broadcast channel is needed, limit the autoload to signal declarations with no mutable state. Nodes subscribe and unsubscribe; the bus owns nothing.

```gdscript
# autoloads/event_bus.gd
class_name EventBus
extends Node

signal player_died
signal score_changed(new_score: int)
signal level_completed(level_id: String)
# No variables. No logic. Signals only.
```

```gdscript
# ui/score_label.gd — subscribes in _ready, no direct reference to game logic
func _ready() -> void:
    EventBus.score_changed.connect(_on_score_changed)

func _on_score_changed(new_score: int) -> void:
    text = str(new_score)
```

Emitting from anywhere: `EventBus.score_changed.emit(100)` — no reference to the UI required.

## Common Pitfalls

- **Forgetting `owner` on runtime-added nodes breaks scene saving.** Any node created with `Node.new()` and added via `add_child()` has `owner == null`. The SceneTree serializer skips nodes without an owner. Set `node.owner = get_tree().edited_scene_root` (in editor tools) or `node.owner = root_scene_node` (in-game serialization). The shorthand `add_child(node, true)` does NOT set `owner`; it only sets `force_readable_name`.

- **Autoloads are not dependency injection.** An autoload is a globally visible singleton, not a service container. Using autoloads as DI creates hidden coupling: changing `GameManager` internals silently breaks every script that reads its fields. The service-locator pattern (`Engine.get_singleton("X")`) has the same flaw — callers depend on a name string with no compile-time contract. Use explicit `Resource` constructor arguments or `@export` node references instead.

- **Circular autoload dependencies cause silent load-order failures.** If `AutoloadA._ready()` calls `AutoloadB` and `AutoloadB._ready()` calls `AutoloadA`, one of them will receive a partially-initialised peer. Godot loads autoloads in the order listed in Project Settings. Design autoloads in a strict dependency hierarchy (data → events → managers) and never let lower layers reference higher ones.

- **Using `Node` when `RefCounted` is sufficient wastes scene-tree overhead.** Every `Node` participates in `_process`, `_physics_process`, group queries, and signal connections tracked by the tree. A helper class that only holds data and runs pure functions should extend `RefCounted` — it allocates less memory, has no per-frame hooks, and is garbage-collected automatically when its last reference drops. Reserve `Node` for objects that genuinely need tree lifetime or built-in virtual callbacks.

- **Deep inheritance chains break scene overrides.** If `EnemyBase` → `MeleeEnemy` → `BossEnemy`, exported property overrides set in the parent scene often fail to propagate correctly after refactors. Prefer one level of inheritance maximum; move shared behaviour into composited child scenes or static utility classes.

- **`duplicate()` on a Resource is shallow by default.** Calling `resource.duplicate()` copies the resource but leaves nested sub-resources as shared references. Two enemies sharing the same `EnemyData` instance will mutate each other's state at runtime. Pass `true` to `duplicate(true)` for a deep copy, or design resources to be immutable.

## Performance

**Node count budget:**
- Aim for fewer than **1 000 active nodes** in the scene tree per frame for typical 2D/3D games on mid-range hardware.
- "Active" means `process_mode != PROCESS_MODE_DISABLED` and visible. Pooled or hidden nodes still exist but cost almost nothing per frame.
- Profile with the **Debugger → Monitor → Object count** panel; spikes above 2 000 nodes warrant investigation.

**When to use nodes vs objects:**

| Need | Use |
|---|---|
| Tree lifetime, signals, built-in callbacks (_process, _input) | `Node` subclass |
| Pure data, config, shared state, serialisation | `Resource` subclass |
| Transient helper with no tree dependency | `RefCounted` subclass |
| Thousands of identical visual instances | `MultiMeshInstance3D` + custom data arrays |
| Collision-only objects without visuals | `Area3D` / `CollisionShape3D` inside pooled scenes |

**Instancing tips:**
- Use `PackedScene.instantiate()` during a loading screen or in `_ready()`, not inside `_process()`.
- Prefer `ResourceLoader.load_threaded_request()` for large scenes to avoid main-thread stalls.
- Group identical projectiles, particles, or enemies under a single `MultiMeshInstance3D` when their transforms are the only variable; this reduces draw calls from N to 1.
- Call `queue_free()` instead of `free()` — it defers deletion to the end of the frame and avoids use-after-free crashes.

## Anti-Patterns

**Service locator via autoload (wrong):**

```gdscript
# WRONG — hidden global coupling, no contract, breaks unit tests
func fire() -> void:
    var pool = Engine.get_singleton("BulletPool")
    var bullet = pool.acquire()
    bullet.position = position
```

**Explicit dependency injection (right):**

```gdscript
# RIGHT — dependency is declared, injectable, testable
var bullet_pool: ObjectPool  # set by parent or factory before _ready

func fire() -> void:
    var bullet := bullet_pool.acquire()
    bullet.position = position
```

---

**Deep inheritance for behaviour reuse (wrong):**

```gdscript
# WRONG — brittle hierarchy, exported vars break across levels
class_name BossEnemy extends MeleeEnemy  # MeleeEnemy extends EnemyBase
```

**Composition via child scene (right):**

```gdscript
# RIGHT — Boss is a CharacterBody3D that holds reusable component scenes
class_name Boss extends CharacterBody3D
# Child nodes: HealthComponent, MeleeAttackComponent, PhaseController
```

---

**Mutating shared Resource instances at runtime (wrong):**

```gdscript
# WRONG — all enemies share the same EnemyData; one death poisons the rest
func take_damage(amount: int) -> void:
    data.current_health -= amount  # data is a shared .tres asset
```

**Duplicating per-instance data correctly (right):**

```gdscript
# RIGHT — each enemy gets its own copy on spawn
@export var data_template: EnemyData

func _ready() -> void:
    var data := data_template.duplicate(true)  # deep copy
    _health = data.max_health
```

## References

- Scene organisation: https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html
- Autoloads vs internal nodes: https://docs.godotengine.org/en/stable/tutorials/best_practices/autoloads_versus_internal_nodes.html
- Resources: https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html
- Node `owner` property: https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-property-owner
- PackedScene and instancing: https://docs.godotengine.org/en/stable/classes/class_packedscene.html
- MultiMeshInstance3D: https://docs.godotengine.org/en/stable/classes/class_multimeshinstance3d.html
- RefCounted: https://docs.godotengine.org/en/stable/classes/class_refcounted.html
- GDScript exports: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_exports.html
- GDQuest — Godot best practices playlist: https://www.gdquest.com/tutorial/godot/best-practices/
- GDQuest — Node composition tutorial: https://www.gdquest.com/tutorial/godot/design-patterns/node-composition/

## Delegate to

| Task | Skill |
|---|---|
| Writing GDScript logic inside a designed system | `coder` |
| Debugging a scene-tree crash or null-reference error | `debugger` |
| Optimising draw calls, GPU, or shader performance | `performance` |
| Designing UI scene hierarchy and theme resources | `ui` |
| Setting up physics layers, collision shapes, joints | `physics` |
