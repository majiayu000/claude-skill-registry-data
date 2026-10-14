---
name: craft-adr
description: Recording architectural decisions. Why we chose X over Y.
---

# Skill: Craft ADR

> "Decisions in code are temporary. Decisions in ADRs are permanent."

## The Standard

1. **Location**: `docs/{domain}/ADR/ADR-001-title.md`.
2. **Status**: Proposed → Accepted → Deprecated.
3. **Structure**: Context → Decision → Consequences.
4. **Rationale**: Document what was rejected and why.

## When to Record

| Record               | Don't Record      |
|----------------------|-------------------|
| Package choice       | Trivial fixes     |
| Pattern choice       | Standard CRUD     |
| Schema design        | Config changes    |
| Integration approach | Obvious decisions |

## Real-World Examples

See [examples.md](examples.md).
