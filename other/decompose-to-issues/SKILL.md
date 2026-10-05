---
name: decompose-to-issues
description: Break high-level work into independently executable GitHub issues using vertical slices. Use when a plan, PRD, roadmap item, or vague feature needs issue-sized execution units.
---

# Decompose To Issues

Use decomposition as context control, not project-management ceremony.

## Workflow

1. Identify the user-visible or operational outcome.
2. Split by vertical slices that can be implemented, reviewed, and verified independently.
3. Put shared setup before dependent slices only when it unlocks multiple issues.
4. Mark dependencies explicitly. Check dependencies between issues: are they real, or are they artifacts of thinking horizontally?
   - **Real dependency**: Issue B cannot be compiled, tested, or deployed without Issue A's code or schema in the target branch (e.g. Issue B consumes an API contract introduced in Issue A).
   - **Horizontal artifact**: Dividing tasks by technical layer (e.g. Issue A for database migration, Issue B for API controller, Issue C for UI). Collapse these into vertical slices that deliver testable end-to-end functionality.
5. Target 3-7 issues for a typical plan. Fewer than 3 usually means slices are too fat; more than 7 usually means you are decomposing tasks instead of value. If a project genuinely requires more than 7 vertical slices, organize the work into milestone phases of 3-7 issues each, completing Phase 1 before decomposing Phase 2.
6. Keep each issue small enough for a fresh agent to complete in one focused pass when possible.

## Issue Shape

Each issue should include:

- Problem
- Acceptance criteria
- Verification plan
- Expected test layers
- Constraints / non-goals
- Links and relevant files
- Risk level

## Wide-Refactor Exception: Expand / Contract

While feature work must always be decomposed into vertical slices, wide cross-cutting refactors (e.g. database schema migrations affecting multiple services, public API signature changes, or replacing an ORM/library across dozens of callers) cannot be delivered in a single vertical slice without risking regressions or producing unreviewable mega-PRs.

For these wide refactors, decompose using the **Expand / Contract** pattern (branching by abstraction):

1. **Expand Issue**: Introduce the new schema, API, or abstraction alongside the old one. Add dual-writing or compatibility adapters so existing callers continue to work without disruption.
2. **Migrate Issues (in batches)**: Migrate existing callers in small, independently-releasable batches (e.g. one subsystem or 3-5 callers per issue). Each batch must be verified and merged independently.
3. **Contract Issue**: Once all callers have migrated and verified in production, remove the deprecated API, adapter shims, or old database columns, leaving clean, non-duplicated code.

## Guardrails

- Avoid horizontal slices like "build backend" and "build frontend" unless the architecture truly requires it.
- Do not create issues that require inherited conversation context to understand.
- Create follow-up issues for scope discovered during implementation.
