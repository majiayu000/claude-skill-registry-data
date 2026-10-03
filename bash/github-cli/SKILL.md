---
name: github-cli
description: >
  MUST USE for GitHub-related operations, including a GitHub URL, repository or
  code search, Issues, pull requests, Actions, Releases, permissions, and API
  requests. Use the local GitHub CLI (`gh`).
---

# GitHub CLI

This skill owns GitHub operations. Use the local `gh` CLI for GitHub reads and
writes, including GitHub URLs and GitHub code search.

Start with `gh auth status` when the active account or authentication could
affect the result. Inspect the current repository, state, and remote data before
making a GitHub mutation; obtain any authorization that the requested mutation
requires.

## Common commands

```bash
# Search
gh search repos "query" --sort stars --limit 10
gh search code "query" --language python

# Repository
gh repo view owner/repo
gh repo clone owner/repo
gh repo create my-repo --private
gh repo fork owner/repo
gh repo sync owner/repo

# Issues and pull requests
gh issue list --repo owner/repo --state open
gh issue view 123 --repo owner/repo
gh issue create --repo owner/repo --title "Title" --body "Body"
gh pr list --repo owner/repo --state open
gh pr view 123 --repo owner/repo
gh pr create --repo owner/repo --title "Title" --body "Body"
gh pr checks 123 --repo owner/repo

# Actions and Releases
gh workflow list --repo owner/repo
gh run list --repo owner/repo --limit 10
gh run view <run-id> --repo owner/repo --log-failed
gh release list --repo owner/repo

# API and structured output
gh api repos/owner/repo
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

Use `gh <command> --help` when the exact command shape is uncertain. For local
Git work, use `git`; use `gh` for the GitHub service operation around it.
