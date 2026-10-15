---
name: architectural-decision-records
description: Use when analyzing architecture diagrams or descriptions to create ADRs, when architecture has gaps in observability/resilience/security, or when architectural decisions lack documentation - systematically identifies blind spots and generates lightweight decision records
---

# Generating Architectural Decision Records

## Overview

Turn architecture diagrams and descriptions into lightweight ADRs by systematically questioning decisions and identifying blind spots. Focus on capturing WHY decisions were made, not just WHAT exists.

## The Process

**Understanding the Architecture:**
- Examine provided architecture (diagrams, text, or code)
- Identify explicit decisions: technology choices, patterns, boundaries
- Note what's stated vs what's implied

**Questioning Decisions (One at a Time):**
- Ask ONE focused question per message
- Prefer "Why X instead of Y?" over "Tell me about X"
- Focus on uncovering: rationale, alternatives considered, constraints, trade-offs
- Examples:
  - "Why PostgreSQL over MongoDB for user data?"
  - "Why separate these services instead of one service?"
  - "What led to choosing REST over events?"

**Identifying Blind Spots Systematically:**
Check for missing architectural decisions using this checklist:
- **Observability**: Error tracking? Monitoring? Logging strategy?
- **Resilience**: Failure handling? Circuit breakers? Retries? Timeouts?
- **Security**: Authentication? Authorization? Data protection? Attack surface?
- **Scalability**: Bottlenecks? Caching? Load balancing?
- **Data Consistency**: Consistency model? Transaction boundaries?
- **Deployment**: Strategy? Rollback? Blue-green? Canary?
- **Testing**: Integration points? Contract testing? E2E strategy?
- **Performance**: Latency requirements? Query optimization?

Ask about gaps ONE AT A TIME. Present conversationally, not as interrogation.

**Generating ADRs:**
- Use lightweight format (below)
- Create separate ADR for each decision
- Number sequentially: ADR-001, ADR-002, etc.
- Save to `docs/adr/` directory
- Keep brief - capture essence, not exhaustive detail

## ADR Format

```markdown
# ADR-NNN: [Short Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]

## Context

What problem or constraint drove this decision? (1-2 sentences)

## Decision

What was chosen? Be specific. (1 sentence)

## Consequences

**Positive:**
- Benefit 1
- Benefit 2

**Negative:**
- Trade-off 1
- Trade-off 2

**Risks:**
- Risk to monitor
```

**Good example (proper brevity):**

```markdown
# ADR-003: Use PostgreSQL for Transactional Data

**Status:** Accepted

## Context

E-commerce platform requires ACID guarantees for financial transactions to meet regulatory compliance. Team has PostgreSQL expertise but no DynamoDB experience.

## Decision

Use PostgreSQL for all transactional data (orders, payments, inventory).

## Consequences

**Positive:**
- ACID compliance meets regulatory requirements
- Leverages existing team expertise
- Strong consistency for financial operations

**Negative:**
- Schema changes require migration planning
- Vertical scaling limits at very high scale

**Risks:**
- Performance bottlenecks at scale - monitor query times and add read replicas as needed
```

## Being Pragmatic

**Not all ADRs are "perfect":**
- Documenting after implementation? That's fine - capture what IS known
- Decision made by authority? Document that honestly
- Alternatives not evaluated? Note that as a gap
- Unknown trade-offs? State what needs monitoring

**Focus on value:**
- Better to have honest "we chose X because team familiarity" than fiction
- ADRs for future decisions are more valuable than perfect retrospectives
- Identify implicit decisions that SHOULD have ADRs but don't yet

## Key Principles

- **One question at a time** - Don't overwhelm with 5 questions simultaneously
- **Why over what** - Focus on rationale, not technology descriptions
- **Systematic gap checking** - Use checklist, don't rely on memory
- **Spot implicit decisions** - Auth, deployment, monitoring often unstated
- **Pragmatic over purist** - Honest documentation beats perfect documentation
- **Lightweight over comprehensive** - Brief ADRs that capture essence

## After ADR Generation

**Documentation:**
- Save each ADR separately: `docs/adr/ADR-NNN-title.md`
- Create index: `docs/adr/README.md` listing all ADRs
- Commit each ADR with descriptive message

**Identify Future Decisions:**
- Note areas needing architectural decisions
- Flag "we'll figure it out later" items
- Suggest which gaps to address next
