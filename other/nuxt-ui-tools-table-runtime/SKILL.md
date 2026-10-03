---
name: nuxt-ui-tools-table-runtime
description: Use this skill when implementing, refactoring, or extending the internal table runtime inside this repository. Covers the current architecture layers, state model, composable flow, where different responsibilities live, how to add features cleanly, and what kinds of refactors are encouraged.
---

# nuxt-ui-tools Table Runtime

Use this skill for internal repository work on:

- table runtime architecture
- table state management
- composables
- runtime components
- schema/builder internals
- adding new table capabilities
- refactoring table internals

## Read First

- `AGENTS.md`
- `.agents/skills/nuxt-ui-tools-maintainer/SKILL.md`
- `.agents/skills/nuxt-ui-tools-table-runtime/references/architecture.md`

## Current Mental Model

The current table runtime is a schema-driven system with these major layers:

1. public schema and public entrypoints
2. schema/building and normalization helpers
3. reactive orchestration in composables
4. pure or mostly pure utilities
5. rendering components
6. playground integration surface

The important split is:

- public shape and schema definition
- runtime orchestration
- pure transformations
- rendering

Do not collapse those layers together.

## Current File Routing

Start from these depending on the task:

- public package surface:
  `src/runtime/table/index.ts`
- schema definition entry:
  `src/runtime/table/schema/index.ts`
- internal orchestration root:
  `src/runtime/table/composables/use-table-internals.ts`
- public table API shape:
  `src/runtime/table/composables/use-table.ts`
  `src/runtime/table/composables/use-table-api.ts`
- query-state bridge:
  `src/runtime/table/composables/use-query-state.ts`
- data orchestration:
  `src/runtime/table/composables/use-table-data.ts`
- columns pipeline:
  `src/runtime/table/composables/use-table-columns.tsx`
  `src/runtime/table/utils/columns/*`
- filter pipeline:
  `src/runtime/table/composables/use-table-filters.ts`
  `src/runtime/table/composables/use-table-filter-presentation.ts`
  `src/runtime/table/composables/use-table-filter-options.ts`
  `src/runtime/table/utils/filters/*`
- rendering shell:
  `src/runtime/table/components/DataList.vue`
  `src/runtime/table/components/data-list/*`
- data-list UI and viewport contexts:
  `src/runtime/table/composables/use-data-list-ui.ts`
  `src/runtime/table/composables/use-data-list-viewport.ts`

## Important Current Reality

The current implementation works, but it is not the final shape.

There are known improvement targets:

- reduce reactive waste
- reduce layers of derived state
- simplify query-state integration
- move toward cleaner structure
- preserve or improve inference while simplifying internals

Do not treat the current layering as sacred.
If an abstraction is wasteful or too indirect, refactor it.

## Feature-Addition Rules

When adding a table feature:

1. identify the public contract first
2. decide whether it belongs in schema, API, runtime orchestration, pure utils, or rendering
3. keep normalized or config-driven handling when multiple variants exist
4. isolate variant-specific behavior behind a shared contract
5. update tests, playground, and consumer skills when the surface changes

Preferred shape:

- schema-facing definition in types/schema/building layer
- normalization or resolution in utils
- orchestration in composables
- view-only consumption in components

Avoid:

- burying domain logic directly in components
- feature behavior implemented only in playground
- one giant helper handling every variant inline

## Specific Internal Guidance

### State

- prefer one strong state abstraction over many computed bridges
- avoid derivation of derivation of derivation
- avoid temporary reactive wrappers when direct state modeling is possible
- if local draft state exists only to mirror another reactive source, reconsider the abstraction

### Columns

- columns are a pipeline, not a flat render blob
- runtime columns, ordering, visibility, pinning, menu items, and render adapters should stay separated

### Filters

- filters should be definition-driven
- filter definitions currently organize around `behavior`, `display`, `source`, `editor`, and `preview`
- each filter kind should have standardized behavior and isolated implementation where logic is non-trivial
- preview generation is a good model: normalized contract plus per-kind implementation files
- filter presentation is a separate orchestration concern from filter semantics
- client facet counts belong to the data/query engine, not the filter render layer

### Components

- `DataListRoot.vue` owns provider and lifecycle behavior while rendering no mandatory wrapper
- `DataList.vue` is the stable assembled recipe and must be built from the same public parts consumers compose directly
- granular parts own rendering only and must consume prepared state from table internals
- popup parts expose a standard custom trigger slot; full and incremental data states stay separate
- every granular part exposes a typed flat `ui` slot map; page defaults belong to `DataListRoot.ui`, while underlying Nuxt UI primitives retain application theme inheritance
- renderer internals should consume prepared state rather than reinvent logic

### Pagination

- pagination is a `none`, `offset`, or `cursor` strategy selected by schema
- only offset page and size state is URL-backed; cursor accumulation stays in TanStack infinite-query state
- filter, search, and sorting owners call the pagination reset command instead of writing page fields
- cursor pages flatten and de-duplicate by `rowKey`; loaded and total counts remain distinct
- the public API is conditional so offset-only and cursor-only commands do not leak across schema modes

## When To Reorganize

Reorganize without hesitation when:

- a file is carrying multiple unrelated concerns
- a feature introduces another variant into a growing domain
- the state model is becoming layered and wasteful
- a top-level folder should really become a subdomain under `utils/`

Builder-specific note:

- existing top-level `src/runtime/table/builders` is transitional
- prefer the long-term direction of `utils/builders/` when touching or growing builder code
