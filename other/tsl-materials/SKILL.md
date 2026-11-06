---
name: tsl-materials
description: Create physically convincing custom materials and shaders with Three.js TSL node materials on WebGPU. Use as the parent material/shader skill for glass, water, metal, paint, rust, plastic, concrete, window interiors and other materials.
---

# TSL Materials

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

Prefer reusable TSL node graphs and material functions over monolithic shaders.

## Sibling skills

This is the parent skill. For a particular material, load the matching sibling as well:

- `glass`: windows, windscreens, canopies, portholes, building windows, transparent panels
- `metal`: bare, brushed, cast, galvanised and structural metal
- `paint`: painted surfaces as layered coatings, wear and dirt
- `rust`: oxidation and corrosion as a layered surface transformation
- `water`: lakes, rivers, reservoirs, puddles and wet surfaces
- `material-composition`: combining these into coherent multi-material objects
- `interior-mapping`: fake rooms behind the windows of buildings that cannot be entered

## Material vocabulary

Reason about a material using:

- base colour / diffuse response
- metalness
- specular intensity and colour
- roughness / gloss
- normal perturbation
- micro-normal detail
- clearcoat
- clearcoat roughness
- anisotropy
- transmission
- IOR
- thickness
- attenuation colour and distance
- reflection
- refraction
- Fresnel response
- emission
- iridescence where physically appropriate
- dirt, wear and damage masks

Three.js physical node materials expose many of these properties directly, including transmission, thickness, IOR, clearcoat, anisotropy, dispersion and specular controls.

## Layered thinking

A realistic material is usually a combination of:

1. macro shape
2. base material response
3. microstructure
4. large-scale variation
5. wear/age
6. environmental interaction

Do not add every effect to every material.

## Scale

Separate macro, meso and micro detail.

Macro: colour blocks, corrosion regions, panels, major stains.
Meso: scratches, brushed grain, dents, dirt accumulation.
Micro: fine roughness and normal variation.

Microdetail should not change the silhouette unless explicitly intended.

## Physical plausibility

Use physically meaningful causes for variation. Dirt accumulates in creases, water collects in low areas, paint wears at exposed edges, polished metal has directional highlights, and rough surfaces produce broader reflections.

Do not use procedural noise merely because it looks interesting.

## Performance

Prefer inexpensive procedural nodes for broad variation. Reuse nodes/material functions. Avoid unnecessary texture samples and expensive loops. Keep high-frequency effects subtle and screen-space aware.

Use environment lighting/reflections where a material depends on reflected surroundings.

## API style

Prefer reusable ES module functions such as:

createMetalMaterial()
createPaintMaterial()
createGlassMaterial()
createWaterMaterial()
createRustMaterial()

Expose meaningful parameters rather than dozens of low-level shader controls. Keep live values in uniforms so they can change without recompiling the material.

```js
import * as THREE from 'three/webgpu';
import { uniform, float, positionWorld, mx_fractal_noise_float } from 'three/tsl';

// Moulded plastic with broad, world-anchored tone variation.
export function createPlasticMaterial({
  color = 0x3a6ea5, roughness = 0.45, variation = 0.08, scale = 0.6, coat = 0.2,
} = {}) {
  const base = uniform(new THREE.Color(color));
  const amount = uniform(variation);
  const n = mx_fractal_noise_float(positionWorld.mul(scale));   // roughly -1..1

  const material = new THREE.MeshPhysicalNodeMaterial({
    metalness: 0, clearcoat: coat, clearcoatRoughness: 0.3,
  });
  material.colorNode = base.mul(n.mul(amount).add(1.0));
  material.roughnessNode = float(roughness).add(n.mul(0.05)).clamp(0.02, 1.0);
  material.userData.uniforms = { base, amount };                // live controls
  return material;
}
```

Share one material between every mesh that looks the same; make a second only when the parameters differ.
