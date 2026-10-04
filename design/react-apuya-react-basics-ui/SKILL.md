---
name: react
description: Engineers React against its rendering model — components as pure functions of props and state, hooks under the Rules of Hooks, composition via children and slots, effects only to sync with external systems, refs as imperative escape hatches, keys matching identity, state at its lowest common owner, derivations computed in render, memoization only after measured cost. Audits unnecessary effects, stale closures, missing deps, broken keys, state mirroring props, and re-renders through memoized children. Use for hooks, composition, re-render or stale-state bugs, sprawling useEffect, local vs lifted state, or component audits. Triggers on "react", "jsx", "hook", "custom hook", "useState", "useEffect", "useMemo", "useCallback", "useRef", "useReducer", "useContext", "rules of hooks", "stale closure", "exhaustive-deps", "lift state", "controlled component", "render prop", "compound component", "key warning", "re-render", "memoize", "react.memo", "forwardRef", "error boundary", "strict mode".
---

# React Engineer

Write and review React using the model the library is built on.

## The rendering model

A component is a pure function of its props and state. React calls it when it decides to render, compares the returned tree to the previous one, and applies the diff to the DOM. You describe the UI; you do not drive the DOM.

Consequences that shape every other rule:

- The same props and state must yield the same JSX.
- Side effects belong outside the render path.
- State updates are scheduled, not immediate; reading state right after `setState` returns the old value.
- A component re-renders when its state changes, its parent re-renders, or a consumed context value changes.

## Rules of Hooks

- Call hooks at the top level of the function body. Never inside conditionals, loops, `try`/`catch`, or after an early `return`.
- Call hooks only from React function components or other hooks. Never from event handlers, class methods, or plain functions.
- The dependency array of `useEffect`, `useMemo`, `useCallback`, and `useImperativeHandle` must list every reactive value referenced inside. Suppressing `react-hooks/exhaustive-deps` is a code smell, not a fix.

A custom hook is any function whose name starts with `use` that calls other hooks. Extract a custom hook when two components share the same hook composition, or when a single component's hook block has grown unreadable.

## Effects

`useEffect` synchronizes a component with something outside the React tree: a DOM API the browser owns, a subscription, a timer, a third-party library, a network resource.

It is the wrong tool for:

