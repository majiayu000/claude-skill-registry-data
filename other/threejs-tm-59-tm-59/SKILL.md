---
name: threejs
description: Use when building 3D browser games or scenes with Three.js — scene setup, procedural models from primitives, toon shading with outlines, third-person and first-person cameras, streaming terrain chunks, draw-call and memory budgets, and testing 3D in headless browsers. Also use when a Three.js scene is slow, leaks GPU memory, looks flat, or enemies fill the whole screen.
---

# Three.js

Default: Three.js via npm with Vite, `WebGLRenderer` with `antialias`, one scene graph, procedural geometry from primitives (no external models unless allowed), a fixed-step simulation separate from rendering.

## Setup

```ts
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));   // cap: 3x DPR costs a lot
renderer.setSize(innerWidth, innerHeight);
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 2000);
```

- Use `THREE.Timer` (or your own clock) for delta time; clamp large deltas after tab switches.
- Keep game state in plain objects; sync meshes from state each frame.

## Procedural models that read well

- Build characters from grouped primitives (boxes, capsules, cones) with a clear silhouette; bake small parts into one geometry (`mergeGeometries`) to save draw calls.
- Toon look: `MeshToonMaterial` with a 3-step gradient map, plus an outline from an inverted hull (same mesh scaled slightly, back faces, black `MeshBasicMaterial`). Limit outlines to nearby objects.
- Vertex colours give variety without textures.

## Camera and scale

- Measure how much of the screen the nearest enemy covers (project its bounding box to screen space). If it exceeds about a quarter of the view at normal fighting distance, players cannot see the fight — adjust model size, camera distance or field of view.
- Third-person: a spring arm with collision against terrain and buildings so the camera does not clip.
- First-person: Pointer Lock API for mouse look; check the sign of strafe directions against the camera's actual right vector.

## Open worlds

- Split terrain into chunks (e.g. 256–512 m) and load/unload by distance; build chunk meshes off the main thread if they are expensive.
- Use fog to hide the streaming edge.
- Instance repeated objects (`InstancedMesh`) — trees, rocks, props.
- Track `renderer.info.render.calls` and `renderer.info.memory`; set budgets and assert them in a test scene.

## Memory

- Dispose geometry, materials and textures you remove (`.dispose()`); removing from the scene does not free GPU memory.
- Share materials and geometries between identical objects.

## Verification loop

1. Unit-test simulation without WebGL.
2. Playwright smoke: load each scene, assert no console errors, record `renderer.info` numbers and a screenshot.
3. Treat headless fps (software rendering) as a relative signal only; check real fps on target hardware.

## Pitfalls

- **Z-fighting** on large scenes: raise `near`, lower `far`, or use a logarithmic depth buffer.
- **Shadows** are expensive: limit casters, tighten the shadow camera frustum, and do not let huge terrain meshes cast shadows.
- **Transparent objects** sort per object, not per triangle; keep transparency rare.
- **Huge single meshes** cannot be frustum-culled; chunk them.
- **Deprecated APIs** move between releases (e.g. `Clock` vs `Timer`, geometry utilities); pin the version and read the migration notes when upgrading.
