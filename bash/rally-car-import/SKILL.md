---
name: rally-car-import
description: LICENCE GATE first, then an end-to-end checklist for importing a 3D car model (STL / print model / GLB) into Gravel Rally as a new car - orient and measure the mesh, split off glass / lamps / trim as real parts, convert, assign materials, paint the livery, bake the boxy profile (fallback body + street car), verify in the car viewer and document. Use when the user shares a car model to add, or when an imported car shows texture bleed, jagged part edges, wrong proportions, lean, white undersides or glare.
---

# Importing a car model (worked examples: `cars/skoda-rally/` GLB import, `cars/bimmer-m3/` single-shell print STL)

The order below is the order that worked. Every step has a check; skipping checks is how our first print-STL car went wrong
three times (crumpled fenders, lean, painted-on lights). API details live in `.claude/skills/rally-content/SKILL.md`
("STL bodies"); this file is the **workflow + the gotchas**. Scripts are in `scripts/car-model/`.

## Licence gate - FIRST, before any file is copied, scanned or converted

The repo is public (PolyForm Noncommercial, see `AGENTS.md` "Public repo and licences"). A converted model is a **derivative
work that we publish**, so its licence must allow redistribution of the file AND of derivatives. We learned this the hard way:
our first car (a Printables STL: "no modifying, sharing, hosting") and the Bimmer (MakerWorld Standard Digital File License:
"no distribution of derivatives") had to be scrapped / replaced after weeks of modelling. Check **before** investing time.

1. **Find the licence text.** Open the download page (URL from the user) and read the licence block + the description (authors often add
   "no redistribution", "ask before use", "membership for commercial use"). Printables blocks bots (Cloudflare challenge: do not
   try to bypass it) - ask the user to paste the licence text. Also check every extra file you will use (wheels, tyres, interior,
   textures): each can have its own licence.
2. **Quote it.** Put the licence name, the verbatim restriction sentence, the author, title and URL in the car
   `DETAILS.md` links table (create the folder + file now; **never write "TODO" for a licence and carry on**).
3. **Give a verdict** and report it to the user before step 0:

   | Licence found                                                                                                                                                                                                                                                         | Verdict                                                                                                                          |
   | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
   | CC0 / public domain                                                                                                                                                                                                                                                   | OK                                                                                                                               |
   | CC BY 3.0 / 4.0                                                                                                                                                                                                                                                       | OK with attribution: author, title, link, licence in `CarDef.credit`, `DETAILS.md`, `THIRD-PARTY.md`, `public/models/CREDITS.md` |
   | CC BY-NC / BY-NC-SA                                                                                                                                                                                                                                                   | OK for this noncommercial project with attribution; mark it NC in the docs and ask the user (a commercial fork could not use it) |
   | CC BY-SA                                                                                                                                                                                                                                                              | the converted GLB must itself be CC BY-SA: conflicts with our licence for that file - ask the user, usually decline              |
   | any ND ("no derivatives"), "Standard Digital File License", "personal use only", "no sharing / hosting", fan / manufacturer licences (Škoda), editorial-only, paid / royalty-free store licences (TurboSquid, CGTrader, Sketchfab Standard), models ripped from games | **NOT OK: stop.** Converting is modifying and publishing is distributing                                                         |
   | no licence, unreadable page, "all rights reserved", licence cannot be confirmed                                                                                                                                                                                       | **NOT OK until confirmed** - ask the user to paste it; unknown is treated as forbidden                                           |

4. **If NOT OK: stop and tell the user the options** - ask the author / owner for written permission (keep the mail in the DETAILS),
   model the car from scratch from photos and blueprints without touching the file (the Zastava route), or use the file purely locally as "bring your own" (git-ignored GLB, car only
   `hideInProd` in `CARS_LIST`, boxy fallback body (`model.profile`, step 6c), docs say where to download it; the live site still cannot host it). Do not add the GLB
   to `public/`, git, tests or the release lists without a green verdict.
5. **Other things to rule out:** brand logos / badges / wordmarks baked into the mesh or textures (remove them, no manufacturer
   or sponsor logos in liveries), real number plates, and reference photos (never shipped, never traced from the mesh).
6. Record the verdict (and the decision) in `THIRD-PARTY.md` the moment the model ships, and keep `public/models/CREDITS.md` in sync.

## 0. Sources first (`.claude/skills/source-files/SKILL.md`)

- Copy every file the user shares to `sources/cars/<car>/` (kebab-case, numbered in the order given) and list each in
  the car DETAILS.md (sources table, links table with the verified licence from the gate above).
- Pasted chat images are only saved to disk when the harness gives a path. If a reference arrives without one
  (mid-turn message), say so in the DETAILS.md ("not saved as a file") rather than inventing a file.
- Look at the reference photos **before** touching the mesh and write down what must be black / carbon / glass /
  coloured (grille, intakes, vents, splitter, mirrors, scoop, wing, window frames, door handles, sills, lamps,
  rear-window vent panel, reflectors, calipers, dampers). That list becomes the parts list in step 4.

## 1. Look at the raw mesh before anything else

```bash
python scripts/car-model/scan-mesh.py <model.stl>                      # real panel edges or a blob?
python scripts/car-model/segment-stl.py <model.source.json> <in.stl> <out.stl> --preview seg --by segment
```

- **The scanner's verdict is a gate** - run it on the raw download before `sources/` bookkeeping, `model.source.json` or a
  `CarDef`, and report it to the user:
  - **already split** (glTF with several primitives / materials / named nodes): import as glTF, map the names in
    `cars/shared/part-materials.ts`.
  - **real panel edges** (hard edges > ~2 % of edges, dozens of crease panels @ 25 deg, largest < 60 % of the surface - CAD /
    print solids, e.g. 132k triangles, watertight, sharp creases): import; the `seeds` picks of step 4 grab every
    part exactly.
  - **blob** (largest panel > 90 %, hard edges < 1 % - photo / image-to-3D meshes like the GR Yaris STL): **abandon the
    model**. Its features are shallow rounded grooves in one smooth skin; every part border would have to be hand-drawn through
    a groove and cut (`region` / `box` picks in `rally-content`, "STL bodies"), which cost a day for the Yaris and never got
    crisp. Document the rejected file in the DETAILS.md and tell the user what to look for instead: a CAD / print model that comes
    as separate shells or with real recess walls. Do not start the import "to see how far it gets".
