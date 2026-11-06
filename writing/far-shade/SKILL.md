---
name: far-shade
description: Use when a large streamed terrain needs hill, ridge and tree shade past the reach of the real shadow map, or a cheap fake ambient occlusion everywhere, without paying for a far shadow cascade. A toroidal RGBA8 world atlas (height + canopy + written flag) written per terrain tile, an 8-tap vertex-stage march toward the sun, canopy blobs displaced down-sun, multiplied into albedo; no shadow pass. Ships `far-shade.tsl.js`.
---

# Far Shade

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

The companion file `scripts/far-shade.tsl.js` is the atlas, the writer and the shader node. Copy it into the project; it imports only from `three/webgpu` and `three/tsl`.

## What it is

A fake terrain self-shadow that takes over from a far shadow cascade. The world's heights live in one 1024 x 1024 RGBA8 texture at 4 m per texel, addressed modulo its span (4096 m), so it never needs an origin or a recentre. Each terrain tile writes its heights and rasterises its trees as soft canopy discs when it arrives. Every material that shows terrain (ground, rocks, stumps, cards) runs a short march toward the sun in the vertex stage: 8 height taps, 8 to 270 m out, against a rising horizon line. That gives hill and ridge shadows. One more tap reads the canopy up-sun, and that gives tree shadow blobs. The result is one varying, multiplied into the albedo as a darkening.

It is not a shadow map. Nothing is rendered from the light, no casters are drawn, and the cost is 9 texture taps per vertex plus one 4 MB upload on frames where tiles arrive.

## When to use it

- streamed open terrain (tiles of 64-512 m) seen to 1-4 km, with a sun that moves
- the far shadow cascade costs too much (a 4096 depth map is 64 MB, and the pass draws everything out to the horizon), or you already run it at a reduced rate and it lags
- a cheap fake AO on the ground under the near cascade: hollows, the lee of ridges, the ground under forest

Not for: moving casters (vehicles, characters, animals), buildings, poles or anything that is not terrain or a tree; shadows on vertical walls; indoor scenes; small worlds where one cascade already covers everything.

## Companion file API

`createFarShade(options)`. Options, from `FAR_SHADE_DEFAULTS`:

- `cells` (1024): atlas texels per side; `cellSize` (4): m per texel. The world wraps every `cells x cellSize` m (4096 m)
- `heightFloor` (-600), `heightStep` (0.05): q = round((h - floor) / step), 16 bit, so -600 .. +2676 m
- `taps` ([8, 14, 24, 40, 65, 105, 170, 270]): m along the sun's ground direction
- `bias` (1.5): m an occluder must clear the sun's ray by; `soft` (4): m from no shade to full shade
- `canopyHeight` (7): m, crown height used for the canopy offset; `canopyReach` (40): cap on that offset in m
- `canopySpread` (2.2): disc falloff `1 - d^2 / (r^2 x spread)`, cut at that radius
- `minTan` (0.02): floor on tan(elevation); `sunFade` ([0.02, 0.12]): sin(elevation) range of the dawn fade-in
- `strength` (0.7), `canopy` (0.8), `near` ([0, 1]): starting values of the knobs below

Returns `{ texture, knobs, write, upload, setSun, shadeNode, apply, options }`:

- `knobs`: uniforms, set `.value`. `strength` (albedo darkening at full shade), `canopy` (canopy relative to hills), `near` (`Vector2`, m from the camera: the shade fades in from x to y; (0, 1) = everywhere), `kill` (1, 0 = off for an A/B, same cost), and the per-frame `dir`, `tan`, `fade` that `setSun` writes.
- `write({ originX, originZ, heights, size, cells, canopies })`: one tile. `heights` is row-major (z rows) with `(cells + 1)^2` samples over a `size`-m square at the origin. It is resampled bilinearly onto the atlas texels inside the square, which is an exact copy when `size / cells === cellSize` (a 256 m tile with 64 cells and 65 x 65 samples). `canopies`: `[{ x, z, r, strength = 1 }]` in world m. Use `r = 3 m x tree scale` for a ~7 m conifer. Sets the dirty flag.
- `upload()`: once per frame. It sets `texture.needsUpdate` only when something was written since the last call, and returns whether it did.
- `setSun(sunDir, fade?)`: `sunDir` is the world vector toward the sun. It writes the unit ground direction and `tan(elevation) = y / |xz|`, clamped to `minTan`. `fade` defaults to a smoothstep of sin(elevation) over `sunFade`. Pass your shadow intensity instead (day gate x overcast) so the fake fades with the real shadows.
- `shadeNode(position = positionWorld)`: `varying(shade)`, a 0..1 float with 1 = lit. Use it inside any colour graph.
- `apply(material, position?)`: `colorNode = vec4((colorNode ?? color x map).rgb x shade, a)`. Vertex colours still multiply after it.

