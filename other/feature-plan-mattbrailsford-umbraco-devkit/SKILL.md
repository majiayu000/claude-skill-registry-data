---
name: feature-plan
description: >-
  Slices a finished design into user stories and an ordered task checklist (STORIES.md and
  PLAN.md) for feature-build. Use once feature-design has decided how to build the feature.
user-invocable: true
argument-hint: [scope to plan, optional]
---

# feature-plan

> 🎯 **Design for change.** Slice tasks so each one touches one seam. A task that edits five
> unrelated files, or straddles both a Management API controller and an unrelated UUI
> component, is a coupling smell — re-slice before handing it to `feature-build`.

Turn the design into something `feature-build` can execute. This command **transforms**
`SPEC.md` — it does not re-elicit requirements.

## Where this writes

The same per-feature plan folder. Owns two files:

- **`STORIES.md`** — via the `user-stories` skill; Given/When/Then acceptance criteria per
  story.
- **`PLAN.md`** — the dependency-ordered task checklist `feature-build` executes.

Read `ARCHITECTURE.md` and `SPEC.md` — this is confirmation and slicing, not a fresh
interview.

Also updates its own two lines in `README.md` — same append-only discipline as
`DECISION-LOG.md`: never touch a line owned by another phase.

A checklist of small, dependency-ordered, independently reviewable tasks forces sizing and
sequencing decisions up front and gives `feature-build` something mechanically parseable to
gate against. Keep this discipline (small, ordered, reviewable units) even for a project that
tracks completion via issues instead of an in-doc checklist.

## Scope

- IN: derive user stories from `SPEC.md`, order tasks into a dependency-aware checklist,
  mark what can run concurrently, then generate executable specs via `bdd-specs` —
  always, no asking.
- OUT: gathering requirements (`feature-explore`/`feature-design`), building
  (`feature-build`).

## Preflight

1. Resolve which feature this run is for. If more than one plan folder exists, prefer a match
   between the current branch/worktree name and a folder name (see `CLAUDE.md`'s "Finding the
   current feature's plan folder" rule) — this is the normal case once `feature-build` has
   started. If nothing matches, fall back to the one plan folder present, or ask if more than
   one is ambiguous.
2. Read `SPEC.md` (and `ARCHITECTURE.md` for context) in the resolved folder. If `SPEC.md` is
   still a stub or full of `TODO`, **stop** — send the user back to `feature-design`.
   Likewise if `SPEC.md` describes a new or visibly changed screen that has no mockup in
   `mockups/`: name the screens and send the user back to `feature-design`. A screen
   without a mockup can't be approved, so it can't be planned.
3. Read any existing `STORIES.md`/`PLAN.md`. Re-entrant: reconcile and extend; never silently
   drop or renumber completed (`- [x]`) tasks.

## Stories

Delegate to `user-stories` to produce/refine `STORIES.md` (Given/When/Then acceptance
criteria per story, formatted so `bdd-specs` can consume it directly). Don't hand-roll the
format.

## Specs (always, no asking)

Once `STORIES.md` is finalized and `PLAN.md` is written, always delegate to `bdd-specs` to
generate executable, pending spec files from the stories. This is part of `feature-plan`'s
contract, not optional. The generated specs should fail (or be marked pending) until
`feature-build` turns them green.

## Interview

Light — confirmation, not elicitation. ~3–5 questions, batched:

1. Here's how `SPEC.md` was sliced into stories — anything mis-cut or missing?
2. Priority/sequence right? What's the first shippable slice?
3. Any task marked parallel that actually shares a file or a migration?
4. Hard external dependencies that gate ordering (a CMS API only available from a certain
   version, a package that must ship first)?

## Produce

Write every file this phase produces following `plain-writing`: a person reads it before the
next phase runs, so it should be quick to read without leaving anything out.

`PLAN.md`, a checklist `feature-build` can execute:

- Every task is `- [ ]`, top-to-bottom in dependency order.
- Each task line carries: a short id, the story it implements, explicit `depends-on:` ids,
  and a `parallel-group:` tag for tasks with no ordering between them.
- One task = one reviewable, committable unit of work.
- No task references a file, extension point, or decision not already in `ARCHITECTURE.md`/
  `SPEC.md`.
- **Wire tasks are first-class.** For every feature that touches a real entry point — a
  Management API controller, a Composer-registered service, a backoffice manifest entry —
  include an explicit `wire: <feature> into <entry point>` task whose acceptance is a real
  request or resolution through the deployed artifact, not just "unit tests pass." A task
  whose only acceptance criterion is unit-test-green is not allowed for anything on that
  path — that's how stubs ship.
- **Sync tasks travel with their entity.** If the project supports Umbraco Deploy or uSync
  (`umbraco-env-sync`'s "Does this project sync?") and a task adds or changes a synced
  entity, the matching sync change from its "Keep sync in step" table is in the plan: in
  the same task, or a task that `depends-on:` it. If `ARCHITECTURE.md` doesn't say how a
  new entity moves, stop and send the user back to `feature-design`.

Update the `STORIES.md` and `PLAN.md` lines in `README.md`: check each box and replace
`<pending>` with one plain-English line (e.g. "N stories" / "M tasks, first parallel group
is...").

Append dated `DECISION-LOG.md` entries for non-obvious sequencing decisions (why task X
blocks task Y, why a slice was deferred).

## Hand off

Summarize: N stories, M tasks, S spec files generated, the first parallel group, then:
`Suggested next: feature-build — specs are in place and pending.` For a large or risky plan,
mention `feature-interrogate` as an optional stress-test before that first build.
