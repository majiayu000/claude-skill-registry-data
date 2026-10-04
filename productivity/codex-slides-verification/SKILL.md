---
name: codex-slides-verification
description: Verify that Codex Slides changes are durably reflected in project state and visibly reflected in the exact Codex Browser slide, panel, version, checkpoint, or presentation surface. Use after creation, rendering, editing, restyling, mark edits, speaker-note changes, version restores, or export.
---

# Codex Slides Verification

Use two signals before reporting a presentation task complete:

1. Read canonical project state with `get_project`, and read a named durable job
   with `get_project_run` or `wait_project_run` when a `runId` was returned.
2. Follow the returned `browserHandoff` and inspect the exact visible result in
   the Codex in-editor Browser.

## Verification sequence

1. Confirm the project id rather than guessing from a similar title.
2. For a durable run, require a terminal `complete` status. Treat `error` and
   `cancelled` as incomplete; a timed-out wait leaves the run active.
3. Confirm the expected page count, changed slide indexes, rendered images,
   transitions, speaker notes, current workflow stage, and current deck version.
4. Open the exact handoff returned by the mutation. Preserve its `slide`,
   `panel`, `version`, `mode`, `conversation`, `checkpoint`, and `run` query
   parameters.
5. In Browser, confirm the intended slide or panel is focused and the visible
   result matches the request. Do not treat a JSON response alone as visual QA.
6. Export only after the current or explicitly selected version passes review.

If the in-editor Browser is unavailable, use the project state and persisted
slide-image endpoints as structural evidence, return the exact handoff URL, and
state that visible Browser verification remains outstanding.

For cross-surface changes, also verify that refreshing or reopening the same
project preserves the run result and deep-link focus.
