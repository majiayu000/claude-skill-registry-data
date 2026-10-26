---
name: react-best-practices
description: Use when writing or reviewing React components and hooks — component design, state management, data fetching, memoization, TypeScript typing in .tsx files.
---

# React Best Practices

## Component design

- Prefer functional components. Follow Single Responsibility: a component does
  one job; extract when it starts doing two.
- Avoid inline render functions/closures created fresh on every render inside
  JSX where they cause unnecessary child re-renders.

## Hooks

- Follow the rules of hooks: only call at the top level, only from React
  functions/custom hooks.
- Use `useState` for local state, `useEffect` only for real synchronization with
  an external system (not for derived state).
- Extract repeated stateful logic into custom hooks (`use*`) instead of
  duplicating it across components.

## State management strategy

- Start local (`useState`). Escalate to Context only when several components
  genuinely need the same state. Escalate to Zustand/Redux only when Context
  causes prop-drilling-scale re-render problems or the state is genuinely
  app-wide.
- Avoid prop drilling more than 1–2 levels — that's a signal to lift state or use
  Context/a store instead.

## Data fetching

- Use **React Query** (or equivalent) for server-state data fetching and
  caching, rather than hand-rolled `useEffect` fetch + loading/error state.

## Memoization

- Apply `React.memo` / `useCallback` / `useMemo` deliberately, where a profiled
  re-render or expensive computation justifies it — not by default on every
  component/function.

## TypeScript

- Type props, state, and hook return values explicitly. No `any` — prefer
  `unknown` + narrowing, or a precise type/interface. Do not use `PropTypes`;
  TypeScript typing replaces it.

## Testing & hygiene

- Test components with React Testing Library (behavior, not implementation
  detail).
- Strip `console.*` calls from production builds.
- List keys, accessibility, and error boundaries are real gaps to watch for and
  are left to team judgment/review rather than dictated here.

---
Source: medium.com/@raveenpanditha — mastering-react-best-practices
