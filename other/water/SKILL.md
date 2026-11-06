---
name: water
description: Create realistic procedural water and wet surfaces with Three.js TSL on WebGPU. Use for lakes, rivers, reservoirs, canals, puddles, drainage, fountains and wet materials.
---

# Water

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

## Water response

Think in terms of:

- reflection
- transmission/refraction
- Fresnel
- depth-dependent absorption
- roughness
- normal waves
- surface displacement
- ripples
- foam
- shoreline effects
- flow direction
- interaction with objects

Do not make all water bright blue.

## Scale-specific variants

Distinguish:

- large reservoir/lake water
- canal/river water
- shallow drainage
- puddles
- fountains
- wet concrete
- wet metal

Each has different wave scale, roughness, depth and reflection behaviour.

## Surface

Use layered wave scales:

- large gentle waves for silhouette and broad reflection
- medium waves for visible surface structure
- small normal-scale ripples for highlights

Do not use high-frequency displacement everywhere.

## Depth

Water should generally become visually deeper with depth. Use attenuation and colour response rather than a flat colour overlay.

## Foam

Place foam where physically plausible:

- shorelines
- obstacles
- strong flow
- turbulence
- waterfalls

Do not distribute foam uniformly.

## Wet surfaces

Wet concrete, rails and metal are not the same thing as standing water. For wet surfaces, primarily alter roughness/specular response and add subtle darkening/reflection rather than turning the entire surface transparent.

## Reflections

Three ways, cheapest first. Pick by what has to appear in the water.

| Need | Use |
| --- | --- |
| the sky and a general sense of surroundings | `scene.environment` only: the PMREM from `photo-sky`; nothing on screen reflects |
| the quay, the boats, the bridge above: what is on screen, seen from a low camera | screen-space reflections (below) |
| a horizon view, the sky dome and a distant coast, exact reflections of hidden geometry | the planar mirror in `ocean-water` (one extra scene render per frame) |

Screen-space reflections on r187 are a post pass fed by a multi-target scene pass. Water is a
dielectric, so `reflectNonMetals: true` is required; without it the pass skips every non-metal
surface and the water stays matte. Ripples reach the reflection only through the normal
attachment, so the water material must write its perturbed normal into `normalNode`.

```js
import * as THREE from 'three/webgpu';
import { pass, mrt, output, normalView, metalness, roughness, packNormalToRGB, unpackRGBToNormal, sample, vec2 } from 'three/tsl';
import { ssr } from 'three/addons/tsl/display/SSRNode.js';

const pipeline = new THREE.RenderPipeline(renderer);
const scenePass = pass(scene, camera);
scenePass.setMRT(mrt({ output, normal: packNormalToRGB(normalView), metalrough: vec2(metalness, roughness) }));
scenePass.getTexture('normal').type = THREE.UnsignedByteType;      // bandwidth; optional
const color = scenePass.getTextureNode('output'), depth = scenePass.getTextureNode('depth');
const normalTex = scenePass.getTextureNode('normal'), mr = scenePass.getTextureNode('metalrough');
const normal = sample((uv) => unpackRGBToNormal(normalTex.sample(uv).rgb));

const reflections = ssr(color, depth, normal, { metalnessNode: mr.r, roughnessNode: mr.g, reflectNonMetals: true });
reflections.maxDistance.value = 1;    // view units a ray may travel; raise for a wide river
reflections.thickness.value = 0.1;    // depth tolerance of a hit
reflections.quality.value = 0.5;      // ray-march steps, 0..1; 0.5 is enough for most scenes
pipeline.outputNode = color.add(reflections.rgb);
// each frame: pipeline.render() instead of renderer.render(scene, camera)
```

- **Roughness is the blur.** The pass blurs by the roughness attachment (`blurQuality` 1 to 3).
  Still water at 0.05 to 0.15 reads as a mirror; wind-ruffled water at 0.3 and above becomes a
  smear, and the mirror in `ocean-water` is cheaper per visible pixel there.
- **Rough water, better.** `stochastic: true` traces GGX rays instead of one mirror ray and needs
  a denoiser: add `velocity` to the MRT and chain `temporalReproject(..., { mode: 'specular',
  accumulate: false })` then `recurrentDenoise(..., { mode: 'specular', accumulate: true })` from
  `three/addons/tsl/display/`, feeding the denoised result back with `setHistory`. This is the
  r187 denoise example; it costs several passes and is for a hero shot, not a default.
- **Limits.** Nothing off screen reflects: the sky beyond the frame, the camera's own side of a
  bridge, the coast behind the viewer. The edge fade (`screenEdgeFade`, 0.2) hides the cut and
  `scene.environment` fills the rest. The `environmentNode` option wants an equirectangular HDR
  with CPU-side pixels, not the PMREM, so it is of no use with `photo-sky`.
- **Material.** Use a `MeshStandardNodeMaterial` or `MeshPhysicalNodeMaterial` for SSR water so
  `metalness` and `roughness` reach the attachment; an unlit sheet gives the pass nothing to work
  with. Not run in this catalog; the values are the r187 example's defaults.
