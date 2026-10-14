---
name: signals
description: Design and implement Godot signal-driven architecture — use when connecting nodes, designing event systems, or debugging missing connections.
type: implementation
---

# Godot Signals

> You are a Godot signal architecture expert who designs decoupled, event-driven systems using typed signals, connection flags, and coroutine suspension.

## Overview

Signals are Godot's built-in observer pattern. They allow nodes to communicate without holding direct references to each other, keeping the scene tree decoupled. In GDScript 4.x, signals are first-class typed objects with `.emit()`, `.connect()`, `.disconnect()`, and `is_connected()` methods.

Use signals when:
- A child needs to notify a parent or sibling without knowing who is listening
- Multiple systems need to react to the same event
- You want to avoid tight coupling between autoloads, scenes, or layers

## Signal Flow Rules

- Signals flow **up** the tree (child → parent). Method calls flow **down**.
- Never store a reference to a sibling — use signals or an autoload event bus.
- Disconnect in `_exit_tree` if you connected manually outside of `_ready` (connections made in `_ready` to nodes that share the same lifetime are cleaned up automatically when the node is freed).
- Always prefer typed `.emit()` over `emit_signal("name")` — it catches type errors at parse time and is faster at runtime.
- Guard duplicate connections with `is_connected()` or use `CONNECT_REFERENCE_COUNTED` if re-connecting intentionally.
- Emit signals after state has been updated, not before — listeners see consistent state.
- Lambdas connected as callbacks must be stored in a variable if you ever need to disconnect them — anonymous closures produce unique `Callable` objects each time.

## Core Patterns

### Pattern 1: Typed Signal Declaration and Basic Connection

```gdscript
# health_component.gd
class_name HealthComponent
extends Node

signal health_changed(new_health: int, delta: int)
signal died()

var max_health: int = 100
var health: int = 100

func take_damage(amount: int) -> void:
    var previous := health
    health = clampi(health - amount, 0, max_health)
    health_changed.emit(health, health - previous)
    if health == 0:
        died.emit()
```

```gdscript
# player_hud.gd
extends Control

@onready var health_component: HealthComponent = $"../Player/HealthComponent"

func _ready() -> void:
    health_component.health_changed.connect(_on_health_changed)
    health_component.died.connect(_on_player_died)

func _on_health_changed(new_health: int, _delta: int) -> void:
    %HealthBar.value = new_health

func _on_player_died() -> void:
    %DeathScreen.show()
```

### Pattern 2: Global Event Bus (Autoload)

```gdscript
# autoloads/event_bus.gd
class_name EventBus
extends Node

signal enemy_died(enemy_id: int, position: Vector3)
signal level_completed(level_index: int, score: int)
signal item_collected(item_type: StringName, collector: Node)
```

```gdscript
# enemy.gd — emitter
func die() -> void:
    EventBus.enemy_died.emit(id, global_position)
    queue_free()
```

```gdscript
# score_manager.gd — receiver (in _ready)
func _ready() -> void:
    EventBus.enemy_died.connect(_on_enemy_died)

func _on_enemy_died(enemy_id: int, _position: Vector3) -> void:
    score += enemy_point_values.get(enemy_id, 10)
```

### Pattern 3: One-Shot and Deferred Connections

```gdscript
# Fires once, then auto-disconnects.
func _ready() -> void:
    %StartButton.pressed.connect(_on_first_press, CONNECT_ONE_SHOT)

func _on_first_press() -> void:
    get_tree().change_scene_to_file("res://scenes/game.tscn")
```

```gdscript
# Deferred: callback runs at end of frame — safe inside physics callbacks.
func _ready() -> void:
    body_entered.connect(_on_body_entered, CONNECT_DEFERRED)

func _on_body_entered(body: Node3D) -> void:
    # Safe to add/remove nodes here; deferred avoids physics-step mutations.
    body.queue_free()
```

### Pattern 4: Signal Chaining

```gdscript
# signal_a.emit() automatically calls signal_b.emit() with the same arguments.
signal stage_cleared(stage: int)
signal ui_stage_cleared(stage: int)

func _ready() -> void:
    stage_cleared.connect(ui_stage_cleared.emit)

func complete_stage(n: int) -> void:
    stage_cleared.emit(n)  # ui_stage_cleared fires automatically
```

### Pattern 5: Lambda Callbacks and Coroutine Suspension

```gdscript
# Lambda callback — store the Callable to disconnect later.
func _ready() -> void:
    var _cb := func(): %FeedbackLabel.text = "Saved!"
    %SaveButton.pressed.connect(_cb)
    # To disconnect: %SaveButton.pressed.disconnect(_cb)
```

```gdscript
# await suspends the coroutine until the signal fires.
func show_dialog_and_wait() -> bool:
    %Dialog.show()
    var confirmed: bool = await %Dialog.choice_made
    %Dialog.hide()
    return confirmed
```

### Pattern 6: Guard Against Duplicate Connections

```gdscript
func connect_once(source: Node, sig: StringName, target: Callable) -> void:
    if not source.is_connected(sig, target):
        source.connect(sig, target)
```

```gdscript
# Or use CONNECT_REFERENCE_COUNTED for intentional multi-connect:
func _ready() -> void:
    some_signal.connect(_handler, CONNECT_REFERENCE_COUNTED)
    some_signal.connect(_handler, CONNECT_REFERENCE_COUNTED)
    # disconnect() must be called twice to fully remove _handler
```

## Connection Flags

