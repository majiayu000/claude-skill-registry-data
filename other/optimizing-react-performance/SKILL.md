---
name: optimizing-react-performance
description: React performance optimization. Identify unnecessary renders, apply memo/useCallback/useMemo correctly.
type: pattern
tier: library
domains: [frontend]
trigger: "performance, render, memo, useMemo, useCallback, slow, laggy, optimization"
---

## Profile First — Never Optimize Blindly

```tsx
// 1. Enable React DevTools Profiler
// 2. Record the slow interaction
// 3. Find components with long render times

// Rule: Only optimize what the profiler shows as slow
```

## The Three Memoization Tools

### React.memo — Prevent Child Re-renders

```tsx
// Without memo: re-renders whenever parent re-renders (even same props)
const ExpensiveList = React.memo(({ items, onItemClick }) => {
  return items.map(item => (
    <Item key={item.id} item={item} onClick={onItemClick} />
  ));
});

// Only re-renders when items or onItemClick reference changes
```

### useCallback — Stable Function References

```tsx
// Without useCallback: new function reference every render → breaks React.memo
const Parent = () => {
  const [count, setCount] = useState(0);

  // BAD: new reference every render
  const handleClick = (id) => console.log(id);

  // GOOD: stable reference (only changes if count changes)
  const handleClick = useCallback((id) => {
    console.log(id, count);
  }, [count]);

  return <ExpensiveList onItemClick={handleClick} />;
};
```

### useMemo — Expensive Computations

```tsx
// Only use useMemo for genuinely expensive calculations
const sortedAndFilteredItems = useMemo(() => {
  return items
    .filter(item => item.active)
    .sort((a, b) => b.priority - a.priority);
}, [items]); // only recalculate when items changes
```

## Anti-Patterns

```tsx
// Anti-pattern 1: Premature optimization
const name = useMemo(() => `${first} ${last}`, [first, last]);
// String concatenation is instant — useMemo adds overhead here

// Anti-pattern 2: Object in deps breaks memoization
const options = { limit: 10 };
const result = useMemo(() => fetchData(options), [options]);
// options is a new object every render! Memoization is pointless.

// Fix: primitives in deps
const result = useMemo(() => fetchData({ limit }), [limit]);
```

## Virtualization for Long Lists

```tsx
// Don't render 10,000 items in the DOM
import { FixedSizeList } from 'react-window';

const VirtualList = ({ items }) => (
  <FixedSizeList height={600} width="100%" itemCount={items.length} itemSize={50}>
    {({ index, style }) => (
      <div style={style}>{items[index].name}</div>
    )}
  </FixedSizeList>
);
```

## State Colocation

```tsx
// Don't put state in parent if only child needs it
// BAD: every sibling re-renders when modalOpen changes
const Parent = () => {
  const [modalOpen, setModalOpen] = useState(false);
  return (
    <>
      <HeavyComponent />  {/* re-renders on every modal toggle */}
      <Modal open={modalOpen} onClose={() => setModalOpen(false)} />
    </>
  );
};

// GOOD: colocate state
const ModalWithState = () => {
  const [open, setOpen] = useState(false);
  return <Modal open={open} onClose={() => setOpen(false)} />;
};
const Parent = () => (
  <>
    <HeavyComponent />  {/* never re-renders for modal */}
    <ModalWithState />
  </>
);
```

## Quick Wins Checklist

- [ ] Add keys to all lists (use stable IDs, not array index)
- [ ] Lazy-load heavy components: `const Chart = lazy(() => import('./Chart'))`
- [ ] Code-split routes (Next.js does this automatically)
- [ ] Move static values outside component body
- [ ] Use virtualization for lists > 100 items
