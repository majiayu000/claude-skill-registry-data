---
name: example-progression-planner
description: Orders examples, demos, tutorials, or sample integrations from minimal setup through realistic use and advanced integration. Use when the user asks to sequence examples for documentation, onboarding, sample apps, SDKs, libraries, components, APIs, plugins, or learning paths so users progress from first success to production-like patterns.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: documentation-authors-and-library-maintainers
  tags:
    - examples
    - documentation
    - onboarding
    - tutorials
    - integration
    - learning-path
    - sequencing
  status: draft
  side_effects: none
---

# Example Progression Planner

## Purpose

Plan a clear example sequence that takes users from the smallest working setup to realistic usage and advanced integration without overwhelming them or hiding important prerequisites.

## When to use this skill

Use this skill when:

- The user asks how to order examples, demos, tutorials, recipes, sample apps, SDK snippets, component stories, API guides, or plugin integrations.
- Existing examples are useful individually but feel scattered, too advanced too early, or missing a learning path.
- A project needs beginner, intermediate, and advanced examples that build on each other intentionally.
- Documentation should guide users from first success to realistic production-like patterns.
- The user wants to decide which examples belong in quickstart, basic usage, recipes, advanced integration, or reference sections.

Do not use this skill when:

- The user only needs one standalone example and does not need a sequence.
- The task is primarily to audit whether demos cover all scenarios; use `demo-coverage-planner`.
- The task is a full documentation information-architecture audit; use a docs-focused review skill.
- The user wants implementation code for examples rather than a progression plan.

## Inputs to inspect

Inspect relevant inputs such as:

- Existing examples, demo pages, sample apps, Storybook stories, tutorials, recipes, playgrounds, or snippets.
- `README.md`, `docs/`, quickstarts, API reference pages, integration guides, and troubleshooting docs.
- Public APIs, component props, CLI flags, configuration options, extension points, schemas, or SDK methods.
- Setup requirements, authentication requirements, environment variables, fixtures, mock data, and external service dependencies.
- User personas, onboarding goals, support questions, issue patterns, release goals, or portfolio goals.
- Tests or fixtures that reveal realistic usage, edge cases, integration boundaries, and advanced behavior.

## Workflow

1. Define the learning outcome: identify what users should be able to do after completing the example sequence.
2. Identify the target audiences and their starting points, such as first-time evaluator, new integrator, advanced maintainer, product developer, or migration user.
3. Inventory existing and proposed examples. For each example, record its goal, prerequisites, concepts introduced, setup burden, realism, integration depth, and likely audience.
4. Classify examples into progression levels:
   - Minimal setup: smallest successful path with the least configuration and fewest concepts.
   - Basic usage: common happy-path behavior with one or two practical options.
   - Realistic workflow: representative data, state, error handling, configuration, accessibility, performance, or deployment considerations.
   - Integration pattern: use with frameworks, services, storage, authentication, build tools, design systems, plugins, or existing application structure.
   - Advanced extension: customization, composition, lifecycle hooks, scaling, migration, performance tuning, or uncommon expert workflows.
5. Remove false prerequisites. Do not force users through broad theory, exhaustive configuration, or advanced architecture before their first working result.
6. Add missing bridge examples where the jump between levels introduces too many new concepts at once.
7. Order the sequence so each example introduces a small number of new concepts while reusing knowledge from earlier examples.
8. Mark examples that should be optional branches rather than part of the main path, especially framework-specific, platform-specific, or niche advanced integrations.
9. Define entry criteria, exit criteria, and validation evidence for each example so users know when they are ready to continue.
10. Name any examples that should be split, merged, moved, rewritten, or deferred because they interrupt the progression.
11. Keep side effects safe: recommend mocks, fixtures, sandboxes, or read-only examples before examples that require credentials, production data, payments, destructive actions, or deployment.

## Progression heuristics

Use these ordering heuristics:

- Put first success before realism, and put realism before advanced extension.
- Teach one primary concept per example when possible.
- Prefer copy-pasteable setup early; explain abstractions after users see working behavior.
- Introduce configuration only when it solves a visible need from an earlier example.
- Move framework-specific examples into branches unless one framework is the documented default.
- Place troubleshooting, failures, and recovery near the first realistic workflow, not only at the end.
- Make advanced examples depend on explicit prior concepts rather than hidden knowledge.
- Avoid ordering by internal implementation structure when user learning order differs.

## Output format

Return the plan using this structure:

```md
## Summary

Briefly state the recommended progression and the main ordering issue.

## Audience and outcome

- Primary audience:
- Starting assumptions:
- End state:

## Example inventory

| Example | Current location | Level | Prerequisites | Concepts introduced | Keep / move / split / add |
|---|---|---|---|---|---|

## Recommended progression

### 1. Example name
- Level:
- User goal:
- Prerequisites:
- New concepts:
- Setup or fixture needs:
- Validation evidence:
- Why this comes here:

## Optional branches

- ...

## Gaps and rewrites

- ...

## Validation checklist

- [ ] The first example reaches a working result with minimal setup.
- [ ] Each later example introduces a limited, named set of new concepts.
- [ ] Realistic workflows appear before advanced integrations.
- [ ] Optional framework- or platform-specific branches are separated from the main path.
- [ ] Risky side effects use mocks, fixtures, sandboxes, or explicit warnings.
- [ ] The sequence names prerequisites and exit criteria for every example.
```

If no examples exist yet, replace `Example inventory` with `Proposed example set` and mark each item as `add`.

## Quality bar

The task is complete only when:

- The recommended sequence has a clear first-success example, at least one realistic workflow when applicable, and advanced integration only after prerequisites are established.
- Each example has a distinct learning purpose and a justified position in the order.
- Concept jumps are identified and bridged or explicitly deferred.
- Optional branches are separated from the main path so they do not block general onboarding.
- Prerequisites, setup burden, validation evidence, and side-effect risks are visible.
- The plan is specific enough for a maintainer to reorganize documentation or create the missing examples.

## Edge cases

- If the product requires unavoidable setup, make the first example a verified setup smoke test and state why it cannot be simpler.
- If advanced users are the only audience, still start with the smallest integration that proves the core contract before moving to expert patterns.
- If examples target multiple frameworks, create one shared conceptual path and branch framework-specific implementations after the common model is clear.
- If realistic examples require private services or credentials, recommend mocked fixtures, local emulators, sandboxes, or recorded responses.
- If existing examples are high quality but unordered, preserve content and recommend navigation, labels, prerequisites, and cross-links instead of rewriting everything.

## Related skills

- `demo-coverage-planner`
- `docs-discoverability-audit`
- `implementation-order-planner`
- `progressive-enhancement-planner`
