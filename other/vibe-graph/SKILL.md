---
name: vibe-graph
description: >
  Dual-layer dependency graph for vibe-* projects. No external packages.
  DEPENDENCY_GRAPH.json maps file-level relationships with confidence
  tagging: EXTRACTED (verified from source, confidence 1.0), INFERRED
  (derived from specs/patterns, 0.6–0.95), AMBIGUOUS (flagged for review).
  Rationale nodes capture WHY, HACK, DECISION comments from source files —
  surfaced during bug diagnosis and review to prevent intent drift.
  God nodes identify highest-coupling files — read first in review,
  flagged in bug diagnosis, blocked from simultaneous parallel writes.
  CONCEPT_GRAPH.json maps semantic relationships (features, agents,
  models, components). graph.html is an interactive visual.
  Auto-updated via git diff. Queried by vibe-fix-bug, vibe-test,
  vibe-review, vibe-parallel. Primary value is semantic navigation:
  accurate blast-radius, intent-drift detection via rationale nodes, and
  safe parallel dispatch via god nodes — not raw token savings (current
  models have large context windows + prompt caching, so the graph is a
  precision/focus overlay, not a way to avoid loading context).
  Triggers on "vibe-graph: build", "vibe-graph: update", "vibe-graph: init",
  "vibe-graph: rebuild", "vibe-graph: query", "vibe-graph: status".
---

# Vibe Graph Skill

Dual-layer dependency graph for vibe-* projects.
Starts as a spec graph before code exists.
Grows into a full dependency map as the project is built.
Updated automatically from git diff — no agent self-reporting.

Three concepts from graphify integrated throughout:
1. **Relationship confidence tagging** — EXTRACTED / INFERRED / AMBIGUOUS on every edge
2. **Rationale nodes** — WHY, HACK, DECISION comments extracted from source files
3. **God nodes** — highest-degree files surfaced for priority review and safe parallel dispatch

---

## Execution model — extract with judgment, compute with the script

Split the work so the model never hand-simulates graph algorithms (a real
silent-error risk on any non-trivial codebase):

- **Extraction is the LLM's job** (needs code comprehension): read the code / specs
  and write `vibe/graph/DEPENDENCY_GRAPH.json` and `CONCEPT_GRAPH.json` — the nodes,
  edges, confidence tags, and rationale.
- **Computation is `scripts/graph.py`'s job** (deterministic): god-node degree
  ranking, blast-radius queries, stats, and the `graph.html` render. **Run it via
  Bash — do not mentally sort degrees or traverse the graph.** The Python shown in
  the reference files documents the algorithm; the script is what actually runs it.

Resolve the script path across install layouts:
```bash
GRAPH=$(ls ~/.claude/skills/vibe-graph/scripts/graph.py \
           ~/.claude/plugins/marketplaces/*/skills/vibe-graph/scripts/graph.py 2>/dev/null | head -1)
python3 "$GRAPH" godnodes --top 5      # compute god nodes → .graph-meta.json
python3 "$GRAPH" query src/x.py        # blast radius (certain / probable / ambiguous + rationale)
python3 "$GRAPH" stats                 # nodes, edges, confidence + AMBIGUOUS count
python3 "$GRAPH" flow                  # regenerate vibe/graph/FLOW.md (execution flow)
python3 "$GRAPH" html                  # render vibe/graph/graph.html
```

---

## The two layers

### Layer 1 — DEPENDENCY_GRAPH.json (file-level)
Maps technical relationships between files.
What imports what. What's tested by what. What route calls what handler.
Every edge tagged EXTRACTED / INFERRED / AMBIGUOUS with confidence score.
Rationale nodes stored per file — why the file works the way it does.
Used by: bug diagnosis, blast radius tracing, test generation, parallel safety.

**Two optional node fields feed the execution-flow layer (see FLOW.md below):**
- `"entrypoint": true` — this file is where execution *starts* (server bootstrap,
  CLI `main`, worker entry, a route-registration root). Mark these during extraction;
  they are the roots FLOW.md walks from. Backward-compatible — a graph with none just
  yields a FLOW.md that asks for them.
- `"calls": [{ "from": "fnA", "to_file": "src/y.ts", "to": "fnB", "confidence": .., "source": .. }]`
  — optional *function-level* call edges, for the "which function calls which" detail.
  Same confidence/source tagging as imports. Omit when you didn't trace functions;
  FLOW.md falls back to file-level reach from the import edges.

