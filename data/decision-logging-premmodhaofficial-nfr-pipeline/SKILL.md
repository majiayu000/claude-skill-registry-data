---
name: decision-logging
description: >
  Use this when writing any entry to runs/<run-id>/decision-log.jsonl —
  decision, lifecycle, communication, event, failure, refactor, skill-evolution,
  or budget. Covers canonical JSON schemas, per-agent entry caps, rework-wave
  cap-reset rules, and the skill-evolution / budget entry types added for the
  SDK pipeline.
  Triggers: decision-log, JSONL, schema, entry cap, skill-evolution, budget, lifecycle, communication, refactor, failure.
---

# decision-logging (SDK-mode, v1.4.0)


## Delta (v1.3.0 → v1.4.0)

Removed the cross-LLM ensemble telemetry layer introduced in v1.3.0. The `cross-llm-devil` MCP server and its sibling devils (`sdk-overengineering-critic-gemini`, `sdk-security-devil-gemini`) were removed from the pipeline; consequently the `cross-llm-call` / `cross-llm-agreement` / `cross-llm-conflict` event categories and the `model_id` / `transcript_path` / `ensemble_role` optional fields are no longer documented or emitted.

**Backward compat**: pre-existing decision-log entries that still carry these fields remain readable — readers ignore unknown categories/fields. No retroactive scrub of historical run data is required.

---


## Delta (v1.1.0 → v1.2.0)

One additive envelope field across **every** entry type to support the language-agnostic pipeline (CLAUDE.md rule 34).

### Required field on every entry: `language`

```json
{
  ...,
  "language": "go" | "python" | "unknown"
}
```

**Source of truth**: read from `runs/<run-id>/context/active-packages.json:target_language` once package resolution (Wave I5.5) has completed.

**Pre-resolution entries**: any entry written BEFORE Wave I5.5 (i.e., during sdk-intake-agent waves I1–I5.5 itself) MUST emit `"language": "unknown"`. Re-stamping is not required — pre-resolution entries are intake-internal and never participate in cross-language metrics.

**Post-resolution entries**: `"language": "unknown"` is a BLOCKER signal. The G01 validator (or its successor) MUST FAIL any entry with `language: unknown` whose timestamp is after `active-packages.json:resolved_at`.

**Rationale**: per-language partitioning of metrics, baselines, and learning-engine signals depends on every log line being attributable to a language. Without this stamp, cross-language quality scoring, devil-verdict-history, and skill-coverage analysis cannot disambiguate.

**Applies to**: `decision`, `lifecycle`, `communication`, `event`, `failure`, `refactor`, `skill-evolution`, `budget` — all eight entry types.

**Validator mapping**: G01 extended to assert presence + valid value. Backward-compat: entries written by pipeline_version <0.5.0 may legitimately omit `language` and are not retroactively invalidated.

---


## Delta  (v1.0.0 → v1.1.0)

Two new entry types added for SDK-pipeline self-evolution:

### `skill-evolution` (cap ≤10 per run)

Emitted by `learning-engine` OR `sdk-bootstrap-lead` when a skill is created / bumped / deprecated.

```json
{
  "run_id": "<uuid>",
  "pipeline_version": "sdk-pipeline@0.7.0",
  "skill_version_snapshot": {"<skill>": "<version>", ...},
  "timestamp": "2026-04-17T...",
  "type": "skill-evolution",
  "agent": "learning-engine",
  "phase": "feedback",
  "skill": "<skill-name>",
  "action": "create | bump-patch | bump-minor | bump-major | deprecate",
  "from_version": "1.2.0",
  "to_version": "1.2.1",
  "trigger": "drift-finding:SKD-042 | devil-verdict:NEEDS-FIX | pattern-recurrence:3 | user-request",
  "devil_verdict": "ACCEPT | NEEDS-FIX | REJECT"
}
```

### `budget` (per-agent emit every 5min OR on phase exit)

Emitted by every agent to track per-phase token + wall-clock consumption.

```json
{
  "run_id": "<uuid>",
  "pipeline_version": "sdk-pipeline@0.7.0",
  "skill_version_snapshot": {...},
  "timestamp": "2026-04-17T...",
  "type": "budget",
  "agent": "<agent-name>",
  "phase": "<phase>",
  "tokens_in": 12345,
  "tokens_out": 6789,
  "wall_clock_sec": 42.5,
  "cumulative_pct_of_budget": 0.34
}
```

