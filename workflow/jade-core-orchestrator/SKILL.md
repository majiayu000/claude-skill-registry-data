---
name: jade-core-orchestrator
description: >-
  Orchestrates JADE migration runs using strict file-based handoff and deterministic state transitions.
  Use whenever running a version migration pipeline that must process rules sequentially (rule-by-rule),
  persist artifacts to disk, and enforce phase gates before continuing.
---

# JADE Migration Orchestrator

## Objective
Run the migration pipeline as a deterministic state machine using artifact file paths only.

## Core constraints
- Never pass large JSON payloads in prompt context.
- Read/write artifacts under `artifacts/`.
- Process migration in strict Rule-by-Rule Sequential Batching.
- Do not dispatch different rules in parallel.
- Stop immediately on gate failure and persist failure reason.

## Required input
- `artifacts/00-run-config.json`

## Produced/updated artifacts
- `artifacts/00-run-state.json`
- `artifacts/phase-history.log.jsonl`
- `artifacts/rule-status.json`
- `artifacts/failure-summary.json` (on failure)
- `artifacts/PROGRESS.md` — human-readable progress table, updated on every state transition

## State machine

The orchestrator is a directed graph. Each state + outcome maps to a next state.
The `TRANSITIONS` dict drives all routing:

| State | Outcome | Next state |
|-------|---------|------------|
| INIT | OK | WORKSPACE_READY |
| WORKSPACE_READY | OK | MANIFEST_READY |
| MANIFEST_READY | OK / ARTIFACT_MISSING | TOOLING_SCOUT_READY / FAILED |
| BUILD_GATE_READY | OK / ARTIFACT_MISSING | KNOWLEDGE_GRAPH_READY / FAILED |
| KNOWLEDGE_GRAPH_READY | OK / DEPENDENCY_MISSING / ARTIFACT_MISSING | SCAN_READY / SCAN_READY / FAILED |
| SCAN_READY | OK / ARTIFACT_MISSING | RULE_BATCH_LOOP / FAILED |
| RULE_BATCH_LOOP | NEXT_RULE / NO_MORE_RULES / VERIFY_FAIL / AWAIT_AGENT / SHARD_ROLLBACK_PENDING | RULE_BATCH_LOOP / VERIFIED / RULE_RETRY / AWAITING_AGENT / AWAITING_AGENT |
| RULE_RETRY | RETRY / ESCALATE | RULE_BATCH_LOOP / RULE_ESCALATE |
| RULE_ESCALATE | OK | RULE_BATCH_LOOP |

Terminal states: DONE, FAILED, AWAITING_SOURCE_INPUT, AWAITING_AGENT.

On `VERIFY_FAIL`, the orchestrator invokes `retry_router.py` as a subprocess.
On `ESCALATE`, the rule is marked `ESCALATED` and skipped; the loop advances
to the next rule.

## Phase order
0. PHASE_0_DOCS (optional — skipped if `JadeDocumentation/` not present in workspace)
1. INIT
2. WORKSPACE_READY
3. MANIFEST_READY
4. TOOLING_SCOUT_READY
5. BUILD_GATE_READY
6. KNOWLEDGE_GRAPH_READY (advisory — builds `03.5-knowledge-graph.json`; missing/partial graph skips)
7. SCAN_READY
8. RULE_BATCH_LOOP
9. VERIFIED
10. DONE (or FAILED / AWAITING_SOURCE_INPUT)

### Phase 0 (Optional): Codebase Documentation
Before INIT, the orchestrator checks for `JadeDocumentation/` in the workspace root
(produced by the `codebase-analysis` skill). If present, it reads:
- `JadeDocumentation/migration/component-order.md` — advisory, not used for rule ordering
- `JadeDocumentation/behavior/workflows.md` — passed to the verification skill for dynamic trace scenarios

If `JadeDocumentation/` does not exist, Phase 0 is skipped silently. The pipeline
never requires documentation to proceed.

### Rule application policy (IMPORTANT)
All rules are applied **system-wide, not component-by-component**. Ordering rules
by component dependency (from `component-order.md`) would break cross-package
contracts (e.g., applying generics to Component A but not Component B causes
compilation failures). The pipeline strictly follows Rule-by-Rule Sequential
Batching — each rule is applied to ALL files before verification and commit.

