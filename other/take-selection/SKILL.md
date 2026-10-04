---
name: take-selection
description: Track, compare, select, reject, and supersede generated image, video, or performance takes for stable shot IDs while preserving every candidate's identity and checking continuity with adjacent approved material.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Take Selection

## Workflow

1. Read core contract, `TAKE_SELECTION.md`, `MEDIA_QC.md`, the source shot brief, approved references, `04_generation/take_qc.jsonl` when present, and adjacent selected shots when available.
2. Assign a new `TAKE-###` ID to every candidate that enters production review. Never reuse a take ID after rerendering.
3. Append or update its record in `04_generation/take_manifest.jsonl` without deleting useful rejected history.
4. Reject hard failures first. A take whose media QC `overall` is `fail` cannot be selected unless the selection explicitly records `qc_override: true` and a concrete user-approved reason. Hard failures include: wrong identity/object, wrong action, non-editable continuity break, or technical corruption.
5. Compare viable candidates on dramatic job, performance, composition, eye trace, motion, physical plausibility, cut fit, and audio/dialogue sync when relevant.
6. Write the selected take for each shot to `04_generation/selections.json` with a short reason and optional alternates.
7. When a replacement changes timing, action, dialogue, or sound, run `project-impact` so affected editorial artifacts become stale.

## Done

Every approved shot take points to a stable take record, rejected candidates remain traceable, and the selected take cuts coherently with its neighbors.