### Consumers of new types

- `baseline-manager` reads `budget` entries to compute phase-duration + token-consumption metrics
- `improvement-planner` reads `skill-evolution` to detect unstable skills (high patch frequency)
- `sdk-skill-drift-detector` reads both to correlate prescription vs. reality

## Validator mapping

- Guardrail `G01` unchanged (valid JSONL).
- Guardrail `G06` (NEW): every entry MUST carry `pipeline_version` + `skill_version_snapshot`.

---



# Decision Logging

Provides the canonical JSON schemas, entry limits, and best practices for appending to `decision-log.jsonl` across both Architecture and Detailed Design phases.

## When to Activate
- When any agent needs to log an architectural or design decision
- When an agent starts, completes, or fails (lifecycle logging)
- When consolidating minor decisions into grouped entries
- When logging a conflict resolution between agents
- When unsure which `phase` field value to use
- Used by: ALL 24 agents (architecture-lead, system-decomposer, api-designer, infrastructure-architect, database-architect, pattern-advisor, simulated-cto, simulated-security-architect, simulated-sre, simulated-tech-lead, simulated-product-owner, detailed-design-lead, component-designer, data-model-designer, sdk-designer, interface-designer, algorithm-designer, concurrency-designer, coding-guidelines-generator, guardrail-validator, simulated-senior-developer, simulated-dba, simulated-qa-lead, simulated-security-engineer)

## Decision Log File Locations

| Phase | File Path |
|-------|-----------|
| Architecture | `docs/architecture/decisions/decision-log.jsonl` |
| Detailed Design | `docs/detailed-design/decisions/decision-log.jsonl` |
| Implementation | `docs/implementation/decisions/decision-log.jsonl` |
| Testing | `docs/testing/decisions/decision-log.jsonl` |
| Frontend | `docs/frontend/decisions/decision-log.jsonl` |

Each file is append-only JSONL (one JSON object per line, no trailing commas, no array wrapper). ALL six entry types (`decision`, `lifecycle`, `communication`, `event`, `failure`, `refactor`) go into the same file for a given phase.

## Decision Entry Schema

Per CLAUDE.md rule #1, every architectural or design decision uses this exact schema:

```json
{
  "run_id": "<from-run-manifest>",
  "type": "decision",
  "timestamp": "<ISO-8601>",
  "agent": "<agent-name>",
  "phase": "<see-phase-values-below>",
  "decision": "<what was decided>",
  "rationale": "<why this over alternatives>",
  "alternatives_considered": ["<alt1>", "<alt2>"],
  "trade_offs": "<what is sacrificed>",
  "confidence": "<high|medium|low>",
  "status": "<success|failed|retried|degraded>",
  "context": "<input that led to this>",
  "impacts": ["<affected-agents-or-artifacts>"],
  "reversibility": "<easy|moderate|hard|irreversible>",
  "tags": ["<tag1>", "<tag2>"]
}
```

### Required Fields — Never Omit

Every field in the schema is mandatory. If a field has no meaningful value, use:
- `"alternatives_considered": []` (empty array, not null)
- `"trade_offs": "none identified"` (not empty string)
- `"impacts": []` (empty array, not null)
- `"tags": []` (empty array, not null)

## Lifecycle Entry Schema

Per CLAUDE.md rule #1, lifecycle events (agent start, completion, failure) use this schema:

```json
{
  "run_id": "<from-run-manifest>",
  "type": "lifecycle",
  "timestamp": "<ISO-8601>",
  "agent": "<agent-name>",
  "event": "<started|completed|failed|retried>",
  "wave": "<1|2|3|4>",
  "outputs": ["<list-of-files-written>"],
  "duration_seconds": "<elapsed>",
  "error": "<error-description-if-failed>"
}
```

Lifecycle entries do NOT count toward the decision entry limit.

## Phase Field Values

### Architecture Phase Agents

| Agent | Phase Value |
|-------|------------|
| system-decomposer | `decomposition` |
| api-designer | `api-design` |
| infrastructure-architect | `infrastructure` |
| database-architect | `database` |
| pattern-advisor | `patterns` |
| architecture-lead | `review` (for synthesis decisions) |
| All Wave 3 review agents | `review` |

### Detailed Design Phase Agents