### Anti-Bypass Guard (IMPORTANT)

At `RULE_BATCH_LOOP`, the Agent MUST NOT manually create a batch artifact
and mark it `DONE` or `NOOP` if flagged files exist for that rule.
Acceptable resolution paths:
1. **Transform** — Write a registry recipe script (`jade-recipe-*`) that actually applies
   the change, then dispatch it via the rule dispatcher.
2. **Defer** — Use `defer_rules.py` to rewrite `// JADE-FLAG:<rule_id>` to
   `// JADE-MODERNIZATION-DEFERRED:<rule_id> <reason>`. This preserves the
   marker as technical debt while removing it from the active pipeline.

Artifact-based bypasses (manually writing a JSON file to skip a rule) are
prohibited and constitute a pipeline integrity violation.

## Rule batch policy
For each `rule_id` in queue:
1. Run rule batch processor for that rule.
2. Run verification gate.
3. Run atomic rule commit.
4. Persist status.
5. Move to next rule.

## Halt/resume states
- `AWAITING_SOURCE_INPUT`
- `AWAITING_AGENT`
- `BUILD_GATE_FAILED`
- `VERIFICATION_FAILED`

## Agent-mode rules (recipe-registry.json entries with `"mode": "agent"`)

A rule whose registry entry carries `"mode": "agent"` skips the legacy
`05-rule-batch-<rule_id>.json` script path entirely. `agent_registry_entry`
reads `recipe-registry.json` directly — this skill never imports
`dispatcher.py` or `registry_modes.py`, and never invokes `dispatcher.py`
as a subprocess. A rule with no `"mode"` field (or `"mode": "script"`)
is completely unaffected; this is a strict backward-compatible addition.

`_process_agent_rule` gates each agent-mode rule against its shard plan
(`05-rule-shards-<rule_id>.json`, produced upstream by `plan_shards.py`)
and its checkpoint ledger (`06-shard-checkpoints-<rule_id>.json`, written
by `shard_checkpoint.py`):

1. No shard plan → `PENDING_AGENT` / `ARTIFACT_MISSING` (pipeline fails;
   the shard plan is a prerequisite this skill does not produce).
2. Shard plan present but `05-agent-tasks-<rule_id>.json` or the
   checkpoint ledger is missing → pause once for the whole rule with
   `AWAITING_AGENT.md` describing every shard's checkpoint / subagent /
   verify / gate / record / accept-or-rollback commands (`AWAIT_AGENT`).
3. Any shard still `CHECKPOINTED` (work started, not yet closed) → pause
   again (`SHARD_ROLLBACK_PENDING` → `AWAITING_AGENT`) until it is
   `ACCEPTED` or `ROLLED_BACK`.
4. A shard `ACCEPTED` in the ledger whose recorded fix status is
   `NEEDS_REVIEW` is a pipeline integrity violation → `FAILED`
   (`SHARD_NEEDS_REVIEW_ACCEPTED`) — a shard needing review must be rolled
   back, never accepted.
5. Every shard `ACCEPTED` or `ROLLED_BACK` → falls through to the same
   build-verification path a script-mode rule uses (unchanged).

`shard_checkpoint.py` makes a shard's edit safely reversible with
`git hash-object -w` / `git cat-file blob` against the enclosing repo's
object store — never a commit, never `git stash`, never HEAD movement,
never the index. Rolling back one shard never touches a sibling shard's
edits (each shard's files are checkpointed independently).

## Binding rule-execution order

`effective_rule_order` (used only by the `RULE_BATCH_LOOP` iteration loop)
permutes the approved `05-rule-queue.json` `rules` list by blast_class
(body-local before signature before unclassified, from the breaking-changes
manifest), with the knowledge graph's `suggested_order` as a binding
second-order tie-break. The on-disk `rules` list itself is never reordered
or rewritten — only the iteration order changes.

Use `scripts/orchestrator.py` to execute the above behavior.
`scripts/shard_checkpoint.py` implements the per-shard checkpoint ledger.
