---
name: react
description: Use when writing or reviewing React. Covers component and state design, hook correctness, memoization that is actually needed, data fetching, and the render behavior behind most React performance problems.
metadata:
  category: frontend
  version: 1.0.0
  tags: [react, hooks, state, rendering, performance]
---

# React

## Purpose

Write React where state lives in one place, effects are rare, and re-renders are understood rather than suppressed with memoization applied at random.

## When to Use

- Building or reviewing React components.
- Diagnosing unnecessary re-renders or stale state.
- Deciding where state belongs: local, lifted, context, or server.
- Removing `useEffect` calls that should not exist.

## Capabilities

- Component decomposition and state colocation.
- Hook correctness: dependencies, cleanup, and the rules that are not optional.
- State management selection: `useState`, `useReducer`, context, external store, server state.
- Data fetching with TanStack Query or the framework's own loader.
- Render profiling and targeted memoization.

## Inputs

- The component tree and where data enters it.
- The interaction and its performance characteristics, if performance is the concern.
- React version — the correct answer changed with 18 and again with 19.

## Outputs

- Components with a single source of truth for each piece of state.
- Effects only where genuinely synchronizing with an external system.
- Memoization applied where a profile shows it is needed.

## Workflow

1. **Locate the state** — Put it as close to where it is used as possible. Lift only when two siblings need it. Reach for context only when prop drilling exceeds about three levels.
2. **Separate server state from client state** — Data from an API is cache, not state. It has staleness, refetching, and error semantics that `useState` does not model. Use a query library.
3. **Delete unnecessary effects** — An effect that computes a value from props belongs in render. An effect that resets state on a prop change belongs in a `key`. Most `useEffect` calls in a typical codebase should not exist.
4. **Profile before memoizing** — React DevTools Profiler shows what actually re-renders and why. `useMemo` on a cheap computation costs more than it saves.
5. **Make the dependencies honest** — Never silence the exhaustive-deps lint rule. If the array is wrong, the bug is a stale closure, and it will be intermittent.

## Best Practices

- Derived state is a bug. If a value can be computed from props or other state, compute it during render.
- `useEffect` is for synchronizing with something outside React: a subscription, a DOM API, a timer. It is not for reacting to state changes.
- Every effect that subscribes must return a cleanup function. Missing cleanup is the standard cause of memory leaks and duplicate listeners.
- Do not put a non-stable key on a list. Index keys break every time the list is reordered or filtered.
- Context re-renders every consumer when its value changes. Split contexts by update frequency, or use an external store with selectors.
- Lift state up only as far as needed. State in the root component re-renders the tree.

## Examples

**An effect that should not exist:**

```jsx
// Wrong: derived state, an extra render, and a chance to be out of sync.
function Cart({ items }) {
  const [total, setTotal] = useState(0);
  useEffect(() => {
    setTotal(items.reduce((sum, i) => sum + i.price * i.qty, 0));
  }, [items]);
  return <Total value={total} />;
}

// Right: compute it during render. It is always correct, by construction.
function Cart({ items }) {
  const total = items.reduce((sum, i) => sum + i.price * i.qty, 0);
  return <Total value={total} />;
}
```

**Server state belongs in a query, not in `useState` plus `useEffect`:**

```jsx
function OrderList({ status }) {
  const { data, isPending, error } = useQuery({
    queryKey: ["orders", status],
    queryFn: ({ signal }) => fetchOrders(status, { signal }),
    staleTime: 30_000,
  });

  if (isPending) return <Skeleton />;
  if (error) return <ErrorState error={error} onRetry={() => refetch()} />;
  return <List items={data} />;
}
```

The manual version needs loading state, error state, cancellation on unmount, a race-condition guard when `status` changes mid-flight, and a cache. That is what the library is.

## Notes

- The React Compiler (React 19) auto-memoizes and removes most hand-written `useMemo` and `useCallback`. Do not spend effort on memoization you are about to delete.
- Strict Mode in development intentionally double-invokes effects to surface missing cleanup. An effect that breaks under Strict Mode is broken in production too — it just fails less often.
- `key` on a component is the idiomatic way to reset its state when an identity changes. It is far cleaner than an effect that resets fields.
