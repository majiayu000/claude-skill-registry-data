---
name: gameplay
description: Godot gameplay developer — use when implementing player controllers, input handling, game mechanics, state machines, or save/load systems.
type: implementation
---

# Godot Gameplay

> Expert Godot 4.x gameplay programmer specialising in player controllers, input systems, state machines, and save/load architecture.

## Overview

This skill covers the full gameplay programming surface in Godot 4.x: character movement with `CharacterBody3D`, responsive input with buffering and coyote time, layered state machines, camera effects, and robust save-slot systems. All patterns target GDScript 4.7 and assume the Godot 4.x physics and input APIs.

## Key Nodes & APIs

| Node / API | Purpose | Key Methods / Properties |
|---|---|---|
| `CharacterBody3D` | Physics-driven player and NPC movement | `move_and_slide()`, `is_on_floor()`, `up_direction`, `floor_snap_length` |
| `CharacterBody2D` | 2-D equivalent | `move_and_slide()`, `is_on_floor()` |
| `Input` | Singleton for action polling | `is_action_pressed()`, `is_action_just_pressed()`, `get_action_strength()`, `get_vector()` |
| `InputMap` | Runtime action registration and remapping | `add_action()`, `action_add_event()` |
| `SceneTree` | Pause, scene switching, groups | `paused`, `create_timer()`, `change_scene_to_file()` |
| `Timer` (node) | Discrete delays | `wait_time`, `one_shot`, `timeout` signal |
| `FastNoiseLite` | Procedural noise for screen shake | `get_noise_1d()` |
| `Camera3D` / `Camera2D` | View, shake offset | `position`, `fov` |
| `ResourceSaver` | Persist `Resource` objects | `save(resource, path)` |
| `ResourceLoader` | Load persisted resources | `load(path)` |
| `DirAccess` | Directory operations for save slots | `make_dir_recursive_absolute()`, `dir_exists_absolute()` |
| `FileAccess` | Low-level binary/text IO | `open()`, `store_var()`, `get_var()` |
| `AnimationPlayer` | State-driven animations | `play()`, `queue()`, `current_animation` |

## Core Patterns

### Pattern 1 — Delta-Time Normalised Character Movement

Always multiply velocity contributions by `delta` inside `_physics_process` so movement is frame-rate independent.

```gdscript
extends CharacterBody3D

const SPEED := 6.0
const JUMP_VELOCITY := 5.5
const GRAVITY := 20.0

# Slope and stair handling
@export var floor_snap_length_value := 0.3

func _ready() -> void:
    up_direction = Vector3.UP
    floor_snap_length = floor_snap_length_value

func _physics_process(delta: float) -> void:
    # Apply gravity when airborne — multiply by delta
    if not is_on_floor():
        velocity.y -= GRAVITY * delta

    # Read analog stick / WASD and normalise
    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction := (transform.basis * Vector3(input_dir.x, 0.0, input_dir.y)).normalized()

    if direction:
        velocity.x = direction.x * SPEED
        velocity.z = direction.z * SPEED
    else:
        # Decelerate — still frame-rate independent
        velocity.x = move_toward(velocity.x, 0.0, SPEED * delta * 10.0)
        velocity.z = move_toward(velocity.z, 0.0, SPEED * delta * 10.0)

    move_and_slide()
```

### Pattern 2 — Coyote Time + Jump Buffer

Coyote time lets players jump slightly after walking off a ledge. Jump buffering queues a jump pressed slightly before landing so it fires immediately on touch-down.

