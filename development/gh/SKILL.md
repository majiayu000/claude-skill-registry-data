---
name: gh
description: Use GitHub CLI for searching and working with Ascend repositories.
---

# GitHub CLI for Ascend repos

Use the `gh` CLI to search and work with Ascend repositories.

## Key repositories

| Repo | Purpose |
|------|---------|
| `ascend-io/ascend-core` | Python SDK, Pydantic models, CLI |
| `ascend-io/ascend-backend` | Backend services, API |
| `ascend-io/ascend-ui` | Frontend application |
| `ascend-io/ascend-docs` | Documentation |
| `ascend-io/ascend-community-internal` | Community projects |

## Search Ascend repos

```bash
# search issues/PRs
gh search issues "query" --owner ascend-io
gh search prs "query" --owner ascend-io

# search code across all Ascend repos
gh search code "pattern" --owner ascend-io
```
## Create PRs

Use `gh pr create -t $TITLE -b $BODY` to create a PR.

Maintain our concise, technically precise style.

