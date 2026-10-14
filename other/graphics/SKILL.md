---
name: graphics
description: Godot graphics developer — use when setting up lighting, environment, post-processing, global illumination, or reflection probes.
type: implementation
---

# Godot Graphics

> Expert Godot 4.x graphics programmer specializing in GI, post-processing, lighting, and rendering performance.

## Overview

Godot 4.x uses a Vulkan-based renderer with two paths: Forward+ (full-featured, desktop) and Mobile (subset, GLES3-compatible). The `Environment` resource drives most visual quality settings — attached to a `WorldEnvironment` node for scene-wide defaults or overridden per-camera. Global illumination, tone mapping, fog, and color grading all live here. Lighting quality is a trade-off between bake time, runtime cost, and dynamism — choose the right GI method for your scene type up front.

## Key Nodes & APIs

| Node / Class | Purpose | Key Properties |
|---|---|---|
| `WorldEnvironment` | Scene-level environment singleton | `environment` (resource) |
| `Environment` | Sky, fog, GI, tone mapping, color grading | Many — see sections below |
| `DirectionalLight3D` | Sun / moon, shadow cascades | `directional_shadow_mode`, `directional_shadow_split_1/2/3` |
| `OmniLight3D` / `SpotLight3D` | Local lights | `shadow_enabled`, `light_bake_mode` |
| `LightmapGI` | Baked static lightmaps | `quality`, `bounces`, `use_denoiser` |
| `VoxelGI` | Real-time voxel GI for small areas | `subdiv`, `extents` |
| `ReflectionProbe` | Local specular reflections | `update_mode`, `interior`, `extents` |
| `OccluderInstance3D` | CPU occlusion culling | `occluder` (Occluder3D resource) |
| `GeometryInstance3D` | Base for all 3D mesh nodes | `lod_bias`, `visibility_range_begin/end` |
| `MultiMeshInstance3D` | GPU-instanced repeated meshes | `multimesh` (MultiMesh resource) |
| `VisibilityNotifier3D` | Trigger logic at visibility boundaries | `aabb`, signals `screen_entered/exited` |
| `Camera3D` | FOV, DoF, per-camera environment override | `environment`, `attributes` |
| `FogVolume` | Local volumetric fog zones | `shape`, `material` (FogMaterial) |

## GI Comparison Table

| Method | Use Case | Bake Required | Dynamic Objects Lit | Runtime Cost |
|---|---|---|---|---|
| **SDFGI** | Large open worlds, outdoor scenes | No (real-time) | Yes | Medium — scales with probe count |
| **LightmapGI** | Indoor scenes, static architecture, highest quality | Yes (CPU/GPU bake) | No (static only) | Very low — texture lookup |
| **VoxelGI** | Small interior rooms, dynamic scenes needing accurate GI | No (real-time) | Yes | High — full voxel traversal per frame |

Decision guide: use LightmapGI for any static scene where bake time is acceptable. Use SDFGI for large outdoor/open-world levels. Use VoxelGI only for small, contained areas where accuracy matters more than cost and baking is not viable.

## Core Patterns

### Pattern 1 — Directional Light Shadow Cascades

Configure PSSM split cascades on `DirectionalLight3D` to balance shadow quality vs. distance:

```gdscript
@onready var sun: DirectionalLight3D = $Sun

func _ready() -> void:
    # Use 4-split PSSM for best quality at range
    sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_4_SPLITS
    # Split distances as fractions of shadow_max_distance (default 100 m)
    sun.directional_shadow_split_1 = 0.1   # 10 m — high detail near camera
    sun.directional_shadow_split_2 = 0.3   # 30 m
    sun.directional_shadow_split_3 = 0.6   # 60 m
    sun.shadow_max_distance = 200.0
    sun.directional_shadow_fade_start = 0.9
```

For mobile / low-end targets prefer `SHADOW_PARALLEL_2_SPLITS` or `SHADOW_ORTHOGONAL`.

### Pattern 2 — HDR Tone Mapping and Color Grading

Set tone mapping and color grading on the `Environment` resource. ACES is the best starting point for filmic look; use a LUT texture for per-project art direction:

```gdscript
func setup_environment(env: Environment) -> void:
    # Tone mapping
    env.tonemap_mode = Environment.TONE_MAPPER_ACES      # ACES | FILMIC | REINHARD | LINEAR
    env.tonemap_exposure = 1.0
    env.tonemap_white = 6.0   # scene-referencing white point

    # Basic color grading
    env.adjustment_enabled = true
    env.adjustment_brightness = 1.0
    env.adjustment_contrast = 1.05
    env.adjustment_saturation = 1.1

    # LUT-based color correction (optional — assign a 256x16 or 512x512 LUT texture)
    # env.adjustment_color_correction = preload("res://art/luts/filmic_lut.png")
```

