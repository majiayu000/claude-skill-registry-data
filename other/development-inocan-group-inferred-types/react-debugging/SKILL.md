---
name: react-debugging
description: Debug React components, fix hooks errors, resolve TypeScript issues, handle state management bugs, and fix rendering problems. Use when encountering React errors, hooks violations, type errors, or component rendering issues.
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# React Component Debugging

Expert assistance for debugging React components and hooks in the MantisNXT Next.js project.

## Capabilities

- **Component Error Debugging**: Fix runtime errors in React components
- **Hooks Troubleshooting**: Resolve issues with useState, useEffect, useQuery, etc.
- **TypeScript Error Resolution**: Fix type mismatches and inference issues
- **State Management**: Debug Zustand stores and React Query caches
- **Rendering Issues**: Fix hydration errors, infinite loops, and performance problems

## Common Errors & Solutions

### "X.map is not a function"

**Cause**: Variable expected to be an array is not an array (undefined, null, or object)

**Solution**:
```typescript
// ❌ Unsafe
const items = data;
items.map(item => ...)

// ✅ Safe - ensure it's always an array
const items = Array.isArray(data) ? data : [];
items.map(item => ...)

// ✅ Alternative - provide default
const items = data || [];
const items = data ?? [];
```

### "Cannot read property 'X' of undefined"

**Cause**: Accessing property on undefined/null object

**Solution**:
```typescript
// ❌ Unsafe
const name = user.profile.name;

// ✅ Optional chaining
const name = user?.profile?.name;

// ✅ With default
const name = user?.profile?.name ?? 'Unknown';
```

### "Rendered more hooks than during previous render"

**Cause**: Conditional hooks usage violates Rules of Hooks

**Solution**:
```typescript
// ❌ Wrong - conditional hook
if (condition) {
  const [state, setState] = useState(0);
}

// ✅ Correct - hook always called
const [state, setState] = useState(0);
if (condition) {
  // use state here
}
```

### "Hydration failed"

**Cause**: Server-rendered HTML doesn't match client render

**Solution**:
```typescript
// ❌ Causes hydration mismatch
<div>{Math.random()}</div>

// ✅ Use client-only rendering
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);
if (!mounted) return null;

// ✅ Or mark component as client-side
'use client'
```

### "Maximum update depth exceeded"

**Cause**: Infinite loop in useEffect or state updates

**Solution**:
```typescript
// ❌ Wrong - infinite loop
useEffect(() => {
  setState(newValue); // triggers re-render → triggers effect again
});

// ✅ Correct - proper dependencies
useEffect(() => {
  setState(newValue);
}, [dependency]); // only runs when dependency changes
```

## React Query Issues

### Stale Data

```typescript
// Force refetch
const { data, refetch } = useQuery(...);
refetch();

// Invalidate cache
queryClient.invalidateQueries(['key']);

// Set stale time
useQuery(['key'], fetcher, {
  staleTime: 5 * 60 * 1000, // 5 minutes
});
```

### Loading States

```typescript
const { data, isLoading, error } = useQuery(...);

// ✅ Handle all states
if (isLoading) return <Loading />;
if (error) return <Error error={error} />;
if (!data) return <Empty />;

return <Content data={data} />;
```

## Component File Locations

```
src/
├── components/
│   ├── dashboard/         # Dashboard components
│   ├── suppliers/         # Supplier management
│   ├── spp/              # Supplier pricelist processing
│   ├── layout/           # Layout components
│   └── ui/               # Shadcn UI components
├── hooks/
│   └── useNeonSpp.ts     # React Query hooks
└── lib/
    ├── stores/           # Zustand stores
    └── services/         # API services
```

## Debugging Workflow

1. **Read the error message** carefully - it often tells you exactly what's wrong
2. **Check the stack trace** to find the exact line causing the issue
3. **Inspect the component** where the error occurs
4. **Verify data types** - ensure variables are what you expect (array vs object vs null)
5. **Check dependencies** - verify useEffect/useCallback dependencies are correct
6. **Add console.logs** strategically to track data flow
7. **Test incrementally** - fix one issue at a time

## Type Safety Best Practices

```typescript
// ✅ Define proper interfaces
interface Upload {
  upload_id: string;
  filename: string;
  status: string;
  row_count: number;
}

// ✅ Type hook data
const { data } = useQuery<Upload[]>(...);

// ✅ Ensure array type
const uploads = Array.isArray(data) ? data : [];

// ✅ Type props
interface Props {
  uploads: Upload[];
  onRefresh: () => void;
}
```

## Common Hook Patterns

### Safe Data Fetching

```typescript
const { data, isLoading, error } = useQuery(
  ['key'],
  fetchFn,
  {
    staleTime: 5 * 60 * 1000,
    retry: 3,
    onError: (err) => console.error(err)
  }
);

// Safely handle data
const items = Array.isArray(data) ? data : [];
```

### Conditional Effects

```typescript
useEffect(() => {
  if (!condition) return; // early exit

  // effect logic

  return () => {
    // cleanup
  };
}, [condition]);
```

### Memoization

```typescript
// Expensive computation
const result = useMemo(() => {
  return expensiveOperation(data);
}, [data]);

// Callback stability
const handleClick = useCallback(() => {
  doSomething(value);
}, [value]);
```

## Performance Optimization

- Use `React.memo` for expensive components
- Implement virtualization for long lists (react-window)
- Lazy load heavy components with `React.lazy`
- Debounce search inputs
- Optimize re-renders with proper dependency arrays

## Testing Components

```typescript
// Check component renders without errors
npm run dev
// Visit page in browser

// Type checking
npm run type-check

// Build check (catches many issues)
npm run build
```

## Best Practices

1. **Always handle loading and error states**
2. **Ensure data is the expected type** before using array/object methods
3. **Follow Rules of Hooks** - call hooks at top level, consistently
4. **Use TypeScript properly** - don't use `any`, define proper types
5. **Add null checks** for optional data
6. **Use optional chaining** (?.) and nullish coalescing (??)
7. **Test edge cases** - empty arrays, null values, loading states
8. **Keep components focused** - single responsibility
9. **Extract custom hooks** for reusable logic
10. **Clean up effects** - return cleanup functions
