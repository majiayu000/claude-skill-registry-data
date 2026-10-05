---
name: complete-slice
description: Mark a rolling-wave slice done on explicit user authority, regardless of its current lifecycle status or missing implementation, finalization, review, verification, or child-project state. Use when the user says a slice is done, complete, finished, accepted, or should be marked done; capture available material learnings, update project state, and output roadmap progress without requiring earlier workflow steps.
---

# Complete Slice

## Core Invariants

- Work under `docs/rolling-wave/{project}/`.
- Store project-level state in `project.md`; store slices in `slices/NNN-slug.md`.
- Use slice statuses: `pending`, `ready`, `in progress`, `ready for review`, `in review`, `done`.
- Treat explicit user completion as authoritative. If the user says the slice is done, mark it `done`.
- Accept completion from `pending`, `ready`, `in progress`, `ready for review`, or `in review`.
- Do not require implementation notes, review notes, verification, accepted breakage records, child-project completion, or a clean `finalize-slice` pass.
- Do not push back, ask for confirmation, or route to `implement-slice` or `finalize-slice` because prior lifecycle steps are missing.
- Do not modify product code, run review, or run verification. This skill records user-declared completion.
- Preserve existing project and slice history. Record only available material learnings; missing notes are not blockers.
- Slice/project artifacts are agent state. Use terse table rows or `key: value` bullets.

## Workflow

1. Resolve project and slice.
   - Use the project or slice named by the user.
   - Otherwise collect slices with status `ready`, `in progress`, `ready for review`, or `in review`; use one only when context identifies it unambiguously.
   - If no active slice exists, use the next non-done roadmap slice when user context clearly identifies it.
   - Ask only when multiple slices remain plausible and user did not identify one.
   - If selected slice is already `done`, report that state and show roadmap progress without rewriting completion history.

2. Read available state.
   - Read `project.md` roadmap and selected slice file.
   - Read implementation, review, test backlog, child-project, risk, and decision state only when present.
   - Do not interpret absent state as evidence against completion.
   - Use `../rolling-wave-common/references/lifecycle.md` for status naming, not as a prerequisite gate.

3. Mark done.
   - Set selected slice status to `done` regardless of prior status.
   - Update matching `project.md` roadmap row to `done`.
   - Clear current or active slice fields when they reference selected slice.
   - If selected slice has an unfinished child project, leave child state unchanged. Parent completion declaration still stands.
   - Do not emit warnings about skipped implementation, finalization, review, tests, or verification.

4. Capture available learnings.
   - Add completion learnings only when existing state contains material information affecting later work, project risk, review notes, accepted breakage, PR context, or roadmap order.
   - Do not invent learnings from missing implementation or review notes.
   - Update `project.md` only for material cross-slice state already supported by artifacts or direct user statements.
   - Preserve future slices unless known learning materially changes scope or order.

5. Output roadmap progress.
   - Inspect roadmap and slice statuses after completion.
   - Output a roadmap checklist window centered on the selected slice: up to two preceding slices, the selected slice, and up to two following slices.
   - Keep the window in planned order and never expand it beyond five slices. Near the start or end of the roadmap, show only the available preceding or following slices; do not pull in extra slices from the other side.
   - Use checked items for `done`; unchecked items for all remaining statuses.
   - Do not add redundant status labels such as `(done)` or `(pending)`.
   - Mark the first remaining roadmap slice as `next` when it appears in the window, unless recorded roadmap pressure changes order.
   - If no unfinished slices remain, say roadmap complete and name only material remaining project risks or open questions.

## Completion

Stop after marking selected slice `done`, capturing available material learnings, naming next planned slice, and showing roadmap checklist. Do not prepare next slice.

Never respond with instructions to run `implement-slice` or `finalize-slice` first when user explicitly declared completion.
