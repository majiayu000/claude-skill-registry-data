---
name: photo-sky
description: Use when a scene needs a photographic sky that follows a day/night clock and the weather, built from equirectangular sky photos on a camera-following dome (the ATS/ETS2 approach) with TSL on WebGPU. Covers sun-elevation bands, per-day variants, overcast/storm/whiteout and night pools, the photo's sun tracking the clock, crossfades without double-exposed clouds, the ACES inverse, and converting sky photos into dome textures.
---

# Photo Sky

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

Companion files in this folder:
- `scripts/photo-sky.tsl.js`: the sky. Copy it into the project; it imports only from `three/webgpu` and `three/tsl`.
- `scripts/convert-sky.mjs` + `scripts/convert-sky.html`: turn 2:1 sky photos into dome textures and measure each photo's sun. Node 22+ and Chrome, no packages.

## What it is

A back-faced sphere around the camera with one texture slot per sky photo. Every frame, `update()` turns the sun direction, the weather and the night into one weight per slot. The shader blends the weighted photos with a cloud-aware crossfade, inverts three's ACES tone map (so the renderer's ACES gives the photo back unchanged), and then runs a grade: horizon haze, a night or overcast wash, and a storm fold toward the fog colour. The dome turns so each photo's sun column follows the clock's azimuth. A per-slot elevation warp moves each photo's sun row toward the clock's elevation. The clipped sun comes back as HDR (about 8), so a PMREM baked from the dome lights the scene from the right direction.

A photo sky costs a fraction of a procedural sky: one to three texture fetches per pixel and no ray march. A procedural dome with a cloud march measured 2.3 to 5 ms; this one is well under 1 ms. Its limits: clouds do not move, and you can only show the light conditions you have photos of.

## When to use it

- driving, flying or walking scenes with a day/night clock where the sky should look photographed
- when realistic clouds matter more than clouds that move
- when the sky is also the environment map (PMREM) for the scene

Do not use it when clouds must drift or react, when the camera flies through clouds, or for planets and space. Use a procedural sky for those.

## API

```js
import { createPhotoSky, PHOTO_SKY_DEFAULTS, PHOTO_SKY_KNOBS, EXAMPLE_SLOTS, acesInverse, dayHash } from './photo-sky.tsl.js';
const sky = createPhotoSky(options);
// -> { mesh, material, textures, uniforms, slots, knobs, load, setSlotImage, update, bakeGate, needsRebake, bake, state }
```

Options (`PHOTO_SKY_DEFAULTS`):
- `slots` (`EXAMPLE_SLOTS`): one row per texture slot, `{ file, sunElev, sunClear, exp }`. `sunElev` is the photo's sun elevation in degrees from the conversion log, or `null` for no sun. `sunClear` (0..1) is how visible the disc is; it feeds `skyClear`, which gates a lens flare. `exp` is an exposure trim.
- `slotCount` (0): number of texture slots. 0 rounds `slots.length` up to a multiple of 4. Spare slots hold 1x1 placeholders and are ready for new pools.
- `bands` (`[[-6, 2], [2.5, 0], [12, 8], [37, 1]]`): `[elevationDeg, slot]` pairs. A slot shows while the sun is above its elevation and below the next band's. Below `bands[0]` the night slot shows. Bands depend only on elevation, so they are symmetric about noon: sunrise shows the band-0 photo too, which works because dawn and dusk light look the same.
- `roles` (`{ night: 3, aurora: 4, overcast: 5, whiteout: 6, storm: 7, nightOvercast: 9 }`): which slot plays each role. Omit a role or set it to -1 for none. A missing weather slot falls back to whichever weather slot exists, and a missing `nightOvercast` falls back to `night`.
- `pools` (`{}`): per-day variants, `{ slot: [row, row, ...] }`. Each game day picks `pool[dayHash(day, 31 + slot) % n]`.
- `basePath` (''), `loadImage` (ImageLoader + `decode()`): where files come from and how they are loaded.
- `radius` (1700), `segments` ([48, 24]), `anisotropy` (8), `placeholder` ('#8fa3b8').
- `hazeColor` (0xd7dee6): the default grade's target colour. Copy `scene.fog.color` into `sky.uniforms.hazeColor.value` every frame.
- `grade` (null): `(lin, ctx) => vec3` replaces the default grade (see below).
- `knobs` ({}): overrides for `PHOTO_SKY_KNOBS`.

