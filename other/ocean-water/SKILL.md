---
name: ocean-water
description: Use when a Three.js WebGPU scene needs a large open sea or coast that follows the camera, with planar reflections, depth-coloured water over a real seabed, shore and crest foam, and an underwater view; also when adding a planar mirror (lake, ice, wet floor, a one-layer puddle reflection). Ships `ocean.tsl.js` (class Ocean) and `planar-reflection.js` (class PlanarReflection).
---

# Ocean water

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL
fallback, no GLSL strings.

This is the implementation kit for open water. The principles (reflection vs transmission, depth absorption,
foam placement, scale variants) are in the `water` skill; read that first.

Two companion files, copy them into the project; they import only from `three/webgpu` and `three/tsl`:

- `scripts/ocean.tsl.js`: `class Ocean`, plus `OCEAN_DEFAULTS`, `OCEAN_PRESETS`, `buildWaveSet()`,
  `makeWaterGeometry()`
- `scripts/planar-reflection.js`: `class PlanarReflection`, `planarReflectionSample()`, `PLANAR_REFLECTION_DEFAULTS`

## What it is

One mesh: a sea sheet centred on the camera. The inner disc is a dense uniform grid that carries a Gerstner
wave spectrum; the outer ring is coarse, flat and fogged out to under the far plane. The unlit material does
all the optics itself: a planar reflection from three's `reflector()` (half resolution, rendered once per
frame as a top-level pass, on a layer whitelist), the refracted scene behind the water, Schlick Fresnel
between them, Beer-Lambert absorption through a water column measured against a seabed height tile,
caustics, subsurface glow through crests, a GGX sun/moon glint, layered foam (shore band, crests, breakers,
floating patches, Worley bubbles), a splash of spot lights on the surface, and a separate look from below
the surface. Fog is the scene's fog, the same as the land's.

`PlanarReflection` is the general mirror for anything flat and horizontal that is not the sea: frozen lakes,
still ponds, wet floors, and "capture one layer only" reflections such as a vehicle in road puddles.

## When to use

- a sea or a big lake that reaches the horizon, seen from a vehicle, a walker or a boat
- coasts: the seabed tile makes shallows, shore foam and breakers follow any coastline you give it as a
  height function
- not for small bounded water bodies: use a mesh per lake with `PlanarReflection` and a simple water
  material (see the `water` skill)
- not for a physically simulated sea (FFT, shallow-water solver): this is an analytic sum of waves, cheap
  and deterministic, with CPU-side height queries that match the drawn surface
- screen-space reflections instead of the mirror when the camera is low, the water is seen over a
  short distance and only what is on screen needs to reflect (a harbour from the quay, a river from
  a bridge): the `water` skill, Reflections. The mirror stays for horizon views, where the sky dome
  and the far coast that should reflect are off screen

## Ocean API

```js
const ocean = new Ocean(scene, options);
ocean.update(camera, dt, sunDir);        // clocks, follow camera, sun/moon glint, spots, seabed re-bake
ocean.renderMirror(renderer, camera);    // the reflection pass; returns false while hidden
ocean.surfaceHeightAt(x, z, camX, camZ); // world Y of the water (floaters, buoyancy)
ocean.submersion(camera);                // metres below the surface (> 0 underwater), -1 when hidden
ocean.setReflectionLayers(mask);         // Layers mask of what the sea reflects; null = inherit the camera's
ocean.setSpots([spotA, spotB]);          // THREE.SpotLight list splashed on the water (up to spotSlots)
ocean.setReflectionBoost(pos, 0.2);      // lift the reflection within ~14 m of a point; null = off
ocean.bakeBedNow(x, z);                  // synchronous full seabed bake (boot)
ocean.applyPreset(name); ocean.push(key); ocean.attachGui(lilGuiFolder); ocean.dispose();
ocean.surfaceAt(worldXZ, rLoc);          // TSL: the surface nodes, for layers that ride the water
ocean.shorePhase(depth, xz);             // TSL: the shore wave train's phase (share with surf / wet sand)
```

