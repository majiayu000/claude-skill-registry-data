---
name: hig-implementation
description: "Implement bounded, evidence-backed UI/UX improvements in an existing codebase while preserving behavior, data contracts, and release safety."
---

# Ship a complete repair, not a replacement app

Follow the [root contract](../../SKILL.md). Use [improvement-plan.md](../../templates/improvement-plan.md), [component contracts](../../references/component-contracts.md), and [improvement recipes](../../references/improvement-recipes.md). This implementation process is WORKFLOW, not Apple-prescribed repository structure.

## Confirm authorization and baseline

Read repository instructions, package/build files, environment requirements, design tokens, component conventions, relevant tests, and existing documentation. Record the current revision and unrelated working-tree changes. Use only tools and capabilities actually available.

Identify the authorized slice, finding IDs, acceptance tests, protected invariants, allowed files, and rollback plan. A user’s instruction to implement a UI fix does not automatically authorize deploying to production, pushing to a protected branch, migrating databases, changing billing, or collecting analytics.

Run relevant baseline checks where feasible and record pre-existing failures. Do not suppress failing rules or delete tests to make the work appear green. Do not install a new framework to avoid understanding the old one.

## Inspect the root cause and blast radius

Trace the visible symptom through component props, state ownership, routing, data fetching, persistence, and server behavior. Search shared component consumers before changing defaults. Check whether a local inconsistency is intentional.

For a shared fix, identify all variants and downstream screens likely to change. Prefer a semantic variant over duplicated special-case styles. Avoid broad selectors, global event handlers, or unbounded style overrides that silently affect unrelated UI.

Preserve domain logic and authorization. Client-side affordances may explain allowed actions, but they must not become the security boundary. Treat validation and state consistency as part of the interaction, not work to discard during a reskin.

## Implement one vertical slice

Make the data/state behavior, visible UI, semantics, copy, loading/error states, and tests agree. A partially restyled form with broken submission is not an improvement.

Use native/established controls and the project’s existing patterns where suitable. Keep roles, labels, focus behavior, keyboard operation, and async state aligned. Add custom interactions only with a complete contract and tests.

Handle delayed, failed, canceled, and out-of-order responses. Avoid duplicate writes and stale updates. Use backend-supported guarantees for consequential transactions; a disabled button alone is insufficient.

Preserve drafts, route history, filters, sorting, and scroll/focus according to the documented state contract. Explicitly clean up event listeners, timers, observers, and requests when the lifecycle requires it. Do not turn a cosmetic fix into memory leaks or runaway rendering.

## Add focused tests

Prefer tests that reproduce the reported failure and verify the intended invariant. Add unit tests for changed deterministic logic, component tests for state/semantics, and end-to-end tests for the affected journey as appropriate to the existing stack.

Avoid broad snapshot churn as the only evidence. Use role/name-based selectors when suitable, but verify that names reflect the real intended accessible semantics. Test one realistic adverse state, not only the ideal fixture.

Do not introduce fixed sleeps as the primary synchronization strategy. Wait for meaningful state, and verify the actual data outcome where relevant. Do not mistake mocked success for integration coverage.

## Recheck visual and runtime behavior

Run applicable lint/type checks, tests, and build. Inspect the affected flow in a real browser/device or supported simulator. Compare equivalent states, not a populated before screen against an empty after screen.

Check console/runtime errors, failed network requests, focus traps, horizontal overflow, content truncation, theme/preference variants, and changed shared consumers. Measure performance when the change affects rendering, fetching, or interaction frequency.

If tools are missing, finish the safe code change and report precisely which checks were not run. Do not call a feature verified just because it compiles.

## Release and handoff

Provide changed files, finding/test links, meaningful behavior differences, preserved invariants, remaining risks, and rollback instructions. Commit, push, or deploy only within explicit authorization and repository policy.

Stop after the agreed acceptance gate. Additional attractive changes belong in the backlog unless required to complete the slice safely. Keep a bounded iteration log so a repeat pass does not reopen resolved preferences or restyle the product indefinitely.