### Layer 2 — CONCEPT_GRAPH.json (concept-level)
Maps semantic relationships between features, agents, models, components.
What concept owns what files. What concepts depend on each other.
Starts from SPEC.md and ARCHITECTURE.md before code exists.
Nodes transition from `planned` to `built` as features are implemented.
Used by: review boundary checking, impact assessment, progress tracking.

---

## Commands

```
vibe-graph: init      ← called by vibe-new-app after scaffold created
vibe-graph: build     ← called by vibe-init after CODEBASE.md written
vibe-graph: update    ← called by vibe-add-feature and vibe-fix-bug at session end
vibe-graph: rebuild   ← full rebuild from scratch (recovery command)
vibe-graph: query [file or concept]  ← manual query during debugging
vibe-graph: status    ← graph health, coverage, god nodes, ambiguous edges
```

---

## Node states

Every node in both graphs has one of three states:

```
planned  → exists in SPEC.md or ARCHITECTURE.md, no code yet
           all edges are INFERRED at this stage
partial  → some tasks complete, feature not fully implemented
built    → all tasks complete, file exists, EXTRACTED edges confirmed
deleted  → file was removed — state transitions, node never removed
```

---

## Step 0 — Pre-flight

```bash
# Verify git is initialised
git status 2>/dev/null || { echo "Not a git repo — vibe-graph requires git"; exit 1; }

# Create graph directory
mkdir -p vibe/graph

# Check for existing graph
ls vibe/graph/DEPENDENCY_GRAPH.json 2>/dev/null && echo "GRAPH EXISTS" || echo "NEW GRAPH"
```

---

## Command: vibe-graph init

**Called by:** `vibe-new-app` after scaffold is created.
**Purpose:** Build the spec graph from SPEC.md and ARCHITECTURE.md
before any code exists. All nodes are `planned` state.
All edges are INFERRED — code hasn't been written yet.

Read `references/SPEC_TO_GRAPH.md` before this step.

**Step 1 — Read planning documents:**
```bash
cat vibe/SPEC.md
cat vibe/ARCHITECTURE.md
cat vibe/PLAN.md 2>/dev/null
cat AGENT_ARCH.md 2>/dev/null
```

**Step 2 — Extract planned concepts from SPEC.md:**

For each feature, agent, model, route, and component in SPEC.md:
Create a concept node with `state: planned`.
Apply confidence scores per SPEC_TO_GRAPH.md rules.
Explicit feature dependencies → `confidence: 0.95`.
Acceptance criteria references → `confidence: 0.90`.

**Step 3 — Extract planned file nodes from ARCHITECTURE.md:**

For each planned file in the folder structure section:
Create a file node with `state: planned`.
Assign concept with INFERRED tag and appropriate confidence.
Folder comment = 0.85. File naming = 0.85. Pattern inference = 0.85.

**Step 4 — For agentic projects, read AGENT_ARCH.md:**
Extract agent topology — which agents call which, tool assignments,
verifier relationships, HITL checkpoints.
All AGENT_ARCH.md edges: `source: INFERRED, confidence: 0.95`.

**Step 5 — Write initial graphs:**

Write `vibe/graph/DEPENDENCY_GRAPH.json` — all planned file nodes.
Write `vibe/graph/CONCEPT_GRAPH.json` — all planned concept nodes.
Write `vibe/graph/.graph-meta.json`:
```json
{
  "version": 2,
  "created": "[ISO timestamp]",
  "last_updated": "[ISO timestamp]",
  "last_commit": "[git rev-parse HEAD, or empty if no commits yet]",
  "update_count": 0,
  "mode": "spec",
  "nodes_planned": 0,
  "nodes_built": 0,
  "god_nodes": [],
  "ambiguous_count": 0,
  "project": "[project name]"
}
```

