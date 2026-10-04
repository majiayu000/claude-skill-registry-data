---
name: social-cutdown
description: Build short social-video edits from approved film, trailer, and pickup media using stable source IDs, destination-specific timing, hooks, subtitles, title cards, and executable timelines.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Social Cutdown

## Workflow

1. Read the campaign and one `SOC-###` video deliverable.
2. Select approved film/trailer source media or approved social pickups.
3. Build an executable timeline under `06_release/social/SOC-###/timeline.json`.
4. Build the matching audio mix when the deliverable has sound.
5. Make the opening understandable at the destination duration without requiring hidden context.
6. Preserve spoiler policy and source traceability.
7. Use `social-reframe` when destination aspect differs from source composition.

## Done

The social video has a complete executable edit that meets its declared duration and content job.
