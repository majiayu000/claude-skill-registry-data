---
name: snow-weather
description: Falling snow, blizzards, rain-or-snow weather spells and wheel spray for open-world Three.js scenes on WebGPU. Use when a scene needs snowfall from calm drift to whiteout around a moving camera, a weather scheduler (clear, overcast, snow or rain, wet ground), ground powder gusts, vehicle spray, or surfaces that carry snow.
---

# Snow and weather

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

Two companion files in this folder. Copy them into the project:

- `scripts/blizzard.tsl.js`: `SnowField`, a GPU compute snowfall, and `softAlphaAt`, a soft-particle helper. Imports only `three/webgpu` and `three/tsl`.
- `scripts/weather-spells.js`: `WeatherSpells`, the CPU scheduler. Plain JS, no imports.

## What it is

- **SnowField.** Up to 64k flakes in a square box (160 x 160 x 18 m by default) around the camera's ground point. One compute pass and one instanced sprite draw. Flakes wrap toroidally in x/z, so the field follows the camera with no spawn band. Each flake chases a target velocity: wind x height shear x two gust fronts, plus fall, plus two octaves of trig turbulence, plus a per-flake swing. It fades in the last 0.15 m before the ground, never shows inside an optional camera bubble or inside exclusion boxes (vehicles), and is lit by the scene light with a floor. Opacity and density are driven separately. A built-in squall clock adds whiteouts. An ash variant turns the same flakes dark.
- **WeatherSpells.** Spells of calm, steady or storm character, picked by weight. Each eases a `snowing` scalar through a cloud gate. A caller-supplied `winter` value decides rain or snow, never both. Also: a wetness integrator, high-key `bright` spells, ground gusts, a powder opacity, and a generic scripted event (wind and ash ramps).

## When to use it

- A camera moving through open country in snow or rain: driving, flying low, walking.
- Weather that changes over minutes and is read by other systems: sky, fog, lighting, wet roads, audio.
- Do not use it for a fixed diorama with a static camera. A few hundred CPU sprites are enough there.

## SnowField API

`new SnowField(renderer, scene, options)`. Options come from `SNOW_DEFAULTS`:

Field:
- `capacity` (64000): buffer size, about 2.8 MB at 64k; at least the largest mode count
- `count` (60000): drawn prefix, which is also the dispatch size. You pay for all of it whatever the density
- `radius` (80): half-width of the wrapped box, m
- `ceiling` (18): slab height above the ground point, m
- `killBelow` (30): flakes this far under the ground point are reborn
- `groundAt` (null): `(x, z) => y` under the camera. Null means 0
- `teleport` (150): a camera jump of more than this many metres reseeds the field

Look:
- `size` (0.8): flake size multiplier on a base of 0.018 to 0.118 m (r^2 distribution)
- `colorSlow` (0xccdbf7), `colorFast` (0xffffff): blended by flake speed from 2 to 20 m/s. Off-white, not blue
- `ashColor` (0x2b2624), `lightFloor` (0.34), `ashLightFloor` (0.5)
- `softDistance` (0.15): soft fade before the ground, m. Live as `field.uSoft.value`
- `hideBelow` (0.03): below this envelope the mesh is hidden and no compute runs
- `renderOrder` (2)

Camera bubble: `bubbleInner` (0.9), `bubbleOuter` (1.4) m around the camera.
Exclusion boxes: `maxBoxes` (4). Each box adds one oriented-box test per fragment.
Squalls: `squalls` (true), `squallWind` (12 m/s), `squallFirst` ([45, 135] s), `squallLength` ([15, 20]), `squallLull` ([60, 180]), `squallMinWinter` (0.55), `squallIn` (0.7/s, blows in over about 3 s), `squallOut` (0.45/s, dies over about 5 s).

Methods:
- `await init(camera)`: warms both compute pipelines. Also warm the sprite pipeline: make the mesh visible during one `renderer.compileAsync(scene, camera)` with no render target set, then hide it (see Warm-up under Performance).
- `update(dt, camera, { envelope, drive: { density, fall, turbulence }, wind: { speed, dir, gustAmp }, gust, ash, winter })`: call once per frame. `WeatherSpells.snowFieldInput(field.count)` builds this object.
- `setLight(color, intensity = 1)`, `setCameraBubble(on)`, `setExclusionBoxes([{ position, forward, size: [length, height, width] }])` (full metres; `forward` is planar; call every frame for moving boxes), `dispose()`.
- `triggerSquall()`, `slam()` (send one hard gust front through now), `whiteout` (the squall envelope 0..1), `envelope` (the opacity used last frame), `size` getter/setter.

`softAlphaAt(alpha, distance, viewZ, varyingName)` returns alpha faded over the last `distance` m in front of the depth buffer. `softParticlesOn.value` = 0 or 1 switches the fade off and on for A/B tests.