- **Print kit?** If the scan reports odd extents (e.g. 3.4 x 4.3 x 0.6 m "car") the STL is a model KIT: every part a
  separate shell laid out on a sprue frame. Assemble it first (step 1b), then scan / segment the assembled STL.
- The licence was checked in the gate above; do not start on a model without a green verdict.
- **Brake discs, hub caps and wheel faces are not body.** A GLB often ships them as their own primitive next to the rims
  (Fabia: `mat_15` = four 0.34 m plates, once guessed to be "sill strips" and sent to `trim`). The game builds its own wheels,
  tyres, brake discs and calipers (`stl-wheel.ts`, `car-model.ts`), so anything round and flat at a hub goes into
  `gltf.drop`. They only show with the wheels hidden or open-spoked, in the car viewer with `tyres=0&rims=0` (body + brakes).
  `glb-to-parts-stl.py --list` the primitives, and **never guess a primitive's content from its material name**: check the
  bbox (a plate centred on a hub, 4 x same triangle count = discs). The importer also prints a `defaulted` list and a
  `WARNING disc-like islands` list after every run - read both, fix every entry, rerun until neither prints.
- Check **what the mesh contains**: a print body can have **no wheels** - the printed wheels / tyres are separate STLs
  that clip onto stub axles inside closed arches. Cutting a tyre-sized hole there tore the fenders. Cut only what is
  really there (`wheels.radius` 0.16 for the stubs). The wheel / tyre STLs became `wheel-stl-to-glb.mjs` input.
- Check orientation: print models are exported in print-bed pose (one was pitched ~52 deg). PCA
  (`orient-tilted-stl.py`) finds the long axis but leaves a **roll** - fit it by left / right symmetry of the height
  profile (roof edges within 3 mm) and a **pitch** by levelling the front / rear hubs. Check with a front view, not
  only a side view - a 2.5 deg lean is invisible from the side and obvious from the front.

## 2. Measure, then set `model.source.json`

- `scale` from the real wheelbase or body length; `offset` x from the body's centreline (one print was 2.7 cm
  off), y from "hubs at tyre radius" (a print sat on its sills: `offset` y = 0.104), z so the front hub is at
  physics `front.z`. Put the measured numbers (hub z / y, track) in the DETAILS.md build notes.
- Physics: start from the closest existing car and adjust mass / power / wheelbase / track / tyre radius; add the
  car's band to `tests/rally/vehicle.test.ts`.
- Triangle budget: 60k. At 45k the simplifier crumpled fenders and arches; above 80k gains nothing. **Compare the
  simplified GLB against the raw mesh** with a plain material before believing any texture problem is a texture
  problem (`view-glb.py` draws the GLB; `segment-stl.py --preview` draws the raw mesh).

## 3. Verify the model naked

Load the car in `/games/rally/car-viewer.html?car=<id>` with a plain livery (body colour only) and check: level
from the front, wheels centred in the arches, nothing see-through, no crumpled panels, hubs at the right height.
Wheels / rims: add `&wheels=1&wcam=FL&body=0` (wheel debugger: fixed hub crosshair + tyre / bead circles, arch fit with
its offset, near-ortho camera along the axle) and compare `wangle=0` with `wangle=180`, zoomed in on the hub (`cam=20,<R>,<z>
&look=<track/2>,<R>,<z>&fov=0.9`) - a rim off its axle shows as the hub bore moving round the 2 cm ring. Judge centring
only in that ortho view: in a 3/4 perspective a deep dish makes a centred hub look off. Print-model wheels may be
cambered: de-camber before centring (`stl-wheel-extract.py` `axis`, worked example `cars/bimmer-m3/` "Rim").
A GLB rim's barrel is often a one-sided tube: it vanishes from the axle side and the rim looks see-through (ground shows
between the spokes). Look into the dish from an angle; fix with `wheel-stl-to-glb.mjs --two-sided 20` (back faces for open
shells) and `--bridge x0,r0,x1,r1` when the barrel stops short of the lip (worked example `cars/peugeot-206/`).
Lamps: check them in the dark too - `&tod=1&beam=0&view=rear&lamps=on` (running lamps; `off` = dark), `lamps=brake`, `lamps=reverse`, and `tod=17.5`
(evening). A bright red glow turns salmon pink under the night tone mapping (AgX): glow maps in pure red, and a `LampNight` (`RED_NIGHT`,
`LENS_NIGHT`...) on every red lamp material in `part-materials.ts`; that also gives the lamp its halo (`lamp-halo.ts`).
Only then start on parts and paint - texture work on a bad mesh is wasted twice.

## 4. Split accent parts off the body (never paint them)

Painting glass / lamps / vents on the body atlas bled colour across overlapping projections and gave saw-tooth
edges. Parts are separate primitives with their own materials instead:

```bash
python scripts/car-model/orient-tilted-stl.py <in.stl> <oriented.stl>                  # if tilted
python scripts/car-model/segment-stl.py <model.source.json> <oriented.stl> <parts.stl> --preview parts
node scripts/car-model/stl-to-glb.mjs <model.source.json> <parts.stl> --preview atlas.png
python scripts/car-model/view-glb.py <model.source.json> check                          # borders after simplification
```

Picking workflow (`parts.picks`, first pick wins):

1. Render `--by segment` views (front, rear, left, right, top at ~400 px/m) and read seed coordinates off the
   grid: `["front", x, y]`, `["left", z, y]`, `["top", z, x]`. Seeds pick the patch _seen_ at that point.
2. Thin strips (window frames 1 - 2 cm, belt mouldings) need `--grid 0.02 --scale 2600 --crop a0,a1,b0,b1`; a seed
   2 mm off lands on the door. The script prints when a seed lands on another pick - read those lines.
