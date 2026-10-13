---
name: mcp-knowledge-graph
description: >
  Use this when reading or writing cross-run pipeline state via the
  neo4j-memory MCP — at end of any phase that produces cross-run signal
  (especially Phase 4 feedback), when learning-engine reads recurring-pattern
  signals, when baseline-manager / metrics-collector / drift-detector /
  improvement-planner persist observations, or when correlating defects /
  baselines / skills across runs. Covers entity / relation / observation
  patterns for Run, Phase, Agent, Skill, Pattern, Defect, Baseline, Patch
  plus the JSONL fallback when G04 mcp-health is RED.
  Triggers: neo4j, neo4j-memory, MCP, knowledge graph, cross-run, entity, relation, observation, fallback, JSONL.
---

# mcp-knowledge-graph (SDK-mode, v1.0.0)

Cross-run pipeline state lives in a **persistent knowledge graph** served by the `mcp__neo4j-memory__*` MCP. This skill is the single source of truth for entity shapes, relation types, observation patterns, and the JSONL fallback that keeps the pipeline from halting when Neo4j is unreachable.

The graph complements — does NOT replace — the per-run `runs/<run-id>/decision-log.jsonl`. The decision log is intra-run; the graph is cross-run.

## When to Use

- End of any phase that produces cross-run signal (Phase 4 Feedback is the primary writer)
- `learning-engine` reading recurring-pattern signals before deciding which patches to auto-apply
- `baseline-manager` writing `Baseline` updates with `(Baseline)-[:UPDATED_IN]->(Run)` relation
- `metrics-collector` writing per-agent `quality_score` as observation on the `(Agent)-[:OBSERVED_IN]->(Run)` edge
- `sdk-skill-drift-detector` writing `Defect` entities linked to the `Phase` that introduced them
- `improvement-planner` querying the graph for recurring-pattern signals to decide which patches to file
- Any agent correlating across runs: "was this defect seen before", "is this skill drifting", "which baselines regressed"

## When NOT to Use

- Single-run state — use `decision-log.jsonl` (per-run, append-only)
- Short-lived preferences or one-off facts — use local file memory
- Anything user-private or credential-bearing — graph is shared; never write secrets
- Intra-wave handoff between agents — use `runs/<run-id>/<phase>/context/<agent>-summary.md`
- If `G04 mcp-health` is RED at phase start — skip MCP writes entirely and take the JSONL fallback path (see below)

## Entity Types

| Entity   | Keyed By                    | Notes                                               |
| -------- | --------------------------- | --------------------------------------------------- |
| Run      | `run-<uuid>`                | Created at end of Phase 4 by `metrics-collector`    |
| Phase    | `<run-id>:<phase-name>`     | One per phase per run                               |
| Agent    | `<agent-name>`              | Global; name matches `agents/<name>.md`     |
| Skill    | `<skill-name>@<version>`    | Version-scoped; new node on bump                    |
| Pattern  | `pattern-<slug>`            | Created on first occurrence, observations on recur  |
| Defect   | `defect-<run-id>-<seq>`     | Written by `root-cause-tracer`                      |
| Baseline | `baseline-<metric>`         | One node per metric; observations accumulate        |
| Patch    | `patch-<run-id>-<seq>`      | Written by `learning-engine` on auto-apply          |

## Entity Creation Pattern

**At end of Phase 4**, `metrics-collector` creates the `Run` entity in a single batched call:

```
create_entities([
  {name: "run-f47ac10b", entityType: "Run", observations: [
    "pipeline_version: sdk-pipeline@0.7.0",
    "started: 2026-04-18T09:00:00Z",
    "ended: 2026-04-18T09:47:00Z",
    "pipeline_quality: 0.87",
    "learning_patches_applied: 2"
  ]},
  {name: "run-f47ac10b:intake", entityType: "Phase", observations: [...]},
  {name: "run-f47ac10b:design", entityType: "Phase", observations: [...]},
  ...
])
```

**On recurrence** (`improvement-planner` sees the same signal in run N and run N-1), create a `Pattern` entity:

```
create_entities([{
  name: "pattern-missing-leak-detection",
  entityType: "Pattern",
  observations: [
    "first_seen: run-a1b2",
    "signal: testing-lead did not register the active language adapter's leak-detection harness",
    "recurrence_count: 2",
    "proposed_remediation: add to tdd-patterns skill"
  ]
}])
```

## Relation Creation Pattern

Relations describe how entities connect across a run and across runs. Create them in batches after all endpoint entities exist.

Canonical relations:

