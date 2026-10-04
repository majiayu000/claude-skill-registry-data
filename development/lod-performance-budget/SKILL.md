---
name: lod-performance-budget
description: Use this skill whenever creating scene geometry, configuring LOD switching, setting texture resolutions, implementing instancing or culling, or writing any performance-sensitive rendering code in the Myelin simulator. This defines the authoritative face counts, texture budgets, memory ceilings, and adaptive quality logic. Load this skill before writing any geometry, LOD, or instancing code.
---

This skill defines the performance budget and Level of Detail (LOD) system for the Myelin simulator. Every geometry object, every texture, and every rendering decision must stay within these budgets. Exceeding them degrades the learner experience on target hardware — a safety-training platform cannot afford to be unusable.

---

## Resolution and Quality Tiers

Four quality tiers. The active tier is detected at session start and may be downgraded adaptively during the session (see `webgl-renderer-baseline` skill for the adaptive logic).

| Tier | Viewport minimum | Texture target | Close-up geometry target |
|------|-----------------|----------------|--------------------------|
| MINIMUM | 1280 × 720 | 1024px | 32–48 segments |
| HD | 1920 × 1080 | 2048px | 64–96 segments |
| HD_PLUS | 2560 × 1440 | 2048–4096px | 96–128 segments |
| UHD | 3840 × 2160 | 4096px | 128+ segments |

"Segments" refers to the subdivision count on curved geometry (valve handwheel spokes, pipe radius, padlock shackle arc). Flat planar geometry has no segment count — it is always minimal.

---

## Memory Ceilings

Hard limits that must not be exceeded at any quality tier:

| Budget | Ceiling |
|--------|---------|
| Geometry (GPU buffer) | 128 MB |
| Textures (VRAM) | 512 MB |
| Physics world | 32 MB |
| Total scene memory (geometry + textures) | 640 MB |

Monitor memory usage in the performance tracking loop:

```javascript
function getMemoryUsage(renderer) {
  const info = renderer.info.memory;
  return {
    geometries: info.geometries,
    textures:   info.textures,
    // Estimate bytes: roughly 1k per geometry, (w*h*4) per texture
    estimatedTextureMB: estimateTextureMB(renderer)
  };
}

function estimateTextureMB(renderer) {
  let totalBytes = 0;
  renderer.info.programs?.forEach(program => {
    // Sum texture sizes from active programs
    totalBytes += estimateProgramTextureCost(program);
  });
  return totalBytes / (1024 * 1024);
}
```

If texture memory approaches 450 MB (88% of ceiling), downgrade one tier and dispose unused textures.

---

## LOD Object Configuration

Each primary interactive object in the LOTO scene must have explicit LOD levels. Use Three.js `LOD` object.

```javascript
function createLODObject(lod0Geo, lod1Geo, lod2Geo, lod3Geo, material) {
  const lod = new THREE.LOD();

  // LOD3 — VR/high detail (shown at close range < 2m)
  const mesh3 = new THREE.Mesh(lod3Geo, material);
  lod.addLevel(mesh3, 0);       // distance 0 = highest detail

  // LOD2 — desktop (shown at < 5m)
  const mesh2 = new THREE.Mesh(lod2Geo, material);
  lod.addLevel(mesh2, 2);

  // LOD1 — tablet (shown at < 12m)
  const mesh1 = new THREE.Mesh(lod1Geo, material);
  lod.addLevel(mesh1, 5);

  // LOD0 — mobile (shown at all distances on MINIMUM tier)
  const mesh0 = new THREE.Mesh(lod0Geo, material);
  lod.addLevel(mesh0, 12);

  return lod;
}
```

LOD distance thresholds (in world-space metres). These values assume a camera FOV of 60° and a standard simulator scene scale where the valve assembly spans approximately 0.8m:

| LOD level | Detail | Switch-in distance |
|-----------|--------|--------------------|
| LOD3 | Close inspection | < 2m from camera |
| LOD2 | Normal interaction | 2–5m |
| LOD1 | Mid-range | 5–12m |
| LOD0 | Distant / mobile | > 12m |

---

## Per-Object Face Count Budgets

Face counts for primary LOTO objects. "Close-up" means LOD2/LOD3. These are target maximums — use fewer faces where the visual result is acceptable.

| Object | LOD0 | LOD1 | LOD2 | LOD3 |
|--------|------|------|------|------|
| Valve handwheel | 80 | 400 | 1200 | 3200 |
| Valve body + stem | 60 | 280 | 900 | 2400 |
| Pipe assembly | 40 | 200 | 600 | 1600 |
| Hasp body | 50 | 240 | 750 | 2000 |
| Padlock body | 60 | 320 | 1000 | 2800 |
| Padlock shackle | 20 | 120 | 380 | 1000 |
| Pressure gauge | 30 | 160 | 500 | 1400 |
| Gauge glass | 8 | 40 | 120 | 320 |
| Safety tag | 6 | 20 | 60 | 160 |
| Bleed valve | 30 | 150 | 480 | 1300 |

Total LOTO scene face budget (all objects combined):

| Tier | Max faces |
|------|-----------|
| MINIMUM | < 500 |
| HD (LOD1) | < 2,000 |
| HD_PLUS (LOD2) | < 8,000 |
| UHD (LOD3) | < 20,000 |

---

## Texture Budget per Object

Texture sizes for primary objects. One texture set = all PBR channels (base color, metalness, roughness, normal, AO). Each texture channel uses this size.