| Agent | Phase Value |
|-------|------------|
| component-designer | `component-design` |
| interface-designer | `interface-design` |
| data-model-designer | `data-model` |
| algorithm-designer | `algorithm` |
| concurrency-designer | `concurrency` |
| sdk-designer | `sdk-design` |
| coding-guidelines-generator | `coding-guidelines` |
| detailed-design-lead | `review` |
| All Wave 4 review agents | `review` |

## Entry Limits (per agent per run)

| Type | Limit | Rationale |
|------|-------|-----------|
| `decision` | 15 (10 for review agents) | Architectural/design choices — consolidate minor ones |
| `lifecycle` | Unlimited | Agent start/end/retry — low volume |
| `communication` | 20 | Cap chattiness — log meaningful exchanges only |
| `event` | 30 (max 10 major, 20 minor/info) | Most granular type — cap to prevent noise |
| `failure` | 10 | Failures should be exceptional |
| `refactor` | 10 | Typically one per review finding |

Only `decision` entries count toward the traditional 15/10 cap. All other types have their own independent limits.

## Communication Entry Schema

Tracks every meaningful agent-to-agent exchange for coordination audit:

```json
{
  "run_id": "<from-run-manifest>",
  "type": "communication",
  "timestamp": "<ISO-8601>",
  "from_agent": "<sender>",
  "to_agent": "<recipient|*>",
  "wave": "<N>",
  "channel": "<message|context-file|escalation>",
  "severity": "<critical|high|normal|low>",
  "topic": "<short subject>",
  "content_summary": "<1-2 sentence summary>",
  "references": ["<file-paths-or-decision-ids>"],
  "requires_response": true,
  "response_status": "<pending|acknowledged|resolved|ignored>",
  "tags": ["<assumption|conflict|dependency|blocker>"]
}
```

### When to Log Communications
- Task assignments from lead to agent
- Escalation messages (ESCALATION: or BLOCKER: prefix)
- Cross-agent dependency requests ("I need X from agent Y")
- Assumption notifications ("ASSUMPTION — pending Z confirmation")
- Review relay messages (lead relaying findings to responsible agent)
- Conflict reports

### When NOT to Log Communications
- "Still working" status pings
- Acknowledgements with no new information
- Internal monologue or self-notes

### Channel Values

| Channel | When to Use |
|---------|-------------|
| `message` | SendMessage / inbox communication |
| `context-file` | Writing/reading a context summary as implicit communication |
| `escalation` | ESCALATION: or BLOCKER: prefixed messages |

## Event Entry Schema

Captures major and minor happenings during agent work:

```json
{
  "run_id": "<from-run-manifest>",
  "type": "event",
  "timestamp": "<ISO-8601>",
  "agent": "<agent-name>",
  "wave": "<N>",
  "severity": "<major|minor|info>",
  "category": "<see-category-values-below>",
  "title": "<short description>",
  "detail": "<what happened and why>",
  "artifacts": ["<files-read-or-written>"],
  "duration_ms": null,
  "outcome": "<success|warning|error|skipped>",
  "parent_event_id": "<optional, for nested events>"
}
```

### Event Category Values

| Category | When to Use |
|----------|-------------|
| `input-read` | Reading a critical input file or context summary |
| `output-write` | Writing a major output artifact |
| `validation` | Running a validation check (schema, syntax, constraint) |
| `compilation` | Running the active language adapter's build command (resolved from `toolchain.build` in the package manifest) |
| `test-run` | Running the active language adapter's test command (resolved from `toolchain.test`) |
| `tool-call` | Invoking an external tool or script |
| `dependency-resolution` | Resolving a dependency between agents or packages |
| `assumption` | Making an assumption about upstream agent output |
| `skip` | Deliberately skipping optional work |
| `retry` | Retrying a failed operation |
| `workaround` | Applying a workaround for a known issue |

### Severity Guidelines
- **major**: Events that change the agent's approach or affect downstream agents (e.g., "compilation failed, switching strategy").
- **minor**: Routine progress events that confirm expected behavior (e.g., "read service-map.md successfully").
- **info**: Context-only events useful for debugging (e.g., "found 5 services in decomposition").

## Failure Entry Schema

Rich failure context for individual operations (supplements lifecycle `"event":"failed"`):

