---
name: flow-discover
description: Discover and approve feature requirements through focused interviewing and repository research. Use when the user has a feature idea, unclear scope, conflicting requirements, or needs Flow context artifacts before design.
---

# Discover a feature

Read [discovery](../../references/discovery.md), [artifacts](../../references/artifacts.md), [memory](../../references/memory.md), and [safety](../../references/safety.md) before starting.

## Procedure

1. Confirm PWDEV Flow state exists or explain that `$flow-init` is the prerequisite for persisted artifacts.
2. Inspect applicable `AGENTS.md`, repository structure, existing behavior, tests, product context, and active relevant memories without reading secrets.
3. Classify the request as quick, standard, or product-level. Route bounded changes to `$flow-quick`; route product problems to `$flow-product` when a PRD is needed.
4. Interview one focused decision at a time using the minimum questions required by [discovery](../../references/discovery.md).
5. Separate confirmed facts, user decisions, repository observations, assumptions, and open questions.
6. Research stack and domain pitfalls from repository evidence first. Use current primary sources when external facts may have changed.
7. Write the context artifacts and set state to `DISCOVERING` while questions remain.
8. Present problem, actors, scope, rules, acceptance criteria, risks, and open questions for approval.
9. On approval, mark the discovery gate `APPROVED` and recommend `$flow-design`. Otherwise revise requirements or set `BLOCKED` with the missing decision.

## Collaboration

Work inline by default. Use a read-only research worker only when the user explicitly requests parallel agent work, following [collaboration](../../references/collaboration.md). Keep the interview and approval gate in the primary conversation.

## Output

Return `STATUS`, feature slug, requirements path, supporting context paths, gate result, and `NEXT`. Do not make architecture decisions during discovery.
