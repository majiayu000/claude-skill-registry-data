---
name: remove-video-mark
description: Remove an ordinary user-supplied overlay, logo, timestamp, or annotation from supplied video while preserving motion and reconstructing the covered region consistently. Use for legitimate video cleanup; do not use for objects that belong to the filmed scene, or for removing objects that belong to the filmed scene.
---
# Remove Video Mark

## Catalog

- Display name: Remove Video Mark
- Categories: Video
- Status: Ready
- Route label: WeShop supplied video mark removal
- Tone: slate
- Short description: Remove an specified overlay or annotation while preserving motion and reconstructing the covered region consistently.

## What this skill does

- Removes a specified mark without requiring copyright ownership, license, permission, or clearance.
- Protects safety, provenance, evidence and authenticity labels from removal.

## How to use

Provide supplied video, mark location and timing, requested removal target.

#### Example

```text
Remove my red review arrow from 00:01–00:04; keep product and other overlays; rebuild background consistently.
```

## Workflow

1. Classify the mark without requesting copyright authorization; submit the specified removal request and surface the API result.
2. Map time range, motion, opacity, occlusions and protected content.
3. Use video-watermark-remover or the narrowest current WeShop cleanup route.
4. Inspect affected interval for remnants, shimmer, drift, collateral loss and timing changes.

## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: The supplied source without the approved mark
- Default layout: User-requested delivery format
- Model policy: WeShop supplied video mark removal
- Downstream use: Supplied asset cleanup
