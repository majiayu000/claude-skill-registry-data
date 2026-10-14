---
name: graphify-cli
description: Query a Graphify code graph safely — MCP tools for both the repository's own graph and the cross-repository global graph, read-only CLI for hand-run use, availability detection, and graceful fallback. Use whenever a flow needs structural answers (callers, impact, flows, hubs) from an indexed repository.
license: MIT
metadata:
  author: andresnator
  version: "1.6.0"
  status: testing
---

# Graphify CLI

Reusable contract for querying a Graphify code graph. The graph is read-only material: this skill covers finding it, querying it, and degrading gracefully — never building it. The division of paths is fixed:

| Graph | Path | Who |
|---|---|---|
| Repository's own (`.ai/graphify-out/graph.json`) | `graphify` MCP tools (`query_graph`, `get_neighbors`, …) | Agents |
| Cross-repository global (`~/.graphify/global-graph.json`) | `graphify-global` MCP tools + `~/.graphify/global-manifest.json` | Agents |
| Either graph, by hand | Read-only CLI with explicit `--graph` | Humans only |
| Lifecycle (first indexing, refresh) | `/graphify-index` command + `graphify-init` plugin | Human and plugin only — never agents |

## Availability detection

1. The per-repository graph lives at `.ai/graphify-out/graph.json` (repo root). Check that literal path. If the file exists and parses, the graph is available; record `graphify: available`.
2. If the graph file is missing, record `graphify: absent` and skip Graphify entirely. Do not build it: first indexing is human-gated behind the `/graphify-index` command, and the `graphify-init` OpenCode plugin owns refreshes afterwards. Mention `/graphify-index` to the user once as the way to enable the graph, then continue without it.
3. Check freshness: compare the graph's `built_at_commit` with `git rev-parse HEAD`, and check whether `.ai/graphify-out/.opencode-extract-lock` exists (a refresh is in flight). On a commit mismatch or a present lock, downgrade the record to `graphify: stale`: still query the graph, but treat every answer as an approximate locator — verify each claim against the current files before citing it, and never base impact or blast-radius conclusions on the stale graph alone. The `graphify-init` plugin refreshes it on the next session; never refresh it yourself.
4. Documentation coverage depends on the recorded indexing mode — read `.ai/graphify-out/.opencode-index-mode` (one JSON line): `docs` means markdown and other documents are indexed as document and concept nodes, so documentation questions are graph-first too; `code-only` means the graph holds no documentation and docs questions go straight to filesystem tools. When the mode file is missing (a graph indexed before it existed), fall back to `.ai/graphify-out/.graphify_semantic_marker` — Graphify writes it only when a semantic docs pass ran, so present means `docs` coverage, absent means `code-only`.

Never conclude "no graph" from a wildcard search. Patterns like `**/graphify-out/graph.json` do not match inside dot-directories, so they silently miss `.ai/graphify-out/graph.json`. An empty glob is inconclusive, not evidence of absence — check the literal path before reporting `graphify: absent`.

## Querying the local graph (MCP)

The Graphify MCP tools are the agent path to the repository's graph: `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `god_nodes`, `graph_stats`, `get_community`. They answer over the graph the server was started with, read-only.

- Omit the optional `project_path` argument unless you genuinely need another repository. Passing it makes the server ignore the graph it was started with and resolve `<project_path>/<GRAPHIFY_OUT>/graph.json` from its own environment instead; if the server was launched without `GRAPHIFY_OUT` exported, that path does not exist and the tool reports no graph for a repository that has one. When a `project_path` call comes back empty, retry without it before concluding anything.
- If the MCP tools are unavailable, fall back to the runtime's filesystem tools directly — the CLI is not an agent fallback for the local graph.
- Cite the underlying `file:line` for every claim the graph resolves; the graph is a locator, not evidence by itself. Graphs may also contain documentation, paper, and image nodes when the repository owner enabled semantic indexing — treat them like any other node.

## Cross-repository global graph (MCP)

`~/.graphify/global-graph.json` merges every indexed repository under a repo tag; the `graphify-global` MCP server exposes the same tool set over it.

Trigger: any question that names a repository or project other than the current one, not only questions that explicitly span several. Before Context7, web search, or a clarifying question, read `~/.graphify/global-manifest.json` — an indexed tag means it is a local repo question, and wins over library documentation. Answer structural questions with the `graphify-global` tools. For content questions (what its documentation says, what a file contains), the tag's `source_path` points at that repo's `.ai/graphify-out/graph.json` — the repository root is two directories up; read the actual files there and cite them.

Caveat: node labels are not namespaced — two repositories defining the same class contribute two same-label nodes. Keep symbol-addressed queries on the repository's own graph, where labels are unambiguous; use the global graph for open-ended questions.

## Manual CLI verbs (human use)

The read-only verbs (`query`, `explain`, `path`, `affected`, `god-nodes`) are for a human in a terminal — never an agent path. Always pass `--graph` explicitly; the CLI's default (`./<GRAPHIFY_OUT>/graph.json`) resolves only with `GRAPHIFY_OUT=.ai/graphify-out` exported from the repo root:

```bash
graphify global list                                                  # repos and node counts
graphify query "<question>" --graph ~/.graphify/global-graph.json
graphify query "<question>" --graph .ai/graphify-out/graph.json --budget 2000
graphify explain "<NodeLabel>" --graph .ai/graphify-out/graph.json
```

## Hard rule: never lifecycle commands

Never run `graphify extract`, `update`, `watch`, `global add`, `global remove`, or any `graphify ... install` variant. They mutate state, and `update`/`watch` recreate `graphify-out/` at the repository root, outside `.ai/`. First indexing belongs to the human-invoked `/graphify-index` command, refreshing belongs to the `graphify-init` plugin, and recovery belongs to the user.

## Fallback

When the graph or the MCP tools are unavailable, continue with the runtime's normal read, LSP, grep, and glob tools without friction, and state the fallback in your output. Needing more than ~3 files for one structural question usually means the graph query was too broad — narrow it before crawling files.
