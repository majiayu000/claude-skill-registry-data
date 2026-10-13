---
name: pr-recreate
description: "Recreate a PR with clean commit history when it has too many messy commits. Use when: (1) User says 'recreate pr' or 'clean up pr history', (2) A PR has accumulated try-and-error commits and needs a fresh start, (3) User wants to squash messy history into clean logical commits."
argument-hint: "[PR_URL]"
---

# PR Recreate Command

Recreate a PR with a clean history when it has too many try-and-error commits or review comments.

**IMPORTANT: This command ALWAYS uses squash merge to discard try-and-error history and create clean, meaningful commits. Never use cherry-pick.**

## Usage

- `/pr-recreate` - Recreate PR for current branch
- `/pr-recreate <PR_URL>` - Recreate PR from specified URL

## Steps

### 1. Identify Target PR

- If PR URL provided: Extract PR information using `gh pr view <URL>`
- If no URL: Get current branch and find PR using `gh pr list --head <current-branch>`

### 2. Analyze PR Information

Extract:

- **Old branch name**
- **Base branch** (CRITICAL: Extract from `gh pr view --json baseRefName`)
- **PR title**
- **PR number**
- **Original issue reference**

**CRITICAL: ALWAYS use the exact base branch from the original PR - NEVER default to `main` or `develop`**

### 3. Determine New Branch Name

Check for existing versioned branches and generate next available version:

- `implement-foo-bar` -> `implement-foo-bar-v2` (or `-v3` if `-v2` exists)

### 4. Create New Branch

```bash
git fetch origin
git checkout -b <new-branch> origin/<base-branch>
```

### 5. Squash Merge Old Branch

```bash
git merge --squash origin/<old-branch>
```

### 6. Create Meaningful Commits

**CRITICAL: ALWAYS create MULTIPLE meaningful commits - NEVER just one commit**

- Review staged changes with `git diff --cached`
- Break down into logical units (feature, tests, docs, refactoring)
- Create separate commits for each unit
- Aim for 2-5 commits minimum

**CRITICAL - NO COMMIT ALTERATION:**

- NEVER use `git commit --amend`
- NEVER use `git rebase`
- Each commit must be created fresh

### 7. Push New Branch

```bash
git push -u origin <new-branch>
```

### 8. Create New PR

Use the EXACT base branch from step 2. Include:

- Original issue reference FIRST
- PR description
- Old PR reference LAST

### 9. Update Old PR

- Add `[outdated]` prefix to title
- Add comment referencing new PR
- Close old PR

### 10. Report Summary

- Old PR: #<number> (closed)
- New PR: #<number> (created)
- Branch: `<old-branch>` -> `<new-branch>`
- Commits created
- Base branch

## Important Notes

- **CRITICAL: ALWAYS use squash merge** to discard try-and-error history
- **CRITICAL: ALWAYS use the original PR's base branch**
- **CRITICAL: Never alter commits** (no amend, no rebase, no force push)
- **CRITICAL: Create MULTIPLE meaningful commits** (2-5 minimum)
- If the target project's CLAUDE.md defines PR conventions (e.g. Japanese titles, an AI-attribution header in the PR body/comments), follow them — otherwise use clear defaults
