---
name: Git Version Control
description: Expert instructions for managing source control operations and commit standards.
---

# Git Version Control

This skill ensures consistent and clean version control practices.

## Core Workflow

### 1. Staging & Committing
- **Atomic Commits**: Group related changes. Avoid massive "catch-all" commits.
- **Message Format**: Use conventional commit style if possible, or clear descriptive sentences.
  - `feat: add emoji keyboard`
  - `fix: resolve crash in settings`
  - `docs: update skill usage guide`

### 2. Branching
- **Feature Branches**: `feature/your-feature-name`
- **Bugfix Branches**: `bugfix/issue-description`
- **Main Branch**: Only merge stable code into `main` (or `master`).

### 3. Merging
- **Pull**: Always pull latest changes before starting work.
- **Conflicts**: When resolving conflicts:
  1.  Identify the conflicting file.
  2.  Look for `<<<<<<<`, `=======`, `>>>>>>>` markers.
  3.  Choose the correct code block (incoming vs. current).
  4.  Remove markers and test.

## Common Operations

### Status Check
Allows seeing which files are changed/staged.
```bash
git status
```

### Viewing History
See recent changes in a compact format.
```bash
git log --oneline -n 10
```

### Discarding Local Changes
**Warning**: This is destructive.
To reset a specific file to HEAD:
```bash
git checkout -- path/to/file
```
