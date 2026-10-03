---
name: plan-work
description: Use for software implementation planning when the user asks for planning, an implementation plan, approach comparison, task breakdown, roadmap, step-by-step plan, or splitting a feature/refactor into clear implementation slices before the next safe implementation step, or when a requested software implementation has unresolved implementation approach, dependency-ordering, sequencing, migration, compatibility, rollout, or scope decisions that cannot be safely inferred. Do not use when the primary request is an architecture, ownership, interface, seam, or dependency-boundary decision; use design-codebase first when available, then return here for dependent rollout or sequencing planning. Do not use for PRD authoring, issue or tracker drafting/publication, durable multi-session decision-map workflows, ordinary code explanation, or implementation of an already-settled plan.
---

# Plan Work

Plan only when planning will reduce risk or clarify execution. Keep ordinary edits in the lightweight development flow.

## First Decision

- If the user explicitly asks for a plan, provide a plan proportionate to the task even when the task is small.
- If the user asks only to plan, do not implement until they ask.
- If the user did not ask for a plan and the task is a small obvious edit or the next safe implementation step is already clear, do not create a plan.
- A task being large, medium-complexity, or multi-file is not by itself a planning trigger.
- If a requested implementation has unresolved approach, dependency, sequencing, migration, compatibility, or scope decisions that cannot be safely inferred, use this workflow to settle only those decisions.
- If the unresolved decision is primarily about architecture, ownership, interfaces, seams, adapters, or dependency boundaries, use `design-codebase` first. Return to this workflow only for dependent rollout, sequencing, migration, compatibility, or scope planning.
- If requirements are unclear, ask the smallest question that changes scope, risk, or approach.
- If a decision is non-obvious, compare the smallest useful set of approaches with trade-offs and a recommendation.
- If the work is too large for one pass, split it into vertical slices.

## Planning Loop

1. Inspect the relevant code, docs, commands, or prior notes before committing to a plan.
2. State the goal in one sentence.
3. Name constraints that affect the implementation: platform, existing patterns, dependencies, performance, data migration, compatibility, or user workflow.
4. Choose an approach. For meaningful alternatives, explain why the chosen option fits best.
5. Break work into executable steps with likely files, verification points, and dependencies.
6. Call out risks, unknowns, and out-of-scope items.

If required project context cannot be inspected, do not invent file paths, commands, dependencies, or existing patterns. State the evidence gap, distinguish confirmed project facts from assumptions, and either produce a clearly provisional plan or ask the smallest question that materially changes the plan.

Before presenting any plan:

- Ensure each step has an observable outcome and a verification point.
- Remove vague placeholders; label any remaining unverified path, command, dependency, or project pattern as an assumption.

## Plan Shape

For normal project work, use a compact plan in chat.

Create or update a durable markdown plan only when the user explicitly requests a file or names an existing plan artifact to update. Otherwise, keep the plan in chat and do not choose a project-specific planning path.

Read [plan-template.md](references/plan-template.md) when producing a durable implementation plan.

Read [vertical-slices.md](references/vertical-slices.md) when splitting a feature, refactor, or PRD into independently useful chunks.

Read [deprecation-and-migration.md](references/deprecation-and-migration.md) when the plan explicitly retires, replaces, migrates, or compatibility-transitions an API, system, feature, dependency, consumer, or data shape.

Read [design-questions.md](references/design-questions.md) when the request is still too vague to plan safely.

## Exit To Implementation

- When a request includes implementation, treat planning as a transient internal phase: once the needed decisions are settled, exit to implementation automatically unless user-only input, an irreversible trade-off, or a scope change remains.
- Do not regenerate, expand, or compare the settled plan unless new evidence changes scope, dependencies, risk, or feasibility; treat it as implementation context rather than a reason to plan again.

## Boundaries

Do not automatically create PRDs, specs, ADRs, issues, decision maps, or subagent workflows.

Do not save plans to a project-specific planning path, publish issue tracker items, or require approval gates unless the user asks for that workflow.

- When a plan file is explicitly authorized, use only the named path; do not guess, duplicate, overwrite, or reuse another target.
