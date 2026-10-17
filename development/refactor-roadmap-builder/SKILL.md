---
name: refactor-roadmap-builder
description: Breaks a large software refactor into behavior-preserving stages with tests, compatibility checkpoints, rollback boundaries, sequencing rationale, and safe migration slices. Use when the user asks to plan a major refactor, decompose a risky rewrite, modernize internals without changing behavior, preserve compatibility during migration, identify refactor phases, define test gates, or create a rollback-aware refactoring roadmap.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: software-maintainers-technical-leads-and-coding-agents
  tags:
    - refactoring
    - roadmap
    - behavior-preservation
    - testing
    - compatibility
    - rollback
    - migration
  status: draft
  side_effects: none
---

# Refactor Roadmap Builder

## Purpose

Turn a broad, risky, or ambiguous refactor goal into a staged roadmap that preserves existing behavior while creating room for safe internal change.

This skill emphasizes tests, characterization, compatibility contracts, reversible slices, checkpoint reviews, and rollback boundaries so implementers can modernize code without combining behavior change, architecture change, and cleanup in one unsafe pass.

## When to use this skill

Use this skill when:

- The user asks to plan a large refactor, rewrite, migration, modernization, or codebase restructuring effort.
- Existing behavior must be preserved while internals, boundaries, dependencies, naming, modules, types, or architecture change.
- The refactor affects public APIs, persisted data, integrations, build systems, shared components, or multiple teams or agents.
- The user needs stages, compatibility checkpoints, test gates, rollback boundaries, or a safe migration sequence.
- A proposed refactor is too large to review or revert as one change.
- The work needs characterization tests before implementation details are changed.
- The user wants to separate mechanical changes from semantic or behavior-changing changes.

Common trigger phrases include:

- “Break this refactor into stages.”
- “Create a refactor roadmap.”
- “How do we preserve behavior during this rewrite?”
- “Plan a safe migration path.”
- “Add test gates and rollback points to this refactor.”
- “De-risk this large cleanup.”
- “Sequence this modernization without breaking compatibility.”

Do not use this skill when:

- The user wants the refactor implemented immediately without planning.
- The task is a small local cleanup that can be safely reviewed in one change.
- The primary goal is adding new product behavior rather than preserving existing behavior through internal change.
- The user needs a general project roadmap with feature milestones rather than a refactor-specific migration plan.
- The request is only code review of an already completed refactor.

## Inputs to inspect

Start with the smallest evidence set that explains the refactor target and risk:

- User-provided refactor goal, constraints, non-goals, and success criteria.
- Existing plan, issue, roadmap, design document, ADR, or migration notes.
- Public API, module boundary, schema, storage format, CLI, UI flow, integration contract, or generated output affected by the refactor.
- Current test suite, coverage reports, golden files, snapshots, fixtures, end-to-end tests, smoke tests, and known manual QA paths.
- Dependency graph, import boundaries, package structure, ownership boundaries, and release process.
- Compatibility requirements: supported versions, migration windows, deprecation policy, feature flags, adapters, dual-write or dual-read periods, and consumer expectations.
- Rollback or recovery constraints: database migrations, config changes, deploy order, generated artifacts, package publishing, and external integrations.

Avoid reading the entire repository by default. Inspect implementation files only when they clarify behavior contracts, coupling, available tests, or migration constraints.

## Workflow

1. Define the refactor objective: target area, desired end state, behavior that must remain unchanged, explicit non-goals, and the audience for the roadmap.
2. Identify behavior contracts that must be preserved, including public APIs, user-visible flows, data shapes, CLI flags, emitted events, file formats, performance thresholds, accessibility expectations, and integration behavior.
3. Map risk and coupling: list callers, downstream consumers, data dependencies, shared abstractions, build or deploy dependencies, and places where the refactor could escape its intended boundary.
4. Establish baseline evidence before changing structure:
   - characterization tests for current behavior
   - golden outputs or snapshots where appropriate
   - smoke tests for critical paths
   - contract tests for public or integration boundaries
   - manual QA paths only when automation is not yet feasible
