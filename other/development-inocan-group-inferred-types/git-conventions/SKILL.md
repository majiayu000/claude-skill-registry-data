---
name: git-conventions
description: Apply when committing code, creating branches, or preparing pull requests. Covers conventional commit format, branch naming, co-author attribution, and pre-commit checklist.
---

# Git Conventions

## Commit Message Format

Use conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `refactor:` - Code refactoring
- `docs:` - Documentation changes
- `style:` - Formatting changes
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

## Commit Template

```bash
git commit -m "feat: add new feature description

- Detailed change 1
- Detailed change 2

Co-authored-by: Ona <no-reply@ona.com>"
```

## Branch Naming

```bash
git checkout -b feature/your-feature-name
git checkout -b fix/bug-description
git checkout -b refactor/area-being-refactored
```

## Workflow

1. Create feature branch from main
2. Make changes with conventional commits
3. Push and create PR:
   ```bash
   git push -u origin feature/your-feature-name
   gh pr create --title "feat: your feature title" --body "Description of changes"
   ```

## Pre-commit Checklist

1. Run `git status` to see all changes
2. Run `git diff` to review modifications
3. Run `git log --oneline -5` to understand commit style
4. Only stage files relevant to current task
5. Do not commit files modified before task began unless related
6. Add co-author line

## Important Rules

- Never commit or push unless explicitly asked
- Single commit permission does not grant future permissions
- For PRs, ensure you're on a non-default branch
