---
name: ss-cleanup
description: Use after development work is finished to confirm the PR/MR is merged (offering to merge it if not), return to the main checkout on an up-to-date default branch, remove the development branch's worktree, and delete the spent branch — both locally and, optionally, on the remote. Exits immediately with nothing to do if there's no development branch or worktree to clean up.
---

# Cleanup After Development

Wrap up finished work: confirm the PR/MR is merged (offer to merge it if it's still open), return to the main checkout on the up-to-date default branch, remove the development branch's worktree if it has one, and delete the spent branch locally and, optionally, on the remote.

**Core principle:** never delete a branch whose work isn't safely landed. A branch is only safe to delete once its PR/MR is merged, or the user explicitly confirms abandoning unmerged work. The same applies to a dirty worktree — uncommitted changes are only discarded after explicit confirmation.

## Inputs

- `--merge`: if the branch's PR/MR is open/draft, merge it without asking first.
- `--delete-remote`: also delete the remote branch if it still exists after the merge.
- `--force`: skip confirmation before discarding a dirty worktree or deleting an unmerged branch.

## Step 0 — Fast exit: nothing to clean up

```bash
git fetch origin --prune
CURRENT=$(git branch --show-current)
BASE=$(git remote show origin | grep 'HEAD branch' | awk '{print $NF}')
```

- Detached HEAD (`CURRENT` empty) → stop, report the detached state and ask what to do.
- `CURRENT` already equals `BASE` → there's no development branch to clean up. This is the common case for **lite**-mode work that never left the default branch. Just run `git pull --ff-only origin $BASE` to refresh, report, and exit — no further steps needed.

## Step 1 — Detect the PR/MR state

Use the same remote-detection logic as the `ss-create-pr` skill (inspect `git remote get-url origin` for `github.com` vs. `gitlab.com`) to pick the right CLI:

```bash
# GitHub
gh pr list --head "$CURRENT" --state all
gh pr view "$CURRENT"

# GitLab
glab mr list --source-branch "$CURRENT" --state all
glab mr view "$CURRENT"
```

Classify the result:

| State | Meaning | Next step |
|-------|---------|-----------|
| Merged | Already merged | Step 3 (safe to delete) |
| Open / draft | Exists, not merged | Step 2 |
| Closed without merging | — | Step 2 (treat as unmerged) |
| None found | No PR/MR was ever opened | Step 2 (treat as unmerged) |

If the forge CLI is missing or unauthenticated, say so and ask the user directly whether the branch's work has been merged — don't guess.

## Step 2 — Handle an unmerged branch

The work isn't safely landed yet. Tailor the question to the state:

- **Open/draft:** with `--merge`, skip the question and merge directly; otherwise ask "This PR/MR isn't merged yet — merge it now?"
  - **Yes** (or `--merge`) → mark it ready if it was a draft, then merge with the remote branch removed as part of the merge, then go to Step 3. If the merge fails (CI not green, conflicts, missing approvals, no permission), report the exact reason and stop — do not delete the branch.
  - **No** → don't delete the branch or its worktree. Offer to just return to the main checkout (Steps 3–4 without removal), or stop entirely.
- **No PR/MR, or closed without merging:** `--merge` doesn't apply — there's nothing to merge; say so if it was passed anyway. Warn that deleting now discards unmerged commits. Only proceed if the user passes `--force` or explicitly confirms abandoning the work.

## Step 3 — Locate the main checkout and the branch's worktree

```bash
# The first entry of `git worktree list --porcelain` is always the main checkout.
# Take the whole remainder of the line, not a fixed field — paths may contain spaces.
MAIN_WT=$(git worktree list --porcelain | awk '/^worktree /{sub(/^worktree /,""); print; exit}')
git worktree list --porcelain   # find the entry whose branch matches refs/heads/$CURRENT
```

If the session is currently inside the development branch's worktree, switch back to `$MAIN_WT` first (use a native worktree-exit tool if available, otherwise `cd`). If the branch was developed in place (no dedicated worktree), skip Step 5.

## Step 4 — Switch the main checkout to the default branch

Run inside `$MAIN_WT`:

```bash
git status --porcelain
git checkout "$BASE"        # only if not already on it
git pull --ff-only origin "$BASE"
```

- If the main checkout is dirty, don't switch silently — report the dirty files and ask whether to discard them, handle them first, or skip the checkout. Exception: if the only dirty file is a `.gitignore` line adding `.worktrees/` (left uncommitted by `ss-create-branch`), it's harmless — note it and continue.
- If `git checkout "$BASE"` itself fails due to conflicting local changes, report the files and stop — never force or stash without asking.
- If `--ff-only` fails because the local `$BASE` has diverged, report it and let the user reconcile — never force.

## Step 5 — Remove the development branch's worktree

This must happen before deleting the branch — git refuses to delete a branch checked out in a worktree.

If the project uses git submodules inside its worktrees, a plain worktree removal will refuse with a "working trees containing submodules cannot be removed" error even on an otherwise clean worktree. That refusal alone doesn't mean anything would be lost — check first:

```bash
git -C <path-to-branch-worktree> status --porcelain --ignore-submodules=none
```

- **Empty output** (clean, blocked only by submodule presence) → remove it directly, no confirmation needed:
  ```bash
  git worktree remove --force <path>
  git worktree prune
  ```
- **Non-empty output** (real uncommitted changes, including inside a submodule) → explicit confirmation required (skipped by `--force`): "There are uncommitted changes in this worktree — removing it will discard them. Confirm?" List the dirty files, including submodule-internal ones — a forced removal discards them silently otherwise. If the user declines, keep the worktree and the branch, report, and stop.
- **Other branches' worktrees**, enumerated from `git worktree list --porcelain` (not by globbing a fixed directory — worktrees created by a native tool may live elsewhere), excluding `$MAIN_WT` and the one just removed → leave them untouched; list them in the final report as candidates for their own cleanup pass.

## Step 6 — Delete the development branch

```bash
git branch -d "$CURRENT"   # -d only deletes if merged — safe by default
```

If that refuses ("not fully merged") and the user already confirmed abandoning the work (or passed `--force`), use `git branch -D "$CURRENT"`; otherwise keep the branch and report why.

For the remote branch: a merge that removed the source branch already deleted it — verify with `git ls-remote --exit-code origin "$CURRENT"`. If it's still there and the user passed `--delete-remote` (or confirms), delete it with `git push origin --delete "$CURRENT"`.

## Step 7 — Report

Summarize: the PR/MR's final state (merged just now / already merged / left open / none), the current location (main checkout on `$BASE`, up to date), whether the worktree was removed (path, or "no worktree — developed in place"), whether the local/remote branch was deleted, and any other worktrees left in place for the user to clean up separately.

## Examples

```
Clean up
Clean up and merge the open PR first
Clean up and also delete the remote branch
Clean up, force — discard the dirty worktree and delete the unmerged branch
```
