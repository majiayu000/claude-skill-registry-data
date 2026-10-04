---
name: tanstack-table-core-sorting
description: "Sort with rowSortingFeature, sortedRowModel, sortFns, multi-sort and removal options, sortUndefined, and manualSorting. Load for comparator direction, incoming server order, or product-specific sorting cycles."
license: "MIT"
metadata:
  internal: true
  tanstack-library: "@tanstack/table-core"
  tanstack-library-version: "9.2.5"
  tanstack-package: "@tanstack/table-core"
  tanstack-package-version: "9.2.5"
  tanstack-requires: "[\"tanstack-table-core\",\"tanstack-table-core-table-features\",\"tanstack-table-core-client-vs-server\"]"
  tanstack-source-skill: "sorting"
  tanstack-sources: "[\"TanStack/table:docs/framework/react/guide/sorting.md\",\"TanStack/table:packages/table-core/src/features/row-sorting\",\"TanStack/table:examples/react/sorting\"]"
  tanstack-type: "sub-skill"
---

This skill builds on `core`, `table-features`, and `client-vs-server`. Sorting state describes order; client processing requires a sorted model and server processing requires sorted input.

## Setup

```ts
import {
  createSortedRowModel,
  rowSortingFeature,
  sortFn_alphanumeric,
  sortFn_text,
  tableFeatures,
} from '@tanstack/table-core'

export const features = tableFeatures({
  rowSortingFeature,
  sortedRowModel: createSortedRowModel(),
  sortFns: { alphanumeric: sortFn_alphanumeric, text: sortFn_text },
})
```

Import individual `sortFn_*` built-ins and register only those your columns
reference by string name or that `sortFn: 'auto'` should resolve for your data
types. The full `sortFns` registry object still works but bundles every
built-in; numeric columns fall back to a basic comparator without registration.

## Core Patterns

```ts
const options = { enableSortingRemoval: false, enableMultiSort: true }
const numericColumn = { sortUndefined: 'last' as const }
```

Configure sort cycles and undefined placement to match the product rather than relying on implicit defaults.

## Common Mistakes

### [CRITICAL] Expecting manual mode to reorder

Wrong: `const options = { data: unsortedRows, manualSorting: true }`

Correct: `const options = { data: serverSortedRows, manualSorting: true }`

Manual sorting bypasses `sortedRowModel` and trusts incoming order.

Source: `packages/table-core/src/features/row-sorting/rowSortingFeature.types.ts`

### [HIGH] Reversing inside the comparator

Wrong: `const newest: SortFn<any, any> = (a, b, id) => b.getValue<number>(id) - a.getValue<number>(id)`

Correct: `const numeric: SortFn<any, any> = (a, b, id) => a.getValue<number>(id) - b.getValue<number>(id)`

Return ascending comparison only; Table reverses it when sorting is descending.

Source: `docs/framework/react/guide/sorting.md#custom-sorting-functions`

### [MEDIUM] Leaving ambiguous sort policy

Wrong: `const options = { enableSortingRemoval: true }`

Correct: `const options = { enableSortingRemoval: false }; const rankColumn = { sortUndefined: 'last' as const }`

Undefined placement and removal cycles can differ from expected product behavior unless configured.

Source: `packages/table-core/src/features/row-sorting/rowSortingFeature.types.ts`

## API Discovery

Inspect `node_modules/@tanstack/table-core/dist/features/row-sorting/` and `dist/features/row-sorting/sortFns.d.ts` for current names and comparator contracts.
