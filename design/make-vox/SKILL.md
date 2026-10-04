---
name: make-vox
description: Build a Vox-style LAYERED-COLLAGE vertical short end-to-end — script + scene dissection into image layers, layer production (AI images via gen_image.py + cutout.py, HTML→PNG, SVG-in-TSX), choreographed TSX assembly on the collage kit (CollageBoard camera, parallax, cutouts, chips, routes), frame QA, render, then voice/SFX via the shared machinery. Use when the user wants a "vox style", documentary, or explainer-collage short, a map-travel or archival-history sequence, or to continue the vox-N series — the paper-collage look, not plain TSX animation (that is make-short) and not video-model pixels (that is make-ai-short). Defers raw TSX crash rules to vidtsx-2d-generator and SFX taste to suggest-sfx.
---

# make-vox — layered-collage documentary shorts, end to end

Every scene is DISSECTED into separate image layers (paper board, die-cut subjects, maps,
archival prints, label chips, arrows) and the TSX side choreographs the layers so they
assemble on screen. Polish = many simple staggered layer moves + a virtual camera — never
complex per-image animation. The visual language + architecture live in
**`vox-shorts/DESIGN.md`** (read it first); this skill is the build pipeline. Proven on
vox-1 (coffee).

Run everything from the repo root. Layer production needs extra Python deps (the only tools
in this repo that do): `pip install pillow rembg` (die-cuts) and `pip install playwright &&
playwright install chromium` (HTML→PNG captures).

## Artifact contract

```
vox-shorts/vox-N-<topic>/
  script.md        — beat sheet: per scene → on-screen layers + camera + (VO)
  scenes.json      — optional machine contract once voice lands (like beats.json)
  voice/ · sfx-plan.json · output/        (same machinery as the short-N flow) [voice/output gitignored]
remotion/src/shots/vox-N/VoxN<Name>.tsx   — THE composition
media/projects/vox-N-<topic>/layers/      — every generated layer + gen_image sidecars (committed)
```

Kit: `remotion/src/lib/collage.tsx` — `CollageBoard` (camera keyframes + parallax context),
`Cutout`, `ArchivalPhoto`, `PaperBG`, `LabelChip`, `SerifStatement`, `SketchArrow`, `Grain`,
`VOX` palette. Grow the kit generically; project-specific hacks stay in the shot.

## Format

1080×1920 @30, 35–45s. The hook grammar of make-short applies: composed frame 0,
loop-friendly tail, no CTA outros.

## Stage 1 — script + scene dissection

Write `script.md`: scenes with, for EACH scene — the camera move (anchor x/y/zoom), the layer
list (what image, which source, entrance + timing), annotations (chips/routes/statements).
Facts verified before scripting. A scene is 2–6 layers; if you can't name the layers, the
scene isn't designed yet.

## Stage 2 — layer production (cheapest source that works, reuse first)

- Photographic subjects / textures / maps / archival prints → `python tools/gen_image.py`, then
  `python tools/cutout.py` for die-cuts (rembg auto; white-key is the no-deps fallback and
  FAILS on contact shadows — don't fight it, install rembg).
  - Maps/archival: prompt "NO text, no labels" — AI text is gibberish; chips annotate instead.
  - Cutout subjects: "isolated on plain white background" still helps rembg edge quality.
- Charts / UI / documents / styled text blocks → HTML file + Playwright screenshot
  (`python tools/capture_web.py`, `omitBackground` for alpha).
- Arrows, routes, shapes → SVG **directly in TSX** (SketchArrow etc.) — never rasterize.
- Layers land in `media/projects/vox-N-<topic>/layers/`; anything reusable by 2+ videos
  graduates to `media/library/`.

## Stage 3 — TSX assembly (the choreography)

- ONE `CollageBoard cam={CAM}` at the root; scenes are `<Sequence layout="none">`s INSIDE it
  so the camera travels ACROSS scene boundaries. Cam keys are GLOBAL frames; entrance `at`s
  are LOCAL to their Sequence (the classic local-frame bug — check every cue).
- Persistent scenery (a map under two scenes) gets its own long Sequence; annotations get a
  shorter one wrapped in a fade-out so they leave before the next scene composes over them.
- Geometry pattern: place big layers via constants (`MAP = {cx,cy,w}`) and derive annotation
  positions as fractions of the layer (`mapPt(0.24, 0.52)`), so re-generating art only means
  re-eyeballing two fractions.
- Depth taste: background board −0.06, scenery 0–0.05, foreground props 0.08–0.15. Every
  layer keeps its idle drift (default) — nothing fully freezes.
- **Contrast rule (locked):** `SerifStatement` over any busy layer (map/photo) MUST use
  `backing`; light-accent chips (VOX.yellow) need dark `kickerColor`. Headlines are
  FONT_EDITORIAL (Source Serif 4 @700) — don't swap fonts per video.
- Hard rules (frame-based only, monotonic interpolate, Easing.bezier, `<Img>` never `<img>`)
  → vidtsx-2d-generator.

## Stage 4 — QA (do not skip; it caught real bugs on vox-1)

```
cd remotion && npm run gen
node scripts/frames.mjs VoxNName <f0,entrance-cues,camera-arrivals,transitions,last> --scale=0.5
```
READ every PNG: every entrance landed · camera framing at each arrival (nothing critical
cropped) · text contrast over its actual background · cutout edges clean (re-cutout, don't
mask in TSX) · scene handoffs (fading annotations gone before the next scene needs the space).
Then `node scripts/render-all.mjs VoxNName --scale=1` and spot-check frames FROM THE MP4.

## Stage 5 — voice

`python tools/gen_voice.py --beats … --emit-ts` exactly as make-short Stage 4 (word-exact
captions if the format wants captions; documentary style often runs caption-free).

## Stage 6 — SFX/music (suggest-sfx machinery)

Collage taste: paper slides on entrances, soft thuds on `place` landings, whooshes on camera
moves, route-draw scribbles — sparse and editorial, decorative cues `optional: true`.
The user's ear is the audit gate.

## Done =

script.md scenes each name their layers · all layers generated + sidecars in media/projects ·
composition QA'd at cues and from the final mp4 · contrast rule honored · voice + SFX when
requested · kit additions generic.
