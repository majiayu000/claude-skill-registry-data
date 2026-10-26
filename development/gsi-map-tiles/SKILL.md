---
name: gsi-map-tiles
description: Use when building 3D worlds, games or visualisations from Japanese open map data — GSI (Geospatial Information Authority of Japan) elevation PNG tiles, vector tiles for buildings, roads, railways and water, aerial photo tiles, and PLATEAU 3D city models; covers tile math, decoding, runtime fetching with caching and fallback, attribution, and procedural generation on top. Also use when terrain has holes or steps, roads break at bridges, water looks wrong, or buildings from the data are plain boxes.
---

# Japanese open map data (GSI tiles, PLATEAU)

Default: fetch tiles at runtime (or preprocess offline for large areas), cache them locally, show attribution on screen, fall back to generated terrain when data is unavailable, and treat the data as a skeleton that procedural generation fills in.

## Tile math

- XYZ tiles in Web Mercator: `n = 2^z`, `x = floor((lon + 180) / 360 * n)`, `y = floor((1 - asinh(tan(lat)) / π) / 2 * n)`.
- Metres per pixel shrink with `cos(latitude)`; compute scale at your origin and keep the world near (0,0,0) to avoid float precision problems far from the origin.

## Elevation PNG

- Elevation PNG tiles encode height in RGB: `x = R·2^16 + G·2^8 + B`; if `x < 2^23` then `h = x · 0.01 m`; if `x > 2^23` then `h = (x − 2^24) · 0.01 m`; `x == 2^23` means **no data** (sea or missing). Check the official specification for the exact rule and available zoom levels.
- Fill no-data cells deliberately (sea level for the sea, interpolation for small gaps), or terrain gets holes and spikes.
- The GSI tile servers support CORS, so browser builds can fetch tiles directly.

## Vector tiles

- Mapbox Vector Tile (protobuf) format; a small decoder is feasible but test it against reference output.
- Layers include buildings, roads (with attributes such as width class and **bridge/elevated flags**), railways and water areas. Read the layer documentation; ignoring the bridge attribute makes roads stop at every river and elevated expressways disappear.
- Footpaths and trails are separate classes; include them if people walk in your world.

## Water

- Height data over water is unreliable (moats and ponds may be interpolated from their banks). Decide water level from the polygon's surroundings ("lower than the banks, nearly flat"), carve terrain under water polygons, and keep the shore well above the water surface.
- Coarse terrain grids make stepped shorelines; refine the grid only in cells crossing the shoreline.

## Buildings

- Footprints come with few attributes. Classify each building (detached house, apartment, office, shop, warehouse...) from footprint size, shape, height and surroundings, then generate facades from parts: windows per wall length, an entrance facing the road, roofs by type.
- PLATEAU provides textured LOD2 models in many cities, but coverage varies: many "LOD2" tiles are mostly LOD1 boxes. Use LOD2 only where it really exists and generate the rest.
- Aerial-photo textures from oblique imagery can show neighbouring roofs on occluded walls; check walls individually, not just from above.

## Attribution and terms

Display the source (e.g. "GSI tiles" / "PLATEAU") on screen as the terms require; read the current terms of use for each dataset.

## Verification loop

1. Unit-test decoding with known tiles (a known summit height, a no-data sea tile).
2. Render a top-down debug view: roads continuous across rivers, no water under buildings, no holes.
3. Walk and fly test routes; measure frame time in dense areas.

## Pitfalls

- **Request volume:** cache aggressively and limit concurrency; do not hammer public tile servers.
- **Seams between tiles** need shared edge vertices or skirts.
- **Coordinate systems:** PLATEAU uses its own reference systems in some products; convert carefully and verify with a known landmark.
- **Huge single meshes** of a whole city cannot be culled; chunk them.
