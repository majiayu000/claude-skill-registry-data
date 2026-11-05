---
name: debugging-react-hooks
description: Debug React hooks infinite loops, stale closures, and missing dependencies. Systematic approach.
type: workflow
tier: library
domains: [frontend]
trigger: "infinite loop, useEffect, hook loop, re-render loop, missing dependency, stale closure"
---

## The Most Common Hook Bugs

### Bug 1: Infinite useEffect Loop

**Symptom:** Component re-renders endlessly, console floods with logs.

**Cause Pattern:**
```tsx
// BUG: object/array created in render → new reference every render
useEffect(() => {
  setData(processData(rawData));
}, [processData]); // processData re-created every render!
```

**Fix:**
```tsx
// Move stable values outside component, or use useCallback/useMemo
const processData = useCallback((data) => {
  return data.map(item => ({ ...item, processed: true }));
}, []); // empty deps = stable reference

useEffect(() => {
  setData(processData(rawData));
}, [processData, rawData]);
```

### Bug 2: Stale Closure

**Symptom:** Effect reads old state value. The count is always 0 in a timer.

```tsx
// BUG: count is captured at effect creation time (0)
useEffect(() => {
  const id = setInterval(() => {
    console.log(count); // always 0!
    setCount(count + 1); // always 1!
  }, 1000);
  return () => clearInterval(id);
}, []); // empty deps = stale closure
```

**Fix:**
```tsx
// Option A: functional update (doesn't need count in deps)
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1); // reads current value
  }, 1000);
  return () => clearInterval(id);
}, []);

// Option B: include count in deps (but re-registers interval)
useEffect(() => {
  const id = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(id);
}, [count]);
```

### Bug 3: Missing Dependency Warning → Incorrect Fix

**Bad fix:**
```tsx
// Silencing ESLint by disabling rule — WRONG
useEffect(() => {
  fetchUser(userId); // depends on userId but it's not in deps
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []);
```

**Correct fix:**
```tsx
useEffect(() => {
  fetchUser(userId);
}, [userId]); // proper dependency
```

## Debugging Checklist

1. **Add console.log to identify the loop:**
   ```tsx
   useEffect(() => {
     console.log('Effect ran, deps:', dep1, dep2);
   }, [dep1, dep2]);
   ```

2. **Check if a dep is an object/array:**
   ```tsx
   // Each render creates a new object! → new reference → triggers effect
   const options = { limit: 10 }; // bad
   const options = useMemo(() => ({ limit: 10 }), []); // good
   ```

3. **React DevTools Profiler:**
   - "Highlight updates when components render" — shows what's re-rendering

4. **Why Did You Render library:**
   ```
   npm install @welldone-software/why-did-you-render
   ```

## Rules of Hooks Compliance

- Only call hooks at the top level (not inside loops/conditions)
- Only call hooks from React functions
- Install `eslint-plugin-react-hooks` — let the linter catch issues
