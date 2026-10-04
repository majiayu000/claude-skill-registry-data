---
name: graph-query
description: Use when the user asks a question about how things in the codebase or wiki relate — what connects two things, how something works end to end, what depends on what, or what a concept means in this repo. Answers from the knowledge graph in graphify-out/graph.json, with source-location citations. Trigger on "/graph-query", "ask the graph", "what connects X to Y", "trace how X works", "explain <concept> from the graph", "shortest path between".
---

# Graph Query

Ask the knowledge graph a relationship question and get a **cited answer grounded in the graph** —
not a guess. The graph is built by `/graph` (graphify) over code + the committed `wiki/`. This skill
only reads it.

## When to run
- `graphify-out/graph.json` exists, and the user has a question about how things relate:
  - "what connects the intake flow to the billing module?"
  - "trace how a `/wiki` capture becomes a committed entry."
  - "explain the WAT execution model from the graph."
  - "shortest path between `wiki_lint.py` and the commit gate."
- Use this for *relationships and explanations*. To (re)build or refresh the graph, run `/graph`.

## The output (always this shape)
```
## Graph answer — <the question>
**Answer** — the relationship/explanation, in plain sentences, grounded only in graph edges.
**Path / nodes used**
- <node A> —[<relation>]→ <node B>   (EXTRACTED · src: <path:line>)
- <node B> —[<relation>]→ <node C>   (INFERRED — not literal in source)
**Citations** — source_location for each EXTRACTED edge (path:line).
**Gaps** — anything the question asked that the graph does NOT contain (say so plainly).
```
Every claim traces to an edge. If the graph doesn't have it, the answer says so — it never fills the gap from memory.

## Process
1. **Check the graph exists.** If `graphify-out/graph.json` is missing, stop and tell the user:
   "No graph yet — run `/graph` first to build it." Don't answer from training data or by re-reading files.
2. **Pick the query that fits the question** (graphify, read-only):
   - Broad / "what relates to X" / "what connects X to Y" → `graphify query "<question>"` (BFS, broad neighborhood).
   - Trace a chain / "how does X flow to Y" / "trace how X works" → `graphify query "<question>" --dfs` (follows a path; `--budget N` to bound it).
   - "shortest path between A and B" → `graphify path "A" "B"`.
   - "explain <concept/node>" → `graphify explain "X"` (the node + its neighbors).
   For richer interactive exploration, the graphify MCP server may be wired
   (`python3 -m graphify.serve graphify-out/graph.json` → `query_graph`, `get_node`,
   `get_neighbors`, `shortest_path`, `god_nodes`, `graph_stats`); use it when the question needs
   several hops or node lookups. Otherwise the CLI is enough.
3. **Answer using ONLY what the graph returns.** Quote the `source_location` (path:line) for each edge
   you rely on. Fill the output shape above. Two hard rules:
   - **Never invent edges.** If the query returns nothing for part of the ask, list it under **Gaps**
     and say the graph doesn't cover it — do not bridge it with a guess or by reading the file yourself.
   - **Honor the honesty trail.** graphify labels every edge `EXTRACTED` (literal in source),
     `INFERRED` (graphify's inference), or `AMBIGUOUS` (uncertain). Present only `EXTRACTED` as fact.
     Tag `INFERRED`/`AMBIGUOUS` edges as such inline — never pass them off as established.

## Autonomy
**L1 — read-only.** Suggests/answers from the graph; the human decides. Builds nothing, sends nothing,
writes no files. (To rebuild the graph, that's `/graph`, not this skill.)

## Guardrails (from CLAUDE.md)
- **Cite, don't invent** (Guardrail #6). Every claim cites a graph edge's `source_location`;
  unsupported parts of the ask are flagged as gaps, never fabricated.
- **Respect the honesty audit trail.** `EXTRACTED` = fact; `INFERRED`/`AMBIGUOUS` are flagged as such,
  not stated as truth.
- The graph covers **code + the committed (de-identified) `wiki/` only** — by design it excludes `raw/`,
  `.env`, `.tmp/`, and secrets. If asked about something outside that scope, say it isn't in the graph.
- Read-only: no commits, no external sends, no file writes from this skill.
