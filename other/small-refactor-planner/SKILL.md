---
name: small-refactor-planner
description: Creates a minimal, behavior-preserving refactoring plan for one function, class, component, or module. Use when the user asks to simplify, extract, rename, reorganize, or improve one bounded code unit without expanding scope, changing public behavior, or planning a broader rewrite.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: code-review
  task_type: planner
  audience: software-developers-maintainers-and-coding-agents
  tags:
    - refactoring
    - code-review
    - scope-control
    - maintainability
    - behavior-preservation
    - testing
  status: draft
  side_effects: none
---

# Small Refactor Planner

## Purpose

Create the smallest useful refactoring plan for one function, class, component, or module while preserving observable behavior and preventing adjacent cleanup from widening the task.

## When to use this skill

Use this skill when:

- The user wants a plan for one clearly bounded code unit.
- The goal is a local improvement such as simplifying control flow, extracting a helper, clarifying names, reducing duplication, tightening responsibilities, or reorganizing internals.
- The change should preserve public behavior, APIs, inputs, outputs, side effects, and error handling.
- The user wants a reviewable sequence of edits and targeted validation before implementation.

Do not use this skill when:

- The request covers multiple modules, a subsystem, an architecture migration, or a broad rewrite.
- The primary goal is to add features, change behavior, fix an unconfirmed bug, or implement the refactor immediately.
- The target cannot be isolated without changing public contracts or coordinating multiple consumers.
- A large staged refactor roadmap is required.

## Inputs to inspect

Inspect only the evidence needed to understand the target and its immediate contracts:

- The named function, class, component, or module.
- Direct callers, imports, consumers, or collaborators that establish its contract.
- Focused tests, fixtures, snapshots, stories, or examples covering its behavior.
- Relevant types, interfaces, props, configuration, and error-handling conventions.
- Local repository instructions and nearby code conventions.
- The user's goal, constraints, and explicit non-goals.

Do not scan unrelated repository areas merely to collect additional cleanup opportunities.

## Workflow

1. Name one refactor target. If the request contains several independent targets, select the one the user prioritized or report that the request must be split.
2. State the desired improvement in one sentence and translate it into a measurable local outcome.
3. Record the behavior contract to preserve: inputs, outputs, public signatures, state changes, side effects, errors, ordering, rendering, accessibility behavior, and performance-sensitive behavior as applicable.
4. Inspect the target, its focused tests, and only the nearest callers or dependencies needed to verify that contract.
5. Identify the smallest structural problem that explains the requested refactor. Separate evidence from preference.
6. Define the scope boundary:
   - **In scope:** the target and any unavoidable focused test updates.
   - **Conditionally in scope:** one directly coupled helper, type, or caller only when the refactor cannot be correct without it.
   - **Out of scope:** adjacent cleanup, feature work, dependency upgrades, formatting churn, public API changes, and unrelated test modernization.
7. Choose the least disruptive refactoring move that addresses the problem, such as rename, extract, inline, simplify, consolidate, split responsibility, or introduce a small seam.
8. Break the work into two to five ordered steps. Keep mechanical edits separate from semantic edits, and omit speculative follow-up work.
9. For each step, name the exact code area, intended edit, preserved behavior, and verification evidence.
10. Define focused validation using existing tests first. Add or adjust a characterization test only when current behavior is important but unprotected.
11. Check the plan for scope leaks. Move useful but nonessential ideas to a short deferred list rather than adding them to the plan.
12. Stop and recommend a broader planning skill if evidence shows the change crosses several modules, alters a public contract, requires migration, or cannot be reviewed as one small change.

## Output format

Return:

```md
## Refactor target

- Target: `path/to/file` — symbol or component
- Goal: ...
- Reason: evidence-backed description of the local problem

## Behavior to preserve

- ...

## Scope boundary

- In scope: ...
- Out of scope: ...
- Assumptions: ...

## Minimal plan

1. **Edit:** ...
   - Location: ...
   - Preserve: ...
   - Verify: ...

## Validation

- [ ] ...

## Deferred observations

- ...
```

Omit `Deferred observations` when there are none. If repository evidence is unavailable, label file and test references as provisional.

## Quality bar

The task is complete only when:

- Exactly one function, class, component, or module is the primary target.
- The plan addresses a specific observed problem rather than a vague desire to make code cleaner.
- Observable behavior and contracts to preserve are explicit.
- The scope boundary excludes unrelated cleanup and feature changes.
- Every step names a concrete edit location and a focused validation method.
- The plan contains no more work than is necessary to achieve the stated goal.
- Uncertainty, missing tests, and assumptions are visible.
- The plan escalates to broader planning instead of disguising a multi-module change as a small refactor.

## Edge cases

- If the target has no tests, propose the smallest characterization test that protects the behavior affected by the refactor.
- If a local rename would alter a public API, keep the public name unchanged or flag the request as broader than a small internal refactor.
- If generated, vendored, or third-party code contains the target, identify the source-of-truth file and do not plan direct edits to generated output.
- If the refactor is motivated by a suspected bug, separate bug reproduction and behavior-change decisions from the behavior-preserving refactor.
- If formatting would dominate the diff, limit formatting to touched lines or make it a separate deferred task.
- If the target mixes several responsibilities, extract only the responsibility required by the stated goal; defer the rest.

## Related skills

- `refactor-roadmap-builder`
- `repository-area-impact-planner`
- `scope-creep-guard`
