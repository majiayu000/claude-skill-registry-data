---
name: create-react-modlet
description: Create React components, hooks, and data-loading surfaces for the Measure of Success app following the modlet pattern. Use when adding any Custom UI component, custom hook, or surface. Adapted for this app (Vitest, @ui/@domain aliases, Tailwind-on-Atlaskit-tokens, injectable loader hooks, portable-stories tests).
---

# Skill: Create a React Modlet (Measure of Success)

Adapted from Bitovi's `create-react-modlet` for **this** app's stack: Custom UI
(React + Vite), **Vitest** (not Jest), Tailwind mapped to **Atlaskit design
tokens** (no shadcn/`cn`), path aliases `@ui`/`@domain`/`@backend`/`@harness`,
and the **injectable loader hook** convention for data-loading surfaces.

## What is a modlet?

A self-contained folder holding everything for one module — implementation,
tests, stories (for visual components), and optional types — with an `index.ts`
that only re-exports. Named after its main export.

## When to use

- Any new Custom UI component or surface (`app/src/ui/…`)
- Any custom hook (data loader, view logic)
- Breaking a complex surface into sub-components

## Locations (this app)

| Kind | Location |
|---|---|
| Surface (page-level Custom UI) | `app/src/ui/surfaces/<Surface>/` |
| Data-loading hook (bridge seam) | `app/src/ui/data/<useHook>/` |
| Shared/leaf component | `app/src/ui/components/<Component>/` (create as needed) |
| Sub-component of a surface | `app/src/ui/surfaces/<Surface>/components/<Sub>/` |

## Modlet shapes

**Visual modlet (component/surface):**
```
IssuePanel/
├── index.ts                 # re-export only:  export { IssuePanel } from './IssuePanel.js';
├── IssuePanel.tsx           # implementation
├── IssuePanel.stories.tsx   # Storybook scenarios + play() interaction tests
├── IssuePanel.test.tsx      # composeStories runner (see below)
└── types.ts                 # optional
```

**Non-visual modlet (hook/util):**
```
usePanelData/
├── index.ts                 # export * from './usePanelData.js';
├── usePanelData.ts
└── usePanelData.test.ts     # optional for thin bridge adapters (see note)
```

## Core rules

1. Folder name matches the main export.
2. `index.ts` **only** re-exports — never define logic there.
3. Import with the `.js` extension and folder entry points:
   `import { IssuePanel } from '@ui/surfaces/IssuePanel/index.js';`
4. Use path aliases (`@ui`, `@domain`), never deep relative paths across layers.
5. **Domain stays pure** — components import `@domain` *types* + pure functions
   only; all Jira/KVS I/O goes through the bridge seam (below).

## The injectable loader hook (data-loading surfaces)

Surfaces must **not** fetch inline. Extract the `@forge/bridge` seam into a
loader-hook modlet and inject it as a prop defaulted to the real hook, so stories
and tests swap in a stub returning canned scenario data — every branch
(loading / error / empty / …) renders deterministically with no bridge or async.

```tsx
// data/usePanelData/usePanelData.ts — the real loader (default)
export interface PanelController {
  data: PanelData | null; pending: boolean; error: string | null; busy: boolean;
  save(a: Assignment): void; remove(kpiId: string): void;
}
export type UsePanel = (issueId: string) => PanelController;
export const usePanelData: UsePanel = (issueId) => { /* useEffect + call() */ };
```

```tsx
// surfaces/IssuePanel/IssuePanel.tsx — loader injected, defaulted to the real hook
export function IssuePanel({ issueId = '10048', usePanel = usePanelData }:
  { issueId?: string; usePanel?: UsePanel }) {
  const { data, pending, error, save, remove } = usePanel(issueId);
  if (error)   return <ErrorState message={error} />;
  if (pending) return <Loading />;
  // …render data, wire save/remove…
}
```

