---
name: flow-design
description: Design an approval-gated feature specification from approved requirements. Use when PWDEV Flow discovery is complete and the user needs architecture decisions, component boundaries, quality constraints, and a definition of done.
---

# Design the central contract

Read [specification](../../references/specification.md), [artifacts](../../references/artifacts.md), [memory](../../references/memory.md), and [safety](../../references/safety.md) before designing.

## Entry gate

Require approved requirements or an equivalent user-approved contract. If requirements are missing, contradictory, or materially open, stop and recommend `$flow-discover` rather than inventing them.

## Procedure

1. Read requirements, project context, applicable repository instructions, current architecture, and relevant decisions or conventions.
2. Identify consequences for components, interfaces, data, permissions, compatibility, failures, operations, and tests.
3. Present consequential architecture choices with viable alternatives, trade-offs, and one recommendation. Obtain user approval before locking each decision.
4. Create `.planning/flow/phases/<slug>/spec.md` with all eight required sections from [specification](../../references/specification.md).
5. Record approved choices in `decisions.md`; capture only genuinely durable decisions through `$flow-memory` semantics.
6. Check every requirement has a specification clause and every definition-of-done item has executable evidence.
7. Scan for ambiguous language, hidden scope, unresolved placeholders, and contradictions.
8. Present the specification for approval. Do not continue to planning in the same step unless the user has explicitly approved it.

## Boundaries

- Keep implementation work out of design.
- Prefer established repository patterns unless the approved requirement demands a departure.
- Return to discovery when a proposed design would change product scope.

## Output

Return `STATUS`, specification path, decisions path, unresolved risks, gate result, and `NEXT`. Recommend `$flow-plan` only after the design gate is `APPROVED`.
