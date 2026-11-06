---
name: indirect-lighting
description: "Baked diffuse global illumination for Three.js WebGPU scenes with the r187 LightProbeGrid (a 3D grid of spherical-harmonic probes, GPU-baked with bounces, applied to every lit material) and LightMapper (bakes that irradiance into a uv1 light map with unwrapUVs). Use for interiors, halls, concourses, under bridges, street canyons and anywhere the sun does not reach but light should: bounce light, colour bleed, ambient that changes from room to room."
---

# Indirect lighting

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`) and TSL node materials (`three/tsl`); WebGPU only, no WebGL fallback, no GLSL strings.

Direct light is the `lighting` skill. This one is what happens after the first bounce: the glow
of a sunlit floor on a ceiling, the colour of a red wall on a white one, the dimness of a corridor
compared to the hall it leaves. Two r187 tools do it, both GPU-resident and both baked, so they
cost almost nothing per frame.

## Two tools

| Tool | What it is | Use for |
| --- | --- | --- |
| `LightProbeGrid` | a `Light` holding a 3D grid of L2 spherical-harmonic probes in one 3D texture; added to the scene it lights every lit node material by position | ambient that changes room to room; moving things (a character, vehicles, instanced facades) lit by the space; the fast default |
| `LightMapper` | bakes an irradiance function into a `uv1` light map, rasterising each mesh in UV space with jittered samples | static architecture that needs crisp bounce detail and the cheapest possible runtime |

The pairing for a hall with a walking character: the grid in the scene for the character and
the instanced things, a light map baked from that same grid for the static walls and floor, and
the static materials told not to read the grid as well (below), so nothing is counted twice.

## LightProbeGrid

```js
import * as THREE from 'three/webgpu';
import { LightProbeGrid } from 'three/addons/lighting/LightProbeGrid.js';
import { LightProbeGridHelper } from 'three/addons/helpers/LightProbeGridHelper.js';

const probes = new LightProbeGrid(23.3, 12.8, 10.5, 10, 7, 7); // size x, y, z in metres; probes per axis
probes.position.set(-0.5, 6, -0.3);                             // centre of the volume
scene.add(probes);

await renderer.init();
renderer.render(scene, camera);                                  // once, so the shadow maps exist
probes.bake(renderer, scene, { cubemapSize: 32, near: 0.05, far: 40, bounces: 1 });

const helper = new LightProbeGridHelper(probes, 0.2);            // one sphere per probe
scene.add(helper);
```

- **Size and spacing.** The constructor takes the full extent and the probe count per axis;
  probes sit at cell centres. The r187 Sponza example covers a 23 x 13 x 10 m hall with
  10 x 7 x 7 probes (about 2.3 x 1.8 x 1.5 m spacing); the light map example covers a
  6 x 5 x 6 m room with 8 x 8 x 8 (0.75 m). Spacing of 1.5 to 3 m indoors, 0.75 m where walls
  and openings are close, 4 to 6 m for a street canyon. Extend the volume half a cell past the
  walls so the probes at the edge are not inside them.
- **Bake options.** `cubemapSize` is the capture face size and must be a multiple of 4 (default
  8; the examples use 32). `near` and `far` are the capture camera planes; `far` must reach the
  far wall (the example uses twice the model's largest extent). `bounces` adds indirect passes,
  each re-capturing the scene lit by the previous pass; 1 is the usual value, 2 for a bright
  white interior.
- **Spread the bake.** `bake` is synchronous GPU work. For a large grid bake 16 probes a frame
  with `start`, `count` and `pass`, finishing a whole pass before raising `pass` for the next
  bounce (ranged calls need `bounces: 0`); the Sponza example does exactly this and keeps the
  helper hidden during captures so its spheres are not baked in. Call `updateBoundingBox()`
  after moving the grid.
- **What the capture sees.** The scene as rendered: shadows must be up to date (one render
  before the first bake; keep the sun's shadow static during the bake), the sky dome and
  `scene.environment` included. Hide what should not bounce (particles, helpers, the character).
  If the sun is the addon `SunLight` rather than a `DirectionalLight`, bracket the bake with
  `replaceSunLights(scene)` and `restoreSunLights` from `LightProbeGridUtils.js`.
- **Strength.** `probes.intensity` scales the result; `probes.visible = false` switches it off
  without disposing. Where grids overlap, the one with the highest `priority` lights the fragment
  (ties go to the most recently created), so a fine grid inside a coarse one needs the higher
  priority.
- **Lives with.** `ClusteredLighting` (the grid is not clustered; it keeps the default path),
  the meshlet pipeline, and the planar mirror (the reflection is lit by the grid too).

## LightMapper

```js
import { LightMapper } from 'three/addons/lighting/LightMapper.js';
import { lightProbeGridIrradiance } from 'three/addons/tsl/lighting/LightProbeGridNode.js';
import { unwrapUVs } from 'three/addons/utils/unwrapUVs.js';

const atlas = unwrapUVs(staticGroup, { resolution: 2048, padding: 3 }); // writes uv1; each mesh gets a new geometry
const mapper = new LightMapper(renderer, atlas.resolution, (position, normal) => lightProbeGridIrradiance(probes, position, normal));
mapper.addObjects(staticMeshes);
mapper.update(16);                                                       // 16 samples at once, or 1 per frame
for (const material of staticMaterials) material.lightMap = mapper.texture;
```

- **UVs.** Every baked mesh needs `uv1`; `unwrapUVs` makes a world-space atlas for a hierarchy
  with `padding` of at least 3 texels (the resolve fills two around each chart). 1024 for a room,
  2048 for a hall, 4096 for a concourse; the atlas is square.
- **Samples.** Probes are deterministic, so 16 samples only antialias the chart edges; the
  example bakes one per frame and shows the map while it fills. At most 256 (half-float
  accumulation). Keep geometry and lighting still while accumulating; `reset()` after moving
  anything.
- **What it stores.** Linear diffuse irradiance in lux, no albedo, no material occlusion, no
  exposure, not divided by pi: exactly what `material.lightMap` expects. Do not put ambient
  occlusion or base colour into the irradiance function; material occlusion is applied once at
  runtime.
- **Direct light in the bake.** `new LightMapper(renderer, size, fn, { lights: [sun] })` adds the
  diffuse part of those lights (shadows included; render them first and freeze them). Then keep
  those lights out of the baked materials' runtime lighting or they count twice.
- **Count nothing twice.** With the grid in the scene, a lightmapped material also reads the
  grid. Give the static materials a lights node without it: `material.lightsNode =
  lights([sun, ...localLights])` from `three/tsl`, or keep the grid out of the scene and use
  light maps for everything static. Not run in this catalog.
- **Not for** skinned or instanced meshes (the instanced facades of `megacity` take the grid),
  or anything that moves.
- **Live preview.** `scenePass.contextNode = builtinGIContext(float(1), fn(positionWorld,
  normalWorld, frame))` evaluates the same irradiance per pixel every frame, for checking the
  grid before baking the map.

## Checklist

1. Build the static geometry and the fixtures; place the sun; render once.
2. Grid: extent half a cell past the walls, 1.5 to 3 m spacing, `cubemapSize` 32, `far` past
   the far wall, one bounce. Show the helper, look at it, hide it.
3. If the walls need detail: unwrap at 2048 with padding 3, bake 16 samples from the grid,
   set the light maps, remove the grid from those materials' lights.
4. Remove the hemisphere light indoors; the room is the fill now.
5. Dispose both (`probes.dispose()`, `mapper.dispose()`) when the area is unloaded.

Not run in this catalog; the sizes and counts are the r187 examples' settings.
