---
name: Pull Request
description: |
  Create a GitHub pull request (PR) with proper formatting and content guidelines. Use when creating or updating pull requests/PRs (or GitLab merge requests/MRs, Gerrit change requests/CRs).
allowed-tools: Bash(gh:*), mcp__github
---
# Pull Request

Guidelines for creating or updating pull requests (PRs), merge requests (MRs), or change requests (CRs).

## Title

- Check recent commits (`git log --oneline -20`) to determine the repo's commit style:
  - **subject** (default): `${subject}: ${summary}` (e.g., `api: add timeout to request`)
  - **conventional**: `${type}: ${summary}` (e.g., `fix: add timeout to request`)
- Keep under 50 characters, max 100
- Use imperative mood, lowercase except proper nouns

## Body

- Use strategy in [`context.md`](context.md) to gather context if needed
- Start with 1-3 sentences summarizing the change (no preceding header)
- **Wrap all code identifiers with backticks**: function names, class names, file paths, endpoints, status codes, etc.
- Use `##` sections for larger changes. See [`sections.md`](sections.md) for detailed guidance on:
  - `## Issue` - Root cause analysis and issue linking
  - `## Changes` - High-level description of changes
  - `## Testing` - Test coverage insights
  - `## References` - Related links and issues

## Issue Handling

When an issue is referenced:

- **ONLY reference the issue** in the PR body (e.g., `Closes #123`, `Fixes #456`)
- **NEVER modify the issue directly** - no comments, labels, milestones, or assignees

## Workflow

See [`workflow.md`](workflow.md) for creating a new pull request.
