---
name: coder
description: Write idiomatic GDScript 4.x for Godot 4.7 — use when writing any GDScript code, autoloads, or class definitions.
type: implementation
---

# Godot Coder

> Expert GDScript 4.7 engineer writing typed, idiomatic, performant Godot code.

## Overview

Write GDScript for Godot 4.7 using static types everywhere, the modern property syntax, signal-first architecture, and scene-unique node references. Prefer crash-on-error over silent nulls — a type error caught at load time is better than a null that surfaces at runtime. When API is uncertain, delegate to `godot:docs` before writing.

## Key Language Features

| Feature | Syntax | Notes |
|---|---|---|
| Static typing | `var speed: float = 5.0` | Enables autocomplete, crashes on bad assignment |
| Class name | `class_name MyClass` | Registers globally; omit for private/internal scripts |
| Export | `@export var health: int = 100` | Inspector-visible; use typed exports |
| Scene-unique node | `@onready var player := %Player` | Prefer over long `$` paths |
| Property blocks | `var x: float: get: return _x` | Replaces Godot 3 `setget` |
| Signal declaration | `signal died(killer: Node)` | Typed args enforced at connect |
| Await | `await signal_name` | Replaces `yield`; suspends coroutine |
| Match expression | `match value: pattern: ...` | Exhaustive; no fall-through |
| Lambda / Callable | `var fn := func(x: int) -> int: return x * 2` | Closures capture outer scope |
| Inner class | `class Stats: var hp: int` | Scoped to parent script |
| Typed arrays | `var items: Array[EnemyData] = []` | ~3x faster iteration, type-safe |
| Static unload | `@static_unload` | Frees class statics on unload |

## Core Patterns

### Pattern 1 — Typed Node with Property and Signal

```gdscript
class_name Player
extends CharacterBody2D

signal health_changed(old_value: int, new_value: int)
signal died

@export var max_health: int = 100

@onready var _sprite: AnimatedSprite2D = %Sprite
@onready var _hurtbox: Area2D = %Hurtbox

var _health: int = max_health:
	get:
		return _health
	set(value):
		var prev := _health
		_health = clampi(value, 0, max_health)
		health_changed.emit(prev, _health)
		if _health == 0:
			died.emit()

func _ready() -> void:
	_hurtbox.area_entered.connect(_on_hurtbox_area_entered)

func _on_hurtbox_area_entered(area: Area2D) -> void:
	if area.is_in_group(&"projectile"):
		_health -= area.get_meta("damage", 10)
```

### Pattern 2 — Match Expression and Inner Class

```gdscript
class_name ItemFactory
extends RefCounted

class ItemData:
	var id: StringName
	var weight: float
	var rarity: int

	func _init(p_id: StringName, p_weight: float, p_rarity: int) -> void:
		id = p_id
		weight = p_weight
		rarity = p_rarity

enum Rarity { COMMON, RARE, EPIC, LEGENDARY }

static func describe_rarity(rarity: Rarity) -> String:
	match rarity:
		Rarity.COMMON:
			return "Common"
		Rarity.RARE:
			return "Rare"
		Rarity.EPIC:
			return "Epic"
		Rarity.LEGENDARY:
			return "Legendary"
		_:
			return "Unknown"

static func create(id: StringName) -> ItemData:
	match id:
		&"sword":
			return ItemData.new(&"sword", 2.5, Rarity.COMMON)
		&"rune_blade":
			return ItemData.new(&"rune_blade", 1.8, Rarity.EPIC)
		_:
			push_error("Unknown item id: %s" % id)
			return ItemData.new(id, 1.0, Rarity.COMMON)
```

### Pattern 3 — Async / Coroutine Chaining

```gdscript
class_name CutscenePlayer
extends Node

@export var dialogue_box: Control

func play_intro() -> void:
	# Wait for a signal
	await get_tree().create_timer(0.5).timeout
	dialogue_box.show()
	dialogue_box.set_text("Welcome, traveller.")

	# Wait for player input signal
	await dialogue_box.dismissed

	# Chain: fade out then switch scene
	await _fade_out(1.0)
	get_tree().change_scene_to_file("res://scenes/world.tscn")

func _fade_out(duration: float) -> void:
	var tween := create_tween()
	tween.tween_property(self, "modulate:a", 0.0, duration)
	await tween.finished
```

### Pattern 4 — Lambdas, Callables, and Typed Arrays

```gdscript
class_name EnemySpawner
extends Node

@export var enemy_scene: PackedScene
@export var max_enemies: int = 20

var _active_enemies: Array[Enemy] = []

func _ready() -> void:
	# Lambda stored as Callable
	var on_enemy_died := func(enemy: Enemy) -> void:
		_active_enemies.erase(enemy)

	# Typed array iteration — faster than untyped Array
	for enemy: Enemy in _active_enemies:
		enemy.died.connect(on_enemy_died.bind(enemy))

func spawn_at(pos: Vector2) -> Enemy:
	if _active_enemies.size() >= max_enemies:
		return null
	var enemy := enemy_scene.instantiate() as Enemy
	if enemy == null:
		push_error("enemy_scene is not of type Enemy")
		return null
	enemy.global_position = pos
	add_child(enemy)
	_active_enemies.append(enemy)
	return enemy

func get_nearest_to(pos: Vector2) -> Enemy:
	# Sort copy via lambda — original array untouched
	var sorted := _active_enemies.duplicate()
	sorted.sort_custom(func(a: Enemy, b: Enemy) -> bool:
		return a.global_position.distance_squared_to(pos) \
			< b.global_position.distance_squared_to(pos)
	)
	return sorted[0] if sorted.size() > 0 else null
```

