---
name: codebase-design
description: Find boundaries that hide complexity and reduce change propagation. Triggers on "deep modules", "深化模块".
---

# Codebase Design

## When to use

- Find boundaries that hide complexity and reduce change propagation.

**Not for:** refactoring for executing a structural move.

## Steps

1. Trace real callers, dependencies and representative business paths; inspect change history without requiring a subagent.

2. Identify leaked internals, shallow modules and repeated coordination with concrete call-site evidence.

3. Compare candidate boundaries by coupling, testability and migration effort; present a behavior contract and one recommendation.

4. Confirm the structural decision and testing seam before refactoring; use Markdown unless an interactive artifact was requested.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/design/codebase-audit.md` when a durable decision is needed.

## Verify

- Candidates have call-site evidence; the selected boundary states what complexity is hidden and how behavior is checked.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/language.md](references/language.md) — glossary: module, interface, implementation, depth, seam, adapter, leverage, locality + principles (deletion test, interface is the test surface, one vs two adapters)
- [references/deepening.md](references/deepening.md) — dependency categories (in-process, local-substitutable, ports & adapters, mock), seam discipline, replace-don't-layer testing
- [references/html-report.md](references/html-report.md) — HTML scaffold, Tailwind/Mermaid via CDN, diagram patterns (mass, cross-section, call-graph collapse), tone and glossary usage
- [references/interface-design.md](references/interface-design.md) — interface design criteria: what an interface includes, depth, testability rules, comparing alternatives
- [references/design-it-twice.md](references/design-it-twice.md) — parallel sub-agent pattern for exploring alternative interfaces (Ousterhout's "Design It Twice")
