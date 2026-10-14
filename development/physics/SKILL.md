---
name: physics
description: Godot physics developer — use when working with collision layers, joints, raycasts, physics bodies, or PhysicsServer3D.
type: implementation
---

# Godot Physics

> Implement, tune, and debug Godot 4.x physics systems — rigid bodies, collision layers, queries, joints, and low-level PhysicsServer3D APIs.

## Overview

Godot 4.x uses the Godot Physics engine (with optional Jolt as an alternative). Physics runs on a fixed timestep controlled by `physics_ticks_per_second` (default 60 Hz). All physics logic belongs in `_physics_process(delta)`. The physics world is divided into spaces; each space has a `PhysicsDirectSpaceState3D` for queries.

Key design rules:
- Never modify physics state from `_process` — always use `_physics_process` or `_integrate_forces`
- Document every collision layer assignment in a single autoload constant file
- Prefer shape casts and ray queries over continuous overlap checks

## Key Nodes & APIs

| Node / Class | Purpose | Notes |
|---|---|---|
| `StaticBody3D` | Immovable world geometry | Zero cost at runtime when sleeping |
| `RigidBody3D` | Fully simulated body | Use `_integrate_forces` for custom forces; set `continuous_cd = true` for fast objects |
| `CharacterBody3D` | Kinematic character | Use `move_and_slide()` with `up_direction` set |
| `AnimatableBody3D` | Kinematic body that pushes rigids | Useful for moving platforms |
| `Area3D` | Overlap / trigger volume | Also overrides gravity and damping per-region |
| `RayCast3D` | Single ray probe | Call `force_raycast_update()` outside physics process |
| `ShapeCast3D` | Shape-swept query | Preferred over ray for thick objects |
| `CollisionShape3D` | Attaches a shape resource to a body | Shape is shared — clone before mutating |
| `HingeJoint3D` | Single-axis rotation joint | Good for doors, wheels |
| `Generic6DOFJoint3D` | Full 6-axis constraint | Use for complex mechanical linkages |
| `PinJoint3D` | Ball-socket point connection | Ragdoll connections |
| `SoftBody3D` | Deformable mesh simulation | Set `simulation_precision`; pin vertices with `pin_point()` |
| `PhysicsServer3D` | Low-level direct physics API | `body_create()`, `body_set_state()` — bypasses scene tree overhead |
| `PhysicsDirectBodyState3D` | Passed into `_integrate_forces` | Read contacts, apply forces, override transform safely |
| `PhysicsDirectSpaceState3D` | Space query interface | `intersect_ray()`, `intersect_shape()`, `cast_motion()` |

## Collision Layer Convention

Assign layers in a central autoload (e.g. `Layers.gd`) and never use raw integers in scene files.

| Layer | Bit | Name | Collides With (Mask) |
|---|---|---|---|
| 1 | `1 << 0` | World | Player, Enemy, Projectile, Debris |
| 2 | `1 << 1` | Player | World, Enemy, Trigger, Projectile |
| 3 | `1 << 2` | Enemy | World, Player, Projectile, Trigger |
| 4 | `1 << 3` | Projectile | World, Enemy, Player |
| 5 | `1 << 4` | Trigger | Player, Enemy |
| 6 | `1 << 5` | Debris | World only |
| 7 | `1 << 6` | Ragdoll | World, Debris |
| 8 | `1 << 7` | Reserved | — |

**Mask matrix rule:** Layer N's mask lists what it should _detect_. Triggers (Layer 5) only detect Player and Enemy — they never need to know about projectiles or debris.

```gdscript
# autoload: Layers.gd
class_name Layers

const WORLD      := 1 << 0
const PLAYER     := 1 << 1
const ENEMY      := 1 << 2
const PROJECTILE := 1 << 3
const TRIGGER    := 1 << 4
const DEBRIS     := 1 << 5
const RAGDOLL    := 1 << 6
```

Apply in code:

```gdscript
$ProjectileBody.collision_layer = Layers.PROJECTILE
$ProjectileBody.collision_mask  = Layers.WORLD | Layers.ENEMY | Layers.PLAYER
```

## Core Patterns

### Pattern 1 — Custom Force Integration with Contact Reading

```gdscript
extends RigidBody3D

func _ready() -> void:
    contact_monitor = true
    max_contacts_reported = 4

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
    # Apply a horizontal wind force
    var wind := Vector3(10.0, 0.0, 0.0)
    state.apply_central_force(wind)

    # Read contact normals this frame
    for i in state.get_contact_count():
        var normal: Vector3 = state.get_contact_local_normal(i)
        var impulse: float  = state.get_contact_impulse(i).length()
        if impulse > 50.0:
            _on_heavy_impact(normal, impulse)

    # Safe transform override (never set transform directly on a RigidBody3D)
    if _needs_teleport:
        state.transform = _target_xform
        state.linear_velocity  = Vector3.ZERO
        state.angular_velocity = Vector3.ZERO
        _needs_teleport = false

var _needs_teleport := false
var _target_xform   := Transform3D()

func teleport_to(xform: Transform3D) -> void:
    _target_xform = xform
    _needs_teleport = true

func _on_heavy_impact(normal: Vector3, impulse: float) -> void:
    pass  # spawn particles, play audio, etc.
```