Knobs (`sky.knobs`, read on every `update()`, safe to change live):
- `fadeDeg` 4: half-width of a band crossfade, in degrees of sun elevation. It is capped at 45% of the narrower neighbouring band, so short bands (dawn and dusk are 8 to 10 deg) still reach full weight.
- `fadeSharp` 4: the cloud-aware blend. 0 is a plain dissolve; 8 is harder.
- `warp` 1, `warpMax` 2.2, `warpTop` 80: the elevation warp (see below).
- `storm` 0.85, `overFold` 0.1, `nightFold` 0.3: the storm fold toward the haze colour, and how much of it remains by day and at night once a weather photo carries the deck.
- `nightHaze` 0.15, `stormHaze` 0.1, `hazeEase` 0.8/s: the whole-dome wash. A full wash erases the night photo.
- `weatherFade` 120 s, `auroraFade` 60 s, `rainPick` 0.3, `brightPick` 0.3: the weather and aurora crossfades.
- `exposureRef` 0.86: the clear-day `renderer.toneMappingExposure` the photos are matched to.
- `horizonBand` 0.22, `horizonHaze` 0.95: below `dir.y` 0.22 the horizon converges to the haze colour, so fogged terrain never stands out as a silhouette against the sky.
- `pin` -1: a slot index from 0 up shows that one photo alone, for inspection.
- `rebakeSunY` 0.06, `rebakeWeight` 0.25, `rebakeEvery` 1.5 s: the PMREM re-bake rule.

Per frame:

```js
const { skyClear, weights } = sky.update({
  dt, sunDir,            // seconds; normalised direction TO the sun (y up)
  overcast, rain, bright,// 0..1 eased weather scalars (see Integration)
  aurora,                // 0..1 target; the caller decides when an aurora night happens
  day,                   // integer game day: drives the per-day variant picks
  dayFrac | azimuth,     // optional: azimuth = dayFrac x 2pi or radians; default atan2(sunDir.z, sunDir.x)
  nightShare,            // optional override of the night weight (default: 1 - band 0's ramp)
  exposure,              // optional live renderer.toneMappingExposure (default knobs.exposureRef)
  camera,                // optional: copies its position into the dome
});
```

Other members: `load(day)` loads every slot with the day's pool picks; await it before the first bake. `setSlotImage(i, img, row?)` swaps a slot's image in place. `bakeGate(on)` switches bake mode. `needsRebake()` reports whether the environment needs a re-bake. `bake(pmrem, { renderTarget, sigma 0.04, near, far, size })` renders the dome alone into a PMREM. `uniforms.imgSunDir` is where the photo actually draws its sun; aim a flare or glare at it.

## How it works

**Display-space blend, then an exact ACES inverse.** The photos are tone-mapped JPGs: display-referred, with the sun clipped at 1. Sampling them as sRGB textures gives display-linear values. The shader blends in that space, then solves three's `RRTAndODTFit` quadratic for its positive root, with both ACES matrices inverted on the CPU. The input is clamped to 0.985 first, so a clipped sun returns as about 8 and the PMREM gets a real sun. The result is multiplied by `0.6 / exposure`, because three's ACES scales by `exposure / 0.6` before the curve. The renderer must use `THREE.ACESFilmicToneMapping`; any other curve shifts every colour.

