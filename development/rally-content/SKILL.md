---
name: rally-content
description: Add or iterate Gravel Rally assets (trees, rocks, props, signs), cars (model + livery) and procedural textures, keeping instancing/LOD performance. Use for any request about rally visuals, models, cars, liveries, vegetation, props or textures.
---

# Rally assets, cars, textures

## Assets (anything placed in the world)

Two files per asset:

1. `src/games/rally/assets/catalog.ts` — metadata: `id`, `category`, `variants` (seeds used in-world),
   `lods` (`maxDistance`, `castShadow`, near -> far), `colliders` (cylinder/sphere in local space; omit for
   drive-through things), `tint` (per-instance colour jitter).
2. A builder in `assets/builders/<category>.ts` registered in `assets/library.ts` `BUILDERS`:
   `({ seed, variant, lod }) => ({ parts: [{ geometry, material }] })`.

Rules (performance — late-2000s look must not lag):

- Use `engine/geo.ts` (`paint`, `merge`, `shade`, `foliageNormals`, UV helpers): non-indexed, vertex-coloured,
  merged into as FEW parts as possible. Each part = 1 draw call per (variant, LOD).
- Materials ONLY from `engine/materials.ts` (`getMaterial(id)`); add a new id there if needed. Never `new Material`
  inside a builder. Foliage materials carry `defines` for the world shading (`engine/world-shading.ts`):
  `RALLY_WIND` (sway, bends ~ height² above the asset origin - keep origins at ground level), `RALLY_FOLIAGE`
  (backlight glow), `RALLY_GROUND` (receives the far canopy shadows). A material with its own `onBeforeCompile` must
  call `addWorldUniforms(shader)`.
- Trees are not catalog builders: `src/games/rally/trees/` grows them (L-system species -> skeleton -> mesh -> impostor; see the
  "Trees" bullet in rally `DETAILS.md` and `.claude/reference/trees/`), placed by the old tree type ids (`TREE_TYPES`). For
  other assets: far LODs must not cast shadows and set `oneVariant` (all variants share one bucket = one draw call).
- Variants are cheap in draw calls: other LODs are drawn as variant sets (one draw per asset / LOD / material, see
  DETAILS.md "Draw calls"). Every variant's parts must share the same attributes (position, normal, color, uv) or the
  asset falls back to one draw per variant; keep LOD0 tree crowns small - sets over the cap are not merged.
- Front of props faces +Z, origin at ground level.
- Alpha grass cards: `foliage_card` (olive green) / `foliage_card_spring` (bright green) / `foliage_card_dry`
  (golden) - the card TEXTURE carries the colour,
  vertex colour only varies it (a green texture x golden vertex colour = dark olive).
- Buildings (`assets/builders/buildings.ts`): UNIT footprint (x, z in [-0.5, 0.5], y 0..1), scaled per
  instance with `ScatterInstance.sx / sy / sz` (width / height / depth) and a `box` collider; keep details
  relative. `house_pitched` walls end at `HOUSE_WALL_FRACTION` of the height (roof above), `building_flat` styles
  0/1 hall, 2 brick block, 3 rendered block; variants 4-7 = two floors of windows.
- Vegetation palette so far (trees: one L-system species each, `trees/species.ts` `TREE_TYPES`): `pine_tree`, `plantation_pine` (a cheaper pine for dense stands), `black_pine`
  (umbrella crown), `juniper`, `birch_tree`, `oak_tree`, `beech_tree` (mountain beech), `hornbeam_tree` (bright-green coppice), `walnut_tree`, `willow_tree` (weeping), `poplar_tree` (columnar), `cypress_tree` (dark column), `locust_tree` (black locust), `bramble_shrub`,
  `fruit_tree` (orchard rows), `hazelnut_tree` (plantation rows), `pale_tree` (tall plane / ash), `young_tree` (sapling),
  `thicket_shrub` (autumn roadside brush, drive-through), `broom_shrub` (yellow flowering broom), `bush` (green), `scrub_bush` (dark olive hill scrub), `grass_tuft`, `spring_grass`, `dry_grass`; props incl. `street_lamp`, `road_barrier` (red-white police / marshal barrier, solid, closes side-road junctions),
  `tape_post` (5.2 m of red / white tape along local X), `fan_flag` (generic designs, no national / club flags).

