---
vendored_from: https://github.com/appautomaton/delineate
name: svg-kinetic-cut
description: >
  Make or change Cut (cut/): a 24 fps browser-native motion-direction film engine in World 01 (Silver
  Gelatin & Cinnabar) built with zero runtime dependencies on multi-pass WebGL2 Leica cinema optics, 3D
  projective homography, creamy f/1.4 Scheimpflug bokeh, beveled Crown-Glass prisms, continuous 2.8px
  fluted-crystal aurora, Swiss millimeter drafting & mineral quadtree shaders, Canvas2D indie foundry
  typography (Switzer + Zodiak + Geist Mono), Turrell architectural light-blade scenes, LUT-graded
  photographic plates, G2 superellipse studio hardware tiles, Leica rangefinder CV telemetry, and an
  original 134 BPM Setloom warehouse techno score. Use for authoring or editing a 24 fps director's
  timeline, tuning WebGL2 optics / fluted-crystal plasma / halation / quadtree shaders, grading plates
  via palette.ts, refining UI montages or CV overlays, or syncing cuts to the 134 BPM score, even if the
  user never says "skill".
triggers:
  - svg-kinetic-cut
  - svg
  - kinetic
  - cut

---

# Kinetic cut

A browser-native **24 fps** motion-direction film engine grounded in **World 01 · Silver Gelatin &
Cinnabar** (`Leica Darkroom × delineate Monochrome`): `93%` warm cotton rag (`#F6F5F0`), selenium
obsidian (`#08090B`), soft bone (`#F2EFE9`), and brushed platinum-graphite (`#6E6D68`), warmed by `5%`
champagne tungsten glass (`#D6CFAF`) and `2%` Swiss cinnabar (`#D9412B`). Read `cut/notes.md` and
`cut/palette.ts` first for the module map, copy arc, beat sheet, and invariants.

## The bar

- **Unified World 01 color architecture (`cut/palette.ts`).** Never use raw digital `#FFFFFF` on `#000000`
  neon gradients. Import `PALETTE`, `getGradedPlate`, and `getGradedEye` from `cut/palette.ts` so every
  photographic plate shares one Leica silver-gelatin & champagne split-tone LUT and `eye.jpg` obeys the
  **strict 3-value anatomical invariant** (desaturated alabaster sclera, luminous striated `#9E9580..#D6CFAF`
  mineral iris `r = 62..208px`, distinct `#08090B` pupil `r = 56px`, and crisp `10:30` corneal catchlight—never
  swallowing the iris in a black void).
- **True 24 fps film cadence (`41.67 ms` per frame) + living speed-ramp kinematics (`shotRamp`).** Quantize
  the director's clock to exact integer frames (`frame = Math.floor(t * 24) % TOTAL_FRAMES`) locked to the
  `134.000 BPM` beat grid, driving montage shots with exponential whip-in settle, continuous dolly push,
  and pre-cut anticipation pull.
- **Four-pass WebGL2 Leica cinema pipeline (`cut/shader.ts`).** Route the `1280 × 720` frame through four
  real-time `RGBA8` GPU passes (`< 2 ms` budget):
  1. *Pass 1 — Leica Cinema Optics, 3D Homography & Five Transmutation Modes*:
     - Radial `pow(r, 1.85)` lens dispersion, organic lens breath, and damped pointer parallax.
     - True 3D ray-plane homography + camera roll (`uPersp`, `uRoll`, `uPerspPivot`, `uZoom`) with creamy
       `pow(defocus, 1.22)` 24-tap Vogel Scheimpflug `f/1.4` DOF (`planeUv.y - uFocusY`).
     - `mode 0` *Archival Cotton Rag, Scheimpflug DOF & Beveled Crown-Glass Prisms*: 3 achromatic/champagne
       beveled crystal slabs (`uGlass`) with subtle dispersion (`~0.004`) and Fresnel `#F2EFE9`/`#D6CFAF`
       top-left specular rims.
     - `mode 1` *Fine Swiss Engraving ASCII & `5.8px` Optical Blueprint Micro-Mesh*: soft `pow(lum, 0.88)`
       gradation (`· : / x o ☒ #`) and silver-champagne X-ray aperture mesh (`uAsciiBg = 0.35`).
     - `mode 2` *Delicate `6.0px` Swiss Millimeter Drafting Grid & Curved Cotton-Paper Peel*: `0.22`
       silver-graphite hairlines on `#F6F5F0` rag with smooth cylindrical corner curl (`uAsciiBg >= 1.5`)
       while foreground typography stays crisp on `fg`.
     - `mode 3` *Mineral Quadtree Micro-Mosaic & Silver-Champagne Mezzotint Halftone*: stepped 3-tier
       quadtree (`uAsciiBg <= 1.5`) and fine mezzotint (`uAsciiBg > 1.5`) preserving 3-value iris clarity.
     - `mode 4` *Silky Continuous `2.8px` Vertical Fluted-Crystal Aurora*: 4-octave domain-warped FBM
       aurora in World-01 `plasmaStops` (`#1B2230`, `#5C6B7E`, `#D6CFAF`, `#F4F1EA`) refracted through
       continuous `sin(px.x * 2.244)` cylindrical glass flutes (`0.84..1.05` sheen, zero black pixel gaps)
       around a serene `#08090B` center pocket.
  2. *Pass 2 — 7-Tap Directional 180° Shutter Blur & Kinetic Persistence*: Hann-weighted shutter smear
     (`uMotionBlur`) + consecutive-frame persistence (`frame === prevFrame + 1`).
  3. *Pass 3 — Half-Res Anamorphic Bloom & Halation*: separable `640 × 360` highlight bloom.
  4. *Pass 4 — Filmic Composite*: platinum `#C8D3E6` Panavision streak (`uAnamorphic`), warm `#D95B38`
     Kodak halation, surgical foreground typography (`0.16x` tamed chroma—zero cyan/red double-vision),
     platinum/champagne AR corner glass sheen, cinema vignette, and dual-frequency 35mm silver grain.