## How it works

- **Toroidal atlas.** A texel index is `round(world / cellSize) mod cells`, and the shader samples `world / span` with `RepeatWrapping`. There is no origin to track and no copy when the camera moves, so the world is unbounded. The 4096 m window only has to be wider than what you can see shaded: tiles far behind are overwritten by tiles ahead. Terrain is static, so a stale cell from an old lap still holds the true height of whatever maps there. It is only wrong if that place is visible at the same time as its alias, 4 km away.
- **Half-texel addressing.** The CPU writes the height of world `i x C` into texel `i`. In uv space, texel `i`'s centre is `(i + 0.5) / N`, so the shader samples at `(world / C + 0.5) / N`. Without the +0.5 the whole field shifts by half a cell (2 m) toward -x/-z. At 4 m soft shade it is invisible, but it is wrong.
- **Height encoding.** R = q >> 8, G = q & 255; decode `R x 255 x 256 + G x 255`. Bilinear filtering of the two bytes separately is still exact: the sum of linear interpolations is the linear interpolation of q. Do not use mipmaps (taps use `.level(0)`).
- **Written flag.** A = 255 on written cells. The decode returns -9999 m where A < 0.5, so unwritten ground never occludes, and a half-filtered edge to an unwritten cell does not either.
- **The march.** For each tap distance d along the sun's ground direction, occlusion = `h(d) - (P.y + tan x d + bias)`. The ray from P toward the sun rises by tan(elevation) per metre, and a height above it blocks the sun. Max over the taps, `smoothstep(0, 4 m)` = hill shade. The taps are spaced geometrically (8 to 270 m) because near occluders need fine steps and far ridges only need coverage. At 4 m texels a ridge narrower than one texel can slip between taps; that is fine for soft shade.
- **Canopy.** Each tree is a soft disc in B (`1 - d^2 / (2.2 r^2)`, max-blended). A crown of height ~7 m shades ground `7 / tan` m down-sun of itself. So the shader reads B at P + dir x min(7 / tan, 40 m), the point UP-sun of P, and the blob lands down-sun of the tree. An early version read down-sun and put the blobs on the wrong side. The 40 m cap stops a low sun from reaching across a valley.
- **Combination.** `max(hill, canopy x canopyK) x fade x kill x reach(near band) x strength`, subtracted from 1. Strength 0.7 matches what the real cascade does on bright snow, where removing the sun term leaves about 30 %.
- **Vertex stage.** 9 taps per VERTEX, not per pixel. Terrain meshes at 2-4 m vertex spacing are as dense as the atlas itself, so per-pixel taps would only interpolate the same 4 m data at 10-50x the cost. Instanced cards, rocks and stumps read it at their vertices. For a card, pass its root position to `shadeNode` (a flat varying of the root), so the whole card is shaded alike.
- **Sun per frame.** `setSun` is three uniform writes. The shade follows the sun continuously, with no re-bake when the sun moves, because nothing is baked except heights.
- **One upload per frame.** Tiles mark the texture dirty; `upload()` turns that into a single `needsUpdate` per frame no matter how many tiles landed. A full 1024^2 RGBA8 upload is 4 MB. Writing `needsUpdate` per tile would upload the same 4 MB several times in one frame at boot.

## Integration