**Step 6 — Generate initial graph.html and FLOW.md:**
Read `references/GRAPH_HTML_TEMPLATE.md` for visual format.
Planned nodes: lighter colour, dashed border.
INFERRED edges: dashed lines. EXTRACTED edges: solid lines.
No EXTRACTED edges yet — all relationships are INFERRED at init.
Also run `python3 "$GRAPH" flow` so `vibe/graph/FLOW.md` exists from the start
(it will say "no entry points marked yet" until code is built — that's expected).

**Step 7 — Tell vibe-new-app:**
```
vibe-graph: init complete
  Planned concepts: [N]
  Planned files:    [N]
  INFERRED edges:   [N] (all edges — code not yet written)
  Graph location:   vibe/graph/
  State: SPEC GRAPH — edges transition to EXTRACTED as files are built
```

---

## Command: vibe-graph build

**Called by:** `vibe-init` after CODEBASE.md is written.
**Purpose:** One-time build for existing projects from CODEBASE.md.

Read `references/CODEBASE_TO_GRAPH.md` before this step.

**Step 1 — Read CODEBASE.md in full:**
```bash
cat vibe/CODEBASE.md
```

**Step 2 — Parse CODEBASE.md sections into nodes with confidence tags:**

Routes, models, components, agents — per CODEBASE_TO_GRAPH.md.
All relationships extracted from CODEBASE.md: `source: EXTRACTED, confidence: 1.0`.

**Step 3 — Attempt rationale extraction:**
For each file found in CODEBASE.md, if the source file is accessible:
```bash
cat [file_path] | grep -n "# WHY:\|# HACK:\|# NOTE:\|# IMPORTANT:\|# REASON:\|# DECISION:\|# TRADEOFF:\|# WARNING:\|# TODO:\|# FIXME:" 2>/dev/null
```
Extract rationale comments and first-paragraph docstrings.
Store in `rationale` array on the file node.
If file not accessible — leave `rationale: []`, populate on first update.

**Step 4 — Compute hashes for all files:**
```bash
git log -1 --format="%H %ai" -- [file_path]
git hash-object [file_path]
```

**Step 5 — Build concept assignments:**
Per CODEBASE_TO_GRAPH.md concept assignment rules.
Feature folder Touches field → EXTRACTED, 1.0.
Naming match → INFERRED, 0.85.
Fallback → foundation, INFERRED, 0.70.

**Step 6 — Compute god nodes:** run the engine, don't compute by hand —
`python3 "$GRAPH" godnodes --top 5` (writes `.graph-meta.json`). The Python below
documents the algorithm the script implements; it is not for you to execute mentally.
```python
import json
from pathlib import Path

graph = json.loads(Path('vibe/graph/DEPENDENCY_GRAPH.json').read_text())

degree = {}
for file_path, node in graph.items():
    if not isinstance(node, dict):
        continue
    imports = node.get('imports', [])
    imported_by = node.get('imported_by', [])
    degree[file_path] = len(imports) + len(imported_by)

god_nodes = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:5]

result = []
for file_path, connections in god_nodes:
    node = graph.get(file_path, {})
    entry = {
        'file': file_path,
        'connections': connections,
        'concept': node.get('concept', 'foundation'),
        'type': node.get('type', 'unknown'),
        'risk': 'HIGH' if connections > 10 else 'MEDIUM' if connections > 5 else 'LOW'
    }
    if connections > 10:
        entry['srp_flag'] = True
        entry['srp_note'] = f'{connections} connections — consider splitting for SRP'
    result.append(entry)

print(json.dumps(result, indent=2))
```

Write god nodes to `.graph-meta.json`.

**Step 7 — Collect AMBIGUOUS edges:**
Run `collect_ambiguous()` per CODEBASE_TO_GRAPH.md.
Write count and list to `.graph-meta.json`.

**Step 8 — Write all output files.**
Then regenerate the derived views: `python3 "$GRAPH" html` and
`python3 "$GRAPH" flow` (writes `vibe/graph/FLOW.md` — the execution-flow map).

**Step 9 — Tell vibe-init:**
```
vibe-graph: build complete
  Files indexed:    [N]
  Concepts mapped:  [N]
  EXTRACTED edges:  [N]
  INFERRED edges:   [N]
  AMBIGUOUS edges:  [N] (see vibe-graph: status for details)
  Rationale nodes:  [N] (WHY/HACK/DECISION comments extracted)
  God nodes:        [top file] ([N] connections), [2nd], [3rd]
  State: BUILT — graph reflects current codebase
```

---

## Command: vibe-graph update

**Called by:** `vibe-add-feature` and `vibe-fix-bug` at session end.
**Purpose:** Incremental update — only files changed this session.

**Step 1 — Find files changed since the graph was last updated:**

Work is usually committed per task before this runs, so `git diff HEAD` alone would see
nothing. Diff from the commit recorded at the last update (`last_commit` in
`.graph-meta.json`) to now, plus anything still uncommitted:
```bash
META=vibe/graph/.graph-meta.json
BASE=$(python3 -c "import json;print(json.load(open('$META')).get('last_commit',''))" 2>/dev/null)
if [ -n "$BASE" ] && git cat-file -e "$BASE" 2>/dev/null; then
  git diff --name-only "$BASE" HEAD        # committed since last update
else
  git diff --name-only HEAD~1 HEAD 2>/dev/null   # no baseline yet: last commit
fi
git diff --name-only HEAD                  # uncommitted working-tree changes
git diff --name-only --cached              # staged
```
Take the union, de-duplicated.

**Step 2 — For each changed file:**

Check if it's a new file (not in graph) or an update to an existing node.

**Step 3 — Transition INFERRED → EXTRACTED:**

For each changed file, read it and extract actual imports:
```bash
# Python
grep -n "^import \|^from " [file_path]

# TypeScript/JS
grep -n "^import \|^require(" [file_path]

# Go
grep -n "^import" [file_path]
```

For each actual import found:
- If it matches an INFERRED edge → update to `EXTRACTED, confidence: 1.0`, add line number evidence
- If it's a new import not in the graph → add as new EXTRACTED edge
- If a planned INFERRED edge is NOT found in actual imports → mark as AMBIGUOUS, flag in status

**Step 4 — Extract rationale comments from changed files:**
```bash
grep -n "# WHY:\|# HACK:\|# NOTE:\|# IMPORTANT:\|# REASON:\|# DECISION:\|# TRADEOFF:\|# WARNING:" [file_path]
# Also extract first 5 lines of module docstring if present
```
Update `rationale` array on the node. Append new entries, never overwrite existing.

**Step 5 — Update concept node state:**

For each concept affected by changed files:
- If all planned files now have state=built → concept state=built
- Update `files` list, `tasks_complete` count
- Update concept edges: if corresponding file import was confirmed → edge source = EXTRACTED

**Step 6 — Recompute god nodes:** run `python3 "$GRAPH" godnodes --top 5` (do not
recompute by hand). God nodes change as files are added and connections grow.
Recompute after every update that adds 3+ new edges.

**Step 7 — Update graph.html and FLOW.md:**
Re-render subgraph of changed nodes and their neighbours.
Transition planned→built (colour change). INFERRED→EXTRACTED (dashed→solid line).
Then run `python3 "$GRAPH" flow` to regenerate `vibe/graph/FLOW.md` so the
execution-flow map reflects the change. Entry points are the nodes tagged
`"entrypoint": true`; if a change added/removed one (or a new call path), it
shows up here. FLOW.md is fully derived — never hand-edit it.

**Step 8 — Update .graph-meta.json:**
```json
{
  "last_updated": "[ISO timestamp]",
  "last_commit": "[output of git rev-parse HEAD — the baseline for the next update]",
  "update_count": "[N+1]",
  "files_updated_this_run": "[N]",
  "mode": "incremental",
  "god_nodes": "[recomputed list]",
  "ambiguous_count": "[updated count]",
  "inferred_to_extracted_this_run": "[N]"
}
```

**Step 9 — Report back:**
```
vibe-graph: update complete
  Files re-indexed:          [N] (from git diff)
  EXTRACTED edges confirmed: [N] (INFERRED → EXTRACTED transitions)
  New EXTRACTED edges:       [N]
  Rationale nodes added:     [N]
  AMBIGUOUS edges:           [N] (run vibe-graph: status to review)
  God nodes updated:         [top file] ([N] connections)
  Nodes built/total:         [N]/[N] ([%] complete)
```

---

## Command: vibe-graph query

**Called by:** `vibe-fix-bug`, `vibe-test`, `vibe-review` at task start.
Also available manually for debugging.

For a **file** query, run the engine — it computes the blast radius (certain /
probable / ambiguous) and surfaces rationale deterministically:
`python3 "$GRAPH" query <file> --depth 2`. Use `python3 "$GRAPH" stats` for the
health/ambiguous summary. Read `references/GRAPH_QUERY_PATTERNS.md` for the concept
query protocol and how to interpret results.

```
vibe-graph: query scout_agent.py
vibe-graph: query competitor-discovery
vibe-graph: query POST /api/brand-dna
```

**Returns for a file query:**

```
DEPENDENCY GRAPH — src/agents/scout_agent.py
─────────────────────────────────────────────
State:      built
Concept:    competitor-discovery [EXTRACTED · 1.0]
Type:       agent

GOD NODE CHECK: Not a god node (3 connections)

RATIONALE (read before diagnosing or reviewing):
  WHY [line 12]: Directory-first approach — Tavily better SMB coverage than LinkedIn API
  HACK [line 47]: 2s rate limit — Tavily free tier hard limit
  DECISION [line 89]: Returns top 5 only — UI constraint from IdentityScreen

CERTAIN (EXTRACTED — load immediately for blast radius):
  → src/agents/base_agent.py       [EXTRACTED · 1.0 · line 3]
  → src/tools/tavily.py            [EXTRACTED · 1.0 · line 7]
  ← src/graph/pipeline.py          [EXTRACTED · 1.0 · pipeline line 12]
  ↔ tests/test_scout_agent.py
  ⇒ src/agents/verifiers/scout_verifier.py [EXTRACTED · 1.0]
  ⇒ GET /api/competitors/{brand_id}

PROBABLE (INFERRED ≥0.80 — load if needed):
  → src/utils/rate_limiter.py      [INFERRED · 0.75 · instantiated at line 34]

AMBIGUOUS (human review needed):
  (none)

Blast radius — certain: 6 files · probable: +1 · ambiguous: 0
→ These are the files to focus on / read fully. The value is precision
  (exactly what this change touches), not avoiding the rest of the context.
```

**Returns for a god node:**
```
⚠️ GOD NODE — src/agents/base_agent.py
  Connections: 14 (HIGH)
  SRP flag: Consider splitting — 14 connections indicates high coupling
  Files connected: [list the 14]
  → Any bug here affects 14 files. Any review here is a priority read.
```

**Returns for a concept query:**
```
CONCEPT GRAPH — competitor-discovery
─────────────────────────────────────
State:      built
Type:       feature

Files:
  src/agents/scout_agent.py          built  [EXTRACTED · 1.0]
  src/agents/verifiers/scout_verifier.py  built  [EXTRACTED · 1.0]
  src/api/competitors.py             built  [EXTRACTED · 1.0]
  tests/test_scout_agent.py          built  [EXTRACTED · 1.0]

Depends on:
  → brand-dna-extraction  [INFERRED · 0.95 · "uses brand industry from Brand DNA"]

Depended on by:
  ← content-gap-analysis  [EXTRACTED · 1.0]

Tasks: 6/6 complete ✅
```

---

## Command: vibe-graph rebuild

Full rebuild from scratch. Recovery command — use when graph has drifted.

1. Read all source files in the project (same as build)
2. Rebuild DEPENDENCY_GRAPH.json from scratch with full confidence tagging
3. Extract rationale from all accessible source files
4. Rebuild CONCEPT_GRAPH.json from feature folders + SPEC.md
5. Recompute god nodes
6. Collect AMBIGUOUS edges
7. Rebuild graph.html and regenerate FLOW.md (`python3 "$GRAPH" flow`)
8. Update .graph-meta.json with `mode: "full-rebuild"`

---

## Command: vibe-graph status

```
GRAPH STATUS — Brandbot
──────────────────────────────────────────────────────────
Last updated:    2026-04-13 09:15:00 (2h ago)
Update count:    14 incremental updates
Mode:            incremental

Coverage:
  Files indexed:    47/47 (100%)
  Concepts mapped:  8/8   (100%)
  EXTRACTED edges:  124   (verified from source)
  INFERRED edges:   18    (derived from specs/patterns)
  AMBIGUOUS edges:  3     (needs review — see below)
  Rationale nodes:  31    (WHY/HACK/DECISION comments)

GOD NODES (highest coupling — read first in review):
  ⚠️  src/agents/base_agent.py    14 connections · HIGH · SRP check recommended
      src/models/brand_dna.py      8 connections · MEDIUM
      src/graph/pipeline.py        7 connections · MEDIUM
      src/api/brand_dna.py         6 connections · MEDIUM
      src/config.py                5 connections · LOW

Build progress (from concept graph):
  brand-dna-extraction:    ✅ built   (6/6 files)
  competitor-discovery:    ✅ built   (6/6 files)
  content-gap-analysis:    🔄 partial (4/6 files)
  article-creation:        ⬜ planned (0/8 files)

AMBIGUOUS — needs human review:
  1. src/shared/validator.py
     Issue: Used by both brand-dna-extraction and competitor-discovery
     Action: Determine primary concept, update CODEBASE.md

  2. src/utils/rate_limiter.py → src/tools/tavily.py
     Issue: Inferred dependency, confidence 0.45
     Action: Check if RateLimiter uses Tavily directly or just wraps it

  3. src/api/auth.py
     Issue: Named 'auth' but no auth concept in CONCEPT_GRAPH
     Action: Assign to foundation or create auth concept

INFERRED EDGES (not yet confirmed by source):
  src/agents/scout_agent.py → src/utils/rate_limiter.py  (0.75)
  src/agents/analyst_agent.py → src/models/competitor.py (0.80)
  ... [N more]

Graph health: ⚠️ 3 AMBIGUOUS edges need review
  Run: vibe-graph: status to see full details
  Resolve: manually update CODEBASE.md and run vibe-graph: update

Files: vibe/graph/DEPENDENCY_GRAPH.json (47 nodes, 142 edges)
       vibe/graph/CONCEPT_GRAPH.json    (8 concepts)
       vibe/graph/graph.html            (interactive — solid=EXTRACTED, dashed=INFERRED)
       vibe/graph/FLOW.md               (execution flow — entry points → reach; derived)
       vibe/graph/.graph-meta.json      (god nodes, ambiguous count, meta)
```

---

## How vibe-fix-bug uses the graph

Read `references/GRAPH_QUERY_PATTERNS.md` for the full query protocol.

At diagnosis start, instead of loading CODEBASE.md:

```
1. Check if suspected file is a god node
   → If yes: warn about large blast radius upfront

2. Read rationale nodes for the suspected file
   → Know WHY the file works the way it does BEFORE proposing a fix
   → This prevents fixing a bug by breaking a documented design decision

3. Query blast radius with confidence tiers
   → CERTAIN (EXTRACTED): load immediately — these are definitely involved
   → PROBABLE (INFERRED ≥0.80): load if CERTAIN tier doesn't resolve
   → Skip AMBIGUOUS — flag separately

4. Query concept for upstream/downstream propagation
   → Check if bug could originate from or propagate to adjacent concepts
```

---

## How vibe-test uses the graph

At blast radius detection start:

```
1. Get changed files from git diff (already done by vibe-graph: update)
2. For each changed file: get EXTRACTED connections
   → Certain test scope (full regression)
3. For each changed file: get INFERRED ≥0.80 connections
   → Probable test scope (smoke tests)
4. Write tests tier by tier — certain first, probable second
5. Files marked ⚠️ no test — create test file
```

---

## How vibe-review uses the graph

At review start, before reading any source files:

```
1. Read god nodes from .graph-meta.json
   → These are read first — highest coupling = highest review priority
   → SRP flag on any god node > 10 connections = check for SRP violation

2. Run concept boundary pre-screening (EXTRACTED edges only)
   → Cross-concept imports = potential violations
   → AMBIGUOUS edges = surface separately, not as violations

3. Read rationale nodes for all files in scope
   → Any code that contradicts a WHY or DECISION rationale = P1 finding (intent drift)

4. Files with violations or SRP flags → deep read
5. Files with no violations, not god nodes → shallow review only
```

---

## How vibe-parallel uses the graph

Before dispatching subagents:

```
1. Check for direct file conflicts (Task A and Task B both write same file)
   → BLOCK: move one task to next wave

2. Check for god node conflicts (both tasks touch files connected to same god node)
   → WARN: ask before dispatching, consider sequencing

3. High-SRP-flag god nodes are never written by two waves simultaneously
   → Treat as implicit serialisation point
```

---

## Absolute rules

**Git diff is the only source of truth for what changed.**
Never rely on agent memory, task manifests, or Touches field alone.
`git diff --name-only HEAD` before every incremental update.

**Never fabricate confidence.**
If the evidence for an edge is weak — mark INFERRED with low confidence.
If unclear — mark AMBIGUOUS. Never upgrade AMBIGUOUS to EXTRACTED without source evidence.

**Never remove a node — only transition state.**
A deleted file transitions to `state: deleted`, not removed from the graph.
Deletion is a graph event — other files may still import it.

**Concept assignment is append-only.**
Once assigned, a file stays in its concept.
Multiple concepts → add `secondary_concepts` field.
Never reassign primary concept without logging in DECISIONS.md.

**Rationale nodes are append-only.**
New rationale comments are appended to the array.
Never overwrite or remove existing rationale entries.
If a rationale comment is deleted from source — log it as a deletion event,
don't remove it from the graph.

**AMBIGUOUS edges must be resolved, not ignored.**
`vibe-graph: status` surfaces them every time.
They accumulate until a human resolves them.
Never silently treat AMBIGUOUS as EXTRACTED.

**The graph is a read-optimisation, not a constraint.**
If diagnosis reveals a file that should be in the blast radius but isn't in the graph —
read the file, update the graph, continue.
The graph is a starting point.
