---
name: openwebf-host-caching-httpcachemode
description: Configure and debug WebF runtime caching in Flutter using HttpCacheMode (stale content, offline-first, cache busting, clearing caches with WebF.clearAllCaches). Use when the user mentions HttpCacheMode, WebF.clearAllCaches, offline-first, stale remote bundles, or cache adapter behavior.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__project_profile, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__docs_related, mcp__openwebf__templates_get, mcp__openwebf__templates_render
---

# OpenWebF Host: Caching (HttpCacheMode)

## Instructions

1. Ask what the user wants: cache-first, network-first, offline-first, or “never cache in dev”.
2. Use project profile and code search to detect current cache settings.
3. Use MCP docs to choose an explicit `HttpCacheMode` and a cache-busting/version strategy.
4. Provide clear “how to clear caches” guidance and verification steps.

More:
- [reference.md](reference.md)
- [doc-queries.md](doc-queries.md)
- [examples.md](examples.md)
