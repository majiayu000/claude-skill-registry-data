---
name: code-review-graph
description: >
  Change risk analysis — detect blast radius, risk score, and breaking changes from git diffs.
  Use before any PR or merge. Crown jewel: detect_changes_tool.
  Triggers on: "review PR", "check impact", "blast radius", "what breaks", "safe to merge"
allowed-tools: []
effort: low
---

# code-review-graph — Change Risk Analysis

Structural change safety gate. Builds a SHA-256 AST graph from source code, then on any diff computes:
- **Risk score** (0–100)
- **Blast radius** — all transitively affected nodes (BFS, 100% recall)
- **Breaking changes** — nodes whose signature changed
- **Impacted flows** — execution paths traversing changed nodes

## Quick Decision Matrix

| Question | Tool |
|----------|------|
| Is this change safe to ship? | `mcp__code-review-graph__detect_changes_tool(base_branch="main")` |
| Build/rebuild the graph | `mcp__code-review-graph__build_graph_tool(repo_path=".")` |
| Graph status + stats | `mcp__code-review-graph__get_graph_info_tool` |
| What changed vs main? | `mcp__code-review-graph__get_diff_tool(base_branch="main")` |
| Node details | `mcp__code-review-graph__get_node_tool(node_id="<id>")` |
| Node neighbors | `mcp__code-review-graph__get_neighbors_tool(node_id="<id>", depth=2)` |
| Find by name | `mcp__code-review-graph__search_nodes_tool(query="AuthService")` |
| Community structure | `mcp__code-review-graph__get_communities_tool` |
| Critical path | `mcp__code-review-graph__get_critical_path_tool(source="<id>", target="<id>")` |
| Dependency chain | `mcp__code-review-graph__get_dependency_chain_tool(node_id="<id>")` |

## Mandatory Pre-PR Workflow

1. `build_graph_tool(repo_path=".")` — first run only (or after major refactor)
2. `detect_changes_tool(base_branch="main")` — risk score + blast radius
3. If risk score ≥ 60 → `get_dependency_chain_tool` on the highest-risk node
4. If impacted flows present → review them with `get_neighbors_tool`
5. Fix or document risks before merging

## Risk Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 0–25 | Low risk | Review and ship |
| 26–50 | Moderate | Verify blast radius manually |
| 51–75 | High | Write tests for affected nodes |
| 76–100 | Critical | Full review + stakeholder sign-off |

## Lifecycle

**First build:** `build_graph_tool(repo_path=".")` — ~6s for 500 files, ~30s for large repos.

**Incremental:** git post-commit hook runs `code-review-graph update` automatically. <2s on any commit.

**After major refactor:** `build_graph_tool(repo_path=".", force_rebuild=True)` — forces full re-index.

**MCP server:** Started automatically by Claude Code when `mcp__code-review-graph__*` tools are invoked.
Started via `uvx code-review-graph serve` — isolated environment, no PATH issues.

## 29 Available Tools

Core: `build_graph_tool`, `detect_changes_tool`, `get_graph_info_tool`, `get_diff_tool`
Navigation: `get_node_tool`, `get_neighbors_tool`, `search_nodes_tool`, `get_critical_path_tool`
Analysis: `get_dependency_chain_tool`, `get_communities_tool`, `get_impact_analysis_tool`
Queries: `get_nodes_by_type_tool`, `get_nodes_by_file_tool`, `get_edges_tool`, `get_entry_points_tool`
Metrics: `get_complexity_metrics_tool`, `get_coupling_metrics_tool`, `get_cohesion_metrics_tool`
Review: `get_review_summary_tool`, `get_change_summary_tool`, `get_risk_breakdown_tool`

## Key Gotchas

- **Build first:** MCP server exits if `.code-review-graph/graph.db` doesn't exist — run `build_graph_tool` before first use
- **uvx required:** `uvx code-review-graph serve` needs uv installed (`pip install uv` or `brew install uv`)
- **Score is aggregate:** individual nodes in blast radius may be critical even at score 30 — check the breakdown
- **After git rebase/reset:** SHA-256 detects all changes — `build_graph_tool(force_rebuild=True)` if graph seems stale
- **[communities] extra:** improves blast radius clustering; falls back to file-based grouping without it