Iterate at `/games/rally/asset-debug.html?asset=<id>&seed=<n>&lod=<n>&grid=20&bounds=1&collider=1`
(`seed=-1` shows the in-world variant). `grid` is an instancing stress test; watch F3 stats.

## Cars

One folder per car: `src/games/rally/cars/<car>/<car>.ts` exporting a `CarDef`, registered in `ALL_CARS` in `cars/index.ts`.
**Release flags** (`src/games/rally/release.ts` - one file tracks all cars + maps): add a new car to `CARS_LIST` with
`hideInProd: true` (required - `tests/rally/release.test.ts` fails for an unlisted car). It is then dev server + test build only (`npm run dev` / `npm run build:test`
use `ALL_CARS`), marked TEST in the menus / HUD / tool pages, and left out of `npm run build`. Remove the flag to ship it
(or set it again to pull it from the published build).
Car-specific extras (e.g. a custom part builder) go in the car's folder; code used by every car (types, body,
model, parts, livery, glTF import) lives in `cars/shared/`.

- `sound`: engine layout, displacement, exhaust / intake, turbo + anti-lag, pops, gearbox, whine, cam - match the real engine
  (rally `DETAILS.md` "Sound"; `tests/rally/engine-sound.test.ts` checks the ranges).
- Every car needs a body for when it has no GLB or the GLB fails: `model.custom` (hand-built, below) or `model.profile`
  (an imported car's boxy stand-in: its side outline extruded to the body width with glass + lamps,
  `cars/shared/profile-body.ts`; it wears the livery when the car's `CarAtlas` sets `layout` = its model.source.json `atlas`
  block). Bake it from the plain GLB into the car folder:
  `node scripts/car-model/side-profile.mjs public/models/cars/<file>.glb --axles <front z>,<rear z> --wheel <radius> > src/games/rally/cars/<car>/profile.ts`.
  The city maps' parked cars use these profiles too (`assets/builders/vehicles.ts` `SHAPES`). Required for every imported
  car: rally-car-import step 6c.
  `tests/rally/car-fallback.test.ts` checks it; see it with `car-viewer.html?car=<id>&fallback=1`.
- `model.wheels(radius, width)` = car-specific tyre + rim geometry (a tyre with a `color` attribute is drawn with vertex colours);
  `model.glass` = window tint; `model.paintFinish: 'satin'` = old paint; `rim.style: 'steel'` = holed steel wheel, no caliper.