```gdscript
extends CharacterBody3D

const JUMP_VELOCITY := 6.0
const GRAVITY := 22.0
const COYOTE_TIME := 0.12   # seconds after leaving floor
const JUMP_BUFFER_TIME := 0.10

var _coyote_timer: SceneTreeTimer = null
var _jump_buffer_timer: SceneTreeTimer = null
var _coyote_valid := false

func _physics_process(delta: float) -> void:
    var was_on_floor := is_on_floor()

    if not is_on_floor():
        velocity.y -= GRAVITY * delta

    # Start coyote window when player walks off edge
    if was_on_floor and not is_on_floor():
        _coyote_valid = true
        _coyote_timer = get_tree().create_timer(COYOTE_TIME)
        _coyote_timer.timeout.connect(func() -> void: _coyote_valid = false)

    # Record a buffered jump when the button is pressed in the air
    if Input.is_action_just_pressed("jump"):
        _jump_buffer_timer = get_tree().create_timer(JUMP_BUFFER_TIME)

    # Execute the jump if on-floor (or coyote-valid) AND buffer is live
    var buffer_live := _jump_buffer_timer != null and _jump_buffer_timer.time_left > 0.0
    var can_jump := is_on_floor() or _coyote_valid

    if buffer_live and can_jump:
        velocity.y = JUMP_VELOCITY
        _coyote_valid = false
        _jump_buffer_timer = null  # consume buffer

    move_and_slide()
```

### Pattern 3 — Input Buffer (Circular Queue)

For fighting-game-style systems, record the last N inputs and replay the most recent valid one on the next eligible frame.

```gdscript
class_name InputBuffer
extends RefCounted

const BUFFER_SIZE := 8

var _buffer: Array[StringName] = []
var _head := 0
var _count := 0

func push(action: StringName) -> void:
    if _buffer.size() < BUFFER_SIZE:
        _buffer.resize(BUFFER_SIZE)
    _buffer[_head] = action
    _head = (_head + 1) % BUFFER_SIZE
    _count = mini(_count + 1, BUFFER_SIZE)

func consume_if_present(action: StringName) -> bool:
    for i in _count:
        var idx := (_head - 1 - i + BUFFER_SIZE) % BUFFER_SIZE
        if _buffer[idx] == action:
            _buffer[idx] = &""
            _count -= 1
            return true
    return false

func clear() -> void:
    _buffer.fill(&"")
    _count = 0
    _head = 0
```

Usage in a player node:

```gdscript
var _input_buffer := InputBuffer.new()

func _process(_delta: float) -> void:
    if Input.is_action_just_pressed("attack"):
        _input_buffer.push(&"attack")

func _physics_process(_delta: float) -> void:
    if _can_attack() and _input_buffer.consume_if_present(&"attack"):
        _start_attack()
```

### Pattern 4 — Push-Down Automaton State Machine

A stack-based FSM lets states layer cleanly — e.g. a `swim` state sits on top of `walk` without breaking walk logic.

```gdscript
class_name StateMachine
extends Node

class State:
    var name: StringName = &""
    ## Called once when this state becomes active.
    func enter(_machine: StateMachine) -> void: pass
    ## Called once when this state is popped or replaced.
    func exit(_machine: StateMachine) -> void: pass
    func process(_machine: StateMachine, _delta: float) -> void: pass
    func physics_process(_machine: StateMachine, _delta: float) -> void: pass
    func handle_input(_machine: StateMachine, _event: InputEvent) -> void: pass

var _stack: Array[State] = []

func push(state: State) -> void:
    if _stack.size() > 0:
        _stack.back().exit(self)
    _stack.push_back(state)
    state.enter(self)

func pop() -> void:
    if _stack.is_empty():
        return
    _stack.back().exit(self)
    _stack.pop_back()
    if _stack.size() > 0:
        _stack.back().enter(self)

func replace(state: State) -> void:
    pop()
    push(state)

func current() -> State:
    return _stack.back() if not _stack.is_empty() else null

func _process(delta: float) -> void:
    if current():
        current().process(self, delta)

func _physics_process(delta: float) -> void:
    if current():
        current().physics_process(self, delta)

func _unhandled_input(event: InputEvent) -> void:
    if current():
        current().handle_input(self, event)
```

Concrete state example:

```gdscript
class SwimState extends StateMachine.State:
    func _init() -> void:
        name = &"swim"

    func enter(machine: StateMachine) -> void:
        # Override gravity while swimming
        machine.get_parent().gravity_scale = 0.1

    func exit(machine: StateMachine) -> void:
        machine.get_parent().gravity_scale = 1.0

    func physics_process(machine: StateMachine, delta: float) -> void:
        var body := machine.get_parent() as CharacterBody3D
        var dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
        body.velocity = Vector3(dir.x, 0.0, dir.y) * 3.0
        body.move_and_slide()
        if body.is_on_floor():
            machine.pop()  # back to walk
```

