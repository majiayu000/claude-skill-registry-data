---
name: context7-docs
description: >-
  Use when looking up current library, framework, SDK, or API documentation via Context7 MCP before coding or integrating tools.
---

# Context7 Docs

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
Context7 MCP — prefer `plugin-context7-plugin-context7`, fallback `user-context7-mcp`

## Env / secrets
—

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
`plugin-context7-plugin-context7` or `user-context7-mcp`

## Primary ops
1. `resolve-library-id` → `query-docs` (max 3 `query-docs` per question unless iterating)
2. Prefer Context7 over training memory for library/SDK APIs (Next, Supabase, Vercel, shadcn, etc.)
3. Record `libraryId` used when material to the handoff / build log
4. If MCP unavailable → `tool_status: unavailable`; fall back to official docs URLs via firecrawl/browser

## Fallback
Official docs URLs via firecrawl/browser

## Common failures
Wrong library match → refine libraryName; do not guess APIs