| Object | MINIMUM | HD | HD_PLUS | UHD |
|--------|---------|----|---------|-----|
| Valve assembly (body + handwheel) | 256 | 512 | 1024 | 2048 |
| Hasp | 256 | 512 | 1024 | 2048 |
| Padlock | 256 | 512 | 1024 | 2048 |
| Pipe assembly | 128 | 256 | 512 | 1024 |
| Gauge | 128 | 256 | 512 | 1024 |
| Safety tag | 128 | 256 | 256 | 512 |
| Environment / floor | 256 | 512 | 1024 | 2048 |

Texture atlas strategy: where objects share material properties (e.g. all steel hardware), pack their textures into a shared atlas to reduce draw calls and VRAM fragmentation.

---

## Performance Targets by Hardware Tier

| Hardware | FPS target | Active objects | Physics bodies | Quality tier |
|----------|-----------|----------------|---------------|--------------|
| High-end desktop | 60 fps | Up to 5,000 | Up to 200 | HD_PLUS / UHD |
| Mid-range desktop | 45 fps | LOD-aggressive | 100 | HD |
| Low-end / tablet | 30 fps | Kinematic fallback | Kinematic only | MINIMUM |

Kinematic fallback: on low-end hardware, physics bodies are replaced with kinematic animation only — no constraint solving. The step validation logic still runs (distance checks, angle checks) but through animation state rather than physics simulation. Assessment accuracy is maintained; only the physical feel changes.

---

## Capability Detection

Detect hardware capability at session start. Do not ask the user to choose a quality setting — autodetect and inform them if a downgrade was applied.

```javascript
async function detectQualityTier(renderer) {
  const gl = renderer.getContext();
  const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');

  const caps = {
    maxTextureSize:    gl.getParameter(gl.MAX_TEXTURE_SIZE),
    maxVertexUniforms: gl.getParameter(gl.MAX_VERTEX_UNIFORM_VECTORS),
    webgl2:            gl instanceof WebGL2RenderingContext,
    floatTextures:     !!gl.getExtension('OES_texture_float')
  };

  // Rough heuristic — refine based on observed performance after first 5 seconds
  if (caps.maxTextureSize >= 8192 && caps.webgl2) {
    return 'HD_PLUS';
  } else if (caps.maxTextureSize >= 4096 && caps.webgl2) {
    return 'HD';
  } else {
    return 'MINIMUM';
  }
}
```

After the first 5 seconds of rendering, use the actual observed frame time average (from `webgl-renderer-baseline` adaptive logic) to confirm or override the initial tier detection.

---

## Instancing

Use `THREE.InstancedMesh` for repeated geometry: bolt heads, warning labels, pipe segments. Even if only 4–6 instances exist, instancing reduces draw calls.

```javascript
function createInstancedBolts(boltGeometry, boltMaterial, positions) {
  const mesh = new THREE.InstancedMesh(boltGeometry, boltMaterial, positions.length);
  const matrix = new THREE.Matrix4();

  positions.forEach((pos, i) => {
    matrix.setPosition(pos.x, pos.y, pos.z);
    mesh.setMatrixAt(i, matrix);
  });
  mesh.instanceMatrix.needsUpdate = true;
  return mesh;
}
```

---

## Frustum Culling

Three.js frustum culling is automatic — do not disable it. Ensure all objects have correct `boundingBox` or `boundingSphere` set. Objects with incorrect or missing bounding volumes are not correctly culled.

```javascript
function prepareGeometryForCulling(geometry) {
  geometry.computeBoundingBox();
  geometry.computeBoundingSphere();
}
```

For the HUD overlay elements (HTML/CSS layer), culling does not apply — they are always rendered. Keep the HUD element count low (< 20 DOM elements active at once during simulation).

---

## Asset Loading Strategy

Use a two-phase loading approach to achieve the startup target of <= 5 seconds to first interaction (PRD Section 10.2):

Phase 1 (blocking — must complete before scene renders):
- LOD1/LOD2 geometry for primary interactive objects (valve, hasp, padlock)
- HD textures for primary objects
- HDRI 2k fallback
- Physics world initialisation

Phase 2 (non-blocking — loads in background):
- LOD3 geometry upgrades
- 4k/8k HDRI upgrades
- Secondary scene objects (pipes, fixtures, background)
- Failure-state effect assets

```javascript
async function loadSceneAssets(qualityTier, onProgress) {
  // Phase 1 — blocking
  const [primaryGeometry, primaryTextures, hdri] = await Promise.all([
    loadPrimaryGeometry(qualityTier),
    loadPrimaryTextures(qualityTier),
    loadEnvironment(renderer, scene, Math.min(qualityTier, 'HD'))  // cap at HD for phase 1
  ]);
  onProgress(0.7);  // 70% complete — scene can render

  // Phase 2 — non-blocking upgrades
  setTimeout(async () => {
    await loadSecondaryAssets(qualityTier);
    await upgradeHDRIIfNeeded(qualityTier);
    onProgress(1.0);
  }, 0);

  return { primaryGeometry, primaryTextures };
}
```

---

## What Not To Do

- Do not exceed the face count budgets for any LOD level
- Do not disable Three.js frustum culling
- Do not load all assets before rendering — use the two-phase loading strategy
- Do not apply LOD3 detail at distances > 2m — it wastes GPU budget
- Do not use a single geometry for all LOD levels (no LOD = always LOD3 = MINIMUM tier unusable)
- Do not set texture sizes above the tier maximum — it pushes VRAM over ceiling on constrained devices
- Do not skip `geometry.computeBoundingBox()` — invisible objects that should be culled will still be rendered
- Do not use physics constraints on low-end/mobile — use kinematic fallback
