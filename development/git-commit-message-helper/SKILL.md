---
name: Git Commit Message Helper
description: Generate conventional commit messages following best practices. Use when user is committing code, needs commit message help, or says "commit" or "create commit". Provides consistent commit formatting across projects.
allowed-tools: Read, Grep
version: 1.0.0
---

# Git Commit Message Helper

## Purpose
Generate conventional commit messages following industry best practices and project standards.

## When This Activates
- User says "commit", "create commit message", "git commit"
- User requests commit message help
- User staging changes for commit

## Steps

### Step 1: Analyze Changes
- Use Grep to examine staged changes
- Identify type of change (feat, fix, docs, style, refactor, test, chore)

### Step 2: Generate Message
Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Step 3: Present to User
Show generated message, allow modifications

---

## Commit Types
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Tests
- chore: Maintenance

---

## Changelog
### Version 1.0.0 (2025-10-20)
- Initial release

---

**End of Skill**
