---
name: data-globe
description: "Turn large location datasets into interactive 3D globe web pages with weighted points, city aggregation, free map tiles, hover previews, filters, a date brush, fly-to entity drilldown, cached logo sprites and shareable views. Use for geographic exploration of CSV or JSON rows with coordinates or city/country."
metadata:
  author: Edge (Federico De Ponte)
  creator: Edge (Federico De Ponte)
  display_name: Data Globe
  license: Apache-2.0
---

# Data Globe

Edge turns location rows into a world you can explore: see where activity concentrates, filter it, then select a point to meet the entities behind it. Use the included starter as a working base; adapt its labels to the user's dataset while keeping the included visual system: warm light-land globe on a night ocean, ember point glow, atmosphere rim, translucent rails, location rankings and entity wall. The optional dark-land button changes contrast without changing the data.

Explore [Rocketmap](https://rocketlist.ai/map), the live production reference, and read [references/rocketmap.md](references/rocketmap.md) for its relationship to this reusable starter.

## Fit the user's setup first

- **Stack:** if the user names a stack or library (globe.gl, react-globe.gl, raw three.js, Next.js, a single HTML file, offline kiosk), build in that stack and apply the data, interaction and performance rules below to it. The MapLibre starter is the default only when they name none.
- **No tools or file access:** if you cannot run the scripts, deliver the complete, runnable code in the reply (one file where the stack allows) with the user's data cleaned inline, and say plainly that it has not been run. Never claim to have rendered, tested, fetched or deployed anything you did not.
- **Pasted data:** start the reply with a short data audit of the rows they gave: rows in, entities after merging, places, total weight, and every fix you made (swapped coordinates, merged duplicates, assumed cities, zero-weight rows kept), each as one line the user can override.
- Keep the code compact and re-read it for runtime errors before replying: undefined returns, missing imports, client-only code in server components, textures and listeners never disposed.

## Start from data, keep the geography honest

Inspect column names, row count, coordinate coverage, categories, weight distribution and date meaning. Record the source URL, licence, download date and exclusion rules. Preserve source entity IDs. Default weight is **one entity** when no meaningful metric exists; do not present invented activity or population. A modification date is not a founding/opening/event date.

The canonical row is `id, name, lat, lng, weight, category, country, city, date`, with optional `domain, logo, url`. Coordinates are `[longitude, latitude]`; country is ISO2; dates are ISO `YYYY-MM-DD`. Accept finite coordinates in range and nonnegative finite weights. Deduplicate by source ID when the rows have one. Without IDs, normalize names (case, punctuation, suffixes such as Inc, Ltd, GmbH, AI) and merge rows that match on normalized name plus domain or city; count each entity once and list every merge so the user can undo it. Check coordinates against the row's country: a point that lands in the wrong country with lat and lng swapped is a swap, fix it and say so. Invalid or unplaced rows go into the audit with their reason. Valid `(0,0)` may be real: check the dataset rather than banning it universally.

For city/country rows, read [references/geocoding.md](references/geocoding.md). Resolve offline against GeoNames with exact aliases, ISO2 and admin constraints. Never pick the biggest city from ambiguous matches, ignore a state suffix, or invent a country-centroid city. Keep unresolved rows explicit. When the rows or the user give a clear signal (a country or state column, the rest of the dataset's region, the company's known HQ), place an ambiguous city with a one-line reviewable assumption instead of dropping it; leave it unplaced only when there is no signal. For authoritative city anchors use `--group city`; coordinate inputs use `point` or `grid`.

## Working starter (Python 3 + a browser; no build system)

Locate this skill folder as `SKILL`, then run:

```bash
python3 "$SKILL/scripts/bootstrap.py" ./app
python3 "$SKILL/scripts/prepare.py" input.csv ./app/data.json \
  --mapping '{"id":"id","name":"name","lat":"latitude","lng":"longitude","category":"category","weight":"weight","date":"date","country":"country","city":"city"}' \
  --title 'My location explorer' --source 'Dataset source / attribution' --group point
python3 -m http.server --bind 127.0.0.1 --directory ./app 0
```

`bootstrap.py` refuses to overwrite a nonempty output and downloads pinned MapLibre GL JS 5.24.0 JS/CSS/licence into `vendor/`. Copy/adapt the template for an existing app instead. `prepare.py` takes CSV or a JSON array, maps fields, validates and writes `data.json` plus `data.audit.json`. Missing weight/category/date columns become 1/Other/undated. Use `--where '{"input_column":["allowed","values"]}'` for explicit source exclusions. Use `--geonames cities1000.txt` for name-only locations. Do not change audit counts to hide inconvenient rows.

For tens of thousands of exact-coordinate entities, use `--group grid --cell 2` initially, then tune cell size for density. Spatial bins use the spherical mean of included coordinates (including across the antimeridian), are labelled “Spatial cell · nearby locations”, and expose actual entity coordinates in the data. They are not city geocodes. City aggregation uses one verified city anchor; never turn logo arrangement offsets into street addresses. Keep original entities for drilldown, and aggregate counts and summed weights after **all** active filters.

Serve over HTTP, not `file://`. Choose a free localhost port, keep the server supervised, and stop it when verification ends. Output remains a normal static web page; deploy only when requested.

## Interaction contract

- MapLibre's real **globe** projection, free keyless OpenFreeMap vector tiles, visible provider/OSM attribution. Use `map-style.js` as provided: world vector geometry stops at zoom 6 and separate street geometry starts at zoom 7. Fly to exact entities/city anchors at zoom 10.4 for detailed roads and labels; spatial bins use a wider overview, then selecting an entity flies to its original coordinates. Never stretch coarse world water into a city view. The starter deliberately specifies the map container size with a selector stronger than MapLibre's default CSS; keep it full viewport.
- Idle rotation starts after the map loads. Drag, touch, wheel, click, keyboard interaction, filters and time input stop it for the mounted session. Hover alone should not take control. Clamp frame deltas, respect reduced motion, pause in hidden tabs, cancel animation frames on teardown.
- Weighted points and a generous hit layer: keep zero-weight entities discoverable. Hover shows location, current count/weight and a bounded logo preview. Use text nodes for data, and permit only HTTP(S) entity links.
- Category/search filters recompute points, totals and drilldown together. A zero-result view stays usable. Date controls are hidden when the dataset has no dates. A brush uses inclusive bounds and discloses what the source date means and what happens to undated rows. Do not synthesize dates just to expose the brush.
- Select a point → stop rotation → fly to its actual aggregate anchor → show its matching entities in a detail panel. Keep the selected entity set consistent when filters change. Select a list row, search result, overview logo or grouped marker to open the individual entity with original coordinates and a safe source link. Grouped logo rings are visual arrangements around an anchor, never invented addresses; many entities in one city must stay individually selectable (ring, list or zoom-dependent clustering), never stacked on one pixel. Back returns to the group; Escape and close remain reachable. Page/virtualize long lists; the starter renders 80 rows at a time.
- Share `category,q,from,to,point,entity` and camera `lng,lat,zoom,pitch,bearing` in the URL. Restore on a fresh load, including the detail panel. Validate numeric values, update after camera settling, and provide Copy link. Reset clears filters/selection and returns to the globe without restarting idle spin.
- Mobile uses a scrollable bottom sheet, reachable close control, touch input and bounded lists. Check a narrow viewport and ensure panel content does not cover the whole globe.

## Logos and performance

Use a local cached sprite, not one network request per entity or per animation frame. Hotlinked third-party logos and logo APIs often fail (CORS, retired services, keys that must not ship in browser code); keep a monogram fallback for every entity and never put an API key in client code. Do not scrape sites whose terms forbid it (for example LinkedIn); say so and offer the official or manual route. `scripts/pack_logos.py data.json logo-manifest.json` takes `{entity_id: local_image_path}` (Pillow required), makes `logos.webp`, sets row sprite indices and adds sprite metadata. `logo` and `domain` fields are hints: acquire only appropriate public assets, with explicit caching, bounded retries/timeouts and an allowlisted source if fetching server-side. No logo is required to explore the dataset; missing/low-resolution images use a monogram. The starter never automatically fetches domain favicons.

For three.js-based globes, fly along the shortest great-circle arc (handle the antimeridian) and keep the camera up vector stable near the poles. Use WebGL layers for data points, not thousands of DOM markers. Aggregate on data/filter changes, never every frame. Debounce text search. Limit hover logos and list DOM nodes. Freeze one JSON snapshot for modest datasets; for hundreds of thousands/millions of rows, move normalization and indexing off the UI thread, separate aggregate metadata from per-location detail files, lazy-load detail and cancel stale fetches. Preserve spatial labels when changing levels of detail. Avoid changing the map source every rotation frame. Dispose listeners, timers, frames and maps on unmount in framework integrations.

## Verify the result

Use a real browser, preferably Playwright with WebGL enabled. Check source row/audit totals, loaded entity count, globe projection, full canvas size, actual rendered point features, map drag, idle rotation and permanent stop after input, hover, one meaningful filter, actual point click and drilldown names, share URL restoration, zero-result reset and a mobile sheet. If dates/logos exist, check those too. Inspect desktop and mobile screenshots of the overview, fly-in and detail panel. Keep the rails legible and leave enough map visible; do not strip the visual system into bare dots and a form. Record uncaught exceptions, console errors, failed requests and map errors; separate nonblocking optional misses from failures that prevent the promised experience. Do not call an unrendered canvas or a fabricated marker a passing globe.

Sources: [MapLibre globe example](https://maplibre.org/maplibre-gl-js/docs/examples/display-a-globe/), [OpenFreeMap quick start](https://openfreemap.org/quick_start/), [GeoNames downloads and attribution](https://download.geonames.org/export/dump/).