### Pattern 5 — Screen Shake via Trauma System

Uses a decaying `trauma` value (0–1) to drive randomised `Camera3D` position offset sampled from `FastNoiseLite`.

```gdscript
extends Camera3D

const MAX_OFFSET := Vector3(0.15, 0.15, 0.0)
const TRAUMA_DECAY := 2.0  # units per second

var trauma := 0.0  # 0 = no shake, 1 = maximum shake
var _noise := FastNoiseLite.new()
var _noise_y := 0.0  # walk along noise in time

func _ready() -> void:
    _noise.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
    _noise.seed = randi()

func add_trauma(amount: float) -> void:
    trauma = clampf(trauma + amount, 0.0, 1.0)

func _process(delta: float) -> void:
    trauma = maxf(trauma - TRAUMA_DECAY * delta, 0.0)
    _apply_shake(delta)

func _apply_shake(delta: float) -> void:
    _noise_y += delta * 20.0
    var shake := trauma * trauma  # square for more natural falloff
    position = Vector3(
        MAX_OFFSET.x * shake * _noise.get_noise_2d(0.0, _noise_y),
        MAX_OFFSET.y * shake * _noise.get_noise_2d(1.0, _noise_y),
        0.0
    )
```

Trigger from anywhere via:

```gdscript
var cam := get_viewport().get_camera_3d() as Camera3D
if cam and cam.has_method("add_trauma"):
    cam.add_trauma(0.4)
```

### Pattern 6 — Save Slots with ResourceSaver

Store typed `Resource` objects per slot, creating the directory structure on first save.

```gdscript
class_name SaveData
extends Resource

@export var player_position: Vector3 = Vector3.ZERO
@export var health: int = 100
@export var inventory: Array[String] = []
@export var play_time_seconds: float = 0.0
```

```gdscript
class_name SaveManager
extends Node

const SAVE_DIR := "user://saves/"
const FILE_EXT := ".tres"

static func slot_path(slot: int) -> String:
    return SAVE_DIR + "slot_%02d" % slot + FILE_EXT

static func save(slot: int, data: SaveData) -> Error:
    var dir := SAVE_DIR
    if not DirAccess.dir_exists_absolute(dir):
        var err := DirAccess.make_dir_recursive_absolute(dir)
        if err != OK:
            push_error("SaveManager: could not create save dir: %s" % error_string(err))
            return err
    return ResourceSaver.save(data, slot_path(slot))

static func load_slot(slot: int) -> SaveData:
    var path := slot_path(slot)
    if not ResourceLoader.exists(path):
        return null
    return ResourceLoader.load(path) as SaveData

static func delete_slot(slot: int) -> void:
    var path := slot_path(slot)
    if ResourceLoader.exists(path):
        DirAccess.remove_absolute(path)

static func list_slots() -> Array[int]:
    var result: Array[int] = []
    var dir := DirAccess.open(SAVE_DIR)
    if dir == null:
        return result
    dir.list_dir_begin()
    var file := dir.get_next()
    while file != "":
        if file.ends_with(FILE_EXT):
            var slot := file.get_basename().split("_")[1].to_int()
            result.append(slot)
        file = dir.get_next()
    return result
```

## Common Pitfalls

- **Forgetting `delta` in `_physics_process`.** Velocity applied without `* delta` is frame-rate dependent and will behave differently at 30 fps vs 144 fps. Always write `velocity.y -= GRAVITY * delta`.

- **Reading input in `_physics_process` for discrete events.** `Input.is_action_just_pressed()` returns `true` for only one frame. If the physics tick and the process tick are decoupled (which Godot allows), the event can be missed. Poll discrete inputs in `_process` and store them in a flag or buffer that `_physics_process` then consumes.

- **Treating `process_mode` as an afterthought.** Nodes default to `PAUSABLE`. If `get_tree().paused = true` is set, UI input nodes must be `WHEN_PAUSED` or they will not receive events. Global audio or analytics nodes should be `ALWAYS`. Set `process_mode` explicitly on every node that has non-default pause behaviour.

