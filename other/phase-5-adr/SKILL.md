---
name: phase-5-adr
description: Phase 5 — Architecture Decisions with ADR generation and validation
version: 2.0.0
tags: [architecture, adr, decisions, phase-5]
trigger_keywords: [adr, architecture decision, pattern selection]
requires_approval: true
estimated_duration: 20-40 minutes
---

# Skill: Phase 5 — Architecture Decisions (ADR)

## Purpose

Execute Phase 5: apply the architecture decision tree, create ADRs for every significant decision, generate C4 diagrams, and validate all ADRs before marking as Accepted.

## When to use

- Phase 5 of the full 8-phase cycle
- When the user needs architecture guidance independently
- When designing a new module or refactoring an existing system

## Decision Tree

Answer these questions in order to select the primary architectural pattern:

1. **Single team or multiple autonomous teams?**
   - Single → Modular Monolith
   - Multiple → Microservices

2. **Does business complexity require a rich domain model?**
   - Yes → Hexagonal Architecture / DDD
   - No → Layered Architecture

3. **Is full state audit trail required?**
   - Yes → Event Sourcing
   - No → Standard persistence

4. **Are reads and writes radically different in volume?**
   - Yes → CQRS
   - No → Standard CRUD

5. **Are there distributed transactions across services?**
   - Yes → Saga pattern (Orchestration or Choreography)
   - No → Local transactions

## ADR Template (mandatory sections)

Every ADR must include:

```markdown
# ADR-NNN: Short description of the decision

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Deciders:** Name, Role

## Context

[2-3 paragraphs: problem, constraints, why decide now]

## Decision

[Clear statement of the decision]

## Alternatives Considered

| Alternative | Pros | Cons | Why rejected |
|---|---|---|---|
| Option A | ... | ... | Rejected because [reason] |
| Option B | ... | ... | Rejected because [reason] |

## Consequences

**Positive:**
- [benefit 1]

**Negative:**
- [drawback 1] — mitigated by [mitigation]

## Compliance Impact

[State which standards affected, or confirm no impact]
```

## Validation step

After generating each ADR, validate it:

```bash
node packs/enterprise-architecture-pack/validators/adr-validator/src/index.ts \
  --format=console docs/adr/ADR-NNN-title.md
```

Or in Antigravity Manager mode, use code execution:
```python
import subprocess
subprocess.run(['node', '--experimental-strip-types', 
  'packs/enterprise-architecture-pack/validators/adr-validator/src/index.ts',
  '--format=console', 'docs/adr/ADR-001-isolation.md'])
```

**Gate:** If validation fails (any `error`-severity rule), fix the ADR and re-run. Only mark as Accepted after validation passes.

## C4 Diagrams

Generate minimum:
- **C4 L1 (System Context):** External actors and systems
- **C4 L2 (Container):** Services, databases, message queues

Use Mermaid format (default) or PlantUML if requested.

## Output artifacts

- `docs/adr/ADR-001-*.md`, `ADR-002-*.md`, ... (one per decision)
- C4 diagrams (inline in ADR or separate files)
- Artifact type in Manager mode: `adr_document`
