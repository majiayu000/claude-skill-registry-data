---
name: design-rendering-architecture
description: "Use when rendering_target.md exists and you need a renderer architecture spec. Triggers: 'renderer spec', 'renderer architecture', 'Phaser renderer', 'Three.js renderer'."
---

## 1. Template Binding

- **Output**: `{TARGET_FOLDER}/docs/renderer_spec.md`
- **Inputs**: `rendering_target.md`, `visual_style.md`

## 2. Quick Reference

**Output**: `{TARGET_FOLDER}/docs/renderer_spec.md`. **Inputs**: `rendering_target.md`, `visual_style.md`.

| Engine | Architecture | Key Mappings |
|--------|-------------|--------------|
| Phaser 3 | ECS wraps Phaser Scene | Sprite→Phaser.Sprite, Camera→Phaser.Camera |
| Three.js | ECS syncs to Three.js Scene | Mesh→THREE.Mesh, Camera→PerspectiveCamera |
| Unity | ECS maps to Unity Renderer/MeshFilter/Material | — |
| Godot | ECS maps to Sprite2D/MeshInstance3D/Camera3D | — |

Components: Transform/Sprite/Camera/Material always; Mesh/Light/Shadow for 3D only; AnimatedSprite/Tilemap for 2D only. System order: `[Game Systems] → CameraSystem → LightingSystem → RendererSystem → ParticleSystem`.

## 3. Core Pattern

### 2.1 Input Analysis
Read `rendering_target.md` + `visual_style.md` (REQUIRED). Abort if target missing.

### 2.2 Engine Architecture

| Engine | Architecture |
|--------|-------------|
| **Phaser 3** | ECS wraps Phaser Scene. Sprite→Phaser.Sprite, Camera→Phaser.Camera. |
| **Three.js** | ECS syncs to Three.js Scene. Mesh→THREE.Mesh, Camera→PerspectiveCamera. |
| **Unity** | ECS maps to Unity Renderer/MeshFilter/Material. |
| **Godot** | ECS maps to Sprite2D, MeshInstance3D, Camera3D. |
| **Other** | Placeholder spec with TODO. |

### 2.3 ECS Components

**Core (always):**

| Component | Fields | Purpose |
|-----------|--------|---------|
| `Transform` | `position: Vec2/Vec3`, `rotation: f32`, `scale: Vec2/Vec3` | Spatial data |
| `Sprite` | `asset_id: AssetRef`, `frame: u32`, `visible: bool`, `z_index: i32` | 2D sprite |
| `Camera` | `viewport: Rect`, `follow_entity: Option<EntityId>`, `zoom: f32` | Viewport |
| `Material` | `color: Color`, `opacity: f32`, `shader: Option<String>` | Appearance |

**3D-Only (3D dimension):**

| Component | Fields | Purpose |
|-----------|--------|---------|
| `Mesh` | `asset_id: AssetRef`, `material_id: AssetRef` | 3D geometry |
| `Light` | `type: Point/Directional/Spot`, `intensity: f32`, `color: Color`, `range: f32` | Lighting |
| `Shadow` | `cast: bool`, `receive: bool`, `resolution: u32` | Shadow mapping |

**2D-Only (2D dimension):**

| Component | Fields | Purpose |
|-----------|--------|---------|
| `AnimatedSprite` | `asset_id: AssetRef`, `frames: Vec<u32>`, `fps: f32`, `looping: bool` | Animation |
| `Tilemap` | `asset_id: AssetRef`, `tile_size: Vec2`, `layers: Vec<String>` | Tile rendering |

### 2.4 System Architecture

| System | Phase | Purpose |
|--------|-------|---------|
| `RendererSystem` | Late | Reads Transform+Sprite/Mesh+Camera+Material, issues draw calls |
| `CameraSystem` | Mid | Updates camera follow targets |
| `LightingSystem` | Mid | Computes light positions, shadow maps (3D) |
| `ParticleSystem` | Late | Particle rendering |

**Order**: `[Game Systems] → CameraSystem → LightingSystem → RendererSystem → ParticleSystem`

### 2.5 Asset Integration
Sprite/Mesh reference `AssetRef`. RendererSystem queries `AssetManager`. Fallback: colored rectangle.

### 2.6 Output Format
Write `renderer_spec.md`: Engine Target, ECS Components, ECS Systems, Pipeline Stages, Asset Integration, Engine Notes.

## 3. When to Use

Use when:
- `rendering_target.md` exists and you need a renderer architecture spec before implementation.
- You're choosing between rendering engines (Phaser 3, Three.js, Unity, Godot) for a defined visual style.
- Upstream specs (`rendering_target.md` or `visual_style.md`) changed and the renderer spec needs regeneration.

Do not use when:
- The rendering target hasn't been decided yet — define it first.
- You only need asset integration details without full architecture.

## 4. Validation Checklist (MANDATORY)

- [ ] `rendering_target.md` + `visual_style.md` exist
- [ ] Dimension (2D/3D) correctly resolved
- [ ] Engine mappings correct
- [ ] Core components always present
- [ ] 3D-only components only for 3D, 2D-only for 2D
- [ ] Execution order, asset integration, engine notes defined

## 5. Red Flags

- **Required Input Present**: Read rendering_target.md and visual_style.md before generating output
- **Correct Dimension Components**: Use 3D-only components for 3D dimension, 2D-only for 2D
- **Concrete Engine Mappings**: Specify exact engine APIs and class names
- **Complete Asset Integration**: Document asset integration with engine-specific details

## 6. Execution Command

Command: `/design-rendering-architecture`
