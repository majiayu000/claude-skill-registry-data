---
name: adr-authoring
description: Architecture Decision Record creation and management
allowed-tools: Read, Glob, Grep, Write, Edit
---

# ADR Authoring Skill

## When to Use This Skill

Use this skill when:

- **Adr Authoring tasks** - Working on architecture decision record creation and management
- **Planning or design** - Need guidance on Adr Authoring approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Create and manage Architecture Decision Records (ADRs) for documenting technical decisions.

## MANDATORY: Documentation-First Approach

Before creating ADRs:

1. **Invoke `docs-management` skill** for ADR patterns
2. **Verify MADR template** via MCP servers (context7 for adr-tools)
3. **Base guidance on Michael Nygard's ADR methodology**

## ADR Overview

```text
What is an ADR?

An Architecture Decision Record (ADR) captures:
- WHAT decision was made
- WHY it was made (context and drivers)
- WHAT alternatives were considered
- WHAT the consequences are

Benefits:
- Preserves decision context for future team members
- Prevents relitigating closed decisions
- Documents trade-offs explicitly
- Creates searchable decision history
```

## ADR Templates

### Template 1: Basic (Nygard)

```markdown
# ADR-[NUMBER]: [TITLE]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context

[What is the issue that we're seeing that is motivating this decision or change?]

## Decision

[What is the change that we're proposing and/or doing?]

## Consequences

[What becomes easier or more difficult to do because of this change?]
```

### Template 2: MADR (Markdown Any Decision Record)

```markdown
# ADR-[NUMBER]: [SHORT TITLE]

## Status

[Proposed | Accepted | Deprecated | Superseded]

Date: [YYYY-MM-DD]
Deciders: [Names/Roles]

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to
three sentences or in the form of an illustrative story. You may want to
articulate the problem in form of a question.]

## Decision Drivers

* [Driver 1: e.g., technical constraint]
* [Driver 2: e.g., business requirement]
* [Driver 3: e.g., team expertise]

## Considered Options

1. [Option 1]
2. [Option 2]
3. [Option 3]

## Decision Outcome

**Chosen option:** "[Option X]", because [justification, e.g., only option
that meets requirement / best trade-off / etc.].

### Consequences

**Good:**
* [Positive consequence 1]
* [Positive consequence 2]

**Bad:**
* [Negative consequence 1]
* [Negative consequence 2]

### Confirmation

[Describe how the implementation of/compliance with the ADR is confirmed.
E.g., by a review or an ArchUnit test.]

## Pros and Cons of Options

### [Option 1]

[Example description]

* Good, because [argument]
* Good, because [argument]
* Bad, because [argument]
* Bad, because [argument]

### [Option 2]

[Example description]

* Good, because [argument]
* Bad, because [argument]

### [Option 3]

[Example description]

* Good, because [argument]
* Bad, because [argument]

## More Information

[Links to related ADRs, external documentation, or discussion threads]
```

### Template 3: Extended (Enterprise)

```markdown
# ADR-[NUMBER]: [TITLE]

| Property | Value |
|----------|-------|
| **Status** | [Proposed \| Accepted \| Deprecated \| Superseded] |
| **Date** | [YYYY-MM-DD] |
| **Author** | [Name] |
| **Reviewers** | [Names] |
| **Approvers** | [Names] |
| **Epic/Story** | [Link] |
| **Supersedes** | [ADR-XXX] |
| **Superseded By** | [ADR-XXX] |

## Executive Summary

[One paragraph summary for stakeholders who don't read the full ADR]

## Context

### Background

[Detailed context explaining the situation]

### Problem Statement

[Clear statement of the problem to be solved]

### Constraints

| Constraint | Description |
|------------|-------------|
| [C-1] | [Description] |
| [C-2] | [Description] |

### Assumptions

| Assumption | Description |
|------------|-------------|
| [A-1] | [Description] |
| [A-2] | [Description] |

## Decision Drivers

1. **[Driver 1]**: [Explanation]
2. **[Driver 2]**: [Explanation]
3. **[Driver 3]**: [Explanation]

## Options Considered

### Option 1: [Name]

**Description:** [What this option entails]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Effort:** [T-shirt size or hours]
**Risk Level:** [Low/Medium/High]

### Option 2: [Name]

[Same structure...]

### Option 3: [Name]

[Same structure...]

## Decision

**We will adopt Option [X]: [Name]**

### Rationale

[Detailed explanation of why this option was chosen]

### Trade-offs Accepted

| Trade-off | Mitigation |
|-----------|------------|
| [Trade-off 1] | [How we'll manage it] |
| [Trade-off 2] | [How we'll manage it] |

## Consequences

### Positive

- [Consequence 1]
- [Consequence 2]

### Negative

- [Consequence 1]
- [Consequence 2]

### Neutral

- [Consequence 1]

## Implementation

### Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action 1] | [Name] | [Date] | [Status] |
| [Action 2] | [Name] | [Date] | [Status] |

### Validation Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Related Decisions

- [ADR-XXX: Related Decision 1]
- [ADR-YYY: Related Decision 2]

## References

- [Reference 1]
- [Reference 2]
```

