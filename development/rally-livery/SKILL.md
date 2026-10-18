---
name: rally-livery
description: Create, change and debug the livery (paint scheme) of an imported Gravel Rally car - the runtime atlas painter, chart seams, panel-line edges, checker/stripe grids, and every debugging technique we used (camera links, chart tinting, debug grids, chart-probe, normals, chartBoxes). Use when the user wants a livery painted or fixed, reports a paint glitch (white line, spike, tooth, spill onto a neighbouring panel, wrong colour on one side), or sends a car-viewer camera link.
---

# Rally liveries - create, update, debug

Worked example for everything below: `src/games/rally/cars/bimmer-m3/` (`livery.ts`; `model.source.json` `atlas.chartBoxes` (each with a `$comment`) = the overrides it needed and why, summary in `DETAILS.md` "Livery chart boxes"; `DETAILS.md` "Bonnet" = fitting an outline to crest + seam lines). Import workflow of the car itself: `.claude/skills/rally-car-import/SKILL.md`. Procedural cars
(`cars/shared/livery.ts` canvas atlas) are a different, simpler system - this skill is for **imported STL / GLB cars** whose
body is painted by `<car>/livery.ts`.

## 1. How the paint reaches the car

- `stl-to-glb.mjs` gives every BODY triangle to ONE **chart** by the direction it faces (largest normal component): `left` /
  `right` (+x / -x), `top` / `bottom` (+y / -y), `front` / `rear` (+z / -z). Each chart is a plain orthographic projection of
  the car laid out in metres in one atlas (`model.source.json` `atlas`: `pxPerMetre`, `bounds`, `charts` = chart origins).
  Glass, lamps, grille, wing, trim... are separate parts with their own materials and are never painted.
- `<car>/livery.ts` exports a `CarAtlas` whose `paint(ctx, info, seed)` draws in **model-space metres** with
  `atlasKit(A)` (`cars/shared/atlas-painter.ts`): `sidePx` / `topPx` / `frontPx` / `rearPx` give canvas px for a model point;
  the Bimmer / Skoda Rally `fill(ctx, chart, pts, style)` helper clips to the chart. Side shapes are drawn on both sides, the top chart
  is `(z, x)` with +x = the car's LEFT, side charts are `(z, y)`, end charts `(x, y)`.