| Wrong use of an effect | Right tool |
|------------------------|------------|
| Transforming props or state into a value to render | Compute it in render |
| Responding to a user action | Put the logic in the event handler |
| Resetting state when a prop changes | Lift the state, derive it, or pass a `key` to remount |
| Notifying a parent that state changed | Lift the state, or call the parent in the handler that caused the change |
| Initializing state from props | `useState` initializer, or a `key` to remount |
| Chaining state updates (one effect's setState triggers the next) | Compute the full next state in one place |

Every effect needs a cleanup if it subscribes, schedules, listens, or otherwise leaves state behind. Strict Mode mounts → unmounts → mounts in development specifically to surface effects that forget to clean up.

## State

- **Place state at its lowest common owner.** Move it up when two siblings need it, not earlier.
- **Treat state as immutable.** Replace, never mutate (`setItems([...items, x])`, not `items.push(x)`).
- **Do not store derived values.** If `b` can be computed from `a`, compute it in render unless profiling shows the cost matters.
- **Group state that changes together; split state that changes independently.** A reducer fits naturally when several fields update in lockstep.
- **Do not mirror props in state.** If a prop must seed an initial value, accept it in `useState(prop)` and treat the prop as the source of truth thereafter, or pass `key={prop}` to remount.

## Keys

Keys tell React which item in a list is which across renders.

- Use a stable id from the data.
- The array index is acceptable **only** when the list is append-only and never sorts, filters, reorders, or inserts.
- A key change unmounts the old subtree and mounts a fresh one — useful as an intentional reset, dangerous as an accident.

## Composition

| Pattern | When |
|---------|------|
| `children` / named slots | Parent does not need to know what is inside |
| Compound components (`Tabs` + `Tabs.Panel` sharing context) | Consumers legitimately rearrange the parts and the parts share state |
| Render prop / function-as-child | The child needs an argument only the parent can supply |
| Higher-order component | A cross-cutting concern that JSX composition cannot express |

Reach for the smallest pattern that satisfies the case. Prefer composition over configuration: a prop that switches between two layouts is usually two components.

## Refs

- `useRef` holds a mutable value that **does not** trigger a re-render when it changes, or holds a DOM node.
- Do not use a ref to cache state the UI is supposed to react to — that is what `useState` is for.
- `forwardRef` any component whose underlying element a parent may focus, scroll to, or measure.
- Read and write refs in effects or event handlers, not during render.

## Memoization

`React.memo`, `useMemo`, and `useCallback` are not free — they add comparison cost and dependency-array maintenance. Reach for them only when one of:

- A profiler shows the re-render cost is a real bottleneck.
- A child is wrapped in `React.memo` and is receiving an inline object or function on every render.
- A value is a dependency of another hook and needs referential stability to avoid a loop.

Default to no memoization. Add it when a measurement justifies it.

> **This library is a deliberate exception, and you should follow its convention.**
> 154 of 167 component files are wrapped in `React.memo`, and `useMemo` guards the
> computed class strings in 76 of them. That is intentional: a published component
> renders inside *someone else's* tree, at a depth and re-render cadence the library
> cannot see or profile. A parent that re-renders on every keystroke would otherwise
> drag every primitive with it.
>
> So: keep `memo` on components, and keep `useMemo` around `cn(...)` results that
> depend on several props. Do **not** strip existing memoization as "unjustified" —
> and do not treat this as licence to wrap every local helper. Inside a component,
> the ordinary rule still applies.

## Context

Context broadcasts a value to every descendant that subscribes. Use it for values genuinely needed at many depths: theme, current user, locale, feature-flag client.

- Two or three levels of prop drilling is not a context use case. Pass the prop.
- Every consumer re-renders when the value changes. Split context by update cadence — separate a frequently-changing value from a rarely-changing one.
- The value should be stable; wrap object values in `useMemo` so unrelated parent re-renders do not invalidate every consumer.

## Error boundaries

Wrap segments of the tree that can fail independently (a route, a widget, a third-party embed). Boundaries catch errors thrown during render, in lifecycle methods, and in constructors of the components below them.

> **This library ships no `ErrorBoundary`** — boundaries are the consuming
> application's call, since only it knows what a survivable segment is. The
> obligation here is the other half: a primitive should not throw during render.
> Guard on missing context with a clear message (`createComponentContext` already
> does), and render an empty or fallback state rather than crashing a consumer's tree.

They do **not** catch:

- Errors inside event handlers — handle them in the handler.
- Errors in asynchronous code (promises, timers) — surface them via state and re-throw in render if you want the boundary to take over.
- Errors during server rendering — the framework handles those.

## Strict Mode

In development, `<StrictMode>` invokes components and effects twice (mount → unmount → mount) to surface impurity and missing cleanup. Production is unaffected. If a component breaks under Strict Mode, the bug exists — Strict Mode just made it visible.

## Audit checklist

| Smell | Fix |
|-------|-----|
| `useEffect` that calls `setState` from props or other state | Compute in render |
| `useEffect` that runs logic belonging to a user action | Move into the event handler |
| `// eslint-disable react-hooks/exhaustive-deps` | Identify the real reactive value and depend on it, or restructure |
| Array index as key on a list that sorts, filters, or reorders | Use a stable id from the data |
| State that duplicates a prop | Lift, derive, or remount via `key` |
| `useCallback` / `useMemo` with no memoized consumer | Remove — **except** the library-wide `memo` + `useMemo(cn(...))` convention above, which is deliberate |
| Inline `{...}` or `() => ...` passed to a `React.memo` child | Memoize the value or restructure the boundary |
| `useRef` holding data the UI should re-render on | Convert to `useState` |
| Context value rebuilt every render | Wrap in `useMemo` with correct deps |
| Hook called inside a condition or after early return | Move to the top level |
| State mutated in place (`arr.push`, `obj.x = y`) | Replace with a new value |
| Effect with no cleanup that subscribes, listens, or schedules | Return a cleanup function |
| `setState` called during render outside the documented `if (prev !== derived)` pattern | Compute in render, or move to an effect or handler |
| Reading state right after `setState` expecting the new value | Use the value you passed in, or a functional updater |

## Anti-patterns

- Calling hooks conditionally or in loops.
- Mutating state, props, or context values.
- Storing JSX in state.
- Using `useEffect` with `[]` to run "once" for logic that belongs to a mount-time event (e.g. analytics fired from a click).
- Using a ref to avoid a re-render the UI actually needs.
- Putting an effect inside an event handler instead of running the work directly.
- Wrapping every *local* callback in `useCallback` "to be safe" (component-level `memo` is a separate, deliberate convention here).

## Definition of Done

- Hooks follow the Rules of Hooks; no suppressed `exhaustive-deps`.
- No effect derives state from props or runs handler logic.
- Lists have stable keys; the index appears only on provably append-only lists.
- State sits at its lowest common owner; no mirror-of-prop state without a remount key.
- Memoization is justified by a profiler, a memoized child, a hook dependency — or the library-wide component `memo` convention.
- Context values are memoized and split by update cadence.
- Effects that subscribe, listen, or schedule return cleanup.
- Component is pure in render: no side effects, no `setState`, no DOM reads.