```json
{
  "run_id": "<from-run-manifest>",
  "type": "failure",
  "timestamp": "<ISO-8601>",
  "agent": "<agent-name>",
  "wave": "<N>",
  "failure_type": "<see-failure-types-below>",
  "severity": "<critical|high|medium|low>",
  "title": "<short description>",
  "detail": "<what failed and why>",
  "error_output": "<first 500 chars of error output>",
  "partial_outputs": ["<files-written-before-failure>"],
  "attempted_recovery": "<none|retry|fallback|skip|manual>",
  "recovery_successful": null,
  "blocked_agents": ["<agents-waiting-on-this>"],
  "root_cause_hint": "<agent's best guess at why>",
  "related_decision_id": "<if failure relates to a logged decision>"
}
```

### Failure Type Values

| Failure Type | When to Use |
|-------------|-------------|
| `timeout` | Operation exceeded time limit |
| `missing-input` | Required upstream file or context not found |
| `validation-error` | Output failed schema/syntax/constraint validation |
| `compilation-error` | The active adapter's `toolchain.build` command failed |
| `test-failure` | The active adapter's `toolchain.test` command failed |
| `dependency-failure` | Upstream agent failed, blocking this agent |
| `tool-error` | External tool (linter, formatter, script) failed |
| `resource-limit` | Exceeded entry limit, file size limit, or iteration cap |

### Key Rule
Log a failure entry BEFORE attempting recovery. This ensures the failure is captured even if recovery succeeds. After recovery, update `recovery_successful` field via a follow-up event entry.

## Refactor Entry Schema

Tracks post-review and post-failure changes to distinguish initial work from rework:

```json
{
  "run_id": "<from-run-manifest>",
  "type": "refactor",
  "timestamp": "<ISO-8601>",
  "agent": "<agent-name>",
  "wave": "<N>",
  "trigger": "<review-finding|test-failure|guardrail-failure|escalation|self-improvement>",
  "trigger_source": "<agent-or-script that triggered this>",
  "trigger_reference": "<finding-id|defect-id|guardrail-name>",
  "files_changed": ["<modified-files>"],
  "change_summary": "<what was changed>",
  "before_state": "<brief description of old approach>",
  "after_state": "<brief description of new approach>",
  "severity": "<major|minor>",
  "confidence": "<high|medium|low>",
  "regression_risk": "<none|low|medium|high>"
}
```

### Trigger Values

| Trigger | When to Use |
|---------|-------------|
| `review-finding` | Changing output after a reviewer flagged an issue |
| `test-failure` | Fixing code/design after a test failed |
| `guardrail-failure` | Updating output to pass an automated guardrail check |
| `escalation` | Changing approach after a BLOCKER or ESCALATION message |
| `self-improvement` | Agent voluntarily improving output without external trigger |

## Consolidating Minor Decisions

When an agent makes several small, related decisions, consolidate them into a single grouped entry rather than logging each individually.

### When to Consolidate
- Three or more decisions about the same domain (e.g., naming multiple NATS subjects)
- Decisions that share the same rationale and alternatives
- Stylistic or formatting choices within a single output file

### How to Consolidate

```json
{
  "run_id": "a1b2c3d4-...",
  "type": "decision",
  "timestamp": "2026-03-09T14:30:00Z",
  "agent": "api-designer",
  "phase": "api-design",
  "decision": "NATS subject naming for entity lifecycle: tenant.{tid}.<domain>.created, tenant.{tid}.<domain>.updated, tenant.{tid}.<domain>.deleted (applied to all bounded contexts)",
  "rationale": "Consistent verb-based suffixes align with AsyncAPI spec and enable wildcard subscriptions per tenant",
  "alternatives_considered": ["dot-separated-entity.action", "slash-separated paths"],
  "trade_offs": "Longer subject names increase NATS overhead slightly",
  "confidence": "high",
  "status": "success",
  "context": "Designing async event subjects for domain services",
  "impacts": ["infrastructure-architect", "concurrency-designer"],
  "reversibility": "easy",
  "tags": ["nats-subjects", "consolidated"]
}
```

Use the `"consolidated"` tag to mark grouped entries.

## Conflict Resolution Logging

Per CLAUDE.md rule #8, when `architecture-lead` or `detailed-design-lead` resolves a conflict between agents, log it with the `"conflict-resolution"` tag:

