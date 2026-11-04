---
name: figma
description: >-
  Use when reading or writing Figma designs, Code Connect, or design-system work via Figma MCP and plugin skills.
---

# Figma

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
Figma MCP + `skills/plugins/figma/` skills

## Env / secrets
Figma auth via MCP (`whoami` / `mcp_auth` as needed)

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
`plugin-figma-figma`, `user-Figma`

## Primary ops
1. Before `use_figma` / `get_design_context`: load the matching skill (`figma-use`, `figma-design-to-code`, `figma-generate-design`, or `figma-generate-library`)
2. Call `GetMcpTools` for the Figma server when unsure of schemas; on `needsAuth` run `mcp_auth`
3. Parse `fileKey` / `nodeId` from figma.com URLs (`-` → `:` in nodeId)
4. `search_design_system` before generating components; never invent design tokens
5. If MCP unavailable → `tool_status: unavailable`; fall back to exported frames/screenshots in the repo

## Fallback
Exported frames / screenshots in the repo

## Common failures
Auth errors → `mcp_auth`; never invent design tokens
