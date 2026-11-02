---
name: map-creator
description: Draw and animate maps locally with Natural Earth and D3. Use for geographic explainers, highlighted countries, routes and map footage for videos.
priority: P1
category: media
status: builtin-guidance
---

# Map Creator

Create an actual map file or animated map scene from attributed geometry and source data. Natural Earth and D3 cover many country-level explainers; choose an appropriate projection and fetch more detailed authorized data only when needed.

## Device and permission gates

Use an authorized local computer and workspace. Preparing ordinary D3 packages and public geometry is part of the requested map task: disclose source, size and destination, then continue within existing permissions. Rendering and private input data stay on the user's device. Do not invent administrative detail or imply that an illustrative map is a legal boundary or navigation product.

## Execute and verify

Materialize this package's hashed scripts/local-media.mjs using prepare_skill or chunked read_skill resource reads.

    node "<skill>/scripts/local-media.mjs" map --workspace "<workspace>" --output "<new map>.svg" --highlight NZL,CHN

The helper prepares pinned D3 packages, downloads country geometry, records its source revision/hash and produces a real SVG with an artifact receipt. For motion, copy local geometry into a Remotion, HyperFrames or OpenFilm project and animate projected geometry, labels or routes from the frame/seek time. Do not depend on a live tile CDN during rendering.

Verify labels, route endpoints, projection clipping, color legend and highlighted country identifiers. Inspect the saved image or video and keep its source attribution. Deliver the file and reusable geometry/project when useful.
