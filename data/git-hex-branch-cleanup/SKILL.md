---
name: git-hex-branch-cleanup
description: >
  This skill should be used when the user wants to clean up a feature branch's
  history using git-hex (squash/fixup commits, reorder/drop/split commits, or
  rebase a branch onto main) without using an interactive terminal. Trigger
  phrases include: "clean up my branch", "polish history", "squash these commits",
  "fixup commits", "rebase onto main", "rewrite commits".
---

# Git-hex Branch Cleanup

## When to use this Skill

This skill should be used when:

- The user says they want to "clean up", "rewrite", "polish", or "squash" a git
  history or feature branch.
- The user wants to rebase a branch onto another branch (e.g. `main`) and present
  a clean, reviewable set of commits.
- The user wants to split, squash, or reword commits using git-hex tools instead
  of manual interactive rebase.

Trigger phrases include: "clean up my commits", "squash fixups", "polish history",
"rewrite commits", "rebase onto main", "make this branch reviewable".

## Workflow

1. **Plan first**
   - Call `git-hex-getRebasePlan` to inspect the commit range you would modify.
   - Optionally call `git-hex-checkRebaseConflicts` to estimate whether the rebase
     is likely to conflict.

2. **Prepare changes**
   - For small edits to the last commit, prefer `git-hex-amendLastCommit`.
   - For fixes to older commits, guide the user to edit and stage changes, then
     use `git-hex-createFixup` targeting the original commit.
   - For large or mixed commits, consider `git-hex-splitCommit` to separate files
     into focused commits.

3. **Apply the rewrite**
   - Use `git-hex-rebaseWithPlan` to reorder, drop, squash, or reword commits.
   - Prefer `autoStash: true` and `autosquash: true` when the working tree is dirty,
     following git-hex documentation.
   - Never use git-hex on shared or protected branches; operate on feature branches
     the user controls.

4. **Safety and recovery**
   - If the result is not what the user wanted, call `git-hex-undoLast` to restore
     the previous state using git-hex backup refs.
   - If a rebase pauses with conflicts, hand off to the conflict resolution Skill.

## Tools to prefer

- Planning: `git-hex-getRebasePlan`, `git-hex-checkRebaseConflicts`
- History rewrite: `git-hex-rebaseWithPlan`, `git-hex-createFixup`,
  `git-hex-amendLastCommit`, `git-hex-splitCommit`, `git-hex-cherryPickSingle`
- Recovery: `git-hex-undoLast`

## Key constraints

- `reword` action **requires** `message` field (without it, git opens an editor → hang).
- Messages must be **single-line** (no TAB/newline characters).
- For reordering commits, set `requireComplete: true` in the plan.
- Prefer `fixup` over `squash` unless you need to combine commit messages.
- Tools that perform their own auto-stash (`amendLastCommit`, `splitCommit`, `cherryPickSingle`) expose `stashNotRestored` when stash pop failed; `rebaseWithPlan` uses Git's native `--autostash` and does not emit this flag.