**Rotation.** The converter puts each photo's sun at column 0.5. The shader samples `u = fract(atan(z, x) / 2pi + 0.5 + rotU)` with `rotU = -azimuth / 2pi`, so column 0.5 sits on the sun azimuth and column 0 sits on its antipode. That is why night photos are rotated so their moon sits at column 0: a moon light that rides the sun's antipode then matches the moon in the photo.

**Elevation warp.** For each slot, `warpV` is piecewise linear in elevation and keeps the horizon (0) and the zenith (90 deg) fixed. It moves the photo's sun row eI to a target eT. eT is the clock's elevation, clamped to `[eI / warpMax, min(warpTop, eI x warpMax)]` so the clouds never stretch more than 2.2x. Each band boundary sits where the warped suns of the two photos meet. With the example photos: dusk 1.0 x 2.2 meets dawn 5.6 / 2.2 at 2.5 deg, dawn 5.6 x 2.2 meets mid 25.8 / 2.2 at 12 deg, and mid 25.8 x 2.2 is above 37, which is above day 52.8 / 2.2. So one sun climbs continuously through every crossfade.

**Seam-free mips.** At the atan wrap, `fract` jumps by 1 between neighbouring pixels. Automatic derivatives see that jump and pick the smallest mip, which draws a one-pixel seam line. The shader computes the azimuth derivative analytically, `(x dz - z dx) / (x^2 + z^2) / 2pi`, takes `dFdx/dFdy` of the warped v, and samples with `.grad(gx, gy)`.

**Cloud-aware crossfade.** A linear dissolve of two cloud photos shows every cloud half-transparent mid-fade, like a double exposure. Each slot's weight is multiplied by `exp(fadeSharp x cloudiness)`, where cloudiness is luminance x (1 - saturation), and the weights are renormalised. Wherever either photo has a cloud, that photo wins and the cloud stays opaque, while clear sky still dissolves.

**Weights.** For band k, `ab[k]` is a ramp of the sun elevation around `bands[k][0]`, and the band's weight is `ab[k] - ab[k+1]`. The night weight is `1 - ab[0]`. Weather: `overK` eases toward `overcast` over `weatherFade` and moves the day share onto one weather photo. The pick is an eased one-hot: rain above 0.3 picks the storm photo, bright above 0.3 the whiteout, otherwise overcast. Because the pick eases too, a change of weather type is also a crossfade. The weather photos are day-lit, so they take only the day share; the night share under weather goes to the `nightOvercast` slot. `aurora` splits the clear night share between the night and aurora photos. Slots with zero weight skip their fetch.

**Per-day variants.** A pooled slot's image is swapped in place, into the same `Texture`, only while both its weight and its band weight are 0. The day photo therefore changes at night and the dusk photo by day, and nothing pops. Each band costs one 4096x1024 upload per day.

**Grade and gate.** The default grade mixes toward `hazeColor` by `max(haze, horizonBand x 0.95)`, then applies the storm fold, then uses the haze colour below the horizon. `ctx` gives a custom grade `{ dir, gate, haze, hazeColor, horizonBand, storm, imgSunDir, defaultGrade }`. Wrap `ctx.defaultGrade(lin)` to add a tint, for example an event colour multiplied by `ctx.gate`. Anything with HDR, a tint or weather must be multiplied by `gate`. `bakeGate(true)` sets the gate to 0, which caps the sky at `bakeCap` and drops the wash and the fold, so the PMREM holds only the plain photo blend and re-bakes never make the lighting jump.

## Integration

