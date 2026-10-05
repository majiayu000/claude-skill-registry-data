---
name: known-gaps-tracker
description: Maintain docs/[version]/known-gaps.md - a per-version log of items that were not implemented, deferred, buggy, suppressed, or left without coverage at the.
---

# Known-Gaps Tracker

Maintain `docs/<version>/known-gaps.md` as a per-version, append-only record of work that did not reach a clean state by the end of each phase, and pull open items forward into the next version's plan.

## When to Use This Skill

- **Inside `/implement-phase` Phase 8**: after `/update-gitignore`, append any new gaps discovered during the phase.
- **Inside `/wrap-up-session` Phase 4**: after `/update-devlog`, sweep the live conversation for uncaptured gaps; on a version bump in Phase 6, flip the file's `Status` to `finalized`.
- **Inside `/generate-plan` Step 0.6** (right after Step 0.5 From-comparison mode): read the immediately prior version's `known-gaps.md` plus any older still-in-progress files, and offer to ingest open items into the new plan.

**When NOT to use**: do not duplicate forward-looking sprint planning that belongs in `docs/todos.md` (managed by `dev-progress-tracker`). `known-gaps.md` records what slipped during the version that just shipped or is shipping; `docs/todos.md` describes the live forward roadmap. Also distinct from `docs/<next-version>/review/00-known-gaps.md` produced by `/run-deep-review`, which is a one-shot pre-release aggregation across many sources - this file is one of the sources that aggregation should read.

## File Format

Path: `docs/<version>/known-gaps.md` - one file per version that has had at least one phase implemented.

```markdown
# Known Gaps - <version>

**Project**: <name>
**Status**: in-progress | finalized
**Last updated**: <YYYY-MM-DD>

## Summary

| Category | Open | Resolved |
|---|---|---|
| Not implemented (NI) | N | N |
| Deferred (DF) | N | N |
| Bugs / regressions (BG) | N | N |
| Warnings (WN) | N | N |
| Missing tests / coverage gaps (MT) | N | N |
| Quality-gate gaps (QG) | N | N |

## Open Items

### Not Implemented

#### NI-1 - <short title>

- **Source phase**: Phase N - <name>
- **Plan reference**: `docs/<version>/plans/<slug>.md` (sub-task N.X)
- **Reason**: <why it was skipped or could not be completed>
- **Suggested next step**: <one-line actionable hint for the next plan>

### Deferred

(DF-1 ... using the same shape as NI)

### Bugs / Regressions

(BG-1 ... include reproduction steps and observed-vs-expected behavior when known)

### Warnings

(WN-1 ... e.g., suppressed lint rules with reason, runtime warnings, dependency deprecation notices)

### Missing Tests / Coverage Gaps

(MT-1 ... files below the project coverage threshold and which paths are uncovered)

### Quality-Gate Gaps

(QG-1 ... gates the user opted to bypass with "Proceed anyway", e.g., 75% coverage instead of 80%)

## Resolved

| ID | Title | Resolved in | Notes |
|---|---|---|---|
| NI-3 | Settings panel keyboard shortcuts | Phase 5 | Implemented as part of authentication subtask |
```

ID prefixes are stable: `NI-`, `DF-`, `BG-`, `WN-`, `MT-`, `QG-`. Numbers are monotonic per category within a version - never reuse an ID once written, even after the item is resolved.

## Instructions

### Append (during `/implement-phase` Phase 8)

1. Locate or create `docs/<version>/known-gaps.md`. The version is the one that owns the active plan (`docs/<version>/plans/<slug>.md`).
2. If the file does not exist, create it with the header (`Project`, `Status: in-progress`, `Last updated`) and empty section scaffolding.
3. Walk the artifacts produced by Phases 2 through 7 of `/implement-phase`:
    - `# DEVIATION:` markers from Phase 2 - classify as `NI` (skipped), `DF` (intentionally deferred), or `BG` (deviation revealed a bug) based on the deviation reason.
    - Unresolved test failures from Phase 6 when the user picked option A "Skip failing tests" - classify as `BG`.
    - Coverage shortfalls from Phases 4 and 5 (files that ended below 80%) - classify as `MT`.
    - Suppressed lint rules or runtime warnings observed during Phase 3 - classify as `WN`.
    - Any gate the user bypassed with "Proceed anyway" in Phase 7 - classify as `QG`.
4. For each item:
    - Allocate the next ID in its category (e.g., `NI-4` if `NI-3` was the last one used).
    - Write all four required fields: `Source phase`, `Plan reference`, `Reason`, `Suggested next step`.
    - Append under the matching `## Open Items` subsection.
5. If this phase resolved any earlier open item (look up by code-change scope or by explicit reference in the deviation log), move that item from `## Open Items` to the `## Resolved` table with `Resolved in: Phase N`.
6. Recompute the `## Summary` table counts so they match the actual number of items in each subsection.
7. Update `Last updated` to today's date.
8. Do **not** finalize the file here - that is `/wrap-up-session`'s job at version bump.