3. Clusters (165 grille patches, intake fins, vent frames) use `inside` boxes; small parts get `maxArea` so a
   missed seed cannot swallow a door (`door handles`).
4. The two sides are often creased differently (window frames, sail panels, arch flares): use
   `mirror: false` with per-side seeds, and drop a part rather than have one side black and the other white.
5. Wheel arches: walls by `inside` boxes; the inward-facing **lips** and the panel behind the front wheel by the
   per-triangle `hub` rule (faces the wheel centre, within radius) - creases are not reliable there. Give it `maxY`
   just above the arch tops: a downward-facing body-line step above the arch is "facing the hub" too and turns into a
   black streak (Bimmer). The flared
   band _outside_ the arch stays body colour (as on the real car); keep paint off it (step 6).
6. Glass: front windows `glass`; rear door + quarter glass `ventglass` (black top panel with vent openings,
   `parts.wrap: side`); lamps `headlight` / `tail` (`parts.wrap: corner`, u from the car's centre outwards, v top
   down) - draw their textures in that 0..1 space after rendering the part's UV layout (a headlight can be a
   widening blade; the layout decides where modules and light guides go).
   Fit the art to the part's **own outline**: draw the lamp shell's triangles in its wrap UV space (u = |x| - |z|, v =
   y, fitted 0..1) and put the round lamps in the lobes / cut-outs of the housing - that alignment is what makes the car
   recognisable from the front (Bimmer). Lamps that should sit back in the housing: a parallax barrel in the material
   (`lampDepth` in `part-materials.ts`, barrels along the car's forward axis; `facing: -1` for rear lamps), not new geometry. A print model's
   domed lamp glass (a bulge over each bowl) gets `parts.flatten` (one smooth cover through the lamp outline, `stl-to-glb.mjs`).
7. Materials by name in `cars/shared/part-materials.ts`; add names there, never per-car material code. Clearcoat on
   dark parts (grille, wing) reflects the sky and reads grey - keep `clearcoat` <= 0.6 and `envMapIntensity` ~0.5
   on blacks and carbon. Calipers / damper colours come from the CarDef (`rim.caliper`, `false` = none; `suspension.damper`).

Check each part close up in the viewer (lamp, vent, wing, arches **with the wheels hidden**:
`__carViewer.model.tires.visible = false; __carViewer.model.rims.visible = false`). The GLB render of
`view-glb.py` must show the same borders as the raw-mesh preview.

### 4b. If the body is a blob anyway (lessons from the GR Yaris, since deleted - it predated the scan gate)

Only for a car that is already in the game; new blobs are rejected in step 1. The Yaris was abandoned after all of this. Per-triangle picks (`region` outline in a
view, `box` in model space - API in `rally-content`, "STL bodies") with these lessons:

- **Find the feature on the mesh, not in a photo.** Render the raw mesh with crease highlighting (triangles whose dihedral
  angle to a neighbour is > 14 deg) at **1200 - 1600 px/m per feature** - a blob's "edge" is a rounded groove 2 - 4 cm wide,
  invisible at 300 px/m. Read coordinates **relative to the labelled grid lines** of a zoomed crop: the image viewer rescales
  pictures, absolute pixel maths on a wide render was wrong by 0.4 m once.
- **Windows**: trace the middle of the frame band once; glass = that polygon with `grow: -0.016`, frames = the whole glasshouse
  (B pillar included) with `grow: +0.018`, glass picked first (first pick wins). Windscreen / rear screen from the top view;
  the rear screen runs from the roof's rear bend to **under the wing blade** (stop it at the blade and a white sliver of hatch
  shows between the two).
- **Vents / lamps / badge**: generate the outline (stadium between the two rounded ends, ellipse, circle) instead of hand-typing
  20 points, and pick the louvre **slot**, not the bulge around it. The Yaris headlight is a recess plus a slim light bar that
  runs along the bonnet lip to the badge - one polygon.
- **Cuts must be exact**: straddling triangles are clipped against the outline (Sutherland-Hodgman, concave outlines ear-clipped
  into convex pieces). Snapping only the nearby border vertices leaves a saw-tooth at triangle size, and a single-line cut per
  triangle is wrong on 20 cm sliver triangles. After every cut the triangle list is re-indexed - any mask from an earlier pass
  (the mirrored side) has to be re-indexed too, or materials land on random triangles.
- **Mirroring**: a `region` on the left view is reused for the right view with the **depth range negated** (x -> -x); forgetting
  that leaves one side of the car without windows and is invisible from the usual camera.
- **Boxes catch what is under them**: wing uprights by their side faces only (`facing: {"|x|": [0.55, 1]}`), the blade split
  into a top box and an underside / leading-edge box (`facing y <= 0.55`), the antenna box a few cm wide - otherwise roof and
  hatch triangles turn carbon in jagged squares.
- **Undertray** = steep down-facing surfaces (`facing y <= -0.6`) below the belt, plus a **lower lip** region cut at the
  intake line (y 0.27): the whole lower bumper is black on a rally car. A looser facing (`-0.25`) grabbed the door skin's lower
  curl and drew black scratches across the doors.
- Each segmentation of a 500k-triangle mesh is ~80 s + 30 s conversion: batch several outline fixes per run, and check the
  `--by part` preview at 300 px/m before converting.

## 5. Body finish

`gltf.matte: true` for a matte car. Pure white paint clips in sunlight and glares on HDR monitors: use an
off-white (`#e9e6dd` pearl) and leave the exposure to `engine/display.ts` (`?display=hdr`, options menu).

## 6. Livery (`<car>/livery.ts`, body atlas only)

- Coordinates are model-space metres; a shape is painted per chart (left / right / top / bottom / front / rear).
  Use the `fill(chart, pts, style)` helper pattern from `cars/skoda-rally/livery.ts` (solid or gradient between two model points).
- **Anything that wraps a corner must use the same y range on the side and end charts** and run all the way to
  the next feature (arch, lamp). Different shapes per chart show as a saw-tooth seam where triangles switch chart
  (seen on a rear bumper band).