```js
import * as THREE from 'three/webgpu';
import { vec4 } from 'three/tsl';
import { createFarShade } from './far-shade.tsl.js';

const farShade = createFarShade();                 // 4 MB texture, 4096 m wrap
farShade.apply(terrainMaterial);                   // after you set its colorNode, before the first render
farShade.apply(rockMaterial);
grassMaterial.colorNode = vec4(grassColour.mul(farShade.shadeNode(rootPositionWorld)), alpha); // by hand

streamer.onTileReady = (tile) => {
  farShade.write({ originX: tile.x, originZ: tile.z, heights: tile.heights, size: 256, cells: 64,
    canopies: tile.trees.map((t) => ({ x: t.x, z: t.z, r: 3 * t.scale })) });
};

renderer.setAnimationLoop(() => {
  farShade.setSun(sunLight.position.clone().sub(sunLight.target.position), sunLight.shadow.intensity);
  farShade.upload();
  renderer.render(scene, camera);
});
```

Steps:
1. One far shade per world. Apply it to every terrain-like material ONCE, before first render: changing `colorNode` later recompiles the pipeline.
2. Write each tile when its heights exist, on the main thread (a 65 x 65 write and a few hundred discs take well under 1 ms). Include trees whose disc crosses in from a neighbour if you want seam-free blobs (see pitfalls).
3. `setSun` and `upload` every frame, before render.
4. With a real shadow map, cut it to ONE near cascade (`maxFar` ~120 m). Then pick a mode:
   - **far only:** `knobs.near.value.set(0.75 x far, far)`, so the fake fades in exactly where the cascade fades out (90..120 m for 120)
   - **fake AO everywhere (recommended):** `near = (0, 1)`, which is the default. Under the cascade it deepens the sharp shadows and darkens hollows and forest floors. The cost is the same, since it was already computed per vertex and only faded to 0 near.

## Pitfalls

- **Straight shadow edge at the cascade's end.** The fake knows only terrain and trees, so pole, building and billboard shadows stop where the near cascade ends. With a 70 m cascade this was a visible straight line from a high camera at low sun. 120 m moved it out of sight. Do not shorten the cascade below ~100 m on the strength of the fake.
- **Low sun only, mostly.** Hill shade needs tan(elevation) of about 0.6 or below to show. At noon only the canopy and steep ridges register. Debug at morning or evening.
- **Canopy seams.** A tile's write clears B in its own square, so the part of a disc that spilled from a neighbour written earlier is erased. Either write the neighbours' edge trees too, or accept that a blob is cut at a tile edge.
- **Toroidal alias.** The atlas holds exactly one place per cell. If you can see further than the span, raise `cells` or `cellSize`.
- **`cameraPosition` in the near band.** In a mirror or reflection pass it is that camera, so the band moves. With `near = (0, 1)` this does not matter.
- **Not for walls.** The march compares heights, so a vertical face is shaded only by the terrain in front of it, never by itself.
- **No moving casters.** A vehicle's shadow must come from the near cascade.
- **Unwritten = lit.** Shade pops in as tiles arrive, from the camera outward. Write tiles before they are visible, or fade the far ring.
- **sRGB.** The DataTexture is linear data (no `colorSpace`); never mark it sRGB, or the height bytes are curved.
- **A stale-cell suspect.** If someone reports a fixed dark patch with a straight edge, toggle `kill` before blaming the far shade. In the source project such a patch survived `kill = 0` and came from something else.

## Performance

Measured in the source project (one 4096 m wrap, 256 m tiles, headless WebGPU) when the far cascade was replaced:
- the 4096 x 4096 far depth map is gone: 64 MB of VRAM, and its depth pass (it was already at every 4th frame) is gone; shadow passes per frame 1.25 -> 1
- CPU render medians within noise at spawn; the certain wins are the depth pass and the VRAM
- the atlas: 4 MB of RAM + VRAM, one 4 MB upload on frames where tiles land, none otherwise
- the look: hills and tree blobs darken 10-25 % of the far ground band, which is subtle by design (truck-sim style far worlds are unshadowed). Kept as a fake AO everywhere at strength 0.7, canopy 0.8.

Cost scales with vertices, not pixels: 9 bilinear taps per vertex of every material it is applied to. Apply it to terrain and its scatter only. Skip the grass if its vertices outnumber the terrain's, and give cards the root-position variant.
