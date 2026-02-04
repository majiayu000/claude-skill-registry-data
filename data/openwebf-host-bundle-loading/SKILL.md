---
name: openwebf-host-bundle-loading
description: Choose and implement WebFBundle loading in a Flutter host (remote URL, assets, localhost dev, inline) and diagnose bundle load failures (bad URL, missing assets, network errors). Use when the user mentions WebFBundle, bundle URL/path, remote vs assets vs localhost vs inline, or “bundle won’t load”.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__project_profile, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__docs_related, mcp__openwebf__templates_get, mcp__openwebf__templates_render
---

# OpenWebF Host: Bundle Loading (WebFBundle)

## Instructions

1. Identify the bundle mode (remote URL, assets, localhost dev, inline) and the constraints (release cadence, store policy, offline needs).
2. Use `mcp__openwebf__project_profile` to detect what the repo already has (controller manager, bundle loading, caching).
3. Use MCP docs to confirm correct `WebFBundle` usage and safe defaults.
4. Provide minimal, copy-pastable host-side code changes and verification steps.

More:
- [reference.md](reference.md)
- [doc-queries.md](doc-queries.md)
- [examples.md](examples.md)
