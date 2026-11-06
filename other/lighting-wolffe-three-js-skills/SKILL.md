---
name: lighting
description: "Light a Three.js WebGPU scene: sun and sky fill, fixtures versus emission, point and spot light budgets, and r187 ClusteredLighting for streets, halls, stations and interiors with hundreds or thousands of point and spot lights. Use when a scene has more than a handful of lights, when fixtures must read as lit, or when deciding what is a real light and what is only an emissive surface."
---

# Lighting

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`) and TSL node materials (`three/tsl`); WebGPU only, no WebGL fallback, no GLSL strings.

This is the general light skill: what lights a scene, what only looks lit, and how many lights
the renderer can carry. Bounce light and probe grids are `indirect-lighting`; the sky, the sun's
direction and the environment map come from `photo-sky`; far terrain shade is `far-shade`.

## Three layers

Every lit scene has three things that are easy to confuse:

1. **Illumination**: real lights that shade materials. The sun (`DirectionalLight`), the sky fill
   (`HemisphereLight` or `scene.environment`), and local point and spot lights.
2. **Emission**: surfaces that look bright. `emissiveNode` on a node material: tubes, signs,
   windows, indicator lamps. They light nothing. With bloom they glow.
3. **Fixtures**: the geometry that holds the light. Housing, mount, diffuser or lens, cable. A
   fixture has an emissive diffuser and, when its light would be seen on something, a real
   light under it.

Rule: every real light has a visible source, and a visible source gets a real light only when
its light lands on a surface the camera can see. A lamp 60 m down a street lights nothing you
can tell apart from the next lamp: emissive only, and the pavement under it gets its pool from
the baked or probe lighting of `indirect-lighting`.

## Base lighting

- **Sun.** One `DirectionalLight` with the only shadow map that is always on. Direction and
  tint from `photo-sky` (elevation drives the colour; overcast pulls it toward white and down).
  Shadow camera shrink-wrapped to the built area, `shadow.normalBias` about 0.05 at city scale,
  `shadow.autoUpdate = false` for static scenes with `needsUpdate = true` when something moves.
- **Sky fill.** Outdoors, `scene.environment` from the sky's PMREM carries the fill and the
  reflections; a `HemisphereLight` is the cheap stand-in (the r187 city example uses sky
  0x7189b5, ground 0x182038, intensity 0.8 under a night sky). Indoors neither is right: the
  fill should come from the room, which is the probe grid.
- **Ratios, not absolutes.** Intensities are photometric (lux for the sun, candela for point and
  spot lights) but what the camera sees is set by tone mapping and exposure, so keep the ratios:
  sky fill 0.2 to 0.4 of the sun on a clear day, up to 1:1 overcast, and local lights that read
  as pools, not as a second sun.

## Local lights

Point and spot lights are the fixtures that matter: entrances, under bridges, platform edges,
signs that light the pavement, headlamps, the row of street lamps nearest the camera.

- **Always set `distance`.** It is the cutoff radius of the light's sphere and, under clustered
  lighting, its bounding volume. A light with `distance = 0` is unbounded and is tested in
  every cluster of every slice. Set it to the visible throw of the fixture: 6 m for a wall lamp,
  10 to 12 m for a street lamp, 2 m for a desk lamp. Keep `decay` at 2 (inverse square).
- **Spot lights** take `angle`, `penumbra` and a `target`. Narrow cones (`Math.PI / 7`) for
  downlights and entrance washes, wide ones (`Math.PI / 4`) for street lamps and floodlights;
  `penumbra` 0.45 reads as a diffuser.
- **The r187 city example's values**, as a starting point under `NeutralToneMapping`: facade
  point lights 24 cd at 6 m, upper floors 10 cd, street rows 55 cd at 10 m; facade spots 180 cd
  at 10 m with a `Math.PI / 7` cone; street spots 320 cd at 12 m with `Math.PI / 4`; penumbra
  0.45 on all. Emissive windows and neon are `MeshBasicNodeMaterial` with colour (3, 3, 3) under
  `bloom(sceneColor, 0.3, 0.5, 1)`.
- **Shadows** are for the sun and at most a few hero spots. A spot with `castShadow` costs a
  shadow pass and, under clustered lighting, leaves the cluster path (below).
- **Flicker and life.** Modulate `intensity` from a stored base, never accumulate:
  `light.intensity = base * (0.55 + 0.45 * Math.sin(t * 2.5 + phase * 2) ** 2)` is the
  example's; keep the phase per light so a street does not pulse in unison.

## Clustered lighting (r187)

The default lighting system evaluates every light in every fragment, which caps a scene at a
few dozen point and spot lights. `ClusteredLighting` is Forward+ clustered shading: a compute
pass splits the view frustum into screen tiles by exponential depth slices and lists, per
cluster, only the lights whose spheres reach it; each fragment then loops over its own cluster's
list. The r187 city example runs 1024 point lights and 512 spot lights this way.

```js
import * as THREE from 'three/webgpu';
import { ClusteredLighting } from 'three/addons/lighting/ClusteredLighting.js';