Tone mapper choice: ACES gives filmic roll-off and slight warm contrast. Filmic is a softer S-curve. Reinhard is simple and cheap but clips highlights. Linear disables tone mapping entirely — use only when the display pipeline handles it externally.

### Pattern 3 — Volumetric Fog

Enable screen-space volumetric fog via `Environment`. Combine with `FogVolume` nodes for localized zones:

```gdscript
func setup_fog(env: Environment) -> void:
    env.volumetric_fog_enabled = true
    env.volumetric_fog_density = 0.02          # overall scene density
    env.volumetric_fog_albedo = Color(0.8, 0.85, 0.9)  # scatter color
    env.volumetric_fog_emission = Color(0.0, 0.0, 0.0) # self-emission (use for glowing fog)
    env.volumetric_fog_emission_energy = 0.0
    env.volumetric_fog_length = 64.0           # meters fog is visible
    env.volumetric_fog_detail_spread = 2.0
    env.volumetric_fog_gi_inject = 0.9         # how much GI tints the fog
    env.volumetric_fog_temporal_reprojection_enabled = true  # reduces flickering
```

For localized fog (e.g. a swamp patch), add a `FogVolume` node with a `FogMaterial` and set `env.volumetric_fog_enabled = true` at scene level — FogVolumes only render if volumetric fog is globally active.

### Pattern 4 — GPU Instancing with MultiMeshInstance3D

Use `MultiMeshInstance3D` for large numbers of identical meshes (trees, rocks, grass, crowd units). Each instance is a single draw call:

```gdscript
func spawn_trees(mesh: Mesh, positions: Array[Vector3]) -> void:
    var mm := MultiMesh.new()
    mm.transform_format = MultiMesh.TRANSFORM_3D
    mm.instance_count = positions.size()
    mm.mesh = mesh

    for i in positions.size():
        var xform := Transform3D(Basis(), positions[i])
        # Optional: randomize rotation/scale per instance
        xform.basis = xform.basis.rotated(Vector3.UP, randf() * TAU)
        xform.basis = xform.basis.scaled(Vector3.ONE * randf_range(0.8, 1.2))
        mm.set_instance_transform(i, xform)

    var mmi := MultiMeshInstance3D.new()
    mmi.multimesh = mm
    add_child(mmi)
```

Prefer `MultiMesh.TRANSFORM_2D` for flat/billboard instances to halve the per-instance data size.

### Pattern 5 — Occlusion Culling with OccluderInstance3D

Place `OccluderInstance3D` around doorways, large opaque props, and building facades. The CPU occluder prevents draw calls for anything behind solid geometry:

```gdscript
# Editor setup — attach script to a scene root to auto-build box occluders
func add_box_occluder(parent: Node3D, size: Vector3, origin: Vector3) -> void:
    var occ_res := BoxOccluder3D.new()
    occ_res.size = size

    var occ_inst := OccluderInstance3D.new()
    occ_inst.occluder = occ_res
    occ_inst.position = origin
    parent.add_child(occ_inst)
```

Available `Occluder3D` resource types: `BoxOccluder3D`, `SphereOccluder3D`, `QuadOccluder3D`, `PolygonOccluder3D`, `ArrayOccluder3D`. Use `PolygonOccluder3D` for custom silhouettes (L-shaped walls, arches). Enable occlusion culling in **Project Settings > Rendering > Occlusion Culling > Use Occlusion Culling**.

### Pattern 6 — LOD and Visibility Range

Control per-mesh detail via `GeometryInstance3D` visibility range and `lod_bias`:

```gdscript
func configure_lod(mesh_instance: MeshInstance3D) -> void:
    # Built-in LOD — importer generates LOD meshes automatically if enabled
    mesh_instance.lod_bias = 1.0   # increase to prefer lower LODs sooner

    # Manual visibility range — hide beyond 80 m, fade out between 60–80 m
    mesh_instance.visibility_range_begin = 0.0
    mesh_instance.visibility_range_end = 80.0
    mesh_instance.visibility_range_begin_margin = 0.0
    mesh_instance.visibility_range_end_margin = 20.0
    mesh_instance.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF

# For logic disable (AI, physics) use VisibilityNotifier3D signals
func _ready() -> void:
    $VisibilityNotifier3D.screen_exited.connect(_on_offscreen)

func _on_offscreen() -> void:
    $NavigationAgent3D.set_process(false)
```

## Common Pitfalls

