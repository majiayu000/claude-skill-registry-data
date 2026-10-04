---
name: timeline-assembly
description: Compile approved picture and postproduction decisions into a portable executable hard-cut timeline that can be deterministically rendered without a nonlinear-editor project.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Timeline Assembly

## Workflow

1. Read `../../references/EXECUTABLE_TIMELINE.md`, edit plan, editorial manifest, media approvals, finished picture, and audio-master path.
2. Write `05_post/timeline.json` for the main film or the equivalent timeline under a trailer/social deliverable directory.
3. Use event order as playback order.
4. Give every event an `EVT-###` ID, positive duration, source identity, and project-relative source path when required.
5. Resolve all placeholders and missing required media before final rendering.
6. Validate with `scripts/render_timeline.py PROJECT --timeline PATH --validate-only`.
7. Render only when the user requested actual output or the owning playbook requires a finished master.

## Weak-model rule

Do not invent transitions or timing to hide missing media. Hard cuts are the safe portable default.

## Done

The timeline can be reconstructed without chat history and contains no unresolved required picture event.
