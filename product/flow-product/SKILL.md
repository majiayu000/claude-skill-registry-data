---
name: flow-product
description: Create an approval-gated product requirements document or decompose an approved PRD into a traceable roadmap. Use for product-level problems, new initiatives, multi-feature scope, PRDs, release outcomes, or roadmap planning.
---

# Plan product outcomes

Read [product](../../references/product.md), [artifacts](../../references/artifacts.md), [memory](../../references/memory.md), and [safety](../../references/safety.md).

## Route

- Use `prd` when the problem, users, goals, scope, or requirements are not yet an approved product contract.
- Use `roadmap` only when `.planning/flow/product/prd.md` exists and its gate is approved.

## PRD procedure

1. Inspect existing product and repository context before interviewing.
2. Ask one product decision at a time: problem, users, outcomes, non-goals, journeys, rules, requirements, risks, and release evidence.
3. Label facts, user decisions, assumptions, dependencies, and open questions distinctly.
4. Write the complete PRD using [product](../../references/product.md).
5. Trace each requirement with a stable ID.
6. Present the PRD for explicit approval and stop. Do not generate a roadmap from an unapproved PRD.

## Roadmap procedure

1. Read the approved PRD and applicable project context.
2. Build `Phase → Epic → Feature → Task` from outcomes rather than technical layers.
3. Give every node a parent, PRD requirement links, objective, acceptance outcome, dependencies, risks, estimate range, and status.
4. Validate there are no orphan requirements or tasks and every phase delivers measurable value.
5. Persist the hierarchy under `.planning/flow/product/roadmap/` and present it for approval.

Work inline by default. A roadmap worker is allowed only when the user explicitly requests parallel agent work; the primary conversation owns approval.

## Output

Return mode, artifact paths, traceability coverage, unresolved decisions, gate result, and next valid action.
