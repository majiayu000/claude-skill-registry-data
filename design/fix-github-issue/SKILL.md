---
name: fix-github-issue
description: Load a GitHub issue, create an isolated worktree, plan the implementation, and submit a PR. Use when asked to fix, implement, or work on a GitHub issue by number. Requires the gh CLI to be authenticated.
---

# Fix GitHub Issue

Plan, implement, and submit a PR for a GitHub issue using git worktrees.

## Phase 1: Plan

### 1. Set up worktree

Before anything else, create an isolated worktree for this issue:

```bash
scripts/setup-worktree.sh $ISSUE_NUMBER
```

This will:
- Checkout main and pull latest changes
- Create a new worktree at `.worktrees/issue-$ISSUE_NUMBER`
- Create and checkout a branch `issue-$ISSUE_NUMBER`
- Change into the worktree directory

All subsequent work happens in the worktree, keeping your main repo clean.

**Note:** The script auto-adds `.worktrees/` to `.gitignore`.

### 2. Load issue context

```bash
scripts/load-issue.sh $ISSUE_NUMBER
```

Fetches issue details, comments, labels, and related PRs.

From the output, identify:
- Main objective from the issue description
- Clarifications, constraints, or scope changes from comments
- Proposed solutions or implementation hints from the author or maintainers
- Any blockers, dependencies, or related issues mentioned

### 3. Explore the codebase

Locate affected files and review current implementation. Identify integration points, dependencies, and side effects.

### 4. Create plan

Analyse the issue and produce a plan using [templates/plan.md](templates/plan.md):

- Summary, root cause analysis, implementation steps
- Testing approach, risks, complexity assessment

### 5. Confirm before implementing

Ask: "Would you like me to start working on this now?"

Wait for confirmation.

---

## Phase 2: Implement

Write the code changes as planned. Test locally.

---

## Phase 3: Submit

### 1. Commit changes

From the worktree (already on the correct branch):

```bash
git add -A
git commit -m "Brief description

Closes #$ISSUE_NUMBER"
```

### 2. Push and create PR

```bash
git push -u origin HEAD
gh pr create --title "Brief description" --body-file templates/pr-body.md
```

Or use the automated script:

```bash
scripts/create-pr.sh $ISSUE_NUMBER "Brief description"
```

### 3. Verify linking

Confirm the PR shows `Closes #N` and the issue appears in the Development sidebar.

---

## Quick Reference

| Keyword | Effect |
|---------|--------|
| `Closes #N` | Links PR and closes issue on merge |
| `Fixes #N` | Same as Closes |
| `Resolves #N` | Same as Closes |
| `Ref #N` | Links without closing |

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/setup-worktree.sh` | Pulls main, creates worktree and branch |
| `scripts/load-issue.sh` | Fetches issue details, comments, and related PRs |
| `scripts/create-pr.sh` | Commits, pushes, and opens PR |
