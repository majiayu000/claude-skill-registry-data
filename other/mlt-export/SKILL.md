---
name: mlt-export
description: Export the executable timeline as portable MLT XML for generic MLT interchange while keeping the FFmpeg-rendered film master as the standalone delivery path.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# MLT Export

## Workflow

1. Read `../../references/MLT_EXPORT.md` and `../../references/EXECUTABLE_TIMELINE.md`.
2. Validate the source timeline first.
3. Run `scripts/mlt_export.py PROJECT --timeline PATH --output RELATIVE_PATH`.
4. Parse the resulting XML and verify that every timeline event is represented in order.
5. If the user specifically requests Kdenlive or Shotcut, route to `editor-project-export` instead of labeling this generic file as native.
6. Do not add untested editor-private effects or UI metadata.

## Done

A structurally valid MLT XML timeline exists with project-relative media resources and matching event durations.
