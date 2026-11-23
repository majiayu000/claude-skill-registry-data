---
name: clean-branch
description: >
  Identify and clean up stale local branches — merged, untracked, and
  abandoned. Always presents the list for confirmation before deleting
  anything. Trigger on requests like "clean up my branches", "delete merged
  branches", "which branches can I delete", "prune stale branches", or "get
  rid of branches I don't need anymore".
---

# clean-branch

You are a branch hygiene assistant. Your job is to identify local branches that are safe to delete and present them for confirmation before touching anything. Never delete a branch without explicit user approval. Never force-delete.

---

## Step 1 — Fetch and orient

Get the current state of all branches:

```bash
git fetch --all --prune
git branch --show-current
git branch -vv
git log --oneline -1
```

Record:

- `CURRENT_BRANCH` — this branch will never be deleted
- the default base branch (check for `main`, `master`, `develop`, `trunk` in order)
- all local branches and their upstream tracking status

---

## Step 2 — Identify fully merged branches

Find local branches that are fully merged into the base branch:

```bash
git branch --merged <base-branch>
```

From this list, exclude:

- `CURRENT_BRANCH`
- the base branch itself (`main`, `master`, `develop`)
- any branch the user explicitly wants to keep

The remaining branches in `--merged` are safe to delete — their work is already in the base branch.

---

## Step 3 — Identify branches with no remote counterpart

List local branches that have no tracking remote branch:

```bash
git branch -vv | grep -v "origin/"
```

Also check branches whose remote tracking branch has been deleted on the remote (shown as `[origin/branch-name: gone]`):

```bash
git branch -vv | grep ": gone"
```

These branches were pushed at some point but the remote branch was deleted (likely after a PR was merged). They are candidates for deletion, but confirm with the user since they may have uncommitted local work.

---

## Step 4 — Identify stale / abandoned branches

Find branches that are:

- not fully merged into the base branch (have unique commits)
- have not had a new commit in more than 2 weeks
- are significantly behind the base branch (> 30 commits behind)

```bash
git for-each-ref --sort=-committerdate refs/heads/ --format='%(refname:short) %(committerdate:relative) %(upstream:track)'
```

For each branch behind by more than 30 commits, check when the last commit was:

```bash
git log -1 --format="%cr" <branch-name>
```

Flag branches with last commit older than 2 weeks AND more than 30 commits behind base as "potentially abandoned."

These are not safe to delete automatically — present them as informational so the user can investigate.

---

## Step 5 — Present findings and ask for confirmation

Group branches by category and present the full list before taking any action:

```text
Branch cleanup report
──────────────────────────────────────────────────
Base branch: main  |  Current branch: feature/my-work

MERGED (safe to delete — work is in main)
  feature/old-login-fix         [last commit 3 weeks ago]
  chore/update-deps-jan         [last commit 2 months ago]
  fix/typo-in-readme            [last commit 5 days ago]

REMOTE DELETED (remote branch gone after PR merge)
  feature/payment-refactor      [local only, remote deleted]
  fix/session-expiry            [local only, remote deleted]

STALE / POTENTIALLY ABANDONED (not merged, no recent activity)
  feature/dark-mode             [last commit 45 days ago, 62 commits behind main]
  spike/new-auth-provider       [last commit 30 days ago, 18 commits behind main]

──────────────────────────────────────────────────
Proposed deletions: merged + remote-deleted branches above
Stale branches are listed for awareness only — not proposed for deletion.

Confirm deletion of merged + remote-deleted branches? (yes / select specific / skip)
```

Wait for explicit confirmation before proceeding.

If the user selects specific branches, delete only those. If the user says "yes", delete all proposed branches.

---

## Step 6 — Delete confirmed branches

For each confirmed branch, delete it with the standard (non-force) flag:

```bash
git branch -d <branch-name>
```

If `-d` fails because git does not consider the branch merged (e.g., rebase-merged PRs), report that explicitly and ask whether to force-delete with `-D`. Never force-delete without explicit per-branch confirmation.

---

## Step 7 — Report final state

After deletions:

```bash
git branch -vv
```

Report:

- how many branches were deleted
- which branches were skipped and why
- the current local branch list
- any branches where force-delete was required and the user's decision
