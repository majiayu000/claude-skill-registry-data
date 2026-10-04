---
name: pbr-materials
description: Use this skill whenever creating, configuring, or assigning materials to any object in the Myelin simulator scene. This defines the PBR channel requirements, industrial material realism values, micro-detail layer rules, and the failure state visual library. No flat-shaded materials in production scenes. Load this skill before writing any material, texture, or shading code.
---

This skill defines the material authoring contract for the Myelin simulator. Every primary interactive object and environmental surface must use physically-based rendering (PBR) materials with the channel values and micro-detail requirements specified here. Visual quality is a non-negotiable part of the platform's trust and realism signal — especially for a safety-critical training context.

---

## Core Principle: PBR-First

All primary objects use `THREE.MeshStandardMaterial` or `THREE.MeshPhysicalMaterial`. `MeshPhysicalMaterial` is required when clearcoat, transmission, IOR, or sheen is needed. `MeshBasicMaterial` and `MeshLambertMaterial` are prohibited on interactive training assets.

```javascript
// Standard — use for most metal, painted, and rubber surfaces
const material = new THREE.MeshStandardMaterial({
  map:           baseColorTexture,    // albedo
  metalnessMap:  metalnessTexture,
  roughnessMap:  roughnessTexture,
  normalMap:     normalTexture,
  normalScale:   new THREE.Vector2(1, 1),
  aoMap:         aoTexture,           // ambient occlusion
  aoMapIntensity: 1.0,
  envMapIntensity: 1.0               // HDRI contribution — do not set to 0
});

// Physical — use for glass gauge faces, clearcoated painted surfaces
const physicalMaterial = new THREE.MeshPhysicalMaterial({
  map:             baseColorTexture,
  metalnessMap:    metalnessTexture,
  roughnessMap:    roughnessTexture,
  normalMap:       normalTexture,
  clearcoat:       0.8,
  clearcoatRoughness: 0.15,
  ior:             1.52              // standard glass
});
```

`envMapIntensity` must never be set to 0 on primary objects. The HDRI environment is the primary light source for PBR — zeroing it out collapses the realism.

---

## PBR Channel Requirements

Every primary interactive object must provide all channels marked Required. Channels marked Optional are strongly recommended for close-up quality tiers.

| Channel | Property | Required | Notes |
|---------|----------|----------|-------|
| Base color / albedo | `map` | Yes | sRGB encoding |
| Metalness | `metalnessMap` | Yes | Linear encoding |
| Roughness | `roughnessMap` | Yes | Linear encoding |
| Normal | `normalMap` | Yes | Tangent-space, OpenGL convention |
| Ambient occlusion | `aoMap` | Yes | Baked, linear encoding |
| Emissive | `emissiveMap` | Conditional | Required for indicator lights, warning labels |
| Clearcoat | `clearcoat` scalar | Optional | Painted metal, safety equipment handles |
| Clearcoat roughness | `clearcoatRoughness` | Optional | Pair with clearcoat |
| Transmission | `transmission` | Optional | Glass gauge faces only |
| IOR | `ior` | Optional | Glass (1.52), plastic (1.46), water (1.33) |

Texture encoding rules:
- Base color: load as `THREE.SRGBColorSpace`
- All other maps (metalness, roughness, normal, AO, emissive): load as `THREE.LinearSRGBColorSpace`

```javascript
function loadTexture(path, colorSpace) {
  const loader = new THREE.TextureLoader();
  return new Promise(resolve => {
    loader.load(path, texture => {
      texture.colorSpace = colorSpace;
      texture.anisotropy = renderer.capabilities.getMaxAnisotropy(); // max sharpness at angles
      resolve(texture);
    });
  });
}

// Usage
const baseColor = await loadTexture('/textures/valve/basecolor.jpg', THREE.SRGBColorSpace);
const roughness = await loadTexture('/textures/valve/roughness.jpg',  THREE.LinearSRGBColorSpace);
```

Anisotropy must be set to the hardware maximum on all textures. Un-anisotropic textures blur badly at the oblique viewing angles common in close-up simulator inspection.

---

## Industrial Material Reference Values

These are the starting-point PBR values for each material class. Adjust based on specific wear/age state of the object, but stay within the ranges.

