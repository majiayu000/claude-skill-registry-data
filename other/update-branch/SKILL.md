---
name: update-branch
description: >
  Brings a branch up to date with its base branch, usually main. It rebases onto origin/<base>, or
  merges when the user agrees, then builds, runs the relevant tests, and asks before it pushes. It
  never uses a plain --force, and it never disturbs uncommitted work: a clone on another branch gets
  a separate git worktree. This skill is user-only: it runs only when the user invokes
  /update-branch [branch] [--base <branch>] [merge]. When the user wants to update a branch with
  main, rebase onto main, or fix "branch is behind main", suggest this command.
argument-hint: "[branch] [--base <branch>] [merge]"
disable-model-invocation: true
---

# Update Branch

A rebase rewrites published history, so every step that can lose work has a check in front of it. The branch defaults to the current branch, and the base defaults to `origin/HEAD`. The word `merge` asks for a merge.

## Step 1: Pick the workspace

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(readlink -f "<skill_dir>/SKILL.md")")")}"
python3 "$PLUGIN_ROOT/scripts/prepare_update_workspace.py" [--branch <branch>] [--base <base>]
```

The helper fetches, then prints `MODE:`, `BASE:`, and `WORKSPACE_PATH:`. Run every later command in that path, with `git -C <workspace_path>` for git. On `STOP: <reason>`, show the reason and stop. **Never** stash, reset, or discard work to get past a refusal.

## Step 2: Protect the remote commits

Record `origin/<branch>` as the lease for Step 6. A branch with no remote ref was never pushed, so skip the rest of this step.

A rebase and a forced push delete the commits in `<branch>..origin/<branch>` from the remote. If the local branch has nothing of its own past `origin/<branch>`, fast-forward to it. Otherwise the two diverged, so show both sides and ask.

## Step 3: Choose rebase or merge

Rebase by default. When one of these is true, propose a merge and wait for the answer:

- `<BASE>..origin/<branch>` holds commits by another author than `git config user.email`.
- The repository docs ask for merge commits.
- The user asked for a merge.

**Never** switch strategy without consent.

## Step 4: Update the branch

Read the conflict conventions in the repository docs before you resolve a conflict. Keep the intent of both sides, and read the base commit that touched the same lines. Record each resolution for the report, including any edit outside the conflict markers.

If the right answer to a conflict is not clear from the code, stop and ask. If the same lines conflict in commit after commit, abort the rebase and offer a merge.

## Step 5: Build and test

Build the projects in `git diff --name-only <BASE>...HEAD`, and run their unit and integration tests. When a shared library changed, also test its dependents. Take the commands from the repository docs and build files. If you find none, ask.

## Step 6: Report, ask, push

Report the strategy, the new base commit, each conflict resolution, and the build and test results. If anything fails, stop there.

**Always** ask before the push, and show the exact command. After a rebase:

```bash
git -C <workspace_path> push --force-with-lease=<branch>:<lease> origin <branch>
```

If the lease fails, stop and report it. Do not retry with a new lease. After a merge, use a plain `git push`, with `-u` for a branch that was never pushed. **Never** use `--force`, `-f`, or a `+<refspec>`.

## Step 7: Clean up

Only `MODE: worktree` belongs to this run. After a successful push, remove it with the helper, never with `git worktree remove`:

```bash
python3 "$PLUGIN_ROOT/scripts/prepare_update_workspace.py" --remove <workspace_path>
```

Git removes a clean worktree with unpushed commits. The helper refuses it. If the helper prints `STOP:` or the user declined the push, keep the worktree and give the user its path.