- The same surface can sit on two charts (a quarter panel's crest, a bumper corner, a bonnet flank): triangles near the
  switch pick a chart by tiny normal differences, and **neighbouring triangles on different charts sample different texels**.
  Almost every glitch is this. The chart a face lands on is also what the texture there means: a vertical wall on the left
  chart reads the LEFT side's paint at its (z, y) even if it is a bonnet crease.
- Seed 0 = the reference scheme; other seeds reuse the shapes with `info.accent` / `accent2`. **No text, numbers or real
  brand logos** (door plate decal does the number; `rally-car-import` step 6).
- Edit `livery.ts` (instant, HMR). Edit `model.source.json` `atlas.chartBoxes` or the converter and you must rebuild the GLB:
  `node scripts/car-model/stl-to-glb.mjs <car>/model.source.json sources/cars/<car>/<car>-parts.stl` (dev server restarts
  itself; reload the page).

## 2. Creating a livery

1. **Start from a clean base** (body colour everywhere, dark underside on the `bottom` chart). Never trace photos
   automatically (tried on the GR Yaris, rejected). Save the user's reference photos to `sources/cars/<car>/` first
   (`source-files` skill) and list them in the car DETAILS.md.
2. **Ask what to keep**: sponsors, flags and text are out by rule; users usually want 2 - 4 big shapes (a band, a split line, a
   flag). Build one element at a time and look at it before the next.
3. **Per element: measure, don't eyeball.** Edges that follow a panel line, seam, crease or lamp come from the mesh (section 4),
   not from a photo or a hand-drawn guess; shape coordinates go in `livery.ts` as named constants with a comment saying what
   they were measured against.
4. **Shapes that cross charts** (a band over a roof edge, a flag round a bumper corner): put the boundaries so each seam falls
   INSIDE one cell/shape painted identically on both charts (section 5).
5. **Grids (checkers/stripes): build row by row** from the lowest row up, inspect each row (close-up, both sides, from behind)
   before adding the next. Constants (`CELL`, `ROWS`, `FIRST_COL`, `COLS_X`, `CREST`, `ROOF_X`) each get a comment naming the
   seam / lamp / ledge that fixed their value. A checker's solid-colour region ends on a stepped edge: start each row on a
   white cell ((col + row) odd).
6. **Mirror** symmetric elements with a loop over `[1, -1]`; the mesh is symmetric in height but NOT guaranteed in every face -
   always look at both sides.
7. Finish with the verification checklist (section 8) and update the car DETAILS.md "Livery" + TODO.

## 3. Updating / fixing a livery (the usual request)

The user sends a small, scoped fix, often a camera link. Do exactly that change (see the memory note
`livery-iteration-style`): open their view, find what is wrong, fix it, re-check the same view AND the mirrored view, report
what else you noticed without fixing it.

1. Open the link (section 4.1). 2. Name the chart of the bad pixels (4.2). 3. Measure the true edge/seam (4.3 - 4.6).
2. Fix at the cheapest level (section 6). 5. Re-render the same view; expect 2 - 3 rounds on an edge ("you over-corrected"
   means: fit to what their view shows). 6. Both sides + one wide shot. 7. Docs (section 8).

## 4. Debug toolbox

### 4.1 Cameras: look from exactly where the user looks

- Car viewer URL: `.../games/rally/car-viewer.html?car=<id>&cam=x,y,z&look=x,y,z&fov=<deg>&clean=1` (model space, metres, +z =
  nose, +x = the car's LEFT, y up; `clean=1` hides the panel; a small `fov` from far away is near-orthographic).
- The panel's **Pose -> "Copy camera link"** copies the current orbit (position, target, fov) as such a URL. The user's links
  point at THEIR dev server (port 3000): keep the query, replace the origin with your own preview's (`preview_list`), add
  `&clean=1`. If they say some links are "the back view / ignore those", use only the ones they say count.
- One `navigate` + `wait 7-8` + `screenshot` per view; batch several views in one `browser_batch`. Standard recipes (replace `X`
  by -1 for the car's right side):

  | View                                 | `cam` / `look` / `fov`                                                |
  | ------------------------------------ | --------------------------------------------------------------------- |
  | straight top-down on a spot (z0, x0) | `cam=x0,3,z0&look=x0,0.8,z0&fov=14` (image: front = down, +x = right) |
  | side close-up at ~1000 px/m          | `cam=X*2.6,1.4,z0+1&look=X*0.8,0.85,z0&fov=10..13`                    |
  | straight from behind, low            | `cam=0,0.75,-9&look=0,0.65,-2&fov=14`                                 |
  | rear 3/4                             | `cam=-4.2,0.9,-6&look=-0.6,0.62,-2.1&fov=10`                          |
  | roof / door top                      | `cam=-3.6,2.4,0.2&look=-0.7,1.0,-0.4&fov=22`                          |

- Look from the glitch's side AND from straight above: top-chart errors only show from above, wall/seam errors only at a low
  angle (a straight top-down view can look perfectly aligned while a 2 - 3 cm spill on a bevel shows from the side).
- ~300 px/m hides 2 cm errors. Use fov 7 - 13 from 2 - 6 m for edges.

### 4.2 Name the chart: tint the atlas in the page (debug only, nothing saved)

Paste via `javascript_tool` on the car-viewer page (find the body atlas = the canvas texture bigger than 1000 px; layout numbers
from `model.source.json` `atlas`, here the Bimmer M3's):

```js
let tex;
__carViewer.shell.scene.traverse((c) =>
  [].concat(c.material || []).forEach((m) => {
    if (m?.map?.image && m.map.image.width > 1000 && m.map.image.height > 2000)
      tex = m.map;
  }),
);
const x = tex.image.getContext('2d'),
  K = 256;
x.globalAlpha = 0.5;
const T = (c, cx, cy, w, h) => {
  x.fillStyle = c;
  x.fillRect(cx * K, cy * K, w * K, h * K);
};
T('#0f0', 0, 0, 4.75, 1.45);
T('#ff0', 0, 1.5, 4.75, 1.45); // left green, right yellow (side charts 4.75 x 1.45 m)
T('#f00', 0, 3.0, 4.75, 2.1); // top red
T('#0ff', 0, 5.15, 2.1, 1.45);
T('#f0f', 2.2, 5.15, 2.1, 1.45); // front cyan, rear magenta
x.globalAlpha = 1;
tex.needsUpdate = true;
```

(Chart rects: origin from `atlas.charts`, size `bounds.z` x `bounds.y` for left/right/front/rear-ish, `bounds.z` x `bounds.x` for
top/bottom - see `chart-probe.py` `chart_rects()`.) Reading it: interleaved tints on a surface = triangles of two charts
alternating (teeth); a strip of the wrong tint along a painted edge = faces that belong to another chart (walls, bevels,
ledges); then probe them (4.4). Reload the page to undo.

### 4.3 Read positions off the car: a debug grid

Draw lines of constant |x| (or z) into the top chart the same way, one colour per 5 cm (`canvas y = (chart.y + x - bounds.x[0]) * K`,
along z `canvas x = (chart.x + bounds.z[1] - z) * K`), then screenshot the user's own view. The lines lie on the surface, so
where a painted edge crosses which line gives its |x| directly - this found the bonnet-tip spill (blue at |x| 0.33 vs the
raised part's wall at 0.36) that top-down views hid.

### 4.4 Ask the mesh: `scripts/car-model/chart-probe.py`

```bash
python scripts/car-model/chart-probe.py <model.source.json> --box x0,x1,y0,y1,z0,z1 [--abs-x]   # per chart: tris, area, normal & position ranges in a box
python scripts/car-model/chart-probe.py <model.source.json> --seam rear                        # per height: where the side chart ends / the rear chart starts
python scripts/car-model/chart-probe.py <model.source.json> --profile z0,z1,x0,x1               # surface height grid (cm)
```

Typical use: a bad strip in box B -> run `--box B` -> "left 47 tris, normal y -0.7..0.7" tells you which faces (walls, ledges)
sit on which chart; `--seam rear` tells you the |x| / z where a cell edge must NOT be.

### 4.5 Find a panel line / seam / crest: use NORMALS, not heights

A bonnet/fender step, roof gutter or shoulder crest is a wall: outward-facing triangles with a low up-component (ny ~0.1 - 0.25).
Slice by z, list the |x| of those walls (numpy over the GLB's `body` primitive; see the snippets in `cars/bimmer-m3/DETAILS.md` or
`chart-probe.py` for the GLB reader). Rules learnt:

- the wall is ~3 cm wide and the visible seam is on its **outer** side (fitting the inner side left a white gap);
- a height profile misleads: it shows the later drop to the cowl (4 - 10 cm further out) not the seam;
- bevels add ~2 cm to a wall: keep a shape 1 - 2 cm clear of a wall it must not cross;
- crease walls inside a painted shape face sideways and land on side charts (white lines) - re-route them (6c);
- raw crease renders help: `python scripts/car-model/view-glb.py <model.source.json> out --views top --crop z0,z1,x0,x1 --scale 800 --grid 0.02`.

### 4.6 Geometry must not move

After any converter/`chartBoxes` change compare sorted vertex positions per primitive against the previous GLB (`np.allclose`):
only the UV chart assignment may differ. Keep a copy of the old GLB in the scratchpad before rebuilding.

## 5. Seam rules (how grids and shapes survive chart boundaries)

- **Put the seam inside one cell/shape painted the same on both charts.** Measure it first (`--seam`, normals), then choose cell
  edges around it: the Bimmer side's last column = the rear's outer column; the side's crest row = the top chart's outer cell.
- **A cell edge on a crest/seam makes teeth.** The quarter-panel crest at |x| ~0.72 inside a 43 cm cell -> clean; an edge at 0.72
  -> saw-teeth. Move the edge past the crest (or widen the cell).
- **One colour across a strip that holds several heights** (quarter-panel top + bumper ledge on the same top-chart strip): give the
  rows involved the same parity and colour, or two colours split at some x make teeth.
- **Rows aligned with features**: a row boundary at lamp top/bottom, bumper ledge height; cells behind a lamp are dropped (slivers).
- **Changing the column / row count moves every edge**: recheck each `chartBoxes` boundary (its `$comment` names the cell it relies
  on) and every edge near a lamp corner. Move a single bad edge on its own (`LAMP_EDGE_Z` in `cars/bimmer-m3/livery.ts`).
- **A thin line/strip sticking out of a shape** = a vertical wall or ledge on another chart at the shape's edge: route it onto the
  shape's chart (6c), never "fix" it by shrinking the shape.
- **Edges that follow a panel line**: outer side of the groove wall, 1 - 2 cm clear of walls you must not cross, and verify in a
  low-angle close-up on BOTH sides.

## 6. Fix levels (cheapest first)

a. **Move the outline** in `livery.ts` onto the measured edge (most fixes; HMR, instant).
b. **Make the charts agree** (cell/shape edges, colours, parity) - still only `livery.ts`.
c. **Re-route faces** with `atlas.chartBoxes` in `model.source.json` (rebuild GLB; cookbook below).

`chartBoxes` (converter `stl-to-glb.mjs`; boxes in model space, `x` is |x| so both sides; first matching box wins; every box needs
a `$comment` saying which glitch it fixed):

| Symptom                                                                                     | Box                                                                       |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| white lines / wedge through a painted top shape along a crease                              | `chart: top`, `minNy` -0.6 (also the sloped walls), box around the crease |
| thin strip/line beyond a painted roof/hood edge (a vertical edge wall on a side chart)      | `chart: top`, `minNy` 0.05 around the wall                                |
| arch flares picking up the paint of the opposite arch (end charts are shared front-to-rear) | `chart: side` boxes round each arch (front and rear arch separately)      |
| steep fender shoulder next to a painted edge turned into slivers                            | `chart: side`, `maxNy` 0.85                                               |
| horizontal ledge (sill, exhaust recess) needing the side's split line                       | `chart: side`, `maxNy` 1.01, `minNy` -0.2                                 |
| low bumper lip among colour rows takes the top chart's colour                               | `chart: rear` (or `front`), `minNy` 0.3                                   |

## 7. Symptom -> first suspect

| What you see                                          | Likely cause -> where to look                                                      |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| paint spills onto the neighbouring panel by 2 - 10 cm | outline measured from a height drop / inner wall side -> 4.5                       |
| white gap between paint and a seam                    | outline on the inner side of the wall / too far in -> 4.5                          |
| teeth along the edge of a stripe                      | cell edge on a crest, or two colours across one strip -> 5                         |
| a long thin line past the paint's end                 | edge wall on a side chart -> 4.2 + chartBoxes `top`                                |
| one square of the wrong colour among a row            | ledge/lip on another chart -> chartBoxes `rear`/`side`                             |
| paint on the wrong side of the car                    | the shape is on the `top`/`left` chart only; or non-mirrored loop -> `[1, -1]`     |
| bumper corner pattern breaks                          | seam not inside one cell -> `--seam rear`, 5                                       |
| blue specks in a lamp recess                          | rim faces of the recess: shrink the outline 1 - 2 cm from the rim; not worth boxes |
| a tooth / wedge of one cell at a lamp corner          | a cell edge on the curved lip there: raycast it, move that edge 1 - 2 cm past it   |
| texture looks soft/blurry                             | `pxPerMetre` 256 = 4 mm per texel; fine for 10 cm cells, don't paint 1 cm details  |

## 8. Gotchas and verification

- **Mute the game**: any URL that can start the game (`/games/rally/?car=...`) gets `&mute=1` (AGENTS.md "Sound while testing").

- **Blank viewer / `__carViewer` undefined**: the dev build is failing, usually ANOTHER session's file (a half-written
  `data.json`, a missing import). `preview_logs` (errors; grep "File:"), wait until it is valid, reload. Not yours to fix.
- **Screenshot timeouts ("pane not displayed")**: `tabs_select` the tab; if hidden/closed, `preview_start` with a `url`
  (new tab id, pass it explicitly). Do not retry a hung `navigate` in a loop.
- **Browser caches the GLB** after a rebuild: reload with a changed query (`&v=2`) if the old model shows.
- **Other sessions edit the same tree**: lint/tsc/test failures in files you did not touch are theirs - report, don't fix.
- Heredocs with apostrophes break in Bash; patch long files with Python slicing by unique anchors and `assert` they exist.
- Debug overlays are in-page only: they vanish on reload and must never be committed.

Verification before you say "done": `npx tsc --noEmit -p tsconfig.json`, `npm run lint`, `npm run test`; the user's view + its
mirror + a wide 3/4 + a top-down; for converter changes the geometry-unchanged check (4.6). Docs (short, `AGENTS.md` "Write short"): car DETAILS.md "Livery"
(the shapes and the one-line why of each seam fix, not the attempts), `TODO.md` (leftovers), `model.source.json` `$comment`s; add a new technique here when you learn one.
