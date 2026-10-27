---
name: codebase-memory
description: >
  Structural graph tools for live codebase navigation — trace call paths, detect change blast radius,
  find dead code, query architecture. Use before reading files. 120x fewer tokens than file exploration.
allowed-tools: []
effort: low
---

# Codebase Memory — Structural Graph

Zero-file-read structural analysis. Always try these tools BEFORE reading files for structural questions.

## Quick Decision Matrix

| Question | Tool |
|----------|------|
| What calls `foo()`? | `trace_path(function_name="foo", direction="inbound")` |
| What does `foo()` call? | `trace_path(function_name="foo", direction="outbound")` |
| Full call chain | `trace_path(direction="both", depth=3)` |
| Impact of my change | `detect_changes(base_branch="main")` |
| Architecture overview | `get_architecture` |
| Find by name/pattern | `search_graph(name_pattern="Auth.*")` |
| Find by label | `search_graph(label="Class")` |
| Dead code | `search_graph(max_degree=0, label="Function")` |
| Custom query | `query_graph(query="MATCH (n:Function)-[:CALLS]->(m) RETURN n.name, m.name LIMIT 20")` |
| Execution flows | `list_flows` → `get_affected_flows` |
| ADR management | `manage_adr(mode="get")` |

## Workflow — First Use

1. `index_repository(repo_path=".")` — first run only (~6s for 500 files)
2. `list_projects` — verify indexed
3. `get_architecture` — architecture map

## Workflow — Before Reviewing Changes

1. `detect_changes(base_branch="main")` → risk score + blast radius
2. `get_affected_flows` → which execution paths break
3. `trace_path` on highest-risk functions

## Workflow — Exploration

1. `get_architecture` → community map, entry points
2. `search_graph(name_pattern="<keyword>")` → find relevant nodes
3. `trace_path` → traverse from found nodes
4. `get_code_snippet(qualified_name="<name>")` → source with context

## Known Gotchas

1. `search_graph(relationship="HTTP_CALLS")` filters by degree — use `query_graph` for actual edge inspection
2. `query_graph` has a 200-row cap — use `search_graph` with degree filters for counts
3. `trace_path` requires **exact** qualified names — use `search_graph(name_pattern=...)` first
4. `direction="outbound"` misses cross-service callers — use `direction="both"`
5. Results default to 10 per page — check `has_more` and paginate with `offset`

## Re-indexing

Graph auto-updates via background git polling (5–60s adaptive). For immediate refresh:
`index_repository(repo_path=".", mode="fast")`
