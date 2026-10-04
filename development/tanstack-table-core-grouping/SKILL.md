---
name: tanstack-table-core-grouping
description: "Group rows with columnGroupingFeature, groupedRowModel, groupedColumnMode, and manualGrouping. Load for grouped or placeholder cells and grouping interactions with expansion or pagination."
license: "MIT"
metadata:
  internal: true
  tanstack-library: "@tanstack/table-core"
  tanstack-library-version: "9.2.5"
  tanstack-package: "@tanstack/table-core"
  tanstack-package-version: "9.2.5"
  tanstack-requires: "[\"tanstack-table-core\",\"tanstack-table-core-table-features\",\"tanstack-table-core-client-vs-server\"]"
  tanstack-source-skill: "grouping"
  tanstack-sources: "[\"TanStack/table:docs/framework/react/guide/grouping.md\",\"TanStack/table:packages/table-core/src/features/column-grouping\",\"TanStack/table:examples/react/grouping\"]"
  tanstack-type: "sub-skill"
---

This skill builds on `core`, `table-features`, and `client-vs-server`. Grouping creates row structure and the renderer chooses grouped-cell UI. Load the separate `aggregation` skill when grouped rows should also calculate values.

## Setup

```ts
import {
  columnGroupingFeature,
  createGroupedRowModel,
  tableFeatures,
} from '@tanstack/table-core'

export const features = tableFeatures({
  columnGroupingFeature,
  groupedRowModel: createGroupedRowModel(),
})
```

## Core Patterns

```ts
const options = { groupedColumnMode: 'reorder' as const }
const mode = cell.getIsGrouped()
  ? 'grouped'
  : cell.getIsPlaceholder()
    ? 'placeholder'
    : 'value'
```

Render these cell modes deliberately.

## Common Mistakes

### [HIGH] Registering processing without grouping

Wrong: `tableFeatures({ groupedRowModel: createGroupedRowModel() })`

Correct: `tableFeatures({ columnGroupingFeature, groupedRowModel: createGroupedRowModel() })`

The grouped row-model slot requires `columnGroupingFeature`.

Source: `packages/table-core/src/types/TableFeatures.ts#FeatureSlotPrereqs`

### [HIGH] Treating rendered rows as underlying records

Wrong: `const leafCount = table.getRowModel().flatRows.filter(row => !row.subRows.length).length`

Correct:

```ts
const countLeafRows = (rows: typeof groupRow.subRows): number =>
  rows.reduce(
    (count, row) =>
      count + (row.subRows.length ? countLeafRows(row.subRows) : 1),
    0,
  )
const leafCount = countLeafRows(groupRow.subRows)
```

Count descendants from one group row rather than the flattened render model,
where group rows and expanded rows may both appear. The current
`table.getRowModel().rows` is render order, while original dataset counts come
from the data owner.

Source: `docs/framework/react/guide/grouping.md`

### [HIGH] Rendering every cell identically

Wrong: `render(cell.getValue())`

Correct: `render(cell.getIsPlaceholder() ? null : cell.getValue())`

Placeholder cells do not represent ordinary leaf values. Group rows should
only render their grouped cell when aggregation is not enabled.

Source: `examples/react/grouping/src/main.tsx`

## API Discovery

Inspect `node_modules/@tanstack/table-core/dist/features/column-grouping/` for
grouping. Load the `aggregation` skill when totals, multiple aggregations,
grouped aggregate values, or custom definitions are part of the task.