Live uniforms are in `ocean.u` (`ocean.u.amp.value` etc.); `ocean.mesh` is the sheet, `ocean.mirror` the
reflector node, `ocean.bedTexture` the seabed tile.

### Options (`OCEAN_DEFAULTS`)

- `seed` (0x5eed), `waveCount` (16), `totalAmplitude` (2.35 m), `wavelengths` ([140, 5.5]): the spectrum
- `focus` (null): `{ x, z }` gives ring waves converging on that point; null gives plane waves
- `ringSpread` (15000): ring mode, how far wave centres scatter from `focus` (m)
- `windDir` (0), `dirSpread` (0.6): plane mode, travel direction and spread (radians)
- `sheet` ({ segments: 320, inner: 160, outer: 1700, frac: 0.55 }): grid resolution, dense radius, total
  radius, share of the grid inside the dense radius. `outer` defaults to `fog.far x 1.15` when `fog.far` is
  given
- `seaLevel` (0)
- `heightAt` (null): `(x, z) => height` of the ground; the seabed tile is baked from it. null = bottomless
  sea, no shore effects
- `stamps` (null): `(cx, cz, half) => { domes: [{ x, z, r }], boxes: [{ x, z, yaw, hx, hz }] }`: objects
  stamped into the bed so foam wraps them. Domes (rocks) crest 0.4 m above the water over 1.5 r; boxes
  (hulls, piers) get a 3 m parabolic rim cresting 0.35 m below the water
- `isActive` (null): `(camera) => bool`, polled every 15th update; false hides the sheet and skips the
  mirror (inland)
- `bed` ({ res: 384, extent: 1536, rebakeDistance: 380, rowsPerFrame: 12, deep: 60 }): the seabed tile, 4 m
  per texel; re-baked around the camera when it moves `rebakeDistance`; outside the tile the water reads
  `deep` metres
- `fog` ({ color: 0xbfc8d0, near, far }): `color` is a `THREE.Color` (held by reference) or a TSL uniform
  node you already share with the sky and land; only the colour enters the shader (reflection haze, foam
  light)
- `mirror` ({ resolutionScale: 0.5, layers: null }): reflector resolution and the whitelist mask
- `fade` ({ vertex: [140, 620], detail: [90, 560], haze: [300, 950] }): metres from the camera where
  displacement, ripples/distortion, and the reflection-to-fog haze fade
- `shore` ({ period: 5.4, depthPerLine: 1.6 }): seconds between breakers, still-water metres between breaker
  lines
- `spotSlots` (2), `spotGain` (0.5): spot lights the shader handles, and intensity scale
- `preset` ('Calm coast'), `presets` (extra presets merged in), `params` (overrides on top of the preset)

`params` keys (sliders in `attachGui`): `amplitude`, `choppiness`, `timeScale`, `roughness`, `rippleScale`,
`rippleStrength`, `reflectivity`, `refractDistort`, `specular`, `absorb`, `absorbTint`, `deep`, `shallow`,
`foam`, `crestFoam`, `crestThresh`, `crestSkew`, `shoreFoam`, `shoreFade`, `shoreFadeOn`, `foamScale`,
`floatFoam`, `caustics`, `sss`. Presets: Calm coast (default, deliberately low so bays and lakes on the same
sheet look still), Glassy calm, Coastal breeze, Tropical shallows, Open ocean, Storm swell, Golden hour,
Moonlit, Arctic. Shore-zone uniforms not in the presets: `shoalRef` (10 m), `shoalMax` (1.5), `shoreBend`
(70 m), `shoreWave` (1.5), `breakerPeak` (2), `noiseFilter` (1), `surfGrain` (1).

## PlanarReflection API

```js
const mirror = new PlanarReflection(renderer, { size: 512, type: THREE.HalfFloatType });
mirror.render(scene, camera, planeY, hide = [], layer = null);
const { color } = planarReflectionSample(mirror, normal.xz.mul(0.03)); // TSL, in the receiving material
```