### Cast iron (valve body, pipe flanges)

```javascript
{
  metalness: 0.85,          // mostly metallic
  roughness: 0.70,          // matte — heavily textured casting surface
  color: new THREE.Color(0x2A2A2A),  // dark grey base, adjusted by dirt/rust maps
  // Normal map: coarse casting surface grain, ~1.5–2.0mm feature scale
}
```

### Painted steel (valve handwheel, hasp body)

```javascript
{
  metalness:        0.0,    // paint layer reads as non-metallic
  roughness:        0.55,   // slight sheen — industrial enamel
  clearcoat:        0.4,
  clearcoatRoughness: 0.3,
  color: new THREE.Color(0xC8230A),  // safety red — adjust per actual asset spec
}
```

### Bare steel (hasp shackle, padlock shackle, bolt hardware)

```javascript
{
  metalness: 0.95,
  roughness: 0.35,          // polished but not mirror — machined finish
  color: new THREE.Color(0xB8B8B8)
}
```

### Safety padlock body (zinc alloy body, anodized)

```javascript
{
  metalness: 0.7,
  roughness: 0.45,
  clearcoat: 0.6,
  clearcoatRoughness: 0.2,
  color: new THREE.Color(0xFFCC00)   // safety yellow; brand colour per asset spec
}
```

### Rubber / grip handle (valve handwheel grip wrapping)

```javascript
{
  metalness: 0.0,
  roughness: 0.85,          // matte rubber
  color: new THREE.Color(0x1A1A1A),
  // Normal map: fine grip texture, ~0.5mm knurl pattern
}
```

### Pressure gauge glass face

```javascript
{
  metalness:    0.0,
  roughness:    0.05,       // near-mirror for glass
  transmission: 0.92,       // mostly transparent
  ior:          1.52,
  thickness:    0.003,      // 3mm glass thickness for refraction depth
  color: new THREE.Color(0xFFFFFF)
}
```

### PCB / circuit board surface (for PCB Rework scenario — feature-flagged)

```javascript
{
  metalness: 0.0,
  roughness: 0.65,
  color: new THREE.Color(0x1A3A1A),  // dark green substrate
  // Emissive map for indicator LEDs
  // Normal map: trace pattern relief, solder mask texture
}
```

---

## Micro-Detail Requirements

Micro-detail layers are required on all primary interactive objects at HD quality tier and above. They are the difference between a training-grade simulation and a game asset.

### Scratch layer

Applied as a secondary normal map blended over the primary normal at reduced strength.

```javascript
material.normalMap = primaryNormal;
material.normalScale = new THREE.Vector2(1.0, 1.0);

// Blend scratch detail via detail normal map in custom shader,
// or as a second UV channel normal if the asset supports it.
// Scratch normal strength: 0.15–0.25 (subtle, not dominant)
```

Scratch patterns must follow the geometry's use pattern — circular marks on rotating handwheels, linear marks on valve bodies from tool contact, edge wear on hasp jaws.

### Rust / oxidation layer

Used on aged cast iron and exposed steel in the default scene state. Applied as a roughness/color blend mask — rusted areas have roughness 0.90–0.95 and a brown-orange hue shift.

```javascript
// In the fragment shader or via a roughness variation map:
// Rust mask: white = rust, black = clean metal
// Rust roughness: lerp(baseRoughness, 0.92, rustMask)
// Rust color: lerp(baseColor, vec3(0.45, 0.22, 0.08), rustMask * 0.6)
```

### Swirl marks and fingerprints

Applied to painted metal and polished steel. Concentric circular scratches on handwheel top surface. Fingerprint smears on padlock body.

These are baked into the roughness variation map as subtle light-grey smear patterns. Roughness delta: +0.05 to +0.12 over the base value.

### Wear transfer

Edges of the hasp jaws and padlock shackle holes show wear from repeated locking cycles. Applied as edge-darkening in the AO map and edge-brightening (lower roughness) in the roughness map.

---

## Emissive Materials

Emissive is used for:
- Pressure gauge indicator band (green → amber → red based on pressure value)
- Step indicator lights on the HUD proximity markers
- Warning label fluorescent ink on safety tags

