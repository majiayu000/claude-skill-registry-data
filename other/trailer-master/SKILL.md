---
name: trailer-master
description: Render, QC, approve, and package each trailer, teaser, or vertical trailer using the common executable timeline, audio mastering, media registry, and delivery-QC systems.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Trailer Master

## Workflow

1. Read the `TRL-###` trailer plan, timeline, audio mix, subtitles, and delivery target.
2. Render its audio mix with `audio-master`.
3. Render the trailer timeline with `scripts/render_timeline.py`.
4. Run `delivery-qc` against duration, aspect, resolution, streams, and codec constraints.
5. Register and approve the final trailer through `asset-approval`.
6. Run `scripts/promo_delivery.py PROJECT --scope trailers --reconcile` after the requested trailer set is rendered.
7. Preserve the trailer timeline, mix, QC report, and checksum with the master.

## Done

Each requested trailer exists as an actual verified media file, not only an edit plan.
