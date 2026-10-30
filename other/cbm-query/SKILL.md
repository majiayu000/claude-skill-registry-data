---
name: cbm-query
description: "Query the Yana AI codebase knowledge graph via codebase-memory-mcp. Use instead of grep/glob when exploring call chains, finding callers/callees, understanding architecture, or tracing impact of changes. Triggers on: 'who calls X', 'trace path', 'find callers', 'search graph', 'cbm', 'knowledge graph', 'what calls', 'call chain', 'what uses', 'where is X defined', 'architecture overview', 'impact of changing'."
source: DeusData/codebase-memory-mcp (MIT)
tier: TIER 2 — CORRECTNESS
project: Users-vutam-Desktop-Yana-AI
---

# /cbm-query — Codebase Knowledge Graph

Query the Yana AI knowledge graph (35K nodes, 68K edges) instead of file-by-file grep.
Answers structural questions in <1ms. 10× fewer tokens than grepping files.

**When to use instead of grep/glob:**
- "Who calls `function_name`?" → `trace_path` (callers)
- "What does this function call?" → `trace_path` (callees)
- "Find anything named X" → `search_graph`
- "What changed and what broke?" → `detect_changes`
- "Overview of the codebase" → `get_architecture`
- "Show me the actual code" → `get_code_snippet` (after finding via search_graph)

**Do NOT use for:** reading config files, editing, writing — graph is read-only structural index.

---

## Project name (always pass this)

```
project: "Users-vutam-Desktop-Yana-AI"
```

If the project is not found, re-index first:
```
index_repository(repo_path="/Users/vutam/Desktop/Yana-AI", project_name="yana-ai")
```

---

## Tool Playbook

### 1. Find a symbol — `search_graph`

```
search_graph(
  project="Users-vutam-Desktop-Yana-AI",
  query="<name or keyword>",
  limit=10                    # default 10, max 50
)
```

Returns: name, qualified_name, label (Function/Class/Package), file_path, start_line.

**Label filter examples:**
- Functions only: add `label="Function"`
- Classes only: add `label="Class"`

---

### 2. Trace call chains — `trace_path`

```
trace_path(
  project="Users-vutam-Desktop-Yana-AI",
  function_name="<exact name from search_graph>",
  direction="callers",   # or "callees" or "both"
  depth=3                # how many hops (default 3, max 10)
)
```

**Workflow:** always `search_graph` first to get the exact `name`, then `trace_path`.

---

### 3. Get actual code — `get_code_snippet`

```
get_code_snippet(
  project="Users-vutam-Desktop-Yana-AI",
  qualified_name="<qualified_name from search_graph result>"
)
```

**Use `qualified_name` (not `function_name`)** — copy from search_graph result field.
Example: `Users-vutam-Desktop-Yana-AI.core.lib.hermes_adapted.context_compressor.ContextCompressor.compress`

---

### 4. Architecture overview — `get_architecture`

```
get_architecture(
  project="Users-vutam-Desktop-Yana-AI",
  aspects=["languages", "clusters"]   # or ["all"]
)
```

Returns: language breakdown, package clusters, service boundaries.

---

### 5. Impact of git changes — `detect_changes`

```
detect_changes(
  project="Users-vutam-Desktop-Yana-AI",
  since="HEAD~1"    # or a commit SHA, or "HEAD~5"
)
```

Returns which functions changed and which callers are potentially affected.
Use before a refactor to understand blast radius.

---

### 6. Text search (graph-augmented grep) — `search_code`

```
search_code(
  project="Users-vutam-Desktop-Yana-AI",
  pattern="<regex or text>",
  file_filter="*.sh"    # optional
)
```

Faster than raw grep — filtered through graph context.

---

### 7. Complex structural query — `query_graph`

```
query_graph(
  project="Users-vutam-Desktop-Yana-AI",
  cypher="MATCH (f:Function)-[:CALLS]->(g:Function) WHERE f.name = 'X' RETURN g.name, g.file_path LIMIT 20"
)
```

Use when the other tools don't cover the exact relationship you need.

---

## Standard Workflow

```
User: "who calls check_egress_target?"

1. search_graph(query="check_egress_target") → get exact name + file
2. trace_path(function_name="check_egress_target", direction="callers", depth=3)
3. If code needed: get_code_snippet(function_name="check_egress_target")
4. Report: callers list + file locations
```

---

## Output Contract

```
Symbol found:   [name] at [file:line]
Callers/callees: [list with file paths]
Code snippet:   [if requested]
Confidence:     [95% if found in graph, 60% if not found — may need re-index]
```

If symbol not found in graph:
- Check spelling via `search_graph` with a broader query
- If still missing: run `index_status` to check freshness, re-index if stale

---

## In-Skill Verification

After every `trace_path` result:
1. Spot-check 1 caller by reading the actual file — confirm the call exists
2. If graph says "no callers" but you expect some → re-index and retry once

---

## Anti-patterns

```
❌ Using grep to find "who calls X" when cbm-query can do it in <1ms
❌ Passing a fuzzy name to trace_path without search_graph first (will fail)
❌ Using query_graph for simple lookups — search_graph is faster
❌ Forgetting to pass project= (required on every call)
```
