---
name: work-unit-commits
description: "Deliver verified implementation as cohesive commits. Trigger: explicit commit request, commit-per-unit, commit splitting, or keeping tests and docs with code."
license: Apache-2.0
metadata:
  author: gentleman-programming
  adapted_by: andresnator
  source: gentleman-programming/gentle-ai
  status: in-progress
  version: "3.0.1"
---

# Work-unit commits

## Activation

Load this skill only after `Delivery: commit-per-unit` has been resolved from an explicit execution instruction or plan. Load it directly, outside `implementation-skill-routing`; delivery and Git are not implementation skills.

The primary coordinator is the sole owner of the Git index. Workers never stage, commit, or push. Review, Judgment, chained PRs, push, and merge remain separate workflows.

## Preflight

Complete this before the first implementation edit:

1. Require a Git repository, a valid `HEAD`, and an attached branch. Record the full `HEAD` as the delivery baseline and expected parent of the first commit.
2. Resolve the exact target scope and reject `.ai/` or any path inside it.
3. Inventory tracked, staged, unstaged, and untracked paths. Preserve every path outside the target scope, including unrelated staged entries.
4. Treat any pre-existing target change as material ambiguity. Direct execution asks whether to include it, switch to `working-tree`, or stop. SDD blocks without editing or changing delivery.
5. Honor an explicit commit count, order, granularity, or message. Otherwise define the smallest cohesive units that are independently useful and verifiable.

Never use `git add .`, `git add -A`, a repository-wide pathspec, or a command that clears the index.

## Commit one unit

A unit keeps one behavior, fix, migration, or documentation outcome with its tests and user-facing docs. Work groups are candidates, not mandatory commit boundaries.

Deliver units serially:

1. Apply only the unit and run its focused check. A failing unit is not committed.
2. Require the current full `HEAD` to equal the previous unit SHA, or the baseline for the first unit.
3. Derive the exact changed path list for the unit and ensure it contains no unrelated or `.ai/` path. For SDD, persist the pending record below before staging.
4. Stage only those paths with `git add -- <paths>`. Require no unstaged diff in them.
5. Inspect the staged path set and staged diff for those paths. Reject empty, missing, or unexpected content, then run `git diff --cached --check -- <paths>`.
6. For SDD, save the pre-hook snapshot below. Commit with hooks enabled and an explicit pathspec, such as `git commit -m <message> -- <paths>`. Preserve unrelated staged entries.
7. Verify that the new commit has the recorded pre-commit `HEAD` as parent, contains exactly the unit paths, excludes `.ai/`, and leaves the unit paths without staged or unstaged changes.

Use outcome-oriented Conventional Commit messages unless the user supplied exact messages. Inspect repository message style before choosing them.

## SDD pending delivery

Before staging, persist a pending record in `run.md`: unit id, source work ids, declared scope and exact changed paths, focused check and result, intended message, expected parent SHA, and a pre-stage Git snapshot. Store snapshot evidence under the run root, outside commits. Include index paths, modes and blob IDs, plus working-tree paths, status, modes and content hashes for tracked and untracked changes, including unrelated state; mark absent paths and exclude `.ai/`.

After staging and validation, save a separate pre-hook snapshot of the same state before invoking `git commit`. Keep both snapshots and the pending record on failure; record the failure and observed state without replacing that evidence.

On resume, require `HEAD` to match both the ledger tip (or `Baseline` when `Commits: none`) and the pending parent. Require Git state to match the saved pre-stage or pre-hook snapshot, then rerun the focused check before retrying that same unit. Missing evidence or any mismatch blocks; never reconstruct a split or combined unit from work groups or absorb new changes.

Only after commit verification, replace `Commits: none` or append one complete row, then clear the pending record:

```text
Commits: <unit-id> | <full SHA> | <message>
```

No pending unit may remain at final verification or archive.

## Hooks, failures, and continuity

Never skip hooks. If a hook fails or changes `HEAD`, the index, or the working tree unexpectedly, inspect all three and stop. Do not retry through amend, reset, checkout, restore, rebase, squash, index clearing, or another destructive shortcut.

A correction after a commit is a new cohesive unit with a new focused check and a new commit. Never amend, reset, rebase, squash, or otherwise rewrite delivery history. If execution stops, preserve every green commit and report its full SHA plus the remaining scope.

Never push.
