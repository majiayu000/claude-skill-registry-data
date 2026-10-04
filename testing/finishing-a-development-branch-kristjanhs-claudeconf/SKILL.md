---
name: finishing-a-development-branch
description: Close out a branch — verify tests, merge to main, no push.
---

# Finishing a Development Branch

## The Process

### Step 1: Verify Tests

**If a caller (`impag` Step 4c/Step 7, `subagent-driven-development` Step 7, `executing-plans` Step 5) already ran the full suite green this turn, skip and report `Tests: <X> passed (caller-run)`.** Re-running is a duplicate.

Otherwise run the project's test suite (`pytest tests/ -q`, `npm test`, `cargo test ./...`, etc.).

**If tests fail:** Stop. Report failures concisely and do not continue. The caller resolves.

**If tests pass:** Continue.

### Step 2: Report Branch State

```
Branch: <current-branch>
Commits ahead of <base>: <N> (<short-sha>..<short-sha>)
Tests: <X> passed
```

### Step 3: Merge to main and activate it

By the end of this skill the work lands on `main` (the repo's default branch) and `main` is the active branch.

1. **Merge only if not already on `main`.** If the current branch *is* `main` (work was committed directly to it), there is nothing to migrate — report `On main; nothing to merge` and skip to returning control.
2. Otherwise, from the current topic branch:
   - `git checkout main`
   - `git merge --ff-only <topic>` when it fast-forwards; if it cannot, `git merge --no-ff <topic>` with a one-line merge message.
   - On a clean merge, delete the merged branch: `git branch -d <topic>` (and remove its worktree if one exists).
   - Leave `main` checked out.
3. **Never push.** Pushing stays an explicit, separate user action (host-only per the git-push policy). Report `main now at <sha>, ahead of origin/main by <N>`.
4. **On conflict or merge failure:** stop, leave the repo on the topic branch untouched, report the conflict, and let the caller/user resolve. Never force, reset, or `-X` your way past a conflict.

Then return control to the caller **in the same turn**. Do NOT print a transition sentence ("Proceeding to /retro", "continuing", "now invoking the next step") — the caller advances directly to its next step in the same response; the handoff is silent by design.

### Step 4: Discard instead (only on explicit `discard`)

If the user says `discard` rather than letting the merge proceed, confirm before acting:

```
Discard will permanently remove:
<commit-list>
Worktree: <path or "—">

Type `discard` again to confirm.
```

On the second `discard`, run the appropriate rollback:
- Local-only commits on an integration branch: `git reset --hard <base-SHA>`.
- Topic branch: `git checkout <base>` + `git branch -D <branch>` + worktree removal if present.

Otherwise do nothing.
