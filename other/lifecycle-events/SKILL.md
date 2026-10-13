---
name: lifecycle-events
description: >
  Use this when an agent begins work (startup), finishes successfully
  (completion), hits an unrecoverable error (failure), or is retried after a
  prior failure — and when calculating duration_seconds for any lifecycle
  entry. Covers the canonical lifecycle JSON schema, startup / completion /
  failure protocols, retry semantics, and duration computation per CLAUDE.md
  rule 1.
  Triggers: lifecycle, started, completed, failed, retried, duration_seconds, startup, completion, agent-failure.
---



# Lifecycle Events

Provides the exact protocols and JSON schema for logging agent lifecycle events (started, completed, failed, retried) across both Architecture and Detailed Design phases.

## When to Activate
- When an agent begins its work (startup protocol)
- When an agent finishes successfully (completion protocol)
- When an agent encounters an unrecoverable error (failure protocol)
- When an agent is retried after a previous failure
- When calculating `duration_seconds` for a lifecycle entry
- Used by: ALL 24 agents (architecture-lead, system-decomposer, api-designer, infrastructure-architect, database-architect, pattern-advisor, simulated-cto, simulated-security-architect, simulated-sre, simulated-tech-lead, simulated-product-owner, detailed-design-lead, component-designer, data-model-designer, sdk-designer, interface-designer, algorithm-designer, concurrency-designer, coding-guidelines-generator, guardrail-validator, simulated-senior-developer, simulated-dba, simulated-qa-lead, simulated-security-engineer)

## Lifecycle Entry Schema

Per CLAUDE.md rule #1, every lifecycle event uses this exact JSON schema:

