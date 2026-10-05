---
name: finalize
description: Prepare a branch for merge — done-checks, pre-merge docs, version bump, then a staged conventional commit. Trigger on:- finalize, ready to merge, ship it, prep for PR, version bump, stage and commit, pre-merge.
argument-hint: "Change type (feature|fix|hotfix|chore|refactor) and optional scope"
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Finalize

The pipeline's land step. Run done-checks, update docs and version, produce a clean
commit. Generic — no repo-specific names. A setup with its own ledger contract wraps
this in an overlay (e.g. `land-feature`) rather than editing it.

## When to use this

- Code is functionally complete and the review thread is `closed`.
- Skip if a regression is outstanding — fix it first.

## Procedure

1. **Read `.specify/memory/constitution.md`.**

2. **Determine change type** (infer from context, else ask):

   | Type | Semver | When |
   |---|---|---|
   | `feature` | minor | new user-facing capability |
   | `fix` / `hotfix` | patch | bug correction |
   | `chore` / `refactor` | patch or none | tooling / restructure, no behaviour change |

3. **Done checks** — verify before touching any file:
   - Planned work items resolved; no new open TODOs from this task.
   - Tests pass locally (the project's own test runner).
   - No debug/temp code (`console.log`, `debugger`, `pdb.set_trace`, `TODO(wip)`).
   - No merge conflicts; lint/type-checks pass if configured.

   If any check fails, stop and report what is blocking.

4. **Pre-merge documentation** — update only what exists in the repo:
   - CHANGELOG / RELEASE_NOTES — an entry under `## [Unreleased]` or the new version.
   - README — if setup, usage, or the feature list changed.
   - API / schema / migration docs — if public interfaces changed or the change is breaking.

5. **Version bump** — locate the version source (`package.json`, `pyproject.toml`,
   `VERSION`, …), apply the semver increment, write it back to every file that must stay
   in sync, report `Version: X.Y.Z → X.Y.Z'`. If the project tags manually, note the tag
   and skip file edits.

6. **Reconcile the plan index.** If `specs/*/plan.md` or `docs/plans/` holds a plan for
   this work, flip its status to `implemented` in the index it lives in — never rename or
   delete the plan file.

7. **Stage and commit — after the user confirms.** `git status --short` first; if
   unrelated files are dirty, stage by path and say what you left out. Show the staged
   paths and the message, then wait.

   ```
   <type>(<scope>): <short imperative summary>

   <optional body — what changed and why, wrapped at 72 chars>
   <optional footer — BREAKING CHANGE: ..., Closes #NNN>
   ```

   First line ≤ 72 chars, imperative mood. Never amend. Push only if asked.

## Done criteria

- All done-checks pass.
- Changelog and version files updated where they exist.
- Commit staged with a conventional message, user-confirmed.
- Plan index reconciled.
