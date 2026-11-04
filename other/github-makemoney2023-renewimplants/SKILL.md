---
name: github
description: >-
  Use when interacting with GitHub repos, PRs, issues, or checks via GitHub MCP or the gh CLI.
---

# GitHub

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
`gh` CLI + GitHub MCP

## Env / secrets
`GITHUB_TOKEN` / `gh auth`

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
`user-github`

## Primary ops
1. Prefer `gh` for PRs/issues per user rules
2. Never force-push main; never skip hooks unless asked
3. Use for build logs, dispatch status, eng collaboration

## Fallback
git remotes + GitHub web UI

## Common failures
Auth → `gh auth login` or token in .env.local
