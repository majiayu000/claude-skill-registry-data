---
name: react-best-practices
description: React component, state, effects, and performance best practices. Use when writing, reviewing, or refactoring React components, hooks, state management, or when the user asks about React patterns, useEffect rules, or component design.
---

# React Best Practices

## Components

- Use `FC` type annotation for all React components.
- Prefer composition over configuration — pass JSX as children or render props instead of adding more props to a component.
- Keep components small and single-responsibility; extract early when a component handles more than one concern.
- Co-locate related code (component, hook, types, styles) in the same directory.
- Prefer named exports over default exports for better refactoring support and explicit imports, unless the framework requires default exports (e.g., route pages, layouts).

## State

- Minimize state — if it can be computed from existing state or props, derive it during render (or `useMemo`), not in `useEffect`.
- Do not sync state in `useEffect`; use a single source of truth (e.g., reducer, URL params, or lifting state up).
- Use `useReducer` over multiple `useState` when state transitions are interdependent.
- Keep state as close to where it's used as possible; lift only when genuinely shared.

## Effects

- Do not turn user actions into effects; handle them in event handlers.
- `useEffect` is for synchronizing with external systems (DOM APIs, subscriptions, timers) — not for reacting to state changes.
- Every effect must have a proper cleanup function when it holds resources (listeners, timers, abort controllers).

## Performance

- Do not optimize prematurely — profile first, then act.
- Use `React.memo` only on components that re-render frequently with the same props and are expensive to render.
- Stabilize callback and object references with `useCallback` / `useMemo` only when they are passed to memoized children or used in dependency arrays.
- Prefer moving state down or splitting components over adding memoization.
- For lists, use stable, unique `key` values — never use array index as key on reorderable or filterable lists.

## Refs

- Use `ref` for imperative access to DOM nodes or to persist mutable values across renders without triggering re-renders.
- Do not use `ref` as a workaround to avoid dependency arrays in effects.

## Error Handling

- Wrap route-level or feature-level boundaries with Error Boundaries to isolate failures.
- Provide meaningful fallback UI — never leave the user with a blank screen.

## Testing & Stories

- Design every component to be testable in isolation — accept dependencies via props, avoid hard-coded singletons.
- Write unit tests with **React Testing Library**; test behavior and user interactions, not implementation details.
- Provide **Storybook** stories for each component covering all meaningful variants: default, loading, empty, error, edge cases, and responsive breakpoints.

## Dependencies

- Prefer well-maintained libraries over hand-rolling solutions. Evaluate before adopting: ESM support, TypeScript types, download volume, recent commit activity, and documentation quality.
- If no library meets the quality bar, implement it yourself.

## Custom Hooks

- Extract reusable logic into custom hooks; name them `use*`.
- A custom hook should do one thing; compose multiple hooks rather than building a monolithic one.
- Return the minimal surface area needed by consumers.