1. `renderer.toneMapping = THREE.ACESFilmicToneMapping`. Set the base `toneMappingExposure` and use the same value as `knobs.exposureRef`.
2. Convert the photos (below) and fill the `slots` table from `sky-stats.json`. Set `bands` from the measured `sunElev` values using the warp rule above.
3. `const sky = createPhotoSky({ slots, pools, basePath: 'assets/sky/' }); scene.add(sky.mesh); await sky.load(day);`
4. Keep `camera.far` above the dome radius (1700 needs a far plane of 1800 or more). Set `sky.mesh.layers` if mirrors or reflection passes should see the sky.
5. Each frame, before rendering: `sky.update({ dt, sunDir, overcast, rain, bright, day, camera })`, then copy `scene.fog.color` into `sky.uniforms.hazeColor.value`. Ease `overcast` first, about 30 s toward the target; the photo swap eases again over `weatherFade`.
6. PMREM: on the first bake `rt = sky.bake(pmrem)` and `scene.environment = rt.texture` once. After that, call `if (sky.needsRebake() && scene.environmentIntensity > 0.01) sky.bake(pmrem, { renderTarget: rt })`. Always bake into the same render target.
7. Lens flare: multiply its strength by `skyClear` and aim it at `uniforms.imgSunDir`, where the photo draws its sun.
8. Light colour does not come from the photos. Drive the sun light's tint from elevation, for example `(1, 0.55 + 0.42k, 0.28 + 0.64k)` with `k = smoothstep(sunY, 0, 0.35)`, lerped toward white by `overcast x 0.5`. Pull the fog toward an amber colour at dawn and dusk so the haze matches the photos.

## Converting photos

`node convert-sky.mjs list.json out/` reads `[{ name, src, night, moon, sunCol, sunRow, shiftPx }]`, where `src` is relative to the list file. Add `--width 4096 --quality 0.9`, `--chrome <path>`, or `--keep` to view the result in a browser and download by hand. Per photo it:

1. takes the top half of the 2:1 tone-mapped image, so 4096x2048 becomes 4096x1024. The dome never shows below the horizon.
2. finds the sun: the circular-mean centroid of clipped-white pixels (every channel at least 250, more than 8 pixels). A veiled sun with no clipped disc falls back to the brightest 33x33 box, which can be off by about 10 deg; pass `sunCol`/`sunRow` when it is wrong.
3. rotates the image so the sun sits at column 0.5. For a night photo with `moon: true`, it rotates the brightest box (the moon) onto column 0.
4. copies row 1015 over rows 1016 to 1023, which removes the anti-aliased ground edge.
5. encodes WebP at 0.9 and logs `sunElevDeg = 90 - (row + 0.5) x 180 / 2048`, which is `90 - (row + 0.5) x 90 / H` on the cropped image. That value goes in the slot's `sunElev`.

HDR sources (Poly Haven `.hdr`) must be tone-mapped to a display PNG first. The example used Reinhard plus sRGB, with the exposure chosen so the sky half's mean display luminance is about 0.3. Low-contrast decks also got a contrast boost of 1.7 around that mean.

Example sources, all CC0. The measured elevations are examples only; measure your own. ambientCG: MorningSkyHDRI007B (dawn, 5.6 deg), DaySkyHDRI040B (day, 52.8), EveningSkyHDRI046B (dusk, 1.0), DaySkyHDRI069B (mid, 25.8), DaySkyHDRI058B / 027B / 001B / 055B (day variants, 44.8 / 54.0 / 57.5 / 41.2), MorningSkyHDRI011B / 014B and EveningSkyHDRI030B / 032B (dawn variants, 3.5 / 4.9 / 7.9 / 6.2), EveningSkyHDRI044B / 041B (dusk variants, 1.4 / 2.1), EveningSkyHDRI039B (textured overcast), DaySkyHDRI068B (whiteout), DaySkyHDRI061B (storm deck), NightSkyHDRI015 (stars and Milky Way), NightSkyHDRI007 / 004 (aurora; 004 has a moon), NightSkyHDRI016B (misty night). Poly Haven: kloppenheim_07_puresky (moonlit overcast night, exposure trim 0.55). Download pattern: `https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/4k/<id>_4k.hdr`. ambientCG has no cloudy night skies; Poly Haven does.

## Pitfalls