5. Separate refactor work into safe slice types:
   - **Prepare**: add tests, observability, fixtures, feature flags, adapters, or seams.
   - **Move mechanically**: rename, extract, relocate, format, or codemod without semantic changes.
   - **Introduce parallel path**: add new implementation behind an adapter, facade, flag, compatibility shim, or dual-read path.
   - **Switch consumers incrementally**: migrate one caller, package, route, or workflow at a time.
   - **Remove legacy path**: delete old code only after evidence shows consumers no longer depend on it.
6. Sequence stages so every behavior-preserving or compatibility-preserving foundation exists before the risky internal change depends on it.
7. For each stage, define:
   - goal and scope
   - behavior-preservation rule
   - files or components likely affected
   - required tests and evidence
   - compatibility checkpoint
   - rollback boundary
   - entry and exit criteria
8. Mark rollback boundaries at points where the system can return to the previous behavior without data loss, contract breakage, or partial migration ambiguity.
9. Identify compatibility strategies: facade, adapter, shim, feature flag, versioned API, deprecation window, dual-write, dual-read, migration script, or explicit consumer opt-in.
10. Prevent mixed-purpose stages. Do not combine behavior changes, dependency upgrades, formatting churn, and structural refactors unless the coupling is unavoidable and documented.
11. Add checkpoints after high-risk boundaries: new abstraction seam, compatibility layer, first migrated consumer, data migration rehearsal, deploy-order proof, and legacy removal.
12. Capture assumptions, unresolved decisions, and out-of-scope improvements so implementers do not quietly expand the refactor.
13. Finish with the safest immediate next actions, usually evidence-gathering and characterization before structural edits.

## Output format

Return the roadmap using this structure:

```md
## Summary

Brief statement of the refactor objective, risk profile, and recommended sequencing.

## Behavior contracts to preserve

| Contract | Evidence needed | Current coverage | Gap |
|---|---|---|---|
| ... | ... | present / missing / unknown | ... |

## Refactor roadmap

| Stage | Goal | Scope | Behavior-preservation rule | Required evidence | Compatibility checkpoint | Rollback boundary |
|---|---|---|---|---|---|---|
| Stage 0: Baseline | ... | ... | ... | ... | ... | ... |

## Compatibility and migration plan

- ...

## Rollback plan

| Boundary | Safe rollback action | Data or contract concern | Owner/check |
|---|---|---|---|
| ... | ... | ... | ... |

## Risks and mitigations

| Risk | Why it matters | Mitigation | Checkpoint |
|---|---|---|---|
| ... | ... | ... | ... |

## Assumptions and open questions

- ...

## Immediate next actions

1. ...
2. ...
3. ...
```

If the user requests tickets or issues, keep the same roadmap logic and express each stage as an issue-ready work item with acceptance criteria and validation steps.

## Quality bar

The task is complete only when:

- The roadmap preserves current behavior unless the user explicitly identifies intended behavior changes.
- Baseline evidence and characterization needs are defined before risky structural changes.
- Each stage is reviewable, testable, and small enough to revert or pause.
- Mechanical, compatibility, migration, behavior-changing, and cleanup work are separated or explicitly justified.
- Compatibility checkpoints name the contract, evidence, and downstream consumers protected.
- Rollback boundaries explain what can be reverted, what cannot, and what data or deploy-order constraints apply.
- Legacy removal is gated by proof that consumers no longer depend on the old path.
- Risks, assumptions, non-goals, and open decisions are visible.
- Immediate next actions do not start with broad rewrites before test coverage and contracts are understood.

## Edge cases

- If no tests exist, make Stage 0 a characterization and smoke-test stage rather than starting the refactor.
- If the refactor intentionally changes behavior, split behavior changes into separate stages with explicit acceptance criteria and migration notes.
- If data migrations are involved, require rehearsal, backup/restore proof, forward/backward compatibility, and a clear point of no return.
- If public APIs are affected, include deprecation, versioning, adapter, or consumer communication steps before removal.
- If multiple agents or teams will work in parallel, define ownership boundaries and integration checkpoints before assigning slices.
- If a complete rollback is impossible, state the irreversible boundary and require approval or a safer phased alternative.
- If the repository is too large to inspect fully, produce a provisional roadmap and identify the specific files, owners, or commands needed to validate assumptions.

## Related skills

- `implementation-checkpoint-planner`
- `implementation-order-planner`
- `implementation-plan-writer`
- `project-roadmap-builder`
- `task-dependency-mapper`
