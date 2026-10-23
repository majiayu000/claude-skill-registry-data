---
name: video-3d
description: >-
  Renders real 3D for any code-built video: three.js scenes inside HyperFrames, deterministic
  (every frame a pure function of t). Covers cameras (rails, ortho, dolly zoom, shake, cuts),
  extrusion, lathe, 3D text, lines, physical materials, HDRIs, baked AO, every EffectComposer
  pass (AO, DOF, AA, grain, LUT, glitch, SSR, motion blur), looks (ASCII, toon, halftone,
  dither, CRT, pixel art, ink), particles and GPU compute, baked physics and cloth, glTF models
  and animation, screens and image sequences, data maps and graphs, audio-driven visuals,
  DOM/GSAP/alpha compositing and WebGPU, each with a tested status. An executor under
  video-studio. Use when a film needs volume, light, depth, element counts or a rendered look
  that CSS 3D cannot give. Triggers: "3D", "three.js", "WebGL", "WebGPU", "3D logo",
  "logo sting", "globe", "particles", "shader", "3D scene", "ASCII", "glTF".
---

# video-3d

The lane for films where flat cards in space (video-moves' CSS 3D) are not enough: solids, light,
real depth and occlusion, huge element counts, a rendered look. HyperFrames seeks frames out of order
in parallel workers, so every visual state is computed from t alone.

Proven by private test films (they do not ship; their numbers, traps and fixes are in the references).
Four finished looks: a logo film (extruded logo, PBR, lock-up landing), a globe film (15k dots, draw-on
arcs, labels), a particles film (64k particles from a voice morphing into words), an ASCII film (a scene
as glyphs, words resolving out of it). Seven capability reels (2026-10-14, one capability per section):
materials, post, styles, models, camera-text, data, WebGPU. The labels are explained in the legend of
`references/capabilities.md`.

video-studio orchestrates the film and its laws (`../video-studio/references/laws.md`, Picture: motion
has a cause, no frozen holds, every frame postable, readable text); video-moves owns camera grammar
(`../video-moves/scripts/camera-kit.js`); video-sound the sound; video-check the gates. Colours come from
the film being made - no brand or film content is baked into this skill.

**Input: the film's `brief.md`** (`../video-studio/references/brief.md`). It owns copy, claims, tone,
material, moments and private data; this skill owns the implementation. If the brief cannot be
met, say so to video-studio - never change it silently.

## Requirements

- HyperFrames CLI ≥ 0.8.156 (tested on 0.8.156; pin it in the film's `package.json`) and a GPU-capable
  browser for the render (`--browser-gpu`). WebGPU films need a hardware adapter. SwiftShader
  (`--no-browser-gpu`) renders WebGL only, ~6-10x slower.
- three.js 0.181.2 (r181), loaded from jsdelivr through an import map (`three`, `three/addons/`; WebGPU
  films also `three/webgpu`, `three/tsl`) - every recipe assumes this version. Other pins the recipes
  use: troika-three-text 0.52.4, d3-force 3.0.0, `@dimforge/rapier3d-compat` 0.19.3 (bakes in Node),
  world-atlas 2.0.2 (maps).
- Node 22+ for the Node tools (`build-map.mjs`, `seek-order-test.mjs`, your bakes). The seek-order test
  uses puppeteer-core and HyperFrames' cached chrome-headless-shell (it finds them in the npx cache).
- Python 3 with numpy and Pillow, plus ffmpeg, for the QA scripts.
- The upstream `hyperframes` skills (heygen-com/hyperframes) and the sibling video skills.

## When 3D, when CSS

| The film needs | Use |
|---|---|
| a card or a screenshot moving in space; parallax between flat layers | video-moves (CSS 3D, `camera-kit.js`) |
| an object with thickness, bevels, glass or metal, a shadow; a logo as an object | **object** / **materials** recipes |
| points, arcs, labels on a globe; bars, maps, graphs, terrain from data | **data in space** / **data maps** recipes |
| thousands to millions of moving elements, morphs, glow, shader grounds | **particles**; **WebGPU counts** above ~8M |
| a rendered look: glyphs, toon, print, dither, CRT, pixel art, ink | **ASCII** / **looks** recipes |
| grading, DOF, AO, grain, glitch, reflections, motion blur | **post chain** recipe |
| a character, a model, a fall, cloth, a flock | **models and baked sims** recipe |
| a device with a live screen, 3D text, footage plates, a 3D layer with alpha | **screens and compositing** recipe |

If flat layers can do it, prefer CSS: cheaper, `check` can see it, text stays DOM.

## What is proven

`references/capabilities.md` is the catalogue: every useful capability by area (17 areas), how to keep
it deterministic, traps, sketches, measured costs and a status - `proven (film)`, `proven, partial
(film): what` or `never` (not seek-safe as shipped, with the replacement). Only rendered capabilities are
listed; the legend names what was left out (Gaussian splats, fracture, fluids, lightmaps, cascaded
shadows, stencil portals, most WebGPU post). All proofs ran on the GPU path; SwiftShader was checked only
in part. Never: `GlitchPass`, `AfterimagePass`, TAA/TRAA accumulation, `VideoTexture`, physics stepping in
the page.

Anything not in the catalogue: render a 3-5 s probe and run the determinism protocol before promising it,
then add it to capabilities.md with the probe film as its status.

## Recipes and code

`references/recipes.md` - eleven proven kinds of scene with the pieces to lift. Reusable code, each
folder with a README: `assets/recipes/ascii/` (glyph pass), `looks/` (toon hull, Sobel ink, halftone,
dither, CRT, ink and paper, wipe), `post/` (seeded AO, grain hash, SMAA wait, sub-frame motion blur,
presenter, seeded glitch), `materials/` (lathe vessels, GPU AO baker), `models/` (seek-safe mixer, baked
rigid bodies and VAT cloth), `compositing/` (sub-composition time, alpha export), `data/` (map builder,
GPGPU replay/bake), `webgpu/` (film clock, node frame, atomic density splat), `qa/` (seek-order test,
per-section comparison, blank/frozen check, exact shimmer).

## Build

1. `references/contract.md` first - binding: the page (build hold, warm-up, visible failures,
   sub-compositions), time (everything from t, integer-frame decisions, seeded libraries, no frozen ends),
   picture (supersampling, culling, lines, text, colour, banding), post-processing, models and animation,
   render (determinism protocol, backends, bitrate), WebGPU.
2. Start from `assets/scene-skeleton/` (index.html + assets/scene.js): a seek-driven renderer with
   camera helpers and a try/catch `renderAt`; fill in `build()` and `renderAt(t)`.
3. Take the recipe and the capability entries the film needs; lift code from `assets/recipes/` first,
   and write the rest from the recipe and the capability entries.
4. Camera moves and story time from video-moves (the same math; copy what you need into the module).
5. Light for the medium: measure hero colours (PBR) or cell luminance (glyph and grid looks) on a
   rendered frame before judging.

## Check

`references/qa-3d.md`: `hyperframes check` is a lint only (it cannot see a canvas). Snapshots at every
state change; the determinism protocol (`--workers 4` vs `--workers 1` - auto is one worker for ≥ 900
frames - plus the in-page shuffled/reverse seek-order test, PNGs per section when checksums differ);
blank/magenta/frozen output; 1:1 crops; chunk seams; banding on the encoded file; hero colours;
shimmer tools for quantised looks. Pin `--browser-gpu` (or `--no-browser-gpu`) for a deliverable and
never mix the two. Then video-check's gates and its independent review.

## Adapt it

- Your palette and brand objects: set the `--film-*` tokens from each film's brief, keep your logo SVGs,
  product models and fonts in one folder that films copy in, and measure your brand colours once under
  the light and tone mapping you use (`capabilities.md` 3) - write the numbers down.
- Your GPU and backend per deliverable: choose `--browser-gpu` (WebGL or WebGPU) or `--no-browser-gpu`
  (WebGL only) for each deliverable, write it into the render command, and never mix chunks. The costs
  here were measured on an M1 Max; time one film on your machine before you plan a long render.
- Adding a capability: render a 3-5 s probe film, run the determinism protocol and the seek-order test
  (`qa-3d.md` step 3), then add an entry to `capabilities.md` with its status, traps and costs, under a
  label for your probe film in the legend.
- Your asset policy: which sources and licences you accept, and whether the agent may download free
  assets without asking (`capabilities.md` 16).
- Upgrading three.js or HyperFrames: re-render one film per recipe you use and re-check the private
  node-frame API (`contract.md`, WebGPU) before you move the pins.
