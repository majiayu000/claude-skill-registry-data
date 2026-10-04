---
name: "Branch: Integrate"
description: "Integrate a target branch into the current one by merge, rebase or squash"
when_to_use: "When main (or another branch) has moved on and needs folding into the current branch: picks merge/rebase/squash and handles conflicts."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: branch
disable-model-invocation: true
allowed-tools: ["Bash(git:*)", "Bash(~/.claude/library/scripts/git-integrate.sh:*)", "Read", "Glob", "Grep", "Edit"]
arguments: ["strategy", "target"]
argument-hint: "[merge|rebase|squash] [target branch, default main]"
---

# Integrate `$target` into the current branch

Replaces the former git-branch-merge / git-branch-rebase / git-branch-squash trio. The mechanical flow (fetch, integrate, state checks) lives in the script; you handle conflicts, the squash commit message, tests and the push.

`$strategy` is required (`merge`, `rebase` or `squash`); `$target` defaults to `main` when empty.

## Steps

1. Check the current branch name and **confirm with the user** before proceeding.
2. Do NOT create a worktree; work in the current directory.
3. Run `"$HOME"/.claude/library/scripts/git-integrate.sh $strategy $target` (bare `$strategy` when `$target` is empty). Its exit codes:
   - **0**: integration done. For `squash` the branch's changes are staged as one unit: write a single descriptive commit message (conventional commits) and commit.
   - **2**: state error (dirty tree, detached HEAD, wrong branch, fetch failure). Report the script's message and stop; fix only what the user asks you to fix.
   - **3**: conflicts, left in place. List them, then resolve with judgement about whose change is *right*: our branch's intent wins for the work this branch is about; the incoming side (usually main) wins elsewhere, since its conflicting change typically carries a fix this branch predates. Never resolve by discarding our changes wholesale, and never by discarding main's either. Then `git commit` (merge) or `git rebase --continue` after each (rebase/squash).
4. Run the project's tests to verify the integration.
5. **Only when tests pass**, push: `git push` after a merge; `git push --force-with-lease` after a rebase or squash. Never plain `--force`.

## Red flags

**Never:** push with failing tests; force-push without `--with-lease`; run the script on a dirty tree ("stash it yourself" is the user's call, not yours).
**Always:** confirm the branch first; keep conflict resolutions minimal and intent-preserving.
