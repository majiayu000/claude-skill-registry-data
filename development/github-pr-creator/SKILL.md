---
name: github-pr-creator
description: Creates GitHub pull requests using gh CLI. Use when creating PRs or submitting code for review.
---

# GitHub Pull Request Creator

Creates Pull Requests using GitHub CLI.

## Prerequisites

Branch must be created with changes committed and pushed.
Refer to git-operator skill for Git operations.

## Procedure

### Confirm Issue Linking

If the user specified an Issue, use that Issue.

If the user explicitly indicated no Issue linking is needed, proceed without linking.

If the user did not specify, briefly summarise what the PR implements and ask the user which Issue to link, or whether Issue linking is not needed.

### Detect Templates

Detect PR templates. Filenames are case-insensitive.

Single file template locations (in priority order):

- `.github/pull_request_template.md`
- `pull_request_template.md` (repository root)
- `docs/pull_request_template.md`

Multiple templates directory locations:

- `.github/PULL_REQUEST_TEMPLATE/`
- `PULL_REQUEST_TEMPLATE/` (repository root)
- `docs/PULL_REQUEST_TEMPLATE/`

If a single file template is found, read and use it.
If a templates directory is found, list available templates and ask the user which one to use.
If no templates exist, use [templates/default.md](templates/default.md).

### Create PR

Create the Pull Request with `gh pr create` and report the PR URL to the user.

## Issue Link Format

Regardless of whether a PR template exists, always use the full URL format for Issue linking.

```
- https://github.com/{owner}/{repo}/issues/xxx
```

## Title Guidelines

The title should be a natural language sentence summarising the task and implemented changes.
Do not use commit message format (e.g., "chore(update): xxx").

## Language

Write PR content in Japanese by default.
If the user explicitly requests English, write in English.
