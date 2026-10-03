---
name: implement-renderer
description: "Use when generating renderer code from renderer architecture spec (Phaser 3 for 2D web, Three.js for 3D web). Triggers: 'implement renderer', 'renderer code'."
---

## 1. Overview

Reads `renderer_spec.md` + `rendering_target.md`, generates engine-specific renderer code with ECS integration.

## 2. Quick Reference

| Engine | Output Directory | Key Files |
|--------|------------------|-----------|
| Phaser 3 (2D) | `src/renderer/` | phaser_renderer.ts, components.ts, systems.ts, asset_wiring.ts, placeholder.ts |
| Three.js (3D) | `src/renderer/` | threejs_renderer.ts, components.ts, systems.ts, asset_wiring.ts, placeholder.ts |
| Other | `src/renderer/` | Placeholder system with TODO comment |

Mappings: Sprite→Phaser.Sprite / Mesh→THREE.Mesh; Camera→Phaser.Camera / PerspectiveCamera.

## 3. Core Pattern

Read `renderer_spec.md` + `rendering_target.md` (REQUIRED). Detect language (TS/JS/Rust).

### 2.3 Renderer Code Generation

**Phaser 3 (2D)** — in `{TARGET_FOLDER}/src/renderer/`:

| File | Content |
|------|---------|
| `phaser_renderer.ts` | Phaser Scene, init, lifecycle |
| `components.ts` | ECS types: Transform, Sprite, Camera, Material, AnimatedSprite, Tilemap |
| `systems.ts` | Systems: RendererSystem, CameraSystem, ParticleSystem |
| `asset_wiring.ts` | AssetRef → Phaser textures |
| `placeholder.ts` | Fallback colored rectangle |

Mappings: Sprite→Phaser.Sprite, Camera→Phaser.Camera, Transform→x/y/rotation/scale.

```typescript
const config = { type: Phaser.AUTO, width: viewport.width, height: viewport.height, backgroundColor: '#000000', scene: [GameScene], scale: { mode: Phaser.Scale.FIT } };
const game = new Phaser.Game(config);
```

**Three.js (3D)** — in `{TARGET_FOLDER}/src/renderer/`:

| File | Content |
|------|---------|
| `threejs_renderer.ts` | Three.js Scene, WebGLRenderer, camera, loop |
| `components.ts` | ECS types: Transform, Mesh, Camera, Light, Shadow, Material |
| `systems.ts` | Systems: RendererSystem, CameraSystem, LightingSystem |
| `asset_wiring.ts` | AssetRef → Three.js textures/geometries |
| `placeholder.ts` | Fallback colored cube/sphere |

Mappings: Mesh→THREE.Mesh, Camera→PerspectiveCamera, Light→PointLight/DirectionalLight/SpotLight, Transform→Object3D.

```typescript
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, viewport.width / viewport.height, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(viewport.width, viewport.height);
document.body.appendChild(renderer.domElement);
function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
animate();
```

**Non-Supported** — Placeholder:
```typescript
// ⚠️ PLACEHOLDER — Manual setup required
export class PlaceholderRendererSystem { update(w: World, dt: number): void { /* TODO */ } }
```

#### 2.4 ECS Components
Generate structs per `renderer_spec.md` (TS interfaces/classes or Rust `Component` trait).

### 2.5 Asset Integration
Store textures in AssetManager; RendererSystem queries it.

### 2.6 Game Loop
Renderer init during bootstrap; RendererSystem called every frame via `world.update(dt)`.

## 3. Output File Structure

```
src/renderer/
├── components.ts          # ECS component definitions
├── systems.ts             # ECS renderer systems
├── {engine}_renderer.ts   # Engine-specific setup
├── asset_wiring.ts        # AssetRef → renderable mapping
└── placeholder.ts         # Fallback renderer
```

## 4. Validation Checklist

- [ ] Files in `{TARGET_FOLDER}/src/renderer/`
- [ ] ECS components match spec
- [ ] RendererSystem registered with ECS World
- [ ] AssetRef → renderable mapping
- [ ] Placeholder fallback
- [ ] Correct engine API
- [ ] Phaser: AUTO type, scale, scene config | Three.js: WebGLRenderer, scene, camera, loop
- [ ] Renderer called via `world.update(dt)`
- [ ] Cleanup/disposal logic

## 5. Red Flags

- **Required Input Present**: Read renderer_spec.md before generating output
- **Correct Engine API**: Use Phaser APIs for Phaser projects, Three.js APIs for Three.js projects
- **Complete Asset Integration**: Include AssetRef mapping and placeholder fallback
- **Code Generation Focus**: Generate implementation code, not spec documents

## 6. Execution Command

Command: `/implement-renderer`
