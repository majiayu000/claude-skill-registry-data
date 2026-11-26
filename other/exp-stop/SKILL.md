---
name: "exp-stop"
description: "Conclude and delete an experiment branch. Shows pending work and a diffstat for a final review, then deletes the current repository's experiment branc"
---

# exp-stop command

Apply this command workflow. Treat any text after its invocation as the command input.

Conclude and delete an experiment branch. Shows pending work and a diffstat for a final review, then deletes the current repository's experiment branch, worktree, and local metadata. Handles both local-only and remote-backed (subtree-synced) experiments.

## Input

$ARGUMENTS

The argument is the experiment slug (e.g. `transformer-perf`). If no argument is given, list existing `exp/*` branches and ask the user to pick one.

## Phase 1 -- Verify and Detect Mode

1. Check that the worktree `../exp-<slug>` exists or the local branch `exp/<slug>` exists:
   ```bash
   git worktree list | grep "exp-<slug>"
   git branch --list "exp/<slug>"
   ```
   If neither exists, report that no experiment with this slug was found and stop.

2. Detect the mode: if `../exp-<slug>/.exp-sync.yaml` exists, this is a **remote-backed** experiment — read `remote_name`, `remote_url`, `upstream_branch`, `prefix`, and `push_branch` from it. Otherwise it is **local-only**.

3. Show the current state of the experiment — uncommitted changes and a diffstat against main:
   ```bash
   cd ../exp-<slug>
   git status --short
   ```
   ```bash
   git diff --stat main...exp/<slug>
   ```

4. Show the commit log for the experiment:
   ```bash
   git log --oneline main..exp/<slug>
   ```

5. **Remote-backed only** — show the subtree sync state so the user knows what has and has not crossed the boundary:
   ```bash
   cd ../exp-<slug>
   git fetch <remote_name>
   # local prefix vs the remote's upstream branch
   git diff --stat HEAD:<prefix> <remote_name>/<upstream_branch>
   # whether a push branch exists in the remote repository
   git ls-remote --heads <remote_name> <push_branch>
   ```
   Then state plainly: **deleting this experiment branch does not undo anything already pushed to `<remote_url>`.** Subtree pushes created branch `<push_branch>` in the remote repository; that content survives all local cleanup below.

6. Ask the user to confirm deletion. This is the last chance to distill keepers via `/gh-issue-push` + `/gh-issue-pop`, and (remote-backed) the last reminder to `git subtree push` any prefix changes that should reach the remote. Do not proceed without explicit confirmation.

## Phase 2 -- Delete (current repository only)

After user confirmation:

1. Delete this repository's remote branch:
   ```bash
   git push origin --delete exp/<slug>
   ```

2. Remove the worktree:
   ```bash
   git worktree remove --force ../exp-<slug>
   ```

3. Delete the local branch:
   ```bash
   git branch -D exp/<slug>
   ```

4. **Remote-backed only** — remove the sync remote from this machine's configuration:
   ```bash
   git remote remove <remote_name>
   ```

Default cleanup ends here: only the current repository's experiment branch, worktree, and local metadata are removed. **The external repository's `<push_branch>` is never deleted by default.** If — and only if — the user explicitly asks to delete it as well, confirm separately and run:

```bash
git push <remote_url> --delete <push_branch>
```

## Phase 3 -- Report

Print cleanup confirmation and instructions for other machines:

```
Experiment exp/<slug> deleted (this repo's remote branch, worktree, local branch<if remote-backed:>, sync remote</if>).
<if remote-backed:>
NOT deleted: branch <push_branch> in <remote_url> — content pushed there
survives this cleanup. Delete it manually only if you are sure.

Other machines that joined this experiment should run:
  git fetch --prune
  git worktree remove --force ../exp-<slug>
  git branch -D exp/<slug>
  git remote remove <remote_name>   # remote-backed only

Note: deletion removes the branch from lists, fetches, and fresh clones,
but commits stay SHA-addressable on GitHub until garbage collection.
GitHub Support can purge on request.
```