const renderer = new THREE.WebGPURenderer({ antialias: true });
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.lighting = new ClusteredLighting(2048);   // before the first render; maxLights
await renderer.init();
```

Constructor: `maxLights` (1024), `tileSize` in pixels (32), `zSlices` (24),
`maxLightsPerCluster` (64).

- **What is clustered.** `PointLight` and `SpotLight` without `castShadow`, without a
  `colorNode`, and spots without a projected `map`. Lights with their own node (`IESSpotLight`,
  `ProjectorLight`), the sun, hemisphere lights, probe grids and any shadowed light keep the
  default path inside the same node, so mixing is free and nothing has to be rewritten.
- **The silent fallbacks.** Setting `castShadow` or `colorNode` on a clustered light moves it
  to the per-fragment path; do that to a hundred lights and the shader is back where it
  started. Keep shadows on the sun and a handful of spots.
- **Capacity.** `maxLights` is the storage size; raise it before adding the lights. Each
  cluster lists at most `maxLightsPerCluster` lights, so where many short cutoffs overlap one
  32-pixel tile at one depth (a wall of fixtures seen close) raise it, or shorten the cutoffs
  so fewer spheres overlap.
- **Cost.** One compute pass per render (the cluster assignment) plus the fragment loop over the
  cluster's list. Smaller tiles and more slices tighten the lists and cost more in the compute
  pass; 32 px and 24 slices are the tested defaults.
- **Nested renders.** A scene rendered inside its own render (the `ocean-water` mirror) gets its
  own cluster node per depth, so the reflection is lit correctly and does not overwrite the
  outer render's cluster data.
- **Lights must be in the scene graph** and visible; lights are collected per render list.
  Hiding a fixture's group hides its light.

## Placement rules of thumb

From lighting design, not measured in this catalog; use them to lay out fixtures before tuning.

| Place | Rule |
| --- | --- |
| street lamps | mounting height 8 to 12 m, spacing 3 to 4 times the height, staggered on a two-sided road |
| platform and concourse | continuous linear fixtures in lines 3 to 4 m apart across, 2.6 to 3.2 m up, ending at the platform edge line |
| entrance | one downlight or wash per door leaf, 0.3 to 0.5 m out from the facade |
| under bridge or canopy | a fixture every 6 to 8 m along, on the soffit, pointing down and slightly out |
| emergency and exit | small, green or white, at every door and change of direction, emissive only |
| vehicle | headlamps are spots (`Math.PI / 6`, 30 m), tail and marker lamps are emissive only |

## Pitfalls

- **A city of unique lights.** Every light is a uniform update per frame even when clustered.
  Instance the fixture geometry, and let far fixtures be emissive only.
- **Double fill indoors.** A hemisphere light plus a probe grid plus `scene.environment` washes
  a hall flat. Indoors: sun through the openings, local lights, the probe grid, nothing else.
- **Bloom as lighting.** Bloom makes emissive surfaces glow; it does not light the floor under
  them. If the pavement must be lit, there is a real light or a baked pool.
- **Tone mapping last.** Pick the tone mapping before tuning intensities; changing it afterwards
  retunes every light.
