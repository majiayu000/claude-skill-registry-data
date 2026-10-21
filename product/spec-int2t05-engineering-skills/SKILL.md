---
name: spec
description: Write or revise requirements with observable acceptance criteria. Triggers on "write spec", "写需求文档".
---

# Spec

## When to use

- Write or revise requirements with observable acceptance criteria.

**Not for:** architecture for technical design; documentation-audit for descriptive drift.

## Steps

1. Read relevant material and confirmed decisions; resolve unknown goals, scope and acceptance without asking the user to guess inspectable facts.

2. Describe scenarios, behavior, rules and relevant exceptions; technical implementation belongs in TECH.

3. Connect requirements to observable acceptance cases. Cover permissions, repetition, failure and recovery where needed; preserve confirmed scope and stable IDs.

4. Prepare a readable draft at the approved path with open decisions and risk-based audit items; confirm governing requirements before dependent implementation.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/PRD.md`; optionally `docs/vX.Y/prd.md` for separately maintained release scope.

## Verify

- Core requirements have observable acceptance cases; approval and unresolved scope are honestly reported.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [product-principles.md](../../../references/product-principles.md) — product discipline (need≠feature, outcomes over outputs, say no to good ideas, the real competitor is the workaround).
- [references/readable-prd-guide.md](references/readable-prd-guide.md) — readable-spec craft rules: layout density, Mermaid figures, requirement cards, human audit & OPN formats, update discipline, engineering sections.
- [references/prd-patterns.md](references/prd-patterns.md) — PRD structure, user stories, Given/When/Then acceptance criteria, INVEST, Non-Goals, success-criteria reframing, anti-patterns.
- [references/prioritization.md](references/prioritization.md) — RICE, ICE, Kano, MoSCoW, Value×Feasibility matrix, true-need vs false-need filter.
- [references/metrics-frameworks.md](references/metrics-frameworks.md) — North Star metric, AARRR funnel, retention curves, cohort analysis, Hook Model, A/B testing discipline, data-driven loop.

- [Human audit](../../../references/human-audit.md) — artifact consent and review.
