---
name: city-walker
description: Project-specific guide to this 3D city-walker viewer — scene architecture, the shadow recipe and its decision history, terrain/water/vegetation/surface rendering, the EPSG/world coordinate frame, the offline geodata pipeline, and the screenshot QA harness. Use for any non-trivial work on the three.js scene, the data bakes, performance, or visual debugging.
---

# City Walker — rendering, data & QA

Stylized client-side 3D walk through a German city from its Land's open
geodata (Dresden is the reference). Read
`AGENTS.md` first for the high-level map; this skill is the deep reference for
*how it's built*. For *what maps to what* — the source→feature provenance
diagram, the transformation ledger (active / experimental / planned /
**discontinued**), and how to render other locations — see `docs/`
(`docs/README.md`). **When you add, change, or drop a data→feature
transformation, update `docs/transformations.md` + `docs/data-flow.md` as part of
the change** (Definition of Done in `docs/README.md`). `docs/rendering.md` is
the human-readable map of the frame (scene graph, the attribute → visual
codebook, budgets, boot sequence), `docs/data-pipeline.md` the bake/build
reference, and `docs/adr/` the record of *why* the load-bearing choices below
were made — add an ADR when you change one.

## Scene architecture

`app/_components/create-app.ts` is the spine: it builds the renderer, scene, a
`PerspectiveCamera`, a `world` group (Z-up data frame, rotated −90° about X to
Y-up), reads the tileset's extras (CRS, recenter offset, tile bounds), starts
streaming the site and the animation loop, and returns a `CityWalkHandle`
(the imperative API the React HUD calls) once the spawn tile's buildings and
any of its terrain levels are on screen — the first frame. The fixed
lamp-light pool and the fog floor are created before the first frame and
retargeted/lowered as tiles land. The data layers are not wired into
`bootApp` by hand: they start on their first switch-on (`lazyFeature`,
`data-layers-feature.ts`) and hear the spine through its hooks
(`feature-seam.ts`: frame, stream change, the look store, the scene's
clock — a watched value a late starter reads first); a tile's traffic
slot waits for their builder. The scene environment
(`scene-environment.ts`, not three's `scene.environment`) holds what the
sun and the date move — the night node, the season watch, the clock —
and a dressing's trees follow its season from birth to release
(`followEnvironment`); the traffic slot follows the look's layer from its hang. The picture styles and Modell are still
wired by hand. The data layers' code stays in the scene chunk: the first `import()` chunk that imports three.js costs the first
load ≈ 33 KB gz (three leaves the scene's hoisted scope), more than the
data layers moved (ADR 0040) — measure before splitting one off.

**The renderer** is three r187's `WebGPURenderer` — its WebGPU backend, or
its WebGL2 backend where the browser has no WebGPU (`?gpu=webgl2` forces it:
`scene-profile.ts` `forceWebGL`; the preflight is `gpu-support.ts`). One
path: every material is a **TSL node material**, there is no GLSL, no
`onBeforeCompile`, no WebGLRenderer
([ADR 0027](../../../docs/adr/0027-webgpu-renderer-and-tsl.md)).
The viewer imports classes and node materials from `three/webgpu`, TSL from
`three/tsl`, addons from `three/addons/…` — never plain `three`
(`lib/city/` stays three-free). See "Node materials" below before touching
a material.

**Streaming** (`tile-stream.ts`, ADR 0024): the build bakes the site into an
OGC 3D Tiles tileset (`lib/city/tileset.ts`): per site tile the buildings
(refine ADD) over the terrain at two levels (a 512² grid, geometric error
40 m, replaced near the camera by an error-bounded TIN of the native DGM,
ADR 0030). Content is glTF (meshopt, quantised,
pre-gzipped `.glb.gz`). 3DTilesRendererJS loads and unloads it by
screen-space error with an LRU cache; the sun's shadow camera is a second
camera while the sun is up, so casters outside the view stay loaded (by
night it is taken off the stream: it draws no shadow) — at a resolution
of its own (`SHADOW_STREAM_PX`, `lib/city/shadow-fit.ts`), not the map's:
the renderer's error for an orthographic camera ignores distance, so at
2048 px it refined the terrain under the whole frustum; at a desktop's
128 px it refines the fine level under the eye-level frustum only (ADR
0047). This camera is a square of its own: it draws no shadow, the rings do, and on a phone it streams nothing (`shadowTilesStream`, plan 071:
the tiles it kept were tiles in use the memory governor cannot free).
On a phone the view's own stream also ends at 2.2 km (`streamFarFor`;
not through Modell's dolly zooms, which back the camera kilometres away). A dressing plugin builds
what a tile carries in `processTileModel` and frees it in `disposeTile`; the
heavy part (vegetation incl. the street-tree cadastre and the OSM hedges,
lamps, rails on the fine terrain level; its walls
and stairs are baked into the glTF) waits
behind the HUD's gate and is built one tile at a time behind the streaming
chip. A terrain level that takes over from its tile's other level on
screen is loaded only once its dressing is built and compiled
(`handsOver`): the renderer keeps the old level, trees and all, drawn
until then, so a change of level never blinks the trees away. The
dressing is compiled off the scene and hung at the renderer's
`load-model` — never before it records the content's materials, which it
disposes with the tile. Every tile change re-renders the shadow map. The layers:

- `city-layer.ts` — `dressCity` on a building tile: one glTF mesh per tile
  with a per-vertex feature id (`EXT_mesh_features`); the per-object table
  (`EXT_structural_metadata`: tint, heights, roof colour, glow, roughness,
  the demolish tree) is packed into a float texture the clay node reads per
  vertex with `textureLoad` by the `featureId` attribute
  (`lib/city/city-mesh.ts`). Demolish = drop the object's building tree from
  the index buffer and rebuild the tile's BVH (you can't hide one building
  in a batched mesh). Picking/collision use `three-mesh-bvh` on every loaded
  tile — its BVH built when a ray first reaches the tile's box
  (`ensureCityBvh`; within 400 m of the camera in idle time), never a ray
  walking a tile without one (three-mesh-bvh's brute-force fallback). No
  CityJSON reaches the browser.
- `terrain-layer.ts` — `dressTerrain` on a terrain tile: the glTF mesh
  gets the land-cover material and hangs the water and mist sheets. The
  fine level is a TIN of the native 1 m DGM1 (±0.15 m,
  `scripts/bake-terrain-tin.ts`; `extras.tin`): `heightAt` reads its
  triangles through a bucket index (`lib/city/terrain-tin.ts` `TinIndex`),
  and the water gets an up-facing normal twin. Nothing is burned into it;
  the wall ribbons in its `walls` node snap to the measured step at bake
  time (`lib/city/wall-snap.ts`, ADR 0030). The coarse level is the 512²
  grid with the wall breaklines burned in (ADR 0030), heights read back
  from its first n·n vertices. Both are shaped under OSM stairs and
  terraces at bake time (`scripts/bake-tiles.ts`, ADR 0030); study and
  numbers in the ledger's "Terrain TIN" entry.
- `landcover-splat.ts` — paints the class raster with the one palette
  (`lib/city/landcover.ts`) into the colour splat on the GPU (ADR 0010).
- `water-layer.ts` — sheets over the terrain geometry, masked by the splat's
  alpha (water coverage), animated normal wobble.
- `vegetation-layer.ts` — instanced trees (`Instances`; rows + DOM1 canopy + the
  laser-scan extra trees + the cadastre's trunks and broadleaf crowns, passed
  in as precomputed `TreeInstance`s), chunked for culling.
  Lives in the **Y-up frame** (a tile's content root), never inside the
  rotated `world` group itself. `tree-inventory-layer.ts` draws only the
  cadastre's reshaped silhouettes (flame / cone / dome) and vetoes canopy
  trees inside its crowns (not in forest/copse); `tile-stream.ts`
  (`buildTileVegetation`) joins both into the tile's one vegetation
  control. `low-vegetation-layer.ts` draws every hedge (OSM's and the
  DLM's), its lumps pushed out by a world-space noise so pieces agree.
  The trunk's foot bulges into roots and turns to earth
  (`buildTrunkMaterial`); `tree-foot.ts` adds the ground round it (pits,
  leaves, the crown's shade glaze, worn earth, roots in the paving,
  grates, guard hoops — the one opaque mesh) as `Instances` sets on the trunks' own
  attribute objects (no bytes of their own, nothing counted twice), their
  materials per tile with the class and edge rasters and the light in
  their slots; `renderOrder` orders the blended sets (rings before earth,
  so pits merge); the crowns' LOD hides a far chunk's sets.
- `shader-chunks.ts` — the shared TSL pieces: the node types (`F`, `V2`,
  `V3`, `V4`, `Live`), `dataXY()` / `dataPosition()` (glTF positions are
  quantised, so the data frame comes from world space: world (x, y, z) =
  data (x, −z, y)), `rasterUv(xy, origin, size)` (the corner a
  `uniform(Vector2)`, so every tile builds the same shader), and what the
  chunks compute with: a raster's texels (`texelSize`, `texelAt`,
  `loadTexel`, `byteOf`), `floorMod`, the hashes and the noise (`gdHash`,
  `gdNoise`, `gdNoiseSlope`, `gdBand`, `hash21`).
- `instancing.ts` — `Instances`, the instanced set every layer uses instead
  of `InstancedMesh`, and its nodes (`instancePosition`, `instanceTint`,
  `instanceMatrix`, `instanceFloat`).
- `three-utils.ts` — `sceneMaterial(key, make)` (scene-wide node
  materials), the dispose helpers, `sceneShared`, the texture byte tracker.
- `height-fog.ts` — `SceneFog`: distance fog, the valley pool (*Talnebel*;
  its depth from the site's ground relief, `lib/city/valley-fog.ts`, set
  in `create-app.ts` from the tileset's `extras.ground`)
  and the site-edge haze as **one `scene.fogNode`**.
- `sun-rig.ts` — directional light + shadow camera, the TSL `SkyMesh` dome
  (tempered, with a horizon haze band), hemisphere fill, fog colour by time
  of day.
- `post-stack.ts` — the scene pass into its own target and three's node
  `RenderPipeline`: GTAO, DoF, the picture style, SMAA, depth grading,
  vignette, paper grain — built per tier (`postProfileFor`, ADR 0047): a
  phone builds no DoF, antialiases with FXAA inside the last pass
  (`fxaa.ts`: a perceptual luma over the linear frame), draws `BeforeAA`
  only while a style is on; no tier warms more than the outline's programs
  (a picture style builds on its first frame); the AO
  smoothing and the outline's mask and blur are one-byte targets, the
  outline drawn only while something is asked; the nameplate
  (`nameplate-layer.ts`, the asked thing's name in the scene) is an
  overlay drawn onto the canvas after the frame (`setOverlay`), its colours
  sRGB, its atlas held only while asked. The picture styles (Comic, Film noir, Sin City,
  Papier; `lib/city/render-style.ts`) are one node, `stylize-effect.ts`
  (ADR 0034), in a styled pipeline pair the default pastel never draws:
  ink from the second difference of `1/z` (zero on planes; relative to `w`
  = silhouette, relative to slope = fold), tone bands / monochrome curves
  on the colour; the mode and the pen are uniforms. Read depth only at
  integer texel radii around a texel centre. Sin City, Papier, Strich and
  Schwarzplan touch the scene (`paper-scene.ts`, the row's `paperScene`
  kind); Papier, for example, sets a per-frame
  `scene.overrideMaterial` (white, flat-shaded node material; three carries
  each material's `positionNode` over) with sprites and see-through sheets
  hidden, restored after the render. QA the styles on a handful of views
  (aerial, roof sea, half-long building shot, street, river) — lite at
  pixel ratio 0.5 hides the stroke widths, so judge them at ≥ 1. Flicker
  and crawling (a still view that changes, a step that flips pixels) is
  measured, not judged: the `flicker-probe` skill.
- `visual-style.ts` — the one building style: opaque archviz clay + facade
  detail (tint, Boden-Verlauf, Höhenlinien, Traufkante, Streiflicht, dusk
  glow) as a `MeshStandardNodeMaterial`, always opaque (the see-through
  slider and its `alphaHash` build are gone too). The old ghost/standard
  styles are gone.
- The map's own marks: the ferry wakes of `riverside-layer.ts` (landing
  stages, groynes, ferries), faded in with height by `map-overlay.ts`. No
  text anywhere in the scene or HUD (plan 032's street names were removed;
  🗃️ in the ledger).
- More dressing: `tram-layer.ts` (tracks in their bed, the contact wire
  sagging between spans and arms, stop signs; `lib/city/tram.ts`),
  `fence-layer.ts` (the fences' material; baked into the fine terrain),
  `furniture-layer.ts` (benches … plan 030's advertising columns, signals,
  hydrants, clocks, drinking fountains, bus-stop signs), `crown-season.ts`
  (per-day crown colour and bare stipple, `lib/city/tree-season.ts`).
- Terms of the terrain's colour node (node functions called in order):
  `ground-detail.ts` (first `smoothPaths`: a path's edge near the camera
  cut on the B-spline-smoothed class texels, which sand, slabs and urban
  green then follow — never a class or paving texel read NEAREST for a
  tint), `sport-ground.ts`, `road-markings.ts`
  (`lib/city/markings.ts`), `cultivated-layer.ts` (colony gardens, vine
  rows; `lib/city/cultivated.ts`); and `sky-light.ts` (sky view → `aoNode`,
  far horizon → `receivedShadowNode`; `lib/city/skyview.ts`, the raster
  shared with the buildings through `tile-rasters.ts`, which hands every
  content root its rasters by kind: the kinds table holds a raster's look,
  tier twin and gate).
- Buildings: `lib/city/building-tint.ts` (tint, storey height, roofs, at
  bake time), `lib/city/small-buildings.ts` (the scan's sheds as boxes, and
  the canopy points they veto at build time), `scripts/measured-roofs.ts`
  (a LoD2 roof that misses DOM1 — the free-form roofs of complex buildings —
  replaced by what `pipeline/bake/roofs.py` measures: flat levels, and
  faces where it slopes — the flanks of a pitched roof section by
  section, planes, an extruded profile, or on a landmark the scan's
  surface (`roof_planes.py`) — each an error-bounded TIN cut
  to its outline, the outlines turned onto the footprint's walls
  (`regular_cover`); ADR 0036).
- Beyond LoD2 (plan 050, ADR 0036): geometry is added only where DOM1
  measures it **and** OSM (or, for a landmark's roof relief, Wikidata)
  names it — never from the surface model alone (cranes). `structures.py`
  → `lib/city/structures.ts` lathes chimneys/towers/masts, extrudes
  missing buildings and builds a landmark's relief from its measured
  height field (`reliefMesh`: the `grid` on 1 m, heights above the host's
  highest LoD2 roof, −1 outside, lightly smoothed in the bake; corners
  average the patch cells around them, each edge wall down to its cell's
  `floor` — the LoD2 roof under it, so a tower folded into a pitched nave
  stands on the slope — no bottom face; DOM voids below the LoD2 roof are
  filled in the bake —
  a truncated spire rises to its tip; the old stacked slabs made a stepped
  pyramid, and a relief without `grid` builds nothing); `appendGapStructures`
  puts them in the city mesh with `source` = 2 (a relief copies its host's
  row, so demolish takes it along). A tower, lighthouse or water tower
  under a LoD2 roof is LoD2's own (`BUILT_TOWERS`) — no second column. OSM `building:material` / `building:colour` /
  `roof:colour` reach the clay only through `osmColourTint` (hue kept,
  saturation ≤ 0.45, lightness clamped) and the palette families; glass
  (flag 4) and metal (8) are a cool tint, lower roughness and, on glass, a
  Fresnel sky sheen (`visual-style.ts`: `osmColour`, `clayGlow`) — no
  panes, no textures (the window grid is vetoed). Landmarks (flag 16) come from Wikidata
  (`landmarks.py`, cached at fetch time), the site's twelve in the
  tileset's `extras.landmarks` (one per building drawn) → the HUD's
  *Orte*, merged with the authored vantages (`lib/city/places.ts`: a
  landmark a vantage names or looks at is folded into it) →
  `landmarkVantage`.
- Modell (plan 055, ADR 0044; `M`): the city in parallel projection.
  `model-rig.ts` owns the view while it is on (pan / zoom about the
  pointer / turn / tilt, the presets, the dolly zoom in and out of the
  perspective camera); `model-camera.ts` is three's ortho camera with a
  shear for the Militärperspektive, 20 km back along the view; the pure
  half is `lib/city/model-view.ts`. **The post passes never hold the real
  camera**: `view-lens.ts` is a stand-in whose matrices are copied from
  the camera drawing the frame, plus `ortho` (which depth→distance
  formula, a per-pixel select) and `equivalent` (the distance a 55°
  camera would show the picture from, for far-field fades). Rays for any
  camera: `view-ray.ts`. The Schnitt (`model-cuts.ts`,
  `visual-style.ts` `setClaySection`: the clay two-sided, back faces the
  poché, a ground-profile strip) and the Ausschnitt (a `ClippingGroup`
  around `world`, a plinth — shown only once `PostStack.holdCut` has
  compiled and holds both sides of every build, since a switch of the
  group rebuilds the city's programs in the frame; its shadows are not
  clipped). The export (`image-export.ts`) tiles the
  frustum with `setViewOffset`, **one tile per animation frame** — SMAA
  and GTAO are `NodeUpdateType.FRAME` nodes and render once per frame.
  The planner styles *Strich* and *Schwarzplan* are rows of the style
  table and kinds of the paper swap (`paper-scene.ts`: `paper`, `line`,
  `figure`; the ground's `paperGroundOn` = 1, 2, 3).
  Each terrain level carries its trees, in every mode: the fine one
  all of them, the coarse one a fixed third (`drawnCoarse`, a hash of
  where each stands), √3 wider, baked by the build from the fine level's
  placement (`crowns_<t>.crw.gz`, `coarse-crowns-layer.ts`) — the coarse
  level shows past 2.5 m/px and wherever the memory governor or a load
  leaves the fine one out, at any scale, so never tie a layer's trees to
  Modell's scale; anything else on the fine level vanishes there at
  once. A two-finger twist turns the ground with the fingers
  (`twistedTurn`).
- `minimap.tsx`, `city-walk.tsx` (HUD), `poc-debug.ts` (`window.__poc`).

Constants live in the layer files and are the source of truth; values quoted
below may drift — confirm in code.

## Node materials — how a look is written, and the traps

A look term is a TSL node in a slot of a node material
(`MeshStandardNodeMaterial`, `MeshBasicNodeMaterial`, `PointsNodeMaterial`,
`NodeMaterial`): `colorNode`, `normalNode` (view space), `positionNode`
(local, before the model matrix), `emissiveNode`, `roughnessNode`,
`opacityNode`, `aoNode` (indirect light only), `receivedShadowNode` (the
shadow a fragment receives), `maskNode` (discard — the shadow pass honours
it), `castShadowPositionNode` (what the shadow pass draws instead of
`positionNode`). A fixed look strength is a constant node named after
its term, beside it in its owner (`TINT`, `WINDOWS`, `GROUND_DETAIL`, …;
plan 073); a slider (only *Nebel* is left) or anything else that moves
is a `uniform()` node every tile's materials share; writing its
`.value` retunes live, no rebuild. A shared `Vector3`
passed to `uniform(v)` stays a live reference. Module-level uniform nodes
that a setter writes (`fountainTime`, `mapAltitude`) are fine; what the
sun and the date move (`sceneNight`, `fountainsOn`, `clockMinutes`) lives
in `scene-environment.ts`, written by `setSun` through the environment —
a layer reads it and adds no setter. A scene-wide material drawn only
after dark wears `drawnAtNight` (its `visible`, no rebuild); a new compile
path shows the night-only materials under what it compiles for its call (`withNightMaterialsShown`), or
such a material builds in the first dusk frame. Inside `If`/branches read textures with an explicit `.level(0)` or
`textureLoad` (no implicit derivatives in non-uniform control flow).

What three keys a node build (TSL → WGSL/GLSL, **on the main thread**) by,
and therefore what keeps builds out of frames:

- **Never `InstancedMesh`.** Up to r186 three put an InstancedMesh's uuid
  in the render object's cache key (its instancing node binds that mesh's
  matrix buffer), so a tile's hundreds of vegetation cells, furniture
  models and lamp parts were hundreds of identical builds, in the scene
  and in the shadow pass. (r187 shares InstancedMesh builds; every layer's
  nodes, shared buffers and anchors are written for `Instances`, and
  moving back buys nothing measured.) `Instances` (`instancing.ts`) is a plain `Mesh` over an
  `InstancedBufferGeometry` view; the matrices travel as named
  instance-stepped attributes (`iMat0`…`iMat3`, colours `iColor`), so every
  set with the same material and attribute layout shares **one** build.
  The material applies the transform itself: `positionNode =
  instancePosition()` (or `instancePosition(local)` to bend the vertex
  first, as the crown sway does) and the colour
  (`colorNode = materialColor.mul(instanceTint())`). Extra per-instance
  floats: an `InstancedBufferAttribute` on the set's geometry, read with
  `instanceFloat(name)`.
- **`Instances` traps.** `drawCount`, never `count` — a `count` above one
  puts the uuid back in the key. `instanceTints`, never `instanceColor` —
  three multiplies the diffuse colour of *any* object with an
  `instanceColor` property by an InstancedMesh-only varying the set never
  writes, and the set renders black. After writing matrices set
  `instanceMatrix.needsUpdate = true` and call `computeBoundingSphere()`.
  Sharing: assign another set's `instanceMatrix` / `instanceTints`.
  Freeing a set is freeing its geometry (`disposeObject3D`).
- **Materials without per-tile data are `sceneMaterial(key, make)`**
  (`three-utils.ts`): one material, one build for the whole site (crowns,
  trunks, hedges, lamps, monuments and fountains, furniture, tram masts and
  wires, vine rows, ferry wakes, the splat pass).
  They carry `userData.shared`; `disposeMaterial`/`disposeObject3D` skip
  them and the last app frees them (`retainSceneMaterials`). Materials
  with per-tile textures (terrain, water, clay) stay per tile — builds per
  tile material are cheap (none over 20 ms in the spike); one shared
  material with textures bound per draw (`onObjectUpdate`) was tried and
  failed (grey ground, untinted clay).
- **The scene renders top-level into its own target** (`post-stack.ts`),
  and the `RenderPipeline` reads that target's colour and depth; the
  styles' swap and dressing wrap exactly that render. A build is keyed by
  the target's attachments and the **kind of camera** (r187; up to r186
  also by the call depth, so a scene `pass()` nested in the pipeline never
  found what `compileAsync` prepared). The frame names every target it
  draws into and ends on the canvas, never on the one it found set: a
  compile in flight sets the target it was called with again after each
  build it resumes (a three r187 bug: `docs/rendering.md`, "Workarounds
  for upstream bugs").
- **Compile ahead.** `PostStack.compile(object)` builds and compiles each
  drawable against the scene target (shown and unculled for the call);
  tiles await it in `processTileModel`, dressings compile one
  representative per material + draw kind + attribute layout
  (`compileRepresentatives` in `tile-stream.ts`), both capped at
  `COMPILE_WAIT_MS`. The crowns a date change may switch to are warmed by
  stand-ins (`crownWarmup`). **One compile at a time**: every
  `compileAsync` goes through `compileInTurn` (compile-lanes.ts) — r187
  keeps a compile's state (target, call depth, render context) on the
  renderer around every await inside it, and two in flight resume into
  each other's state and throw (an upstream bug, worked around until a
  release fixes it: `docs/rendering.md`, "Workarounds for upstream
  bugs"). Within one call three compiles the GPU
  pipelines side by side, so a whole set of stand-ins goes in one call
  (`PipelineAnchors.anchorAll`: the Ausschnitt's holds, Modell's warm-up)
  — never real tile objects, which a tile may free mid-call. A queued
  compile may start frames later: a drawable whose tile left while it
  waited compiles nothing (`left`, post-stack.ts), and a tile's own
  material anchored as itself leaves its set when the tile frees it
  (`onOwnedGone`, pipeline-anchors.ts). **Modell's
  parallel camera has builds of its own** (r187: a parallel view's light
  comes from one fixed direction): `PostStack.warmView` builds them while
  the dolly zoom in runs and for every tile landing while Modell shows;
  `holdCut` holds for Modell's camera. `compileAsync` primes the **main pass only**:
  the shadow pass's pipelines for new casters still build in the frame that
  first draws them, and the WebGL2 backend compiles synchronously — the
  price of public API. Measure with a flight before adding machinery.
- **Different graphs are different builds.** An optional raster that did
  not load leaves its term out of the terrain's colour node, so that tile
  builds apart; that is fine, but do not branch a graph on per-tile
  *values* — put them in uniforms. Toggling a graph-level flag
  (`side`, `alphaHash`, a new slot) needs `material.needsUpdate = true`.
- **Fog is `scene.fogNode`** (`height-fog.ts` `installSceneFog`): every
  material gets it; `material.fog = false` opts out (the river mist, the
  splat pass). Never fog a material by hand.
- **No custom depth materials.** The shadow pass draws
  `castShadowPositionNode ?? positionNode` and discards by `maskNode`: a
  swaying crown casts rigidly through `castShadowPositionNode =
  instancePosition()`; the bare crown thins its shadow through its mask.
- **Vertex formats.** WebGPU has no 1-component 8/16-bit vertex formats
  (and the WebGL2 backend rejects them against TSL's float attribute): the
  feature id is baked as FLOAT (`scripts/tile-glb.ts`); the roof flag
  rides in the windows' snorm16 `_FACADE` (−1 in its third,
  `lib/city/windows.ts` `FACADE_ROOF`).
  3-component snorm8/16 positions and normals are fine (three pads them).
- **Eight vertex buffers a draw on WebGPU** (the device's default limit;
  three requests no more). Each non-interleaved attribute is one buffer,
  `position` and `normal` included (an interleaved instance matrix is
  one). A ninth invalidates the pipeline and the mesh silently draws
  nothing on a real GPU, while the WebGL2 backend (sixteen) — the
  headless e2e's — draws it fine: the traffic flows vanished that way
  with ten single-float attributes. Pack scalars into vec4s and test the
  count.
- **Points are 1 px on WebGPU**, whatever their size. The lamp halos are
  billboard quads: an `Instances` set under a `PointsNodeMaterial`.
- **No tone mapping.** The output node is `renderOutput(…, NoToneMapping,
  SRGBColorSpace)`; the look was tuned without tone mapping (the old
  composer never applied the renderer's ACES). ACES washed the clay out.
- **Public API only**: no prototype patches, no `_`-prefixed members, no
  wrapping renderer internals. Subclassing a node material's documented
  `setup*` is the last resort; prefer a slot. The spike's render guard,
  shared-instancing patch and render-context override were rejected.
- Things a node material cannot reach, found in the port: the sun's shadow
  map from inside another material (three's public `shadow(light)` builds a
  second shadow node with its own map); `SkyMesh`'s own cloud horizon fade (inside its
  colour node) — the haze band covers it.
- 3DTilesRendererJS loads fine under `WebGPURenderer`; its fade and overlay
  plugins patch GLSL and stay unused.

More traps, each found the hard way:

- **A `ClippingGroup` switch rebuilds everything under it.** three keeps
  one render object per drawable for both sides and keys its build by the
  clipping, freeing the side a switch leaves; a compile that does not walk
  through the group builds the wrong side. Modell's Ausschnitt shows only
  once `PostStack.holdCut` holds both sides (`aloneUnder`), and leaves its
  shadows unclipped.
- **The clay is two varyings short of WebGPU's limit**: of sixteen
  inter-stage variables, `front_facing` takes one (and the Ausschnitt's
  clip distances one on the vertex side), and the clay passes thirteen
  of the other fifteen. A new value per building or per vertex rides in
  a varying it already passes; past fifteen the buildings vanish on
  WebGPU while WebGL2 still draws them (ADR 0010).
- **A TSL `select` is an if/else in the shader.** three builds each arm in
  its own scope: what an arm builds first is built again where it is used
  outside, and a derivative or texture read first built in an arm runs in
  non-uniform control flow (three turns WGSL's uniformity check off, so
  nothing says so). In a per-pixel graph use `mix`/`step` with safe
  denominators; a select whose arms are constants is harmless.
- **A `Loop`'s body is a scope too.** A node shared with the rest of the
  graph and first built inside the loop is assigned there, so only when
  the loop runs: the water's foam loop (no foam line on the tile: no
  iteration) left the waves' position at 0, and the Elbe lay flat on
  every tile without a weir beside a rippling one. Take what a loop reads
  of the fragment into a `toVar()` before it (`foamAt`, water-layer.ts).


Unit tests assert the node setup (a node material, the expected slots set,
the uniforms shared, instances written), not shader strings; node materials
and their node graphs construct without a GPU under `bun test`.

## Coordinate frame (critical)

Data is ETRS89/UTM, Z-up — EPSG:25833 (zone 33) for Saxony and Berlin,
EPSG:25832 (zone 32) for Hamburg, Bavaria and NRW; the provider sets it
(`sites/providers.ts`, `Provider.epsg`) and every path takes it from the
site. `world` is rotated −90° about X so data-Z (elevation) → scene-Y. Conversions (`lib/city/ground-clamp.ts`):

```
world.x = epsgX − cx       world.z = −(epsgY − cy)       world.y = elevation
```

`(cx, cy)` = recenter offset from the **spawn** tile's CityJSON loader matrix,
taken at bake time and carried in the tileset's root extras; every tile is
baked against it so they align. The glTF content is Y-up and the renderer's
up-axis turn cancels `world`'s rotation, so a tile's content root is the Y-up
frame. **Trap:** vegetation uses Y-up coords, so it never goes into the
rotated `world` group itself (else the −90° applies twice and trees launch
into the sky). Tiles are `<zone><EEE>_<NNNN>_2<suffix>` — the zone from the
CRS, the suffix the provider's (`_sn`, `_nw`, `_by`, `_hh`, `_be`); Dresden's
spawn tile is `33412_5656_2_sn`, Hamburg's tiles look like `32564_5932_2_hh`.

## Shadows — the recipe and why (this took many rounds)

`PCFShadowMap` is **soft**: three's `ShadowFilterNode` (`PCFShadowFilter`)
spreads a 5-tap Vogel disk, rotated per pixel, by `shadow.radius * texel`
(`node_modules/three/src/nodes/lighting/ShadowFilterNode.js`). Default
`radius` is 1 ≈ hard. (`PCFSoftShadowMap` has been deprecated since r182.)

The map is **four concentric rings** (`sun-rings.ts`,
`lib/city/shadow-rings.ts`, ADR 0009; the numbers are in
`docs/rendering.md`):

| Setting | Value | Why |
|---|---|---|
| `renderer.shadowMap.type` | `PCFShadowMap` | only soft option that doesn't ring (VSM "corduroy"-rings on grazing ground) |
| rings (`SHADOW_RING_HALVES`) | half-sizes 80, 240, 720, 2160 m | texels fine near, coarse far, whatever the view's or the sun's direction: a map warped over the view failed at a low sun looking along its light |
| ring edge (`shadowMapSizeFor`) | 2048 (phones 900; smaller at a raised safety level, ADR 0047) | four of 900² are less than a phone's old 2048²: they pay for what the wide rings' casters hold |
| `shadow.radius` | 2.5 (`RING_PCF_RADIUS`) | five samples over 5 texels leave gaps: a thin shadow shows them as a stipple |
| `shadow.normalBias` | **0** | a positive normalBias offsets the flat ground sample → bright peter-panning contact strip. Safe at 0 because terrain doesn't cast and solids cast via back faces (lit faces never self-acne) |
| casters' depth | the material itself | no custom depth materials: the shadow pass draws `castShadowPositionNode ?? positionNode` and honours `maskNode` |
| bias | 1.1 of a ring's texels, per ring, 2.5 m at most | residual cleanup |
| terrain `castShadow` | **false** | a casting terrain self-shadows into triangle/staircase acne at grazing sun; ground only receives |
| the map's colour target | none (`RingShadowNode`, set as `sun.shadow.shadowNode`: a depth array in a `count: 0` target, r187) | three's shadow map carries a colour texture of the shadow's `mapType` beside the depth, as large again, though only coloured shadows read it; keep `renderer.shadowMap.transmitted` off |
| `shadow.autoUpdate` | false | a ring redraws when it has drifted a fifth of its half-size, the sun moves or a caster changes (`invalidateShadows()`), one a frame, the longest waiting first, the wide two at a distance in time |

Traps of the rings:

- **One camera for all rings**, moved per ring (`placeRing`): three keeps its
  state per drawable and camera. Never a camera per ring.
- **A ring's matrix changes only as it is drawn.** Read a ring's map through
  `ringLookup` (`sunRig.shadowMap.rings`); `sun.shadow.matrix` and
  `sun.shadow.camera` hold whichever ring was drawn last.
- **Coarse rings do not draw thin casters.** A new thin caster calls
  `markThinCaster`: `tiny` (the finest ring alone: a coarser filter turns it
  into a smear) or `slender` (the first three: thin but long, a lamp post).
- **Plates and captures wait for the rings**: `handle.shadowBusy()`. They
  redraw one a frame.
- **Ask only what a change touches.** `invalidateShadows()` redraws all four
  rings; a tile's change goes through `invalidateShownTiles` (only the rings it
  can fall on, only if what shows changed), a change near the eye through
  `sunRig.invalidateShadow(undefined, finest)`.
- **`renderer.clear()` on a depth array throws on the WebGL2 backend**; the
  render's own clear is what draws a layer clean.
- The stream's square (`lib/city/shadow-fit.ts`, `sunRig.shadowCamera`) only
  loads tiles: `fitShadowRadius` and `shadowFocusAhead` have no say over what
  is shadowed.

### The far field: baked horizon + sky view (plan 033)

What the frustum cannot reach is baked: `pipeline/bake/skyview.py` writes,
from the committed DGM1 + LoD2 only, a **sky-view factor** (≈2 m) and a
**horizon** (≈8 m, 16 azimuths, two bands: occluders 80–1 500 m and
8–80 m away; eight layers of one array texture). The ground takes the
horizon as its material's **`receivedShadowNode`**, folded into the sun's
shadow by `min(shadow, lit)` (`sky-light.ts` `applyGroundLight`;
`groundLitMaterial` for what is baked into the fine terrain: kerbs, fences,
stairs, walls) — `min`, never a product, so an occluder both see never
darkens twice. **The near band only counts outside the shadow rings**:
the sun rig keeps the ground centre and half-size of the widest ring with
texels of 2 m at most in
`shadowReach` (a shared `uniform(Vector3)`, live by reference); the near
band fades in over that ring's last 20 % and beyond it the horizon is
max(near, far) — without it a street past the map lost the shadow of
the block beside it. Change the rings and this follows by itself;
never feed the near band inside them (its 8 m / 22.5° smear would
fight the map's crisp edges). The sky view is the **`aoNode`**, which three
multiplies into the indirect light only (after the lights; the sun is
untouched), on the terrain and the clay facades (`createClaySky`: sampled
2.5 m outside the wall, doubled, faded out toward the eaves); cells under a
roof carry the nearest open value in both rasters (no dark bleed through
LINEAR/mipmaps). Unjudged on a GPU — watch for SVF + GTAO reading as dirt in
courtyards (weaken the contact shadows there first) and the hand-over at
the frustum's edge.
[ADR 0009](../../../docs/adr/0009-shadow-recipe.md).

Dead ends (don't repeat): large `normalBias` (peter-panning), VSM at any blur
(rings/grid on lit faces), one map warped over the view (LiSPSM: gone at a low
sun looking along its light, ADR 0009), a radius of 5 on five samples (a
stipple). **Open limit:** past the widest ring the ground's shadows are the
horizon's (an angle at 8 m and 22.5°, no shape, not on facades or trees).

## Surfaces (the land-cover splat)

The bake writes only a **4096² class raster** (ids 0–9, `pipeline/bake/landcover.py`;
the ids and their names in `pipeline/bake/classes.py`).
At runtime `landcover-splat.ts` paints it with the one palette
(`lib/city/landcover.ts`, a `uniformArray`) into an RGBA target, one
full-screen `QuadMesh` pass per tile (a scene-wide node material per raster
size, `textureLoad` of the class ids; the class texture is on the GPU
before the paint — decoded in its turn (on a phone one raster at a time
for the site, uploaded at once, its bytes dropped; `tile-rasters.ts`,
`raster-upload.ts`); a
bitmap the decoder fell back to is never closed — a closed `ImageBitmap`
uploads empty on node pages): RGB = the pastel class colour,
**A = water coverage** (a 3×3 tent over the water class — the soft
shoreline). The terrain shader samples it `LinearFilter` + mipmaps +
**anisotropy 16** (GPU AA at grazing angles — kills the NEAREST staircase);
water reads the alpha and `smoothstep`s it for a crisp shoreline. Edge
sharpness is bounded by the class raster's resolution, not the GPU filter.
A colour change is a look change, never a re-bake (ADR 0010).

The terrain's colour node (`terrain-layer.ts` `splatColour`) composes its
terms in a fixed order over one shared set of inputs (`GroundInputs`) and
colour fields (`GroundColour`): the palette splat, the meadow mottle, the
ground fields, urban green, the ground detail, the allotment gardens, the
sports grounds, the road markings, the NDVI tint, then the gated contour
ink. A term whose raster is absent is left out of the graph.

**Ground detail** (`ground-detail.ts`, a term of the same colour node): the
kerb band, lawn edges, parking lanes and the paving rows along a kerb are
drawn at *signed distances in metres* from the baked, smoothed edge raster
(`pipeline/bake/edges.py` → `edges_<tile>.png`, RG, valid to ±6 m). The
class texels alone give that distance only within a texel of the edge and
follow the 0.5 m staircase — a shading-normal "kerb face" from them read as
dashes, and 2–5 m parking lanes from them as arcs. They remain the fallback
(4×4, box-smoothed) where the edge raster is absent. The same bake writes
the kerb lines; the fine terrain glTF stands a real 12 cm **kerb stone** on
them (`lib/city/kerbs.ts`, `kerb-layer.ts`; triangles wound CCW about their
normals — the first cut was clockwise and rendered black). The OSM paving
raster (`surface_<tile>.png`, RGBA: surface ids + parking bits, the bearing,
a per-segment along-street offset — along = offset + (position from the
tile's NW corner)·d, exact per straight piece) picks the pattern; every
pattern length along a street divides `SURFACE_ALONG_PERIOD` (165 m).
Rotating patterns by the bearing about the far data origin made every bend
a shower of arcs — don't. Both rasters are greyscale PNGs 2×/4× wide with
the bytes interleaved, so the viewer's own decoder (`lib/city/png-raster.ts`)
reads them exactly. *Bodendetail* and *Stadtgrün* (urban green painted as
meadow) are their fixed strengths (`GROUND_DETAIL`, `URBAN_GREEN`). The contour ink guards `fwidth == 0`.

**Sports grounds** (`sport-ground.ts` `sportGround`, same node, after the ground
detail): `pipeline/bake/sport.py` writes a table of grounds (frame,
surface, line scheme, shape) and an RGBA index raster (row on top, a
second row grown wider, the exact bit). The fragment evaluates up to eight
candidate rows' *analytic* shapes (rotated rect, a track's capsule band,
else the raster outline) and keeps the deepest — reading one row per texel
sawed teeth into a track's inner edge where the capsule model strays past
the mapped outline. Lines use `spLine`, an exact box filter over the pixel
footprint; keep new lines on it (no `smoothstep` lines — they shimmer).
Goals, posts and nets are dressing (`sport-fixtures.ts`), one merged mesh
per tile, owned by the tile holding the ground's centre.

**Road markings and allotment beds** (plans 026, 028) are two more
terms of the same colour node (`roadMarkings`, `colonyGarden`), fine level
only. `road-markings.ts` reads a
table of rotated rectangles (crossings, stop lines; axis across the road)
and an RGBA raster (`markings.py`: 16-bit row in R + 256·A, per-side
cycle-lane bit and centre-line bit in G, the signed offset to the
carriageway's middle in B — the side is resolved in the bake because the
paving raster's bearing is modulo 180°). Every stripe is box-filtered
exactly (`rmStripes`), and along-street periods divide 165 m.
`cultivated-layer.ts` paints faint beds on the colony raster
(`cultivated.py`) in jittered-Voronoi plots — no colony in the fifteen tiles
maps its parcels, so keep it faint.

## Parts meet the ground (ADR 0030)

The DGM1 rounds every real step into a 1–2 m ramp, so whatever stands on
the ground meets an edge that is not where its own is. Five layers got it
wrong at once (2026-09-30: the kerb's second step on the pavement, a quay
wall's jagged cap, bridge decks ending in the air, stairs in a trench, tram
beds decided per whole chain). The rules, in `lib/city/ground-join.ts`:

- **feet under** by a `SINK` row (band 5 cm, kerb 6, box/patch 20,
  planted/relief 25, wall 40, stair 60) — pick a row, don't add a number;
- **edges meet the ground**: `meetGround` (end the top at the ground's
  level, never below a floor such as the road), `reachLevel` (run on until
  the ground comes up to a flat or falling level: a cap, an approach ramp);
- **per-sample decisions smoothed along the part** (`farthestNear`; in the
  Python bakes a window majority + a minimum run, `tram.py`
  `smooth_beds`/`absorb_short`) — never one decision per whole line, never
  raw per sample (a sawtooth);
- **report the joins**: a builder returns `joins` (`foot` must reach the
  ground, `edge` must not stand > 5 cm above it), every metre along each
  span via `joinsAlong`. Baked parts are listed in
  `scripts/ground-joins.ts` `JOIN_PARTS`; its test holds each part's
  share of misses to a budget on the spawn tile. `bun
  scripts/ground-joins.ts [tile]` prints the shares and the worst places —
  render those, obliquely.

Before shipping a part that stands on the ground, answer in its doc
comment: what happens where the ground beside it is **higher** than the
part (a bank: Wange, cap run-on), and where it is **lower** (a raised
flight, a deck end: dig the DGM's shoulder down, land a ramp)?

## Terrain seams

Vertices sit at pixel centres, so a tile stops half a pixel short of its bounds;
abutting tiles of different resolution left a sky-gap "white seam". Fix in
`terrain-geometry.ts` (run by the bake now): snap the border ring to the true tile edge **and** drop a
vertical **skirt** (~30 m) so any residual height-mismatch crack shows terrain,
not sky.

## Vegetation

- Trees = `Instances` sets (trunk + crown), hedges = `Instances` of a
  trimmed block (`low-vegetation-layer.ts`), all
  on scene-wide materials (`sceneCrowns`, `sceneMaterial`). Crown =
  `IcosahedronGeometry(r, 2)` (180 tris) with lobes and radial normals. Three
  tiers per 250 m chunk, planned over the whole site on the 10 Hz pose
  tick (`lib/city/vegetation-lod.ts`, applied by `createVegetationLod`,
  whose arrays are kept between passes; `createLodSchedule` runs it in the
  frame the tiles in view change, or the eye jumps; the cadastre's own
  silhouettes are planned with the chunks, their cheap crown standing for
  mid and far): the
  **rich multi-tuft crown** (~1 440 tris) near the camera (in 220 m / out
  300 m) but only within a **site-wide budget of 2 500 trees**, nearest
  chunks first — forest tiles (one tree per 7 m, up to ~1 300 per chunk)
  otherwise put ~9 000 rich crowns on screen and lost the GPU context; the
  mid crown + trunk; and past 650 m (back at 550 m) a detail-1 crown (80
  tris), no trunk, dense chunks thinned to every other tree drawn wider.
  Trunks, mid and rich crowns of a chunk share ONE `instanceMatrix` (and
  the crowns one `instanceTints`) — ~9 MB instead of ~21 MB for a forest
  tile; compute each set's bounding sphere after sharing.
- Crown look (`buildCrownMaterial`): sway in `positionNode`
  (`instancePosition(sway.local)`, the per-tree phase from the instance's
  world column), the shadow rigid (`castShadowPositionNode`); occlusion
  and the gust's brightness pulse in `colorNode`, no `emissiveNode` (the
  backlit glow flattened the crown, removed 2026-11-06).
- Phones cache **168–336 MiB** of tile content at safety level 0 (148–296,
  136–272, 96–232 at levels 1–3; `tileCacheBytesFor` in
  `app/_components/scene-profile.ts`, `lruCache.min/maxBytesSize`),
  weighed as the GPU holds it (the dressing plugin's `calculateBytesUsed`,
  less the site-shared buffers; a tile that left is never re-weighed —
  the cache frees it inside its eviction, and `recalculateBytesUsed`
  there adds its bytes back to the total for good). `max` is derived: the governor's soft
  line − the fixed costs (24 B per drawn pixel + the shadow map) −
  100 MiB; `max − min` must exceed the largest tile (128 MiB on a phone).
  The 320–600 MB before had `max` above the governor's own hard line, so
  the cache never bound anything before Safari took the GPU; the 120–180 MB
  before that was broken the other way: a phone flying to the Alaunpark
  never loaded the ground there. See `docs/rendering.md`, "GPU memory on a
  phone", and ADR 0047 — with its two rules: an attribute read on the CPU
  after the dressing (or first by a later material) stays off the
  CPU-copy drop lists, and a site-shared buffer is never on a geometry
  that is disposed.
- **Chunking:** placements are bucketed into 250 m cells, one instanced set per
  cell (shared geo/material), so off-screen cells frustum-cull from both the
  main and shadow pass. After `setMatrixAt` you **must**
  `instanceMatrix.needsUpdate = true` + `computeBoundingSphere()` or the whole
  cloud is wrongly culled when the world origin is off-screen.
- Canopy from `pipeline/bake/canopy.py`: `nDOM = DOM1 − DGM1`, one tree per ~7 m cell
  at the tallest pixel, scaled to measured height, gated off road/bridge/water
  via the class raster.
- **Tree LOD (shipped):** the three tiers above; a tier change invalidates
  the shadow map (plan 009).
- **Cadastre + laser scan + hedges (all default-on):** the street-tree
  cadastre (`pipeline/bake/trees.py`), the laser-scan trees outside the canopy
  mask (`canopyx`, thinned in the bake against the cadastre within max(4 m,
  crown radius)) and the OSM hedges with their laser-scan height
  (`low-vegetation-layer.ts`, superellipsoid chains, static, chunked) from
  `pipeline/bake/lowveg.py`. The bake's laser-scan-only hedges and shrubs are NOT
  shipped (~30 % crown-rim false positives; `--step lowveg --research` writes them for
  research). Measured lesson: the LSC **multi-echo ratio is a tall-tree cue,
  not a shrub cue** (hedges 26 % vs fences 56 % at ≥ 0.5). Draw-call model:
  `scripts/eval/kataster-cost.ts`. Numbers in `docs/transformations.md`.
- **Species and season (plan 025):** the tree data carries the genus (`gn`,
  an index into the file's `genera` = `lib/city/tree-season.ts`
  TREE_GENERA) and the trunk diameter; OSM `natural=tree` fills in where the
  cadastre has no tree within 3 m. `crown-season.ts` turns the scene date
  into per-instance tints (`instanceTints`) and `aBare` (1 − leaf, read
  with `instanceFloat`) **on a change of calendar day only** (throttled,
  never per frame); a chunk with a bare crown wears the seasonal crown
  material, whose hashed alpha test in crown space (~1.25 px cells — fixed
  cells shattered big crowns into shards) is its `maskNode`, which the
  shadow pass honours, so the winter shadow thins. Cost:
  `scripts/eval/season-cost.ts`.

### Sandbox crown — what is left to port

Cost = `geometry_tris × instances`, paid twice (shadow pass). Still open:
**dappled canopy shadow** (a colour-less proxy caster per chunk whose
`maskNode` cuts the gaps — the shadow pass honours it). Radial normals
and the LOD-gated multi-tuft crown are in
`vegetation-layer.ts`.
`aesthetic-sandbox.html` at the repo root is the historical playground those
were ported from; the layer file, not the sandbox, is the source of truth.

## Bridges (ADR 0041)

Decks come from the Basis-DLM (`ver06_l` centrelines, `ver06_f` outlines),
built per fine terrain tile by `bridge-layer.ts` (called from
`rail-layer.ts`; the lift table and the approaches' plan are
`bridge-deck.ts`, which a layer that only rides the decks imports alone);
**only the tile owning a deck's centre draws it** (`BridgeContext.owns`),
every copy still lifts that tile's rails. The bake (`rail.py` + `bridge.py`) reads a DGM/DOM mosaic
700 m around the tile, so a seam bridge is the same in both files. What it
measures in DOM1: the **roadway** (lower third across the deck, held
−6/+4 m around the abutment ramp) and, on bridges whose class stands above
the deck (Wikidata over OSM: arch, truss, suspension, cantilever,
cable-stayed), the **ribs** — per half of the cross-section, the highest
surface over the deck, opened 7 m / closed 11 m, kept ≥ 3 m for ≥ 25 m.
Runtime (`lib/city/bridge.ts`): arch ribs share the tightest rib's
parabola (`archFits`) and are carried below the deck to the ground
(`archSpringing`) — the Waldschlößchenbrücke; a rib that fits no arch is
not drawn (catenary, trees). Truss/suspension ribs are drawn as measured
with pylons where they peak ≥ 10 m (the Blaues Wunder); cable-stayed gets
a pylon and a fan. The deck's `depth` comes from the OSM fairway clearance
over the DGM water; beam piers keep the fairway clear. The LoD2's own
bridge slabs (`53001_*`) are dropped from the building mesh.

**Surfaces** (`bridge-surface.ts`): the deck's top mesh carries its frame
per vertex (`aDeck` = station, offset, the outline's left/right there —
`addDeckFrame`, the outline's width read 3 m in from the ends; the top's
triangles split to ≤ 6 m, `splitDeckTop`, since the triangulation of a
curved deck joins vertices 190 m apart and the frame, exact at each
vertex, interpolates truly only over a short reach — the Marienbrücke's
carriageway sat 8 m off); the scene-wide deck material lays a road
deck out from it (footways, kerb and gutter, carriageway grain, centre
dashes on two lanes), a path deck as sand with kerbs, a rail deck as bed
and walkways; the stone (fascia, parapets, piers, masonry) is ashlar in
world space along each face's own horizontal. Fine detail fades by
`fwidth`; the footway/carriageway split and the mottle hold to 1 : 10 000.

**Lines take their level along the whole line** (ADR 0041). Rails and
trams are not lifted onto whatever deck lies under a point (a lower line
jumped onto the flyover above it; an upper one fell into the DGM's gap
beside its deck): `lib/city/levels.ts` picks, per 4 m (rail) / 2 m (tram)
sample, the ground or a deck within 2 m by a Viterbi on the climb beyond
the grade (rail 4 %, tram 8 %), then a grade cone turns a gap the line
cannot get down into from either side into a *span* (the layer draws a
span deck, `addSpanDeck`) and a fill it cannot climb into a *cut*. The
build solves every piece with 450 m of context from the pieces that run
on through its ends (`lib/city/line-levels.ts`) and publishes the runs as
`lv`; a cut ≥ 30 % under a drawn deck opens a passage in the terrain bake
(`lib/city/passages.ts`). Check with `bun scripts/line-levels-cli.ts <site>`.

**Underground is not drawn.** The DLM's rail lines say nothing of a
tunnel, so `rail.py` cuts a stretch that runs within 2 m of a DLM tunnel
(`ver06` `BWF=1870`) for more than 15 m — a shorter overlap is a surface
track crossing over it (a 6 m reach took Munich Hauptbahnhof's surface
tracks). DLM trams (`BKT=1201`, standard gauge in Bavaria) are the OSM
tram layer's. OSM platforms below ground (`osm.below_ground`: tunnel,
`location=underground`, negative `layer`/`level`) and tram ways in a
tunnel (`osm.in_tunnel`) are skipped. A tram's `street` bed is any
pavement: road, path (squares, pedestrian zones) or built-up.

## Tiles: batching, lifetime, freeing, rays, streaming

**Buildings are already batched.** Each tile's buildings are ONE glTF mesh
(`scripts/bake-city-mesh.ts` runs `cityjson-threejs-loader` at build time
and, `cityMesh`, writes it with a per-vertex feature id,
`EXT_mesh_features`), so draw calls are already low and **BatchedMesh would
not help** (and would break feature-id picking/demolish). Per-building data
(tint, heights, roof colour, glow, roughness, the demolish tree) is **one row
per object** in an `EXT_structural_metadata` property table, packed into a
float texture the clay shader reads (`lib/city/city-mesh.ts`) — add a
building attribute there, not as a vertex attribute. A word packed into
bits there (the windows' style) or a value that seeds a hash (the
roughness jitter) reaches the fragment as a **flat** varying
(`setInterpolation(InterpolationSamplingType.FLAT)`): interpolated, even a
value all three vertices share drifts by a few ulps, which past 2²⁰ reaches
a word's low bits and which a hash magnifies into a new value every pixel
(a loose grid's windows frayed at their sides). The perf bottleneck is
**fill-rate** (post FX + shadow map), not draw calls.

**Tiles come and go.** 3DTilesRendererJS loads and unloads tiles by
screen-space error (`app/_components/tile-stream.ts`; two terrain levels,
the coarse one's geometric error is `COARSE_TERRAIN_ERROR` in
`lib/city/tileset.ts`). Everything a tile brings (dressing, BVH, materials,
textures) is built in the dressing plugin's `processTileModel` and freed in
its `disposeTile` — never in `bootApp`, or it leaks when the tile unloads.
Before a tile or its dressing shows, its node materials are built and
compiled with `compileAsync` against the scene pass's target
(`PostStack.compile`, each drawable shown and unculled for the call) — add
new per-tile objects inside that path, or they build inside a frame.
**Freeing is on us, not on three or the tile renderer** (WebGPU keeps GPU
state per drawable that WebGL never had). WebGPURenderer frees a
drawable's render objects — its uniform buffers and bind groups — only on
its material's `dispose` or its own `dispose` event, and a scene-wide
material is never disposed; 3DTilesRenderer frees only the glTF's own
materials (not the per-tile ones the dressing put on), and on a load it
aborts after `processTileModel` it frees the textures alone — geometry a
compile already uploaded would stay. So a tile's release runs
`disposeObject3D` over its content (`releaseRenderState` dispatches the
event), a released or aborted tile is freed by the plugin itself, and
nothing released is compiled. Leak hunts: `handle.getGpuDebug()` sets the
scene's buffers against three's `info.memory` (a gap that grows per visit
to the same place is a leak; a steady one is the tile cache). What a
tile adds beyond its glTF must reach the cache's weighing
(`DressingPlugin.calculateBytesUsed`), and a phone's memory is watched
by `lib/city/memory-governor.ts` — see docs/rendering.md, "GPU memory on
a phone". A part that lands after its tile is a `LatePart`
(`late-parts.ts`: the dressing, the murals, the traffic bodies, the window niches), which
weighs it from its build, frees it after its compile and reports for it.
A content's CPU copies go once its compile has uploaded them
(`dropCpuCopies` over `cpuDroppable` / `cityCpuDroppable`, ADR 0047; a
compile resolves only once every drawable under it is uploaded, those
another compile had started too — `compile-lanes.ts`): **an
attribute read on the CPU after the dressing, or first read by a material
the tile's own does not use, stays off those lists** — met after the drop,
three uploads an empty buffer. **A buffer the site shares**
(`markSceneShared`: the coarse grid's and water's index) **is never on a geometry when
that geometry is disposed** — three would destroy it for every tile;
detach it first. A lost GPU reloads a safety level lighter, where the
player stood (`gpu-recovery.ts`, ADR 0047).
The terrain has no BVH: ground rays march the height function
(`lib/city/ground-ray.ts`) — the coarse grid's vertices, or the fine TIN's
triangles through a bucket index (`lib/city/terrain-tin.ts` `TinIndex`).
**A building tile's BVH is built when a ray first needs it** (ADR 0024,
`ensureCityBvh`), so a ray against the buildings goes through
`nearestCityHit`, `cityObjectsAlong` or the collider, which ask only the
tiles whose box the ray enters and build (or skip) a missing BVH — a
plain `intersectObject(city.mesh)` on a tile without one is
three-mesh-bvh's brute-force fallback over two million triangles. The
tiles near the camera get theirs ahead in the BVH worker
(`bvh-client.ts`): their positions and index are handed over meanwhile,
so **nothing may read a building tile's CPU positions or index while
`bvhBuilding` says so** — skip the tile or wait. The glTF extras key is **`tileId`**: the
renderer writes `userData.tile` itself and would overwrite ours. The
walk/fly camera does not stream itself: the renderer streams for its twin
whose far plane ends where the fog does, on a phone at 2.2 km at the
latest — not through Modell's dolly zooms, which back it kilometres away
(`streamFarFor`, `lib/city/atmosphere.ts`; synced each frame
before the update) — past the
fog's end a tile shows nothing, and the camera's 6 km far plane loaded the
site's every building tile in that direction as fog colour; register a new
streaming need against that twin, not the camera. The sun's shadow camera is a second
streaming camera while the sun is up, so tiles that cast into the view stay
loaded (by night it streams nothing: `streamShadowTiles` in `create-app.ts`;
on a phone never, `shadowTilesStream`) — at 128 px on a desktop
(`SHADOW_STREAM_PX`), not the map's resolution: an orthographic camera's error ignores distance, and at
2048 px it refined the terrain under its whole frustum;
`displayActiveTiles` keeps loaded tiles drawn while turning.


## Performance model

The bottleneck is **fill-rate**: the post
pipeline (GTAO is the priciest) and the shadow-map render — which is why
**DoF** is skipped while the camera moves (`lib/city/regression.ts`; a
phone does not build it at all — its targets were the cost there, not its
passes). **AO is
not**: the contact shadows blinked on every footstep, so GTAO instead runs
permanently at half resolution (`resolutionScale = 0.5`, normals
reconstructed from depth, radius 2 m, occlusion raised to
`AO_EXPONENT`, 1.5) — about what the skip saved, paid every frame. Its sample
count (`aoSamplesFor`: 16, lite 8) rebuilds the pass's material, so it is a
construction-time setting. DoF is dropped by switching between **two
prebuilt `RenderPipeline`s** (with and without the lens blur, both
built under the load screen), never by swapping one pipeline's output node,
which re-translates the whole post graph on the main thread. SMAA carries
the anti-aliasing (the canvas and the scene target have no MSAA) — once, in
a last pipeline over the target every pipeline draws into; a phone uses
FXAA inside that last pass instead (no targets of its own). Buildings
are opaque clay only; `MeshPhysicalMaterial.transmission` ≈ doubles scene
cost, so the frosted "ghost" style was dropped rather than kept as an
option. `handle.getRenderInfo()` exposes `renderer.info` of the last frame
— every pass (shadow map, scene, post). Spike numbers (Apple Silicon,
Chrome): WebGPU 40–80 % faster than the old WebGL path at the same look;
the WebGL2 backend on par in steady state but stalling while it compiles
(`docs/plans/completed.md`, plan 020).

## QA: self-verify on a real GPU

The in-app **Snapshot** panel serializes camera + sun time + the look's
controls (*Nebel*, the style, the data layers) to JSON; `__poc.handle.getCameraState()` / `applyCameraState()` replay it. To eyeball a
change yourself:

```bash
# drop the snapshot JSON into shots/, then:
bun run shots   # = SHOTS=1 playwright test e2e/snapshot-shot.spec.ts --headed
# writes shots/<name>.png (HUD hidden, real GPU). shots/ is gitignored.
# Before/after pairs: SHOTS_QUERY=scene=lite SHOTS_TAG=x bun run shots
# appends the query to the page URL and writes shots/<name>.x.png.
# The shots are taken at /dresden; SHOTS_SITE=leipzig takes them in another
# built city.
# The committed QA views (qa/views/*.json, plan 019's reference views,
# written by `bun scripts/qa-views.ts`) render too, as shots/qa-<name>.png;
# one of them: bun run shots -- --grep qa-<name>.
# Plain `bun run test:e2e` ignores the harness (testIgnore in playwright.config.ts).
```

A view also travels as a link: *Link kopieren* writes
`/<site>?snap=<base64url of the snapshot>` (lib/city/snapshot.ts) — in
the query, like every URL parameter, so the host's request log shows it
(the privacy page says so; the crash trail keeps only the QA knobs);
the boot reads it through `parseSnapshot` (a waiting GPU recovery wins,
`lib/city/gpu-recovery.ts` `arrivalOf`). Another link is another page
load.

Headless e2e uses SwiftShader through the renderer's WebGL2 backend (headless
Chromium has no WebGPU adapter) — shadows/AA look nothing like a real GPU, so
use `--headed` for any lighting work. To check the fallback on a GPU, add
`?gpu=webgl2` (`SHOTS_QUERY=gpu=webgl2`); to see a lighter page of the
safety ladder, `?safety=1`–`3` (ADR 0047: pixel ratio, shadow map, tile
cache and governor a step down; nothing stored). Verify from **oblique** angles (a tree through
a bridge is invisible looking straight down). Snapshot JSON shape:

```json
{ "v": 1,
  "camera": { "mode": "fly", "pos": {"x":0,"y":0,"z":0}, "epsg": {"x":0,"y":0},
              "headingDeg": 0, "pitchDeg": 0, "fov": 55 },
  "date": "2026-06-15T08:30:00.000Z",
  "look": { "fogPct":35,"style":"pastel" } }
```

**Budget the e2e specs in frames, not seconds.** Under SwiftShader every pixel
is shaded on the CPU. At the **full** profile this scene costs ~**14 s to boot**
and ~**4 s per frame** at 1280×720 (measured on four cores). Anything that waits
on rendered frames — the control walk uses `waitForFrames` — walks straight into
the per-test timeout if it spends frames carelessly. Playwright runs a single worker on CI for the same reason: parallel
viewer pages halve each other's frame rate. CI splits the suite over **three
runners** instead (the `e2e` matrix in `.github/workflows/ci.yml`), by tag: the
whole site with the shell and `/wissen`; the desktop HUD group
(`@desktop-hud`) with the phone (`@phone`); the desktop rendering group
(`@desktop-render`). Each desktop group boots its own page. The required
status check "E2E (Playwright)" is the small job that reports them all. A new
spec lands in the whole-site shard unless it carries one of those tags —
keep the shards within about 1.5 minutes of each other (the workflow's
comment has the measured runs).


### The `lite` scene profile (headless e2e only)

`?scene=lite` (`app/_components/scene-profile.ts`) exists because SwiftShader
shades every pixel on the CPU. It changes four knobs (tiles, shadow map,
render scale, AO samples), all resolved once in `city-walk-client.tsx`
(`currentSceneBudget`) and handed down as numbers:

| Knob | full | lite | Why it is the right knob |
|---|---|---|---|
| tileset streamed | `tileset.json` (every site tile) | **`tileset-spawn.json`** (spawn tile only) | 3/4 of the geometry AND 3/4 of the boot (measured on the old block loader: 14 s → 4.4 s, 74 MB → 18 MB) |
| shadow ring edge (`shadowMapSizeFor`) | 2048 | **256** | the depth pass is fill that does *not* shrink with the canvas |
| `pixelRatio` | dpr≤1.5 | **0.5** | the canvas fills the viewport and the HUD needs ≥768 px to lay out, so render scale is the only honest way to cut fill-rate |
| GTAO samples (`aoSamplesFor`) | 16 | **8** | half the AO samples; keyed on the profile, not `navigator.webdriver` (Playwright sets that in the `--headed` shot harness too, which must show the product's AO) |

Everything a spec asserts on — loaders, layer construction, every node
material, the HUD wiring — is identical in both. **Never** use lite to judge a
render: it is coarse by design; that is what the `--headed` harness above is for.

The specs share one booted page per context (`mode: "serial"` + `beforeAll`),
because boot is the largest fixed cost left once frames are cheap. The
`snapshot-shot.spec.ts` harness deliberately stays on the **full** profile.


## Data pipeline

Every script takes the site as its first argument (`bun run fetch leipzig`,
ADR 0037); its data is `data/<site>/`. One deployment serves every site
whose data is ready, each at `/<site>`; `/` is the start page.
Bulk raw downloads (DLM, DOM1, DOP, OSM `.osm.pbf`) stay in the gitignored
`data/_raw/<provider>/{dom1,dop,dlm,osm,trees,lsc,downloads}`, shared by the
provider's sites; no Git-LFS. The build sources are the CityJSON **and the
DGM1 GeoTIFF per tile in `data/<site>/{cityjson,dgm}/`** — `prepare-data.ts`
bakes the terrain from it at build time and the canopy/rail bakes read it —
next to the small derived artifacts in `data/<site>/{dlm,dop}/`. Dresden,
Grimma, Hamburg, Leipzig, Meißen, München and Unna are committed; a new
site's folder is a maintainer decision. `bun run fetch <site>` downloads everything through the
provider's adapter (`pipeline/bake/providers/<id>.py`) and converts the LoD2
CityGML itself (`citygml.py`); `bun run site <site>` says what is missing.

**Stage 1, the offline bakes** (ADR 0037): one Python package,
`pipeline/bake/`, in a uv environment (numpy, rasterio, pyogrio, shapely,
Pillow, scipy, scikit-image; GDAL inside the wheels, with the OSM driver;
laspy for the laser scan — no PDAL). If a tool is missing,
fix the environment (`pipeline/pyproject.toml`), don't bend the code.
`bun run bake <site>` runs every step for every tile of the site with its extent and
CRS, land cover first:

```bash
bun run fetch dresden                  # download what the site needs (its provider's adapter)
bun run bake dresden                   # every tile, every step
bun run bake dresden 33412_5656_2_sn   # one tile, all steps
bun run bake dresden --step canopy     # one step; the order is STEPS in pipeline/bake/__main__.py,
                                       # each entry's comment says what it must follow;
                                       # `transit` runs once for the site (SITE_STEPS)
bun run test:pipeline                  # pytest + ruff
```

Missing DOM1 or DOP skips the canopy, NDVI and roof-colour steps (the
runtime falls back); rail decks fall back to the DGM ramp. An RGB-only DOP
(Bavaria) gets the NDVI raster from the visible bands (GLI, `ndvi.py`
`_gli`). Every flight's index is mapped onto Dresden's scale (its
carriageways and mown lawns as anchors, pooled over the site's tiles), so a
green threshold tuned on Dresden holds in every city — never tune one per
site. Without a Basis-DLM (Hamburg, Berlin) `rail` reads OSM
(`rail_osm.py`: rails, ballast beds, bridge ways merged per bridge and
level) — it runs before `canopy`, which keeps crowns off those decks.
Stand-ins are marked per city in the generated
`docs/guide/*/sources-by-city.md` (`bun run docs:matrix`, ADR 0012). `rasters.py`
refuses a height mosaic flatter than 0.5 m (1–99 %) — Hamburg's DGM was
once committed as 0 m everywhere and every house floated; the pipeline
tests hold every committed DGM to ≥ 2 m. The laser scan (`--lsc`) is read
for Saxony (GeoSN's LSC), NRW (3D-Messdaten) and Bavaria (four 1 km LAZ
merged per tile by `lsc.merge_laz`, each provider's classes mapped into
AdV's by its table — NRW keeps the crown tops in class 1); every scan's
intensities are normalised against its own ground (`lsc.rasterise`).

The later modules, one step each: `osm_buildings.py` (shops, heritage,
material and colours per LoD2 object), `markings.py`, `cultivated.py`, `tram.py`,
`riverside.py`, `skyview.py` (DGM + LoD2, the rebuilt roofs of `roofs.py`
in place of theirs), `small_buildings.py` (plan 034),
`landmarks.py` and `structures.py` (plan 050; landmarks first, the relief
is measured on their objects). **Seams:**
a step whose result must agree on both sides of a tile edge reads the
neighbours through `Tile.neighbours` (the committed DGMs): markings
measure on the neighbours' class rasters and paint a neighbour's crossing
that reaches in, cultivated
takes a vineyard's slope from every DGM it touches, tram and small-buildings
read the neighbours' furniture / scan — so bake those steps on every tile. All OSM layers come
from the Geofabrik extract — no Overpass.

**Stage 2, the build step** (`bun dev` / `bun run build` →
`prepare-sites.ts` → `prepare-data.ts <site>` for every ready site, then the
index `public/data/sites.json` the start page and `app/[site]` read): per
site the tileset (`tileset.json`, `tileset-spawn.json`), per tile
`city_<tile>.glb.gz`, `terrain_<tile>_l0|l1.glb.gz`, `footprints_<tile>.json`
and the side files, all content-hashed under `public/data/<site>/` with its
`manifest.json` (and the shared `sites.json`) as the no-cache entries. `scripts/tile-glb.ts` owns the
glTF writing (meshopt, quantisation, the feature table); the `.tif` and the
CityJSON are never served. It caches by content in `.cache/prepare-data`.

## Researching three.js releases

GitHub's releases **HTML** page is JS-heavy and reads poorly via WebFetch.
Authoritative: `registry.npmjs.org/three/latest` (version),
`github.com/mrdoob/three.js/releases.atom` (feed),
`raw.githubusercontent.com/wiki/mrdoob/three.js/Migration-Guide.md` (API
changes). Confirm shader/behaviour claims in `node_modules/three/src`.
On a bump, go through *Workarounds for upstream bugs* in
`docs/rendering.md` and drop what the release fixed.
