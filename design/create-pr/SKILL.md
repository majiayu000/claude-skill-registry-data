---
name: create-pr
description: Create a well-structured pull request with proper description, design decisions, and file changes. Use when asked to create a PR, open a PR, or submit changes for review.
---

# Create Pull Request

Create a pull request with a comprehensive description that explains the problem, solution, design decisions, and changes.

## Instructions

### 1. Gather context

Run these commands in parallel to understand the current state:

```bash
# Current branch
git branch --show-current

# Check if tracking remote
git status -sb

# All commits on this branch (not on main)
git log main..HEAD --oneline

# Full diff from main
git diff main...HEAD --stat
```

### 2. Extract Linear ticket ID

Check the branch name for a Linear ticket ID (format: `thr-XX` or `THR-XX`):

```bash
# Extract ticket ID from branch name
git branch --show-current | grep -oiE 'thr-[0-9]+' | tr '[:lower:]' '[:upper:]'
```

If found, this ticket ID **must** be included in:

- The PR title (e.g., `feat(THR-19): implement agent loop`)
- The PR description (link to Linear issue)

### 3. Analyze the changes

For each commit, understand:

- What problem does it solve?
- What design decisions were made?
- What alternatives were considered?

Read relevant files if needed:

- Task docs in `tasks/` or `docs/plans/`
- Work notes if they exist
- The actual code changes

### 4. Structure the PR description

The PR must include these sections:

```markdown
**Linear:** [THR-XX](https://linear.app/threa/issue/THR-XX) _(if applicable)_

## Problem

[What issue or limitation exists? Why does this change need to happen?]

## Solution

[High-level description of the approach taken]

### How it works

[Architecture diagram or flow explanation if applicable]

### Key design decisions

[For each significant decision:]
**1. [Decision title]**

[What was chosen and why. Include alternatives considered if relevant.]

## New files

| File              | Purpose           |
| ----------------- | ----------------- |
| `path/to/file.ts` | Brief description |

## Modified files

| File              | Change       |
| ----------------- | ------------ |
| `path/to/file.ts` | What changed |

## Deleted files (if any)

| File              | Reason      |
| ----------------- | ----------- |
| `path/to/file.ts` | Why removed |

## Test plan

- [x] Completed tests
- [ ] Manual verification steps

---

🤖 _PR by [Claude Code](https://claude.com/claude-code)_
```

### 5. Create the PR

```bash
# Push branch if needed
git push -u origin $(git branch --show-current)

# Create PR (write body to temp file first to avoid heredoc issues)
# If ticket ID exists, include it: "[type](THR-XX): [short description]"
gh pr create --base main --title "[type](THR-XX): [short description]" --body-file /tmp/claude/pr-body.md
```

If `gh pr create` fails with GraphQL errors, use the API directly:

```bash
gh api repos/{owner}/{repo}/pulls --method POST \
  -f title="[type]: [short description]" \
  -f head="$(git branch --show-current)" \
  -f base="main" \
  -f body="$(cat /tmp/claude/pr-body.md)"
```

### 6. Return the PR URL

Always provide the PR URL to the user when done.

## PR Title Conventions

Use conventional commit format with Linear ticket ID when available:

- `feat(THR-XX):` - New feature
- `fix(THR-XX):` - Bug fix
- `refactor(THR-XX):` - Code restructuring without behavior change
- `docs(THR-XX):` - Documentation only
- `test(THR-XX):` - Test additions/changes
- `chore(THR-XX):` - Maintenance tasks

If no Linear ticket exists, omit the parenthetical: `feat: description`

## Examples

**User says:** "Create a PR"
**Action:** Analyze current branch, gather context from task docs, create comprehensive PR

**User says:** "Open a PR for this feature"
**Action:** Same as above, ensuring all design decisions are documented

**User says:** "Submit this for review"
**Action:** Create PR, return URL for user to review

## Important Notes

- **Always include Linear ticket ID** in title and description when working from a ticket
- Never create a PR with an empty or minimal description
- Always explain the "why" not just the "what"
- Include divergences from original plans if applicable
- Reference task docs or issues when relevant
