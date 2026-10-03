---
name: gh
description: GitHub CLI usage and workflow patterns. Use when working with GitHub repositories, pull requests, issues, or API interactions.
---
# gh CLI

Use `gh` for all GitHub interactions. It handles authentication automatically and works with private repositories.

## Common Commands

- `gh repo view` — view repository README and metadata
- `gh issue view <number>` — view issue details
- `gh pr view <number>` — view pull request details
- `gh run view <run_id>` — view workflow run status
- `gh run view --job <job_id> --log` — view job logs

## API Access

Use `gh api` for operations not covered by built-in commands:

```bash
gh api repos/{owner}/{repo}/contents/{path}  # fetch file contents
gh api repos/{owner}/{repo}/pulls/{number}/comments  # PR review comments
```

## Reference Files

- **reviews.md**: Pull request review patterns

## Workflows

### Pull Request

- You must `git push` a branch before creating a pull request with `gh pr create`.