```json
{
  "run_id": "<from-run-manifest>",
  "type": "lifecycle",
  "timestamp": "<ISO-8601>",
  "agent": "<agent-name>",
  "event": "<started|completed|failed|retried>",
  "wave": "<1|2|3|4>",
  "outputs": ["<list-of-files-written>"],
  "duration_seconds": "<elapsed-since-start>",
  "error": "<error-description-if-failed>"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `run_id` | string (UUID) | Yes | From `run-manifest.json`, never self-generated |
| `type` | string | Yes | Always `"lifecycle"` for lifecycle entries |
| `timestamp` | string (ISO-8601) | Yes | UTC with `Z` suffix, e.g., `"2026-03-09T14:30:00Z"` |
| `agent` | string | Yes | Must match agent frontmatter `name` exactly |
| `event` | string | Yes | One of: `started`, `completed`, `failed`, `retried` |
| `wave` | string | Yes | Wave number: `"1"`, `"2"`, `"3"`, or `"4"` |
| `outputs` | string[] | Yes | File paths written; `[]` for started/failed events |
| `duration_seconds` | number | Yes | `0` for started events; elapsed seconds for others |
| `error` | string or null | Yes | `null` unless event is `failed` |

## Log File Locations

| Phase | File Path |
|-------|-----------|
| Architecture | `docs/architecture/decisions/decision-log.jsonl` |
| Detailed Design | `docs/detailed-design/decisions/decision-log.jsonl` |

Lifecycle entries go into the SAME file as decision entries. They are distinguished by `"type": "lifecycle"` vs `"type": "decision"`.

## Startup Protocol

Every agent MUST perform these 3 steps before doing any design work:

### Step 1: Read the Run Manifest

```
Architecture:      docs/architecture/state/run-manifest.json
Detailed Design:   docs/detailed-design/state/run-manifest.json
```

Extract the `run_id` field. If the manifest does not exist or is unreadable, the agent MUST NOT proceed -- escalate to the lead immediately.

### Step 2: Note the Start Time

Record the current UTC timestamp. This timestamp is used for:
- The `"timestamp"` field in the started lifecycle entry
- Calculating `duration_seconds` at completion or failure

### Step 3: Log the Started Entry

Append to the decision log file:

```json
{
  "run_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "lifecycle",
  "timestamp": "2026-03-09T14:00:00Z",
  "agent": "database-architect",
  "event": "started",
  "wave": "2",
  "outputs": [],
  "duration_seconds": 0,
  "error": null
}
```

Rules:
- `outputs` is always `[]` at startup (nothing written yet)
- `duration_seconds` is always `0` at startup
- `error` is always `null` at startup
- The `started` entry MUST be the first thing appended, before any decision entries

## Completion Protocol

When an agent finishes all work successfully, perform these 3 steps in order:

### Step 1: Log the Completed Entry

Calculate `duration_seconds` (see calculation section below) and list all output files:

```json
{
  "run_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "lifecycle",
  "timestamp": "2026-03-09T14:45:00Z",
  "agent": "database-architect",
  "event": "completed",
  "wave": "2",
  "outputs": [
    "docs/architecture/data/schemas/core-tables.sql",
    "docs/architecture/data/schemas/tenant-provisioning.sql",
    "docs/architecture/data/schemas/indexes.sql",
    "docs/architecture/context/database-architect-summary.md"
  ],
  "duration_seconds": 2700,
  "error": null
}
```

Rules:
- `outputs` MUST list every file the agent wrote, including the context summary
- `error` is `null` on successful completion
- `duration_seconds` is the elapsed time from the `started` entry's timestamp

### Step 2: Send Completion Message to Lead

Send a Teammate inbox message to the orchestrator:

- Architecture phase: message `architecture-lead`
- Detailed Design phase: message `detailed-design-lead`

Message format:
```
database-architect completed. Outputs: core-tables.sql, tenant-provisioning.sql, indexes.sql, database-architect-summary.md. Duration: 2700s. No issues.
```

### Step 3: Notify Downstream Agents (if applicable)

If the agent's output is a critical dependency for other agents, send targeted messages:

```
[database-architect -> api-designer]: Database-per-tenant isolation design complete. Tenant connection routing uses TenantRouter.GetPool(). See database-architect-summary.md for key constraints.
```

This step is optional for agents with no known downstream dependencies.

## Failure Protocol

Per CLAUDE.md rule #10, when an agent encounters an unrecoverable error, perform these 3 steps:

### Step 1: Log the Failed Entry

```json
{
  "run_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "lifecycle",
  "timestamp": "2026-03-09T14:20:00Z",
  "agent": "database-architect",
  "event": "failed",
  "wave": "2",
  "outputs": [
    "docs/architecture/data/schemas/core-tables.sql"
  ],
  "duration_seconds": 1200,
  "error": "Failed to generate tenant provisioning config: requirements document missing tenant isolation requirements for audit_log table"
}
```

Rules:
- `error` MUST be a descriptive string (never null, never empty string)
- `outputs` lists any partial files that were written before failure
- `duration_seconds` is calculated from the started timestamp to the failure timestamp

### Step 2: Write Partial Output

Write whatever output was completed before the failure. Partial data is always better than no data. Mark incomplete sections:

```markdown
<!-- Generated: 2026-03-09T14:20:00Z | Run: f47ac10b-... -->
<!-- PARTIAL -- agent failed before completion -->
# Database Architect Summary (PARTIAL)

## Completed
- Core table schemas for primary domain entities

## Not Completed
- Tenant database provisioning for audit_log service
- Index optimization strategy
```

### Step 3: Escalate to Lead

Send an escalation message to the orchestrator:

```
ESCALATION: database-architect failed -- Failed to generate tenant provisioning config: requirements document missing tenant isolation requirements for audit_log table
```

The exact format is: `ESCALATION: <agent-name> failed -- [reason]`

## Retry Protocol

When the lead retries a failed agent (max 1 retry per CLAUDE.md rule #10):

### Before Retry
The lead archives previous outputs by renaming with `.prev` suffix:
- `core-tables.sql` becomes `core-tables.sql.prev`
- `database-architect-summary.md` becomes `database-architect-summary.md.prev`

### On Retry Start
Log a `retried` lifecycle entry:

```json
{
  "run_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "lifecycle",
  "timestamp": "2026-03-09T14:30:00Z",
  "agent": "database-architect",
  "event": "retried",
  "wave": "2",
  "outputs": [],
  "duration_seconds": 0,
  "error": null
}
```

Then follow the normal startup protocol (the `retried` entry replaces `started` for retries). On completion, log a normal `completed` entry. The `duration_seconds` measures from the retry start, not the original start.

## Calculating duration_seconds

Duration is the wall-clock elapsed time in whole seconds between the agent's start and its completion or failure.

### Method

```
duration_seconds = completion_timestamp - start_timestamp (in seconds)
```

Where:
- `start_timestamp` is the `timestamp` from the agent's `started` (or `retried`) lifecycle entry
- `completion_timestamp` is the `timestamp` from the `completed` or `failed` entry

### Rules
- Always use whole seconds (integer), not fractional
- For `started` entries, always use `0`
- For `retried` entries used as a new start, always use `0`
- On retry, measure from the retry start, not the original start
- If exact measurement is not possible, estimate conservatively

### Example Calculation

```
Started:   2026-03-09T14:00:00Z
Completed: 2026-03-09T14:45:00Z

