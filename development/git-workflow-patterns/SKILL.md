---
name: Git Workflow Patterns
description: Conventional commits, PR practices, branching strategies
---

# Git Workflow Patterns

Modern Git workflows and best practices.

## Conventional Commits

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

```
feat: New feature
fix: Bug fix
docs: Documentation only
style: Formatting, missing semi-colons, etc
refactor: Code change that neither fixes a bug nor adds a feature
perf: Performance improvement
test: Adding missing tests
chore: Updating build tasks, package manager configs, etc
ci: Changes to CI configuration
build: Changes to build system or dependencies
revert: Reverting a previous commit
```

### Examples

```bash
# Simple
git commit -m "feat: add user authentication"

# With scope
git commit -m "fix(api): handle null user IDs"

# With body
git commit -m "feat: add dark mode

Implements dark mode theme toggle with:
- System preference detection
- Manual override option
- Persisted user choice"

# Breaking change
git commit -m "feat!: redesign API endpoints

BREAKING CHANGE: /api/v1/users is now /api/v2/users"
```

## Branch Naming

```
feature/add-user-auth
fix/login-redirect-bug
refactor/simplify-api
docs/update-readme
chore/update-dependencies
```

## Pull Request Practices

### PR Title

```
feat: Add user authentication
fix: Resolve login redirect issue
docs: Update API documentation
```

### PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots
[If UI changes]

## Breaking Changes
[If applicable]

## Related Issues
Closes #123
```

### PR Size Guidelines

```
✅ Small PR: 50-200 lines (ideal)
⚠️  Medium PR: 200-400 lines (ok)
❌ Large PR: 400+ lines (split if possible)
```

## Code Review

### Reviewer Checklist

- [ ] Code follows project conventions
- [ ] Tests are included and passing
- [ ] No obvious bugs or security issues
- [ ] Documentation is updated
- [ ] PR description is clear
- [ ] Commits are logical and well-messaged

### Review Comments

```
✅ Good:
"Consider extracting this into a separate function for better testability"
"This could cause a race condition if called multiple times"

❌ Bad:
"This is wrong"
"Why did you do it this way?"
```

## Branching Strategies

### Git Flow

```
main - Production-ready code
develop - Integration branch for features
feature/* - New features
release/* - Release preparation
hotfix/* - Emergency fixes to production
```

### GitHub Flow (Simpler)

```
main - Always deployable
feature/* - All work happens in feature branches
- Create PR to merge into main
- Deploy after merge
```

## Useful Commands

### Rebase

```bash
# Update feature branch with main
git checkout feature/my-feature
git rebase main

# Interactive rebase (clean up commits)
git rebase -i HEAD~3
```

### Stash

```bash
# Save work in progress
git stash

# List stashes
git stash list

# Apply stash
git stash pop
```

### Amend Last Commit

```bash
git commit --amend
git commit --amend --no-edit
```

### Cherry Pick

```bash
git cherry-pick <commit-hash>
```

## Best Practices

✅ **Do**:
- Write clear commit messages
- Keep commits atomic (one logical change)
- Rebase feature branches before merging
- Review your own PR first
- Keep PRs small and focused
- Write descriptive PR titles
- Link PRs to issues
- Respond to review comments

❌ **Don't**:
- Commit directly to main
- Create massive PRs
- Use generic commit messages ("fix bug", "update")
- Force push to shared branches
- Merge without review
- Leave unresolved comments
