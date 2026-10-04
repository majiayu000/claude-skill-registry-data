---
name: knowledge-graph
description: >
  Build, update, and query a persistent project knowledge graph from skills,
  memory, docs, and code structure — stdlib Python only, no external tools.
  Dual-mode: skill-library (agent-loom) or application (any consumer repo).
  Load when the user asks for a knowledge graph, project map, skill
  relationships, query the graph, update the graph, or trace how components
  connect. Auto-runs on memory-handoff and project-setup bootstrap.
  Also triggers on "build the graph", "what connects to X", "map this project".
license: MIT
metadata:
  author: dvy1987
  version: "2.3"
  category: project-specific
  sources: safishamsi/graphify patterns (native stdlib impl, no pip install)
  resources:
    references:
      - schema.md
      - integration.md
      - examples.md
    scripts:
      - build_graph.py
      - query_graph.py
      - graph_health.py
---

# Knowledge Graph

You maintain a **queryable project graph** at `docs/knowledge-graph/`. Stdlib Python only — no Graphify, no pip deps, no external URLs in outputs.

## Deployment Context

| Host | Mode | Typical use |
|---|---|---|
| **agent-loom** (skill library) | `skill-library` | Map skill invoke chains, memory, handoffs |
| **Any consumer project** | `application` | Map modules, docs, memory for GRAPHIFY-style project management |

Mode auto-detects from authoritative skill-library files: `docs/skill-graph.md` **and** `docs/SKILL-INDEX.md` → `skill-library` label; otherwise `application`. **Both modes always perform a repo-wide scan** — skills, all application source (any path), packages, config, docs, memory, directories. Never skills-only.

## Hard Rules

- **Full repo, always.** `build_graph.py` walks the entire repository for source files. `.agents/skills/` is indexed as skills, not skipped — but application code in `packages/`, `artifacts/`, `lib/`, etc. must appear as `module` nodes.
- **Query before rebuild.** Relational questions → `query_graph.py` first.
- **Authoritative > inferred.** `invokes` from `docs/skill-graph.md` + `SKILL-INDEX.md` **Calls:** lines are authoritative; `references` edges are hypotheses.
- **Shrink guard.** No `--force` unless user confirms or graph is corrupt.
- **Handoff sync.** Every `memory-handoff` → `--incremental` build.
- **No secrets.** Skip `.env`, credentials, tokens by path name.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just grep" | Grep misses invoke chains and handoff lineage. Query the graph. |
| "Graph is stale, full rebuild" | Try `--incremental` first; authoritative sources may be unchanged. |
| "INFERRED edge = fact" | Read `source_file` / `provenance` before acting. |
| "Skip graph on handoff" | Next agent loses relational context. |
| "Need Graphify pip package" | Native stdlib scripts; patterns only, no install. |
| "Only for agent-loom" | Bootstrap in every project via `project-setup`. |
| "Many skills = skills-only graph" | Wrong — repo-wide scan always runs; read build stdout `Why:` line. |

---

## Workflow

### Step 1 — Check existing graph
Read `GRAPH_INDEX.md` and `GRAPH_REPORT.md` when present.

### Step 2 — Build or update
```bash
python3 .agents/skills/knowledge-graph/scripts/build_graph.py              # full repo scan
python3 .agents/skills/knowledge-graph/scripts/build_graph.py --incremental  # handoff/default
python3 .agents/skills/knowledge-graph/scripts/build_graph.py --force       # override shrink guard
python3 .agents/skills/knowledge-graph/scripts/build_graph.py --strict      # fail if source on disk but 0 modules
```
**Stdout always prints:** auto mode label, **why** that label was chosen, and **scan layers** (skills, code dirs, docs, memory). Read it before assuming skills-only — both modes scan the full repository.

### Step 3 — Query
```bash
python3 .agents/skills/knowledge-graph/scripts/query_graph.py query "memory handoff connections"
python3 .agents/skills/knowledge-graph/scripts/query_graph.py path memory-handoff knowledge-graph
python3 .agents/skills/knowledge-graph/scripts/query_graph.py explain validate-skills
```
Cite `path`, `confidence`, and `provenance` for every hit. **`routing_note`** in JSON output confirms authoritative-first ordering — prefer `invokes` edges from `skill-graph.md` over INFERRED heuristics when choosing skills.

### Step 4 — Health audit (optional / validate-skills hook)
```bash
python3 .agents/skills/knowledge-graph/scripts/graph_health.py
```

### Step 5 — Report
Summarize: mode, node/edge counts, authoritative vs inferred ratio, hub nodes, communities, top query results.

---

## Handoff Hook (mandatory for memory-handoff)

After appending to `agent-handoffs.md`:
```bash
python3 .agents/skills/knowledge-graph/scripts/build_graph.py --incremental
```
If build fails, note in handoff `### Graph` — do not block save.

---

## Output Format

```markdown
## Knowledge graph — [full | incremental | query | health]

Mode: [skill-library | application]
Stats: [N] nodes, [E] edges ([A] authoritative invokes)
Hub nodes: [top 3]
Query: "[question]" → [matches with confidence tags]
Files: graph.json, call-graph.json, GRAPH_INDEX.md, GRAPH_REPORT.md
```

---

## Verification

- [ ] `graph.json`, `GRAPH_INDEX.md`, `GRAPH_REPORT.md` exist under `docs/knowledge-graph/`
- [ ] Build stdout shows `repo-wide source` layer (not skills-only)
- [ ] Consumer repos with code have `module` nodes in `graph.json` stats
- [ ] `call-graph.json` present when mode=skill-library
- [ ] Shrink guard respected (or `--force` approved)
- [ ] Query results cite path + confidence + provenance
- [ ] Handoff hook ran `--incremental` when invoked from `memory-handoff`
- [ ] No secrets or external URLs in graph artifacts

---

## Red Flags

- Full graph rebuild run before query_graph for relational ask
- Inferred edges override authoritative Calls: from SKILL-INDEX
- Repo walk skipped — partial graph presented as complete
- graph.json stale versus latest handoff not rebuilt
## Reference Files

- `references/schema.md` — node/edge types, provenance priority
- `references/integration.md` — producers/consumers, project-setup bootstrap
- `scripts/build_graph.py` — full/incremental build
- `scripts/query_graph.py` — query, path, explain
- `scripts/graph_health.py` — dangling invokes, stale graph, orphan skills

---

## File Output

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | knowledge-graph | docs/knowledge-graph/ | [N] nodes, [E] edges, mode=[mode] |
```

---

## Examples

<examples>
  <example>
    <input>Build a knowledge graph for this project.</input>
    <output>
Ran `build_graph.py` → mode=skill-library, 120 nodes, 412 edges (164 authoritative invokes). Hubs: universal-skill-creator, validate-skills, secure-skill. Saved to `docs/knowledge-graph/`. See `GRAPH_REPORT.md` for communities and suggested questions.
    </output>
  </example>
  <example>
    <input>How does memory-handoff connect to knowledge-graph?</input>
    <output>
`query_graph.py path memory-handoff knowledge-graph` → 1 hop via `invokes` [EXTRACTED, provenance: memory-handoff/SKILL.md]. Neighbors: memory-capture, agent-handoffs [recorded_in].
    </output>
  </example>
</examples>

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Knowledge graph: [full/incremental/query/health]
Mode: [skill-library|application] | Nodes: [N] | Edges: [E]
Authoritative invokes: [A] | EXTRACTED: [E] | INFERRED: [I]
Shrink guard: [ok/refused/forced] | Handoff sync: [yes/no]
Consumers notified: [list or n/a]
```
