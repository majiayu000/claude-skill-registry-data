---
name: animation
description: Godot animation developer — use when working with AnimationPlayer, AnimationTree, blend spaces, state machines, or skeletal IK.
type: implementation
---

# Godot Animation

> Expert Godot 4.x animation programmer specializing in AnimationPlayer, AnimationTree state machines, root motion, skeletal IK, and procedural overrides.

## Overview

Godot's animation stack is layered: `AnimationPlayer` drives keyframe tracks; `AnimationTree` blends and routes between clips using blend spaces, state machines, and blend trees; `Skeleton3D` and `SkeletonIK3D` handle bone transforms and IK. In Godot 4.3+, `AnimationMixer` is the unified base class for both `AnimationPlayer` and `AnimationTree`, exposing shared playback and callback APIs. Always drive characters through `AnimationTree` — use `AnimationPlayer` only as a clip library.

## Key Nodes & APIs

| Node / Class | Purpose | Key Methods / Properties |
|---|---|---|
| `AnimationPlayer` | Keyframe clip library and standalone playback | `play()`, `queue()`, `stop()`, `animation_finished`, `CallbackTrack` |
| `AnimationTree` | Blend graph controller; references an `AnimationPlayer` | `active`, `advance_expression_base_node`, `get_root_motion_position()` |
| `AnimationMixer` | Base class for `AnimationPlayer` and `AnimationTree` (4.3+) | `animation_list`, `get_animation()`, `AnimationMixerPlaybackUpdated` |
| `AnimationNodeStateMachine` | State machine node inside an `AnimationTree` | `travel()`, `get_current_node()`, `is_playing()` |
| `AnimationNodeStateMachinePlayback` | Runtime playback handle retrieved via `tree["parameters/playback"]` | `travel()`, `start()`, `stop()`, `get_current_node()` |
| `AnimationNodeBlendSpace1D` | 1-D blend space for speed-based locomotion | Add points with `add_blend_point()` |
| `AnimationNodeBlendSpace2D` | 2-D blend space for directional locomotion | `set_blend_position()` via tree parameters |
| `Skeleton3D` | Bone hierarchy; target for IK and procedural overrides | `set_bone_global_pose_override()`, `find_bone()` |
| `SkeletonIK3D` | FABRIK IK solver attached to `Skeleton3D` | `start()`, `stop()`, `target` property |
| `BoneAttachment3D` | Attaches a node (weapon, prop) to a specific bone | `bone_name`, `override_pose` |
| `MeshInstance3D` | Renderable mesh; exposes blend shapes as property tracks | `set_blend_shape_value()`, `get_blend_shape_value()` |

## Core Patterns

### Pattern 1 — State Machine Travel

Retrieve the `AnimationNodeStateMachinePlayback` resource at runtime and call `travel()` to transition to a named state. `AnimationTree.active` must be `true` first.

```gdscript
# character.gd
@onready var tree: AnimationTree = $AnimationTree
@onready var playback: AnimationNodeStateMachinePlayback = tree["parameters/playback"]

func _ready() -> void:
    tree.active = true

func jump() -> void:
    playback.travel("Jump")

func land() -> void:
    playback.travel("Idle")

func _physics_process(delta: float) -> void:
    # Feed blend space parameter each frame
    tree["parameters/LocomotionBlend/blend_position"] = velocity.length()
```

### Pattern 2 — Root Motion on CharacterBody3D

Enable root motion in the `AnimationTree` inspector (`root_motion_track` set to the hips bone path). Each frame, extract the delta position and apply it to `velocity` so the physics engine handles collisions.

```gdscript
# root_motion_character.gd
@onready var tree: AnimationTree = $AnimationTree
@onready var body: CharacterBody3D = self

func _ready() -> void:
    tree.active = true

func _physics_process(delta: float) -> void:
    # Root motion gives world-space displacement for this frame
    var root_motion: Vector3 = tree.get_root_motion_position()
    var motion: Vector3 = global_transform.basis * root_motion

    velocity = motion / delta  # Convert displacement to velocity
    move_and_slide()
```

### Pattern 3 — Procedural Look-At Bone Override