| Relation                           | Example                                                    |
| ---------------------------------- | ---------------------------------------------------------- |
| `(Run)-[:HAS_PHASE]->(Phase)`      | Links run to its phases                                    |
| `(Agent)-[:OBSERVED_IN]->(Run)`    | Per-agent quality_score on observations of the edge        |
| `(Defect)-[:INTRODUCED_IN]->(Phase)` | Root-cause tracing points to the phase that introduced it |
| `(Defect)-[:DETECTED_IN]->(Phase)` | Phase that caught it (usually testing)                     |
| `(Patch)-[:APPLIED_TO]->(Agent\|Skill)` | Learning-engine patch target                           |
| `(Patch)-[:MOTIVATED_BY]->(Pattern)` | Which recurring pattern motivated the patch              |
| `(Baseline)-[:UPDATED_IN]->(Run)`  | Baseline value history                                     |
| `(Skill)-[:SUPERSEDES]->(Skill)`   | Version bumps (`skill@1.2.0` supersedes `skill@1.1.0`)     |

Example batched write at end of Phase 4:

```
create_relations([
  {from: "run-f47ac10b", to: "run-f47ac10b:testing", relationType: "HAS_PHASE"},
  {from: "sdk-testing-lead", to: "run-f47ac10b", relationType: "OBSERVED_IN"},
  {from: "defect-f47ac10b-001", to: "run-f47ac10b:design", relationType: "INTRODUCED_IN"},
  {from: "defect-f47ac10b-001", to: "run-f47ac10b:testing", relationType: "DETECTED_IN"},
  {from: "patch-f47ac10b-001", to: "tdd-patterns@1.3.0", relationType: "APPLIED_TO"},
  {from: "patch-f47ac10b-001", to: "pattern-missing-leak-detection", relationType: "MOTIVATED_BY"}
])
```

## Observation Pattern

Observations are short strings appended to an entity over its lifetime. They are the canonical place to record evolving state.

**On skill patch**, `learning-engine` appends observations to the target `Skill` entity recording the patch_id and confidence:

```
add_observations([{
  entityName: "tdd-patterns@1.3.0",
  observations: [
    "patched_in: run-f47ac10b",
    "patch_id: patch-f47ac10b-001",
    "confidence: high",
    "trigger: pattern-missing-leak-detection recurrence=2",
    "devil_verdict: ACCEPT",
    "user_notified: true"
  ]
}])
```

**Baseline updates** append one observation per metric change:

```
add_observations([{
  entityName: "baseline-pipeline-quality",
  observations: ["run-f47ac10b: 0.87 (prev 0.82, +6.1%)"]
}])
```

## Example Cypher Queries

Three queries that `improvement-planner` / `learning-engine` actually run:

**1. Recurring patterns in the last 5 runs:**

```cypher
MATCH (p:Pattern)<-[:MOTIVATED_BY]-(patch:Patch)-[:APPLIED_TO]->(s:Skill)
MATCH (patch)<-[:HAS_PATCH]-(r:Run)
WHERE r.started > datetime() - duration('P30D')
RETURN p.name AS pattern, count(patch) AS occurrences, collect(DISTINCT s.name) AS skills_touched
ORDER BY occurrences DESC LIMIT 10
```

**2. Per-agent quality trend across runs:**

```cypher
MATCH (a:Agent {name: "sdk-testing-lead"})-[obs:OBSERVED_IN]->(r:Run)
RETURN r.name AS run, obs.quality_score AS score, r.started AS when
ORDER BY r.started DESC LIMIT 10
```

**3. Defects introduced in design phase but detected in testing (phase-miss signal):**

```cypher
MATCH (d:Defect)-[:INTRODUCED_IN]->(p1:Phase), (d)-[:DETECTED_IN]->(p2:Phase)
WHERE p1.name ENDS WITH ":design" AND p2.name ENDS WITH ":testing"
RETURN d.name, p1.name AS introduced, p2.name AS detected
ORDER BY d.name DESC LIMIT 20
```

## GOOD and BAD Examples

### GOOD: batch 10 entity creations into one `create_entities` call

```
create_entities([
  {name: "run-f47ac10b", entityType: "Run", observations: [...]},
  {name: "run-f47ac10b:intake", entityType: "Phase", observations: [...]},
  {name: "run-f47ac10b:design", entityType: "Phase", observations: [...]},
  {name: "run-f47ac10b:impl", entityType: "Phase", observations: [...]},
  {name: "run-f47ac10b:testing", entityType: "Phase", observations: [...]},
  {name: "run-f47ac10b:feedback", entityType: "Phase", observations: [...]},
  {name: "defect-f47ac10b-001", entityType: "Defect", observations: [...]},
  {name: "defect-f47ac10b-002", entityType: "Defect", observations: [...]},
  {name: "patch-f47ac10b-001", entityType: "Patch", observations: [...]},
  {name: "patch-f47ac10b-002", entityType: "Patch", observations: [...]}
])
```

Why: one round-trip, atomic from the writer's perspective, ~10x faster than per-entity calls.

### BAD: one `create_entities` call per entity

```
create_entities([{name: "run-f47ac10b", ...}])
create_entities([{name: "run-f47ac10b:intake", ...}])
create_entities([{name: "run-f47ac10b:design", ...}])
... (10 more calls)
```

Why wrong: 10 round-trips where 1 would do. On flaky networks the probability that ALL succeed is `(1-p)^10` — ten chances to partially-fail and leave the graph inconsistent.

