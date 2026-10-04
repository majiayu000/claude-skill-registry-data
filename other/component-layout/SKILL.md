---
name: component-layout
description: >
  How a component is laid out on disk: when a single file becomes a
  folder, what the parts are called, and which way the imports run.
  Applies whenever adding to a component that is already long, or
  splitting one that has grown past reading in one sitting.
---

A component file is read top to bottom by somebody looking for one thing. Past about 600 lines nobody reads it that way any more, so it becomes a folder.

## The folder

The folder is named for the component in kebab-case and sits where the file did: `catches/CatchDialog.tsx` becomes `catches/catch-dialog/`. Importers keep their old path minus the file name — `from '../catches/catch-dialog'` — so a split is invisible to everything outside it.

```
catches/catch-dialog/
  index.tsx        the exported component, and what declares its resources
  sheet.tsx        the reading half, one component
  describe.ts(x)   pure readings of a record: no state, no JSX beyond a leaf
  sections/        one file per part of the panel, each a component
```

- **`index.tsx`** holds the component the folder is named for and nothing else worth reading elsewhere. It is the only file importers know about.
- **Pure helpers** go in a lowercase file named for what they answer — `describe.ts`, `metrics.ts`, `field.ts`, `summary.ts`. Constants that two parts share live in `metrics.ts`.
- **Sub-components** are PascalCase files, one component each, default-exported. Several small ones that only make sense together may share one lowercase file (`counters/care.tsx`).
- A file with a single export default-exports it; the linter enforces this.

## Which way the imports run

Parts never import from `index`. If a part needs a type the index declares, the type moves down into the part and `index` re-exports it:

```tsx
// index.tsx
import { AuctionBoard, type AuctionTabProps } from './board';

export type { AuctionTabProps };
```

A cycle between two parts means the thing they share belongs in a third file.

## What to pull out first

In order of how much they buy:

1. **Pure functions and constants.** They move with no props to thread and are the easiest thing to test.
2. **Sections of the returned markup.** Each takes explicit props — the values it reads and the callbacks it calls — never a bag of the parent's internals. A section that would need eight props is usually two sections.
3. **The reading half of a resource.** See the `resource-suspense` skill: the declaring body stays in `index.tsx`, the reading body is the part.

Splitting a canvas component is the same exercise with different names: measurements in `metrics.ts`, what is where in `field.ts`, painting in `draw.ts`, movement in `motion.ts`, and the component itself in `index.tsx`.

## What not to do

- Do not split by size alone. Two hundred lines that are read together stay together.
- Do not invent a `utils.ts`. A file is named for what it answers, not for what it is.
- Do not leave a part exporting only to `index` and importing back from it.