- Keep paint off arch flares and lips: start side stripes at the door's front shut line, stop bumper bands short of
  the arch. Stop top-chart paint at the tailgate edge (z) or it lands on the bumper's top ledge.
- The atlas needs a real `bottom` chart (`charts.bottom` with room in the atlas) - without it every downward face
  shares one white texel (bumper undersides showed white). Paint the underside dark, colour it where a band wraps
  under a corner.
- Symmetric sides: draw once, apply to both charts. Asymmetric middle: `mirror = false` on top / rear / front.
- No brand names or sponsor logos: car number (`info.number`), model name, generic team words only.
- Seeds: seed 0 = the reference scheme; other seeds reuse the shapes with `info.accent` / `accent2`.
- Verify from side, front 3/4, top, rear 3/4, and low rear (underside) - one page load per screenshot in the
  browser pane.
- **Photo tracing is a last resort, and never all at once.** Warping press photos into the atlas (one 2D
  warp per view + per-axis stretch pairs, letters dropped, plates kept as quads) gave a livery the user rejected outright -
  the mesh and the real car differ by centimetres everywhere, so every edge was slightly off and the whole looked smeared.
  The user prefers to **start from a clean base colour and add livery elements step by step, guided**. If a photo trace is
  still wanted: measure the wheel centres in each photo with a zoomed crop (a 4 cm error on the right-side photo shifted that
  whole side), draw `--debug` overlays of warped photo on mesh edges per view, and expect to tune `stretch` pairs.
- No text at all in the atlas (no sponsor words, no painted numbers): the number + rally name live on the door-plate decal
  (`cars/shared/rally-badge.ts`, `model.doorBadge`). Sponsor plates, if any, are plain coloured boxes.

### 6b. Debugging livery glitches -> `.claude/skills/rally-livery/SKILL.md`

Livery creation, edge/seam fitting and every glitch-debugging technique (camera links, chart tinting, debug grids,
`scripts/car-model/chart-probe.py`, normals for panel lines, `atlas.chartBoxes` cookbook, symptom table) live in the
**`rally-livery`** skill - read it before painting or fixing a livery. In short: a glitch is a triangle on a chart you did not
expect, or two charts that disagree where a surface switches; find which, then move the outline, make the charts agree, or
re-route the faces with a `chartBoxes` entry (rebuild the GLB, verify the geometry did not move).

## Lessons from `cars/bimmer-m3/` (CC BY single-shell print STL, 2026-10-04) - read `cars/bimmer-m3/DETAILS.md` for the numbers

- **Axes must be a proper rotation** (`["x", "z", "-y"]` for a bed-pose print): a swap mirrors the mesh and inverts every normal (renders
  show the floor from the top). Scale from the wheelbase measured between the tyre contact patches.
- **Crease angle 12 deg** (not 25) when the panel gaps are engraved grooves (scan verdict "marginal"): every pane and panel becomes its
  own segment.
- **Borders on smooth panels are `region` outlines, never `box` / `inside` / seeds**: the outline clips straddling triangles exactly
  (clean edges); boxes take whole big skin triangles by their centre (ragged patches, spikes). `region.any: true` also cuts triangles
  an earlier segment pick labelled; cut pieces keep their label. Segment picks run BEFORE region cuts.