## ADR Lifecycle

```text
ADR Status Flow:

    ┌──────────────┐
    │   Proposed   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐     ┌──────────────┐
    │   Accepted   │────▶│  Deprecated  │
    └──────────────┘     └──────────────┘
           │
           ▼
    ┌──────────────┐
    │  Superseded  │
    │  by ADR-XXX  │
    └──────────────┘
```

## Numbering Convention

```text
ADR Numbering Patterns:

Sequential:
  ADR-001, ADR-002, ADR-003, ...

Date-based:
  ADR-2025-01-001, ADR-2025-01-002, ...

Category-prefixed:
  ARCH-001 (architecture)
  DATA-001 (data/database)
  SEC-001 (security)
  API-001 (API design)
```

## Example ADRs

### Example 1: Technology Choice

```markdown
# ADR-001: Use PostgreSQL as Primary Database

## Status

Accepted

Date: 2025-01-15

## Context and Problem Statement

We need to choose a primary database for the order management system.
The database must support complex queries, transactions, and scale to
millions of records.

## Decision Drivers

* Need ACID compliance for financial transactions
* Team has strong SQL expertise
* Must support JSON for flexible data
* Open source preferred for cost

## Considered Options

1. PostgreSQL
2. MySQL
3. MongoDB
4. SQL Server

## Decision Outcome

**Chosen option:** "PostgreSQL", because it provides the best combination
of ACID compliance, JSON support, and open-source licensing.

### Consequences

**Good:**
* Strong transaction support for financial data
* JSONB for flexible schema when needed
* Excellent query optimizer
* Large ecosystem and community

**Bad:**
* Requires careful tuning for high write loads
* Connection pooling essential (PgBouncer)
```

### Example 2: Architectural Pattern

```markdown
# ADR-002: Adopt Event-Driven Architecture for Order Processing

## Status

Accepted

Date: 2025-01-20

## Context and Problem Statement

The order processing system needs to coordinate multiple services
(inventory, payment, shipping) while maintaining loose coupling and
supporting eventual consistency.

## Decision Drivers

* Services must be independently deployable
* Need to handle partial failures gracefully
* Want to enable event sourcing in future
* Must support audit trail requirements

## Considered Options

1. Direct synchronous calls (REST)
2. Event-driven with message broker
3. Choreography with events
4. Orchestration with saga pattern

## Decision Outcome

**Chosen option:** "Event-driven with message broker (Kafka)", combined
with saga orchestration for complex workflows.

### Consequences

**Good:**
* Loose coupling between services
* Natural audit trail through event log
* Enables replay and debugging
* Supports eventual consistency model

**Bad:**
* Added complexity of message broker
* Eventually consistent (not immediate)
* Requires careful event schema design
* Team needs messaging expertise
```

## ADR Registry

```markdown
# Architecture Decision Registry

| ADR | Title | Status | Date | Category |
|-----|-------|--------|------|----------|
| [ADR-001](./ADR-001.md) | Use PostgreSQL | Accepted | 2025-01-15 | Data |
| [ADR-002](./ADR-002.md) | Event-Driven Architecture | Accepted | 2025-01-20 | Architecture |
| [ADR-003](./ADR-003.md) | REST for External APIs | Accepted | 2025-01-22 | API |
| [ADR-004](./ADR-004.md) | gRPC for Internal Services | Accepted | 2025-01-22 | API |

## By Category

### Architecture
- [ADR-002: Event-Driven Architecture](./ADR-002.md)

### Data
- [ADR-001: Use PostgreSQL](./ADR-001.md)

### API
- [ADR-003: REST for External APIs](./ADR-003.md)
- [ADR-004: gRPC for Internal Services](./ADR-004.md)
```

## Best Practices

### Writing Good ADRs

1. **Write early**: Capture decisions when context is fresh
2. **Be concise**: One page per ADR is ideal
3. **Include context**: Future readers need to understand why
4. **List alternatives**: Show you considered options
5. **Document consequences**: Both good and bad
6. **Keep immutable**: Supersede rather than modify

### Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No ADRs | Decisions forgotten | Start ADR practice |
| Stale ADRs | Reality diverged | Review and update status |
| Huge ADRs | Too much detail | Split into multiple ADRs |
| Vague ADRs | Not actionable | Be specific |
| Solo ADRs | No review | Require peer review |

## Workflow

When creating ADRs:

1. **Identify Decision**: Recognize significant decisions
2. **Draft ADR**: Use appropriate template
3. **Gather Options**: Research alternatives
4. **Analyze Trade-offs**: Document pros/cons
5. **Propose**: Share for feedback
6. **Decide**: Finalize with stakeholders
7. **Record**: Commit to repository
8. **Maintain**: Update status as needed

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