### GOOD: check `G04 mcp-health` at phase start; skip MCP if down

```
# At phase start
if guardrail G04 mcp-health != PASS:
    log event: "MCP down; taking JSONL fallback path for this run"
    set local flag: USE_JSONL_FALLBACK = true
    # All subsequent writes go to runs/<run-id>/feedback/*.jsonl
    return
# Otherwise proceed with neo4j-memory calls
create_entities([...])
```

Why: fail fast, single branch point, no retry storms, no catch blocks polluting every call site.

### BAD: try MCP call, catch, retry

```
for attempt in 1..3:
    try:
        create_entities([...])
        break
    except MCPConnectionError:
        sleep(2 ** attempt)
# Every single MCP call repeats this pattern. No clean fallback. Retry storm.
```

Why wrong: per-call retry loops multiply latency, obscure the real failure, and the phase still has no coherent fallback. Health-check once, branch once.

### GOOD: use `find_memories_by_name` for exact lookups

```
# Looking up a specific skill version
find_memories_by_name(["tdd-patterns@1.3.0"])
```

Why: O(1) index lookup, deterministic, returns `null` cleanly when absent.

### BAD: use `search_memories` for exact lookups

```
search_memories("tdd-patterns@1.3.0")
```

Why wrong: `search_memories` is a fuzzy/embedding search — slower, may return unrelated matches ranked above the exact one, and noisy for callers who want a single answer.

### GOOD: version-scoped Skill nodes

```
# Bumping tdd-patterns 1.2.0 -> 1.3.0 creates a NEW node and a SUPERSEDES relation:
create_entities([{name: "tdd-patterns@1.3.0", entityType: "Skill", observations: [...]}])
create_relations([{from: "tdd-patterns@1.3.0", to: "tdd-patterns@1.2.0", relationType: "SUPERSEDES"}])
```

Why: history is preserved; queries can ask "which skill versions were live during run X" without guessing.

### BAD: mutate a single Skill node across versions

```
# Appending "version: 1.3.0" observation onto tdd-patterns node with no version suffix
add_observations([{entityName: "tdd-patterns", observations: ["bumped to 1.3.0 in run-f47ac10b"]}])
```

Why wrong: loses the ability to query by live-version at time-of-run, makes `SUPERSEDES` chains impossible, collapses all history into an unordered pile of observations.

## Fallback Behavior

**Decision rule**: `G04 mcp-health` guardrail is checked at phase start. If it fails (Neo4j unreachable, MCP server not responding, container down), the phase sets `USE_JSONL_FALLBACK=true` and all would-be MCP writes go to JSONL files instead:

| MCP intent                         | Fallback file                                               |
| ---------------------------------- | ----------------------------------------------------------- |
| `create_entities` (Run)            | `runs/<run-id>/feedback/run-entity.jsonl`                   |
| `create_entities` (Defect/Pattern) | `runs/<run-id>/feedback/defects-patterns.jsonl`             |
| `add_observations` (Skill patch)   | `evolution/knowledge-base/prompt-evolution-log.jsonl`       |
| `add_observations` (Baseline)      | `baselines/shared/baseline-history.jsonl`                          |
| `add_observations` (Agent quality) | `runs/<run-id>/feedback/agent-performance.jsonl`            |
| `create_relations` (any)           | `runs/<run-id>/feedback/relations.jsonl`                    |

**Backfill**: on the next run where `G04 mcp-health` passes, `metrics-collector` runs `scripts/migrate-jsonl-to-neo4j.py` which replays every JSONL file produced during fallback mode, deduplicating by `(entity_name, observation_content)` so idempotency is preserved. Backfill is recorded as an observation on the Run entity: `"backfilled_from: [run-a1b2, run-c3d4]"`.

**Never halt**. A down MCP is a WARN, not a BLOCKER. The JSONL fallback is lossless; backfill restores the graph on the next healthy run.

## Consumers

- `metrics-collector` (F1) — writes Run + per-Agent observations
- `sdk-skill-drift-detector` + `sdk-skill-coverage-reporter` (F4) — write drift/coverage observations
- `learning-engine` (F7) — reads Pattern recurrence, writes Patch entities + Patch relations
- `baseline-manager` (F8) — writes Baseline observations
- `improvement-planner` (F6) — reads Pattern / Defect / quality-trend queries as input

## Common Mistakes

1. **Writing per-entity instead of batching** — see GOOD/BAD #1.
2. **Missing health check, adding per-call try/except** — see GOOD/BAD #2.
3. **Fuzzy search for exact lookup** — see GOOD/BAD #3.
4. **Mutating a Skill node across versions** — see GOOD/BAD #4. Always create a new version-suffixed node.
5. **Writing secrets as observations** — the graph is shared. Never write credentials, PII, or user-private text.
6. **Creating relations before endpoint entities exist** — `create_entities` first, then `create_relations` in a second call.
7. **Forgetting backfill** — if this run used the JSONL fallback, the NEXT healthy run must backfill before writing new data, else the graph drifts out of sync.
