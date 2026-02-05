---
name: github-issue-workflow
description: Issue-first GitHub development workflow. Use when working on any GitHub repository task, feature, or bug fix. Enforces a disciplined workflow that starts with a GitHub issue, creates a linked feature branch, iterates until validated, then cleans up. Triggers on requests to fix bugs, add features, refactor code, or any development work in a git repository.
---

# GitHub Issue-First Workflow

All development work follows this strict issue-first workflow. Never start coding without an issue.

## Workflow Overview

1. **Issue First** → Create or identify GitHub issue
2. **Branch** → Create feature branch linked to issue
3. **Implement** → Make changes on feature branch
4. **Validate** → Test thoroughly until 100% working
5. **PR** → Open pull request referencing issue
6. **Merge & Cleanup** → Merge, delete branches, close issue

## Phase 1: Issue First

Before any code changes, ensure a GitHub issue exists.

**Creating a new issue:**
```bash
gh issue create --title "Brief description" --body "Detailed description of the problem or feature"
```

**Finding existing issues:**
```bash
gh issue list
gh issue view <number>
```

**Issue requirements:**
- Clear title describing the change
- Body explaining the problem/feature and acceptance criteria
- Labels if applicable (bug, enhancement, etc.)

Note the issue number (e.g., `#42`) for branch naming.

## Phase 2: Feature Branch

Create a branch that links to the issue. Branch naming convention: `<issue-number>-<short-description>`

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create and switch to feature branch
git checkout -b 42-fix-login-timeout
```

Push the branch to establish remote tracking:
```bash
git push -u origin 42-fix-login-timeout
```

## Phase 3: Implementation

Make changes on the feature branch. Commit frequently with meaningful messages referencing the issue:

```bash
git add <files>
git commit -m "Add timeout configuration option (#42)"
```

**Commit message guidelines:**
- Reference the issue number in commits
- Use present tense ("Add feature" not "Added feature")
- Keep first line under 72 characters

## Phase 4: Validation Loop

This is critical. Do not proceed until the implementation is 100% validated.

**Validation checklist:**
1. Run existing tests: `npm test`, `pytest`, `go test`, etc.
2. Add new tests covering the change
3. Manual testing of the specific functionality
4. Check for regressions
5. Lint and format code

**If validation fails:**

Add comments to the GitHub issue documenting what was tried and what failed:
```bash
gh issue comment <number> --body "Attempted X approach. Failed because Y. Trying Z next."
```

Then iterate: fix → commit → validate again.

**Continue this loop until validation passes 100%.** Do not move to PR phase with partial solutions.

## Phase 5: Pull Request

Only after validation passes, create a PR:

```bash
gh pr create --title "Fix login timeout (#42)" --body "Closes #42

## Changes
- Added configurable timeout
- Updated tests

## Testing
- All existing tests pass
- Added new timeout test"
```

**PR requirements:**
- Title references issue number
- Body includes `Closes #42` (or `Fixes #42`) for auto-closing
- Describes what changed and how it was tested

## Phase 6: Merge and Cleanup

After PR approval (or for personal repos, after self-review):

**Merge the PR:**
```bash
gh pr merge <pr-number> --squash --delete-branch
```

The `--delete-branch` flag removes the remote feature branch.

**Clean up local branch:**
```bash
git checkout main
git pull origin main
git branch -d 42-fix-login-timeout
```

**Verify issue is closed:**
```bash
gh issue view 42
```

If the issue didn't auto-close, close it manually:
```bash
gh issue close 42 --comment "Resolved in PR #<pr-number>"
```

## Quick Reference

| Phase | Key Command |
|-------|-------------|
| Create issue | `gh issue create --title "..." --body "..."` |
| Create branch | `git checkout -b <issue#>-<desc>` |
| Push branch | `git push -u origin <branch>` |
| Commit | `git commit -m "Message (#issue)"` |
| Comment on issue | `gh issue comment <#> --body "..."` |
| Create PR | `gh pr create --title "... (#issue)" --body "Closes #issue"` |
| Merge & cleanup | `gh pr merge <#> --squash --delete-branch` |
| Delete local branch | `git branch -d <branch>` |
| Close issue | `gh issue close <#>` |

## Handling Edge Cases

**Issue already exists:** Skip Phase 1, proceed to Phase 2 with existing issue number.

**Multiple issues for one change:** Create a parent issue and reference all related issues in PR body.

**Validation takes multiple sessions:** Always document progress in issue comments before stopping work.

**Need to abandon an approach:** Comment on issue explaining why, then start fresh implementation on same branch or create new branch if significant pivot.