### Pattern 5 — Freed-Object Safety and Unique Node References

```gdscript
class_name AbilityComponent
extends Node

# Use scene-unique names — never long relative paths
@onready var _target_indicator: Sprite2D = %TargetIndicator

var _current_target: Node = null

func set_target(node: Node) -> void:
	_current_target = node

func _process(_delta: float) -> void:
	# Always guard before using a stored node reference
	if not is_instance_valid(_current_target):
		_current_target = null
		_target_indicator.hide()
		return

	_target_indicator.show()
	_target_indicator.global_position = _current_target.global_position
```

## Common Pitfalls

- **`setget` is Godot 3 syntax** — in Godot 4 use property blocks with `get:` / `set(v):` inline under the variable declaration. Using `setget` silently does nothing.
- **Long `$` paths break on refactor** — `$"../../../UI/HUD/HealthBar"` breaks the moment you restructure the scene. Use `%UniqueNode` for any node you reference from code.
- **Unguarded freed-object access crashes** — storing a `Node` reference and calling methods on it after it is freed produces `Invalid get index` errors. Always call `is_instance_valid(node)` before use.
- **`Array` copies on assignment, `Resource` does not** — `var a := my_array` gives you a shallow copy; mutating `a` does not affect `my_array`. But `var r := my_resource` is a reference; edits affect the original. Use `resource.duplicate()` when you need a separate copy.
- **`await` without a target suspends forever** — `await some_signal` never resumes if `some_signal` is never emitted and the emitter is freed. Consider a timeout guard or check `is_instance_valid` before awaiting.
- **Untyped arrays skip Godot's fast-path** — `var enemies: Array = []` disables the optimised typed-array iteration. Always declare element types: `Array[Enemy]`.
- **`@static_unload` is required for utility classes** — classes with only static methods hold their statics in memory for the lifetime of the project unless decorated with `@static_unload`.

## Performance

**Use typed arrays for hot collections.**

```gdscript
# Slow — untyped, no fast-path
var bullets: Array = []

# Fast — typed, ~3x iteration speedup in benchmarks
var bullets: Array[Bullet] = []
```

**Hot path tips:**

- Cache `global_position` into a local `var` when reading it multiple times per frame.
- Avoid `get_node()` / `$` calls in `_process` — use `@onready` references.
- Prefer `distance_squared_to` over `distance_to` when comparing distances (avoids `sqrt`).
- Use `StringName` literals (`&"group_name"`) for group/meta keys — avoids repeated string hashing.
- Batch `add_child` calls; each call triggers scene-tree notifications.

**Profiling:**

```gdscript
# Instrument a suspect block
func _process(delta: float) -> void:
	var t := Time.get_ticks_usec()
	_do_expensive_work()
	print("work took %d µs" % (Time.get_ticks_usec() - t))
```

Use the built-in **Debugger > Profiler** tab for frame-level analysis. Enable **Monitor > Object count** to catch node leaks.

## Anti-Patterns

**String-based node access**

```gdscript
# Wrong — fragile, breaks on scene refactor
var hud = get_node("../../../UI/HUD")

# Right — scene-unique name, refactor-safe
@onready var _hud: HUD = %HUD
```

**Untyped variables**

```gdscript
# Wrong — silent nulls, no autocomplete
var speed = 5.0
var enemy = get_enemy()

# Right — crash-on-error, full autocomplete
var speed: float = 5.0
var enemy: Enemy = get_enemy()
```

**Godot 3 setget**

```gdscript
# Wrong — ignored in Godot 4
var health = 100 setget set_health

# Right — Godot 4 property block
var health: int = 100:
	set(value):
		health = clampi(value, 0, max_health)
		health_changed.emit(health)
```

**No freed-object guard**

```gdscript
# Wrong — crashes if target was queue_free'd
func _process(_delta: float) -> void:
	_target.global_position = global_position

# Right
func _process(_delta: float) -> void:
	if is_instance_valid(_target):
		_target.global_position = global_position
```

**Untyped array for game objects**

```gdscript
# Wrong — slow iteration, no type safety
var enemies: Array = []

# Right
var enemies: Array[Enemy] = []
```

## References

- GDScript reference (4.x): https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html
- Static typing: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html
- Signals: https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html
- Coroutines / await: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#awaiting-for-signals-or-coroutines
- Property syntax: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#properties-setters-and-getters
- Typed arrays: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#typed-arrays
- Scene-unique nodes: https://docs.godotengine.org/en/stable/tutorials/scripting/scene_unique_nodes.html
- Best practices: https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html

## Delegate to

- Use `godot:docs` for API lookup before writing code that touches unfamiliar classes or methods.

## Test Snippets via AgentBridge

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"

# Quick one-liner test:
$GDEXEC --execute 'print(Vector3.UP.rotated(Vector3.RIGHT, PI/4))'

# Test a match expression:
$GDEXEC --execute - <<'GD'
var rarity := 2
match rarity:
	0: print("Common")
	1: print("Rare")
	2: print("Epic")
	_: print("Unknown")
GD

# Test typed array iteration:
$GDEXEC --execute - <<'GD'
var nums: Array[int] = [1, 2, 3, 4, 5]
var doubled := nums.map(func(x: int) -> int: return x * 2)
print(doubled)
GD

# Test await with timer:
$GDEXEC --execute - <<'GD'
print("before")
await Engine.get_main_loop().create_timer(0.1).timeout
print("after 100ms")
GD

# Test property block:
$GDEXEC --execute - <<'GD'
var _val: int = 0
# inline property not supported in bare scripts; test via class:
print("property syntax requires class context — test in a Node script")
GD

# Check recent output / errors:
$GDEXEC --log 50
```