- **Pipes / bars fused into the body** (merged with the floor pan into one segment): a `segment-stl.py` `tube` pick per pipe
  (`path` read off exact z cross-sections, `radius` just over the pipe's, `over: ["trim"]`). Facing-filtered boxes trade pipe and
  skin triangles near the tips.
- **Underside boxes**: only for surfaces hidden from normal views; a face visible from behind (bumper ledges, slanted lower faces)
  stays livery. A `"|x|"` facing takes both sides' outward skin too - for inward faces use one `mirror: false` pick per side.
- **After each rebuild, re-open every camera link the user sent this session**: per-triangle fixes often regress an earlier view.
- **Modelled wheels**: label them with a `region` circle as a material listed in `parts.drop` (exact opening, no saw teeth on arch lips);
  keep underbody / axle `inside` boxes out of the wheel area; add `wheels.liner` (+ `floorY`) so the wells are not see-through, and make
  the car's atlas black + `matteRect` at the matte texel the liner uses.
- **Gaps in the source mesh** (glass that stops short under the wipers): `parts.fills` patches.
- **A part to rebuild** (a grille whose thin bars look weak): drop the source shapes with a `region` rule -> `logo`, build the new bars / badge from `parts.solids` (convex prisms in a tilted frame, optional bevel; worked example `cars/citroen-c4/`).
- **Textured lamps** (`'corner'` wrap): draw the lamp in `part-materials.ts` (`tailC4Maps`: stripes, dot matrix, ribs, reverse lens) and map the lamp's `Phares` rule to it.
- **Recess walls in a bumper** take the side charts' flank colour: `atlas.chartBoxes` `{ chart: 'rear', any: true }` puts every face in the box on the rear chart.
- **An open slot / tunnel in the body** (the GT2's fender slot beside each tail lamp, `cars/bimmer-gt2/`): close it with a `parts.solids`
  wall (`chart` + `at` = one flat livery colour; without `chart` a solid has no atlas UVs), paint the slot's own inner faces one colour
  with `atlas.flatBoxes` (`maxNx` keeps the outer skin's livery), and add `atlas.backBoxes` (reversed copies) where its skin is seen from
  inside and culled. Put all three in the `recess` material (add it to `parts.materials`; boxes take `material`): the livery in shadow
  (`CarModel.recessMaterial`), since the lighting has no ambient occlusion and the plain livery lights a tunnel like the outer skin.
- **Look from below** (hide the viewer's ground plane; a z-buffer of the GLB from below finds faces looking up = holes).
- **Livery edges from geometry**: a top-down curvature map (d2y/dx2 of the highest-surface heightmap) shows crests (convex) and seams
  (grooves) - read their x per 5 cm of z and use them as the shape outline (`cars/bimmer-m3/livery.ts` hood).
- **Ride height vs hull**: the lowest believable stance is set by the stages (a test-map dip needed ~9 cm of hull clearance) and by
  `hull-fit.test.ts` (hull at most 3 cm above the real underside) - do not lower the body below that; the wheel-to-arch gap is then
  a wheel-size question (`wheelRadius`, tyre sizes).
- A new tyre fitment changes the car's character: `car-setup.test.ts` ("Bimmer wins on tarmac") needed `front.grip` 1.06 once 300-wide
  race tyres were replaced by street 245s.

## Lamps on a print model (Bimmer tail lamps, 2026-10-06) - worked example `cars/bimmer-m3/` + `TAIL` in `part-materials.ts`

- **Trace lamp edges on the SOURCE STL, not the GLB** (the GLB is simplified, its groove walls are patchy): rasterise the outermost
  surface per 1 mm cell in the view (exact per-triangle barycentric fill - point sampling leaves holes that read as fake grooves),
  high-pass it (minus a gaussian, sigma ~6 cells), take the weighted centre of the dip per row / column, fit a smooth curve,
  and draw the result over the depth image BEFORE writing picks. The lamp ends on the groove's lamp-side wall.
- **A dark seal in the groove** = its own part material (`seal`), the groove centre +- half its width, picked AFTER the lamp
  picks. Ends must meet the next dark line (top rim, divider) or they read as "not connected".
- **A region's `depth` decides what it can take**: a side-view lamp outline with depth from |x| 0.55 grabbed the rear face above a
  lower neighbouring piece (a red wedge). Start each pick's depth at the piece boundary.
- **Every outline vertex and every crossing of a dense source mesh is a kept border**: a 100-vertex seal on the groove took 3k
  triangles from glass / lamps under the fixed `targetTriangles`. Resample outlines to ~1 cm (check the chord error), raise the
  budget, and compare the per-part counts in the converter's `output:` line before / after.
- **`corner`-wrap UVs** (u = |x| - |z|, v = y, fitted 0..1 to the part's extreme vertices): moving any outline end rescales the
  texture - re-measure the `end` table / constants from the GLB after a rebuild. A mesh edge at constant |x| is a SLANTED line in
  u (the lamp face leans): measure u per v and draw dividers along it. u / v texture px are not square: size round things in
  metres via px-per-metre (`PXU` / `PXV`) or they come out as tall ovals.
- **Lamp light layers** (one emissive map scaled idle -> brake): tail-light parts full in it, brake-only areas ~20 % (the map is
  sRGB: `#78` is ~19 % linear; brighter washes red to salmon); `reverseGlow` = the reversing section only; indicators never lit.
- **Graphics that wrap a corner look flat** without depth: keep LED rings etc. on the faces that look at the viewer (mean normal
  per u band from the GLB).

## Tools added 2026-10-04 (Fabia + Bimmer round 2)

- **`near` rule** in `glb-to-parts-stl.py` (`gltf.parts`): `{"mat": "Car_body", "near": {"mat": "mat_25", "z": [..], "d": 0.05}, "material": "trim"}`
  = body triangles whose centre is within `d` of another source material (black screen borders / A-pillars of a GLB car). Centre based:
  big triangles crossing the line leave small spikes.
- **`region` rule** in `glb-to-parts-stl.py` (`gltf.parts`): `{"mat": "Car_body", "region": {"view": "front", "poly": [[x, y], ...], "depth": [zmin, zmax], "mirror": true}, "material": "trim"}`
  = exact outline cut (model coordinates, convex polygon): triangles are clipped along the outline, no saw teeth (bumper intakes).
- **`uv` rule** in `glb-to-parts-stl.py` (`gltf.parts`): `{"mat": "Car_body", "uv": [u0, u1, v0, v1], "x": [0.28, 1], "material": "<lamp part>"}` = triangles whose
  TEXCOORD_0 centroid lies in that texture rectangle (v down). For models that paint lamps into the body texture: each lamp is its own UV island, so
  this is exact, and the lamp's art can be cut out of the texture rectangle into a lamp sheet (check orientation: correlate UV u / v with
  |x|-|z| / y of the triangles; the `corner` wrap fits the part bbox, u from the centre outwards, v top down). Needs to come before any `region` of the same primitive.
- **Modelled lamps with their own (photo) texture**: send each lamp node to a `corner`-wrap lamp part, list both sides'
  nodes in `lampSheet` (`model.source.json`) and run `bake-lamp-sheet.py <model.source.json>`: it paints the source triangles into the wrap
  space (lens over housing) and prints the sheet rectangles for a `part-materials.ts` table. The sheet has three rows:
  base colour, emissive, normal map. A low-poly lamp gets its depth from those two maps - use them, or it reads flat. For real 3D
  round lamps, `gltf.lampCups` (`glb-to-parts-stl.py`) builds reflector cups + bulbs behind the shell and the lens material gets
  see-through windows over them.
- **Modelled lamps without textures** (plain emissive shells, `cars/bimmer-gt2/`): send them to the stock `lenscover` / `headled` / `amber` /
  `brakecover` / `tailled` parts. A shell with no housing behind it shows the ground through the lens: add a `parts.solids` prism
  (`lamphousing`) just behind it.
- **Tilted model** (modelled at an angle to the axes): `glb-orient.py <in.glb> <out.glb> --heading <deg> [--shift x,y,z] [--scale k]` turns the scene
  about y (heading = atan2(dx, dz) of the front / rear wheel centres) and centres it, so the `gltf.parts` boxes use the car's own axes;
  `--scale 100` for an FBX export in centimetres (worked example `cars/subie-22b/`).
- **`adjacent` pick** in `segment-stl.py`: small segments touching an earlier-picked material; and for frames that are NOT own segments
  (smooth skins) use a `region` with the glass outline (shapely union of the glass triangles in the view) + `grow`.
- More `gltf.parts` options (2026-10-04 evening): `facing` (normal component ranges, `"|x|": [0, 0.6]`) on a rule or inside `near`
  (sample only the windscreen / rear screen when the side windows share the glass material - otherwise the body round the side
  windows turns black); `whole: true` (the x / y / z box must contain the whole connected island: wing, scoop, mirror glass, a
  rear-screen frame welded into the body primitive, without nibbling the panel next to it); `islandTris: [min, max]` (islands of
  that size, e.g. the A-pillar end of a roof-rail island). Find islands first: weld + union-find over one material, print bbox /
  size / mean normal, render them in random colours - then write the boxes.
- **`arch` rule** (`{"arch": {"axles": [z, ...], "y": hub y, "r": [0.28, 0.5], "toward": 0.3, "|x|": [0.45, 1], "dy": -0.25}, "material": "trim"}`,
  source coordinates): body triangles round each hub whose normal points at it = wheel-arch liners and inner flare faces modelled
  into the body primitive, so the arches are black, not painted (worked example `cars/subie-22b/`).
- **A model's own springs / dampers**: keep them (node rules; `node` takes a list) instead of dropping the whole wheel material - an
  empty wheel well reads as missing suspension. If the physics track is narrower than the model's, `move: [dx, 0, 0]` (source units,
  per side) puts each corner on the game's hub. With none in the model, set `model.cornerSuspension` (`cars/subie-22b/`).
- **Roll cage** in the same primitive as seats / door cards: the `tube` rule (`{"tube": {"r": [0.012, 0.024], "score": 0.15,
"length": 0.3}, "material": "cage"}`) picks whole tube-shaped islands; send steering column / gear rod to `interior` with
  earlier `whole` boxes, flat gusset plates to `cage` by box. `cage` = light grey part material (worked example `cars/skoda-rally/`).
- `parts.maxTriangles` (`stl-to-glb.mjs`): `{"interior": 24000}` pre-simplifies one part on its own before the global budget; raise
  `targetTriangles` by the same amount, or the body loses detail. At 6k the Fabia's seats, dash and wheel became shards.
- **See-through glass**: set `model.glass` (tint + opacity) on a car whose model has a cockpit; without it the `glass` part is
  opaque (right for a model with an empty shell).
- **Every material name in `parts.materials` must exist in `part-materials.ts`** (or be the body): an unknown name silently gets the
  LIVERY material - the Fabia's whole cockpit was painted that way (`interior` was missing; its lining showed as a white ring round
  the rear screen). Raycast the pixel in the viewer and read the hit mesh's material name before blaming a box rule.
- New shared part names `chrome`, `amber`, `lenscover` (smoked see-through cover, 45 % opaque) in `part-materials.ts`: a modelled lamp keeps its
  bowls (`chrome`), indicator (`amber`) and gets a clear cover instead of a textured wrap.

## Lessons from `cars/fiesta/` (CC BY Sketchfab GLB with a cockpit, 2026-10-07)

- **Sketchfab FBX exports can carry a 0.01 root node scale on a model already in metres** (everything lists as 4 cm long): fix the node
  with `glb-set-root-scale.py <in> <out> <node> 100` before writing `gltf` boxes, so rules read in metres.
- **The GLB's `asset.extras` holds author / licence / source** (Sketchfab): read it first, then still quote the page's text in DETAILS.
- **A model's wheel can sit low in its body** (hub y 0.2 for a 0.32 m tyre): `offset` y lifts the body until the hubs are at the
  physics tyre radius; the car's floor clearance is then what the real car has.
- **Own rim, centred**: `glb-rim-extract.py` takes the tyre's centroid as the hub and its smallest principal axis as the axle,
  de-cambers the wheel and centres the rim's lip-to-lip span on the tyre's mid-plane (`wheel-stl-to-glb.mjs --keep --barrel <tyre bore>`
  flushes the tyre stub to the lip, so any offset there shows as an off-centre rim). Check with `wheels=1&wcam=FL&body=0`.
  Rim and tyre in ONE primitive: `--wheel <node-prefix>` splits it by islands (outer islands = tyre).
- **A modelled cockpit** (seats, dash, cage) is `interior` (+ `parts.maxTriangles`) under `model.glass` (tint + opacity): it shows through
  the windows. A model without one is an empty shell - do not promise an interior; `rawview`-style cut views tell (half the car, view from the cut).
- **Lamps whose look is their texture** (reflectors, bulbs, lens ribs painted into one lamp sheet, `cars/lancer-evo-6/`): the STL route
  has no UVs and turns them into flat colour. Drop those primitives in `gltf.drop`, list them in `srcParts` and run
  `python3 -I scripts/car-model/glb-src-parts.py <model.source.json> <source.glb>` after every `stl-to-glb.mjs`: it appends them with
  their own UVs as `src:lamp:<png>` / `src:tail:<png>` primitives and writes the sheet next to the GLB (`srcPart` in
  `part-materials.ts`: the sheet's bright pixels glow; `tail` = brake lamp, red pixels for the brake, neutral white for reversing;
  `src:tail:<png>:<x>,<y>` limits the reversing glow to the lens around that sheet pixel, so clear ribbed trim behind a red cover stays dark, `cars/subie-wrx-sti/`).
  `src:int:<png>` keeps a cockpit part's own texture (seat fabric; matt, double-sided, back faces dark). Check each sheet for logos
  before shipping it (a dash sheet with wordmarks stays out), and credit it like the GLB. Seats that are one open sheet (no back
  panel: look at them from the rear seats) get a closed back from `srcParts.shells` (dark hull, `cars/lancer-evo-6/`).
- **Holes where the source is double-sided**: Sketchfab exports mark materials `doubleSided`; our part materials are single-sided,
  so a cockpit / cowl shell seen from behind shows the ground through it. Name the part `<part>:2s` (`trim:2s`, `interior:2s`)
  in `parts.materials` / the rules: `partMaterial` draws it double-sided.
- **Grille openings with no own island** are `region` cuts (front view, convex outline, `depth` behind the bumper face) on the body material;
  grille bars / badge islands are `whole` + `islandTris` boxes. Badges go to `logo` (dropped).
- `tests/rally/hull-fit.test.ts` spread a whole vertex array into `Math.min`: a 100k-triangle model with a cockpit overflowed the stack (now `reduce`).

## Viewer and tooling gotchas (cost real time this session)

- **Mute the game**: any URL you open that can start the game (`/games/rally/?car=...`) gets `&mute=1` (AGENTS.md "Sound while testing"). The car viewer has no audio.

- **"White undertray" from below is the ground plane**: the viewer's ground is single-sided, seen from under it renders as a
  bright sheet with the car poking through. Hide it before judging the underside (`scene.traverse`: any mesh with a bounding
  box > 20 m wide -> `visible = false`), or check the GLB with `view-glb.py --views bottom`.
- **The browser caches the GLB**: after `stl-to-glb.mjs` run `await fetch('/models/cars/<file>.glb', {cache: 'reload'})` in
  the page, then reload with a changed query string, or you keep reviewing the previous model.
- **Rewriting the GLB stops the dev server** (`dev.watchFiles` restart under the preview wrapper): `preview_start` again - the
  port changes, re-navigate.
- **The browser pane renders at ~1 fps**: set the camera with damping off
  (`__carViewer.shell.controls.enableDamping = false; camera.position.set(...); controls.target.set(...); controls.update()`),
  hide the panel (`.dp-panel`), wait ~5 s, then screenshot - earlier screenshots show the previous frame. Decline the cookie
  banner once per page load.
- **Other sessions edit the same tree**: the viewer reloads itself when they save (HMR full reload), car names change under
  you, `tsc` / lint errors in files you did not touch are theirs - report, do not fix.
- **Blank / white viewer page, `__carViewer` undefined**: the dev build is failing, usually because ANOTHER session's file is
  broken or half-written (a map `data.json` truncated while a bake writes it, an import of a file not created yet). `preview_logs`
  (`level: error`, grep the "File:" lines), wait until the file is valid (`python -c "json.load(...)"`), reload. Not yours to fix.
- **README screenshots as files** (1280 x 720): the pane screenshot is not saved, so read the canvas: `shell.renderer.setSize(1280, 720)`,
  set the camera, `shell.env.update(controls.target); shell.env.follow(camera.position)` (else no shadow - the loop is paused while
  the pane is hidden), render twice, `toDataURL('image/jpeg', 0.88)` and POST it to a throwaway node http receiver in the
  scratchpad that writes the file. Bimmer cameras (look 0, 0.55, 0): front 3/4 `4.2,1.5,5.2` fov 32, rear 3/4 `-4.6,1.5,-5` fov 32,
  side `6.8,0.9,0` fov 38.
- **Screenshot timeouts ("pane is not displayed")**: `tabs_select` the tab; if the pane was hidden or closed, `preview_start`
  with a `url` reopens it (new tab id - pass it explicitly). A hung `navigate` means the same; do not retry in a loop.
- **Converter changes (`stl-to-glb.mjs`, `chartBoxes`) must not move geometry**: after a rebuild compare the sorted vertex
  positions per primitive with the previous GLB (`np.allclose`) - only the UV chart assignment should differ.
- **Check order after any livery change**: `npx tsc --noEmit`, `npm run lint`, `npm run test`, then the views. Lint / tsc errors
  in other sessions' files are reported, not fixed.
- Writing helper scripts: a Bash heredoc with an apostrophe in the body ("don't") fails with "unexpected EOF" - write the script
  with the Write tool and run the file. Python patches of long files: slice by unique anchors and `assert` they exist. On
  Windows write with `open(p, 'w', newline='\n')` - text mode silently turns the file CRLF (prettier then fails on every line).

## 6c. Boxy profile - required for every imported car

Every GLB car needs a baked `profile.ts`: it is the car's body when the GLB fails to load (never a blob) and a parked
car on the city maps (`assets/builders/vehicles.ts` `SHAPES`). Do it as soon as the plain GLB is final, and re-run it
whenever the GLB is regenerated.

1. Bake it from the plain GLB (axle z and wheel radius from the car's physics):
   `node scripts/car-model/side-profile.mjs public/models/cars/<file>.glb --axles <front z>,<rear z> --wheel <radius> > src/games/rally/cars/<car>/profile.ts`
2. `<car>.ts`: `import { profile } from './profile';` and `model.profile: profile`; an explicit `model.doorBadge`.
3. `<car>/livery.ts`: `layout: A` (the `model.source.json` atlas block) on the `CarAtlas`, so the box wears the livery.
4. Append the profile to `SHAPES` in `assets/builders/vehicles.ts` (append: `FIXED_CARS` and placed props use the
   indices) and name it in the `street_car` description in `assets/catalog.ts`, so the car also parks on the city maps
   (variants 0-11 cycle the shapes, nothing else changes).
5. A GLB without its own interior keeps tinted glass (no `model.glass`, the default dark tint): no procedural cockpit,
   the user rejected those.
6. Check: `tests/rally/car-fallback.test.ts` (size, arches, glass, lamps, UVs) and `tests/rally/street-car.test.ts`
   (triangle budget) pass; look at `car-viewer.html?car=<id>&fallback=1` (glass over the windows, lamps on the nose and
   tail, livery) and `asset-debug.html?asset=street_car&variant=<n>`. Tweak `--tol` only if the outline looks wrong.

## 6d. Service-park copy (released cars only)

The service park draws its team cars from a cheap copy of the final GLB. When the car is released (no `hideInProd`):
`node scripts/car-model/park-lods.mjs <id>` writes `public/models/cars/<id>_park.glb` (needs the livery atlas in
`model.source.json`; every material name needs a colour in the script's `PART_COLORS`), then add the id to `PARK_CARS` in the
script and to `PARK_CAR_IDS` in `world/park-cars.ts`. Re-run it whenever the GLB or its atlas changes. Check it in
`map-viewer.html?map=ajvatovci` at the lots; `tests/rally/park-cars.test.ts` checks size and budgets. Details: `DETAILS.md` "Park cars".

## 7. Done

- **Hub check in the viewer**: `car-viewer.html?car=<id>&tyres=0&rims=0&clean=1&mute=1` (body + brakes only), cameras at each
  wheel (`wcam=FL|FR|RL|RR`). Only the game's disc (dark, with a hat) and a caliper may show. Any other flat plate, floating
  piece or black disc is a source part that was not dropped or recoloured: find its island (`glb-to-parts-stl.py` warning, or
  bbox of the part around the hub) and drop it.
- Boxy profile baked and wired (step 6c): fallback body and street car checked.
- `npx tsc --noEmit -p tsconfig.json`, `npm run lint`, `npm run test`.
- Car `README.md` (high level: description, 3 screenshots, credits + licence) and a **short** `DETAILS.md` (sources + links tables, the few
  measured numbers the code does not show, rebuild commands (orient -> segment -> convert -> view-glb), one line per non-obvious
  decision, no diary of what was tried - see `AGENTS.md` "Write short"; never a licence TODO: the gate is done before the import). `public/models/CREDITS.md` row,
  `src/games/rally/DETAILS.md` car table, `TASKS.md` open items.

## Tyres and set-ups (every new car)

A car needs `physics.tyres` (the real sizes: the default rolls on `wheelRadius`, every other size scaled by its marking and within
4 % of it; `byCompound` per compound, `rear` for a staggered car; PHYSICS.md "Tyre sizes"), `physics.setups` +
`physics.setup` (three presets from `deriveSetups` with the car's own limits: rally car wide range, road car soft half, race car
stiff half) and `model.suspensionStyle`. Give every preset a `ride` offset (softer = higher, a few cm).

**Collision hull = the real body.** Never ship `autoHull` (a box with its underside at 0.85 x wheel radius - far above
low splitters / sills). Run `npx rstest run tests/rally/hull-fit.test.ts --reporter=default` once: it prints the model's
underside per zone; then build `physics.hull` with `bodyHull(BODY, centreZ, low)` (`physics/hull.ts`; `centreZ` = middle
of the body's z extent, `low` = sphere rows along splitter, sills / floor, rear bumper with `bottom` = the printed heights;
worked examples `cars/bimmer-m3/bimmer-m3.ts`, `cars/skoda-rally/`). The test then guards it; check it in the car
viewer with `hull=1`. `tests/rally/car-setup.test.ts`, `car-matrix.test.ts` and `tyre-mesh.test.ts` run every
registered car; see `src/games/rally/PHYSICS.md`.

## Per-compound wheels and a GLB's own wheel (Bimmer GT2)

- A GLB's modelled wheel becomes a game wheel with `scripts/car-model/glb-wheel-extract.py` (rim + tyre STLs of one wheel group, axle = STL z,
  outer face at z max) then `wheel-stl-to-glb.mjs --keep --barrel <bore radius it prints>`. A wrong outer-face sign shows as spokes
  sunk behind the barrel. A rim that ends at its bead seat (no lip above the tyre bore: max rim radius ~0.62 in the GLB) shows a
  groove between rim and tyre (the game tyre flares out from its bead): add `--flange 0.68` (a lathed lip, `cars/lancer-evo-6/`).
- A busy source rim: `glb-rim-extract.py --min-island 400` drops small islands (wheel nuts / bolts); `wheel-stl-to-glb.mjs --two-tone <r>:<face hex>:<lip hex>`
  paints the rim in two colours as vertex colours (centre / spokes below unit radius r, lip above; the game then ignores `model.rim.color`,
  worked example `cars/porsche-911-930/`: ash-black centre, silver lip, with `--flange 0.68`; the setup screen's tyre
  pickers use the same material, `createRimMaterial` in `car-model.ts`).
- `model.wheelByCompound` gives a compound its own wheel GLB and / or rim colour (`rimColorFor`, `wheelModelFor` in `stl-wheel.ts`).
- Wide gravel tyres lose grip on loose ground (`sizeFactors`): keep a rally tyre near 235 mm, and raise `rear.grip` for more than the M3's power.
- A GLB body whose paint / carbon split lives only in its texture: `glb-to-parts-stl.py` rule `{"mat": "Body", "texture": {"maxLum": 0.42, "maxSat": 0.06, "blur": 9, "refine": 0.02}, "y": [..], "z": [..], "material": "carbon"}`
  labels body triangles by the (blurred) texture and splits them along its border. Put it first in `gltf.parts`, box it tight (dirt looks like carbon), keep `blur` (raw texels speckle: 140k triangles). `exclude` UV boxes keep emblems out. The GT2 sends its
  black rubbers, mirrors, lip and diffuser to `trim` this way (without it the body is one flat paint colour).
- A minimal GLB import still needs these fixes from the user's close-ups (worked example `cars/porsche-911-930/`):
  - Paint striped on the arch walls: an `arch` rule first in `gltf.parts` (`mat` = body, `material: "trim"`; hub y / axle z in SOURCE units,
    `r` just over the arch opening, `dy` -0.25 so the walls below the hub count). Check with `wheels=1&wcam=FL&body=0`.
  - Exhaust that is a bent single-faced shell: drop its node and build the tail pipes with `parts.tubes` in `steel` (hollow tube: outer wall + rim
    in `material`, bore in `inner`, same frame as `parts.solids`; `tilt` 180 points a pipe at the back).
  - Sawtooth paint edge on a slanted fender lip: an `atlas.chartBoxes` entry with chart `rear` and `any: true` (one paint colour inside).
  - Reflectors that light on braking: their own island (`whole` + a y box) in a `reflector` part.
  - Lens texture the model keeps only as flat colours: `tailweave`, `amberweave`, `lensweave`, `clearweave` (`part-materials.ts`, one
    drawn tile of faceted pyramids with a normal map, 6 mm pitch, no shipped texture). `side-profile.mjs` `LAMPS` must list new tail / lens part names.
- A new car needs its own `suspensionStyle` (`suspension-mesh.test.ts`): add one to `SUSPENSION_STYLE_COLORS`.

## Bump the times version (last step)

Add the car's id to `CAR_TIMES_VERSIONS` in `game/stage.ts` (start at 1; a test fails without it). It stays at 1 while the car has `hideInProd` in `CARS_LIST` (a test checks); once released, handling changes bump it when the user says we are making a build (livery / model fixes
never). Old times stay below the new ones.
