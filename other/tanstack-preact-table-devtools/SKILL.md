---
name: tanstack-preact-table-devtools
description: "Connect native Preact Table v9 instances to Devtools with tableDevtoolsPlugin and useTanStackTableDevtools. Load for React-package mixups, missing targets, required options.key, enabled state, cleanup, or development gating."
license: "MIT"
metadata:
  internal: true
  tanstack-framework: "preact"
  tanstack-library: "@tanstack/preact-table-devtools"
  tanstack-library-version: "9.2.5"
  tanstack-package: "@tanstack/preact-table-devtools"
  tanstack-package-version: "9.2.5"
  tanstack-requires: "[\"tanstack-table-core\",\"tanstack-table-devtools\"]"
  tanstack-source-skill: "devtools"
  tanstack-sources: "[\"TanStack/table:docs/devtools.md\",\"TanStack/table:packages/preact-table-devtools/src/index.ts\",\"TanStack/table:packages/preact-table-devtools/src/useTanStackTableDevtools.ts\"]"
  tanstack-type: "framework"
---

This skill builds on @tanstack/table-core#core and @tanstack/table-devtools#devtools.

## Setup

```tsx
import { TanStackDevtools } from '@tanstack/preact-devtools'
import { useTable, tableFeatures } from '@tanstack/preact-table'
import {
  tableDevtoolsPlugin,
  useTanStackTableDevtools,
} from '@tanstack/preact-table-devtools'

const features = tableFeatures({})
const columns = [{ accessorKey: 'id' }]
const data: Array<{ id: string }> = []

export function App() {
  const table = useTable({
    key: 'users-table',
    features,
    columns,
    data,
  })
  useTanStackTableDevtools(table)
  return <TanStackDevtools plugins={[tableDevtoolsPlugin()]} />
}
```

## Hooks and Components

Use the native Preact packages throughout. Pass `{ enabled }` rather than conditionally calling the registration hook.

## Common Mistakes

### HIGH React Devtools package mixed into Preact

Wrong: import the hook from `@tanstack/react-table-devtools` through compat.

Correct: use `@tanstack/preact-table-devtools` with `@tanstack/preact-devtools`.

The native adapter owns Preact effect lifecycle and plugin types.

Source: TanStack/table:docs/devtools.md

### HIGH Missing or duplicate key

Wrong: omit `key` or reuse `users-table` for multiple mounted tables.

Correct: give each live table one stable unique key.

Keyless registration is skipped; duplicate keys replace targets.

Source: TanStack/table:packages/table-devtools/src/tableTarget.ts

### MEDIUM Production no-op mistaken for failure

Wrong: expect the default entrypoint to stay active in a production bundle.

Correct: keep Devtools development-only unless an explicit production import is required.

The default index deliberately selects no-op implementations outside development.

Source: TanStack/table:packages/preact-table-devtools/src/index.ts

## API Discovery

Inspect `node_modules/@tanstack/preact-table-devtools/dist/index.d.ts` and `useTanStackTableDevtools.d.ts`; do not copy React adapter imports.