duration_seconds = 45 minutes * 60 = 2700
```

## Wave Assignments

For the `wave` field, use the correct value for each agent:

### Architecture Phase

| Wave | Agents |
|------|--------|
| `"1"` | system-decomposer |
| `"2"` | api-designer, infrastructure-architect, database-architect, pattern-advisor |
| `"3"` | simulated-cto, simulated-security-architect, simulated-sre, simulated-tech-lead, simulated-product-owner |

### Detailed Design Phase

| Wave | Agents |
|------|--------|
| `"1"` | component-designer, data-model-designer, sdk-designer |
| `"2"` | interface-designer, algorithm-designer, concurrency-designer |
| `"3"` | coding-guidelines-generator |
| `"4"` | guardrail-validator, simulated-senior-developer, simulated-dba, simulated-qa-lead, simulated-security-engineer |

## Examples

### GOOD -- Full Lifecycle Sequence

```jsonl
{"run_id":"f47ac10b-...","type":"lifecycle","timestamp":"2026-03-09T14:00:00Z","agent":"api-designer","event":"started","wave":"2","outputs":[],"duration_seconds":0,"error":null}
{"run_id":"f47ac10b-...","type":"lifecycle","timestamp":"2026-03-09T14:50:00Z","agent":"api-designer","event":"completed","wave":"2","outputs":["docs/architecture/api/openapi/order-service.yaml","docs/architecture/api/async/order-events.yaml","docs/architecture/context/api-designer-summary.md"],"duration_seconds":3000,"error":null}
```

### BAD -- Missing Started Entry

```jsonl
{"run_id":"f47ac10b-...","type":"lifecycle","timestamp":"2026-03-09T14:50:00Z","agent":"api-designer","event":"completed","wave":"2","outputs":["docs/architecture/api/openapi/order-service.yaml"],"duration_seconds":3000,"error":null}
```

Why it is wrong: No `started` entry was logged. Every agent MUST log `started` before doing work and `completed`/`failed` when done. The lead uses the `started` entry to track which agents are active.

### BAD -- Failed with null error

```jsonl
{"run_id":"f47ac10b-...","type":"lifecycle","timestamp":"2026-03-09T14:20:00Z","agent":"api-designer","event":"failed","wave":"2","outputs":[],"duration_seconds":1200,"error":null}
```

Why it is wrong: A `failed` event MUST have a non-null `error` string describing what went wrong. Silent failures violate CLAUDE.md rule #10 ("No silent failures").

## Common Mistakes

1. **Logging started after doing work** -- The `started` lifecycle entry must be the very first action, before reading inputs or making decisions. If the agent fails during input reading, the started entry ensures the lead knows the agent attempted to run.

2. **Omitting files from the outputs array** -- The `completed` entry must list ALL files written, including the context summary. Missing files make it impossible for the lead to verify completeness via the manifest.

3. **Using null for error on failed events** -- Every `failed` entry must include a descriptive `error` string. `null` means "no error" which contradicts the `failed` event type. Per CLAUDE.md rule #10, no silent failures are allowed.

4. **Incorrect duration_seconds calculation** -- Duration measures from the `started` (or `retried`) timestamp to the current event timestamp. Common errors include measuring from session start instead of agent start, or using milliseconds instead of seconds.

5. **Wrong wave number** -- Each agent has a fixed wave assignment. Using the wrong wave value corrupts the lead's orchestration logic. Check the wave assignment tables above.

6. **Skipping the escalation message on failure** -- Logging the `failed` lifecycle entry is not enough. The 3-step failure protocol requires: (1) log failed, (2) write partial output, (3) send ESCALATION message to lead. All three steps are mandatory.
