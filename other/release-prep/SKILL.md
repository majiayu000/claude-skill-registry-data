---
name: release-prep
description: "Full release pipeline from feature branch to TestFlight. Pushes branch, creates PR, squash merges to main, then runs archive + TestFlight distribution. TRIGGER when the user says \"release this\", \"ship it\", \"release prep\", \"merge and archive\", \"get this to TestFlight\", or any request to take a feature branch through to TestFlight distribution."
allowed-tools: Read, Write, Edit, Bash(git:*), Bash(gh:*), Bash(grep:*), Bash(test:*), Bash(xcodebuild:*), Bash(cat:*), Bash(swift:*), Bash(curl:*), Bash(jq:*), Bash(sleep:*), Bash(Tools/appstore-connect:*), Bash(Tools/bump-build.sh:*), Bash(chmod:*), Bash(awk:*), Bash(mv:*), Skill
---

# Release Prep — Branch to TestFlight

Full pipeline: push branch → create PR → squash merge → archive → TestFlight.

**CRITICAL: Permission-safe execution.** Run each operation as a SEPARATE Bash tool call. Never chain commands with `&&`, `||`, or pipes.

## Current State

- Branch: !`git branch --show-current`
- Remote tracking: !`git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "no upstream (will push with -u)"`
- Uncommitted changes: !`git status --short`
- Commits since main: !`git log main..HEAD --oneline 2>&1`

## Pre-Flight Checks

Before starting, verify:
- [ ] NOT on `main` (must be on a feature/bugfix branch)
- [ ] All changes committed (clean working tree, excluding pre-existing unstaged changes)
- [ ] At least one commit ahead of main
- [ ] `docs/development-journal.md` has current session entry
- [ ] `docs/insights-log.md` has any unlogged insights

If on `main` already, skip to Step 4 (archive). If there are uncommitted changes, warn the user.

## Step 1: Push Branch

```bash
git push -u origin <branch-name>
```

If already pushed and up to date, skip.

## Step 2: Create Pull Request

Invoke `/pr` to create the PR. This delegates to the canonical skill so PR format stays consistent. Wait for the PR URL before proceeding to Step 3.

## Step 3: Squash Merge to Main

```bash
gh pr merge <PR-NUMBER> --squash --delete-branch
```

Then update local:
```bash
git checkout main
```
```bash
git pull origin main
```

Verify merge succeeded:
```bash
git log --oneline -3
```

## Step 4: Archive & Distribute

Invoke the archive skill to handle the rest:
```
/archive
```

This handles: build number bump → archive → upload → TestFlight distribution.

## Step 5: Final Report

```
Release Pipeline Complete

Git:
  Branch:    <branch-name> → main (squash merged)
  PR:        #<number> (<url>)

Build:
  Version:   <marketing-version> (build <number>)
  Status:    [from archive output]
```

## Arguments

- No arguments: full pipeline (push → PR → merge → archive → TestFlight)
- `--no-archive`: push → PR → merge only, skip archive/TestFlight
- `--pr-only`: push and create PR only, don't merge or archive

## Error Handling

- **Merge conflicts**: Stop and ask user to resolve
- **PR checks failing**: Warn user, ask whether to merge anyway
- **Archive failure**: Report error, suggest checking Xcode signing
- **Already on main**: Skip steps 1-3, go directly to archive

## Notes

- This skill orchestrates existing workflows. The archive step uses `/archive` which handles all Xcode/App Store Connect mechanics.
- Pre-existing unstaged changes (like unrelated modified files) are fine — they won't be included in the PR.
- The PR body is auto-generated from commit history, following project conventions.
