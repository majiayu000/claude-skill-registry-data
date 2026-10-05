---
name: gh
description: GitHub CLI (212 man pages).
metadata:
  trit: 0
---

# gh

GitHub CLI (212 man pages).

## Auth

```bash
gh auth login
gh auth status
gh auth token
```

## Repo

```bash
gh repo clone owner/repo
gh repo create name --public
gh repo view --web
```

## PR

```bash
gh pr create --title "Title" --body "Body"
gh pr list --state open
gh pr checkout 123
gh pr merge --squash
```

## Issue

```bash
gh issue create
gh issue list --label bug
gh issue close 42
```

## API

```bash
gh api repos/{owner}/{repo}/issues
gh api graphql -f query='{ viewer { login } }'
```

## Actions

```bash
gh run list
gh run view 12345
gh workflow run deploy.yml
```
