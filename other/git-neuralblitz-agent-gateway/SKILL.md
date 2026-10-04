---
name: git
description: Git version control best practices and workflows
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: devops
---
## What I do
- Follow conventional commit message format
- Create effective git branches
- Manage merge requests/PRs
- Use git rebase for clean history
- Handle merge conflicts properly
- Use git stash for work-in-progress
- Write good pull request descriptions
- Follow branch naming conventions

## When to use me
When writing commit messages, creating branches, or managing git workflows.

## Commit Message Format
```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring without behavior change
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks, dependency updates

**Examples:**
```
feat(api): add user authentication endpoint

Implement JWT-based authentication for the REST API.

- Add login endpoint
- Add token refresh mechanism
- Add authentication middleware

Closes #123
```

```
fix(database): resolve connection pool exhaustion

Connection pool was not properly released on error conditions,
causing resource exhaustion under high load.

Fixes #456
```

```
docs(readme): update installation instructions

Added prerequisites section and troubleshooting guide.
```

## Branch Naming
```
feature/authentication   (new feature)
fix/login-bug           (bug fix)
docs/api-reference      (documentation)
refactor/user-service   (code refactoring)
test/payment-flow       (tests)
chore/dependencies       (maintenance)
```

## Git Workflow
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat(scope): description"

# Keep up to date with main
git fetch origin
git rebase origin/main

# Push and create PR
git push -u origin feature/my-feature

# Interactive rebase for clean history
git rebase -i HEAD~5
# Squash commits, edit messages
```

## Pull Request Guidelines
- **Title**: Clear, concise summary using conventional format
- **Description**:
  - What changed and why
  - How to test
  - Screenshots for UI changes
  - Breaking changes highlighted
- **Size**: Keep PRs small (< 400 lines)
- **Review**: Request review from relevant team members

## Undo Changes
```bash
# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (unstage changes)
git reset HEAD~1

# Undo last commit (discard all changes)
git reset --hard HEAD~1

# Revert a commit (safe for shared history)
git revert <commit-hash>

# Undo uncommitted file changes
git checkout -- <file>
git restore <file>
```
