---
vendored_from: https://github.com/appautomaton/delineate
name: svg-optical-mesh
description: >
  Make or change Mesh Gradient (mesh/): a pure 4-tile 8+4 asymmetric WebGL2 GLSL 300 es optical mesh Bento
  Grid with OKLab color science, unified Fontshare Cabinet Grotesk + IBM Plex Mono typography, autonomous
  vertical backlit-vessel scrolling, nonlinear spring scroll & morph motion, and Day/Night optical physics —
  01 Frosted Halo (anisotropic frosted morphing halo on pure porcelain/obsidian), 02 Thin-Film Crystal
  (precision-cut raymarched 3D Cauchy & Airy crystal solids floating directly on pure porcelain/obsidian with
  zero painted backdrop box), 03 Atmospheric Plumes (wide Swiss editorial triptych of analytical asymmetric
  silk curtains), and 04 Backlit Vessels (full-height Turrell obsidian vertical totem of autonomous
  auto-scrolling superellipse vessels with vertical/horizontal anamorphic blur). Use for adding or tuning an
  nonlinear scroll-spring motion, frosted anisotropy, silk advection, thi …
triggers:
  - svg-optical-mesh
  - svg
  - optical
  - mesh
---

# Optical mesh

A pure 4-tile `8 + 4` asymmetric Bento Grid of physical light over colour fields — proving why next-generation
mesh gradients belong to optics, advection, and glass rather than static CSS radial blurs or noisy banners.
Read `mesh/notes.md` first for the module map and shared layout contracts.

## The bar (anti-slop laws)

- **Zero banner, zero hero, zero header — four silent optical worlds fitting one desktop viewport.** Start
  directly at the top on gallery stone (`#F2F1EC` Day / `#04060B` Night): left 8 columns hold `01 Frosted Halo`
  (`span 4`) + `02 Thin-Film Crystal` (`span 4`) above wide `03 Atmospheric Plumes` (`span 8`); right 4 columns
  span both rows as a full-height `#070A10` Turrell obsidian vertical totem (`04 Backlit Vessels`). Place
  `delineate / Mesh Gradient` and global controls (`Palette` swatch · `Drift/Still` · `Night/Day` · `Source` ·
  `Skill`) on one frameless bare-ground colophon line beneath the grid — never inside a coloured gradient card.
