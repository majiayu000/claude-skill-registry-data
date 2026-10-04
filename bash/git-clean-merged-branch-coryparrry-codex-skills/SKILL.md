---
name: git-clean-merged-branch
description: Safely clean up a local Git branch after it has been merged on GitHub. Use when the user says short commands like "clean merged branch", "cleanup merged branch", "sort git", "clean up git", "branch merged", "merged branch cleanup", or invokes "git-clean-merged-branch"; also use for longer requests that say the branch has been merged and is no longer needed.
---

# Git Clean Merged Branch

Use this skill to return a repo to a clean local Git state after the current branch has already been merged on GitHub.

The user may intentionally use a short trigger such as:

- `clean merged branch`
- `sort git`
- `branch merged`
- `git-clean-merged-branch`

Treat those as shorthand for: fetch GitHub, update the default branch, and remove the old local branch safely.

## Core Rules

- Inspect before changing anything.
- Do not continue if the worktree has uncommitted or untracked changes.
- Prefer the repo default branch from `origin/HEAD`; fall back to `main`, then `master`.
- Use `git fetch --prune` before deciding what exists remotely.
- Use fast-forward-only pulls for the default branch.
- Delete the local branch only after switching away from it.
- Prefer safe branch deletion with `git branch -d`.
- If safe deletion fails because GitHub used squash or rebase merge, verify the merged GitHub PR and compare the branch diff against the merged PR diff before deleting the local branch with `git branch -D`.
- Use forced branch deletion without merge verification only when the user has clearly said the branch is merged or no longer needed, and after the repo is clean and the default branch is updated.
- Delete the old remote branch only after verifying the fetched remote tip is safe; use `--keep-remote` when the user explicitly asks to preserve it.
- Never run `git reset --hard`, `git clean`, or other broad destructive cleanup for this workflow.

## Recommended Workflow

1. Confirm the current directory is inside a Git repo.
2. Record the current branch name.
3. Stop if there are local changes and explain that the user needs to commit, stash, or discard them first.
4. Fetch from `origin` with pruning.
5. Resolve the default branch.
6. Switch to the default branch.
7. Pull the default branch with fast-forward-only.
8. If the starting branch was not the default branch, delete the local starting branch.
9. If normal deletion fails, let the script verify a merged GitHub PR and exact diff equality before using `git branch -D`.
10. Delete the old remote branch after local cleanup succeeds and the fetched remote tip is verified safe.
11. Show the final `git status --short --branch`.
12. Update relevant documents as when this prompt is sent, it means the end of a phase/slice.

## Script

Use `scripts/clean_merged_branch.sh` from this skill for the standard cleanup.

Run it from the repo root or any directory inside the target repo:

```bash
bash /path/to/skill/scripts/clean_merged_branch.sh
```

If the user's wording clearly says the branch is already merged or no longer needed, and safe deletion reports the branch is not merged because GitHub used squash or rebase merge, rerun with:

```bash
bash /path/to/skill/scripts/clean_merged_branch.sh --force-delete-unmerged
```

The script now verifies squash-merged branches by default before force-deleting locally. Use `--force-delete-unmerged` only when GitHub verification is unavailable or insufficient and the user has clearly accepted local branch deletion.

The script deletes the old remote branch by default after local cleanup succeeds. To preserve the old remote branch, run:

```bash
bash /path/to/skill/scripts/clean_merged_branch.sh --keep-remote
```

Do not use `--force-delete-unmerged` when the user only asks for a status check or is unsure whether the branch was merged.

## Output

Tell the user:

- which branch was cleaned up
- which default branch was updated
- whether the old local branch was deleted
- whether deletion used merge diff verification
- whether the old remote branch was deleted
- whether the final repo state is clean
- any action still needed if cleanup stopped
