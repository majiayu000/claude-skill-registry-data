---
name: pr-review-helper
description: Create pull requests with an interactive review and approval step. Use this skill when the user asks to create a pull request, open a PR, or submit their changes for review. This skill ensures PR descriptions are reviewed before submission.
---

# PR Review Helper

## Overview

Create pull requests with an interactive review workflow that allows users to edit the PR description before submission. This skill analyzes all commits since diverging from the base branch and generates a comprehensive PR summary for user review.

## Workflow

Follow these steps sequentially when creating a pull request:

### 1. Gather Git Context

Collect all necessary git information to understand the full scope of changes:

- Current git status: `git status`
- All changes since diverging from main: `git diff main...HEAD`
- Current branch name: `git branch --show-current`
- All commits on this branch: `git log main..HEAD`
- Remote tracking status: `git status -b --porcelain | head -1`
- Check if current branch tracks a remote: `git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "No upstream tracking"`

Execute these commands in parallel for efficiency.

### 2. Analyze Changes and Draft PR Description

Based on the gathered context:

- Analyze ALL commits that will be included in the pull request (not just the latest commit)
- Review the full diff to understand the complete scope of changes
- Draft a comprehensive PR summary that includes:
  - Clear, descriptive title
  - Summary section with 1-3 bullet points covering the main changes
  - Test plan section with a bulleted markdown checklist of testing TODOs

### 3. Write Description to File for Review

Use the `write_pr_description.py` script to write the PR description to a deterministic location in `docs/prs/`:

```bash
python scripts/write_pr_description.py "PR Title" "## Summary

- Main change point 1
- Main change point 2
- Main change point 3

## Test plan

- [ ] Test item 1
- [ ] Test item 2
- [ ] Test item 3"
```

The script will:
- Create the `docs/prs/` directory if it doesn't exist
- Write the description to a timestamped file (e.g., `docs/prs/pr_20250129_143022.md`)
- Display the file path for the user to review

Inform the user where the PR description has been written and ask them to review and edit it before creating the PR.

### 4. Wait for User Approval

After writing the description file, explicitly wait for the user to indicate they have reviewed and approved the description. Do not proceed to creating the PR until the user confirms they are ready.

### 5. Create the Pull Request

Once the user approves, use the `create_pr.py` script to create the PR:

```bash
# Ensure current branch is pushed to remote with upstream tracking if needed
git push -u origin $(git branch --show-current)

# Create the PR from the most recent description file
python scripts/create_pr.py
```

Optionally, specify a particular PR description file or base branch:

```bash
# Use a specific PR description file
python scripts/create_pr.py docs/prs/pr_20250129_143022.md

# Use a different base branch
python scripts/create_pr.py docs/prs/pr_20250129_143022.md develop
```

The script will:
- Read the PR description file (uses the most recent one if not specified)
- Parse the title and body
- Create the PR using `gh pr create`
- Display the PR URL
- Clean up by deleting the PR description file

Return the PR URL to the user.

## Important Notes

- Always analyze ALL commits in the branch, not just the most recent one
- The PR description should reflect the complete scope of changes since diverging from the base branch
- Never skip the user review step - this is a critical part of the workflow
- If the user provides additional notes or context as arguments, incorporate them into the PR description
- The scripts handle file I/O and git operations deterministically, reducing errors
- PR description files are stored in `docs/prs/` with timestamps for easy tracking

## Scripts Reference

### write_pr_description.py

Creates a PR description file in `docs/prs/` with a timestamp.

**Usage:**
```bash
python scripts/write_pr_description.py <title> <body>
```

**Arguments:**
- `title`: The PR title (required)
- `body`: The PR body content with summary and test plan (required)

### create_pr.py

Creates a GitHub PR from a description file in `docs/prs/` and cleans up the file after.

**Usage:**
```bash
python scripts/create_pr.py [filepath] [base-branch]
```

**Arguments:**
- `filepath`: Path to PR description file (optional, defaults to most recent)
- `base-branch`: Base branch for the PR (optional, defaults to "main")
