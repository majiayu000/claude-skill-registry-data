---
name: pr
description: Create a pull request from the current branch. Triggers on create PR/open PR/make PR/submit PR/push PR/raise PR/open a pull request/create a pull request/ready to merge/branch is ready when the user wants to turn their current branch into a GitHub pull request with a well-structured description
---

# Pull Request

Create a pull request from the current branch with a well-structured description derived from commits and diffs.

## Step 1: Read Local Repo Conventions

Before doing anything, check for repo-specific instructions that override the defaults below:

```bash
# Check for conventions in order of priority
cat CLAUDE.md 2>/dev/null || cat AGENTS.md 2>/dev/null || cat .github/CONTRIBUTING.md 2>/dev/null
```

Look for:

- Branch naming rules
- PR title format
- Required PR template sections
- Base branch (default: `main`)
- Ticket/issue reference format

## Step 2: Verify Branch

```bash
git branch --show-current
git status
git log main..HEAD --oneline
```

- Confirm there are commits ahead of the base branch
- If on `main` directly, stop and ask the user to create a feature branch first
- Branch prefix should match the change type: `feat/`, `fix/`, `chore/`, `ci/`, `docs/`, `test/`, `refactor/`
- Use `no-jira/` or `no-ticket/` when there is no associated issue

## Step 3: Push Branch

```bash
git push origin <branch_name>
```

Always use the explicit branch name (not `HEAD`).

## Step 4: Build PR Title

Use Conventional Commits format — **NO scopes in parentheses**. CI rejects
`feat(scope):`, only `feat:` is valid.

```
<type>: <description>
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`, `ci`

## Step 5: Build PR Description

### If the repo has a PR template

Read it and replace all placeholder text with content derived from commits and diffs:

```bash
cat .github/pull_request_template.md
```

Fill in every section. Leave any screenshots/video section for the author to populate.

### If there is no PR template

Use this structure:

```markdown
## Background

- {Why this change is needed}

## What Has Changed

- {What this PR introduces or modifies}

## Screenshots/Video

- {Leave for author}

## Checklist

- [ ] Self-review completed
- [ ] Tests added or updated
- [ ] Tested locally

## Reference Issue

- Closes #{issue-number} ← only include if there is an associated issue
```

### Checklist rules

- Leave all checklist items **unchecked** — never check boxes on the author's behalf

### Reference Issue rules

- If the branch name contains a ticket/issue number, include a closing reference
- If there is no ticket, omit the section entirely

## Step 6: Create the PR

```bash
gh pr create \
  --title "<title>" \
  --body "<description>" \

```

After creating the PR, **do not perform any additional commits**.

## Step 7: Return the PR URL

Share the URL so the user can review it immediately.
