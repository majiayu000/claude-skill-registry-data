---
name: rulebook-git-workflow
description: Git workflow standards including branching strategy, commit conventions, and PR guidelines. Use when creating branches, writing commit messages, preparing pull requests, or following git best practices.
version: "1.0.0"
category: core
author: "HiveLLM"
tags: ["git", "workflow", "branching", "commits", "pull-requests"]
dependencies: []
conflicts: []
---

# Git Workflow Standards

## Branch Naming

```
feature/<task-id>-<short-description>
fix/<issue-id>-<short-description>
refactor/<scope>-<description>
docs/<scope>-<description>
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Example

```
feat(auth): add JWT token validation

Implement JWT validation middleware for protected routes.

Closes #123
```

## Pull Request Guidelines

### PR Title
```
feat(scope): short description
```

### PR Description

```markdown
## Summary
Brief description of changes.

## Changes
- Change 1
- Change 2

## Testing
How this was tested.

## Checklist
- [ ] Tests pass
- [ ] Lint passes
- [ ] Documentation updated
```

## Workflow Steps

1. Create feature branch from main
2. Make commits following conventions
3. Run quality checks before push
4. Create PR with description
5. Address review feedback
6. Squash and merge