After the animation pose is computed, override a specific bone's global pose to make a character look at a target. Set `weight` to blend smoothly between animated and procedural.

```gdscript
# look_at_head.gd
@onready var skeleton: Skeleton3D = $Armature/Skeleton3D
var head_bone_idx: int = -1
var look_target: Node3D

func _ready() -> void:
    head_bone_idx = skeleton.find_bone("Head")

func _process(_delta: float) -> void:
    if head_bone_idx == -1 or look_target == null:
        return

    var bone_origin: Vector3 = skeleton.get_bone_global_pose(head_bone_idx).origin
    var look_dir: Vector3 = (look_target.global_position - bone_origin).normalized()

    var look_transform := Transform3D(
        Basis.looking_at(look_dir, Vector3.UP),
        bone_origin
    )

    # weight 1.0 = fully procedural; true = persistent override
    skeleton.set_bone_global_pose_override(head_bone_idx, look_transform, 1.0, true)

func stop_look_at() -> void:
    skeleton.clear_bones_global_pose_override()
```

### Pattern 4 — Await Animation Finished

Use `await animation_player.animation_finished` to sequence actions after a clip ends. Never use `Timer` nodes as a workaround — they drift from actual animation length.

```gdscript
# combo_attack.gd
@onready var anim: AnimationPlayer = $AnimationPlayer

func execute_combo() -> void:
    anim.play("Attack1")
    await anim.animation_finished

    anim.play("Attack2")
    await anim.animation_finished

    anim.play("AttackFinisher")
    await anim.animation_finished

    anim.play("Idle")
```

### Pattern 5 — CallbackTrack for Keyframe Events

Add a `CallbackTrack` inside an animation to call a method at a specific keyframe time. The method must exist on the node set as the animation player's owner or any node reachable from it.

```gdscript
# footstep_handler.gd — method called from CallbackTrack keyframe
extends CharacterBody3D

func _ready() -> void:
    # CallbackTrack in AnimationPlayer calls "play_footstep" at keyframe time
    pass

func play_footstep() -> void:
    $FootstepAudio.play()
```

In the editor: open the animation, add a **Method Track**, set the node path to this node, and insert a key at the desired time with method name `play_footstep`.

### Pattern 6 — Blend Shape Animation

Animate blend shapes by creating a **Property Track** targeting the path `MeshInstance3D:blend_shapes/shape_name`. You can also drive them from code.

```gdscript
# facial_expression.gd
@onready var face_mesh: MeshInstance3D = $Armature/FaceMesh

func set_smile(weight: float) -> void:
    # weight is 0.0–1.0
    face_mesh.set_blend_shape_value(
        face_mesh.find_blend_shape_by_name("mouth_smile"),
        weight
    )

func _ready() -> void:
    # AnimationPlayer property track path for the editor:
    # Node path:  Armature/FaceMesh
    # Property:   blend_shapes/mouth_smile
    pass
```

### Pattern 7 — BoneAttachment3D for Weapon/Prop

Attach a weapon or prop to a skeleton bone without manual transform math. `BoneAttachment3D` keeps itself parented to the bone every frame.

```gdscript
# weapon_equip.gd
@onready var attachment: BoneAttachment3D = $Armature/Skeleton3D/RightHandAttachment
@onready var weapon_scene: PackedScene = preload("res://weapons/sword.tscn")

func equip_weapon() -> void:
    # BoneAttachment3D.bone_name is set in the inspector to "RightHand"
    var weapon: Node3D = weapon_scene.instantiate()
    attachment.add_child(weapon)
    weapon.position = Vector3.ZERO  # local offset relative to bone
```

## Common Pitfalls

