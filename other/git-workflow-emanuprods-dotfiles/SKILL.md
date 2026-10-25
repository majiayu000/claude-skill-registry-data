---
name: git-workflow"
description: Git workflow automation including conventional commits, branch management, PR creation, and release tagging. Use when working with git repositories for commit, push, PR, or release tasks.
---

# Git Workflow Skill

## Conventional Commits

Format: `<type>(<scope>): <subject>`

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Formatting, no logic change
- `refactor` - Code restructuring
- `perf` - Performance improvement
- `test` - Adding tests
- `chore` - Maintenance, deps, build
- `ci` - CI/CD changes

### Examples
```bash
feat(auth): add OAuth2 login flow
fix(api): handle null response in user endpoint
refactor(db): extract query builder class
```

## Branch Strategy

```
main                    # Production releases
├── develop             # Integration branch
├── feature/*           # New features
├── fix/*               # Bug fixes
├── release/*           # Release preparation
└── hotfix/*            # Production patches
```

## Common Commands

### Start Work
```bash
git checkout develop && git pull
git checkout -b feature/your-feature-name
```

### Commit with Conventional Format
```bash
git add -A
git commit -m "feat(scope): description"
```

### Push & Create PR
```bash
git push -u origin feature/your-feature-name
gh pr create --base develop --title "feat(scope): description" --body "## Changes\n- ...\n\n## Testing\n- ..."
```

### Sync with Develop
```bash
git fetch origin
git rebase origin/develop
# resolve conflicts if any
git push --force-with-lease
```

### Release
```bash
git checkout main && git pull
git merge --no-ff release/v1.2.3
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin main --tags
```

## GitHub CLI Integration

```bash
# View PR
gh pr view 123 --json title,body,files,reviews

# Review PR
gh pr review 123 --approve --body "LGTM"

# Merge PR
gh pr merge 123 --squash --delete-branch

# List workflow runs
gh run list --workflow=ci.yml --limit=10
```

## Automation Hooks

Add to `.git/hooks/prepare-commit-msg`:
```bash
#!/bin/bash
# Auto-prefix with branch name if feature/fix branch
BRANCH=$(git symbolic-ref --short HEAD)
if [[ $BRANCH =~ ^(feature|fix|hotfix)/(.+) ]]; then
  PREFIX="${BASH_REMATCH[1]}(${BASH_REMATCH[2]}): "
  sed -i "1s/^/$PREFIX/" "$1"
fi
```

## When to Use

- Creating commits with proper format
- Managing feature branches
- Creating and reviewing PRs
- Preparing releases
- Automating git workflows