## WeatherSpells API

`new WeatherSpells(options)`. Options come from `SPELL_DEFAULTS`:

- `modes` (`SPELL_MODES`): `{ name, weight, intensity: [lo, hi], fall, wind, gust, count, turb, swing?, bright? }`. Defaults:
  calm w3, 0.28-0.42, fall 3, wind 0.5, count 16k; steady w3, 0.50-0.68, fall 6, wind 1.8, count 32k, turb 0.4;
  storm w1, 0.90-1.00, fall 14, wind 16, gust 7, count 64k, turb 5.5, swing 1.4 rad
- `firstSpell` ([25, 70] s), `spellLength` ([90, 270]), `clearLength` ([140, 420])
- `cloudIn` (30 s), `cloudOut` (45 s), `cloudGate` ([0.4, 0.85]), `fallRate` (0.12/s)
- `shareBand` ([0.45, 0.55]), `wetIn` (20 s), `dryOut` (45 s), `brightChance` (0.4)
- `powderFloor` (0.32), `powderGain` (0.2), `powderCap` (0.5)
- `gustStrength` ([6, 14] m/s), `gustLength` ([2.5, 5.5] s), `gustLull` ([16, 52] s), `firstGust` ([6, 16]), `gustSpread` (1.2 rad)
- `onSpell(mode | null)`, `onEvent(phaseName | null)`: hooks

Per frame, call `update(dt, { winter })`. Readouts: `snowing`, `cloud`, `snowShare`, `rain`, `rainWet`, `bright`, `powderOpacity`, `gust` (`{ dir, strength, t, dur }` or null), `gustEnvelope`, `windDir`, `wind`, `gustAmp`, `fall`, `turbulence`, `count`, `mode`, `stormy`, `ash`, `eventWind`.
Control: `setMode(name)` and `force(target)` both hold until `release(seconds)`. `startEvent([{ name, dur, wind: [from, to], ash: [from, to], rate }])` runs scripted phases: for example a warning with rising wind, then a blast, then an aftermath of falling ash.

## How it works

**Compute.** Seven storage buffers: position, velocity, seed, age, life, size and alpha. The init pass fills the whole volume with scattered ages, so lifecycles never march in step. Each step of the update pass:
- Two Gaussian gust bands sweep along the wind axis between -radius and +radius at 13-31 m/s, and recycle when they leave.
- Height shear: wind speed x (0.62 + 0.055 y).
- Each flake chases the target velocity at its own rate of 1.1 to 4.5 per second. This spread is the main source of the chaotic look.
- Positions wrap with `rel - span * floor((rel + R) / span)`.
- A flake dies at the end of its life (2.5-9 s), above `ceiling + 8`, or below `killBelow`. It is reborn somewhere random in the volume.
- Births hug the ground (r^2 height) when the wind is strong or a squall is on.

**Density versus opacity.** Opacity is `envelope` = max(squall, spell x snowShare, ash x 0.9), and it applies at once. Density is a rebirth gate: at each birth a flake rolls against `density` and, if it loses, lives at size 0 for that life. Density therefore takes a lifetime to change, which means no pops. It also means density must lead: open it from the squall clock, not from the eased envelope, or a squall arrives see-through.

**Cloud gate.** The cloud deck eases toward 1 with a 30 s time constant as soon as a spell is scheduled. `snowing` follows `target x smoothstep(0.4, 0.85, cloud)`, so the sky closes about 30 s before flakes are visible. When the spell ends, the deck opens with a 45 s time constant. Feed `cloud` (or max(cloud, snowing, field.whiteout)) to the sky and the lighting.

**Rain or snow.** `snowShare = smoothstep(0.45, 0.55, winter)`, `rain = snowing x (1 - snowShare)`, and the flakes are multiplied by `snowShare`. Squalls need `winter >= 0.55`. `rainWet` eases up toward `rain` with a 20 s time constant and dries with 45 s. It drives sheen, puddles, spray and grip.

**Gusts.** A ground gust (6-14 m/s, 2.5-5.5 s, lulls of 16-52 s) is one object. The field edge-detects a new object and launches gust front B at a strength-scaled speed. A powder system sweeps along the gust's heading.

## Usage

