---
name: rally-maps
description: Create or edit Gravel Rally maps (road layout, terrain, jumps, scatter, road-side props, environment) and verify them. Use for any request about rally stages, tracks, terrain, forests, crowds, start/finish, or the map viewer.
---

# Rally maps

Every stage needs `tyre` (`StageDef`, required `TyreId`: the recommended compound for its road surfaces - `tarmac`, `mixed` or `gravel`, see `physics/tyres.ts` / `src/games/rally/PHYSICS.md`; the recommended suspension follows from it); `integration-tests/rally/tyres.test.ts` lists the maps it drives (add the new id).

A map is pure data: one folder per map, `src/games/rally/maps/<id>/map.ts` exporting a `MapDef` (the world) with its
`stages` (`stages.ts`: the events on it, rally `DETAILS.md` "Maps")
(format in `maps/shared/types.ts`; helpers shared by maps in `maps/shared/`), registered in `maps/index.ts`.
Map-specific files (baked `data.json`, `TODO.md`, later textures / props) live in the map's folder.
Every map folder has a `DETAILS.md` tracking ALL external links / files used (route links, data sources +
licences / citations, downloaded files, reference screenshots) - add one short row whenever you use a new source (no prose; `AGENTS.md` "Write short"). Public-facing
sources (data sets) also go in `MapDef.sources` (label / url / note; a stage's own route link in `StageDef.sources`) - listed on the main menu About screen. Everything (heightfield, road carving, trees, colliders) is
generated deterministically from it. There is no map editor on purpose — edit the data.

## Coordinate system

+X east, +Z **south** (north = -Z), +Y up, metres (three.js is right-handed: +Z north would mirror real maps).
`bounds` = streamed/playable area; terrain outside rises (`edgeRise`).

## Editing the road

- `road.points`: Catmull-Rom control points `[x, z]`, or `{ x, z, dy, width }`.
  - Keep consecutive points 30-80 m apart; tight hairpins need 3-4 points ~25-35 m apart.
  - The road must not cross itself or come within ~50 m of another part (terrain carving blends to the nearest road).
  - Crest / jump: three close points (~15 m apart) with `dy` 0 -> 1.5..2 -> 0 (see test map #16-18).
- Height: the road follows terrain smoothed over `smoothing` m, clamped to `maxGrade` (0.11 = 11%), the grade changes rounded over
  `gradeSmoothing` m (default 12; fast stages need ~50 or a +7/-7 % kink launches the car), then `dy` is added.
- Cross-section: `width`, `shoulder` (loose verge), `ditch`, `crown`.
- Surface changes along the stage: `road.sections: [{ from: <metres along>, surface, texture }]` (applies until the
  next entry; `road.surface` / `texture` are used before the first). E.g. asphalt valley road -> gravel climb
  (`maps/petralica`). Real maps: check Street View for where the surface really changes.
- `stage.start` / `stage.finishFromEnd` / `stage.splits` define timing. They also place the start / finish gantries, the lines
  and the split boards automatically (`world/stage-signs.ts`; the gantry header shows `name` + `year`) -
  do not add arch props. Every map needs `year`.

## Terrain

`terrain.layers` noise (scale = feature size m, amplitude m, `ridged` for crests).
`flatAreas` = pads (service park / test pad); `name` makes them spawnable (`?spawn=pad`) and shown in the viewer.

## Scatter & props

- `scatter` rules per asset: `density` per 1000 m², `minRoadDist` (from road EDGE), `maxSlope`, `mask` (noise clustering
  -> forests/clearings), `scale`, `tilt`, `alignToGround`, `sink`, `detail` (grass: only near camera).
- `roadside` rules: `every` m or `at: [metres]`, `side` (`outside` = outside of the bend), `offset` from edge,
  `maxRadius` (only in tight bends), `count/spread/depth` (crowds), `faceRoad`.
- Real maps: grow the area by widening `detail` / `landcover` / `outer` extents and ADDING the new strips to
  `osmBoxes` (each box is downloaded / cached on its own, the first wins: the old area's route, roads and building ids
  stay identical - diff the old and new `data.json` to prove it). `railways.drop` leaves out tracks of given services
  inside a box (a freight yard the track bed cannot level). Far backdrop: `python scripts/realmap/horizon.py <config>` (a grid takes `radius` or a world `extent`: reach far where the view goes, little behind a ridge - Vodno); `buildings.dropWays` = OSM ways a landmark asset draws instead; `paths.dropWays` / `dropKinds` leave roads / kinds out (a junction ring the engine cannot level, gully streams that hold no water), `paths.mergeJoints` joins ways that meet end to end at a plain two-way node (short ways = a height step at every joint); `MapDef.aerialways` = a cable car line (pylons, ropes, cabins).
- `cornerFans: {}`: tape + spectators + flags on the inside of tight corners over the whole stage (`every`, `maxRadius`,
  `chance`, `fans`, `flagChance`, `tapeOffset`; `world/corner-fans.ts`). Use it on rural stages; hand-placed crowds
  (`roadside` `at`) stay for the big spots.
- `servicePark`: team bays at the start on a `ServiceLot` (`maps/shared/service-lot.ts`); add a `terrain.pads` entry with `servicePad` for the same rectangle (see `maps/ajvatovci/service-park.ts`).
- `props`: explicit, either `x/z` or `along` (+`lateral`, negative `along` = from the end).
- Asset ids must exist in `assets/catalog.ts` (see the rally-content skill).

## Verify (always)

1. `npm run test -- tests/rally/world.test.ts` — prints road length, max grade, control-point distances (use
   these to place `at:` props), checks the road is flat/gravel and no solid scatter is on the road.
2. `npm run test:integration -- integration-tests/rally/stage.test.ts` — the autopilot must finish the stage with every car without rolling.
   If it fails, trace the failing distance (lower `maxGrade`, widen a hairpin, move a crest out of a corner).
3. Look: `/games/rally/map-viewer.html?map=<id>&stage=<id>` (one stage of the map, default the first; oblique overview, `grid=1` chunk grid, `splat=1` surfaces,
   click terrain -> "Drive from here").
4. Drive: `/games/rally/?stage=<id>&spawn=<metres along the stage>&mute=1` to test a section directly.
5. **No sound while testing**: add `mute=1` to every game URL you open (see AGENTS.md "Sound while testing").
6. **Stage card** (every stage, stage select; a stage without one is built live in the menu, dev warning): NEVER re-bake on your own - only when the user asks. Then
   `/games/rally/?bakecard=<stage id>&season=all&mute=1` (or `?bakecards=1&season=all`; `season=` one of spring / summer / autumn
   bakes just that picture, none = the map's own season; one `<stage id>-<season>.jpg` per season in `environment.groundTints`) on `npm run dev:noreload` (launch config `portal-dev-noreload`;
   on the normal server each saved card - or another session's edit - reloads the page and restarts / cuts off the bake),
   wait for "saved", and the changed `maps/<map>/preview/<stage>.json` + `<stage>-<season>.jpg` go in the commit. An out-of-date card only warns in the dev console -
   mention it to the user. `stageCardHash` covers only what the card draws: text (names, descriptions, tyre, links) and
   `previewRelief` (e.g. 1.8 on a flat map) need no re-bake. Code: `tools/stage-card*.ts`.

## Real-world maps (OSM + elevation + land cover)

Example: `maps/ajvatovci/` (`map.ts`, baked `data.json`, task list `TODO.md`, sources `DETAILS.md`);
`maps/shared/real-map.ts` helpers.

1. Config `scripts/realmap/<id>.json`: `origin` (lat, lon = world 0,0), `waypoints` (route start / end / via,
   e.g. from a Google Maps directions URL), world-space extents for the `detail` (10 m) / `outer` (50 m) height
   grids and the `landcover` (5 m) raster, `canopy` heights subtracted from the surface model, `minCornerRadius`.
   Optional: `dem` (`file` = local GeoTIFF or the OpenTopography `.tar.gz` in `sources/maps/<id>/`, `credit`) instead
   of Terrarium tiles - the detail grid must lie inside the file, the horizon grid falls back to Terrarium beyond it;
   `landcover.highTrees` / `osmWood` = `"trees"` where the woods are broadleaf (default: pine plantations); `landcover.plainOrchards = false` keeps big lowland tree patches as woods (default: they become `orchard`, which only suits farmland maps - a city forest turns empty), `landcover.plainTreesAs = "shrub"` makes them scrub (a valley of bushes); `landcover.manualCover` = hand-traced lat / lon rings painted over the cover (orchards WorldCover reads as crops: fit the screenshot to the baked route line by ICP, see ajvatovci DETAILS.md "Traced land cover");
   `landcover.belts` = cover by altitude (`[{from: [covers], to, min?, max?}]`, DEM metres, e.g. oak -> beech -> pasture on a
   mountain; covers `beech`, `pasture`); `lakes.levels` = fixed water level by lake name (big multipolygon lakes are stitched
   and clipped to the map, `LakeDef.level`); `paths.keepNear` = `[[lat, lon, radius]]` keeps every road round the stage ends
   beyond `paths.corridor`; `buildings.box: true` = one Overpass building query for the box (long winding routes);
   Mountain roads: `barriers: hairpinRails(data.route, { maxRadius: 30, lead: 20 })` rails the outside of every hairpin.
   `buildings.worldcover: true` generates houses on WorldCover built-up ground where no footprint data set covers
   the area (source `wc` - say so in the map DETAILS.md); `buildings.manual` = known buildings by lat / lon;
   `msRoads: { country, clearance, minLength }` adds roads OSM lacks from Microsoft ML Road Detections (ODbL,
   `msroads.py`, dirt tracks, needs pyarrow >= 21) - it finds side roads, not forest tracks under trees.
   **Check the route against the user's link** (overlay it on their screenshot): the shortest OSM path can take
   another road, and OSM may not have the road at all. Missing parts: `python scripts/realmap/trace_route.py
scripts/realmap/<id>.json` (config `trace`: screenshot, start / end marker pixels, line colour) prints
   `extraWays` for the config; add a via waypoint on each. Traced parts are only as good as the screenshot -
   list them in the map DETAILS.md + TODO and ask for close-up crops.
2. Bake: `python scripts/realmap/bake.py scripts/realmap/<id>.json --preview` (needs numpy, scipy, Pillow,
   opencv-python; downloads are cached in `scripts/realmap/.cache/`). It prints route length, control point
   spacing, min corner radius, self-proximity; `--preview` writes a land cover + roads PNG (north up).
3. Map file: `terrain.heightmap` (+ `offset` so the start is near y = 0, small noise `layers` for detail,
   `edgeRise: 0`), `landcover` (+ `splat` weights per cover, `fields` patchwork), `paths`, `road.points` from
   `data.route` (widths per section), `geo`, `credits: data.meta.sources`.
4. Scatter by cover class: `cover: ['pine']`; orchards `rows: { spacing, rowSpacing }` (row angle per zone);
   `minPathDist` keeps trees off other roads / canals (default 1.5 m solid, 0.4 m grass). Other roads are carved
   flat on their own smoothed height line (`PATH_PROFILE` per OSM kind in `world/terrain-gen.ts`); a new road kind
   that should be smoother / steeper gets a row there. `tests/rally/side-roads.test.ts` checks them. Water ways
   (canal / drain / river / stream / ditch / brook, depth per kind in `CHANNEL_DEPTH`; a `brook` - 1 m, 0.2 m deep, bake
   config `waterways` kind - is crossed on culverts: roads fill over it) are carved and filled with water
   automatically (`world/water-mesh.ts`); `tests/rally/water.test.ts` checks every channel holds water. A street along a drain bank
   stops its embankment at the water (only its own surface crosses a channel, as a culvert); a drain ending in another
   drops until its water meets that channel's over its last 60 m. A stream OSM lacks (a lowered valley with no water):
   `python scripts/realmap/dem_stream.py <config> --at=<x>,<z>` traces the DEM flow line through that point down to the
   next baked water way and prints a config `waterways` entry (lat / lon); the baker appends it as a `stream` path. To add
   it without the other drift of a full re-bake, bake to a temp `out` and copy only the new path (+ the buildings it drops);
   worked example `maps/petralica/DETAILS.md` "Valley creek". Lakes /
   ponds / reservoirs come from the baker (`data.lakes`): set `lakes: data.lakes` in `map.ts`. To add them to an
   already baked map without renumbering its buildings, bake to a temp `out` and copy only `lakes` into its data.json. Roadside `minRadius` keeps solid props out of hairpins.
   Junctions: side roads are joined to the stage road automatically (`world/junctions.ts`); add
   stage `closures: { asset: 'road_barrier', length: 2.2, setback: 4 }` (+ `stageMargin` on a map with several stages) to
   close their mouths like a real stage. Check them in game (`/games/rally/?stage=<id>&spawn=<along>`; `__rally.world.gen.junctions` lists every one).
   Season month: `environment.months` (`{ spring: 4, summer: 7, autumn: 10 }`, the default) says which month each season is driven in; shown on the stage screen, and each stage's `temps` (`[air, road]` per season and time-of-day slot in its `stages.ts`; DETAILS.md "Temperatures", figures in PHYSICS.md "Climate") are researched for it, at the stage start (higher up the car is colder, 6.5 K per km). A new stage needs a full table.
   Season look: `environment.groundTint` (the map's own season, `environment.season`; `groundTints` = the other two, same fields; a stage opens in another one with `StageDef.season`; `grass` + `amount`, `crop` = ripe crop colour, `moisture` = wet hollows / dry
   ridges strength, default 1); a `fields.palette` entry
   whose weights sum to < 1 leaves the rest as ripe crop (`[0, 0, 0, 0]` = wheat field, drives like grass). Match the
   detail grass cards to the ground: `spring_grass` (bright green), `dry_grass` (golden), `grass_tuft` (olive,
   untinted ground). Example: `ajvatovci` is spring (mostly green palette, a few ploughed / wheat parcels).
5. Verify as below. Map viewer "Picked point" shows lat/lon, cover class and Google Maps / Street View links -
   use it to match screenshots. Keep `maps/<id>/TODO.md` updated (missing assets, screenshots needed); a new map
   (even a planned one) gets a row in the "Map task lists" table of `src/games/rally/TASKS.md`.

Widening a real map (free-drive background, worked example `maps/ajvatovci/DETAILS.md` "Free-drive background"): grow the
config's `detail` / `outer` / `landcover` extents (keep their origins on the cell grid) and `bounds` in `map.ts`; bake to a
temp `out` dir holding a copy of the current `data.json` (stable building ids) and check before copying it in: identical
`route`, unchanged heights near the road, old building rows unchanged. A newer bake also carries building `kind`s - strip
them (`kinds: undefined`) to keep box buildings. Then run the water / side-road / junction tests: towns bring streets along
drain banks and small bridges that rural stages never had.

Buildings (real maps): the baker merges OSM + Microsoft ML footprints (`scripts/realmap/buildings.py`) into
`data.buildings` (oriented boxes, type house / flat, wall height, floors) + `<map>/buildings.csv`; `World` places
them as per-axis scaled instances of `house_pitched` / `building_flat` with `box` colliders and keeps scatter out.
They are referred to as `stage <stageNumber> - building <id> - lat, lon`; ids are stable across re-bakes
(matched by position). Map viewer: click a building or `?building=<id>`.

Junctions (rule for every real-world map): the world must not end at the stage road. Every other road / track
that meets it is joined to it (`world/junctions.ts` extends the baked side roads to the stage road edge) and its
mouth is closed like on a real rally stage - set the stage's `closures: { asset: 'road_barrier', length: 2.2,
setback: 4 }` in `map.ts`. The baker marks ways that only pass over / under the stage road (bridge, no shared
OSM node) with `junction: false` - those get a bridge TODO, not barriers. `tests/rally/junctions.test.ts` prints
the junction / barrier count per map and checks the barriers are off the road; look at a few in game
(`?spawn=<along>` from the test output) and note the count in the map DETAILS.md.

City maps (example `maps/jackie/`, config `scripts/realmap/jackie.json`) - extra baker options and engine features:

- `osm: { source: "overpass" }` (`scripts/realmap/overpass.py`): the plain OSM API refuses a city-sized box. Base query for the
  whole box, then buildings only within `buildings.corridor` m of the route (default 220: a wide map must not model
  every building). Needs `curl` (TLS). `paths: { corridor, highwayCorridor }` limit the other roads the same way.
- `dem: { source: "3dep", cell: 5 }`: USGS 3DEP lidar bare earth (US only, public domain) - no `canopy` to subtract.
- `route: { highways: true, offHighwayCost: 5 }`: the stage may follow motorway / parkway carriageways (one-way respected);
  the bake prints the OSM roads the route follows. The other carriageway, ramps and cross streets become `paths`
  with `bridge` / `layer` / `lanes` / `oneway` / `name`.
- Bridges: the baker writes `routeSpans` (route on `bridge=yes` / `layer<0`) -> `routeSpans(data.routeSpans)` in
  `RoadDef.spans`; the stage road is then a deck over lowered ground (street / rail beneath). OSM `bridge=yes` paths are
  elevated decks (lifted over what crosses them, piers, parapets; `bridgeStyle`: `stone` parkway look by default (arch soffit on street overpasses, on stage-road spans >= 12 m and their twin carriageway decks),
  `concrete` = modern overpass with an open railing - use it for anything that is not an old stone bridge; concrete decks
  keep parallel railings end to end unless the map sets `bridgeCorners: true`, and their wing walls splay outward - the
  ends open up, never close in) - see the rally DETAILS.md "City maps". Check with
  `tests/rally/bridges.test.ts` and the map viewer (`?map=<id>&along=<m>&zoom=0.5`).
- Buildings with `kind` (baker `classify_kind`: house, row, apartment, commercial, industrial, garage, church, tomb) are mesh
  buildings (`world/building-mesh.ts`: real outline, OSM `height`, facade textures in `engine/facade-textures.ts`).
- More city options (see the rally DETAILS.md "City maps"): `pathBarriers` (Jersey / guard rail along the opposite carriageway),
  `road.cutWalls` (sheer cuts with a stone retaining wall; `concreteFrom` = concrete + chain-link), `goreAreas` (hatched wedge between the road and a shallow ramp), `junctionPlazas` (outline of a big junction on a portal slab: one plain asphalt box, no crossing ribbons), `junctionAreas` +
  `plazaIslands` / `plazaCrosswalks` / `plazaSignals` / `plazaTrees` (the whole street space around a junction from open
  surface data: height field, islands, markings, furniture; worked example `maps/jackie/DETAILS.md` "Kew Gardens junction"), `parkwayLanes` (streets OSM draws beside the carriageways that really run down in the cut: treated as carriageways), `cityStreets` (city asphalt, kerbs, sidewalks, crosswalks, lamps),
  `streetDressing` (parked cars, crowds, police / ambulance / fire vehicles), `overheadSigns` (green "EXIT n" gantries from the
  ramps + hand-placed boards), `road.trenchFills` (pad the land where the lidar has a void beside a sunken stretch). Streets
  crossing over a tunnelled parkway (`under` spans) become bridge decks automatically (`world/under-bridges.ts`) and the span
  becomes a portal structure (`world/portals.ts`: slab, headwalls with name / clearance plates, railings, median piers; the
  street grid on top is padded to the slab top). Overpass decks and junction plazas are drivable in free roam. Bridges / underpasses: see "Bridges and underpasses (city maps)" below.
- Looking at a map in the preview pane (it renders one frame every few seconds): `window.__mapViewer.look(cx, cy, cz, lx, ly, lz, fov)`
  parks the camera and streams all terrain + instances around it; wait ~10-30 s, then screenshot. Helpers to build camera
  positions along the road: `world.road.at(d)` (x, y, z, tx, tz), lateral `x + tz * l, z - tx * l`.
- Power lines: `MapDef.pylons` / `powerLines` (baked from OSM, `data.pylons` / `data.powerLines`) become `power_pylon` / `power_pole` instances + cables
  (`world/power-lines.ts`). Scatter option `channelDist: [min, max]` = only within that distance of a canal / drain edge (willows, reeds).
- Railways: `MapDef.railways` = `data.railways` (baker `railway_lines`: OSM `railway=rail`, electrified flag). Tracks become
  `rail` paths (300 m smoothing, 2.5 % grade limit, never eased to a road - a road crossing at grade meets the rail level;
  drivable ballast hump carved, decks over them lifted by `RAIL_CLEARANCE`, placeholder buildings on the bed dropped), drawn
  by `world/rail-mesh.ts`, masts every ~58 m on the electrified ones. To add them to an already baked map: bake to a temp `out`, copy only `railways` into its data.json (as
  for lakes). Check `tests/rally/railways.test.ts` and look under the road bridges in the map viewer. Stations and
  platforms are landmarks (example `maps/ajvatovci/station/`: platforms placed from the baked tracks in `site.ts`).
- Road texture `road_parkway` (lane lines), structures `jersey_barrier` / `guard_rail` / `concrete_block`, roadside rule
  options `onBridge` / `skipJunctions`, `terrain.rockSlope` (grassed cut slopes instead of bare rock).
- Browser checks: the preview pane throttles rendering hard; stream terrain by hand from the console
  (`__rally.terrain.update(pos, 300)` in a loop, `__rally.streamer.updateNow(pos)`) and park the camera with
  `__rally.rig.update = () => {}` + `__rally.camera.position.set(...)`.
- README shots in game (`?stage=<id>&car=<car>&spawn=<along>&mute=1`, no HUD): step the game by hand (`__rally.frame(1 / 60)` x 90,
  what `benchmark` uses) and read `__rally.renderer.domElement` in the same task - `renderer.render` outside the loop draws
  sky only (the frame sets up the camera-relative scene). A hidden pane stalls loading: `tabs_select` the tab first.

Gotchas: +Z is SOUTH (the baker handles it); uneven control-point spacing makes Catmull-Rom loop (the baker evens
it out, `world.test.ts` "no loops or kinks" catches it); the elevation is a surface model (trees / roofs) - tune
`canopy` if roads climb walls of forest.

## Bridges and underpasses (city maps)

Owner rules - a review fails on any of these:

- Approved bridge tops are never touched; bridge walls run parallel unless the bridge curves; always check the bridge START and END.
- Retaining walls are concrete, straight, continuous (also at OSM way joints), never on a road / shoulder, never through the deck above,
  never higher than the parkway beside them; no fence on underpass / approach walls; no tunnels in underpasses.
- The street under a bridge is flat and unbroken (no ground through it); sidewalks continue under bridges; lamps under a deck go on the
  wall (`wall_lamp`), never a pole; nothing scattered in a trench; no barrier / wall / sign post on another road; streets never overlap
  a carriageway.
- Fences / railings never cross a road: a rim fence keeps a street off the drop to the parkway, it never stands on a street, plaza or
  bridge deck, and never bridges a gap (one railing per run of fenced wall rows, `cut-wall-mesh.ts`). Where OSM puts a street's lane on
  the wall line, move the street off the cut (`MOVED_NODES` in `maps/jackie/map.ts`); a junction plaza stays between the headwalls.
  Check every new wall / plaza / street change at the bridge start and end for a railing across the road.

Where it lives: path pipeline in `TerrainGen` (`world/under-bridges.ts`: `separateStreets`, `alignParallelDecks`, ...), trench and deck
terrain in `terrain-gen.ts` (`dipUnderBridges`, `pathCutWeight`, `capUnderDecks`), walls in `cut-wall-mesh.ts`, span fitting in
`maps/shared/real-map.ts`. `World.analytic` is the TOP surface (includes the stage deck): anything on a street samples the ground
(`GroundTerrain` / `gen.height`). No terrain through streets: a street ribbon holds its own height line where the land under it
falls away (cut beside it, trench under a portal slab; not on / under the stage road, `pathMeshesJob`), the ground under a deck
end is not pitted inside a junction plaza (`capUnderDecks`), a sidewalk is lifted clear of a bank, and decks on a portal slab
carry sidewalks (`street-detail.ts` `deck`). Motorway / trunk ways are carriageways, never dipped - except a not-connected one
crossing beneath a stage-road span on a country map (`TerrainGen.highwayUnder`, worked example `maps/petralica/`, E-871).

Approaches (`TerrainGen.raiseApproaches`): the ways a street deck continues into climb to the deck end at `DECK_GRADE`, relative to
their own land line (a hillside street keeps following the hill), smoothed over 24 m; motorway / trunk and portal decks are left
out. Two raised approach streets within 10 m share one fill (no notch in the gore). A road that only passes beside a deck end (no
node there) is never anchored to it (`meetsEnd`).

Most bugs come from **OSM way joints**: one street is several ways, and every per-way step (2 m sampling, square ends, a profile
smoothed alone, "another road here" checks) breaks at the joint - sample to the exact end, mitre to the mean direction, treat the next way
of the same street as itself.

Fixing one: open the owner's camera link in your own preview (`__mapViewer.look(...)`), hide scene groups (`terrain`, `road` children
`bridges` / `cut-walls` / `paths` / `street-detail` / `barriers`) + `shell.renderer.render(...)` to name the culprit mesh, probe heights in
the page (`gen.height` vs `world.analytic.height`, `pathHeight`, path ends near the point - indices shift, find ways by position), fix the
rule (never a per-bridge offset), re-check start / end and the other underpasses, run `city-maps` / `bridges` / `side-roads` tests.

## Landmarks (hand-modelled streets / lots) and pads

When a stretch of a real map needs more than placeholder boxes (the Ilinden street at the start of `ajvatovci`):
make a landmark folder `maps/<id>/<name>/` (worked example `maps/ajvatovci/start-row/`, read its DETAILS.md first) with a pure
layout (`layout.ts`, node-testable), a `Landmark` (`index.ts`: `replaces` = placeholder buildings to hide, `occupies` =
keep scatter out, `colliders`, `instances` = rally assets as fixed scatter, `build` = geometry job), register it in
`world/landmarks.ts` and list its id in `MapDef.landmarks`. Geometry: `build/kit.ts` (soups per tile + material with the paint
in vertex colours, metre UVs, `Frame` = site -> world + shear onto a lot's plane), `build/wall.ts` (walls with real
window / door openings), materials in `build/materials.ts`, textures `engine/lot-textures.ts`. Level the ground with
`terrain.pads` (polygon + frontage knots `x, z, ...` on the stage road; the pad is level across the street and follows
the road height along it). Place lots from a satellite screenshot: trace pixels with a px -> site transform fitted to the
road (`start-row/trace.ts`), share one fence between neighbouring lots (`layout.ts` `sharedFences`), and make fences /
poles colliders and kerbs `groundOverride` ground so the car feels them (`start-row/index.ts`, `streetwork.ts`).
Parked vehicles are instanced (`build/vehicles.ts`): keep a car < ~500 triangles. Check: `tests/rally/start-row.test.ts` style
tests + the stage test (colliders must stay off the road), look at it in `/games/rally/?stage=<id>&spawn=<along>`.
Single buildings away from the stage road (example `maps/ajvatovci/hilltop/`: church, bell tower, court): positions from
OSM ways reprojected with the baker's `Proj`, one `Local` frame per structure (`hilltop/build/shapes.ts`: the kit's
`Frame` with its own `origin`, walls with real openings, tiled roof planes), ground levelled with named `flatAreas`
(pads need a stage-road frontage) - keep their blend rim off the road (`tests/rally/hilltop.test.ts`).

## New map checklist

Copy `maps/test/` to `maps/<id>/` (fill in its `DETAILS.md` sources), change `id`, `name`, `seed`, `bounds`, `road.points` and
its `stages` (one or more `StageDef`: id, name, tyre, `timing`, `reverse` for a stage driven the other way along the road,
`closures`, `cornerFans`); add to `ENTRIES` in `maps/index.ts` (a real map with baked data: put the menu fields + `stages.ts` in
`<id>/info.ts`, load `map.ts` with a dynamic import, see rally DETAILS.md "Lazy loading"); the stage test picks every stage up
automatically. Several stages on one road: measure each stage end's distance along the road in node (bake `meta.waypointsAlong`
is along the baked polyline, the game road differs by metres) and hard-code `timing`. **Add every stage to `STAGES_LIST` with
`hideInProd: true`** in `src/games/rally/release.ts` (`tests/rally/release.test.ts` fails for an unlisted stage): it is then
dev server only (TEST badge) and out of the published build. Remove the flag to release it (or set it again to pull it).

## Source files

Files / links the user provides (models, reference photos, data downloads) go to `sources/` (git-ignored) and are
listed in the car / map folder `DETAILS.md` - follow `.claude/skills/source-files/SKILL.md`.

## Bump the times version (last step)

A new stage adds its id to `STAGE_TIMES_VERSIONS` in `game/stage.ts` (start at 1). Changing a released stage's road, layout, length or surfaces bumps its entry (a map's road change bumps every stage on it), but only when the user says we are making a build;
until then say in the PR which stage changed (AGENTS.md "Rally times versions"). A `hideInProd` stage stays at 1 until released (a test checks). Old times stay below the new ones.
