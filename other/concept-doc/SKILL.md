---
name: concept-doc
description: "Writes a short concept doc under docs/concepts before a new service or major feature is built, covering problem, goals, non goals, approach, alternatives and open questions. Use when planning a new service or major feature."
---

# Concept doc

Capture the plan for a new service or major feature before implementation.

## When to use

Write one when a new service or repository starts, a feature touches several
components or changes a data model, or a new external dependency is added.

Skip it for small fixes, refactors, version bumps and anything one pull request
description already explains.

## Steps

1. Read `AGENTS.md` for `## Deviations`. An entry that drops concept docs means: say so and
   stop.
2. Apply the gate above. If skipped, say so and stop.
3. Create one file per feature, lowercase with hyphens, in the concepts directory. No
   directory yet means this is the first record: create it now.
4. Problem: what hurts today, who is affected, what the workaround costs. No solution.
5. Goals: checkable outcomes, not tasks. Non goals: what a reader would wrongly assume
   is included.
6. Approach: components, data flow, boundaries, where it runs. Not a line by line plan.
7. Alternatives: the real reason each was dropped: cost, operational load, complexity,
   lock in.
8. Open questions: one line each, with an owner or a next step. An empty section in a
   first draft is a warning sign, not a success.
9. Link related ADRs. Write the ADR now for any decision that is already settled.
10. Review before implementation starts. Update when the approach changes.
11. Write as intent, never as if the work is already done. Do not retrofit afterwards.
12. One page, one line bullets. Depth goes to ADRs and `docs/`.
13. Promote an open question to an ADR when it is architecture, infrastructure or
    tooling, expensive to reverse, or must outlive this feature.

## Guardrails

- `## Deviations` checked before the directory is touched.
- Gate applied, concept doc actually warranted.
- `docs/concepts` created with the first record, not ahead of one.
- Problem section has no solution in it.
- Goals verifiable, non goals explicit.
- Alternatives carry real rejection reasons.
- Open questions stay honest and open, not pre answered.
- Settled decisions moved into an ADR and linked.
- One page, one line bullets.

## Config

- `docs.concepts`: directory for concept docs. Default `docs/concepts`.

## References

- `adr` for the decisions a concept doc settles.
