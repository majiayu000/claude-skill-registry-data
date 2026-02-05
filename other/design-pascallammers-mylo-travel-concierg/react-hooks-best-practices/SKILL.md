---
name: React Hooks Best Practices
description: This skill should be used when the user asks to "review React hooks", "check useEffect usage", "optimize hooks performance", "design custom hooks", "refactor to use hooks", "remove unnecessary useEffect", "simplify useMemo usage", or discusses React hooks patterns. Provides guidance on writing minimal, effective React hooks code.
version: 0.1.0
---

# React Hooks Best Practices

This skill provides guidance for writing clean, efficient React hooks code with emphasis on **eliminating unnecessary hooks** and following established best practices.

## Core Philosophy: Less Is More

The primary principle is to use hooks only when necessary. Many React applications suffer from **hook overuse**, particularly:

- `useEffect` for logic that should be in event handlers
- `useMemo`/`useCallback` for cheap computations
- `useState` for derived state

Before adding any hook, ask: **"Can this be done without a hook?"**

## Mandatory Rules

### 1. Linter Compliance is Non-Negotiable

**Never suppress `react-hooks/exhaustive-deps` warnings.** The ESLint plugin understands React's rules better than manual reasoning. If a warning appears:

- Add missing dependencies
- Use functional updates to remove dependencies
- Restructure code to eliminate the need
- **Never use `// eslint-disable-next-line`**

### 2. Constants at Module Level, Not in Hooks

Never use `useMemo` for constant values. Define unchanging values at module scope:

```tsx
// ❌ WRONG: useMemo for constants
function Component() {
  const options = useMemo(() => [
    { value: 'a', label: 'Option A' },
    { value: 'b', label: 'Option B' },
  ], []);
}

// ✅ CORRECT: Module-level constants
const OPTIONS = [
  { value: 'a', label: 'Option A' },
  { value: 'b', label: 'Option B' },
] as const;

function Component() {
  // Just use OPTIONS directly
}
```

### 3. Custom Hook Returns Must Be Stable

All values returned from custom hooks must have stable references:

```tsx
// ❌ WRONG: Unstable return values
function useData(id: string) {
  const [data, setData] = useState(null);
  return {
    data,
    refresh: () => fetch(id),  // New function every render
    meta: { id },              // New object every render
  };
}

// ✅ CORRECT: All returns memoized or stable
function useData(id: string) {
  const [data, setData] = useState(null);

  const refresh = useCallback(() => fetch(id), [id]);
  const meta = useMemo(() => ({ id }), [id]);

  return { data, refresh, meta };
}
```

### 4. Prefer Modern Hooks When Available

Use experimental/newer hooks when React version permits:

| Hook | Purpose | Replaces |
|------|---------|----------|
| `useEffectEvent` | Stable event callbacks in effects | `useRef` + manual sync |
| `use` | Read resources in render | `useEffect` + `useState` |
| `useOptimistic` | Optimistic UI updates | Manual state management |
| `useFormStatus` | Form submission state | Custom loading state |

### 5. Prefer Suspense for Async Operations

Prefer React Suspense boundaries over manual loading state management:

```tsx
// ❌ AVOID: Manual loading state in component
function UserProfile({ userId }: Props) {
  const { data, isLoading, error } = useUser(userId);

  if (isLoading) return <Spinner />;
  if (error) return <ErrorDisplay error={error} />;
  return <Profile user={data} />;
}

// ✅ PREFER: Suspense boundary with data hook
function UserProfile({ userId }: Props) {
  const user = useUser(userId); // Suspends until ready
  return <Profile user={user} />;
}

// Parent handles loading/error
<ErrorBoundary fallback={<ErrorDisplay />}>
  <Suspense fallback={<Spinner />}>
    <UserProfile userId={id} />
  </Suspense>
</ErrorBoundary>
```

**Note**: Internal hook implementations may still use `{ data, error, loading }` structures. The preference for Suspense applies to component-level API design.

## Quick Decision Framework

### When NOT to Use useEffect

| Scenario | Wrong Approach | Correct Approach |
|----------|---------------|------------------|
| Transform data for rendering | `useEffect` + `useState` | Calculate during render |
| Respond to user event | `useEffect` watching state | Event handler directly |
| Initialize from props | `useEffect` syncing props | Compute in render or use key |
| Fetch on mount only | `useEffect` with `[]` | Use data fetching library |

### When NOT to Use useMemo/useCallback

| Scenario | Skip Memoization When... |
|----------|--------------------------|
| Simple calculations | Operation is O(1) or simple array methods |
| Non-object returns | Returning primitives (string, number, boolean) |
| No child optimization | Child components don't use `React.memo` |
| Development phase | Premature optimization without profiling |

## Essential Patterns

### 1. Derived State: Calculate, Don't Store

```tsx
// ❌ Anti-pattern: Storing derived state
const [items, setItems] = useState<Item[]>([]);
const [filteredItems, setFilteredItems] = useState<Item[]>([]);

useEffect(() => {
  setFilteredItems(items.filter(item => item.active));
}, [items]);

// ✅ Correct: Calculate during render
const [items, setItems] = useState<Item[]>([]);
const filteredItems = items.filter(item => item.active);
```

### 2. Event Responses: Use Handlers, Not Effects

```tsx
// ❌ Anti-pattern: Effect watching state
const [query, setQuery] = useState('');

useEffect(() => {
  if (query) {
    analytics.track('search', { query });
  }
}, [query]);

// ✅ Correct: Track in event handler
const handleSearch = (newQuery: string) => {
  setQuery(newQuery);
  if (newQuery) {
    analytics.track('search', { query: newQuery });
  }
};
```

