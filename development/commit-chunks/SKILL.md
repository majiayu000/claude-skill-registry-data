---
name: commit-chunks
description: Review and commit changes in meaningful chunks. Use when the user has multiple uncommitted changes that should be organized into logical, atomic commits.
allowed-tools: Bash(git:*)
---

# Commit Chunks

Review and commit changes in meaningful chunks.

## Instructions

1. Run `git status` and `git diff` to see all uncommitted changes
2. Review each changed file and understand what was modified
3. Group related changes into logical commits (e.g., by feature, by file type, by purpose)
4. For each group:
   - Stage only the relevant files with `git add <files>`
   - Create a commit with a clear, descriptive message following conventional commits (feat, fix, chore, docs, refactor, style, test)
5. After all commits, show `git log --oneline -10` to display the results

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]
```

Examples:

- `feat(studio): add branding to graph controls`
- `fix(cli): resolve path issue in static file serving`
- `chore: update gitignore for docs folder`

## Guidelines

- Keep commits atomic (one logical change per commit)
- Don't mix unrelated changes in the same commit
- Write commit messages that explain WHY, not just WHAT
- If unsure about grouping, ask for clarification