```js
import * as THREE from 'three/webgpu';
import { SnowField } from './blizzard.tsl.js';
import { WeatherSpells } from './weather-spells.js';

const spells = new WeatherSpells();
const snow = new SnowField(renderer, scene, { groundAt: (x, z) => terrain.heightAt(x, z) });
await snow.init(camera);
const flakeLight = new THREE.Color();

function frame(dt) {
  // 1. climate at the viewer (or vehicle), 1 = snowfields, 0 = temperate
  spells.update(dt, { winter: climateWinterAt(vehicle.position) });
  // 2. the sky and lighting read the weather BEFORE the lights are set this frame
  const overcast = Math.max(spells.snowing, snow.whiteout); // lighting; the cloud LAYER reads max(overcast, spells.cloud)
  updateSkyAndLights(dt, overcast, spells.bright);
  // 3. flakes take the scene light: hemi x 0.65 + sun x 0.3, clamped
  flakeLight.setRGB(
    Math.min(1, hemi.color.r * hemi.intensity * 0.65 + sun.color.r * sun.intensity * 0.3),
    Math.min(1, hemi.color.g * hemi.intensity * 0.65 + sun.color.g * sun.intensity * 0.3),
    Math.min(1, hemi.color.b * hemi.intensity * 0.65 + sun.color.b * sun.intensity * 0.3));
  snow.setLight(flakeLight);
  snow.setCameraBubble(cameraMode === 'cabin');
  snow.setExclusionBoxes([{ position: vehicle.bodyCentre, forward: vehicle.forward, size: [5.6, 2.4, 2.4] }]);
  snow.update(dt, camera, spells.snowFieldInput(snow.count));
  // 4. wet materials and powder
  roadMaterial.userData.wet.value = spells.rainWet;
  powder.setOpacity(spells.powderOpacity);
  if (spells.gust) powder.emit(camera, spells.gust.dir, spells.gust.strength * spells.gustEnvelope, dt);
  renderer.render(scene, camera);
}
```

Exclusion boxes should be the body plus a margin. A 4.2 x 2 m car takes about [5.6, 2.4, 2.4], centred 0.2 m above the chassis origin. The mask works from any camera. It hides the flakes but does not stop them, which reads correctly at these flake sizes. Hide `snow.mesh` from reflection passes (mirror and planar water renders).

## Ground powder

Ground powder is spindrift: a swarm of tiny grains (0.05-0.13 m), 0.5-2.2 m above the ground, streaming downwind and following the terrain height. It is not big fog quads, which depth-clip into hard lines against the ground.
- **Emission.** During a gust, emit 260 grains/s scaled by `gustEnvelope`. During a storm between gusts (wind >= 8, snowing > 0.45), emit 150/s. Spawn 6-54 m around the camera, live 4.5 s, and cap the pool at 1600.
- **Opacity.** `powderOpacity` has a floor of 0.32 because gusts blow under clear skies too. It is capped at 0.5 and multiplied by `winter`: no ground snow, no powder.
- **Near the camera.** Grains within 8 m of the camera dissolve fast. Otherwise one crossing the near plane flashes the whole screen.
- **Look.** Use soft particles with a 0.6 m fade and the same light floor as the flakes.

## Spray (wheel sheets, puffs, splashes)

Spray is not shipped as code: emission depends on the vehicle's wheel contacts and surface types. The pattern:
- **One pool.** One `InstancedBufferGeometry` of camera-facing quads (4 shared corners plus per-instance offset, life and kind) and one draw. Pool about 1500. Upload only the slots touched each frame (`updateRanges`).
- **Kinds.**
  - Snow puffs: rate 1.6 x speed x 1.1, x (0.9 + snowing), x winter.
  - Off-road powder: 2.4x bigger, kicked to the wheel's own side.
  - Water sheets: taller than wide (0.95 x 1.65), leaning away from the vehicle, with a noise mass that is dense at the base and breaks into droplets at the top. Rate scales with speed x `rainWet`, with a wet gate at 0.2. Do not raise the gate to 0.4: light showers never reach it.
  - Mist trail: large and faint.
  - Rain splashes.
- **Physics.** Gravity 6 m/s^2, drag 0.92 per 1/60 s, life about 1.1 s. Soft fade 0.3 m against the road, wheels and body.
- **Kill sphere.** From a cabin camera, do not spawn within 2.5 m of the eye. Particles already inside that radius lose life 8x faster. From chase cameras, skip both.
- **Fade box.** Fade every fragment by an oriented box around the seats: view position to world via `cameraWorldMatrix`, then into vehicle space. The box must be WIDER than the cabin (1.45 x 1.3 x 0.75 m half-extents for a car). A box narrower than the cabin lets wheel sheets show through the door glass. Do not use a radius around the eye instead: it also removes the rear-wheel sheets you want to see from inside.
- **Draw order.** Draw the spray after the vehicle's glass and lamp lenses from chase cameras, and before the windscreen tint from the cabin. Equal render orders sort by object centre, and a particle mesh's centre is nowhere near its particles.
- **Rain splashes.** 520/s x rain, on the ground 1.5-10 m around the camera, white discs 3.5-11 cm wide, lasting 0.2 s. On grass they read as snowflakes. If that matters, gate them to wet hard surfaces (road, rock) or tint them by the ground.

