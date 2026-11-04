---
name: resolve
description: Guided merge conflict resolution with verification. Shows each conflict with context from both branches, suggests resolution based on understanding both changes, verifies tests pass after resolution, and checks that no functionality was lost. Use when user says "resolve conflicts", "merge conflict", "fix conflicts", "rebase failed", "conflict resolution", or has merge conflicts to resolve. Use only when a merge or rebase has stopped on conflicts; for general debugging, use /investigate; for code review, use /review.
argument-hint: "/resolve"
allowed-tools: "Read, Edit, Bash, Grep, Glob, AskUserQuestion"
sensitive: true
---

## Overview

Interactive conflict resolution that understands the intent behind each side of a conflict. Resolves conflicts one at a time with test verification after all conflicts are resolved.

## When to Use

- A merge, rebase, or cherry-pick stopped on conflicts and `git status` lists unmerged paths.
- The user says "resolve conflicts", "merge conflict", "fix conflicts", "rebase failed", or "conflict resolution".

For test failures with no conflict in progress, use `/investigate`; for reviewing the merged result, use `/review`.

## Arguments

- No arguments: detect and resolve conflicts in the current working tree.

## Process

### Step 1: Detect conflict state

Run `git status` to find all conflicted files. If no conflicts exist, check whether a rebase or merge is in progress:

```
git status
git rev-parse -q --verify MERGE_HEAD
git rev-parse -q --verify CHERRY_PICK_HEAD
test -d "$(git rev-parse --git-path rebase-merge)" || test -d "$(git rev-parse --git-path rebase-apply)"
```

Ask git for these paths instead of reading `.git/` directly. In a linked worktree `.git` is a file, not a directory, so `.git/MERGE_HEAD` never exists there and an in-progress merge reads as absent.

If no conflicts and no in-progress operation, inform the user and exit.

### Step 2: List all conflicted files

Present the full list of conflicted files with their conflict type:

| File | Type |
|------|------|
| src/auth/login.ts | Both modified |
| src/api/routes.ts | Both modified |
| src/config/db.ts | Deleted by theirs, modified by ours |

### Step 3: Resolve each file

For each conflicted file, in order:

#### 3a. Read the conflict

Read the full file. Identify each conflict block marked by `<<<<<<<`, `=======`, `>>>>>>>`.

#### 3b. Understand both sides

For each conflict block:

1. Read the "ours" section: the changes from the current branch.
2. Read the "theirs" section: the changes from the incoming branch.
3. Check the git log for both branches to understand what each change was trying to accomplish:

```
git log --oneline -5 HEAD -- <file>
git log --oneline -5 MERGE_HEAD -- <file>
```

If this is a rebase, use `REBASE_HEAD` instead of `MERGE_HEAD`.

State what each side intended: "Our branch added input validation to the login handler. Their branch refactored the handler to use a service layer."

#### 3c. Choose a resolution strategy

| Situation | Strategy |
|-----------|----------|
| Changes are in different logical areas that happen to touch the same lines | Combine both changes |
| One side is a superset of the other | Take the more complete version |
| Both sides changed the same logic differently | Merge both intents into a single implementation |
| One side deleted code the other modified | Understand why it was deleted. If the deletion was intentional, keep the deletion. If the modification is important, keep the modification |
| Formatting-only conflict | Take whichever matches the project's formatter output |

#### 3d. Apply the resolution

Remove the conflict markers. Write the resolved content. Explain what was kept and what was discarded.

### Step 4: Stage resolved files

After all conflicts in a file are resolved:

```
git add <file>
```

Repeat Steps 3-4 for every conflicted file.

### Step 5: Verify with tests

Run the full test suite. This catches resolutions that compile but break behavior.

If tests fail:

1. Identify which resolution likely caused the failure by examining the test error and the resolved files.
2. Re-read the conflicting change.
3. Re-resolve that specific conflict with a different approach.
4. Run tests again.

### Step 6: Complete the operation

Continue the interrupted git operation:

- For merge: `git commit` to finalize the merge commit.
- For rebase: `git rebase --continue` to apply the next commit.
- For cherry-pick: `git cherry-pick --continue`.

If more conflicts appear after continuing a rebase, return to Step 1.

### Step 7: Final verification

After the operation completes with no remaining conflicts:

1. Run the formatter check.
2. Run the linter.
3. Run the type checker.
4. Run the full test suite.
5. Verify the branch builds cleanly.

## Rules

- Never lose functionality from either side of a conflict. If both sides added features, the resolution must include both features.
- Always explain what each side intended before resolving. A resolution without understanding is a guess.
- Always test after resolution. A conflict that resolves cleanly at the text level can still break behavior.
- Never use `git checkout --ours` or `git checkout --theirs` on an entire file without reading every conflict in that file first. Blanket ours/theirs discards changes without review.
- When a conflict involves a generated file such as a lockfile, `package-lock.json`, or `pnpm-lock.yaml`, regenerate it from the resolved manifest instead of hand-merging it: resolve the manifest first, then run the package manager's install, which rewrites a lockfile holding conflict markers from the resolved manifest while keeping every unchanged pin, and stage the result. When the tool refuses the conflicted file, restore the base side with `git checkout --ours -- <lockfile>` and install again. Never delete the lockfile: a fresh resolve moves every dependency to its newest allowed version, which is an unreviewed upgrade hidden inside a merge.
- If a conflict is too complex to resolve confidently, present both versions to the user with your analysis and ask for a decision. Do not guess.

## Common Rationalizations

- "Our side is newer, so take ours for the whole file": newer is not more complete. Read every block, since a blanket `--ours` drops the other branch's feature with no trace.
- "The file has no markers left, so it is resolved": text-level cleanliness says nothing about behavior. Step 5 runs the suite for that reason.
- "Hand-merging the lockfile is faster than regenerating it": a hand-merged lockfile passes review and fails a frozen install. Regenerate it with the package manager.
- "The intent is obvious from the diff": state each side's intent from `git log` before choosing a strategy. The log names what the diff hides.

## Red Flags

- Stop and read the commit history for both sides when you cannot state in one sentence what each side intended.
- Stop and ask the user, with both versions and your analysis, when two conflict blocks pull the same logic in incompatible directions.
- Stop and re-resolve the specific conflict the failure points at when the suite fails after resolution.
- Stop and return to Step 1 when `git rebase --continue` reports new conflicts.

## Verification

- `git diff --name-only --diff-filter=U` prints nothing.
- `grep -rn '^<<<<<<<\|^>>>>>>>' <resolved files>` prints nothing.
- Every resolved block has a one-line statement of what was kept from each side.
- The formatter check, linter, type checker, full test suite, and build pass after the operation completes.
- No `git merge`, `git rebase`, or `git cherry-pick` is still in progress: `git rev-parse -q --verify MERGE_HEAD` and `git rev-parse -q --verify CHERRY_PICK_HEAD` exit non-zero, and neither `git rev-parse --git-path rebase-merge` nor `git rev-parse --git-path rebase-apply` names an existing directory.

## Related skills

- `/investigate` -- Debug test failures caused by a bad resolution.
- `/review` -- Review the merged result before pushing.
- `/ship commit` -- Commit after successful resolution.