`render` reflects the camera about `y = planeY`, clips everything below the plane with an oblique near
plane, and renders into `mirror.rt`. `hide` is switched off for the pass (the mirror surface itself,
anything that samples `mirror.rt`, particles). `layer` set: only that layer is rendered over a transparent
clear with `scene.background` dropped, so the target's alpha is the mask of the reflected objects; blend
with it. `mirror.textureMatrix` maps world positions to the target; `planarReflectionSample` reads it
through a uniform that references the matrix, so no copy per frame.

## How it works

- **Spectrum.** `buildWaveSet` makes a geometric series of wavelengths from swell to chop, amplitude
  proportional to `(L / Lmax)^0.85` with seeded jitter, phases seeded, and the sum normalised to
  `totalAmplitude`; `params.amplitude` scales it live. Wave constants bake into the shader (the sum
  unrolls); only per-wave clocks are uniforms, `(k c t) mod 2 pi` wrapped on the CPU. Deep-water speed `c =
  sqrt(g / k)`.
- **Ring waves.** With `focus`, each wave converges on its own centre near the focus (phase `-k |x - c_i|`),
  so every coast of an island gets onshore waves at slightly different angles. Plane waves around one wind
  direction leave lee coasts with waves running away from the beach.
- **Gerstner with analytic frame.** Displacement, tangent, binormal and fold (sum of `Q A k sin f`) per
  vertex. Each wave fades out where the local cell size passes 0.2 to 0.45 of its wavelength (Nyquist), so
  outer cells never alias.
- **Sheet.** `makeWaterGeometry` warps a plane grid radially: uniform inside `inner`, power 2.2 out to
  `outer`. The origin snaps to the inner cell size each frame, so vertices sit on a fixed world lattice.
  Displacement and the normal fade together by camera distance; the far ring is flat and fogged.