- **Architectural instrumentation, sacred negative space & indie typography.** Set narrative copy in
  tight-tracked **`Switzer`** (`-0.028em`), reserve **`Zodiak`** serif exclusively for S06's `158 × 76`
  variable-radius micro-dot `"noise"`, and **`Geist Mono`** for `0.68px` Leica rangefinder CV overlays
  (`cut/cv.ts`). Keep `S08a` (`10s`) serene (`65%` untouched `#08090B` void above one delicate `· : +`
  silk-stipple horizon ridge, zero CV boxes) and `S09` architectural (James Turrell vertical light-slit →
  `#F6F5F0` 28-strand drafting ribbon → `38°` diagonal prism light-blade, zero rocket flames).
- **Rubin figure-ground finale (`R3-03` Sheared Director's Gate `16:9 → d`).** Pay off `"you do."` by
  whip-morphing Card #5's `16:9` frame into the center `16:9` aperture (`F 398–407`), then slamming
  `#FFFFFF → #F6F5F0` archival rag at `F 408` as `#161615` L-blades lock into `delineate`'s `d`.
- **Frame-locked opt-in studio audio (`cut/audio.ts`).** Stream the `18.000 s` `134.000 BPM` Original
  Setloom Warehouse Techno score (`cut/assets/audio/score.m4a`), strictly muted until user gesture.

## Editing or adding a scene

1. Keep the timeline deterministic in `cut/scenes.ts`: each scene owns a `[startFrame, endFrame)` span
   inside the `432`-frame (`18.000 s @ 24 fps`) master reel and returns a `ShaderParams` object.
2. Preload all canvas webfonts explicitly via `document.fonts.load(...)` in `cut/main.ts` and re-bake
   offscreen typographic dot-matrix grids (`ensureGrids()`) once `document.fonts.check(...)` confirms both
   `Switzer` and `Zodiak` are active.
3. Credit every external photograph, plate, font, and audio master's exact source and license inside `cut/notes.md`.

## Done means

`npm run check && npm run cut:build` pass cleanly and `npm run cut` (`http://localhost:5390/`) runs at
exact 24 fps in Chrome:
- Capture and inspect borderless keyframes across all 10 scenes (`?frame=...&paused=1&hud=0`) confirming
  World-01 Silver Gelatin & Cinnabar cohesion, `s07Amber` `5.8px` X-ray mesh (`S02`), `f/1.4` LUT-graded
  SaaS UIs (`S03`), `6.0px` drafting paper peel (`S04`), 3-value anatomical eye (`S05`), variable-radius
  `Zodiak` `"noise"` (`S06`), serene `10s` horizon (`S08a`), Turrell vertical slit & `38°` diagonal prism
  light-blade (`S09`), continuous `2.8px` fluted-crystal aurora (`S10a`), and `#161615` `R3-03` Director's
  Gate on `#F6F5F0` archival rag (`S10d`).
- Confirm `glErr === 0`, zero console errors, minimalist HUD (`Play`, `‹`, `›`, `Sound`), HTTP 200 Web
  Audio decode (`18.000 s` stereo) for `cut/assets/audio/score.m4a`, and strictly opt-in audio playback.