Rain streaks: about 5k world-vertical quads in a 48 m box around the camera, falling at 9-12 m/s. They are faint (alpha 0.09-0.18) and 0.2-0.5 m long. Keep them out of a 1 m column around the camera, apply the same vehicle box mask as the flakes, and soft-fade them over 0.25 m.

## How surfaces carry snow

There is one rule for everything that wears a covering: trees, poles, boulders, rock ledges, roofs, guardrails. **The coat never melts; only its colour changes with the climate.** Mix snow, lichen and moss in the shader from the same climate scalars the ground uses: snow where cold, lichen-tan where dry, moss where temperate. Gating the coverage by climate instead leaves bare grey boulders and white skirts standing in green fields. Weather-driven frost on top of the coat (falling snow settling) is gated by `winter`, or snowfall frosts boulders in the south.
- **Masks.** An up-facing mask (`smoothstep` of the normal's y) puts the coat on tops and ledges. A skirt mask (height above the object's ground line) puts it at the base of poles and walls. On cliffs, add a steepness gate (nothing below about 30 degrees, full by 50) or the coat smears over every ordinary hillside.
- **Trees.** Trees take a whole-tree snow load: one per-instance amount that whitens the upward faces of the canopy, scaled per object by the climate at its position (a ceiling such as 0.8, multiplied in the shader).
- **Carrier texture.** When a snow texture carries the coat pattern, recolour it by its luminance (coat colour x lum / lum(snow colour)). Using its blue-white RGB as the carrier turns lichen grey-green.
- **Baked textures.** Never re-bake textures on the CPU when the viewer crosses a snow line. That is a frame hitch every crossing. Put the climate into the shader.

## Pitfalls

- **Rain and snow at once.** `rain = snowing x (1 - winter)` drizzles through northern snowfall. Use the thin `shareBand` crossfade.
- **Precipitation leading the sky.** Flakes under a blue dome look wrong. Gate `snowing` on the cloud deck, and fold `whiteout` into the overcast.
- **Far from the origin**, `sin(worldPos)` jitters. Every trig argument in the compute pass is camera-relative, and the clock resets when the field turns on. Keep both if you edit it.
- **The three.js soft-particle addon reads `positionView`.** On quads placed by a custom `vertexNode` from an offset attribute, that is the zero position stub, and every particle fades to nothing. Pass the real view z to `softAlphaAt`. On a `SpriteNodeMaterial` with `positionNode`, `positionView` is real.
- **Sharing one vertex `Fn` between a `vertexNode` and a varying** hung the shader build at boot. Keep the two separate.
- **No ground clamp on flakes.** A flat skim plane is wrong on slopes. Let the soft fade and death below the ground handle it.
- **Dry-out time.** Keep `dryOut` near 45 s. A 180 s dry-out left a wet road under a clear sky.

## Performance

- **Fragment cost.** Snow is overdraw. 64k flakes at 0.02-0.1 m are cheap per flake, but whiteouts fill the screen. Measure on the weakest GPU you target.
- **The invisible tail.** Below 0.03 envelope the field is hidden and dispatches nothing. An envelope of 0.015 still costs the full compute and draw.
- **Count is fixed.** `count` is paid whatever the density. Lower `count` (not density) to save GPU time, for example 30k on integrated GPUs.
- **Depth copy.** All soft particles share ONE `viewportDepthTexture` node, which means one depth copy per frame (about 0.2-0.4 ms at 1080p). Each new `viewportDepthTexture()` node adds another copy.
- **Exclusion boxes.** Each box adds about 12 ALU per flake fragment. Keep `maxBoxes` to what the scene uses.
- **Warm-up on r187.** `init` warms both compute passes. For the sprite pipeline, make the mesh visible during one `renderer.compileAsync(scene, camera)` with NO render target set, then hide it. r187 keys node builds and render pipelines by the target's attachment state, and the renderer's own framebuffer target (what a null-target compile builds against) matches an RGBA16F scene pass and HalfFloat planar mirrors, so that one sweep covers every pass that draws the flakes; give pass and mirror targets `texture.colorSpace = THREE.LinearSRGBColorSpace` so the pipeline keys match as well (the colour space is part of the key). `compileAsync` builds up to 16 pipelines in parallel and yields every 8 ms. Two traps, both measured: never run two `compileAsync` calls at once (one precompile state on the renderer; the second rejects silently and the call depth leaks), and never compile with a render target set (every queued item re-sets that target and leaves it set between items; frames rendered meanwhile draw into it). Shadow and reflector passes are skipped during precompilation, so their variants still compile on the first real render: do one behind the loader. One open-world game went from 120 s to 42 s of boot, 893 to 500 builds and 226 to 102 pipelines with exactly this.
