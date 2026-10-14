---
name: tcr
description: "Run Test && Commit || Revert as exact, attributable Direct microsteps. Trigger: TCR, test and commit, revert on red, or micro commits."
license: MIT
metadata:
  author: andresnator
  status: backlog
  version: "2.0.1"
---

# TCR

`TCR = Test && Commit || Revert` applies one deliberately small change at a time. Green commits the microstep; red reverts only that microstep.

## Activation

Use TCR only in Direct execution after `Delivery: tcr` has been resolved explicitly. The primary coordinator owns every inventory, rollback, stage, and commit. Workers never use this skill or mutate Git.

Before editing:

1. Require a Git repository, a valid `HEAD`, and an attached branch.
2. Resolve an exact target scope that excludes `.ai/`. Any staged, unstaged, or untracked target path blocks TCR.
3. Inventory all target and unrelated tracked, staged, unstaged, and untracked paths. Preserve unrelated state, including staged entries.
4. Run every supplied `Verify` item, or the resolved full-scope check for a request without a plan. The complete baseline must be green.
5. Record the full `HEAD`. It is the expected parent for the first microstep.

TCR is not available for SDD. Never silently replace it with `commit-per-unit` or `working-tree`.

## One microstep

Before each edit, declare one small intent and its exact existing and proposed paths. Record:

- the current full `HEAD`;
- tracked paths the step may modify, delete, or rename;
- every proposed new path and whether it already exists;
- scoped staged, unstaged, and untracked state;
- the focused check for this step.

Apply only that intent and run the focused check.

### Green: commit

1. Require `HEAD` to equal the recorded pre-step SHA.
2. Derive the exact changed paths and ensure all belong to the declared microstep and exclude `.ai/`.
3. Stage only those paths with `git add -- <paths>`; never use a broad add.
4. Require no unstaged diff in them. Inspect their staged path set and diff, then run `git diff --cached --check -- <paths>`.
5. Commit with hooks enabled and an explicit pathspec. Preserve all unrelated staged entries.
6. Verify the commit parent, exact path set, `.ai/` exclusion, and clean microstep paths before starting the next step.

Use the user's exact message when supplied; otherwise use one outcome-oriented Conventional Commit message.

### Red: exact rollback

First determine that the failure is caused by this microstep. Then:

1. Restore only tracked paths changed by the step from its recorded pre-step `HEAD`.
2. Remove only untracked paths that were absent from the pre-step inventory and demonstrably created by this step. Name every path explicitly; remove a new directory only after its attributable files are gone and it is empty.
3. Reinspect the target scope and require it to match the pre-step inventory exactly. Preserve every unrelated path and index entry.

Never use `git reset`, broad `git checkout`, broad `git restore`, `git clean`, globs, repository-wide deletion, or rollback by directory. If the failure is flaky, environmental, ambiguous, or the attributable rollback set cannot be proven, do not delete or restore anything; inspect and stop.

## Completion and failures

After the last green microstep, run the complete baseline `Verify` set again. A focused green check does not replace final verification.

Never skip hooks. A hook failure is not a test-red rollback signal: inspect `HEAD`, index, and working tree, then stop without a destructive retry. Corrections after a successful commit are new TCR microsteps and new commits; never amend, reset, rebase, squash, or rewrite history.

Never push.