### 3. Parent-Child Communication

```tsx
// ❌ Anti-pattern: Effect to notify parent
useEffect(() => {
  onChange(internalValue);
}, [internalValue, onChange]);

// ✅ Correct: Call during event
const handleChange = (value: string) => {
  setInternalValue(value);
  onChange(value);
};
```

### 4. Initialization from Props

```tsx
// ❌ Anti-pattern: Sync props to state
const [value, setValue] = useState(initialValue);

useEffect(() => {
  setValue(initialValue);
}, [initialValue]);

// ✅ Correct: Use key to reset
<Editor key={documentId} initialValue={initialValue} />
```

## Legitimate useEffect Use Cases

Effects are appropriate for:

1. **External system synchronization** (DOM manipulation, third-party libraries)
2. **Subscriptions** (WebSocket, event listeners, observers)
3. **Data fetching** (when not using a data library)

```tsx
// ✅ Legitimate: External system sync
useEffect(() => {
  const map = new MapLibrary(mapRef.current);
  map.setCenter(coordinates);

  return () => map.destroy();
}, [coordinates]);

// ✅ Legitimate: Subscription
useEffect(() => {
  const unsubscribe = store.subscribe(handleChange);
  return unsubscribe;
}, []);
```

## Performance Optimization Strategy

### Step 1: Measure First

Never optimize without profiling. Use React DevTools Profiler to identify actual bottlenecks.

### Step 2: Structural Solutions Before Memoization

Try these before adding `useMemo`/`useCallback`:

- **Lift state down**: Move state closer to where it's used
- **Extract components**: Isolate frequently updating parts
- **Use children prop**: Pass static JSX as children

### Step 3: Memoize Strategically

When memoization is needed:

```tsx
// Memoize expensive computations
const sortedData = useMemo(
  () => data.toSorted((a, b) => complexSort(a, b)),
  [data]
);

// Memoize callbacks for optimized children
const handleClick = useCallback(
  (id: string) => dispatch({ type: 'SELECT', id }),
  [dispatch]
);

// Combine with React.memo for child optimization
const MemoizedChild = memo(function Child({ onClick }: Props) {
  return <button onClick={onClick}>Click</button>;
});
```

## Custom Hook Design Principles

### Single Responsibility

Each custom hook should do one thing well:

```tsx
// ✅ Focused hooks
function useLocalStorage<T>(key: string, initial: T) { /* ... */ }
function useDebounce<T>(value: T, delay: number) { /* ... */ }
function useMediaQuery(query: string) { /* ... */ }
```

### Return Type Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| Tuple `[value, setter]` | State-like API | `useState`, `useLocalStorage` |
| Object `{ data, error, loading }` | Multiple related values | `useFetch`, `useQuery` |
| Single value | Read-only derived data | `useMediaQuery`, `useOnline` |

### Composition Over Complexity

Build complex behavior from simple hooks:

```tsx
function useSearchWithDebounce(initialQuery: string) {
  const [query, setQuery] = useState(initialQuery);
  const debouncedQuery = useDebounce(query, 300);
  const results = useSearch(debouncedQuery);

  return { query, setQuery, results };
}
```

## Common Mistakes at a Glance

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| `useState` + `useEffect` for filtering | Extra render, sync bugs | Calculate during render |
| `useMemo(() => CONSTANT, [])` | Unnecessary overhead | Module-level constant |
| `// eslint-disable-next-line` | Hides real bugs | Fix the dependency issue |
| Unstable custom hook returns | Breaks consumer memoization | Memoize all non-primitives |
| `useEffect` for analytics on click | Delayed, indirect | Track in click handler |
| Manual loading/error state | Boilerplate, race conditions | Suspense + ErrorBoundary |

## Code Review Checklist

When reviewing React hooks code, verify:

**Mandatory (Zero Tolerance)**
- [ ] No ESLint `exhaustive-deps` warnings suppressed
- [ ] No `useMemo` for constant values (use module-level)
- [ ] All custom hook returns are stable (memoized or primitives)

**Anti-Patterns**
- [ ] No `useEffect` for derived state calculations
- [ ] No `useEffect` for event response logic
- [ ] No `useState` for values computable from other state/props
- [ ] No `useMemo`/`useCallback` without proven performance need

**Quality**
- [ ] Dependencies arrays are complete and accurate
- [ ] Custom hooks follow single responsibility principle
- [ ] Cleanup functions provided where needed
- [ ] Modern hooks used where React version permits

## Additional Resources

### Reference Files

For detailed guidance and examples, consult:

- **`references/unnecessary-hooks.md`** - Comprehensive patterns for eliminating unnecessary hooks with before/after examples
- **`references/custom-hooks.md`** - Advanced custom hook design patterns and composition strategies
- **`references/dependency-array.md`** - Deep dive into dependency array management and common pitfalls

### Example Files

Working examples in `examples/`:

- **`good-patterns.tsx`** - Correct hook usage examples
- **`anti-patterns.tsx`** - Common mistakes with corrections

## Summary

The goal is writing React code that is:

1. **Minimal**: Use hooks only when necessary
2. **Direct**: Prefer event handlers over effects
3. **Calculated**: Derive values during render when possible
4. **Measured**: Optimize based on profiling, not assumptions

Apply the principle: **"The best hook is the one you don't need to write."**
