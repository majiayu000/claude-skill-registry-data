---
name: jotai
description: Write, review, refactor, or debug idiomatic Jotai state code for React and TypeScript. Use when work involves Jotai atoms, derived atoms, write-only action atoms, async atoms, Provider/store usage, jotai/utils, atomWith* helpers, atomFamily or jotai-family migration, large-object/list state, render performance, testing Jotai code, or converting React Context/useState/reducer-style state into a more Jotai-like atom model.
---

# Jotai

## Overview

Use this skill to make Jotai code feel atomic, composable, and React-friendly. Prefer small state boundaries, derived atoms, write-only action atoms, stable atom references, and narrow subscriptions over store-shaped objects and broad component rerenders.

## Workflow

1. Inspect the target code before changing it. Identify existing state ownership, update paths, render hot spots, async behavior, and test coverage.
2. Model state as atoms. Split values when they change independently, derive computed values with read-only atoms, and move commands into write-only atoms.
3. Use the narrowest React hook. Prefer `useAtomValue` for reads and `useSetAtom` for writes; use `useAtom` only when the component genuinely needs both.
4. Keep atom configs stable. Define atoms at module scope when possible; if created during render, memoize them with `useMemo`, `useRef`, or `useState`.
5. Reach for utilities only when they match the shape of the problem. Prefer plain derived atoms first; use `splitAtom`, `focusAtom`, `atomWithStorage`, `atomWithReset`, `unwrap`, or related helpers when they remove real complexity.
6. Verify behavior from the user-facing surface when possible. Add focused atom-level tests only for logic that is hard to exercise through components.

## Reference Routing

Read only the files that match the task:

- `references/atom-modeling.md` for deciding atom boundaries, derived atoms, action atoms, writable adapters, resets, storage, and family-style parameterized atoms.
- `references/react-usage.md` for hook selection, Provider/store scope, hydration, dynamic atom creation, and component architecture.
- `references/async-and-side-effects.md` for Suspense, async reads, async actions, abort signals, non-Suspense states, refresh flows, and external side effects.
- `references/performance-and-large-state.md` for render tuning, `selectAtom`, `focusAtom`, `splitAtom`, large objects, lists, and dependency graph depth.
- `references/typescript-and-testing.md` for TypeScript inference, writable atom argument types, `ExtractAtomValue`, and testing strategy.
- `references/utilities-decision-guide.md` for choosing built-in utilities such as storage, SSR hydration, resettable/default atoms, lazy atoms, callbacks, reducers, select, split, and family migration.
- `references/extensions-decision-guide.md` for choosing extension packages such as TanStack Query, optics, Immer, effects, location, scope, cache, XState, GraphQL/RPC, and external-store bridges.
- `references/tools-and-debugging.md` for choosing Devtools, Babel, SWC, and Rolldown support for debugging, labels, React Refresh, and bundler integration.
- `references/recipes-decision-guide.md` for deciding when to use or adapt official recipes such as debounce, listeners, broadcast, compare, toggle, custom hooks, reducer hooks, and atom effects.

## Jotai-Like Review Heuristics

Favor these changes during reviews and refactors:

- Replace monolithic app-state atoms with smaller atoms when fields update or render independently.
- Replace repeated component-local derivations with read-only derived atoms when the value is shared or belongs to the state graph.
- Replace reducer-shaped dispatch atoms with focused write-only action atoms when actions can be code-split or used independently.
- Hide implementation atoms in module scope and export intentional read/action atoms when it clarifies the public state API.
- Replace `const [, setValue] = useAtom(valueAtom)` with `useSetAtom(valueAtom)` when a component only writes.
- Replace `const [value] = useAtom(valueAtom)` with `useAtomValue(valueAtom)` when a component only reads.
- Avoid creating atoms inline in render without memoization.
- Treat `selectAtom` as an escape hatch for equality or previous-slice needs, not the default way to derive values.
- Prefer `splitAtom` for dynamic lists that need item-level subscriptions or updates.
- Avoid very deep chains of derived atoms; keep dependency graphs wide and compute reductions inside one read/action.

## Common Refactor Targets

Use this skill for requests such as:

- "Review this Jotai atom design."
- "Refactor this Context/useReducer state into Jotai."
- "Make this component stop rerendering on unrelated atom changes."
- "Move this async fetch/update flow into idiomatic Jotai atoms."
- "Design atoms for a form, table, todo list, editor, wizard, or cache."
- "Migrate `atomFamily` from `jotai/utils` to `jotai-family`."
- "Write tests for this Jotai state behavior."

## Compatibility And Source Verification

This revision was written against Jotai 2.20.2. Before giving version-sensitive API guidance, determine the target project's installed Jotai and extension-package versions, then inspect their exported types, source, or matching documentation and tests. Do not assume current documentation matches the installed version.