```json
{
  "run_id": "a1b2c3d4-...",
  "type": "decision",
  "timestamp": "2026-03-09T16:00:00Z",
  "agent": "architecture-lead",
  "phase": "review",
  "decision": "Tenant isolation uses schema-per-tenant per database-architect's design, not application-level filtering as proposed by api-designer",
  "rationale": "Schema-per-tenant provides hard isolation; application filtering alone risks cross-tenant data leakage if a query is missed",
  "alternatives_considered": ["application-level tenant filtering", "separate schemas per tenant", "row-level security (RLS)"],
  "trade_offs": "Schema-per-tenant requires per-tenant connection pool management and coordinated migrations across all tenant databases",
  "confidence": "high",
  "status": "success",
  "context": "ESCALATION: CONFLICT between database-architect (schema-per-tenant) and api-designer (app-level filtering)",
  "impacts": ["api-designer", "database-architect", "component-designer"],
  "reversibility": "hard",
  "tags": ["conflict-resolution", "tenant-isolation"]
}
```

### Required Tags for Conflict Entries
- `"conflict-resolution"` (always present)
- Domain-specific tag (e.g., `"tenant-isolation"`, `"nats-subjects"`)

## Status Field Values

| Value | When to Use |
|-------|-------------|
| `success` | Decision made with confidence, no issues |
| `failed` | Decision attempted but agent could not reach a conclusion |
| `retried` | Decision made after a previous failed attempt |
| `degraded` | Decision made with incomplete inputs (upstream agent failed) |

## Reading the run_id

Before logging any entry, the agent MUST read the `run_id` from the appropriate manifest:

- Architecture phase: `docs/architecture/state/run-manifest.json`
- Detailed Design phase: `docs/detailed-design/state/run-manifest.json`

Never generate a run_id. Never hardcode a run_id. Always read it from the manifest.

## Examples

### GOOD

```json
{"run_id":"f47ac10b-58cc-4372-a567-0e02b2c3d479","type":"decision","timestamp":"2026-03-09T10:15:00Z","agent":"database-architect","phase":"database","decision":"All tenant tables use UUID v7 for primary keys with tenant_id as the first column in composite indexes","rationale":"UUID v7 is time-sortable, reducing index fragmentation; schema-per-tenant isolation means no tenant_id columns needed in tables","alternatives_considered":["UUID v4","BIGSERIAL","ULID"],"trade_offs":"UUID v7 requires Go 1.26+ uuid library; 16-byte keys are larger than BIGSERIAL","confidence":"high","status":"success","context":"Designing primary key strategy for tenant-scoped tables","impacts":["data-model-designer","component-designer"],"reversibility":"hard","tags":["primary-keys","multi-tenancy"]}
```

### BAD

```json
{"agent":"database-architect","decision":"use UUIDs","rationale":"they are good"}
```

Why it is wrong: Missing `run_id`, `type`, `timestamp`, `phase`, `status`, `alternatives_considered`, `trade_offs`, `confidence`, `context`, `impacts`, `reversibility`, and `tags`. Every field is mandatory.

### BAD

```json
{"run_id":"f47ac10b-...","type":"decision","timestamp":"2026-03-09T10:15:00Z","agent":"database-architect","phase":"database","decision":"chose index type A","rationale":"","alternatives_considered":null,"trade_offs":"","confidence":"high","status":"success","context":"","impacts":null,"reversibility":"easy","tags":null}
```

Why it is wrong: Empty strings and null arrays. Use `"none identified"` for trade_offs, `[]` for arrays, and descriptive text for rationale and context.

## Common Mistakes

1. **Forgetting to read run_id from the manifest** -- Agents generate their own UUID or hardcode a placeholder. The run_id MUST come from `run-manifest.json` so all entries for a run are correlated.

2. **Using the wrong phase value** -- An `api-designer` agent logging with `"phase": "design"` instead of `"phase": "api-design"`. Check the phase table above for the exact string.

3. **Exceeding the entry limit without consolidating** -- Logging 20+ individual decisions when related ones could be grouped with the `"consolidated"` tag. Count entries before appending and consolidate if approaching the limit.

4. **Counting lifecycle entries toward the decision cap** -- Lifecycle entries (`"type": "lifecycle"`) are separate and unlimited. Only `"type": "decision"` entries count toward the 15/10 limit.

5. **Omitting the conflict-resolution tag** -- When `architecture-lead` resolves a conflict per CLAUDE.md rule #8, the resulting decision entry MUST include `"conflict-resolution"` in tags. Without it, conflict audit trails are broken.

6. **Logging to the wrong file** -- Architecture agents must append to `docs/architecture/decisions/decision-log.jsonl`. Detailed design agents must append to `docs/detailed-design/decisions/decision-log.jsonl`. Never cross-write.
