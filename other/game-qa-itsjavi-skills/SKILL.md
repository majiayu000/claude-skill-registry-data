---
name: game-qa
description:
  "For GameGen projects, verify game behavior and visual quality through isolated tests, actual Godot playthroughs and
  reference comparisons, with clear evidence and verification limits."
---

# Verify a game or asset integration

Read [shared context](../../references/shared-context.md), project preferences and the task's actual changed files. Use
the scope and selected review policy to choose checks. For read-only reviews, report missing preferences without making
unrelated changes.

## Separate the evidence

- Structural checks: files, imports, paths, resource metadata, sprite layout, rig/clip presence and asset hashes.
- Functional checks: actual gameplay state, input, collisions, action/recovery behavior, progression and save/load.
- Visual checks: real renderer output, continuous animation and comparison with the approved references at matched
  camera and size.
- Performance checks: real-time profiling at the target workload, performed through game-optimization.

A passing structural test cannot establish attractive anatomy or fluid animation. Apply the shared verification rules to
headless, fixed-fps and desktop evidence.

## Test the meaningful paths

Import the final asset, not a fixture or earlier revision. Record the asset/source hashes that were actually tested.
Read errors from the current run separately from historical editor logs.

Exercise the complete scoped loop and its failure/recovery path. Check continuous traversal across boundaries, repeated
actions, pause/resume, focus loss, and the configured input methods. Test actual global overlays and mobile controls
together. Save/load checks must assert meaningful restored state.

For animation, check visible vertex/frame changes, limb contacts, transitions and action-event timing. For
tiles/sprites, check native scale, alpha edges, atlas layout, pivots, seams and direction changes. For 3D, compare
silhouette, face, materials and ground contact from front, side and gameplay views.

Capture actual engine stills and short motion footage with enough context to review the result. Identify whether footage
shows real movement or an in-place animation demo. Use meaningful assertions on observable behavior rather than tests
that reproduce implementation statements.

## Handoff

Record what ran, where, against which revision, and what passed or failed. Keep untested physical devices, export
stages, facial features or content explicit when relevant. Run further checks only when new changes, failures or
unresolved concerns warrant them. Final evidence belongs in the configured artifacts directory and existing task record.
