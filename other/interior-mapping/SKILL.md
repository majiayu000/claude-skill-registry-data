---
name: interior-mapping
description: Fake rooms behind the windows of buildings that cannot be entered, with a layered-parallax TSL window material on WebGPU. Use for facades with many windows, city blocks, distant buildings and night-time window lights.
---

# Interior Mapping

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

The companion file `scripts/windowMaterial.tsl.js` is the material. Copy it into the project; it imports only from `three/webgpu` and `three/tsl`.

## What it is

A flat pane whose shader draws what you would see through a window: a frame and glazing bars, then blinds, curtains or net curtains a few centimetres behind the glass, then a blurred room behind them (a back wall with a doorway or far window, dark furniture masses on a middle plane). Each layer is shifted by the view ray times its depth, so the room moves with parallax as the viewer moves. The glass adds a Fresnel reflection of a fake sky, horizon and ground. At night a share of windows have their lights on, warm or cool, glowing through closed blinds. Every window picks its dressing, drop, colour, brightness and light from a seed, so no two are alike.

## When to use it

- windows of buildings that cannot be entered
- many windows: a facade, a street, a city
- far cheaper than modelling rooms and lighting them, and cheaper than transmissive glass

Use real glass (the `glass` skill) for windows the viewer can look through into a modelled space. Model the reveal, sill and frame in geometry around the pane either way; the shader's own frame is the sash and glazing bars inside the opening.

## Options

From `WINDOW_DEFAULTS`, grouped as in the file. Pass any of them to `createWindowMaterial(options)`.

Layout:
- `unitsPerMeter` (1): scene units per metre; 100 for a scene in centimetres
- `grid` ([1, 1]): windows per quad, [cols, rows]; more than 1 means one quad covers a facade
- `idAttribute` (false): read the per-window seed from a float `windowId` attribute

Parallax depths, metres behind the glass:
- `dressingDepth` (0.08): blinds and curtains
- `interiorDepth` (2.2): the back wall; the middle plane sits at 0.38 of it

Interior hint:
- `interiorTint` (0x8f887c): overall colour of the unlit room
- `interiorMap` (null): optional texture, any photo, sampled blurred on the back plane; mirrored tiling reads as a room corner
- `interiorMapBlur` (4): mip bias for the map; higher is blurrier
- `interiorMapSize` (3.0): metres the map spans at the back plane
- `ambient` (0.5): daytime visibility of the room; 0 is black glass

Lights (night):
- `night` (0): 0 day, 1 night; drive it with `setWindowNight()`
- `litRatio` (0.6): share of windows lit at night
- `warm` (0xffb066), `cool` (0x9fc4ff), `coolChance` (0.15): incandescent versus TV/fluorescent
- `lightLevel` (2.2): emissive strength of a lit room
- `transmission` (0.35): how much room light glows through closed blinds and curtains

Dressing (per-window random pick, weights):
- `dressing` ({ venetian: 1, roller: 1, curtains: 1, bare: 1 }); a partial object means only those: `{ venetian: 1 }` puts venetian blinds everywhere
- `sheerChance` (0.35): chance of a net curtain, only behind curtains or bare glass
- `dressingColorA` (0xf2efe6), `dressingColorB` (0xb9ac98): each window blends between them
- `slatPitch` (0.035): venetian slat spacing, metres
- `dropMin` (0.35): blinds are lowered between this and 1 of the window height

Frame:
- `frameWidth` (0.05): metres; 0 disables the frame
- `mullionWidth` (0.035): metres; 0 disables glazing bars
- `panes` ([2, 1]): glazing bars split the window into [cols, rows]
- `frameColor` (0xf4f4f1)