- **WGSL branch scoping.** A TSL node first used inside an `If` is declared in that branch. Every later slot then samples an unassigned `u` and draws concentric rings. Declare everything shared across slots (`u`, its derivatives, `e`) with `.toVar()` before the first `If`. Take `dFdx/dFdy` outside the `If` too, because derivatives need uniform control flow.
- **Two suns.** Photos whose suns sit at very different elevations, crossfaded at one boundary, show two suns. Add a mid-elevation photo and place the boundaries where the warped suns meet. `warpMax` above about 2.5 visibly stretches the clouds.
- **Featureless overcast** reads as fog, not sky. Pick a textured deck with no blue gaps, and keep `stormHaze` and `overFold` low (0.1): the photo carries the deck, and the wash is only a veil.
- **Starry sky in the rain.** Day-lit overcast photos cannot take the night share. Use a separate night-overcast slot, and trim its `exp` (0.4 to 0.55) so it sits darker than the mid-grey rain fog. `nightFold` 0.3 makes the horizon meet that fog.
- **A drawn moon disc on top of a moonlit photo** gives two moons. Rotate the photo so its moon is on the antipode column, and draw no disc.
- **Exposure trims per slot.** Match brightness between pool variants with `exp`: scale by the ratio of mean luminances, for example 0.55 x 77/103 = 0.42.
- **Per-frame arrays.** The weight arrays are allocated once and `.fill(0)` every frame. Code that adds to them with `+=` without clearing them first accumulates forever.
- **Never assign a new texture to `scene.environment`** after boot: it rebuilds every lit material, roughly 300 ms. Bake into the same render target.
- **The bake position.** `bake()` passes `mesh.position` to `fromScene`. A cube camera at the origin with the dome kilometres away renders outside the dome.
- **Depth.** Depth-testing the dome slices distant terrain. Keep `depthTest` and `depthWrite` off and `renderOrder` at -1.
- **Texture slots.** WGSL allows 16 sampled textures per stage. 12 slots is a comfortable ceiling; past 16, merge roles.

## Tuning by eye

Pin a slot (`knobs.pin = i`) to judge one photo alone, then set it back to -1.

| Symptom | Change |
| --- | --- |
| clouds look transparent mid-fade | raise `fadeSharp` (4 to 6) |
| a crossfade looks like a hard switch | lower `fadeSharp`, or raise `fadeDeg` |
| two suns during a band fade | move the boundary to where the warped suns meet; check that photo's `sunElev` |
| clouds stretched near the sun | lower `warpMax` (2.2 to 1.8) and add a photo between the two bands |
| sky too bright or dark against the world | per-slot `exp`, not the renderer exposure |
| the horizon shows a line against fogged terrain | raise `horizonHaze` or `horizonBand`; copy the fog colour into `hazeColor` every frame |
| under weather the deck is hidden by grey | lower `stormHaze` and `overFold` |
| the night deck is paler than the rain fog | lower the night-overcast `exp`, raise `nightFold` |
| lighting jumps when weather arrives | the bake picked up the fold: check `bakeGate`; lower `rebakeWeight` |
| a faint glow beside the sun at dawn | the photo's sun column came from the brightest box; give `sunCol` by hand |

## Performance

- Each pixel samples only the slots whose weight is above 0: one fetch for most of the day, two during a crossfade, up to three when weather or aurora overlaps a band fade. Every slot still costs a uniform branch and its derivative maths.
- A 4096x1024 WebP is about 45 to 380 KB on disk. In VRAM it is about 22 MB with mips, so 12 slots take about 270 MB. If that is too much, drop to 2048 wide: the sun disc softens, the clouds hold up.
- A re-bake (6 faces plus mips) is throttled to one per `rebakeEvery` seconds; a crossfade costs 2 to 3 bakes. Skip bakes at night when environment intensity is 0.
- The dome needs no shadow, no fog and no depth. 48x24 segments are enough because the direction is computed per pixel.
