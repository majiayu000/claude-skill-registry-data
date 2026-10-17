---
name: repository-area-impact-planner
description: Identifies which repository files, modules, APIs, tests, examples, demos, documentation, configuration, and dependency areas are likely to be affected by a proposed change before implementation. Use when the user asks for an impact map, blast-radius analysis, affected areas, likely files to inspect or edit, test/doc update scope, or a planning handoff that predicts downstream repository impacts.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: developers-technical-leads-maintainers-and-coding-agents
  tags:
    - impact-analysis
    - repository-analysis
    - change-planning
    - blast-radius
    - tests
    - documentation
    - api-contracts
  status: draft
  side_effects: none
---

# Repository Area Impact Planner

## Purpose

Identify the likely repository blast radius of a proposed change before implementation. Produce an evidence-backed impact map covering files, modules, APIs, tests, examples, demos, documentation, configuration, and follow-on validation needs.

This skill plans affected areas only. It should not implement changes, refactor code, or modify files unless the user separately asks for implementation after the impact plan is complete.

## When to use this skill

Use this skill when:

- The user describes a change and asks which files, modules, packages, APIs, tests, examples, or docs are likely to be affected.
- A maintainer wants blast-radius analysis before approving or sequencing work.
- A coding agent needs a focused impact map before editing a repository.
- The change may cross boundaries such as source code, public APIs, schemas, routes, configuration, examples, tests, generated artifacts, docs, or demos.
- The user asks for likely affected areas, inspection targets, downstream dependencies, regression risks, or validation scope.

Common trigger phrases include:

- “What areas will this change affect?”
- “Map the blast radius before implementation.”
- “Which files should we inspect or update?”
- “What tests and docs need to change?”
- “Identify likely affected modules and APIs.”
- “Create an impact plan for this repository change.”

Do not use this skill when:

- The user wants a generic project plan without repository inspection.
- The user asks to implement the change immediately and does not need a planning artifact.
- The request is primarily feature prioritization, MVP scoping, or roadmap sequencing.
- The repository or enough source context is unavailable; in that case, ask for the repository or provide only a clearly labeled provisional impact hypothesis.
- A more specific skill covers the same planning need, such as a full repository feature plan or refactor roadmap.

## Inputs to inspect

Start with the proposed change, desired behavior, non-goals, target users, compatibility expectations, and any named files, symbols, packages, routes, commands, or issue references.

Then inspect the smallest useful set of repository evidence, such as:

- Repository instructions: `AGENTS.md`, `CONTRIBUTING.md`, architecture docs, ADRs, style guides, or ownership notes
- Project metadata and boundaries: `package.json`, workspace files, build config, framework config, dependency manifests, or monorepo package maps
- Source entry points: `src/`, `app/`, `lib/`, `packages/`, `server/`, `client/`, `components/`, `routes/`, `pages/`, or equivalent folders
- Public contracts: exported modules, CLI commands, API routes, schemas, types, migrations, configuration keys, environment variables, events, hooks, or plugin interfaces
- Direct dependency ring: imports, callers, implementers, consumers, fixtures, generated source-of-truth files, and shared utilities around the target area
- Tests: `test/`, `tests/`, `__tests__/`, `spec/`, unit/integration/e2e folders, test fixtures, mocks, snapshots, stories, or visual regression assets
- Examples and demos: `examples/`, `demo/`, `playground/`, `stories/`, sample apps, seed data, screenshots, or walkthroughs
- Documentation: `README.md`, `docs/`, API references, changelog notes, migration guides, tutorials, troubleshooting pages, and release notes
- Validation infrastructure: CI workflows, lint/type/test commands, build scripts, codegen scripts, and release checks

Do not scan the whole repository by default. Use targeted search for named concepts, imports, exports, routes, config keys, and test references, then expand only when evidence shows a dependency or consumer relationship.

## Workflow

1. Define the proposed change boundary:
   - State the intended behavior or structural change.
   - Separate confirmed scope, non-goals, assumptions, and unresolved questions.
   - Classify the change type: feature, bug fix, API change, schema/data change, UI change, refactor, dependency/config change, docs-only change, or migration.
2. Locate the primary change surface:
   - Find likely source files, modules, packages, routes, commands, components, services, schemas, or config entries.
   - Identify the source of truth when generated files, build outputs, snapshots, or docs mirror another file.
   - Prefer paths and symbols backed by repository evidence over guesses.
3. Trace affected contracts and dependency rings:
   - Inspect direct imports, exports, callers, consumers, types, interfaces, fixtures, route definitions, schemas, CLI flags, events, and config keys.
   - Distinguish internal implementation impact from public or cross-package contract impact.
   - Mark areas as confirmed, likely, possible, or unlikely based on evidence strength.
