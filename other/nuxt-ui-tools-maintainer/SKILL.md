---
name: nuxt-ui-tools-maintainer
description: Use this skill for internal maintenance and feature work in the nuxt-ui-tools repository. It explains the repository operating model, exact placement rules, how runtime domains relate, how features should be structured and extended, how consumer skills must be maintained, and what to keep in sync when changing the library.
---

# nuxt-ui-tools Maintainer

Use this skill for internal repository work.

This is the main internal maintainer skill.
It should be the first deeper skill loaded after `AGENTS.md` when the task is about implementing, refactoring, organizing, or extending code in this repository.

## Read First

- `AGENTS.md`
- `.agents/skills/nuxt-ui-tools-maintainer/references/core-approach.md`
- `.agents/skills/nuxt-ui-tools-maintainer/references/placement-rules.md`
- `.agents/skills/nuxt-ui-tools-maintainer/references/change-workflow.md`
- `.agents/skills/nuxt-ui-tools-maintainer/references/consumer-skills.md`

Then load the domain reference that matches the task:

- table runtime:
  `.agents/skills/nuxt-ui-tools-maintainer/references/table-runtime.md`
- query-state runtime:
  `.agents/skills/nuxt-ui-tools-maintainer/references/query-state.md`
- shared runtime:
  `.agents/skills/nuxt-ui-tools-maintainer/references/shared-runtime.md`
- form runtime:
  `.agents/skills/nuxt-ui-tools-maintainer/references/form-runtime.md`
- dashboard runtime:
  `.agents/skills/nuxt-ui-tools-maintainer/references/dashboard-runtime.md`
- file preview runtime:
  `.agents/skills/nuxt-ui-tools-maintainer/references/file-preview-runtime.md`
- spreadsheet import runtime:
  `.agents/skills/nuxt-ui-tools-maintainer/references/spreadsheet-runtime.md`

For technical foundation work, also load the matching skill:

- TypeScript policy and schema typing:
  `.agents/skills/nuxt-ui-tools-typescript/SKILL.md`
- lean reactivity and query-state integration:
  `.agents/skills/nuxt-ui-tools-reactivity/SKILL.md`
- config/registry-driven feature architecture:
  `.agents/skills/nuxt-ui-tools-config-driven/SKILL.md`

## What This Skill Exists To Solve

It should make two things easy:

1. maintenance and development by both AI agents and humans
2. adoption of the library by package consumers

That means internal code decisions should optimize for:

- clear placement
- low cognitive load
- modular structure
- predictable extension patterns
- stable and discoverable consumer surfaces

## Core Internal Rule

When making changes, always think in both directions:

- inward:
  does this make the codebase easier to understand, evolve, and validate?
- outward:
  does this make the package easier to use, document, and teach?

If a change improves implementation convenience but makes consumer usage or future maintenance worse, it is probably the wrong move.

## What Agents Must Be Able To Answer

After reading this skill, an agent should be able to answer all of these quickly:

- which runtime domain owns the change
- which layer inside that domain owns the change
- whether the feature should be config-driven, registry-driven, or a simpler direct abstraction
- whether complexity should be absorbed by the package instead of leaking to consumers
- which tests, playground routes, consumer skills, and internal references must be updated

If the current guidance does not make those answers obvious, improve the guidance as part of the task.

## Internal Routing

If the task is about:

- overall repository structure, placement, or feature organization:
  use `core-approach.md` and `placement-rules.md`
- extension workflow or how to land a feature cleanly:
  use `change-workflow.md`
- table internals:
  use `table-runtime.md`
- query-state internals:
  use `query-state.md`
- TypeScript and type-system shaping:
  use `.agents/skills/nuxt-ui-tools-typescript/SKILL.md`
- reactive state design:
  use `.agents/skills/nuxt-ui-tools-reactivity/SKILL.md`
- config-driven or registry-driven architecture:
  use `.agents/skills/nuxt-ui-tools-config-driven/SKILL.md`
- consumer-facing package skill maintenance:
  use `consumer-skills.md`

## Skill Split Reminder

Internal maintainer guidance belongs in:

- `.agents/skills/`

Consumer package guidance belongs in:

- `skills/consumer/`

Do not mix them.