```javascript
function updateGaugeEmissive(material, pressureBar) {
  if (pressureBar < 0.1) {
    material.emissive.setHex(0x003300);     // dim green — zero energy confirmed
    material.emissiveIntensity = 0.4;
  } else if (pressureBar < 2.0) {
    material.emissive.setHex(0x332200);     // amber — residual pressure
    material.emissiveIntensity = 0.6;
  } else {
    material.emissive.setHex(0x330000);     // red — active pressure
    material.emissiveIntensity = 0.8;
  }
}
```

Never set `emissiveIntensity` above 1.0 unless the bloom pass is active (HD_PLUS / UHD tier only). Over-bright emissives on MINIMUM tier produce blown-out artefacts without the bloom pass to tone them.

---

## Failure State Visuals

Trade-specific failure state materials are required for the following events. These are triggered by the state machine — they are not decorative.

### Arc flash (electrical isolation failure)

- Bright cyan-white emissive burst on the isolation point mesh
- Emissive intensity: 3.0–5.0 (requires bloom pass — only trigger on HD_PLUS+)
- Duration: 120ms flash, fade to char mark
- Follow-on: blackened roughness patch (roughness 0.98, metalness 0.1) at the arc point

### Thermal runaway indicator (battery/PCB scenarios)

- Emissive gradient from yellow to red on the component body
- Thin smoke particle system (particle count <= 50 to stay within budget)
- Component roughness increases to 0.95 (heat damage)

### Fluid leak (pressure release without zero-energy verification)

- Translucent spray particle effect from pipe joint
- Particle color: semi-opaque grey-white (steam/water)
- Particle count: <= 80 at HD tier

### Smoke (overheating scenario)

- Slow-rising volumetric-style particle system
- Particle count: <= 60
- Opacity: 0.3–0.6 per particle with additive blending

All failure state effects must be preloaded and ready to trigger — not loaded on demand. Loading latency during a failure event breaks immersion.

---

## Level of Detail (LOD) Material Strategy

At LOD0 and LOD1 (mobile/tablet), use simplified materials:

| LOD | Normal map | Micro-detail | AO | Emissive |
|-----|-----------|-------------|-----|---------|
| LOD0 mobile | Disabled | No | Baked into albedo | Flat color only |
| LOD1 tablet | 512px | No | Separate map | Simple scalar |
| LOD2 desktop | 1024px | Yes | Separate map | Map + scalar |
| LOD3 VR/high | 2048px | Yes (2 layers) | Separate map | Map + dynamic |

See `lod-performance-budget` skill for face count and texture memory budgets per tier.

---

## Texture Loading Strategy

All textures must be loaded non-blocking before the scene renders. Show a loading state — do not render a partially-textured scene.

```javascript
async function loadAllMaterials() {
  const [
    valveMaterial,
    haspMaterial,
    padlockMaterial,
    pipeMaterial,
    gaugeMaterial
  ] = await Promise.all([
    buildValveMaterial(),
    buildHaspMaterial(),
    buildPadlockMaterial(),
    buildPipeMaterial(),
    buildGaugeMaterial()
  ]);

  return { valveMaterial, haspMaterial, padlockMaterial, pipeMaterial, gaugeMaterial };
}
```

Texture assets are loaded in parallel. Do not chain them sequentially — it compounds cold load time. Target: all textures loaded and applied before the first frame is rendered to the learner.

---

## What Not To Do

- Do not use `MeshBasicMaterial` or `MeshLambertMaterial` on any interactive training asset
- Do not set `envMapIntensity` to 0 — it collapses PBR lighting
- Do not load base color textures as `LinearSRGBColorSpace` — they must be `SRGBColorSpace`
- Do not load non-color maps (roughness, normal, AO) as `SRGBColorSpace`
- Do not skip anisotropy setting on textures
- Do not set `emissiveIntensity` above 1.0 on MINIMUM or HD tiers without bloom pass
- Do not trigger failure-state effects from on-demand loaded assets — preload them
- Do not apply micro-detail at LOD0 or LOD1 — budget does not support it
- Do not use flat-shaded geometry on any object visible at close-up inspection angles
