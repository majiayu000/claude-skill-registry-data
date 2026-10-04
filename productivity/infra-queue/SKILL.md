---
name: infra-queue
description: Manage AICP's queue surfaces — primary is the per-day JSONL Dead-Letter Queue (`~/.aicp/dlq/`); secondary is the in-process task_manager queue (`aicp/core/tasks.py`); future fleet integration may add a real message queue. Distinct from `aicp-ops-dlq` (DLQ runtime ops via CLI) — this skill is the design/scale lifecycle for queue infrastructure. Loads when the operator says "scale the queue" / "replace DLQ with Redis" / "add a queue for fleet" / "queue throughput limit" / "is JSONL DLQ enough".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# infra-queue

Manage AICP's queue infrastructure DESIGN. AICP intentionally uses a
file-based per-day JSONL DLQ (per the dlq-with-retry-budget pattern)
instead of a real message queue. This skill is the LIFECYCLE: when does
JSONL stop scaling, when to migrate to a real queue, and how to do it
without losing entries.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Scale concern**: "scale the queue", "is JSONL DLQ enough", "queue
  throughput limit", "fleet rollout will overwhelm DLQ"
- **Migration planning**: "replace DLQ with Redis", "add a queue for
  fleet", "switch to Redis Streams", "evaluate Kafka"
- **Design**: AICP team is considering a new queue surface (e.g., for
  inter-agent messaging in fleet)

Do NOT load when:

- The concern is DLQ runtime operations (load `aicp-ops-dlq` for the
  CLI-driven inspect/retry workflow)
- The concern is AICP's runtime task_manager (load `aicp-ops-tasks`)
- The concern is the per-day-jsonl-dlq pattern's design rationale (load
  `wiki/patterns/01_drafts/per-day-jsonl-dlq-with-retry-budget.md` directly)

## Operations

### Operation 1 — Audit current queue throughput vs scale assumptions

**When**: pre-fleet rollout or after operator notices DLQ growth.

**Process**:

1. Inspect DLQ throughput: `aicp --dlq-status` (current pending count)
2. Historical: `ls -la ~/.aicp/dlq/` (per-day file sizes show daily
   throughput)
3. Per the pattern doc, JSONL is suitable for <100 failed tasks/sec.
   Sustained higher rates indicate scale migration is needed.
4. Inspect task_manager throughput: `aicp --tasks` (active + total counts)
5. Build a throughput profile: peak ops/sec × duration → daily volume

**Quality bar**: most fleet rollouts (10 agents × moderate task rate)
stay well under the 100 ops/sec threshold. Migration is rarely needed
in the near term.

### Operation 2 — Migrate DLQ to a real message queue

**When**: Operation 1 confirmed throughput exceeds JSONL's safe range.

**Process**:

1. Choose target queue: Redis Streams (smallest operational footprint),
   RabbitMQ (richer routing), Kafka (very high throughput)
2. Per `wiki/decisions/00_inbox/` create a decision page documenting
   choice + alternatives + reversibility
3. Implement adapter behind the existing `aicp/core/dlq.py` API:
   - `enqueue(prompt, mode, backend, project, error, failover_chain, config)` — write to new queue
   - `list_entries(max_count)` — read from new queue
   - `retry_pending(controller, config, max_items)` — same retry semantics
   - `count()` — queue depth
4. Drain the existing JSONL DLQ first (run `aicp --retry-dlq` to clear,
   or migrate entries one-by-one)
5. Switch the implementation under feature flag (per `config-feature-flags`)
6. Run for a release cycle to validate; remove JSONL implementation once
   validated

**Quality bar**: NEVER cut over without draining old DLQ. JSONL entries
not migrated will be silently lost when the implementation switches.

### Operation 3 — Add a fleet-wide message queue surface

**When**: agent-to-agent messaging needs persistence + cross-process
delivery (a NEW concern, not DLQ replacement).

**Process**:

1. Per the audit decision (the MCP-vs-CLI lesson — bridges between agents
   are legitimate MCP territory), evaluate if MCP server tools or a
   real queue is the right shape
2. If real queue: same options as Operation 2 (Redis Streams typically)
3. Define message schema: who sends, who receives, ack semantics,
   ordering guarantees
4. Document in `wiki/decisions/00_inbox/` the design + trade-offs
5. Implement as a NEW package (`aicp/core/fleet_queue.py` or similar) —
   not bolted onto existing DLQ

**Quality bar**: NEW queue surfaces are major architectural additions
— author the decision page BEFORE implementing.

### Operation 4 — Tune JSONL DLQ within current scale

**When**: scale is fine but DLQ behavior needs adjustment.

**Process**:

1. Per `aicp-ops-dlq` skill, edit `config/<profile>.yaml` `dlq:` section:
   - `max_entries` — bound disk usage
   - `max_retries` — retry budget per entry
   - `retry_delay_seconds` — back-off window
   - `enabled` — disable persistence entirely (rare)
2. The `reliable.yaml` profile is the canonical production tuning
   (max_retries: 5)

**Quality bar**: tuning is the LIGHT-WEIGHT response; migration is the
HEAVY response. Try tuning first.

## Gotchas

- **Detection**: agent recommends migrating DLQ to Redis without measuring throughput.
  **Rule**: per the per-day-jsonl-dlq pattern, JSONL is correct for <100
  ops/sec. Don't migrate based on hypothetical scale.
  **Reasoning**: premature migration adds operational complexity (Redis
  service, persistence config, monitoring) for no gain at current scale.

- **Detection**: agent confuses DLQ with task_manager queue.
  **Rule**: DLQ is the DURABLE persistence for FAILED tasks. task_manager
  is the IN-PROCESS lifecycle tracker. Different concerns.
  **Reasoning**: same word "queue", different stores, different scopes.
  Clarify which is the concern before recommending changes.

- **Detection**: agent cuts over to a new queue without draining the old DLQ.
  **Rule**: drain old (run `aicp --retry-dlq` to clear) before switching
  the implementation under feature flag.
  **Reasoning**: undrained entries in the old store are silently lost
  when the implementation switches reads to the new store.

- **Detection**: agent treats a new fleet messaging queue as a DLQ extension.
  **Rule**: fleet messaging is a NEW concern (cross-agent delivery), not
  DLQ replacement. Author separately.
  **Reasoning**: bolting unrelated concerns onto DLQ couples them; future
  changes to one impact the other.

## Reference exemplars

- `aicp/core/dlq.py` — current per-day JSONL DLQ implementation
- `wiki/patterns/01_drafts/per-day-jsonl-dlq-with-retry-budget.md` — the
  full pattern doc (rationale, alternatives, when to apply)
- `aicp/core/tasks.py` — in-process task_manager (separate queue concern)
- `wiki/decisions/01_drafts/aicp-active-state-mechanism-for-hooks.md` —
  example of a stateful storage decision with alternatives

## Domain context

AICP's queue strategy is intentional: JSONL for DLQ (operator-inspectable,
no daemon), in-process dict for task_manager (per-invocation), no
general-purpose application queue. The pattern doc explains WHY (operator
inspection beats throughput at AICP's current scale). Migration is a real
option but should be triggered by measured throughput, not hypothetical.

## Related skills

| Skill | When to use |
|-------|-------------|
| `aicp-ops-dlq` | When the concern is DLQ runtime operations (CLI workflow) |
| `aicp-ops-tasks` | When the concern is task_manager runtime tasks |
| `infra-monitoring` | When the concern is alerting on queue depth/growth |
| `architecture-propose` | When proposing a NEW queue surface (e.g., fleet messaging) |
| `evolve-scale` | When the concern is scaling broader than queue specifically |
