---
name: godot
description: "Build Godot 4 scenes and GDScript workflows, inspect physics behavior, and configure headless project exports."
category: game-engines
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["godot", "godot4", "gdscript", "gamedev", "scenetree", "characterbody", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Godot Engine 4.x Game Development AI Skill Guide (Claude)

## Overview & Engine Architecture
Godot Engine 4.x is a lightweight, open-source 2D and 3D game engine featuring a unified **SceneTree Node Architecture**, **GDScript 2.0** (with static typing, first-class functions, and lambdas), C# (.NET 8) support, and multi-backend rendering (**Forward+ Vulkan, Mobile Vulkan, and Compatibility OpenGL 3.3/WebGL2**). Claude operates as a Principal Game Developer and Engine Architect, specializing in **GDScript 2.0 statically typed systems**, **signal-driven decoupled communication**, **PhysicsServer optimization (`move_and_slide`)**, and **headless CLI CI/CD export automation**.

### Godot 4.x Core Engine & Node Hierarchy Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Godot 4.x Engine Architecture               │
│                                                             │
│  SceneTree & Node Hierarchy (Data Model)                    │
│  ├── Root Viewport $\rightarrow$ Current Scene Tree Branch  │
│  ├── Node2D / Control (CanvasItem, Anchor Positioning)      │
│  └── Node3D (Transform3D, VisualInstance3D, CollisionObject3D)│
│                                                             │
│  Execution & Scripting Layer                                │
│  ├── GDScript 2.0 Static VM / C# .NET 8 CLR Interop         │
│  ├── Signal Event Bus (Observer Pattern, Typed Callables)   │
│  └── AnimationPlayer & AnimationTree (State Machine Blends) │
│                                                             │
│  Servers & Low-Level Subsystems                             │
│  ├── RenderingServer (Forward+ Clustered Vulkan / OpenGL)   │
│  ├── PhysicsServer2D / PhysicsServer3D (Direct Nodal Stepper│
│  └── AudioServer (Dynamic Audio Buses & DSP Effects)        │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Statically Typed GDScript 2.0 Development**: Author clean, type-safe GDScript (`@export`, `@onready`, `Vector3`, `Callable`, `Array[T]`) enforcing strict static typing for maximum compiler optimization and zero runtime nil exceptions.
2. **Physics & Character Controller Tuning**: Implement robust 2D/3D kinematic movement using `CharacterBody2D` / `CharacterBody3D`, incorporating coyote time, jump buffering, wall sliding, and delta-independent smoothing.
3. **Signal Event Bus Architecture**: Build decoupled game communication architectures using global Autoload Singletons without tight spatial node coupling (`get_parent().get_parent()`).
4. **Headless CI/CD Export Pipelines**: Script automated build matrix pipelines via `godot --headless --export-release` for Windows, Linux, macOS, and Web (HTML5).

---

## Production GDScript 2.0 Code: Advanced 3D Character Controller with State Machine

Save this script as `res://scripts/player/player_controller.gd`:

```gdscript
# ==============================================================================
# Godot 4.x GDScript 2.0: Statically Typed 3D Character Controller
# Features: Coyote Time, Jump Buffering, Slope Snapping, and Signal Dispatch
# ==============================================================================
class_name PlayerController
extends CharacterBody3D

signal health_changed(new_health: int)
signal player_died

@export_group("Movement Parameters")
@export var speed: float = 6.5
@export var acceleration: float = 40.0
@export var friction: float = 35.0
@export var jump_velocity: float = 5.2
@export var mouse_sensitivity: float = 0.003

@export_group("Gameplay Stats")
@export var max_health: int = 100
var current_health: int = 100

@onready var camera_pivot: Node3D = $CameraPivot
@onready var camera: Camera3D = $CameraPivot/Camera3D

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var coyote_timer: float = 0.0
var jump_buffer_timer: float = 0.0
const COYOTE_DURATION: float = 0.15
const JUMP_BUFFER_DURATION: float = 0.12

func _ready() -> void:
	current_health = max_health
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * mouse_sensitivity)
		camera_pivot.rotate_x(-event.relative.y * mouse_sensitivity)
		camera_pivot.rotation.x = clamp(camera_pivot.rotation.x, deg_to_rad(-80), deg_to_rad(80))

func _physics_process(delta: float) -> void:
	# 1. Update Coyote & Jump Buffer Timers
	if is_on_floor():
		coyote_timer = COYOTE_DURATION
	else:
		coyote_timer = max(0.0, coyote_timer - delta)
		velocity.y -= gravity * delta

	if Input.is_action_just_pressed("jump"):
		jump_buffer_timer = JUMP_BUFFER_DURATION
	else:
		jump_buffer_timer = max(0.0, jump_buffer_timer - delta)

	# 2. Execute Jump if buffered and within coyote window
	if jump_buffer_timer > 0.0 and coyote_timer > 0.0:
		velocity.y = jump_velocity
		jump_buffer_timer = 0.0
		coyote_timer = 0.0

	# 3. Horizontal Movement Calculation
	var input_dir: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction: Vector3 = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	if direction.length_squared() > 0.0:
		velocity.x = move_toward(velocity.x, direction.x * speed, acceleration * delta)
		velocity.z = move_toward(velocity.z, direction.z * speed, acceleration * delta)
	else:
		velocity.x = move_toward(velocity.x, 0.0, friction * delta)
		velocity.z = move_toward(velocity.z, 0.0, friction * delta)

	# 4. Execute Physics Step with Slope Snapping
	floor_snap_length = 0.3 if is_on_floor() else 0.0
	move_and_slide()

func take_damage(amount: int) -> void:
	current_health = max(0, current_health - amount)
	health_changed.emit(current_health)
	if current_health <= 0:
		player_died.emit()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Exported HTML5 Web Build Shows Blank Screen** | Web server hosting the build is missing Cross-Origin Isolation headers (`SharedArrayBuffer` requires COOP/COEP). | 1. Configure web server headers: `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`.<br>2. In *Export Presets $\rightarrow$ Web*, switch Threading to **Single-threaded** if host cannot send headers. |
| **Physics Jitter / Camera Stutter During Movement** | Camera position updated in `_process(delta)` while character body moves in `_physics_process(delta)` without interpolation. | 1. Move camera update logic to `_physics_process(delta)`.<br>2. In *Project Settings $\rightarrow$ Physics $\rightarrow$ Common*, enable **Physics Interpolation**. |
| **Cyclic Dependency Error: `class_name` cycle** | Script A references Script B as a static type while Script B references Script A, breaking the compilation DAG. | 1. Decouple using abstract base interfaces or duck typing.<br>2. Pass untyped `Node` parameters or use string signals (`call_deferred`). |
| **Vulkan Renderer Crash on Older GPUs** | Target GPU lacks Vulkan 1.2 physical device support for Forward+ clustered shading. | In *Project Settings $\rightarrow$ Rendering $\rightarrow$ Renderer*, switch **Rendering Method** to `gl_compatibility` (OpenGL 3.3 / WebGL2). |

---

## Command Line Syntax & CI/CD Recipes

```bash
# 1. Headless Export for Windows Release Package
godot --headless --export-release "Windows Desktop" "C:\Builds\Game_Win64.exe"

# 2. Run Automated GUT (Godot Unit Test) Suite Headless
godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://test/unit -gexit

# 3. Launch Dedicated Multiplayer Server Headless on Port 7777
godot --headless -- --server --port=7777
```

### Essential File Locations
- **Project Settings**: `<ProjectRoot>/project.godot`
- **Export Presets**: `<ProjectRoot>/export_presets.cfg`
- **Global Editor Config**: `%APPDATA%\Godot\editor_settings-4.tres` (Windows) or `~/.config/godot/` (Linux)

---

## Agent Operational Directive
> **MANDATORY**: Always write GDScript 2.0 with strict static type annotations (`var x: float = 1.0`). Use `_physics_process` for all character movement and enable physics interpolation to prevent display stutter.