The controller returns **data + status + actions**; name the hook `use*` and call
it unconditionally (rules of hooks). This is the "pure core, thin adapters" rule
(constitution §3) applied to the UI: the component is pure given `usePanel`.

## Styling

Tailwind utilities mapped to Atlaskit tokens (see `tailwind.config.js` +
`src/ui/styles.css`): `bg-surface`, `text-text-subtle`, `border-border`,
`text-brand`, `text-danger`, `text-success`. No `cn()`/shadcn. Prefer Atlaskit
components for standard widgets once adopted; Tailwind for custom layout/canvas.

## Stories = scenarios + tests

Stories inject a **stub loader hook** per scenario and assert in `play()` using
`@storybook/test` (`within`, `userEvent`, `expect`, `fn`, `waitFor`). Cover the
data matrix: loading, error, empty, and each meaningful data shape, plus at least
one interaction (edit/save/record) with a spy.

```tsx
// IssuePanel.stories.tsx
const stub = (over): UsePanel => () => ({ data: over.data, pending: false, error: null, busy: false, save: over.save ?? (() => {}), remove: () => {} });
export const AllGroups: Story = {
  args: { usePanel: stub({ data: ALL_GROUPS }) },
  play: async ({ canvasElement }) => {
    await expect(within(canvasElement).getByText('Shared with parent')).toBeInTheDocument();
  },
};
```

Every visual modlet gets a **`*.test.tsx`** that replays its stories via portable
stories (no browser, runs in jsdom under Vitest):

```tsx
// IssuePanel.test.tsx
import { composeStories } from '@storybook/react';
import { render } from '@testing-library/react';
import * as stories from './IssuePanel.stories.js';
const composed = composeStories(stories);
describe('IssuePanel stories', () => {
  for (const [name, Story] of Object.entries(composed)) {
    test(name, async () => {
      const { container } = render(<Story />);
      await Story.play?.({ canvasElement: container });
    });
  }
});
```

## Test segmentation (npm scripts)

| Script | Runs | Env |
|---|---|---|
| `npm test` | pure-domain unit tests (`src/**/*.test.ts`) | node — fast |
| `npm run test:stories` | story tests (`src/ui/**/*.test.tsx`) via `vitest.stories.config.ts` | jsdom |
| `npm run test:all` | both | — |
| `npm run storybook` | the visual workbench | browser |

Story tests are `.test.tsx` and the domain config only includes `.test.ts`, so
the two suites never overlap.

## Creation process

1. `manage_todo_list` the steps.
2. Create the folder + `index.ts` re-export.
3. Add the implementation. For a surface, extract/require an injectable loader hook.
4. Add `*.stories.tsx` (scenarios + play interaction tests).
5. Add `*.test.tsx` (composeStories runner).
6. Verify: `npm test`, `npm run test:stories`, `npm run typecheck`, and eyeball
   `npm run storybook`.

## Quality checklist

- [ ] Folder name matches the export; `index.ts` only re-exports
- [ ] Surfaces take an injectable loader hook (no inline `call()`/fetch)
- [ ] Component is pure given its loader (all I/O behind the bridge seam)
- [ ] Stories cover loading/error/empty + each data shape + ≥1 interaction
- [ ] `*.test.tsx` replays the stories; `npm run test:stories` green
- [ ] `npm test` + `npm run typecheck` green
- [ ] Tailwind-on-Atlaskit tokens (no shadcn/`cn`); `@domain` used for types/logic

## Note on hook tests

Thin bridge-adapter loader hooks (`usePanelData`, …) are primarily validated
*through* the surface story tests (which inject stubs) and the resolver contract.
Add an isolated `*.test.tsx` (jsdom + `renderHook` against the mock bridge) when a
hook grows non-trivial logic of its own.

## Reference implementations

- Surface: `app/src/ui/surfaces/IssuePanel/`
- Loader hook: `app/src/ui/data/usePanelData/`
- Storybook config: `app/.storybook/`, story test config: `app/vitest.stories.config.ts`
