---
name: pre-build-review
description: Run a pre-implementation plan review that attacks a settled product, UI, or technical plan for blockers, missing states, edge cases, accessibility gaps, mobile failures, awkward data assumptions, and implementation ambiguity. Invoked automatically by the build skill before implementation, and available manually before coding after grill-with-docs, paper-prototype, a design decision, prototype, PRD, brief, or implementation plan, especially when the user asks to red-team, sanity-check, review, or decide go/no-go before build.
---

# Pre-build Review

## Overview

Use this as a small gate before implementation. Its job is to find the plan gaps that would become expensive once coding starts, then route the work back to the right stage if needed.

Do not turn this into a broad strategy exercise. Review the plan, name the risks, and decide whether it is ready to build.

## Inputs

Use the user's plan, brief, prototype notes, issue, PRD, `CONTEXT.md`, ADRs, or nearby code as evidence. If important context can be found in the repo, inspect it instead of asking.

Ask a concise question only when the missing context makes the go/no-go decision unreliable.

## Workflow

1. Reconstruct the intended build in 2 to 4 sentences.
2. Identify which stage should own any unresolved issue:
   - Product or domain uncertainty returns to `grill-with-docs`.
   - UI direction uncertainty returns to `paper-prototype`.
   - Implementation ambiguity can usually be resolved in the build plan.
3. Attack the plan through these lenses:
   - Scope clarity, non-goals, and decision boundaries.
   - Missing states: loading, empty, error, disabled, permission, offline, long content, maximum volume, and partially complete data.
   - Data assumptions: ownership, identity, persistence, ordering, sync, validation, privacy, and failure modes.
   - Interaction and responsive behaviour: mobile, keyboard, focus, hover-only affordances, touch targets, interruption, and recovery.
   - Accessibility: semantics, labels, contrast, reduced motion, screen reader flow, and visible focus.
   - Technical fit: integration points, existing patterns, dependencies, migration risk, test surface, and deployment constraints.
   - Coherence: the plan must name the pattern it extends, the task it improves, the states it adds, and the complexity it removes or justifies.
   - Product feel: copy, feedback, pacing, affordance clarity, and whether the result will feel generated or considered.
4. Decide whether to proceed.

## Output

Lead with the verdict:

- `Go`: ready to build.
- `Go with changes`: buildable after specific adjustments.
- `No-go`: return to an earlier stage first.

Then provide only the useful detail:

- `Blockers`: issues that must be resolved before coding.
- `Risks`: issues that can be managed during implementation.
- `Missing states`: specific states the build must cover.
- `Accessibility/mobile checks`: concrete checks to include.
- `Implementation questions`: questions the builder must answer or assumptions to lock.
- `Recommended changes`: brief edits to the plan, brief, or prototype.
- `Next step`: the single next action.

Each finding names the stage that owns it, so a `No-go` returns to the right place: product or domain uncertainty to `grill-with-docs`, UI direction to `paper-prototype`, implementation ambiguity to the build plan. A `Go` hands off to implementation — the `build` skill, applying the `ui-craft` suite for user-facing work.

## Rules

- Be direct. Do not soften a real blocker.
- Prefer concrete scenarios over abstract warnings.
- Do not invent new product direction unless the existing plan is broken.
- Do not block on details that are cheap and safe to resolve during implementation.
- If the user asks to continue into implementation, resolve blockers or get explicit confirmation before building; an explicit owner override is recorded by the build skill as `Go with changes`.
