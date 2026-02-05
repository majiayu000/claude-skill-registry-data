---
name: openwebf-host-theming-sync
description: Sync theming between Flutter and WebF (automatic theme sync, prefers-color-scheme, dark mode patterns). Use when the user mentions theme sync, dark mode, prefers-color-scheme, CSS variables, or WebF theming from MaterialApp.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__templates_get, mcp__openwebf__templates_render
---

# OpenWebF Host: Theming Sync

## Instructions

1. Determine desired behavior: automatic sync vs manual overrides.
2. Use MCP docs to confirm how theme synchronization works by default and safe patterns.
3. Provide concrete patterns for:
   - CSS `prefers-color-scheme`
   - JS/React theme toggles
   - Flutter-driven theme propagation
4. Offer templates where applicable:
   - `host/theme-sync-materialapp`
   - `app/theming-prefers-color-scheme-css`
   - `app/theming-matchmedia-listener`

More:
- [reference.md](reference.md)
- [doc-queries.md](doc-queries.md)
- [examples.md](examples.md)