### Pattern 2 — Swept Shape Query (No Tunneling)

```gdscript
extends Node3D

func can_move(body: CollisionObject3D, motion: Vector3) -> bool:
    var space := body.get_world_3d().direct_space_state
    var params := PhysicsShapeQueryParameters3D.new()
    params.shape      = body.shape_owner_get_shape(0, 0)
    params.transform  = body.global_transform
    params.motion     = motion
    params.collision_mask = body.collision_mask
    params.exclude    = [body.get_rid()]

    # cast_motion returns [safe_fraction, unsafe_fraction]
    var result: Array = space.cast_motion(params)
    # result[0] == 1.0 means fully clear
    return result[0] >= 1.0

func move_safely(body: CharacterBody3D, desired: Vector3) -> void:
    if can_move(body, desired):
        body.global_position += desired
    else:
        body.move_and_slide()
```

### Pattern 3 — PhysicsServer3D Bulk Spawning

Use the direct API to create thousands of physics objects without instantiating nodes.

```gdscript
extends Node3D

var _bodies: Array[RID] = []
var _scenario: RID

func _ready() -> void:
    _scenario = get_world_3d().space

func spawn_debris(count: int, origin: Vector3) -> void:
    var sphere := SphereShape3D.new()
    sphere.radius = 0.15
    var shape_rid := PhysicsServer3D.shape_create(PhysicsServer3D.SHAPE_SPHERE)
    PhysicsServer3D.shape_set_data(shape_rid, sphere.radius)

    for i in count:
        var body := PhysicsServer3D.body_create()
        PhysicsServer3D.body_set_mode(body, PhysicsServer3D.BODY_MODE_RIGID)
        PhysicsServer3D.body_set_space(body, _scenario)
        PhysicsServer3D.body_add_shape(body, shape_rid)

        var xform := Transform3D(Basis(), origin + Vector3(
            randf_range(-2.0, 2.0),
            randf_range(0.0, 3.0),
            randf_range(-2.0, 2.0)
        ))
        PhysicsServer3D.body_set_state(
            body,
            PhysicsServer3D.BODY_STATE_TRANSFORM,
            xform
        )
        PhysicsServer3D.body_set_param(
            body,
            PhysicsServer3D.BODY_PARAM_MASS,
            0.5
        )
        _bodies.append(body)

func _exit_tree() -> void:
    for body in _bodies:
        PhysicsServer3D.free_rid(body)
    _bodies.clear()
```

### Pattern 4 — Continuous Collision Detection (CCD) for Fast Projectiles

```gdscript
extends RigidBody3D

@export var speed: float = 120.0  # m/s — fast enough to tunnel without CCD

func _ready() -> void:
    # Enable CCD — required when object moves more than its own size per frame.
    # Rule of thumb: enable when speed > (shape_diameter / physics_delta).
    continuous_cd = true

    collision_layer = Layers.PROJECTILE
    collision_mask  = Layers.WORLD | Layers.ENEMY | Layers.PLAYER

    body_entered.connect(_on_hit)
    linear_velocity = -global_basis.z * speed

func _on_hit(body: Node) -> void:
    # Handle impact
    queue_free()
```

### Pattern 5 — Sleep Management

```gdscript
extends RigidBody3D

func _ready() -> void:
    can_sleep = true  # default true; set false only for always-active bodies

func wake_up_nearby(radius: float) -> void:
    # Wake all sleeping rigid bodies within radius
    var space := get_world_3d().direct_space_state
    var params := PhysicsShapeQueryParameters3D.new()
    var sphere := SphereShape3D.new()
    sphere.radius = radius
    params.shape = sphere
    params.transform = global_transform
    params.collision_mask = Layers.DEBRIS | Layers.RAGDOLL

    var hits := space.intersect_shape(params, 32)
    for hit in hits:
        var rb := hit.collider as RigidBody3D
        if rb and rb.sleeping:
            rb.sleeping = false  # force wake; also triggers "sleeping_state_changed"
```

### Pattern 6 — SoftBody3D Cloth Setup

```gdscript
extends SoftBody3D

@export var pinned_vertex_indices: Array[int] = [0, 1, 2, 3]

func _ready() -> void:
    simulation_precision = 5      # higher = more accurate, more CPU
    damping_coefficient  = 0.01
    drag_coefficient     = 0.0

    # Pin top-edge vertices so the cloth hangs
    for idx in pinned_vertex_indices:
        pin_point(idx, true)

    collision_layer = Layers.DEBRIS
    collision_mask  = Layers.WORLD
```

## Common Pitfalls