| Flag | Effect | When to Use |
|---|---|---|
| `CONNECT_ONE_SHOT` | Auto-disconnects after the first emission | Initialization events, splash screens, tutorial triggers that fire exactly once |
| `CONNECT_DEFERRED` | Callback is queued to end of frame instead of called immediately | Physics step callbacks (`body_entered`, `area_entered`), anywhere that mutating the scene tree mid-call would cause errors |
| `CONNECT_REFERENCE_COUNTED` | Each `connect()` call increments a refcount; `disconnect()` decrements — fully removed when refcount reaches zero | Plugin/module systems where multiple owners share a connection and each manages its own lifetime |
| `CONNECT_PERSIST` | Connection is saved to the scene file (editor-only) | Wiring signals in the Godot editor Inspector so they survive scene serialization; not used in runtime code |

Flags can be combined with bitwise OR: `CONNECT_ONE_SHOT | CONNECT_DEFERRED`.

## Common Pitfalls

- **Connecting to freed nodes.** If the emitter outlives the receiver, the callback fires on a freed object and crashes. Use `is_instance_valid(receiver)` in the callback or ensure the receiver disconnects in `_exit_tree`.
- **Lambda disconnect failure.** `button.pressed.disconnect(func(): print("x"))` silently fails because each `func()` literal creates a new `Callable` with a different identity. Always store lambdas in a variable before connecting.
- **`disconnect()` callable mismatch.** `disconnect()` requires the exact same `Callable` object (same object reference and same method). Passing a re-bound or wrapped version of the method will raise an error.
- **Emitting before state is final.** Emitting `health_changed` before clamping or updating dependent state means listeners read stale or inconsistent data. Mutate all state first, then emit.
- **Using `emit_signal("name")` in GDScript 4.x.** It works but bypasses static type checking and is slower than the typed `.emit()` form. Linters will warn on it.
- **Physics callback mutations without CONNECT_DEFERRED.** Adding or removing nodes inside a physics-step signal (e.g., `body_entered`) without deferring can corrupt the physics server state mid-step.
- **Circular signal chains.** `signal_a` connects to `signal_b.emit` and `signal_b` connects to `signal_a.emit` — infinite recursion until stack overflow. Always audit chains for cycles.

## Performance

**Emission cost.** Signal emission in GDScript 4.x is cheap for low subscriber counts — roughly equivalent to a direct method call per connected callable. It becomes measurable only when hundreds of signals fire per frame with many subscribers each.

**Polling vs signals.** Polling state in `_process` (e.g., `if health != last_health`) wastes CPU every frame even when nothing changed. Signals pay a tiny connection overhead but eliminate continuous polling. Prefer signals for infrequent or irregular events; polling is acceptable for values that change nearly every frame anyway (e.g., lerped positions).

**`CONNECT_DEFERRED` overhead.** Deferred callbacks are pushed onto the message queue and flushed at the end of the physics or idle frame. This adds one frame of latency. Use it only where needed (physics callbacks, scene tree mutation) — it is not a general-purpose optimisation.

**`await` cost.** `await signal` suspends the current coroutine and resumes it when the signal fires. The suspension itself is cheap (one Callable allocation). Avoid `await` in tight inner loops; it is designed for sequential async flows, not per-frame work.

**Typed signals vs `Variant` signals.** Declaring signal arguments with explicit types (`signal foo(x: float)`) allows the engine to skip Variant boxing for primitive types in some call paths and catches errors earlier, with no runtime downside.

## Anti-Patterns

**Wrong — direct sibling reference:**
```gdscript
# player.gd
func _ready() -> void:
    $"../HUD".update_health(health)  # brittle: breaks if HUD moves in tree
```

**Right — signal to parent/event bus:**
```gdscript
# player.gd
signal health_changed(new_value: int)

func take_damage(amount: int) -> void:
    health -= amount
    health_changed.emit(health)  # HUD listens; Player has no reference to HUD
```

---

**Wrong — string-based emit:**
```gdscript
emit_signal("health_changed", health)  # no type checking, slower
```

**Right — typed emit:**
```gdscript
health_changed.emit(health)  # type-safe, parse-time error if args mismatch
```

---

**Wrong — connecting in a loop without a guard:**
```gdscript
func refresh() -> void:
    source.data_updated.connect(_on_data_updated)  # duplicate each call
```

**Right — guard or one-shot:**
```gdscript
func refresh() -> void:
    if not source.is_connected("data_updated", _on_data_updated):
        source.data_updated.connect(_on_data_updated)
```

---

**Wrong — anonymous lambda disconnect attempt:**
```gdscript
button.pressed.connect(func(): do_thing())
button.pressed.disconnect(func(): do_thing())  # different Callable, fails silently
```

**Right — store the Callable:**
```gdscript
var _on_pressed := func(): do_thing()
button.pressed.connect(_on_pressed)
button.pressed.disconnect(_on_pressed)  # same object, works correctly
```

## References

- [Signals — Godot Docs](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html)
- [GDScript reference: Signals](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#signals)
- [Using signals — best practices](https://docs.godotengine.org/en/stable/tutorials/best_practices/signals.html)
- [Object.connect() — API reference](https://docs.godotengine.org/en/stable/classes/class_object.html#class-object-method-connect)
- [Object.is_connected() — API reference](https://docs.godotengine.org/en/stable/classes/class_object.html#class-object-method-is-connected)
- [Coroutines and await](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#awaiting-signals-or-coroutines)

## Verify Connections via AgentBridge

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"

$GDEXEC --execute - <<'GD'
var node = EditorInterface.get_edited_scene_root().get_node("Player")
var connections = node.get_signal_list()
for sig in connections:
    print(sig.name, ": ", node.get_signal_connection_list(sig.name))
GD
```
