---
name: graphify
description: >-
  Use Graphify knowledge-graph MCP (graphify-gallery) or CLI for Electron/React
  architecture connectivity. Prefer after rg/fff; never for IPC/backend triage
  (use is-ui-mcp).
---

# Graphify (architecture graph)

Local AST knowledge graph — no vector store. Soft rule: [`.cursor/rules/graphify.mdc`](../../rules/graphify.mdc) (`alwaysApply: false`).

## When to use

- Cross-module “how does X connect to Y” (main ↔ preload ↔ renderer), god nodes, communities
- `graphify-out/graph.json` exists (build: `graphify . --code-only`)
- MCP server **`graphify-gallery`** is connected (or fall back to CLI)

## When not to use

| Need | Use instead |
|------|-------------|
| Gallery IPC / backend health / CDP | [`image-scoring-mcp`](../image-scoring-mcp/SKILL.md) (`is-ui-mcp`) |
| Literal string / filename | [`agent-search`](../agent-search/SKILL.md) / **fff-gallery** |
| Graph missing | `graphify . --code-only` then retry |

## Setup

1. `uv tool install "graphifyy[mcp]"`
2. `graphify . --code-only`
3. Enable in [`.cursor/mcp.json`](../../mcp.json) (see [mcp.example.json](../../mcp.example.json)):

```json
"graphify-gallery": {
  "command": "graphify-mcp",
  "args": ["graphify-out/graph.json"],
  "cwd": "${workspaceFolder:image-scoring-gallery}"
}
```

4. Reload Cursor MCP. Check tool schemas before calling.

## MCP tools (`graphify-gallery`)

| Tool | Args | Use for |
|------|------|---------|
| `graph_stats` | (none) | Sanity check |
| `query_graph` | `question` (req); `mode`; `depth`; `token_budget` | Subgraph search |
| `get_node` | `label` | One symbol / file |
| `get_neighbors` | `label`; optional `relation_filter` | Direct edges |
| `get_community` | `community_id` | Cluster members |
| `god_nodes` | optional `top_n` | Hubs |
| `shortest_path` | `source`, `target` | Path between concepts |
| `list_prs` / `get_pr_impact` / `triage_prs` | PR impact (network) | Only if user asks |

Optional `project_path` on every tool for multi-root.

## Preferred workflow

```text
graph_stats()
query_graph({question: "how does electronAPI connect to preload"})
shortest_path({source: "preload", target: "db.ts"})
```

CLI fallback: `graphify query "…"`, `graphify path A B`, `graphify explain "…"`.

## Agent-safe patterns

- Bound `token_budget`; escalate depth only when needed.
- Pipeline/DB questions → sibling **`is-be-mcp`**, not Graphify.
- Soft rule only — do not run stock `graphify cursor install`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| MCP missing | Reload MCP; confirm `graphify-gallery` + `graphify-out/graph.json` |
| Build wants API key | `graphify . --code-only` |
| Stale graph | Re-run extract + `graphify cluster-only .` |

## Related

- [agent-cli-hub](../agent-cli-hub/SKILL.md) · [mcp-code-intelligence](../mcp-code-intelligence/SKILL.md) · AGENTS.md § Graphify