Glass:
- `glassRoughness` (0.06)
- `haze` (0): 0 to 1, a milky or dirty veil; makes the room more nondescript
- `skyColor` (0xbcd4ee), `horizonColor` (0x7f8a8c), `groundColor` (0x4a463f): the fake reflection; head-on the glass mirrors the street opposite, not the sky
- `reflection` (1.0): strength of the fake reflection; set 0 if `scene.environment` is set
- `glassReflectance` (0.1): head-on reflectance; about 0.1 for double glazing, 0.04 for a single pane
- `grazingFade` (1.0): how hard the interior fades into reflection at shallow angles

`seed` (0) reshuffles every window. Extra keys in `options.material` go to the `MeshStandardNodeMaterial` constructor. Live uniforms are on `material.userData.window` (for example `.uWinNight.value`).

## Usage

The pane needs continuous UVs, 0 to 1 across one window (or across the grid). Three ways:

- **one quad per window**: a `PlaneGeometry` the size of the opening; the seed comes from the object's world position
- **one quad per facade** with `grid: [cols, rows]`: one draw, one quad, a whole wall of windows; the seed adds the grid cell. Best when the facade is a regular grid
- **one `InstancedMesh`** of window quads: the seed adds the instance index; or give the geometry a float `windowId` attribute and set `idAttribute: true` for stable ids

```js
import * as THREE from 'three/webgpu';
import { createWindowMaterial, setWindowNight } from './windowMaterial.tsl.js';

const mat = createWindowMaterial({ grid: [10, 6], panes: [2, 2], litRatio: 0.45 });
const facade = new THREE.Mesh(new THREE.PlaneGeometry(14, 18), mat);   // 1.4 m x 3 m per window
facade.position.set(0, 9, -0.12);   // set back from the wall face, behind the reveals
scene.add(facade);

setWindowNight(mat, 1);             // dusk: animate 0 -> 1
```

Set the pane back 5 to 20 cm from the wall face, as real glass is. One material per building style; vary `seed` between buildings that share options.

## Privacy

Keep rooms nondescript: soft tones, masses and light, never legible objects, people or text. The interior is a hint that the building is occupied. For offices and anything that should read as private, raise `haze` or restrict `dressing` to blinds.

## Level of detail

Same shader near and far; nothing pops. The slats and curtain folds already fade to their average before they reach two pixels. Beyond that, once one window is too small to tell its light from its neighbours', draw the mean of all windows instead of the per-window pattern: a medium grey by day and a dim warm glow by night (about `litRatio` times the lamp level, scaled down). Blend by `fwidth` of the window coordinates so the change follows screen size, not a distance switch:

```js
import { uv, fwidth, smoothstep, mix, max, vec3 } from 'three/tsl';

const w = mat.userData.window;
const cells = fwidth(uv().mul(w.uWinGrid));                         // windows per pixel
const far = smoothstep(0.3, 0.7, max(cells.x, cells.y));
const nightMean = w.uWinWarm.mul(w.uWinLitRatio.mul(w.uWinLightLevel).mul(0.12));
const mean = mix(vec3(0.18), nightMean, w.uWinNight);
mat.emissiveNode = mix(mat.emissiveNode, mean, far);               // colour slot still runs first
```

This blend is not in the companion file; add it where facades are seen from far away.

## Pitfalls

- **Clamped or constant coordinates** give zero derivatives: the tangent frame divides by them and returns NaN, and the pane turns black or white. Do not clamp the UVs, do not use degenerate UVs, and if you pass your own `coords` node keep it continuous across the pane.
- **Keep the pane flat.** The tangent frame comes from screen derivatives of position and UV; a curved or bent pane gives a wobbling room. Curve the building, not the window: one flat quad per window on a curved facade.
- **The same shader near and far.** Do not swap to a texture or a different material for distance; the built-in filtering and the `fwidth` blend above are the level of detail.
- The colour slot computes everything and writes the emissive and roughness values for the other slots; if you replace `colorNode`, keep the original node in the graph or the other slots read nothing.
- `scene.environment` set: lower `reflection` to 0 so the fake sky is not added on top of the real one.
