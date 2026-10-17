---
name: repository-feature-plan
description: Plans how a proposed new feature should fit into an existing repository's architecture, conventions, tests, documentation, examples, and demo surface before implementation. Use when the user asks where a feature belongs, how to integrate a feature into the current codebase, what files or modules will likely change, how to preserve project patterns, or how to plan tests/docs/demo updates for a repository-specific feature.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: developers-technical-leads-maintainers-and-coding-agents
  tags:
    - feature-planning
    - repository-analysis
    - architecture
    - conventions
    - tests
    - documentation
    - demos
  status: draft
  side_effects: none
---

# Repository Feature Plan

## Purpose

Plan how a specific new feature should fit into an existing repository before code is written, with attention to current architecture, naming and style conventions, tests, documentation, examples, demos, and safe implementation boundaries.

This skill produces a repository-specific planning artifact. It should inspect enough of the codebase to understand existing patterns, but it should not implement, patch, or refactor code unless the user separately asks for implementation after the plan is complete.

## When to use this skill

Use this skill when:

- The user proposes a feature and wants to know where it belongs in the current repository.
- The user asks for a feature plan that respects existing architecture, module boundaries, naming, style, tests, docs, examples, or demo conventions.
- A coding agent needs a repository-aware implementation brief before making changes.
- The feature may touch multiple surfaces such as data model, API, UI, tests, documentation, examples, and demo assets.
- The user asks which files or modules are likely to change, what needs to be added, or how to avoid architectural drift.
- The repository has conventions that should be discovered from existing code rather than invented from scratch.

Common trigger phrases include:

- “Plan how this feature fits into the repo.”
- “Where should this feature go?”
- “Make a repository-aware feature plan.”
- “Analyze the architecture before implementing this feature.”
- “Tell another agent what to inspect and change for this feature.”
- “Plan the tests, docs, and demo updates for this feature.”

Do not use this skill when:

- The user wants immediate implementation rather than planning.
- The user only needs a generic implementation plan without repository inspection.
- The task is primarily a product roadmap, feature prioritization, or MVP scoping exercise.
- The request is a broad repository health review rather than planning one feature.
- The repository is unavailable and the user has not provided enough architectural context to make repository-specific claims.

## Inputs to inspect

Start with the proposed feature, target users, desired behavior, acceptance criteria, constraints, and non-goals.

Then inspect the smallest useful set of repository files, such as:

- `README.md`, `docs/`, `examples/`, `demo/`, or showcase routes
- `package.json`, workspace files, build config, framework config, or project metadata
- `src/`, `app/`, `lib/`, `components/`, `pages/`, `routes/`, `server/`, or equivalent source folders
- Existing modules near the proposed feature area
- Existing tests such as `test/`, `tests/`, `__tests__/`, `spec/`, Playwright/Cypress files, or framework-specific test folders
- Existing fixtures, seed data, mocks, stories, screenshots, or demo data
- Architecture notes such as `ARCHITECTURE.md`, `CONTRIBUTING.md`, ADRs, dependency rules, or style guides
- CI workflows or validation commands when they affect the feature plan

Do not scan the whole repository by default. Use file search and targeted inspection to identify patterns, then cite the specific files or folders that shaped the plan.

## Workflow

1. Define the feature boundary: target user, behavior, success criteria, non-goals, expected surfaces, and whether this is a new capability, extension, integration, or UI/demo addition.
2. Map the current architecture:
   - Locate relevant entry points, modules, routes, services, components, data flows, configuration, and build/test boundaries.
   - Identify ownership boundaries and dependencies between layers.
   - Note existing abstractions that should be extended instead of duplicated.
3. Discover repository conventions:
   - Naming, folder organization, import style, state management, error handling, logging, validation, styling, accessibility, and testing patterns.
   - Documentation, example, and demo patterns that should be mirrored.
   - Commands or CI checks that define the validation path.
