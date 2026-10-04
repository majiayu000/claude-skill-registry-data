---
name: unstick-pr
description: Recover a PR whose head SHA disagrees with its branch ref (webhook desync). Force-push and close+reopen rarely fix it — recreate the PR.
triggers:
  - unstick pr
  - webhook desync
  - pr head stuck
  - pr conflicting but local clean
---

# unstick-pr

Symptom: `gh pr view N --json headRefOid` returns a SHA that disagrees with `git ls-remote origin <branch>`. The PR shows `CONFLICTING/DIRTY` even when local `git merge-tree` is clean.

Force-push, `gh pr update-branch`, close+reopen, empty-commit nudge: each may fail. The robust fix is to recreate the PR.

## Steps

```bash
PR=N; REPO=owner/repo
HEAD_BRANCH=$(gh pr view $PR -R $REPO --json headRefName -q .headRefName)
BASE_BRANCH=$(gh pr view $PR -R $REPO --json baseRefName -q .baseRefName)

# 1. Diagnose — confirm desync
PR_HEAD=$(gh pr view $PR -R $REPO --json headRefOid -q .headRefOid)
BR_HEAD=$(git ls-remote origin "refs/heads/$HEAD_BRANCH" | cut -f1)
[ "$PR_HEAD" = "$BR_HEAD" ] && { echo "ABORT: not a desync"; exit 1; }
echo "Desync confirmed: PR=$PR_HEAD branch=$BR_HEAD"

# 2. Preserve PR metadata
TITLE=$(gh pr view $PR -R $REPO --json title -q .title)
BODY=$(gh pr view $PR -R $REPO --json body -q .body)

# 3. Close old PR with note
gh pr close $PR -R $REPO -c "Closing — webhook desync on head SHA. Recreating as fresh PR from same branch."

# 4. Open fresh PR
gh pr create -R $REPO \
  --base "$BASE_BRANCH" \
  --head "$HEAD_BRANCH" \
  --title "$TITLE" \
  --body "$BODY"$'\n\n_Recreated from #'$PR' (webhook desync)._'
```

## Validation

- New PR's `headRefOid` matches `git ls-remote origin <branch>`
- New PR `mergeStateStatus` is not `DIRTY` (give 30s for GH to compute)

## When NOT to use

- PR has CodeRabbit / reviewer threads you'd lose — comment first, ask reviewer to re-review
- PR has approval you need to preserve — closing loses approval state; the trade-off is usually still worth it but call it out

## Anti-pattern

Don't iterate: force-push → wait → empty-commit → wait → close+reopen → wait. If two SHAs disagree after the first re-push, jump straight to recreation. The webhook is not coming back without it.
