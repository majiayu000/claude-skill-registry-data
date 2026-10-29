---
name: cleanup-local-branches
description: "Use when cleaning up local Git branches after origin pruning. Deletes local branches whose upstream was deleted on origin (marked gone) and local branches with no origin counterpart that have been inactive for more than six months, while always protecting the current branch and the default branches. Previews every deletion before running it."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/git/general.md`
- Output must be in English
- This skill deletes **local** refs only — it never deletes, force-pushes, or modifies any branch on origin
- Never delete the currently checked-out branch
- Never delete protected branches: `main`, `master`, `develop`, `development`, `production`, `staging`, or any branch matching `release/*` or `hotfix/*`
- Always print the full deletion preview (branch, category, last commit date, integration status, planned action) **before** deleting anything
- Never rewrite history, force-push, or run `git gc` / `git reflog expire`
- Determine integration status by patch identity against the default branch (`git cherry`), so squash- and rebase-merged branches are recognized as integrated
- Never delete a `stale` branch that is not integrated into the default branch automatically — keep it and report it unless the user explicitly authorizes force deletion (its commits never reached origin and are unrecoverable)

---

## Scope
Prune dead local branches so the working copy only keeps branches that are still alive on origin or still recently active.

Two deletion categories:
- **Gone** — local branches whose upstream tracking branch was deleted on origin (e.g. the PR was merged and the origin branch removed).
- **Stale** — local branches that have **no** counterpart on origin and have not received a commit for **more than six months**.

---

## Use when
- The user asks to clean up, prune, or "pročistit" local branches that no longer exist on origin
- Local branches piled up after their pull requests were merged and the origin branches were deleted
- The repository accumulated old experiment branches that were never pushed and are no longer needed

---

## Execution

### 1. Refresh remote state
Update remote-tracking refs and prune deleted ones so the `gone` markers and origin counterparts are accurate:

```bash
git fetch --prune origin
```

If the repository has no `origin` remote, stop and report that the skill needs an `origin` remote to decide which branches are alive.

### 2. Record protected refs and the default branch
- Current branch: `git rev-parse --abbrev-ref HEAD`
- Protected set: `main`, `master`, `develop`, `development`, `production`, `staging`, plus any branch matching `release/*` or `hotfix/*`
- Default branch (the integration target used for merge detection in step 5):

```bash
git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' \
  || git remote show origin | sed -n 's/.*HEAD branch: //p'
```

Exclude the current branch and every protected branch from **both** candidate groups below.

### 3. Build candidate group A — gone upstream
List local branches whose upstream was deleted on origin:

```bash
git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads
```

A branch is a **gone** candidate when its `%(upstream:track)` value is exactly `[gone]`.

### 4. Build candidate group B — stale without origin counterpart
List local branches with their last commit time and upstream:

```bash
git for-each-ref --format='%(refname:short)|%(committerdate:unix)|%(upstream)' refs/heads
```

Compute the six-month cutoff timestamp:

```bash
date -v-6m +%s 2>/dev/null || date -d '6 months ago' +%s   # BSD/macOS first, GNU fallback
```

A branch is a **stale** candidate when **all** of the following hold:
- it has no upstream on origin — the `%(upstream)` field is empty (or does not start with `refs/remotes/origin/`), **and** `git ls-remote --heads origin <branch>` returns no rows (it genuinely does not exist on origin), and
- its `%(committerdate:unix)` is **older** than the cutoff timestamp from above.

A branch already captured in group A is not re-listed in group B.

### 5. Determine merge status
Classify each candidate by whether its work is already integrated into the default branch. Use **content-based** detection, not ref ancestry — `git branch --merged` / `git branch -d` only recognize fast-forward / merge-commit history and would report a **squash-merged or rebase-merged** branch as unmerged even though its changes already landed (the common case for a `gone` branch whose PR was squashed or rebased).

Detect integration by patch identity. Plain `git cherry` compares individual commits, which catches rebase / cherry-pick but **not** squash merges (a squash collapses many commits into one with a different patch id). To cover squash as well, synthesize a single commit holding the branch's net diff on top of the merge base and ask whether that patch already exists on the default branch:

```bash
default="origin/<default-branch>"   # the freshly-fetched remote ref, never the possibly-stale local branch
base=$(git merge-base "$default" "<branch>")
probe=$(git commit-tree "$(git rev-parse '<branch>^{tree}')" -p "$base" -m probe)
git cherry "$default" "$probe"   # one line: '- <sha>' ⇒ integrated, '+ <sha>' ⇒ not integrated
```

- **Integrated** — the probe line starts with `-`: the branch's net change is already present on the default branch (via fast-forward, merge, squash, or rebase) → safe to remove.
- **Not integrated** — the probe line starts with `+`: the branch carries changes absent from the default branch → it may hold unpushed local-only work.

`git branch -d` still refuses squash/rebase-integrated branches (it uses ref ancestry), so deletion of an integrated branch uses `git branch -D`. This is safe precisely because step 5 already proved the work is on the default branch.

### 6. Preview before deleting
Print one row per candidate with: branch name, category (`gone` / `stale`), last commit date, integration status (`integrated` / `not integrated`), and the planned action. Group rows by category. Do not delete anything before this preview is shown.

- **Interactive run:** show the preview and ask the user to confirm before deleting; for *not integrated* branches, include them only when the user authorizes discarding the unmerged commits.
- **Autonomous run** (e.g. invoked by another skill or a scheduled task):
  - **`gone` category** — delete every branch. A gone upstream means the PR lifecycle ended on origin; *integrated* branches delete cleanly, and *not integrated* ones are also removed because the branch is already gone from origin and the local ref is the lifecycle remnant. List each deletion with its integration status in the report.
  - **`stale` category** — delete only *integrated* branches; **keep** every *not integrated* branch (it never existed on origin, so its commits are local-only and unrecoverable once deleted). List the kept ones in the report with the `git branch -D <branch>` command the user can run manually.

### 7. Delete
- Use `git branch -D <branch>` for every branch cleared for deletion in step 6 — `-D` is required because `git branch -d` rejects squash/rebase-integrated branches even after step 5 proved their work is on the default branch.
- A *not integrated* branch is deleted **only** when step 6 cleared it (every `gone` branch; a `stale` branch only on explicit interactive authorization).
- Delete one branch per command so a single failure does not abort the rest; capture and report any failure.

### 8. Verify and report
Confirm the deletions with `git branch -vv` and produce the report described below.

---

## Output

- **Preview** (before deletion): candidates grouped by category with branch, last commit date, integration status (`integrated` / `not integrated`), and planned action.
- **Result** (after deletion):
  - Deleted branches grouped by category (`gone`, `stale`), each with its integration status
  - Kept branches with the reason (`protected`, `current`, `stale + not integrated — needs force`, `still on origin`, `active within six months`)
  - Any deletion that failed, with the error

Keep the report concise and in English.

---

## Done when
- Remote state was refreshed with `git fetch --prune origin`
- Both candidate groups were computed with the protected set and the current branch excluded
- The deletion preview was shown before any branch was deleted
- Integration status was computed by patch identity (`git cherry`) against the default branch
- Eligible branches were deleted (every `gone` branch; `stale` branches only when integrated, or not-integrated on explicit authorization)
- The final report lists deleted and kept branches with reasons, plus any failures

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
