---
name: gpx-route-repair
description: Repair off-road shortcuts, straight lines through hills, missed bends, and incorrect turnarounds in GPX or Strava routes using OpenStreetMap, public rides or segments, and imagery. Deliver an importable planning GPX, or estimate ascent with tunnel elevation artifacts corrected. Use for route planning, not activity synchronization or uploading rides.
---

# GPX Route Repair and Tunnel-Corrected Ascent

Perform route repair, ascent estimation, or both as requested. An ascent-only request does not authorize changing the route. When the user asks for a GPX, deliver the file without requiring an online editor import first.

## Repair route geometry

- Preserve the source file. Inspect track segments, distance, endpoints, missing elevations, long straight sections, and repeated turnarounds. Evenly spaced interpolated points do not establish that a line follows a road; maximum point spacing alone will miss a shortcut through a hill.
- Compare the route with road geometry to locate suspect sections. Map matching may return a primary result, alternate or disconnected fragments, and unmatched points. Check coverage and original point indices across all fragments; the first matched fragment is not necessarily the full route.
- Find evidence that supports the intended alignment: connected OSM roads, public Strava segments or rides, and visible imagery. A missing OSM road does not prove there is no road; a successful match does not establish current access. Use normally visible data or data the user is authorized to access.
- For reference rides, check point order, direction, connections, whether the rider used a different descent or detour, the ride date, and bicycle type. An uphill segment alone cannot establish the downhill exit. Exclude unrelated sections and personal data from the delivered file.
- Trace missing geometry where imagery shows a clear, continuous road, and record the evidence and uncertainty. Do not invent a rideable road across an obscured connection, footpath, staircase, or closed area. Keep and identify unresolved sections when evidence is insufficient. Explain the tradeoff if a repair would substantially change intended waypoints or the nature of the route.
- Join supported repairs back into the original route. Preserve hairpins during simplification and add points where needed. Check connections, jumps, and reversed point order before comparing distances. After changing geometry, do not reuse old elevations by point index; explain elevation datum offsets, interpolation, and unknown values.
- Export a planning GPX 1.1 with explicit track and segment structure and the intended endpoints. Usually include coordinates and available elevation only; do not copy timestamps, heart rate, power, or identities from reference activities. Reparse the output and check continuity, joins, distance, point count, and elevation. Validate against an XSD when available. Distinguish format validation from an actual successful import into a platform.

When either a GPX or a Strava edit is acceptable, a local GPX can satisfy the request. Overwrite an online route only within the user's authorization and retain the original. Exporting a file does not authorize creating an activity, publishing a route, or changing privacy settings. If repaired roads are missing from OSM, automatic rerouting in an editor can lose the repairs; recommend manual drawing mode when relevant.

## Estimate tunnel-corrected ascent

Read [references/tunnel-elevation.md](references/tunnel-elevation.md) before calculating. By default, remove false hills caused by terrain elevations above a tunnel while retaining the tunnel's real uphill gradient. Do not force every ascent inside a tunnel to zero.

Recalculate from the final delivered GPX. A Python standard-library helper is included; resolve its path relative to this skill's folder:

```bash
python3 scripts/gpx_ascent.py /absolute/path/route.gpx
python3 scripts/gpx_ascent.py /absolute/path/route.gpx --tunnels /absolute/path/tunnels.json --threshold-m 3
```

The helper reports both the sum of positive elevation differences and a threshold-filtered result, calculated separately for each GPX segment. It makes no network requests and does not modify the GPX. Review tunnel intervals and portal elevations first; the reference defines the JSON input. The helper cannot establish road access or verify portal evidence.

## Deliver results

Lead with the requested GPX or ascent estimate. For repairs, briefly describe the changed sections, before/after distance, and unresolved sections. For ascent, identify the route used, correction method, tunnel coverage, and elevation limitations. Round to match data quality rather than implying meter-level accuracy. Keep a file-only delivery concise; provide comparison maps and detailed notes when useful or requested.