- **Seabed tile.** A half-float red texture of bed heights, baked from `heightAt` plus stamps, a few rows
  per frame, swapped atomically with its origin when complete. The vertex stage reads a smoothed depth (5
  taps, 8 m apart) for shoaling (Green's law, capped), a static shore phase lag (refraction as a delay, `k x
  shoreBend x (1 - sqrt(depth / shoalRef))`), and waves dying to zero at the waterline. The same taps give
  the bed gradient for the shore train.
- **Shore train.** A second wave system whose phase is still-water depth, so crests follow depth contours on
  any coastline; it grows to a break at about 1.4 m depth, peaks (cnoidal), leans shoreward and collapses to
  a bore.
- **Optics.** Ripple normals from four filtered noise octaves; Fresnel `0.02 + 0.98 (1 - NoV)^5`; reflection
  = `reflector()` with uv distorted by the normal, hazed toward the fog colour with distance; refraction =
  `viewportSharedTexture` behind the water; transmittance `exp(-thick x absorb x absorbTint)` plus
  in-scattered `deep`/`shallow` body colour; caustics on the shallows; GGX glint clamped at 12 (no bloom
  assumed); filtered-away ripples are added back as roughness.
- **Foam.** Sampled at the rest position (minus the orbital displacement) so it rides the water. Shore ring
  and contact pulses by column depth; crest foam from the fold, skewed onto the back of the dominant crest
  (`crestSkew`); breaking where height / column exceeds ~0.78; lace from warped fbm; floating patches;
  Worley bubbles shade the interior; the surf zone adds whitewater and a decaying wash. Foam light is
  `max(foamLight, fogColor x 1.1)`.
- **Noise filtering.** Every noise layer fades to its mean by its own frequency against the pixel footprint
  (`fwidth`), not by distance.
- **Underwater.** The sheet is double-sided; back faces draw a Snell window, a dark internal reflection,
  faint foam and a sun glow.
- **Sun and moon.** `update` turns `sunDir` into a glint colour (warmer and weaker low in the sky) and
  switches to the antipode as a dim blue moon once the sun is down.

## Integration

```js
import * as THREE from 'three/webgpu';
import { Ocean } from './ocean.tsl.js';
import { PlanarReflection, planarReflectionSample } from './planar-reflection.js';

const SEA = 4, VEHICLE = 3;                 // layers: the sea-mirror whitelist, the puddle capture
scene.fog = new THREE.Fog(0xbfc8d0, 80, 1400);
const ocean = new Ocean(scene, {
  heightAt: (x, z) => terrain.heightAt(x, z), seaLevel: 0, focus: { x: 0, z: 0 },
  fog: { color: scene.fog.color, far: 1400 },
  isActive: (cam) => terrain.distanceToCoast(cam.position.x, cam.position.z) < 1500,
});
ocean.setReflectionLayers(1 << SEA);
skyDome.layers.enable(SEA); boats.traverse((o) => o.layers.enable(SEA));
for (const l of [sun, hemi]) { l.layers.enable(SEA); l.layers.enable(VEHICLE); } // lights are layer-tested
car.traverse((o) => { o.layers.enable(SEA); o.layers.enable(VEHICLE); });
ocean.setSpots(car.headlights);
ocean.bakeBedNow(camera.position.x, camera.position.z);

const puddles = new PlanarReflection(renderer);   // the car only, in wet-road puddles
roadMaterial.userData.puddleRefl = planarReflectionSample(puddles).color; // blend by .a in the road shader

renderer.setAnimationLoop(() => {
  const dt = clock.getDelta();
  // ...move camera, sun...
  puddles.render(scene, camera, roadYUnderCar, [], VEHICLE); // other mirrors first, top-level
  ocean.update(camera, dt, sunDir);                         // moves the sheet: before its mirror
  ocean.renderMirror(renderer, camera);                     // the sea reflection, top-level, every frame
  renderer.render(scene, camera);                           // the scene pass samples both
});
```

Steps: create the ocean after the terrain (it needs `heightAt`); assign layers to everything the sea should
reflect, lights included; feed `sunDir` (unit vector toward the sun); call the three per-frame calls in that
order; drive underwater fog and audio from `submersion(camera)`; float objects with `surfaceHeightAt` (pass
the camera xz so the fade matches). For a lake mirror, `hide` the ocean mesh and the lake surface itself.

## Surf (layering only, no code here)

Breakers, beach washes and spray are separate layers on top of the sheet, all keyed to the same clock and
the same seabed: a wash mesh per stretch of beach whose vertices call `ocean.surfaceAt()` so it rides the
water exactly, with its run-up driven by `ocean.shorePhase()` at depth 0 and `ocean.u.shoreT`; the terrain's
wet-sand band reads the same phase so wet sand, wash and breakers agree to the frame; spray particles fire
where the shore train breaks (depth ~1.4 m). Keep them off the sea mirror's layer.

## Pitfalls and lessons

- **The mirror must be a top-level pass.** Left to itself, `reflector()` renders from inside the scene
  render when the sea is drawn (a nested pass). Up to r186 nested passes were keyed as their own render
  context (by call depth and target shape), so every material visible in the reflection compiled again
  the first time it was seen there: stalls of hundreds of ms on first sight of a new area. r187 shares
  node builds across call depths (three.js #35014), which removes most of that cost, but the top-level
  pass is still the layout the kit is built around and the whitelist below depends on it. The
  kit wraps `updateBefore` to do nothing unless `renderMirror` is calling it, and `renderMirror` passes a
  hand-made frame `{ scene, camera, renderer, material }`. Call it every frame the sea is visible.
- **Do not alternate mirror frames.** Rendering the reflection every other frame produced a 2:1 frame-time
  judder (27 ms / 15 ms) that read as choppy; it was rejected. Render it every frame and make the pass
  cheaper instead.
- **The whitelist is what pays.** Measured at a coast: mirror pass 12 to 7 ms, 365 to 291 draws, 13M to 11M
  triangles, by reflecting only the sky dome, vehicles, boats, wrecks and structures, and skipping
  terrain, trees, grass, wires, surf and particles. A distance-based geometry diet saved 9 draws and was
  reverted: the reflector already frustum-culls; what survives culling is the near ground, which the
  whitelist removes.
- **The virtual camera is cloned once.** `reflector.getVirtualCamera(camera)` clones the main camera on
  first use and later only refreshes its matrices. The clone inherits whatever layers the main camera had at
  that moment (a later-enabled grass layer leaked into the reflection this way), so `renderMirror` sets the
  mask every call. Lights are layer-tested per pass: a light not on the whitelist layer is missing from the
  reflection.
- **Fog is the scene fog** (`material.fog = true`). A private sea fog with its own range left a dark sea
  sheet under a white land haze in a whiteout. The reflection still gets its own distance haze toward the
  fog colour, because the mirror texture holds clear sky.
- **HalfFloat targets.** `reflector()` renders into HalfFloat; give every `PlanarReflection` HalfFloat too,
  and with a HalfFloat post-processing frame buffer all mirrors and the boot compile land in one render
  context. A different target type is a different context and recompiles everything that appears in it.
- **Never feed unbounded time into shader trig.** f32 loses the phase after minutes; wrap per wave on the CPU.
- **Snap the sheet origin** to the inner cell, or the vertex stage samples the seabed at sliding points and
  shore crests wobble.
- **Branch with `If`, not with a zero multiplier or `select()`.** The spot splash, the underwater path, the
  shore pulse and the surf block are inside `If`; `select()` and `x * 0` evaluate both sides on every water
  pixel.
- **Foam must not go black.** Light foam with `max(sun, fogColor x 1.1)`; at dusk the fog colour is the
  brightest thing in the scene.
- **Stamped box crests stay below the waterline** (-0.35 m); at or above 0 the soft waterline cuts holes in
  the sea beside hulls.
- **Outside the seabed tile force deep water**: the clamped border texel would otherwise paint shallows to
  the horizon.
- **Ring-mode precision.** Phase is `k x distance to centre`; keep `focus` within a few tens of km of play
  (f32 phase error grows with distance). Plane mode uses world xz directly, the same limit applies to very
  large worlds; rebase the world origin if you go past ~50 km.
- `reflectionLayers = null` means the reflection shows everything the camera sees, including the terrain;
  set a mask.
- The sea is `transparent` so it draws after the opaque seabed, which the refraction reads through
  `viewportSharedTexture`; one frame-buffer copy per frame. Each extra `viewportSharedTexture()` node
  elsewhere (glass) is its own copy and render-pass split: share one node.

## Performance

- Cost is three things: the mirror pass (a second scene render at half resolution: the whitelist decides its
  price), the sheet's vertex stage (16 waves x ~103k vertices plus 5 seabed taps), and the fragment stage
  (about 30 noise octaves in the near field, fewer far away as bands fade and `If` blocks skip).
- Bake the seabed off the main thread for big tiles: a worker can compute the heights and the main thread
  only converts rows to half floats; the inline bake (`rowsPerFrame: 12`, ~1.5 ms of `heightAt` per frame
  with a moderate height function) is the fallback.
- Use `isActive` so inland nothing runs: hidden sheet, no mirror, no bake.
- Warm-up on r187: `compileAsync` skips reflector and shadow passes during precompilation, so one real
  `renderMirror` with the sheet forced visible, behind the loader, is still the only way to compile the
  reflection's materials. Everything else the sea draws with comes out of one plain
  `renderer.compileAsync(scene, camera)` with no render target set: builds and pipelines are keyed by the
  target's attachment state, and the renderer's framebuffer target matches the HalfFloat mirror targets once
  those carry `texture.colorSpace = THREE.LinearSRGBColorSpace` (the kit sets it on both mirrors; the colour
  space is part of the pipeline key). Serialise `compileAsync` calls and never compile with a render target
  set; the snow-weather skill's Warm-up note has the two traps and the measurements.
- `resolutionScale` 0.5 is the sweet spot; the normal distortion hides the softness. Keep `bounces: false`
  (the kit sets it).
- `PlanarReflection` at 512 px for a one-layer capture (a vehicle into puddles) is cheap; run it only when
  its strength is above ~0.01 and ease the strength rather than toggling, so a stale target is never read.
- The code has been exercised headless (construction, CPU wave heights, seabed bake, mirror maths) against
  r186, and its imports were re-checked against r187; the TSL fragment graph is a faithful port of a
  shipped shader but compile it once in the target project before relying on it.
