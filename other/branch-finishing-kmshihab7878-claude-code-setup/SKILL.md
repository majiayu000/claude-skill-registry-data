---
name: Branch Finishing
description: Guidance for verifying, presenting finish options, and closing feature branches safely.
---

# Branch Finishing

> Tests pass. Base determined. Options presented. Clean finish.

## Triggers

- Feature implementation is complete and verified
- User says "finish this branch", "merge this", "create a PR", "we're done"
- After `verification-before-completion` confirms the work is done
- After `executing-plans` Phase 3 completes

## HARD GATE: Pre-Finish Verification

Before presenting finish options, ALL of these must be true:

1. **Tests pass**: Full test suite runs green
2. **No uncommitted changes**: Working tree is clean (or changes are staged)
3. **Branch is not main/master**: You're on a feature/fix branch
4. **Verification evidence exists**: The work has been verified per `verification-before-completion`

If any condition fails, resolve it before proceeding.

## 4-Option Branch Finishing

After pre-flight checks pass, present exactly these 4 options:

### Option 1: Merge to Base Branch
```
Best for: Completed features ready for integration
Steps:
  1. Determine base branch (main/master/develop)
  2. Rebase onto latest base: git fetch origin && git rebase origin/<base>
  3. Resolve any conflicts
  4. Fast-forward merge: git checkout <base> && git merge --ff-only <branch>
  5. Delete feature branch: git branch -d <branch>
```

### Option 2: Create Pull Request
```
Best for: Team review required, CI/CD validation needed
Steps:
  1. Push branch to remote: git push -u origin <branch>
  2. Create PR with gh CLI:
     gh pr create --title "<concise title>" --body "<summary + test plan>"
  3. Return PR URL to user
  4. Do NOT delete branch (PR lifecycle manages it)
```

### Option 3: Squash and Merge
```
Best for: Many small commits that should be one logical change
Steps:
  1. Determine base branch
  2. Interactive rebase to squash: git rebase -i origin/<base>
     (or: git reset --soft origin/<base> && git commit)
  3. Write comprehensive commit message
  4. Fast-forward merge to base
  5. Delete feature branch
```

### Option 4: Discard Branch
```
Best for: Spike/experiment that won't be merged
Steps:
  1. CONFIRM with user: "This will delete all work on this branch. Proceed?"
  2. Switch to base: git checkout <base>
  3. Delete branch: git branch -D <branch>
  4. Clean up remote if pushed: git push origin --delete <branch>
```

## Base Branch Detection

Determine the base branch automatically:

```bash
# Check for common base branches
git branch -a | grep -E '(main|master|develop)' | head -1

# Or check the branch this was created from
git log --oneline --first-parent <branch> ^main | tail -1
```

Priority: `main` > `master` > `develop` > ask user.

## Integration

- Pre-finish checks use `verification-before-completion`
- PR creation follows `/pr-prep` command patterns
- Merge conflicts trigger `/debug` skill for resolution
- Worktree cleanup follows `git-worktrees` skill
