---
name: architecture
description: Design or audit system boundaries and consequential technical decisions. Triggers on "system design", "架构设计".
---

# Architecture

## When to use

- Design or audit system boundaries and consequential technical decisions.

**Not for:** spec for behavior; codebase-design for existing module boundaries.

## Steps

1. Extract confirmed behavior, real constraints and operational context; do not invent quality thresholds.

2. Investigate comparable implementations and current official docs for consequential choices; compare complexity, failure modes and operating costs.

3. Define components, trust boundaries, ownership, contracts and recovery using the simplest adequate architecture.

4. Record significant decisions and rejected alternatives; prepare TECH and risk-based human review before dependent implementation.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/TECH.md`; optionally `docs/vX.Y/tech.md` and `docs/design/adr/NNNN-slug.md`.

## Verify

- Boundaries and failure paths fit requirements; significant decisions have evidence, trade-offs and review criteria.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [mermaid-diagrams.md](../../../references/mermaid-diagrams.md) — Mermaid syntax for architecture diagrams
- [references/tech-audit-guide.md](references/tech-audit-guide.md) — reference-first discipline, the audit→confirm→revise→mature lifecycle, and the TECH-doc AUD catalog with table formats
- [references/nfr-checklist.md](references/nfr-checklist.md) — NFR categories (scalability, performance, availability, security, reliability, cost) with targets
- [references/architecture-patterns.md](references/architecture-patterns.md) — pattern comparison (monolith, microservices, event-driven, CQRS, serverless)
- [references/database-selection.md](references/database-selection.md) — database types and decision matrix
- [references/system-design.md](references/system-design.md) — full system design template
- [references/adr-template.md](references/adr-template.md) — ADR format, example, and naming convention
- [references/error-resilience.md](references/error-resilience.md) — throw-vs-return, error propagation, retry/circuit-breaker, idempotency, fallback UX, error-to-message mapping

- [Human audit](../../../references/human-audit.md) — artifact consent and review.
