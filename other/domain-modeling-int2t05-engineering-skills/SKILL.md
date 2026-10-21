---
name: domain-modeling
description: Clarify domain terms, invariants and ownership from real scenarios. Triggers on "domain model", "领域模型".
---

# Domain Modeling

## When to use

- Clarify domain terms, invariants and ownership from real scenarios.

**Not for:** schema-design for storage; architecture for system boundaries.

## Steps

1. Read existing terminology, requirements, code and decisions; identify ambiguous concepts.

2. Test terms against normal and exceptional scenarios, specifying invariants and state transitions rather than extracting nouns into entities.

3. Resolve business ambiguity with the user and update the glossary and affected approved descriptions consistently.

4. Record only consequential decisions separately; give examples distinguishing similar concepts.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `CONTEXT.md`; optionally `docs/design/adr/NNNN-slug.md`.

## Verify

- Terms explain actual scenarios and invariants; glossary and implementation agree or discrepancies are explicit.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/context-format.md](references/context-format.md) — CONTEXT.md structure, rules, single vs multi-context repos
- [references/adr-format.md](references/adr-format.md) — ADR template, numbering, what qualifies as an ADR-worthy decision
