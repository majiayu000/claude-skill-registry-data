---
name: vercel
description: >-
  Use when deploying, inspecting deployments, env vars, runtime logs, or Vercel platform docs via Vercel MCP or plugin skills.
---

# Vercel

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
Vercel MCP + `skills/plugins/vercel/`

## Env / secrets
`VERCEL_TOKEN`

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
`user-vercel`

## Primary ops
1. search_vercel_documentation for platform questions
2. list_deployments / get_runtime_logs for incident work
3. Pair with Next.js plugin skills for app code

## Fallback
`vercel` CLI

## Common failures
Missing token → secrets; do not deploy production without ask
