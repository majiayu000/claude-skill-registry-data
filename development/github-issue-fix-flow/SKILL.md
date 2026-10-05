---
name: github-issue-fix-flow
description: Use when asked to take a GitHub issue number, implement a fix, run builds/tests, commit with a closing message, and push. End-to-end workflow using gh CLI, local code changes, and git.
---

# GitHub Issue Fix Flow

## Overview

Resolve a GitHub issue from intake through fix, validation, and push using gh CLI, local edits, and git.

## Workflow

### 1) Intake and Issue Context

Get full issue context:
```bash
gh issue view <id> --comments
```

If repo is unclear:
```bash
gh repo view --json nameWithOwner
```

Capture from the issue:
- Reproduction steps
- Expected behavior
- Maintainer notes or labels
- Related issues or PRs

### 2) Locate the Code Path

Search for relevant code:
```bash
# Find files related to the issue
rg -n "keyword from issue"

# Find function definitions
rg -n "func relevantFunction"

# Find type definitions
rg -n "struct|class|enum RelevantType"
```

Read relevant code paths and understand:
- Entry points
- Data flow
- Existing patterns and conventions

### 3) Implement the Fix

Guidelines:
- Edit the minimal set of files
- Keep changes aligned with existing architecture and style
- Add tests when behavior changes and coverage is practical
- Follow repo-specific conventions (check CONTRIBUTING.md, AGENTS.md, CLAUDE.md)

### 4) Build and Test

For Swift/Xcode projects:
```bash
# Build
swift build
# or
xcodebuild -scheme MyApp -destination 'platform=macOS' build

# Test
swift test
# or
xcodebuild -scheme MyAppTests -destination 'platform=macOS' test
```

For other projects, use appropriate build/test commands.

Report warnings or failures - do not hide them.

### 5) Commit and Push

Check for unrelated changes:
```bash
git status --short
git diff
```

Stage only the fix:
```bash
git add <specific files>
```

Commit with closing message:
```bash
git commit -m "Fix: <description>

Closes #<issue number>"
```

Push:
```bash
git push
```

### 6) Report Back

Provide summary:
- What changed and where
- Test results (including any failures)
- Follow-ups or blocked items

## Quick Reference

| Task | Command |
|------|---------|
| View issue | `gh issue view <id> --comments` |
| List issues | `gh issue list` |
| View repo | `gh repo view --json nameWithOwner` |
| Create branch | `git checkout -b fix/issue-<id>` |
| Stage files | `git add <files>` |
| Commit | `git commit -m "Fix: ... Closes #<id>"` |
| Push | `git push -u origin HEAD` |
| Create PR | `gh pr create --fill` |

## Commit Message Format

```
Fix: Brief description of the fix

More detailed explanation if needed.
- What was the problem
- How it was fixed
- Any notable changes

Closes #123
```

## Branch Naming

```bash
# Feature
git checkout -b feature/issue-123-add-feature

# Bug fix
git checkout -b fix/issue-123-fix-bug

# Refactor
git checkout -b refactor/issue-123-cleanup
```

## PR Workflow (Optional)

If working on a branch for PR:

```bash
# Create branch
git checkout -b fix/issue-<id>

# Make changes, commit
git add .
git commit -m "Fix: description (closes #<id>)"

# Push and create PR
git push -u origin HEAD
gh pr create --fill
```

## Checklist

- [ ] Issue context captured (repro steps, expected behavior)
- [ ] Code path located and understood
- [ ] Fix implemented with minimal changes
- [ ] Tests added/updated if applicable
- [ ] Build passes
- [ ] Tests pass
- [ ] Only relevant files staged
- [ ] Commit message includes `Closes #<id>`
- [ ] Changes pushed
- [ ] Summary provided
