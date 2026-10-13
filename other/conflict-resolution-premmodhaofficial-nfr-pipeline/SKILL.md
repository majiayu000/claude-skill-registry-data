---
name: conflict-resolution
description: >
  Use this when an agent's output contradicts another agent's, when a decision
  falls in a domain another agent owns, when same-wave designs are incompatible,
  or when a phase lead receives an ESCALATION message. Covers ownership-matrix
  lookup, escalation message format, assumption marking, phase-lead resolution
  procedure, and conflict-resolution decision-log tagging.
  Triggers: conflict, ownership, escalation, ESCALATION, assumption, contradiction, phase-lead, resolution.
---

# conflict-resolution


---



# Conflict Resolution

Provides the step-by-step conflict detection, escalation, and resolution protocol for the multi-agent architecture design fleet, ensuring single-owner authority and traceable resolution across both Architecture and Detailed Design phases.

## When to Activate
- When an agent discovers its output contradicts another agent's output
- When an agent needs to make a decision in a domain it does not own
- When two Wave 2 agents produce incompatible designs
- When an agent reads another agent's context summary and finds conflicting assumptions
- When architecture-lead or detailed-design-lead receives an ESCALATION message
- Used by: all Wave 2 agents (api-designer, infrastructure-architect, database-architect, pattern-advisor, interface-designer, algorithm-designer, concurrency-designer, component-designer, data-model-designer, sdk-designer), architecture-lead, detailed-design-lead

## Ownership Matrix Lookup Process

Before making any decision, check whether the domain is owned by this agent or another.

### Step 1: Identify the Domain

Determine which domain the decision falls into. Common domains:

| Domain Category | Examples |
|----------------|----------|
| Service boundaries | Which microservice owns a capability, service splitting/merging |
| Data schemas | Table structure, column types, relationships, constraints |
| API contracts | Request/response shapes, endpoint naming, HTTP methods |
| Event subjects | NATS subject naming, message payload structure |
| Infrastructure | Stream/consumer config, deployment topology, resource sizing |
| Auth flow | Token propagation, permission model, session handling |
| Design patterns | Which pattern applies, pattern parameters |

### Step 2: Look Up the Owner

#### Architecture Phase Ownership Matrix (CLAUDE.md rule #7)

| Domain | Owner | Consulted |
|--------|-------|-----------|
| Service boundaries & decomposition | system-decomposer | ALL |
| Tenant isolation strategy | system-decomposer | database-architect, infrastructure-architect |
| Entity/table schemas | database-architect | api-designer |
| Request/response DTOs | api-designer | database-architect |
| NATS subject naming & hierarchy | api-designer | infrastructure-architect |
| NATS stream/consumer config | infrastructure-architect | api-designer |
| Auth token propagation | api-designer | simulated-security-architect |
| Design pattern selection | pattern-advisor | ALL Wave 2 agents |
| Final architecture synthesis | architecture-lead | ALL |

#### Detailed Design Phase Ownership Matrix (CLAUDE.md Detailed Design section)

| Domain | Owner | Consulted |
|--------|-------|-----------|
| Go package structure & components | component-designer | interface-designer, sdk-designer |
| Detailed SQL schemas & migrations | data-model-designer | component-designer |
| Internal SDK libraries | sdk-designer | component-designer, concurrency-designer |
| DTOs, validation, error types | interface-designer | component-designer, data-model-designer |
| Business logic algorithms | algorithm-designer | component-designer |
| Concurrency patterns | concurrency-designer | component-designer, sdk-designer |
| Coding guidelines | coding-guidelines-generator | ALL design agents |
| Final detailed design synthesis | detailed-design-lead | ALL |

### Step 3: Determine Action

| Situation | Action |
|-----------|--------|
| Agent owns the domain | Make the decision, log it, proceed |
| Agent is consulted on the domain | Document concerns, defer to owner |
| Agent is neither owner nor consulted | Do not decide; escalate if needed |
| Owner's output not yet available | Proceed with assumption (see below) |

## Proceeding with Assumptions

Per CLAUDE.md rule #7, when an agent needs to make a decision in a domain it does NOT own and the owner's output is not yet available:

### Step 1: Make a Best-Judgment Decision

The agent proceeds with its best judgment to avoid blocking.

