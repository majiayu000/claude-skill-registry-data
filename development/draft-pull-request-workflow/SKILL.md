---
name: Draft Pull Request Workflow
description: This skill should be used when the user requests to create a pull request from the current branch (e.g., "create PR", "draft PR", "open PR"). Provides workflow guidance for creating well-structured Draft PRs using GitHub CLI.
---

# Draft Pull Request Workflow

This skill provides procedural knowledge for creating well-structured Draft Pull Requests with clear titles and motivation-focused descriptions using GitHub CLI (`gh`).

## Safety Constraints

- Never modify git config
- Never open browser (`--web` flag prohibited)
- Never force-push or rebase (unless explicitly requested)
- Never create a PR if no diffs exist between head and base
- Never include secrets or sensitive data in PR description

## Input Parameters

Optional parameters that may be provided:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `base` | Target base branch | Repository default branch |
| `reviewers` | GitHub handles (comma-separated) | None |
| `assignees` | GitHub handles (comma-separated) | None |
| `labels` | Labels (comma-separated) | None |
| `project` | Project name or ID | None |
| `milestone` | Milestone name | None |
| `title` | Explicit PR title | Agent drafts |
| `body` | Explicit PR body | Agent drafts |

## Procedure

### 1. Validate Context

```bash
# Check current branch and status
git rev-parse --abbrev-ref HEAD
git status -sb

# Check for existing PRs from this branch
gh pr list --limit 5 --head $(git rev-parse --abbrev-ref HEAD)
```

**Stop conditions:**
- Open PR already exists → Ask whether to update instead
- No commits ahead of base branch → Report "nothing to propose" and stop

### 2. Determine Base Branch

```bash
# If base not provided, get default branch
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```

### 3. Run Quality Gates

Execute repository-standard validations:

```bash
# Examples (adjust to repository):
pnpm lint
pnpm test
pnpm build
# or: npm run lint && npm run test
# or: make check
```

**Stop condition:** Any validation fails → Report outcomes and stop (do not create PR)

### 4. Draft PR Title and Body

#### Title Guidelines

- Semantic format: `<type>(<scope>): <subject>`
- Maximum 72 characters
- Focus on "why" + "what"
- No trailing period

#### Body Guidelines

- Read repository's `.github/pull_request_template.md` if it exists
- If no repository template exists, use [templates/default-pr-template.md](templates/default-pr-template.md)
- Fill every template section from the layout
- Keep each field concise (1-5 lines)
- Add checklists when applicable
- Write `N/A` with brief note when something does not apply

**Security check:** Scan for secrets before including in body → Stop if found

### 5. Propose and Confirm

Present the drafted **Title** and **Body** to the user:

```
## Proposed PR

**Title:** <drafted title>

**Body:**
<drafted body>

---
Please confirm or request edits.
```

Revise until user approves.

### 6. Create Draft PR

```bash
gh pr create \
  --draft \
  ${base:+--base "$base"} \
  ${reviewers:+--reviewer "$reviewers"} \
  ${assignees:+--assignee "$assignees"} \
  ${labels:+--label "$labels"} \
  ${project:+--project "$project"} \
  ${milestone:+--milestone "$milestone"} \
  --title "$(cat <<'TITLE'
<title>
TITLE
)" \
  --body "$(cat <<'BODY'
<body>
BODY
)"
```

**Notes:**
- Stage any necessary generated files before PR creation
- Ensure branch is up to date with remote
- Let `gh` push if needed

### 7. Post-Creation

```bash
# Capture and display PR URL from output
# Show next steps
```

Report to user:
- PR URL (clickable)
- Next steps: push more commits, convert to ready (`gh pr ready`), assign reviewers

## PR Title Style

### Format

```
<type>(<scope>): <subject>
```

### Types

- `feat`: User-facing feature
- `fix`: User-facing bug fix
- `docs`: Documentation only
- `style`: Formatting, no logic change
- `refactor`: Code change without behavior change
- `test`: Add/modify tests only
- `chore`: Maintenance, tooling, infrastructure

### Examples

```
feat: add user authentication flow
fix(api): handle timeout on large uploads
refactor: migrate to new config format
docs: update API reference for v2
```

## Quick Reference

### Validation Checklist

- No existing open PR for this branch
- Commits exist ahead of base branch
- Quality gates pass (lint, test, build)
- No secrets in title or body
- Title follows semantic format
- Title ≤72 characters
- Body fills template sections
- User approved title and body

### Common Pitfalls

- Creating PR without running quality gates
- Vague titles like "Updates" or "Fix stuff"
- Empty or minimal PR body
- Missing template sections
- Including debug or WIP commits
- Not checking for existing PRs first

### Useful gh Commands

```bash
# List PRs from current branch
gh pr list --head $(git branch --show-current)

# Get default branch
gh repo view --json defaultBranchRef -q .defaultBranchRef.name

# View PR after creation
gh pr view

# Convert draft to ready
gh pr ready

# Add reviewers after creation
gh pr edit --add-reviewer <handle>
```
