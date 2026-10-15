---
name: solidjs
description: Use this when writing, reviewing, or auditing SolidJS code for fine-grained reactivity, stable view identity, and owned resource lifetimes.
---

# SolidJS

Make each state change update only its dependent bindings. Consult the
[Solid docs](https://docs.solidjs.com) for API details; apply these rules when
choosing reactive boundaries.

## Preserve views and identity

- Components run once per mount; bindings react thereafter. Never rebuild a
  subtree just to display changed state. If `<Show>`, `<Switch>`, keyed
  `<Show>`, `<Dynamic>` or a ternary swaps a heavy subtree on tab, split,
  breakpoint, collapse or loading changes, keep one subtree and update its
  classes, attributes or visibility, preserving DOM and local state.
- Render retained tabs, panes and collapsible regions with `<For>` over
  stable objects, mounting each once. For large retained subtrees, prefer an
  out-of-flow, explicitly sized host with `content-visibility: hidden` over
  `display: none` to preserve host geometry and avoid discarding layout on
  every switch.
- Give persistent items stable IDs. Use `<For>` for item identity and
  `<Index>` only when position **is** identity; never index per-item state,
  registries or memory by position, because reorder would transfer ownership.
- Put stable keys in lists and read current values inside each row. A `<For>`
  over freshly minted objects rebuilds rows; inspect the data layer's source
  to establish whether updates preserve object identity rather than assuming
  they do. See [list rendering](https://docs.solidjs.com/concepts/control-flow/list-rendering).

## Keep dependencies narrow

- Avoid a wholesale-replaced Map, Set, array or object signal with many
  readers: every replacement wakes them all. Read a store per key, or use
  `createSelector` for selection, focus, hover and active-tab membership so
  only affected readers update.
- A memo computes a value: no side effects, resource acquisition or ordering
  tricks. Derive state with a memo instead of an effect computing and setting
  another signal, which duplicates state and adds propagation. See
  [memos](https://docs.solidjs.com/concepts/derived-values/memos).
- For a keyed projection of derived state, use one `createComputed` to build
  the next table, compare per key, write only changed entries and clear removed
  keys; this keeps unchanged readers silent. Do not `reconcile` values you do
  not own, or object arrays without a declared identity key: positional reuse
  can write the next record's fields into a shared previous object. See
  [createComputed](https://docs.solidjs.com/reference/secondary-primitives/create-computed)
  and [reconcile](https://docs.solidjs.com/reference/store-utilities/reconcile).
- Keep props reactive: do not destructure them, capture a prop or signal's
  current value in the component body for later use, or spread an accessor's
  result into a snapshot. Do not construct JSX inside a repeatedly read prop:
  reads can recreate its subtree. Pass reactive accessors through to bindings.
- Use refs for elements Solid renders, not `document.querySelector`; scope
  necessary lookups to the component's own subtree so another mounted copy
  cannot receive its work.
- `batch` related writes after each `await`, because batching does not span
  the suspension and readers must not observe partial updates. See
  [batch](https://docs.solidjs.com/reference/reactive-utilities/batch).

## Own work and visibility

- Put subscriptions and fetches under the narrowest owner that outlives their
  consuming views; views lease them, so remounts, folds and tab switches do not
  refetch. Give every `createRoot` a reachable disposer and every listener,
  timer and observer an `onCleanup`, so owner departure ends its work. See
  [cleanup](https://docs.solidjs.com/reference/lifecycle/on-cleanup).
- Put state that exists only while a condition holds in a child component
  under `<Show>`, not a memo that allocates: the condition defines that child's
  lifetime. Keep the surrounding retained view outside this boundary.
- Make hidden mounted views inert through one contextual `shown` accessor.
  Gate window/document handlers, scrolling, focus, timers and "is anyone
  watching?" decisions on it. Hidden portalled overlays and menus retain state
  but withdraw from global layer stacks, so they cannot intercept the visible
  view's input. Never infer visibility from another component's DOM, element
  size or the pressed target; settle the gesture, then ask `shown()` so the
  decision uses the resulting view state.

## Review and measure

For each state change, ask **what re-runs, and what is rebuilt?** Prove fixes
with element identity before and after, and notification counts: switching a
single selection between two rows should wake exactly those two rows. Timing
alone cannot prove identity or dependency scope. Measure before claiming a
speed-up, and report the workload, metric and before/after results.