- **`AnimationTree.active` is false.** Calling `playback.travel()` silently does nothing if `active` is not `true`. Set it in `_ready()` and assert it in debug builds.
- **`advance_expression_base_node` not set.** When an `AnimationTree` uses expression conditions in transitions (e.g., `speed > 0.5`), Godot evaluates them on the node at `advance_expression_base_node`. If left empty or pointing to the wrong node, all expression conditions fail and no transition ever fires. Set it to the character root node.
- **Root motion and `move_and_slide()` fighting.** If you apply root motion via `velocity = motion / delta` but also set `velocity` elsewhere in the same frame (e.g., gravity), gravity wins or they cancel. Keep a clear single site that owns `velocity.y` separately from `velocity.xz`.
- **Using `Timer` instead of `await animation_finished`.** Timers drift if animation speed changes or the clip is interrupted. Always use `await animation_player.animation_finished` for sequencing.
- **Driving a bone override before the skeleton pose is computed.** `set_bone_global_pose_override` must be called after `_process` animates the skeleton, or it gets overwritten. Use `_process` with `NOTIFICATION_TRANSFORM_CHANGED` or call it in a deferred manner after `AnimationTree` updates.
- **Forgetting to call `skeleton.clear_bones_global_pose_override()`.** Overrides persist until explicitly cleared. If a look-at or IK system is disabled, clear the override or the bone stays locked in the last procedural pose.
- **Blend shape property track path mismatch.** The property track path must exactly match `blend_shapes/shape_name` on the `MeshInstance3D`. A renamed shape or wrong node path produces no error but animates nothing.

## Performance

| Concern | Guidance |
|---|---|
| **Animation update mode** | Use `AnimationPlayer.playback_process_mode = ANIMATION_PROCESS_PHYSICS` for characters that call `move_and_slide()`; use `ANIMATION_PROCESS_IDLE` for UI and non-physics objects to avoid redundant updates. |
| **Bone count** | Keep character skeletons under 60 bones for mobile. Desktop is comfortable at 150+. High bone counts multiply the cost of every `set_bone_global_pose_override()` call. |
| **IK solver cost** | `SkeletonIK3D` runs FABRIK iteratively each physics frame. Limit `max_iterations` (default 10) and restrict it to characters in camera range. Disable `start()` when off-screen. |
| **`AnimationTree` graph complexity** | Deep nested blend trees with many `AnimationNodeBlendTree` layers add per-frame blend cost. Flatten where possible; merge infrequently toggled branches with `AnimationNodeOneShot`. |
| **Root motion read** | `get_root_motion_position()` is cheap (a single `Vector3` read). Do not cache it across frames — it accumulates delta and resets each call. |

## Anti-Patterns

| Wrong | Right |
|---|---|
| `await get_tree().create_timer(anim.current_animation_length).timeout` | `await anim.animation_finished` |
| Set `velocity` from both root motion and a separate movement script | Own `velocity.xz` exclusively through root motion; add `velocity.y` (gravity) separately |
| Leave `advance_expression_base_node` empty | Assign it to the character root node in the inspector |
| Drive `AnimationPlayer.play()` directly for a character with `AnimationTree` active | Always use `playback.travel()` through the state machine; direct `play()` bypasses blending |
| `BoneAttachment3D.override_pose = true` without setting `bone_idx` | Set both `bone_name` and let the node resolve `bone_idx` in `_ready()`, or set `bone_idx` explicitly |
| Calling `set_bone_global_pose_override` every `_ready()` | Call it every frame in `_process()` or `_physics_process()` — pose resets each frame from animation |

## References

- [AnimationPlayer](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html)
- [AnimationTree](https://docs.godotengine.org/en/stable/classes/class_animationtree.html)
- [AnimationMixer (4.3+)](https://docs.godotengine.org/en/stable/classes/class_animationmixer.html)
- [AnimationNodeStateMachine](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachine.html)
- [AnimationNodeStateMachinePlayback](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachineplayback.html)
- [Skeleton3D](https://docs.godotengine.org/en/stable/classes/class_skeleton3d.html)
- [SkeletonIK3D](https://docs.godotengine.org/en/stable/classes/class_skeletonik3d.html)
- [BoneAttachment3D](https://docs.godotengine.org/en/stable/classes/class_boneattachment3d.html)
- [Using AnimationTree (tutorial)](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html)
- [Root motion tutorial](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html#root-motion)

## Delegate to

| Task | Skill |
|---|---|
| GDScript animation logic | `godot:coder` |
| Signal connections | `godot:signals` |
| API lookup | `godot:docs` |
