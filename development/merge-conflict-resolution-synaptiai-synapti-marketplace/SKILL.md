---
name: merge-conflict-resolution
description: "Detect, classify (porcelain status; complexity: trivial, semantic, structural, delete-modify), and resolve git merge conflicts through per-file strategy selection (accept-ours, accept-theirs, manual-merge, rebase), manual conflict hunk parsing, and post-resolution verification (orphaned markers, build, tests). Use when a branch has conflicts with its merge target or when rebasing onto an updated base. This skill MUST be consulted because silently dropping changes is non-negotiable; every conflict resolution must account for both sides."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, TaskCreate, TaskList, TaskUpdate, AskUserQuestion
context: fork
agent: general-purpose
---

# Merge Conflict Resolution

## Contract

Iron law: **never silently drop changes — every resolution accounts for both sides, documents any excluded lines, and asks the user rather than guessing.** Invoked by `/flow:resolve` Phase 1 (detect and classify), Phase 2 (per-file strategy plan), Phase 3 (resolve hunks), and Phase 4 (marker audit, complete merge/rebase, quality checks). Returns, per conflicted file: type (UU/AA/UD/DU/AU/UA), complexity (trivial/semantic/structural/delete-modify), strategy (accept-ours/accept-theirs/manual-merge/ask-user), hunk count, and result, plus the quality outcome. Permitted skips: none — trivial files auto-resolve only when `conflictResolution.autoResolveTrivial` is true; delete-modify and competing hunks always go to the user.

## Detect

```bash
git diff --name-only --diff-filter=U
git status --porcelain
```

Settings: `conflictResolution.autoResolveTrivial` (default `true`), `conflictResolution.maxConflictFiles` (default 20). Above the limit, `AskUserQuestion`: proceed anyway, or abort and rebase in smaller steps.

## Classify

| Status | Type |
|--------|------|
| UU | Content — both sides modified the same file |
| AA | Add-add — both sides added the same name |
| UD | Delete-modify — ours deleted, theirs modified |
| DU | Delete-modify — theirs deleted, ours modified |
| AU / UA | Rename collision |

| Complexity | Meaning |
|------------|---------|
| trivial | Non-overlapping changes in different sections |
| semantic | Both sides change the same logical unit |
| structural | One side refactored (moved code, renamed, restructured) |
| delete-modify | One side deleted what the other modified |

## Strategy

| Strategy | When | Autonomy |
|----------|------|----------|
| accept-ours | Their change is superseded by ours | Tier 1 for trivial |
| accept-theirs | Our change is superseded by theirs | Tier 1 for trivial |
| manual-merge | Both changes are needed | Tier 2 — show rationale |
| rebase | Linear history wanted, few conflicts | Tier 2 — show rationale |

Create one task per file (type, complexity, strategy, hunks) and display the Conflict Analysis table. Trivial files auto-proceed when `autoResolveTrivial` is true; semantic, structural, and delete-modify files show both sides and the proposed strategy via `AskUserQuestion` first. Never "take ours for everything" — analyze each conflict individually, and verify that "identical" changes really are identical.

## Resolve Each Hunk

1. Parse the ours block (`<<<<<<<` to `=======`) and theirs block (`=======` to `>>>>>>>`).
2. Identify each side's intent.
3. Compatible (different imports, non-overlapping logic) → combine both. Competing (two implementations of the same thing) → `AskUserQuestion` showing both sides with context.
4. Write the resolved content with all markers removed; `grep -n '<<<<<<<\|=======\|>>>>>>>' "$FILE"` must return nothing.
5. `git add "$FILE"`; mark the task completed.

**Delete-modify**: show what was deleted and what was modified; offer keep-modified, accept-deletion, or keep-modified-at-new-location (if the file moved); wait for the decision. Never auto-resolve.

## Verify (Phase 4)

1. Repo-wide marker audit — must return nothing; any hit goes back to resolving that file:
   ```bash
   grep -rn '<<<<<<<\|=======\|>>>>>>>' --include='*' . 2>/dev/null | grep -v '.git/' | grep -v 'node_modules/'
   ```
2. Complete: `git commit --no-edit` (merge) or `git rebase --continue` (rebase).
3. Run lint, tests, typecheck (commands from capability-discovery). Failures → `debugging-patterns`, up to `closedLoop.maxBuildIterations`.
4. Review the resolution diff (`git diff HEAD~1 --stat`) — passing tests do not prove semantic correctness. Every file in the conflict list is verified or its skip explicitly documented; "this file isn't important" is not a reason.
