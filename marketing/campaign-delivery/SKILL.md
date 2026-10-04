---
name: campaign-delivery
description: Render and verify the planned social campaign deliverables across aspect ratios and durations, then reconcile masters, copy, artwork, captions, subtitles, and QC into a complete campaign delivery set.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Campaign Delivery

## Workflow

1. Read social campaign, deliverables, copy, calendar, approved social media, and delivery specifications.
2. For each `SOC-###`, ensure required picture/audio/copy/art dependencies are approved.
3. Render video timelines and audio mixes when needed.
4. Apply deterministic reframes only where declared.
5. Run delivery QC on every final media file.
6. Register approved campaign masters in the media registry.
7. Run `scripts/promo_delivery.py PROJECT --scope social --reconcile` to prove media, approval, copy, and QC readiness.
8. Mark each deliverable `ready` only when all required pieces exist and QC passes.
9. Preserve optional omitted deliverables as explicit decisions rather than silent gaps.

## Done

Every required campaign deliverable has its media, copy, metadata, and QC state reconciled.
