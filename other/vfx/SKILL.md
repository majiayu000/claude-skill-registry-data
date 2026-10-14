---
name: vfx
description: Godot VFX developer — use when creating particle effects, trails, impacts, or screen-space effects.
type: implementation
---

# Godot VFX

> Design, implement, and optimize real-time visual effects in Godot 4.x using GPU particles, shaders, decals, and screen-space techniques.

## Overview

VFX in Godot 4.x centers on `GPUParticles3D` for particle simulation, `Decal` for surface projection, shader-based effects for screen-space and material overrides, and `ImmediateMesh` for procedural geometry like trails. Effects should be standalone scenes instantiated at runtime, pooled where possible, and culled by distance or visibility.

## Key Nodes & APIs

| Node / API | Purpose | Key Properties |
|---|---|---|
| `GPUParticles3D` | GPU-accelerated particle system | `amount`, `lifetime`, `one_shot`, `explosiveness`, `sub_emitter` |
| `CPUParticles3D` | CPU fallback for low-end targets | Same surface API as GPU variant |
| `GPUParticlesAttractorBox3D` | Pull particles toward a volume | `strength`, `attenuation` |
| `GPUParticlesAttractorSphere3D` | Spherical attractor | `radius`, `strength` |
| `GPUParticlesCollisionBox3D` | Make particles collide with geometry | `extents` |
| `GPUParticlesCollision3D` | Base class for particle collision shapes | — |
| `Decal` | Project textures onto surfaces (bullet holes, scorch) | `texture_albedo`, `cull_mask`, `upper_fade`, `lower_fade` |
| `ImmediateMesh` | Procedural mesh rebuilt each frame (trails, ribbons) | `surface_begin()`, `surface_add_vertex()`, `surface_end()` |
| `VisibilityNotifier3D` | Emit signals when AABB enters/exits screen | `screen_entered`, `screen_exited` |
| `ParticleProcessMaterial` | Controls per-particle behavior via shader parameters | `emission_shape`, `color_ramp`, `turbulence_enabled` |
| `VisualShader` | Node-based shader editor for particle materials | — |

## Core Patterns

### One-Shot VFX Pool

Pre-instantiate N effect instances and replay them with `restart()` instead of destroying and re-creating nodes.

```gdscript
# vfx_pool.gd
class_name VFXPool
extends Node

@export var effect_scene: PackedScene
@export var pool_size: int = 8

var _pool: Array[GPUParticles3D] = []
var _index: int = 0

func _ready() -> void:
    for i in pool_size:
        var fx: GPUParticles3D = effect_scene.instantiate()
        fx.one_shot = true
        fx.emitting = false
        add_child(fx)
        _pool.append(fx)

func play(pos: Vector3, normal: Vector3 = Vector3.UP) -> void:
    var fx: GPUParticles3D = _pool[_index]
    _index = (_index + 1) % pool_size
    fx.global_position = pos
    fx.global_basis = Basis(normal, Vector3.UP, normal.cross(Vector3.UP).normalized())
    fx.restart()
```

### Decal for Bullet Holes and Scorch Marks

Place a `Decal` at the hit point oriented along the surface normal. Use `cull_mask` to avoid projecting onto the sky or specific layers.

```gdscript
# impact_decal_spawner.gd
extends Node3D

@export var decal_scene: PackedScene
@export var max_decals: int = 20

var _decals: Array[Decal] = []

func spawn_decal(hit_position: Vector3, hit_normal: Vector3) -> void:
    var decal: Decal = decal_scene.instantiate() as Decal
    get_tree().root.add_child(decal)

    decal.global_position = hit_position + hit_normal * 0.01  # small offset to avoid z-fight
    decal.look_at(hit_position - hit_normal, Vector3.UP)
    # Exclude sky layer (layer 20) and transparent layer (layer 19)
    decal.cull_mask = 0b0000_0000_0000_0000_0111_1111_1111_1111

    _decals.append(decal)
    if _decals.size() > max_decals:
        _decals.pop_front().queue_free()
```

### Shader-Based Hit Flash

Override a material's `flash_amount` uniform via script for a brief white flash on damage.

```gdscript
# hit_flash.gd
extends MeshInstance3D

var _tween: Tween

func flash(duration: float = 0.15) -> void:
    var mat: ShaderMaterial = get_active_material(0) as ShaderMaterial
    if mat == null:
        return
    if _tween:
        _tween.kill()
    _tween = create_tween()
    mat.set_shader_parameter("flash_amount", 1.0)
    _tween.tween_method(
        func(v: float) -> void: mat.set_shader_parameter("flash_amount", v),
        1.0, 0.0, duration
    )
```