### Step 2: Mark the Assumption in Output Files

```markdown
<!-- ASSUMPTION -- pending database-architect confirmation -->
Entity table primary key is UUID v7 with composite index on (tenant_id, entity_id).
This assumption affects the DTO field types in CreateEntityRequest.
```

### Step 3: Mark the Assumption in Context Summary

```markdown
## Dependencies & Assumptions
<!-- ASSUMPTION -- pending database-architect confirmation -->
- Assumed UUID v7 PKs for all tenant-scoped entities
- Assumed composite index (tenant_id, entity_id) on all tables
```

### Step 4: Flag in Decision Log

Log the assumption as a decision with `"confidence": "low"` and appropriate tags:

```json
{
  "run_id": "f47ac10b-...",
  "type": "decision",
  "timestamp": "2026-03-09T14:15:00Z",
  "agent": "api-designer",
  "phase": "api-design",
  "decision": "DTO ID fields use UUID v7 type, matching assumed database PK strategy",
  "rationale": "database-architect output not yet available; UUID v7 is the most likely choice given project constraints",
  "alternatives_considered": ["UUID v4", "ULID", "BIGSERIAL"],
  "trade_offs": "May require DTO changes if database-architect chooses a different PK strategy",
  "confidence": "low",
  "status": "success",
  "context": "Designing CreateEntityRequest DTO; database-architect has not published schemas yet",
  "impacts": ["database-architect"],
  "reversibility": "easy",
  "tags": ["assumption", "pending-confirmation"]
}
```

## When to Escalate vs Proceed with Assumptions

| Scenario | Action |
|----------|--------|
| Owner's output not yet available, decision is reversible | Proceed with assumption |
| Owner's output not yet available, decision is irreversible | Escalate to lead |
| Agent reads owner's output and disagrees | Escalate to lead |
| Two agents produce directly contradictory outputs | Escalate to lead |
| Minor stylistic difference between agents | Proceed, do not escalate |
| Agent discovers a gap in its own owned domain | Decide and log, no escalation needed |

### Reversibility Guide

| Reversibility | Examples | Action |
|---------------|----------|--------|
| Easy | Naming conventions, DTO field names, log format | Proceed with assumption |
| Moderate | Index strategy, NATS subject hierarchy, middleware ordering | Proceed with assumption, flag for review |
| Hard | Primary key type, tenant isolation model, encryption strategy | Escalate before proceeding |
| Irreversible | Data model fundamentals, auth protocol, compliance approach | Always escalate |

## ESCALATION Message Format

When escalation is needed, send a message to the lead using this exact format:

```
ESCALATION: CONFLICT between <agent-A> and <agent-B> on <domain>.
<agent-A> position: <brief description>.
<agent-B> position: <brief description>.
Ownership: <domain> is owned by <owner-agent> per CLAUDE.md rule #7.
Recommended resolution: <agent's recommendation>.
```

### Example

```
ESCALATION: CONFLICT between api-designer and database-architect on entity field naming.
api-designer position: Use camelCase in JSON DTOs with snake_case mapping annotations.
database-architect position: Use snake_case everywhere for consistency with SQL columns.
Ownership: Request/response DTOs owned by api-designer; Entity/table schemas owned by database-architect.
Recommended resolution: camelCase in DTOs, snake_case in DB, explicit mapping layer in component-designer.
```

## How the Lead Resolves Conflicts

When `architecture-lead` or `detailed-design-lead` receives an ESCALATION message, the resolution follows CLAUDE.md rule #8:

### Step 1: Read Both Positions
The lead reads the context summaries and relevant output files from both agents.

### Step 2: Decide Based on Ownership Matrix
The domain owner's position is preferred unless:
- It violates a non-negotiable constraint (see `docs/architecture/constraints.md`)
- It creates a cross-cutting inconsistency that affects 3+ other agents
- The consulted agent raises a valid security, compliance, or data integrity concern

### Step 3: Log the Resolution

The lead logs a decision entry with `"tags": ["conflict-resolution"]`:

