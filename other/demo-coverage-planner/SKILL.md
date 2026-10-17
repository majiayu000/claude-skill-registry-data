---
name: demo-coverage-planner
description: Plans a coordinated demo set that collectively covers core usage, configuration variants, error and recovery paths, accessibility expectations, and advanced behavior. Use when the user asks to design examples, sample apps, storybook stories, documentation demos, playground scenarios, or portfolio demo coverage for a feature, component, plugin, library, or product workflow.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: frontend-library-maintainers
  tags:
    - demos
    - examples
    - coverage-planning
    - configuration
    - error-states
    - accessibility
    - advanced-usage
  status: draft
  side_effects: none
---

# Demo Coverage Planner

## Purpose

Plan a compact, purposeful set of demos that proves a feature, component, plugin, library, or workflow works across the scenarios users need to understand: core usage, configuration, errors, accessibility, and advanced behavior.

## When to use this skill

Use this skill when:

- The user asks what demos, examples, stories, sample pages, or playground scenarios should exist.
- A project needs demo coverage before documentation, launch, portfolio review, or release.
- Existing demos show only the happy path and need broader coverage.
- The user wants examples that reveal configuration options, failure states, accessibility behavior, or advanced usage.

Do not use this skill when:

- The user only wants implementation code for one already-defined demo.
- The task is primarily an accessibility audit rather than demo planning.
- The task is primarily visual polish for an existing demo surface.
- The project has no demoable user-facing behavior or public API.

## Inputs to inspect

Inspect relevant inputs such as:

- `README.md`, `docs/`, examples, demo pages, Storybook stories, playground routes, or screenshots.
- Public API documentation, component props, plugin options, CLI flags, configuration files, or schema definitions.
- Source files for core user flows, state machines, validation, error handling, and accessibility hooks.
- Tests that reveal expected behavior, edge cases, or supported variants.
- Issue notes, launch goals, portfolio goals, or release criteria that define the intended audience.

## Workflow

1. Identify the demo target: the feature, component, library, plugin, workflow, or product area the demos must explain.
2. Identify the primary audience and decision moment: first-time evaluator, integrator, maintainer, recruiter, stakeholder, or end user.
3. Inventory existing demos and mark which coverage lane each one satisfies:
   - Core usage: the smallest successful path.
   - Configuration: meaningful options, variants, themes, modes, integrations, or environment differences.
   - Errors and recovery: validation failures, empty states, loading failures, permission problems, network failures, retries, and user mistakes.
   - Accessibility: semantic structure, keyboard flow, focus behavior, screen-reader naming, reduced motion, contrast-sensitive states, and zoom or responsive behavior.
   - Advanced behavior: composition, extension points, performance-sensitive usage, complex data, lifecycle interactions, or integration with other systems.
4. Find gaps, overlaps, and sequencing problems. Prefer fewer demos that each teach a distinct concept over many repetitive demos.
5. Design the recommended demo set. For each demo, specify the scenario, user goal, setup data, interactions to show, expected outcome, and coverage lanes.
6. Order the demos from simple to complex so users can learn progressively.
7. Define evidence requirements for each demo, such as screenshots, live page routes, Storybook story names, test fixtures, notes, or validation steps.
8. Flag implementation risks, missing fixtures, missing API clarity, or design decisions that block good demo coverage.
9. Avoid adding demos that require external services, secrets, destructive actions, or production data unless the user explicitly approves a safe mock or sandbox plan.

## Output format

Return the plan using this structure:

```md
## Summary

Briefly state the recommended demo strategy and the main coverage gaps.

## Demo coverage matrix

| Demo | Core usage | Configuration | Errors/recovery | Accessibility | Advanced behavior | Priority |
|---|---|---|---|---|---|---|

## Recommended demo set

### 1. Demo name
- Goal:
- Audience:
- Scenario:
- Setup data or fixtures:
- User interactions:
- Expected outcome:
- Coverage lanes:
- Evidence to capture:
- Implementation notes:

## Gaps and risks

- ...

## Suggested sequence

1. ...
2. ...
3. ...

## Validation checklist

- [ ] The set includes at least one clear core usage demo.
- [ ] Configuration variants are represented without duplicating the core demo unnecessarily.
- [ ] Error and recovery behavior is visible and safe to trigger.
- [ ] Accessibility behavior is explicit, not assumed.
- [ ] Advanced behavior is included only after foundational demos are covered.
- [ ] Each demo has a clear audience, scenario, and expected outcome.
```

If the repository already has demos, include an `Existing demo assessment` section before the matrix.

## Quality bar

The task is complete only when:

- The recommended set collectively covers core usage, configuration, errors and recovery, accessibility, and advanced behavior, or explicitly explains why a lane does not apply.
- Each demo has a distinct teaching purpose and avoids redundant happy-path examples.
- The plan identifies required fixtures, mock data, routes, stories, screenshots, or validation evidence.
- Accessibility coverage names concrete behaviors to demonstrate rather than generic compliance claims.
- Error demos use safe, deterministic failure triggers and avoid real destructive or production-side effects.
- The output gives enough detail for a maintainer to implement or prioritize the demos.

## Edge cases

- If the project is early and APIs are unstable, plan thin placeholder demos and mark decisions that must stabilize first.
- If only one demo is feasible, make it multi-section and explicitly call out which coverage lanes remain deferred.
- If advanced behavior would confuse first-time users, put it after foundational demos or in a separate advanced examples area.
- If accessibility behavior cannot be demonstrated visually, specify keyboard steps, screen-reader labels, focus expectations, or reduced-motion checks as evidence.
- If a demo would need third-party credentials, recommend a mock, fixture, recorded response, or sandbox mode.

## Related skills

- `accessibility-validation-planner`
- `interface-state-coverage-review`
- `portfolio-project-planner`
- `user-flow-planner`