Companion `canvas_item` shader (attach to a `MeshInstance3D` surface material):

```glsl
shader_type spatial;
uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;
uniform sampler2D albedo_texture : source_color;

void fragment() {
    vec4 base = texture(albedo_texture, UV);
    ALBEDO = mix(base.rgb, vec3(1.0), flash_amount);
    ALPHA = base.a;
}
```

### Particle LOD via VisibilityNotifier3D

Disable expensive `GPUParticles3D` when their AABB leaves the screen to save GPU time.

```gdscript
# particle_lod.gd
extends GPUParticles3D

@onready var _notifier: VisibilityNotifier3D = $VisibilityNotifier3D

func _ready() -> void:
    _notifier.screen_exited.connect(_on_screen_exited)
    _notifier.screen_entered.connect(_on_screen_entered)

func _on_screen_exited() -> void:
    emitting = false

func _on_screen_entered() -> void:
    emitting = true
```

### Screen-Space Heat Shimmer (Distortion)

Sample `SCREEN_TEXTURE` with a UV offset driven by a noise texture for heat haze.

```glsl
shader_type spatial;
render_mode unshaded, depth_draw_never, cull_disabled;

uniform sampler2D noise_texture : hint_default_white;
uniform float distortion_strength : hint_range(0.0, 0.05) = 0.01;
uniform float scroll_speed : hint_range(0.0, 2.0) = 0.3;

void fragment() {
    vec2 scroll = vec2(0.0, TIME * scroll_speed);
    vec2 noise_uv = UV + scroll;
    vec2 offset = (texture(noise_texture, noise_uv).rg - 0.5) * distortion_strength;
    vec2 screen_uv = SCREEN_UV + offset;
    ALBEDO = texture(SCREEN_TEXTURE, screen_uv).rgb;
    ALPHA = 1.0;
}
```

### ImmediateMesh Ribbon Trail

Rebuild a triangle-strip mesh every frame to trace a trail behind a moving object.

```gdscript
# ribbon_trail.gd
extends MeshInstance3D

@export var max_points: int = 32
@export var width: float = 0.1

var _points: Array[Vector3] = []
var _mesh: ImmediateMesh

func _ready() -> void:
    _mesh = ImmediateMesh.new()
    mesh = _mesh

func _process(_delta: float) -> void:
    _points.push_front(global_position)
    if _points.size() > max_points:
        _points.pop_back()

    _mesh.clear_surfaces()
    if _points.size() < 2:
        return

    _mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
    for i in _points.size():
        var dir: Vector3 = Vector3.ZERO
        if i > 0:
            dir = (_points[i - 1] - _points[i]).normalized()
        var right: Vector3 = dir.cross(Vector3.UP).normalized() * width * 0.5
        _mesh.surface_add_vertex(_points[i] + right)
        _mesh.surface_add_vertex(_points[i] - right)
    _mesh.surface_end()
```

### Sub-Emitter on Particle Collision

Assign a child `GPUParticles3D` to the `sub_emitter` property so secondary sparks spawn when primary particles hit a surface.

```gdscript
# setup_sub_emitter.gd
extends GPUParticles3D

@onready var _sparks: GPUParticles3D = $SparksSubEmitter

func _ready() -> void:
    # The ParticleProcessMaterial collision must be enabled for sub_emitter to fire.
    sub_emitter = _sparks.get_path()
    var mat := process_material as ParticleProcessMaterial
    if mat:
        mat.collision_mode = ParticleProcessMaterial.COLLISION_RIGID
```

### GPUParticlesCollisionBox3D — Floor Collisions

Place a collision volume at floor height so particles bounce or stick instead of passing through.

```gdscript
# scene tree: GPUParticles3D > GPUParticlesCollisionBox3D (child)
# In _ready, configure the collision material parameter:
func _ready() -> void:
    var mat := $GPUParticles3D.process_material as ParticleProcessMaterial
    mat.collision_mode = ParticleProcessMaterial.COLLISION_RIGID
    mat.collision_bounce = 0.3
    mat.collision_friction = 0.8
    # The GPUParticlesCollisionBox3D in the scene tree is detected automatically.
```

## Common Pitfalls

