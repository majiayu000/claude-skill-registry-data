---
name: creating-github-pull-requests
description: Use when creating a pull request on GitHub.
---

# Create Pull Request

## Overview

Create a well-structured GitHub pull request that follows project conventions: check prerequisites, analyze commits, search for contribution guidelines and PR templates, present a pre-flight summary for confirmation, create as draft, then publish on explicit approval.

## Prerequisites Check

Before proceeding, verify the following:

### 1. Check if `gh` CLI is installed

```bash
gh --version
```

If not installed, inform the user:
> The GitHub CLI (`gh`) is required but not installed. Please install it:
> - macOS: `brew install gh`
> - Other: https://cli.github.com/

### 2. Check if authenticated with GitHub

```bash
gh auth status
```

If not authenticated, guide the user to run `gh auth login`.

### 3. Verify clean working directory

```bash
git status
```

If there are uncommitted changes, ask the user whether to:
- Commit them as part of this PR
- Stash them temporarily
- Discard them (with caution)

## Gather Context

### 1. Identify the current branch

```bash
git branch --show-current
```

Ensure you're not on `main` or `master`. If so, ask the user to create or switch to a feature branch.

### 2. Find the base branch

```bash
git remote show origin | grep "HEAD branch"
```

This is typically `main` or `master`.

### 3. Analyze recent commits relevant to this PR

```bash
git log origin/main..HEAD --oneline --no-decorate
```

Review these commits to understand:
- What changes are being introduced
- The scope of the PR (single feature/fix or multiple changes)
- Whether commits should be squashed or reorganized

### 4. Review the diff

```bash
git diff origin/main..HEAD --stat
```

This shows which files changed and helps identify the type of change.

## Information Gathering

Before creating the PR, you need the following information. Check if it can be inferred from:
- Commit messages
- Branch name (e.g., `fix/issue-123`, `feature/new-login`)
- Changed files and their content

If any critical information is missing, ask the user:

### Required Information

1. **Related Issue Number**: Look for patterns like `#123`, `fixes #123`, or `closes #123` in commit messages
2. **Description**: What problem does this solve? Why were these changes made?
3. **Type of Change**: Bug fix, new feature, breaking change, refactor, cosmetic, documentation, or workflow
4. **Test Procedure**: How was this tested? What could break?

### Example clarifying question

If the issue number is not found:
> I couldn't find a related issue number in the commit messages or branch name. What GitHub issue does this PR address? (Enter the issue number, e.g., "123" or "N/A" for small fixes)

## Git Best Practices

Before creating the PR, consider these best practices:

### Commit Hygiene

1. **Atomic commits**: Each commit should represent a single logical change
2. **Clear commit messages**: Follow conventional commit format when possible
3. **No merge commits**: Prefer rebasing over merging to keep history clean

### Branch Management

1. **Rebase on latest main** (if needed):
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Squash if appropriate**: If there are many small "WIP" commits, consider interactive rebase:
   ```bash
   git rebase -i origin/main
   ```
   Only suggest this if commits appear messy and the user is comfortable with rebasing.

### Push Changes

Ensure all commits are pushed:
```bash
git push origin HEAD
```

If the branch was rebased, you may need:
```bash
git push origin HEAD --force-with-lease
```

## Search for Contribution Guidelines

**Before writing the PR, search for contribution guidelines** that may affect the PR format, required checks, or process:

```bash
# Check common locations for contribution guidelines
ls CONTRIBUTING* CONTRIBUTING.md .github/CONTRIBUTING* docs/CONTRIBUTING* 2>/dev/null
```

Also check:
- `README.md` for a "Contributing" section
- `.github/` directory for any process documents

If contribution guidelines exist, read them and adjust the PR accordingly:
- Follow any required PR title formats or prefixes
- Include any mandatory sections or sign-offs
- Respect branch naming conventions or review requirements
- **Extract every checklist item** from the guidelines (e.g. "run tests", "run formatter", "update CHANGELOG") and record each one — you will report all of them in the pre-flight summary, regardless of whether they are obligatory

If no guidelines are found, proceed with standard conventions.