- **Radical chrome restraint — zero developer jargon.** Never dump `GLSL 300 ES`, `IOR`, `OPD`, watermarks, or
  control instructions onto the art. Every tile carries only its quiet `01`–`04` tabular index, title, and
  inline specimen strip (`04` keeps its top-right completely empty above `Reeded`'s flutes).
- **One disciplined studio grotesque (`Cabinet Grotesk` `@1` + `IBM Plex Mono`).**
  - Never mix three competing display voices. Load `https://api.fontshare.com/v2/css?f%5B%5D=cabinet-grotesk@1&display=swap`
    paired with `IBM Plex Mono` (`400;500`).
  - Set tile titles (`13.5 px`, `wght 540`), all 3 Plume poster headlines (`wght 560` paper vs `450` obsidian
    halation compensation), and all 6 Lantern vessel labels (`wght 560 → 250` optical DOF on `contain: layout
    style` spans, quantized to integer steps) in `Cabinet Grotesk`.
  - Set tabular `01`–`04` indices, Plume micro-specs, and specimen strips in `IBM Plex Mono`. Use real `1 px`
    `.plume-rule` hairline bars instead of ASCII underscores and keep Plume's 2-column Swiss poster grid
    uncollapsed above `145 px` sheet width.
- **Unified porcelain/obsidian ground (`uGround`) and zero PowerPoint gloss dots.**
  - Both `01 Veil` and `02 Prism` float directly on `#FCFCFB` pure porcelain (Day) or `#070913` deep obsidian
    (Night) — NEVER paint a separate bright blue/teal sky-box behind 3D crystals, and NEVER place circular
    white Blinn-Phong gloss orbs on curved glass surfaces. Let specular brilliance come strictly from grazing
    thin-film Fresnel caustics.
- **Nonlinear spring scroll, staggered morphing & autonomous vertical Lantern glide.**
  - Feed passive scroll deltas via power-law impulse (`|dy|^1.3`) into an underdamped `scrollSurge` `Spring`
    (`ω = 14, ζ = 0.34`) driving Veil defrost tilt + strong-flick morph, Prism angular crystal orbit, Plume
    thermal updraft surge, and subtle Lantern shimmer.
  - Stagger autonomous spring morphs (`Veil ~4.2 s`, `Prism ~5.1 s` offset `2.3 s`).
  - On `Lantern`, hold razor-sharp center lock for `2.6 s` in `Drift` mode before launching an elastic spring
    step vertically (`scroll.target += 1` with velocity impulse for Y-axis anamorphic streaks); pause
    immediately on hover/drag/click and resume `3.8 s` after leave without trapping mobile `pan-y` scroll.
- **Four optical plates:**
  1. **01 — Veil (`shaders/veil.ts`)**: Four rounded 2D SDFs (`squircle`, `circle`, `reuleaux`, `pentagon`)
     with decoupled `sigmaOuter`/`sigmaInner` analytical `erf` convolution, lower-right inner contrast pool
     behind the `1.2 px` specular crescent, upper-right acrylic frost stipple, and decoupled radial zero-cutoff
     fade melting imperceptibly into porcelain or obsidian.
  2. **02 — Prism (`shaders/prism.ts`, shapes `0..3`)**: Precision-cut raymarched solids (`spool`, `dome` with
     dished equator planes for zero aliasing, `diamond`, `tetra`) floating directly on pure `uGround` with
     bounding-sphere early-out (`r = 0.94`, 48 steps with sub-pixel cone-coverage silhouette AA), single
     14-step exit trace + 2-step exact `d = 0` surface snap (0% bevel staircase ripples), analytical R/G/B
     Cauchy dispersion (`1.48/1.52/1.57`), Airy thin-film Fresnel caustics (`630/532/460 nm`), zero circular
     Phong spots, and zero grey TIR.
  3. **03 — Plume (`shaders/plume.ts`)**: 4-tap curl-warped analytical asymmetric silk-curtain caustics
     evolving across a 3-chord harmonic cycle on 3 Swiss posters (`wash` with Night top-left `typeCalm` guard,
     `bloom` rising `32–38%` beneath `62%` clean paper, `emission` obsidian aurora curtains blooming to
     `#FFFDF8`). Compact card mode (`compact > 0.5`) renders one full-bleed silk sheet.
  4. **04 — Lantern (`shaders/lantern.ts`)**: Six glowing superellipses (`n = 4.6`, `Tangent`, `Aperture`,
     `Cipher`, `Foci`, `Warp`, `Reeded`) with thick corner Fresnel rims, velvet cavities, jeweler-fine
     procedural motifs, and two-pass `RGBA8` FBO + 17-tap hash-jittered dual-axis anamorphic blur (Y-axis when
     `isVerticalLantern(w, h)`, X-axis when wide).
- **Strict GPU & scroll efficiency, adaptive 24 / 60 fps pacing, silent off-screen.**
  - On `mesh/`, each of the 4 tiles compiles only its own shader via `new MeshRenderer(canvas, { plates })`,
    uses per-tile optimal backing DPR (`plume: 1.0`, `lantern: 1.35`, `veil: 1.5`, `prism: 1.65`), paces calm
    ambient drift at **24 fps** (`41 ms`) while ramping cleanly to **60 fps** (`15.5 ms`) during interaction,
    morphs, or glides, and sleeps completely off-screen via `IntersectionObserver` + `document.hidden` (`0`
    off-screen draws).
  - On `delineate`'s landing card (`card.ts`), all 4 live plates share ONE `MeshRenderer` WebGL2 context via
    `gl.scissor` + `gl.viewport` with `ResizeObserver`-cached rects (zero `getBoundingClientRect` in RAF).

## The task

- **Tuning an optical plate**: edit `mesh/shaders/<plate>.ts` and verify with `?plate=<plate>&still` across
  `?light=day`, `?light=night`, `?palette=0|1|2`, and `?shape=0..5`.
- **Adding or refining a curated palette**: edit `mesh/palette.ts` using OKLab-verified Day/Night 5-stop
  tuples; inspect every tile in both lights for zero clipped noise or muddy mid-tones.
- **Adjusting bento grid layout, vertical Lantern auto-scroll, or variable typography**: edit `mesh/physics.ts`,
  `mesh/show.ts`, `mesh/main.ts`, `mesh/stage.css`, and `mesh/style.css`.
- **Updating the landing-page card**: edit `mesh/card.ts` and `mesh/card.css`, keeping all 4 live plates in
  one shared WebGL2 canvas, zero-race `:root` `--paper`/`--ink` ground math, and `data-theme` sync.

## Done means

`npm run check` and `npm run site` pass with zero TypeScript or console errors, and in real GPU Chrome on
`npm run mesh` (http://localhost:5400/):
- Confirm `Cabinet Grotesk` and `IBM Plex Mono` report `status === "loaded"` (zero 3-font clash).
- Inspect the pure 4-tile `8 + 4` Bento Grid across **Desktop (`1440 × 900`, Day & Night)**, **Tablet
  (`820 × 1180`)**, and **Mobile (`390 × 844`)**, confirming:
  - Zero `#horizon` banner, zero coloured box behind controls, and all 4 live optical tiles + frameless
    colophon fit cleanly in one `1440 × 900` desktop viewport.
  - `01 Frosted Halo` and `02 Thin-Film Crystal` share pure `#FCFCFB` porcelain / `#070913` obsidian ground
    with zero painted sky-box behind crystals, zero circular Phong orb dots, and zero equator aliasing on `dome`.
  - `03 Atmospheric Plumes` preserves crisp 2-column Swiss poster grids with `Cabinet Grotesk`, `1 px`
    `.plume-rule` hairlines, and readable Night Sheet 01 ink contrast.
  - `04 Backlit Vessels` spans full height on the right in `#070A10` obsidian with a clean empty top-right
    corner, auto-scrolls vertically every `2.6 s` with Y-axis anamorphic trails, pauses on hover, and snaps
    `Cabinet Grotesk` labels sharp (`wght 560`, `filter: none`) at center lock.
  - Off-screen tiles burn `0` `gl.drawArrays` calls; `.mesh-show` on `site/dist/index.html` and
    `site/dist/mesh/card.jpg` render cleanly.
