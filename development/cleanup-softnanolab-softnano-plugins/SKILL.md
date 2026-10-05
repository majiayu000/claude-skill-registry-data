---
name: cleanup
description: After a PR has merged, tear down its worktree and feature branch. Verifies the PR is actually merged on GitHub, deletes the local + remote feature branch if they still exist, removes the git worktree, and switches the session back to the main worktree. Use when the user says they're done with a feature and want to clean up.
argument-hint: "[pr-number (default: PR for current branch)]"
allowed-tools: Bash, Read
---

# Cleanup

Post-merge teardown: verify PR is merged → delete feature branch (local + remote) → remove the worktree → switch back to the main worktree.

## Input

<args>
$ARGUMENTS
</args>

Optional PR number. If absent, resolve it from the current branch with `gh pr view --json number,state,headRefName,baseRefName,headRepositoryOwner,headRepository,url`.

## Step 0: Pre-flight

```bash
git rev-parse --is-inside-work-tree
git rev-parse --abbrev-ref HEAD
git status --porcelain
git worktree list
gh auth status
```

Capture for later:
- `CURRENT_BRANCH` — the branch we're on now.
- `CURRENT_WORKTREE` — the absolute path of the current worktree (from `git worktree list --porcelain`, the entry whose `worktree` line matches `pwd`).
- `MAIN_WORKTREE` — the entry from `git worktree list --porcelain` whose `branch` matches `main` (or whatever `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` reports). Fall back to the first entry in `git worktree list` if no main worktree exists.

Hard stops:

- Not a git repo / `gh` not authenticated.
- Uncommitted or untracked changes in the current worktree — ask the user. Cleanup is destructive; never blow away work-in-progress without explicit confirmation.
- We're already in the main worktree (the one tracking `main`). There's nothing to switch back *to* — confirm with the user before deleting any branch and skip the worktree-removal step.

## Step 1: Verify the PR is actually merged

```bash
gh pr view <pr> --json number,state,mergedAt,mergeCommit,headRefName,headRepositoryOwner,headRepository,baseRefName,url
```

Required: `state == "MERGED"` **and** `mergedAt` is non-null. Anything else is a hard stop:

- `OPEN` — refuse and tell the user the PR is still open.
- `CLOSED` (not merged) — refuse and ask the user whether they really want to delete the branch (the work is unmerged; deletion is destructive). Only continue if they explicitly say yes.

Also confirm the PR's head repo matches `origin` — if it's from a fork (`headRepositoryOwner.login` differs from the `origin` owner), we cannot delete the remote branch; do the local-side cleanup only and say so in the report.

## Step 2: Delete the feature branch (remote then local)

The PR's head branch name is `HEAD_REF` (`gh pr view ... -q .headRefName`).

GitHub's "automatically delete head branches" setting may have already deleted the remote ref — that's fine, treat it as success.

```bash
# Remote — only if the PR head was on origin (not a fork).
if git ls-remote --exit-code --heads origin "$HEAD_REF" >/dev/null 2>&1; then
  git push origin --delete "$HEAD_REF"
else
  echo "remote branch already gone"
fi

# Local — only delete if the branch exists AND it's been merged into origin/<base>.
# Use -d (safe), not -D (force). A failure here means the branch has unmerged
# work; refuse and surface to the user rather than forcing.
if git show-ref --verify --quiet "refs/heads/$HEAD_REF"; then
  # The branch can't be deleted while it's checked out anywhere — Step 3
  # removes the worktree first, so defer the local delete until after that.
  echo "will delete local branch $HEAD_REF after worktree removal"
fi
```

If the local branch is checked out in another worktree besides the current one, stop and tell the user — don't yank the rug out from under a parallel session.

## Step 3: Remove the current worktree (if applicable)

Only if `CURRENT_WORKTREE` is not the main worktree:

1. Switch the *session* out of the worktree first. The session has to leave before the worktree directory is deleted, otherwise the cwd vanishes mid-operation. Use the `ExitWorktree` tool with `action: "remove"` (or `"keep"` if the user wants the directory preserved — ask if unsure). `ExitWorktree` handles both `cd`-ing back to the main checkout and running `git worktree remove`.

2. If `ExitWorktree` is unavailable for any reason, fall back to manual cleanup **from the main worktree path** (never from inside the worktree being removed):

   ```bash
   cd "$MAIN_WORKTREE"
   git worktree remove "$CURRENT_WORKTREE"        # refuses if worktree is dirty
   # If the user already confirmed in Step 0 that pending changes are disposable:
   # git worktree remove --force "$CURRENT_WORKTREE"
   ```

   Never `rm -rf` the worktree directory — that leaves a stale entry in `.git/worktrees/` and corrupts `git worktree list`. Always use `git worktree remove`.

3. After the worktree is gone, finish the local branch delete from the main worktree:

   ```bash
   git branch -d "$HEAD_REF"     # safe delete; refuses if unmerged
   ```

   If `-d` refuses (branch claims to be unmerged — common when the PR was squash- or rebase-merged, since the local commits' SHAs don't appear in `main`), verify the PR is really merged (`gh pr view <pr> --json state,mergeCommit`), then it's safe to use `-D`. Mention this in the report so the user knows force-delete was used and why.

## Step 4: Pull latest main

Now in the main worktree:

```bash
git fetch origin
git checkout main   # or whatever the default branch is
git pull --ff-only origin main
```

`--ff-only` so we never accidentally create a merge commit on `main`. If the pull isn't fast-forward, stop and tell the user — something else is going on (local commits on main, a rewritten history upstream).

## Step 5: Report

```markdown
## Cleanup summary for PR #<n>

- PR state: MERGED at <mergedAt> — <url>
- Remote branch `<head-ref>`: <deleted | already gone | skipped (fork)>
- Local branch `<head-ref>`: <deleted (-d) | force-deleted (-D, squash-merge) | not present>
- Worktree: <removed <path> | skipped (already in main worktree)>
- Main branch: pulled to <short-sha>
```

## Notes

- **Never** force-delete a branch (`git branch -D`) just because `-d` refused, unless you have already confirmed via `gh pr view` that the PR is merged. The refusal exists to protect unmerged work.
- **Never** `rm -rf` a worktree directory. Use `git worktree remove` so git's bookkeeping stays consistent.
- **Never** delete `main` (or the default branch), even if the user asks — refuse and explain.
- If the user invokes cleanup from inside the worktree they want removed (the normal case), the session has to exit the worktree before the directory can be deleted. `ExitWorktree` is the safe path; manual `cd && git worktree remove` from the main worktree path is the fallback.
- If `git worktree list` shows the current worktree as `prunable` or with a missing path, run `git worktree prune` first to clean up the bookkeeping before any other operation.