4. Map tests and validation impact:
   - Identify existing tests that should change or protect the behavior.
   - Identify missing test coverage that the change should add.
   - Include fixtures, mocks, snapshots, stories, visual tests, accessibility checks, build/type/lint commands, and manual QA when relevant.
5. Map examples, demos, and documentation impact:
   - Identify user-facing docs, API references, snippets, example apps, demo data, screenshots, tutorials, changelogs, or migration notes that may need updates.
   - Separate required updates from optional discoverability or polish improvements.
6. Identify configuration, dependency, and operational impact:
   - Check build, runtime, environment, package, CI, deployment, telemetry, security, privacy, performance, and compatibility implications when applicable.
   - Note any generated artifacts or lockfiles that should not be edited directly unless they are the repository's normal source of truth.
7. Prioritize and sequence inspection or edits:
   - Put high-confidence and high-risk areas first.
   - Group related files by module, package, layer, or user-facing surface.
   - Identify parallel-safe areas and areas that should wait for contract decisions.
8. Record risks and decisions:
   - Capture backward compatibility, migration, data integrity, accessibility, performance, security, and API stability risks.
   - Turn unknowns into explicit questions or discovery tasks.
9. Produce the impact plan:
   - Include evidence for each affected area.
   - Label confidence and recommended action.
   - Avoid presenting speculation as fact.

## Output format

Return the impact plan using this structure:

```md
## Summary

Briefly state the proposed change, overall blast radius, and highest-risk affected area.

## Scope and assumptions

- Confirmed scope:
- Non-goals:
- Assumptions:
- Open questions:

## Repository signals inspected

- Source and architecture:
- Public contracts and APIs:
- Tests and validation:
- Examples, demos, and docs:
- Configuration and operations:

## Impact map

| Area | Confidence | Evidence | Likely action | Risk if missed |
|---|---|---|---|---|
| Source/modules | Confirmed/Likely/Possible/Unlikely | ... | Inspect/Edit/Add/No change | ... |
| Public APIs/contracts | ... | ... | ... | ... |
| Tests/fixtures | ... | ... | ... | ... |
| Examples/demos | ... | ... | ... | ... |
| Documentation | ... | ... | ... | ... |
| Config/dependencies/CI | ... | ... | ... | ... |

## Likely file and module checklist

| Priority | Path or symbol | Why it matters | Action | Depends on |
|---|---|---|---|---|
| P0 | ... | ... | ... | ... |

## Tests and validation plan

- Existing tests to update or run:
- New tests or fixtures to add:
- Regression risks:
- Manual checks:
- Commands to run:

## Docs, examples, and release notes

- Required updates:
- Optional updates:
- User-facing migration or compatibility notes:

## Risks, decisions, and follow-up discovery

| Item | Type | Owner or next step | Blocks implementation? |
|---|---|---|---|
| ... | Risk/Decision/Discovery | ... | Yes/No |
```

If the user asks for a brief answer, keep the summary, impact map, likely file checklist, tests/docs impact, and open questions.

## Quality bar

The task is complete only when:

- The impact map is specific to the actual repository and proposed change.
- Each affected area includes evidence, confidence, and a recommended action.
- Source, public contracts, tests, examples, documentation, and configuration are each considered, even if marked not affected.
- Confirmed impacts are separated from likely or possible impacts.
- The plan identifies both direct edit targets and downstream consumers or validation surfaces.
- Generated files and source-of-truth files are distinguished.
- Open questions and blockers are explicit.
- The result is actionable for a maintainer or coding agent without requiring a repository-wide reread.

## Edge cases

- If the proposed change is vague, create a provisional impact map around the smallest plausible interpretation and list the decisions needed to refine it.
- If the repository is a monorepo, identify the target package, shared packages, cross-package contracts, and workspace-level checks before listing files.
- If a public API, schema, or persisted data format may change, include compatibility, migration, versioning, and rollback considerations.
- If generated files appear affected, locate the generator or source definition before recommending edits.
- If tests are sparse or absent, recommend the narrowest useful coverage that matches existing tooling rather than introducing a new test stack by default.
- If docs, examples, or demos do not exist, state whether the change still requires user-facing notes and where a minimal note should live.
- If current external behavior affects the plan, mark claims that need web, registry, API, or product documentation verification before implementation.

## Related skills

- `repository-feature-plan`
- `implementation-plan-writer`
- `implementation-order-planner`
- `refactor-roadmap-builder`
- `task-context-packager`
- `task-dependency-mapper`