- **`amount` alone does not determine memory cost.** Peak live particles equals `amount * lifetime / emission_rate`. A system with `amount = 1000` and `lifetime = 5.0` keeps up to 1000 particles alive simultaneously — set `amount` to the peak concurrency you can afford, not an arbitrary large value.
- **Re-instantiating one-shot effects every trigger is expensive.** Calling `queue_free()` followed by a new `instantiate()` per hit stresses the allocator and triggers shader compilation stalls. Always use `restart()` on a pooled instance.
- **`Decal` projects onto every layer unless you set `cull_mask`.** Sky boxes, transparent glass, and background planes will receive the decal unless their collision/render layer is excluded via `cull_mask`.
- **`ImmediateMesh` allocates a new surface every frame** if `clear_surfaces()` is not called before `surface_begin()`. Always call `clear_surfaces()` at the start of `_process` before rebuilding the mesh.
- **Sub-emitters require `collision_mode` to be set on `ParticleProcessMaterial`.** The `sub_emitter` property is ignored if the process material does not have collision enabled — there is no editor warning.
- **`VisibilityNotifier3D` AABB defaults to a unit cube.** If the particle system emits beyond 0.5 m in any axis the notifier will fire prematurely. Set `aabb` to match the actual emission bounds.
- **Shader uniforms set via `set_shader_parameter()` are per-instance only when the material is set to `local to scene`.** Forgetting this causes all objects sharing the material to flash simultaneously.

## Performance

**Peak particle memory = `amount` × `lifetime`** (not just `amount`). Each particle occupies a fixed GPU buffer slot for its entire lifetime. Budget this product against your per-frame particle limit.

| Budget tier | Recommended `amount × lifetime` product |
|---|---|
| Mobile / low | ≤ 500 |
| Desktop / medium | ≤ 5 000 |
| Desktop / high | ≤ 20 000 |

**LOD strategy:**
1. Use `VisibilityNotifier3D.screen_exited` to stop `emitting` when off-screen.
2. Scale `amount` down in `_process` based on `Camera3D.global_position.distance_to(global_position)`.
3. Swap `GPUParticles3D` for `CPUParticles3D` only as a last resort on mobile — CPU particles bypass the GPU pipeline entirely but cost main-thread time.

**GPU vs CPU particles:**
- `GPUParticles3D`: simulation runs entirely on GPU; zero CPU cost per particle; requires Vulkan/Forward+.
- `CPUParticles3D`: simulation runs on CPU; compatible with Compatibility renderer (OpenGL); use only when targeting very low-end hardware or WebGL.

**Other tips:**
- Prefer `ONE_SHOT` + pool over spawning new scenes — avoids per-frame node tree modification overhead.
- Limit `sub_emitter` chains to one level; nested sub-emitters multiply particle counts quickly.
- Use `explosiveness = 1.0` for burst effects instead of high `amount` with spread emission.

## Anti-Patterns

| Wrong | Right |
|---|---|
| `queue_free()` + `instantiate()` per hit | Pool N instances, call `restart()` |
| `amount = 10000` for a smoke trail | Set `amount` to peak concurrency (e.g. 200) and tune `lifetime` |
| Child particle scene embedded in player scene | Standalone VFX scene, instantiated and positioned at runtime |
| `set_shader_parameter()` on a shared material | Set material to `local to scene`, then call `set_shader_parameter()` |
| Decal with default `cull_mask = 0xFFFFFFFF` | Set `cull_mask` to exclude sky, glass, and background layers |
| Spawning sub-emitters by instantiating new scenes | Assign `sub_emitter` path in editor; let the particle system trigger it |
| Rebuilding `ImmediateMesh` without `clear_surfaces()` | Always call `clear_surfaces()` before `surface_begin()` each frame |

## References

- [GPUParticles3D class reference](https://docs.godotengine.org/en/stable/classes/class_gpuparticles3d.html)
- [ParticleProcessMaterial class reference](https://docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html)
- [Decal class reference](https://docs.godotengine.org/en/stable/classes/class_decal.html)
- [ImmediateMesh class reference](https://docs.godotengine.org/en/stable/classes/class_immediatemesh.html)
- [VisibilityNotifier3D class reference](https://docs.godotengine.org/en/stable/classes/class_visibilitynotifier3d.html)
- [GPUParticlesCollision3D class reference](https://docs.godotengine.org/en/stable/classes/class_gpuparticlescollision3d.html)
- [Particle systems (3D) — Godot docs](https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html)
- [Using VisualShaders — Godot docs](https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html)
- [Screen-reading shaders — Godot docs](https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html)

## Delegate to

| Task | Skill |
|---|---|
| Particle/visual shaders | `godot:shader` |
| Scene instantiation | `godot:scene` |
| GDScript particle control | `godot:coder` |
| API lookup | `godot:docs` |
