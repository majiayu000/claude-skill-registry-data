---
name: executing-development-issues
description: Complete development lifecycle for GitHub/local issues - branch, implement, test, PR, merge with quality gates
---

# Executing Development Issues

## Purpose

Complete workflow: branch → code → tests → PR → merge. Works for GitHub and local issues (ISSUES.LOCAL/).

**Core principle:** One issue at a time, full lifecycle before next.

## Uses

**Standard Interface:** aug-just/justfile-interface (Level 0+1)

```bash
just test-watch  # Continuous testing
just check-all   # Quality gate before merge
```

## Quick Reference

```bash
# 1. Get issue
gh issue view [NUMBER]              # GitHub
cat ISSUES.LOCAL/LOCAL###-Title.md  # Local

# 2. Branch (if not in worktree)
git checkout -b [ISSUE_ID]-description

# 3. Implement with TDD
just test-watch

# 4. Quality gate
just check-all

# 5. PR (GitHub only)
gh pr create --draft
gh pr ready

# 6. Merge
gh pr merge --squash --delete-branch  # GitHub
git merge --squash BRANCH            # Local
```

## Worktree vs Main

**Check:**
```bash
git rev-parse --git-dir  # .git = main, worktrees/name = worktree
```

**In worktree:** Already on feature branch, work normally
**Not in worktree:** `git checkout -b [ISSUE_ID]-description`

## Branch Naming

- GitHub: `42-add-user-auth`
- Local: `LOCAL001-fix-parser`

## Implementation

**1. Read acceptance criteria**
- Understand "done"
- Note all requirements
- Identify edge cases

**2. TDD cycle**
- Write test
- Implement
- Refactor while green
- Commit frequently

**3. Commit messages**
```bash
git commit -m "feat: specific change

Refs #42"
```

**4. Draft PR early (GitHub)**
```bash
gh pr create --draft --title "feat: description" --body "Closes #42"
```

## Definition of Done

- ✅ All acceptance criteria met
- ✅ Tests written and passing
- ✅ Coverage >= 96%
- ✅ `just check-all` passes
- ✅ Documentation updated
- ✅ Self-review completed (self-reviewing-code skill)
- ✅ Merged to main
- ✅ Issue closed

## Merging

**GitHub:**
```bash
gh pr ready
gh pr merge --squash --delete-branch
```

**Local:**
```bash
sed -i '' 's/^status: ready$/status: closed/' ISSUES.LOCAL/LOCAL###-Title.md
git checkout main
git merge --squash BRANCH
git commit -m "feat: description

Closes LOCAL###"
git branch -d BRANCH
```