- **Tunneling on fast objects.** A RigidBody3D moving faster than its own diameter per physics tick will pass through thin geometry. Always set `continuous_cd = true` on bullets, arrows, and high-velocity projectiles.
- **Mutating a shared shape resource.** `CollisionShape3D.shape` is a resource that can be shared across instances. Calling `shape.radius = x` changes every body using that resource. Call `shape = shape.duplicate()` before mutating.
- **Setting `transform` directly on a RigidBody3D.** Writing `rigid_body.global_position = x` outside of `_integrate_forces` is unreliable — the physics engine overwrites it next tick. Use `_integrate_forces(state)` and write to `state.transform` instead, or call `reset_physics_interpolation()` after a teleport.
- **Using `TrimeshShape3D` on dynamic bodies.** Concave mesh shapes are only valid on `StaticBody3D` and `AnimatableBody3D`. Attaching a `TrimeshShape3D` to a `RigidBody3D` either silently fails or causes undefined collision behavior. Use `ConvexPolygonShape3D` (convex hull) for dynamic bodies.
- **Physics queries outside `_physics_process`.** `PhysicsDirectSpaceState3D` queries called from `_process` read stale state and produce one-frame-old results. Always query from `_physics_process` or deferred calls that run within the physics step.
- **Forgetting to free PhysicsServer3D RIDs.** RIDs created with `body_create()`, `shape_create()`, etc. are not garbage collected. Store them and call `PhysicsServer3D.free_rid()` in `_exit_tree()`.
- **`Area3D` overlap signals firing for bodies that share no mask bits.** Godot fires `body_entered` only when _both_ the area's mask includes the body's layer _and_ the body's mask includes the area's layer. One-sided mask setup causes silent missed overlaps.

## Performance

### Sleeping Bodies

`RigidBody3D.can_sleep = true` (default) lets the engine suspend simulation for bodies at rest. A sleeping body costs near zero CPU. Design levels so debris and ragdolls can settle and sleep. Avoid calling `apply_impulse` on a timer — it continuously wakes bodies.

```gdscript
# Check sleep state
if rigid_body.sleeping:
    pass  # no simulation cost this tick

# Connect to state change
rigid_body.sleeping_state_changed.connect(func(): print("sleep toggled"))
```

### PhysicsServer3D Direct API

Node-based bodies carry scene tree, signal, and scripting overhead. When spawning more than ~200 physics objects (particles, crowds, projectile pools), bypass nodes entirely with `PhysicsServer3D`. This eliminates `_ready`, `_physics_process`, and node parent traversal costs. See Pattern 3 above.

### Shape Complexity Budget

| Shape | Cost | Use Case |
|---|---|---|
| `SphereShape3D` | Lowest | Projectiles, rolling objects |
| `BoxShape3D` | Low | Crates, walls, platforms |
| `CapsuleShape3D` | Low | Characters, cylinders |
| `CylinderShape3D` | Low-Medium | Barrels, columns |
| `ConvexPolygonShape3D` | Medium | Irregular dynamic bodies — preferred over concave |
| `ConcavePolygonShape3D` | High (static only) | Complex static world geometry |
| `TrimeshShape3D` | High (static only) | Exact mesh collision — static bodies only |
| `HeightMapShape3D` | Low-Medium | Terrain — highly optimized |

Rules:
- Dynamic bodies (`RigidBody3D`, `CharacterBody3D`): use convex shapes only
- Static world geometry: `ConcavePolygonShape3D` or `TrimeshShape3D` are acceptable
- Prefer compound convex shapes over one complex concave shape
- Reduce vertex count on convex hulls — Godot's importer has a "Simplification" slider

## Anti-Patterns

| Wrong | Right |
|---|---|
| `rigid_body.global_position = target` | Set `state.transform` inside `_integrate_forces` |
| `TrimeshShape3D` on `RigidBody3D` | `ConvexPolygonShape3D` on dynamic bodies |
| Raw integers: `collision_layer = 4` | Named constants: `collision_layer = Layers.ENEMY` |
| Physics query in `_process` | Physics query in `_physics_process` |
| Spawning 500 `RigidBody3D` nodes | Use `PhysicsServer3D.body_create()` directly |
| `continuous_cd = false` on a fast bullet | `continuous_cd = true` whenever speed > shape diameter / delta |
| Mutating `shape.radius` in place | `shape = shape.duplicate(); shape.radius = x` |
| `SoftBody3D.simulation_precision = 1` for cloth | Use 4–8 for believable cloth; 1 causes visible instability |

## References

- [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html)
- [RigidBody3D](https://docs.godotengine.org/en/stable/classes/class_rigidbody3d.html)
- [PhysicsDirectBodyState3D](https://docs.godotengine.org/en/stable/classes/class_physicsdirectbodystate3d.html)
- [PhysicsServer3D](https://docs.godotengine.org/en/stable/classes/class_physicsserver3d.html)
- [PhysicsDirectSpaceState3D](https://docs.godotengine.org/en/stable/classes/class_physicsdirectspacestate3d.html)
- [Collision layers and masks](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html#collision-layers-and-masks)
- [SoftBody3D](https://docs.godotengine.org/en/stable/classes/class_softbody3d.html)
- [Using CharacterBody3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html)
- [Ray-casting](https://docs.godotengine.org/en/stable/tutorials/physics/ray-casting.html)

## Delegate to

| Task | Skill |
|---|---|
| GDScript implementation | `godot:coder` |
| Joint and body scene setup | `godot:scene` |
| API lookup | `godot:docs` |