### Sweep (during `/wrap-up-session` Phase 4)

1. Re-read `docs/<version>/known-gaps.md`. Create it (status `in-progress`) if it does not exist.
2. Mine the live session conversation for items not already captured during `/implement-phase`. Look for: "we'll come back to", "TODO", "deferred", "skipped", "good enough for now", suppressed warnings, hand-rolled mocks left in production code, stubbed-out functions, commented-out tests, partial implementations marked as such in chat.
3. Add any new items using the same ID allocation rules as Append. Cite the originating session (date) in the `Reason` field when the item came from chat rather than from a plan deviation.
4. Recompute the `## Summary` table.
5. Update `Last updated` to today's date.

### Finalize (during `/wrap-up-session` Phase 6 if a version bump occurs)

1. After `/update-version` completes successfully, edit the file's `Status:` line to `finalized`.
2. Append a one-line note immediately after the Summary table:

    > Finalized on <YYYY-MM-DD> at the <new-version> bump. Open items will be ingested by `/generate-plan` when the next version's plan is created.

3. Do not delete or move resolved items - the file is now an archived record. Anything still in `## Open Items` remains there for the next-version ingest step to pull forward.

### Ingest (during `/generate-plan` Step 0.6)

1. Resolve the prior version: the immediately previous semver tag (for a `v0.2.0` plan, look at `v0.1.0`).
2. Build the candidate file list:
    - `docs/<prior-version>/known-gaps.md` - always include if it exists.
    - Any older `docs/v*/known-gaps.md` whose `Status:` is still `in-progress` (gaps that lingered across more than one version).
3. Parse all candidate files. Merge their `## Open Items` into a single in-memory list, tagged with the originating version.
4. If the merged list is non-empty, show the user a compact summary and ask how to handle them:

    ```
    Found N open items from prior versions:

    From v0.1.0 (finalized):
      [NI-2] Settings panel keyboard shortcuts not wired (Phase 4)
      [BG-1] Token refresh race condition (Phase 6)

    From v0.0.5 (still in-progress):
      [MT-3] tests/integration/payment_flow.py below 60% coverage

    How should I treat these in the new plan?
      A. Ingest all open items as scope (recommended)
      B. Pick a subset to ingest
      C. Skip - I will handle them outside this plan
    ```

5. Selected items are seeded into the discovery interview at Q2 (Scope) and Q3 (Affected Areas). They become tagged sub-tasks in Step 4 with the prefix `[from <prior-version> known-gaps: NI-2]`. Each Step 4 sub-task `Prompt` block must restate the original `Reason` and `Suggested next step` so the executable prompt is self-contained.
6. After the new plan file is written, edit each ingested item in its source `known-gaps.md`: move it from `## Open Items` to the `## Resolved` table with `Resolved in: transferred to <new-version> plan`. Items are not yet *fixed* - just transferred to a different tracking surface.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll just remember to fix this in the next session" | The next session is in a different conversation; the gap will be lost. The file is the only durable channel between sessions. |
| "It's already in the devlog" | The devlog is chronological narrative. `known-gaps.md` is structured, queryable, and ingested by `/generate-plan` automatically. The two complement each other. |
| "I'll add it to docs/todos.md instead" | `docs/todos.md` is forward-looking and manually maintained; it does not flow into `/generate-plan` automatically. Use `known-gaps.md` for items that came out of an actual implemented phase. |
| "This warning isn't really a gap" | If a future version would benefit from fixing it, it is a gap. Record at the appropriate severity - `WN` is fine for low-impact items. Better to over-record and let `/generate-plan` Step 0.6's "pick a subset" option filter than to lose the signal entirely. |
| "I already wrote this up in the session history" | Session-history files are per-session, not per-version. The known-gaps file aggregates across every phase of a single version and is the only artifact `/generate-plan` reads to pull work forward. |

## Verification

- [ ] `docs/<version>/known-gaps.md` exists and has the required header (`Project`, `Status`, `Last updated`).
- [ ] Every open item has all four fields: `Source phase`, `Plan reference`, `Reason`, `Suggested next step`.
- [ ] Summary-table counts match the actual number of items in each subsection (compute, do not estimate).
- [ ] After `/wrap-up-session` runs on a version bump, `Status:` reads `finalized` and the version-bump note is present immediately after the Summary table.
- [ ] When `/generate-plan` ingests items, the corresponding entries in the source file have moved from `## Open Items` to `## Resolved` with `Resolved in: transferred to <new-version> plan`.
- [ ] Item IDs are not reused: a resolved `NI-3` does not become a new `NI-3` later.

## Related Skills

- `dev-progress-tracker` - maintains `docs/todos.md` (forward-looking sprint roadmap); known-gaps is the per-version archive companion that records what slipped.
- `session-history` - retrospective per-session record; known-gaps is a structured punch-list aggregated across sessions of the same version.
- `version-upgrade` - the version-bump operation that triggers known-gaps finalization.
- `implementation-plan` - generates the plan that known-gaps eventually feeds into for the next version.
