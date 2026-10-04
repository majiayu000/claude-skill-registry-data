---
name: worktree-finish
description: Clean up after a worktree PR is merged. Use after the PR has been merged into presentation.
---

# Finish Worktree — Cleanup après merge

Follow these steps **strictly in order** to clean up after a merged PR.

The branch being cleaned is: `issue-<N>-<slug>` (passed as `$ARGUMENTS`)

## Step 1 — Verify that the PR is merged

```bash
gh pr view issue-<N>-<slug> --json state,mergedAt,number
```

If `state` is NOT `MERGED` → **stop and inform the user** that the PR is not yet merged.

## Step 2 — Find the worktree path

```bash
git worktree list
```

Confirm the path is `../KLASSCIv2-issue-<N>`.

## Step 3 — Remove the worktree

```bash
git worktree remove ../KLASSCIv2-issue-<N> --force
```

`--force` is required because the local branch hasn't been merged locally yet.

## Step 4 — Delete the local branch

Use `-D` (uppercase) because the branch was only merged on GitHub (remote merge commit):

```bash
git branch -D issue-<N>-<slug>
```

## Step 5 — Delete the remote branch

```bash
git push origin --delete issue-<N>-<slug>
```

If GitHub already auto-deleted it → ignore the error.

## Step 6 — Update presentation

```bash
git checkout presentation
git pull origin presentation
```

## Step 7 — Close the GitHub issue

```bash
gh issue close <N> --comment "Fermé via merge de la PR #<PR number>"
```

To find open issues: `gh issue list --state open`

## Step 8 — Check for related epic / next steps

```bash
gh issue view <N> --json body 2>/dev/null
```

Look for "Parent: #P" in the body. If found:

```bash
gh issue view <P> --json title,body,state
```

**Suggest next steps:**

| Situation | Suggestion |
|-----------|------------|
| Parent epic still open, more lots | "Epic #P still open. Prochaine issue : `/create-issue`" |
| Parent epic fully done | "Tous les lots terminés ! Fermer l'epic : `gh issue close <P>`" |
| No parent epic | "Cleanup terminé. Prêt pour la suite." |
| Other open issues | Show `gh issue list --state open --limit 5` |

## Step 9 — Verify

```bash
git worktree list          # must show only the main repo
git log --oneline -3       # must show the merge commit at top
git branch -a | grep issue-<N>   # must return nothing
```

Output:
```
Cleanup terminé:
  Worktree supprimé : ../KLASSCIv2-issue-<N>
  Branche supprimée : issue-<N>-<slug> (local + remote)
  Issue fermée      : #<N>
  Presentation      : à jour

Prochaine étape: [suggestion basée sur Step 8]
```

## Rules

- **Always verify that the PR is MERGED before cleaning up**
- **Always use `git worktree list` before removing** to confirm the path
- **Always use `--force` on `worktree remove`**
- **Always use `-D` (uppercase) on `branch` delete** — branch is not merged locally
- **Always return to `presentation`** at the end (never `main`, never `develop`)
- **Always delete the remote branch** with `git push origin --delete`
- **Always suggest next steps** — guide the user to the next piece of work

$ARGUMENTS