- `model.wheelModel` = a wheel GLB made from rim + tyre STLs (`scripts/car-model/wheel-stl-to-glb.mjs`, unit wheel
  space, scaled per car by `cars/shared/stl-wheel.ts`; adds a brake disc + hat + caliper behind the open spokes).
  `skoda_rally_wheel.glb` (the imported model's own rim, `--keep`) is on the Skoda Rally. For another wheel STL, re-measure
  the rim with cross-sections and adjust the strip rules in the script (print-only tubes / plates hide the brakes).
- `model.rim`: `color`, `spokes`, `style` spoke|steel (the procedural wheel, until / unless a wheel GLB loads).
- Livery = the car's atlas painter (`CarAtlas.paint`, rally-livery skill) with seeded colours from `cars/shared/livery.ts`
  (`liveryInfo`: base + 2 accents; seed 0 = `model.paint`; no real brand logos).
  Liveries carry **no numbers / lettering**: the car number + rally name are the door plate
  (`cars/shared/rally-badge.ts`, a decal projected onto the paint). Place it per car with `model.doorBadge`
  (`z`, `y`, optional `tilt` in degrees to follow a sloping body line; check both sides in the car viewer with `&num=7&rally=<map>` - clear of handles / seams).
- Model space: y = 0 ground at ride height, z = 0 centre of mass. For wide-arch cars set physics `track` so the
  tyre's outer face sits just inside the arch.
- Per-car performance bands live in `tests/rally/vehicle.test.ts` (`BANDS`) - add one for every new car.

Free camera for close-ups / screenshots: add `&cam=x,y,z&look=x,y,z&fov=10&clean=1` (model space, +z nose, +x car's left; `clean=1` hides the panel; the panel's "Copy camera link" button copies the current view). Liveries (create / fix / debug): the `rally-livery` skill + `scripts/car-model/chart-probe.py`.

Iterate at `/games/rally/car-viewer.html?car=<id>&seed=<n>&view=side&hull=1&wire=1` (pose sliders for
steer/suspension, specs + torque/power chart, "Test drive" link). Physics changes -> rally-physics-tuning skill.
Console: `__carViewer.model`.

### Hand-built bodies (`model.custom`) - example: `cars/zastava-101/`

When there is no mesh but there is a blueprint, build the body in code
(which cannot do crisp creases, leaning noses or clean window openings):

1. Measure: crop + upscale each blueprint view with a pixel grid, find the scale from the wheelbase (hub centres),
   and write every curve into `<car>/blueprint.ts` (centreline silhouette, pillar / rail edges, crease, plan half
   width, arches, windows, seams). Use the dimensioned numbers where the drawing gives them.
2. `<car>/body.ts` builds the mesh with `cars/shared/mesh-kit.ts` (`Soup`: `grid`, `polygon` with holes, `sweep`,
   creased normals): body-side columns at stations (dense round arches + corners, rows on circles round the arch
   so the lip is crisp), top rows from nose to tail ending on the side / pillar edges, a polygon for the cabin
   sides with the window openings, nose / tail panels; then glass, rubbers, lamps, bumpers, cabin.
   It returns `{ paint, parts }` (`CarCustomBody.build`): `paint` gets the atlas texture, `parts` is the usual
   `CarPartGeometry` (trim, mesh, glass, lights, tail, amber, interior, cage = bright metal, lining, optional
   `chrome` = polished reflectors / bezels and `lens` = clear lamp glass). Lamps: build them as geometry on a
   local plane (`cars/zastava-101/lamps.ts`: frames, reflector dishes, ribbed lens slabs), not flat boxes.
3. `<car>/paint.ts`: atlas layout (`atlasKit`) + UV functions used by `body.ts` + the painter - plain projections
   (sides z-y, top z-x, ends x-y), so seams / dirt are drawn in model-space metres.
4. Check against the blueprint: copy it to `public/_tmp/` (delete afterwards), overlay it as a fixed `<img>`
   (`mix-blend-mode: multiply`) on an orthographic car-viewer render - `__carViewer.shell.camera` fov ~2.6 from
   60 m, `near` 20, aspect set, panel hidden - scaled / placed from two projected model points. Side, top, front, rear.
5. Pin the key dimensions in a test (`tests/rally/zastava-body.test.ts`); keep the car under ~35k triangles.

### Importing a model? Start in `.claude/skills/rally-car-import/SKILL.md`

That skill is the workflow (scan gate -> orient -> measure -> naked check -> parts -> materials -> livery -> verify -> docs);
the two sections below are the API reference it points at. Its step 1 (`scan-mesh.py` verdict) decides whether a model is
imported at all - a blob verdict (image-to-3D) means the model is abandoned, not hand-cut.

### Imported models (glTF / GLB, e.g. Sketchfab)

A real model replaces the car's `custom` / `profile` body when its file exists; that body is the fallback.

1. **Licence gate first** (`.claude/skills/rally-car-import/SKILL.md`): the model must allow redistribution of derivatives (CC0 / CC BY; no ND, no
   "personal use" / Standard Digital File licences). Then download it as **glTF/GLB** (Sketchfab: needs your login; CC BY needs credit).
2. Inspect / slim it (big models hurt: aim < 60k triangles, textures ≤ 2k, webp):
   ```bash
   npx @gltf-transform/cli inspect model.glb
   npx @gltf-transform/cli optimize model.glb public/models/cars/<file>.glb --texture-compress webp --texture-size 2048 --simplify-ratio 0.25
   ```
3. Reference it in the car: `model.gltf = { file, credit, rotationY?, scale?, offset?, hideNodes? }`
   (`cars/shared/types.ts` `CarGltfDef`) and bake its `model.profile` (above). Auto-fit: scaled to physics `length`, centred between the axles, ground = lowest
   mesh (tyres). Node names matching `hideNodes` (default wheel|tire|tyre|rim|brake|caliper|disc) are hidden -
   physics-driven procedural wheels are used.
4. The file list is baked in at startup (`rsbuild.config.ts` -> `__CAR_MODEL_FILES__`); the dev server restarts by
   itself when a file is added / removed in `public/models/cars/` (`dev.watchFiles`). Production builds list what
   exists at build time. If the car viewer still says `procedural`, reload the page. Commit the GLB plain: the build
   serves it meshopt-compressed (`scripts/car-model/glb-meshopt.mjs`, dev server too; already-compressed files pass through).
5. Car viewer "model" row must say `imported glTF`; fix orientation with `rotationY` (front must be +Z),
   position with `offset`. Add a row to `public/models/CREDITS.md`.
   Files are served page-relative (`<base>/models/cars/…`), so subfolder hosting works.

### STL bodies (untextured meshes, e.g. 3D-print / generated models) - example: `cars/bimmer-m3/`

The end-to-end order of work + every gotcha hit so far is in `.claude/skills/rally-car-import/SKILL.md`; the steps
below are the tool reference.

1. Put the settings in the car folder: `model.source.json` (axes, scale, offset, wheel cut-outs, target
   triangles, atlas layout). Measure first: render the STL (or run the converter once) and read off the
   wheel centres / radius - scale so the wheel radius matches physics `wheelRadius`; `offset` puts the front axle
   on physics `front.z`.
2. Convert (the original STL lives in `sources/cars/<car>/`):
   If the STL is exported tilted (print-bed orientation), level it first with
   `scripts/car-model/orient-tilted-stl.py` (PCA + pitch / roll; check left / right symmetry and hub heights).
   ```bash
   node scripts/car-model/stl-to-glb.mjs src/games/rally/cars/<car>/model.source.json sources/cars/<car>/<model>.stl --preview atlas.png
   ```
   It welds, re-orients to model space, **cuts the wheels out** (cylinders at `wheels.centres` - procedural
   physics wheels replace them; that centre-based cut leaves saw teeth on big arch-lip triangles when a modelled tyre
   sits 1 cm from the lip - then label the wheel with a `region` circle in `segment-stl.py` and list its material in
   `parts.drop`: an exact clip, worked example `cars/bimmer-m3/`; give the region `any: true` so it also cuts triangles an earlier segment pick labelled, and `parts.fills` (converter) adds flat patches (e.g. glass continued under wipers: `[{material, poly:[[x,y,z],...]}]`); `wheels.liner` `floorY` to close the well's inner wall for a view from below; the liner takes the atlas' matte texel, so the car's atlas needs `matteRect` + a black patch there), simplifies (meshoptimizer, ~45k tris) and writes creased normals + projection UVs:
   each triangle goes to the left / right / top / front / rear chart by its facing, charts laid out in metres
   (+ a `bottom` chart like the top one when the atlas has room for it - otherwise one underside texel).
3. Livery = `<car>/livery.ts` exporting a `CarAtlas` (`model.gltf.atlas`, with `autoFit: false`): a canvas painter
   that draws in **model-space metres** (`side(z, y)` on both sides, `top(z, x)`, `end('front'|'rear', x, y)`,
   multi-contour shapes, per-side `'left' | 'right'`). Use the `--preview` image (10 cm grid) to find window / light / vent
   positions. Shapes and plain boxes only - never text (the painter has no text helpers; number + rally name are the door-plate
   decal), no real brand logos. Build the livery up step by step with the user from a clean base colour - automatic photo tracing
   was tried on the GR Yaris and rejected (`rally-car-import`, "Livery").
   Chart overrides: `atlas.chartBoxes` (`stl-to-glb.mjs`, boxes in model space, x mirrored): `chart: 'top'` sends up-facing triangles
   (normal y > `minNy`, default 0) to the top chart (crease walls inside a painted bonnet shape, a roof edge wall);
   `chart: 'side'` sends front / rear-facing ones - plus, with `maxNy` / `minNy`, steep or horizontal ones - to their own side
   chart (arch flares that share end-chart texels, shoulders next to a painted edge, sill ledges); `chart: 'rear'` / `'front'`
   sends up-facing ones to the end chart (a low bumper lip among colour rows). Example + reasons: `atlas.chartBoxes` `$comment`s in `cars/bimmer-m3/model.source.json` (summary: DETAILS.md "Livery chart boxes");
   how to find the faces: `rally-livery`.
4. Wheel arches: `wheels.arch` (`faceRadius`, `radius`, `maxNormalX`, `minAbsX`) sends arch triangles to the atlas' matte texel; livery painters call `atlasKit(...).matteRect` (black fill) and export it as `CarAtlas.matteRect`. `wheels.liner` adds a dark wheel-well cup if the arch is see-through (`lip: true` also seals the slit between the cup rim and a cut edge further out; the rings are raycast to stay behind the skin). `model.suspension: true` draws uprights + wishbones + damper behind the wheels.
5. Accent parts (glass, lamps, grille, vents, wing, trim): **never paint them on the atlas** - projection charts
   overlap (a wing over the rear window) and triangle-by-triangle colouring gives saw-tooth edges. Split them off
   as real parts instead (example: `cars/bimmer-m3/`, `parts` block of its `model.source.json`):
   ```bash
   python scripts/car-model/segment-stl.py <model.source.json> <in.stl> <parts.stl> --preview seg --by segment
   node scripts/car-model/stl-to-glb.mjs <model.source.json> <parts.stl>
   python scripts/car-model/view-glb.py <model.source.json> check
   ```
   `segment-stl.py` splits the mesh into smooth patches along its creases and `parts.picks` assign patches to
   materials: `seeds` = `[view, a, b]` (the patch seen at those model coordinates; read them off the `--by segment`
   preview, `--grid 0.02 --scale 2600 --crop ...` for thin strips) and / or `inside` boxes. Use `mirror: false` with
   per-side seeds where the two sides are creased differently; `hub` picks (per triangle: surfaces inside a wheel
   arch that face the hub) make arch lips black without relying on creases. The converter writes one primitive per material
   name; `cars/shared/part-materials.ts` maps names to shared materials (trim, gloss, mesh, carbon, glass,
   headlight, lens, tail, reflector) - add new names there. `parts.wrap` materials get UVs fitted to 0..1
   over the part (`corner` for lamps, `side` for side windows), so their textures are drawn in part space. Crease segments need a clean mesh with real feature edges (CAD /
   print models). Image-to-3D blobs (the former GR Yaris, deleted) have none - the import gate rejects them. `region` (an outline polygon measured
   in a view; triangles crossing it are cut along it) and `box` picks exist in `segment-stl.py` for the rare soft feature on a CAD mesh.
   Measure outlines on crease-highlighted renders (dihedral angle > 14 deg = the mesh's recess rings) at 1200+ px/m, one section at a time,
   and check each in the car viewer close up before the next.
6. Check in the car viewer (`model` row = imported glTF), add a CREDITS row.

## Textures

Procedural canvas textures in `engine/textures.ts` (`TextureId` + entry in `DEFS`). Colour maps set `color: true`
(sRGB); multipliers/masks `false`. View at `asset-debug.html?asset=tex:<id>&repeat=4`.
To replace with real images later, return a loaded texture for the same id.

## Done checklist

`npx tsc --noEmit -p tsconfig.json`, `npm run lint`, `npm run test` + `npm run test:integration:rally` (stage test catches colliders on the road),
check F3 stats in game (`__rally.benchmark(240)` in the console). Open game URLs with `mute=1` (AGENTS.md "Sound while testing").

## Source files

Files / links the user provides (models, reference photos, data downloads) go to `sources/` (git-ignored) and are
listed in the car / map folder `DETAILS.md` - follow `.claude/skills/source-files/SKILL.md`. Models / references
a player should see credited also go in `CarDef.sources` (label / url / note) - listed on the main menu About screen.

## Tyres, rims and coil-overs

Every tyre comes from `cars/shared/tyre-mesh.ts` (size from `CarPhysicsDef.tyres`, tread per compound, compound ring); a car only
supplies its rim (`model.wheelModel` GLB rim - rescaled per tyre size - or `model.wheels` for a custom rim + caliper) and flags
(`tyreDust`). Coil-overs / struts for the setup screen: `cars/shared/suspension-mesh.ts`, pick `model.suspensionStyle`
(`rally` / `road` / `race`). Verify in the car viewer (`?tyre=tarmac|mixed|gravel`) and on the setup screen (parts bench).