## Create the Pull Request

**IMPORTANT**: Read and use the PR template at one of the supported paths (Filenames are not case sensitive and can also use other extensions like .txt): `pull_request_template.md`, `.github/pull_request_template.md`, `docs/pull_request_template.md`.
The PR body format must **strictly match** the template structure. Do not deviate from the template format.

When filling out the template:
- Replace `#XXXX` with the actual issue number, or keep as `#XXXX` if no issue exists (for small fixes)
- Fill in all sections with relevant information gathered from commits and context
- Mark the appropriate "Type of Change" checkbox(es)
- Complete the "Pre-flight Checklist" items that apply

### Pre-flight Summary and Confirmation

Before creating the draft PR, present a summary of everything that was checked and the proposed PR, then ask for confirmation:

> **Ready to open a draft PR — here's what I checked:**
>
> - **Branch:** `feature/my-branch` → `main`
> - **Commits:** 3 commits ahead of main
> - **Contribution guidelines:** Found / Not found
>   - ✅ Run `cargo fmt` — done
>   - ✅ Run `cargo clippy` — done
>   - ❌ Update CHANGELOG — not done
>   - ❓ All tests pass — not verified
>   *(list **every** checklist item extracted from the guidelines, none omitted; use ✅ verified/done, ❌ not done, ❓ not verified)*
> - **PR template:** Found at `.github/pull_request_template.md` / Not found
> - **Related issue:** #123 / None
>
> **Proposed PR:**
> - **Title:** "feat: add foo bar"
> - **Type:** Bug fix / Feature / etc.
>
> Shall I open this as a draft PR?

If any items are marked ❓ (not verified), offer to run them before opening the PR. For example:

> Some checks haven't been verified yet. Shall I run them now?
> - `cargo test` (all tests pass)
> - `cargo clippy -- -D warnings` (no warnings)

Wait for the user to confirm which checks to run (if any) before proceeding to create the PR.

### Create PR as Draft

**Always create the PR as a draft first.** Use a temporary file for the PR body to avoid shell escaping issues:

1. Create a temporary file and write the PR body to it:
   ```bash
   PR_BODY=$(mktemp)
   ```

2. Create the PR as a draft against the base branch from step 2:
   ```bash
   gh pr create --title "PR_TITLE" --body-file "$PR_BODY" --base BASE_BRANCH --draft
   ```

3. Clean up the temporary file:
   ```bash
   rm "$PR_BODY"
   ```

**Why use a file?** Passing complex markdown with newlines, special characters, and checkboxes directly via `--body` is error-prone. The `--body-file` flag handles all content reliably.

## Review and Publish

After creating the draft PR:

1. **Share the PR link prominently** in your response so the user can open it and review it on GitHub.
2. **Ask the user to review it** and confirm before publishing:

   > The draft PR is ready: [PR URL]
   > Please review it on GitHub. Would you like me to publish it when you're ready, or would you like any changes first?

3. **Wait for explicit confirmation** before publishing. When the user confirms, mark it as ready for review:
   ```bash
   gh pr ready PR_NUMBER
   ```

## Error Handling

### Common Issues

1. **No commits ahead of main**: The branch has no changes to submit
   - Ask if the user meant to work on a different branch

2. **Branch not pushed**: Remote doesn't have the branch
   - Push the branch first: `git push -u origin HEAD`

3. **PR already exists**: A PR for this branch already exists
   - Show the existing PR: `gh pr view`
   - Ask if they want to update it instead

4. **Merge conflicts**: Branch conflicts with base
   - Guide user through resolving conflicts or rebasing

## Summary Checklist

Before finalizing, ensure:
- [ ] `gh` CLI is installed and authenticated
- [ ] Contribution guidelines searched and followed (CONTRIBUTING.md, README contributing section, .github/)
- [ ] Working directory is clean
- [ ] All commits are pushed
- [ ] Branch is up-to-date with base branch
- [ ] Related issue number is identified, or placeholder is used
- [ ] PR description follows the template exactly
- [ ] Appropriate type of change is selected
- [ ] Pre-flight checklist items are addressed
