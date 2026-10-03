---
name: codebase-graph-scout
description: >
  Use graph-backed or semantic codebase intelligence before editing. Use when
  tasks need symbol search, blast radius, affected tests, architecture health,
  dependency paths, large-codebase context, Roam, CodeAlive, GraphRAG, or MCP
  code search. Skip for tiny scripts where rg/read is enough.
---

# Codebase Graph Scout

Prefer graph tools when the repo is large enough that raw file reading will
waste context.

## Tool Preference

| Available tool | Use for |
|---|---|
| `roam-code` | local symbol graph, preflight, impact, health, affected tests |
| CodeAlive MCP | hosted semantic/GraphRAG code search with API key |
| `rg` + manifests | fallback for small repos or missing graph tools |

## Roam Loop

```bash
roam init
roam health
roam understand
roam context <symbol>
roam preflight <symbol>
roam affected-tests <symbol>
```

Use `--json` for parsing and `--budget <n>` when context is tight.

## CodeAlive Loop

1. List data sources.
2. Run `semantic_search` or `grep_search`.
3. Fetch only the relevant artifacts.
4. Expand relationships for the smallest useful set.
5. Use chat/synthesis only after search results are insufficient.

## Output

Return:

- symbols/files to read
- edit risk
- likely tests
- dependency or call paths that matter
- what not to touch

Reference source patterns in `references/source-repos.md`.

## Validation

- The returned file/symbol set is smaller than a broad repo read.
- Claimed impact paths cite graph/search output or exact files.
- If graph tools are unavailable, the fallback `rg`/manifest path is stated.