4. Decide the integration approach:
   - Where the feature should live.
   - Which existing modules should be extended.
   - Which new files, types, routes, components, fixtures, or docs are justified.
   - Which areas should be avoided to prevent coupling or architectural drift.
5. Plan data and contract changes if relevant: schemas, types, API contracts, migrations, fixtures, mocks, compatibility requirements, persistence, privacy, and fallback behavior.
6. Plan user-facing and demo behavior: primary flow, empty/loading/error states, accessibility expectations, responsive behavior, sample data, screenshots, and demo routes or examples.
7. Plan tests alongside implementation:
   - Unit tests for isolated logic.
   - Integration tests for module boundaries or API/data flow.
   - End-to-end or component tests for user-visible behavior.
   - Regression tests for existing behavior likely to be affected.
   - Manual QA or demo verification when automation is not enough.
8. Plan documentation updates: README, docs pages, examples, changelog notes, API references, usage snippets, architecture notes, or demo instructions.
9. Sequence the work in safe increments from discovery and contracts through implementation, tests, docs, demos, and cleanup.
10. Identify risks, unresolved decisions, and validation checkpoints before handing the plan to an implementer.

## Output format

Return the feature plan using this structure:

```md
## Summary

Briefly state how the feature should fit into the repository and the main architectural risk.

## Repository signals inspected

- Architecture and source patterns:
- Conventions:
- Tests and validation:
- Docs/examples/demo surface:

## Feature fit

- Recommended location:
- Existing abstractions to extend:
- New files or modules likely needed:
- Areas to avoid:
- Assumptions and open questions:

## Ordered implementation plan

| Step | Goal | Likely files/modules | Work to do | Validation |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

## Tests and validation plan

- Unit:
- Integration:
- End-to-end/component/manual:
- Regression risks:
- Commands to run or add:

## Documentation, examples, and demo plan

- README/docs:
- Examples:
- Demo/story/sample data:
- Screenshots or walkthrough notes:

## Risks and decisions

| Risk or decision | Why it matters | Recommendation | Validation point |
|---|---|---|---|

## Handoff checklist

- [ ] Architecture fit is confirmed.
- [ ] Conventions to follow are named.
- [ ] Tests are planned next to the relevant work.
- [ ] Docs/examples/demo updates are included.
- [ ] Open questions are resolved or explicitly marked.
```

If the user asks for a shorter answer, keep the feature fit, ordered implementation plan, tests, docs/demo plan, and open questions.

## Quality bar

The task is complete only when:

- The plan is specific to the actual repository rather than a generic feature checklist.
- Architectural fit is explained with references to existing modules, boundaries, or conventions.
- The plan identifies both code changes and non-code work such as tests, docs, examples, and demos.
- New files are justified by repository patterns, not invented unnecessarily.
- Tests and validation are tied to individual feature risks.
- Assumptions and open questions are visible.
- The plan avoids code patches, diffs, or implementation snippets unless the user explicitly requests them.
- The handoff is concrete enough for a coding agent or maintainer to implement safely.

## Edge cases

- If the repository has multiple apps, packages, or workspaces, first identify the target package and shared boundaries before planning file changes.
- If conventions conflict across the repository, prefer the convention nearest to the feature area and document the conflict.
- If the feature crosses public APIs or persisted data, include compatibility, migration, versioning, and rollback considerations.
- If tests are missing, propose the smallest test scaffold that matches the repository's tooling instead of prescribing a new test stack by default.
- If docs or demos do not exist, recommend whether they are necessary for this feature and where a minimal addition should live.
- If the feature request is vague, create a provisional plan around the smallest coherent behavior and list decisions needed before implementation.
- If current external API behavior or package capabilities affect the feature, mark the relevant claims as needing verification before implementation.

## Related skills

- `implementation-plan-writer`
- `architecture-decision-planner`
- `implementation-order-planner`
- `task-context-packager`
- `project-plan-reconciler`