```json
{
  "run_id": "f47ac10b-...",
  "type": "decision",
  "timestamp": "2026-03-09T16:00:00Z",
  "agent": "architecture-lead",
  "phase": "review",
  "decision": "Field naming: camelCase in API DTOs (api-designer owns), snake_case in DB columns (database-architect owns), explicit mapping in Go struct tags",
  "rationale": "Each agent's convention is correct within its owned domain; mapping layer resolves the mismatch without forcing either to change",
  "alternatives_considered": ["snake_case everywhere", "camelCase everywhere", "auto-generated mapping"],
  "trade_offs": "Requires explicit json/db struct tags on every Go model; adds maintenance burden",
  "confidence": "high",
  "status": "success",
  "context": "ESCALATION: CONFLICT between api-designer and database-architect on entity field naming",
  "impacts": ["api-designer", "database-architect", "component-designer", "interface-designer"],
  "reversibility": "moderate",
  "tags": ["conflict-resolution", "field-naming"]
}
```

### Step 4: Notify the Non-Owning Agent

The lead sends a message to the agent whose position was overridden (or both agents if a compromise was reached):

```
RESOLUTION: Field naming conflict resolved. camelCase in DTOs, snake_case in DB. See decision log. Please update your output to align.
```

### Step 5: Update ARCHITECTURE.md or DETAILED-DESIGN.md

If the lead cannot resolve the conflict, it is recorded as an open question:

```markdown
## Open Questions
- **Field naming consistency**: api-designer and database-architect have different conventions.
  Resolution deferred to implementation phase. Current approach: mapping layer in struct tags.
```

## Conflict-Resolution Decision Log Tags

All conflict-resolution entries MUST include these tags:

| Tag | Required | Purpose |
|-----|----------|---------|
| `conflict-resolution` | Always | Identifies the entry as a conflict resolution |
| Domain tag (e.g., `tenant-isolation`) | Always | The domain where the conflict occurred |
| `assumption` | If applicable | If resolution involved confirming/rejecting an assumption |
| `cross-cutting` | If applicable | If resolution affects 3+ agents |

## Examples

### GOOD -- Assumption Marking in Go Code

```go
// Package orderservice contains the order management service.
//
// ASSUMPTION: pending database-architect confirmation
// Entity PK is UUID v7 with composite (tenant_id, entity_id) index.
package orderservice

// Order represents a domain entity.
// [traces-to: order-service]
type Order struct {
    ID       uuid.UUID `json:"id" db:"id"`
    TenantID uuid.UUID `json:"tenantId" db:"tenant_id"` // ASSUMPTION: UUID v7
    Subject  string    `json:"subject" db:"subject"`
    Status   string    `json:"status" db:"status"`
}
```

### BAD -- Silently Overriding Another Agent's Domain

```go
// Package orderservice uses BIGSERIAL primary keys for performance.
package orderservice

type Order struct {
    ID       int64     `json:"id" db:"id"`           // Decided BIGSERIAL
    TenantID uuid.UUID `json:"tenantId" db:"tenant_id"`
}
```

Why it is wrong: Primary key type is owned by `database-architect`. The `api-designer` or `component-designer` cannot unilaterally decide to use BIGSERIAL without an assumption marker or escalation. This creates a silent conflict that will surface late.

## Common Mistakes

1. **Deciding in a domain without checking ownership** -- Before making any cross-domain decision, always consult the ownership matrix. Even if the decision seems obvious, the owner may have context that changes the answer.

2. **Escalating minor stylistic differences** -- Not every disagreement is a conflict. If two agents name things slightly differently but the semantics match, the non-owner should align with the owner's convention without escalating. Reserve escalation for genuine incompatibilities.

3. **Omitting the `conflict-resolution` tag in the decision log** -- When the lead resolves a conflict, the decision entry MUST include the `"conflict-resolution"` tag. Without it, the conflict audit trail is broken and future agents cannot find prior resolutions.

4. **Proceeding with assumptions on irreversible decisions** -- If a decision is hard or irreversible (e.g., primary key strategy, encryption model), always escalate instead of assuming. Reversibility determines whether to assume or escalate.

5. **Not updating output after receiving a RESOLUTION message** -- When the lead resolves a conflict and the non-owning agent receives a RESOLUTION message, that agent MUST update its output files to align. Ignoring resolution messages creates persistent inconsistencies.

6. **Escalating without including both positions** -- The ESCALATION message format requires both agents' positions, the ownership reference, and a recommended resolution. Incomplete escalation messages slow down resolution because the lead has to investigate independently.