- **Duplicating WorldEnvironment** — Godot merges multiple `WorldEnvironment` nodes unpredictably. Keep exactly one per scene tree; override per-camera via `Camera3D.environment` instead of adding a second `WorldEnvironment`.
- **Shipping unbaked LightmapGI** — an unbaked `LightmapGI` node falls back to flat ambient light and destroys visual quality silently. Always bake before export; add a CI check or pre-export script that warns if `LightmapGI` data is missing.
- **VoxelGI over large areas** — VoxelGI voxel count scales with volume cubed. Doubling the `extents` in all axes multiplies cost by 8×. Keep extents below ~20 m on each axis; tile multiple small volumes rather than one large one.
- **Leaving ReflectionProbe on `UPDATE_ALWAYS`** — `UPDATE_ALWAYS` re-renders the probe every frame (6 cube faces). Use `UPDATE_ONCE` for static environments; trigger a manual update via `ReflectionProbe.update_mode` toggle in script only when environment changes.
- **Volumetric fog without temporal reprojection** — disabling `volumetric_fog_temporal_reprojection_enabled` causes severe per-pixel noise at low sample counts. Keep it enabled unless you have a specific anti-ghosting reason to disable it.
- **Forgetting `light_bake_mode` on dynamic lights** — by default, `OmniLight3D` and `SpotLight3D` contribute to LightmapGI. Set `light_bake_mode = LIGHT_BAKE_DISABLED` on lights that are spawned at runtime or toggled frequently to avoid bake-time errors.

## Performance

**Draw calls** — each `MeshInstance3D` with a unique material is a draw call. Batch static geometry using `MeshInstance3D` merge (editor tool) or use `MultiMeshInstance3D` for repeating meshes. Target < 500 draw calls on mid-range desktop, < 200 on mobile.

**LOD** — enable automatic LOD generation in **Project Settings > Rendering > Mesh LOD**. Set `lod_bias` globally via `Viewport.mesh_lod_threshold`. Use `GeometryInstance3D.visibility_range_end` for hard pop-out of distant props that have no LOD mesh.

**Shadow cascades** — PSSM4 is the most expensive; use PSSM2 or Orthogonal for mobile. Reduce `DirectionalLight3D.shadow_max_distance` aggressively — shadows beyond 150 m are rarely visible. `directional_shadow_pancaking` reduces self-shadow artifacts at cascade boundaries.

**Occlusion culling** — only effective when the scene has large opaque occluders (buildings, terrain). Profile with the **Rooms & Portals** debug view. Misplaced occluders that cull visible geometry cause objects to pop out; verify placement in the occlusion debug overlay.

**Volumetric fog cost** — controlled by `ProjectSettings > rendering/environment/volumetric_fog/volume_size` and `volume_depth`. Halving `volume_size` roughly quarters GPU cost with minor quality loss.

**GI cost** — SDFGI probe density is set in `Environment.sdfgi_cascades` and `sdfgi_min_cell_size`. Fewer cascades or larger cell size cuts cost. Disable SDFGI on mobile; use baked lightmaps instead.

## Anti-Patterns

| Wrong | Right |
|---|---|
| One `WorldEnvironment` per sub-scene for modular levels | One global `WorldEnvironment` in the root scene; override per-camera with `Camera3D.environment` |
| `VoxelGI` covering an entire outdoor level | SDFGI for outdoors; `VoxelGI` only for small enclosed spaces |
| `ReflectionProbe.update_mode = UPDATE_ALWAYS` in a static room | `UPDATE_ONCE` — trigger re-bake only on environment change |
| Spawning 1000 `MeshInstance3D` for grass blades | `MultiMeshInstance3D` with one draw call for all instances |
| Shipping with `LightmapGI` node present but not baked | Bake before export; automate a check in pre-export script |
| Enabling volumetric fog with defaults on mobile | Disable volumetric fog on mobile; use depth fog (`Environment.fog_enabled`) instead |

## References

- Environment resource: https://docs.godotengine.org/en/stable/classes/class_environment.html
- LightmapGI: https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/using_lightmap_gi.html
- SDFGI: https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/using_sdfgi.html
- VoxelGI: https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/using_voxel_gi.html
- Volumetric fog: https://docs.godotengine.org/en/stable/tutorials/3d/volumetric_fog.html
- MultiMeshInstance3D: https://docs.godotengine.org/en/stable/classes/class_multimeshinstance3d.html
- OccluderInstance3D: https://docs.godotengine.org/en/stable/classes/class_occluderinstance3d.html
- GeometryInstance3D LOD: https://docs.godotengine.org/en/stable/classes/class_geometryinstance3d.html
- DirectionalLight3D shadows: https://docs.godotengine.org/en/stable/classes/class_directionallight3d.html
- Rendering performance: https://docs.godotengine.org/en/stable/tutorials/performance/rendering/index.html

## Delegate to

| Task | Skill |
|---|---|
| Custom shaders | `godot:shader` |
| GDScript configuration | `godot:coder` |
| API lookup | `godot:docs` |
