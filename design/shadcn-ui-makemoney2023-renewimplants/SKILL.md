---
name: shadcn-ui
description: >-
  Use when looking up or applying shadcn/ui components, blocks, or themes via shadcn MCP during frontend work.
---

# shadcn/ui

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
shadcn MCP + Vercel shadcn plugin skill

## Env / secrets
—

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
`user-shadcn-ui`

## Primary ops
1. list_components / get_component before inventing primitives
2. Match project existing design tokens
3. Pair with web-designer / tech-lead craft packs

## Fallback
`npx shadcn@latest add <component>`

## Common failures
Wrong style registry → check components.json in target app
