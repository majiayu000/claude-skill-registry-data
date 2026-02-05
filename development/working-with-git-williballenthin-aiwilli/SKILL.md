---
name: working-with-git
description: Git version control cheatsheet - viewing history, making commits, diffs, and descriptions
---

# Working with Git

Quick reference for common Git operations used in development workflows.

## Detecting Git

Check if the project uses Git:
```bash
test -d .git && echo "git" || echo "not git"
```

## Viewing the Log

**Show recent commits:**
```bash
git log --oneline -10
```

**Show log with graph:**
```bash
git log --oneline --graph --all -10
```

**Show specific commit:**
```bash
git log -1 <commit-sha>
```

**Find commits by message:**
```bash
git log --oneline --grep="keyword"
```

## Viewing Diffs

**See uncommitted changes:**
```bash
git diff
```

**See staged changes:**
```bash
git diff --cached
```

**Diff between commits:**
```bash
git diff <base-sha>..<head-sha>
```

**Diff stats:**
```bash
git diff --stat <base-sha>..<head-sha>
```

**Show what changed in a commit:**
```bash
git show <commit-sha>
```

## Getting Commit References

**Current commit SHA:**
```bash
git rev-parse HEAD
```

**Parent commit SHA:**
```bash
git rev-parse HEAD~1
```

**Branch's remote tracking commit:**
```bash
git rev-parse origin/main
```

**Relative references:**
- `HEAD` - current commit
- `HEAD~1` or `HEAD^` - parent commit
- `HEAD~2` - grandparent commit
- `origin/main` - remote branch tip

## Making Commits

**Stage and commit:**
```bash
git add <files>
git commit -m "commit message"
```

**Commit all tracked changes:**
```bash
git commit -am "commit message"
```

**Stage specific hunks interactively:**
```bash
git add -p
```

## Modifying Commit Descriptions

**Amend last commit message:**
```bash
git commit --amend -m "new message"
```

**Amend last commit (open editor):**
```bash
git commit --amend
```

**Change older commit messages (interactive rebase):**
```bash
git rebase -i HEAD~3
```
(Then mark commits with `reword` in the editor)

## Branch Information

**Current branch:**
```bash
git branch --show-current
```

**Check if branch tracks remote:**
```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

## Quick Status

**See working tree status:**
```bash
git status
```

**Short status:**
```bash
git status -s
```

## Common Patterns

**Get range for code review:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
echo "Reviewing: $BASE_SHA..$HEAD_SHA"
```

**Compare against main:**
```bash
git diff origin/main..HEAD
```

**See files changed:**
```bash
git diff --name-only <base>..<head>
```