- **Using plain `Dictionary` for save files.** `FileAccess.store_var()` with a raw `Dictionary` works but loses type information and breaks when property names change. Use a typed `Resource` subclass with `ResourceSaver` so Godot handles versioning and type coercion automatically.

- **`create_timer()` timers silently stopping on pause.** `SceneTree.create_timer()` respects `pause_mode_process` by default. Pass `true` as the second argument (`process_always`) if the timer must continue while the game is paused (e.g. a UI countdown).

- **Ignoring `up_direction` and `floor_snap_length` for slope traversal.** Without `floor_snap_length > 0`, `CharacterBody3D` loses floor contact on the downward side of slopes and triggers spurious jumps. Without a correct `up_direction`, ramps at steep angles are mis-classified as walls.

## Performance

**Input polling cost** is negligible — `Input.is_action_pressed()` is an O(1) hash lookup. Use `_process` for input and reserve `_physics_process` for physics mutations only. Avoid calling `Input.get_action_strength()` inside deeply nested loops each frame.

**State machine cost.** Flat `enum` + `match` state machines have near-zero overhead. Push-down automaton stacks with virtual-dispatch `State` objects add a small allocation cost per push/pop but are negligible for player-count entities (< 10). For hundreds of NPCs, prefer flat FSMs or HFSM encoded in a `Dictionary`.

**Save file tips.**
- Write saves asynchronously using threads (`Thread`) or Godot 4's `WorkerThreadPool` to avoid frame hitches on large `Resource` graphs.
- Keep `SaveData` resources shallow; avoid embedding large `Texture2D` or `Mesh` references — store resource paths (`String`) instead and reload on demand.
- Compress with `ResourceSaver.FLAG_COMPRESS` when save data is large or persisted to a network location.

## Anti-Patterns

**Frame-rate-dependent velocity (wrong):**

```gdscript
# Wrong — velocity applied without delta
func _physics_process(_delta: float) -> void:
    velocity.y -= 20.0
    move_and_slide()
```

**Delta-time normalised velocity (right):**

```gdscript
func _physics_process(delta: float) -> void:
    velocity.y -= 20.0 * delta
    move_and_slide()
```

---

**Raw Dictionary save (wrong):**

```gdscript
# Wrong — untyped, fragile across refactors
var data := {"hp": 100, "pos": player.position}
var f := FileAccess.open("user://save.dat", FileAccess.WRITE)
f.store_var(data)
```

**Typed Resource save (right):**

```gdscript
var data := SaveData.new()
data.health = 100
data.player_position = player.position
ResourceSaver.save(data, "user://saves/slot_01.tres")
```

---

**Hardcoded digital-only input (wrong):**

```gdscript
# Wrong — ignores analog controller sticks
var moving_right := Input.is_action_pressed("move_right")
velocity.x = 6.0 if moving_right else 0.0
```

**Analog-aware input (right):**

```gdscript
# Correct — works for both keyboard (returns 0/1) and analog stick (returns 0.0–1.0)
var strength := Input.get_action_strength("move_right")
velocity.x = strength * 6.0
```

## References

- CharacterBody3D — https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html
- Input singleton — https://docs.godotengine.org/en/stable/classes/class_input.html
- InputMap — https://docs.godotengine.org/en/stable/classes/class_inputmap.html
- SceneTree — https://docs.godotengine.org/en/stable/classes/class_scenetree.html
- ResourceSaver — https://docs.godotengine.org/en/stable/classes/class_resourcesaver.html
- ResourceLoader — https://docs.godotengine.org/en/stable/classes/class_resourceloader.html
- DirAccess — https://docs.godotengine.org/en/stable/classes/class_diraccess.html
- FastNoiseLite — https://docs.godotengine.org/en/stable/classes/class_fastnoiselite.html
- Camera3D — https://docs.godotengine.org/en/stable/classes/class_camera3d.html
- Node.process_mode — https://docs.godotengine.org/en/stable/classes/class_node.html#enum-node-processmode
- Using CharacterBody3D (tutorial) — https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html
- Saving games (tutorial) — https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html

## Delegate to

| Task | Skill |
|---|---|
| Writing GDScript | `godot:coder` |
| Signal design | `godot:signals` |
| Physics movement | `godot:physics` |
| API lookup | `godot:docs` |
