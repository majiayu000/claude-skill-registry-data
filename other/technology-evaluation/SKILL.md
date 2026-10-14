---
name: technology-evaluation
description: "Technology evaluation: fitness functions, landscape, proportional governance, migration guidance. Decide with trade-offs and reversibility."
---

# technology-evaluation

Decide with trade-offs and reversibility: fitness functions, proportional process, migration path.

## Activate when

- Adopting frameworks, platforms, databases, or vendors; proposing migrations or deprecations.

## Do NOT activate for

- Single-library picks (see library-selection); version lookups (see documentation-search).

## Inspection

Gather requirements, constraints (team, compliance, scale, budget), current-state pain with evidence, and candidate landscape (docs, releases, community health, hiring implications).

## Decision rules

- Fitness functions: 3–5 measurable criteria the choice must satisfy (latency, cost, operability, hiring, compliance) — scored, not vibed.
- Reversibility rules: easily reversible → decide fast, document briefly; hard to reverse (DB, cloud, framework) → spike first, ADR mandatory.
- Proportional governance: solo/small-team choices need a paragraph; org-wide bets need a reviewed ADR with migration + rollback plan.
- Total cost: license + operations + learning + exit cost. The cheapest license is rarely the cheapest choice.

## Procedure

1. Spike the top 2 candidates against the fitness functions (timeboxed).
2. Record the ADR: context, options with scores, decision, migration plan, rollback plan, review date.
3. Pilot on a bounded slice before full commitment.
4. Verify: fitness functions pass on the pilot, rollback demonstrated or explicitly waived with owner.

## Failure modes

- Resume-driven adoption; evaluation without a spike; ignoring exit cost; unbounded "evaluate everything" phases; ADR written to justify a foregone conclusion.

## Escalation

Deep-dive research method → research/documentation-search; SaaS/vendor specifics → saas/multitenancy-billing, cloud/*.

## References

- Related: `../library-selection/`, `../source-evaluation/`, `../../core/requirements-analysis/`.
