---
name: hooks-best-practices
description: React Hooks patterns including custom hooks and dependency management. Use when implementing component logic.
---

# React Hooks Best Practices Skill

This skill covers React Hooks patterns, custom hooks, and dependency management.

## When to Use

Use this skill when:
- Writing custom hooks
- Managing component state
- Handling side effects
- Optimizing with memoization

## Core Principle

**EXTRACT AND REUSE** - Extract reusable logic into custom hooks. Keep components focused on rendering.

## Custom Hook Patterns

### Basic Custom Hook

```typescript
import { useState, useCallback } from 'react';

interface UseToggleReturn {
  value: boolean;
  toggle: () => void;
  setTrue: () => void;
  setFalse: () => void;
}

export function useToggle(initialValue = false): UseToggleReturn {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue((v) => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse };
}
```

### Data Fetching Hook

```typescript
import { useState, useEffect } from 'react';

interface UseQueryResult<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
  refetch: () => void;
}

export function useQuery<T>(
  queryFn: () => Promise<T>,
  deps: unknown[] = []
): UseQueryResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await queryFn();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, deps);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, error, isLoading, refetch: fetchData };
}
```

### Form Hook

```typescript
import { useState, useCallback, ChangeEvent, FormEvent } from 'react';

interface UseFormReturn<T> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  handleChange: (e: ChangeEvent<HTMLInputElement>) => void;
  handleSubmit: (onSubmit: (values: T) => void) => (e: FormEvent) => void;
  reset: () => void;
  setFieldValue: (field: keyof T, value: T[keyof T]) => void;
}

export function useForm<T extends Record<string, unknown>>(
  initialValues: T
): UseFormReturn<T> {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});

  const handleChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setValues((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  }, []);

  const handleSubmit = useCallback(
    (onSubmit: (values: T) => void) => (e: FormEvent) => {
      e.preventDefault();
      onSubmit(values);
    },
    [values]
  );

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
  }, [initialValues]);

  const setFieldValue = useCallback((field: keyof T, value: T[keyof T]) => {
    setValues((prev) => ({ ...prev, [field]: value }));
  }, []);

  return { values, errors, handleChange, handleSubmit, reset, setFieldValue };
}
```

## Dependency Array Management

### Correct Dependencies

```typescript
// ✅ All dependencies included
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// ✅ Stable callback with useCallback
const handleClick = useCallback(() => {
  onClick(id);
}, [onClick, id]);

useEffect(() => {
  document.addEventListener('click', handleClick);
  return () => document.removeEventListener('click', handleClick);
}, [handleClick]);
```

### Common Mistakes

```typescript
// ❌ Missing dependency
useEffect(() => {
  fetchUser(userId); // userId not in deps
}, []);

// ❌ Object/array causing infinite loops
useEffect(() => {
  doSomething(options); // options is new object each render
}, [options]);

// ✅ Fix: Use useMemo or extract values
const { page, limit } = options;
useEffect(() => {
  doSomething({ page, limit });
}, [page, limit]);
```

### Stable References

```typescript
// ❌ Function recreated each render
function Component({ onSave }: { onSave: (data: Data) => void }): React.ReactElement {
  useEffect(() => {
    const handler = () => onSave(data);
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [onSave, data]); // onSave might change
}

// ✅ Use useCallback in parent or useRef
function Component({ onSave }: { onSave: (data: Data) => void }): React.ReactElement {
  const onSaveRef = useRef(onSave);
  onSaveRef.current = onSave;

  useEffect(() => {
    const handler = () => onSaveRef.current(data);
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [data]); // Stable reference
}
```

## Effect Cleanup

### Subscription Cleanup

```typescript
useEffect(() => {
  const subscription = eventEmitter.subscribe(handleEvent);

  return () => {
    subscription.unsubscribe();
  };
}, [handleEvent]);
```

### Abort Controller for Fetch

```typescript
useEffect(() => {
  const controller = new AbortController();

  async function fetchData(): Promise<void> {
    try {
      const response = await fetch(url, { signal: controller.signal });
      const data = await response.json();
      setData(data);
    } catch (err) {
      if (err instanceof Error && err.name !== 'AbortError') {
        setError(err);
      }
    }
  }

  fetchData();

  return () => controller.abort();
}, [url]);
```

### Timer Cleanup

```typescript
useEffect(() => {
  const timerId = setInterval(() => {
    setCount((c) => c + 1);
  }, 1000);

  return () => clearInterval(timerId);
}, []);
```

## Memoization Patterns

### useMemo for Expensive Computations

```typescript
const sortedItems = useMemo(() => {
  return items.slice().sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

const filteredData = useMemo(() => {
  return data.filter((item) => item.status === filter);
}, [data, filter]);
```

### useCallback for Stable Functions

```typescript
// ✅ Stable function for child components
const handleSelect = useCallback((id: string) => {
  setSelectedId(id);
  onSelect?.(id);
}, [onSelect]);

// ✅ Stable function for effects
const fetchData = useCallback(async () => {
  const result = await api.getData(params);
  setData(result);
}, [params]);
```

### When NOT to Memoize

```typescript
// ❌ Premature optimization
const name = useMemo(() => `${firstName} ${lastName}`, [firstName, lastName]);

// ✅ Simple computation - no memoization needed
const name = `${firstName} ${lastName}`;

// ❌ Memoizing primitives
const isActive = useMemo(() => status === 'active', [status]);

// ✅ Direct comparison
const isActive = status === 'active';
```

## Hook Rules

1. **Only call at top level** - Not in loops, conditions, or nested functions
2. **Only call in React functions** - Components or custom hooks
3. **Start with 'use'** - Custom hook naming convention
4. **Keep hooks pure** - Same inputs = same outputs

```typescript
// ❌ Conditional hook call
function Component({ shouldFetch }: { shouldFetch: boolean }): React.ReactElement {
  if (shouldFetch) {
    const data = useQuery(fetchData); // Error!
  }
}

// ✅ Always call, conditionally use
function Component({ shouldFetch }: { shouldFetch: boolean }): React.ReactElement {
  const data = useQuery(fetchData, { enabled: shouldFetch });
}
```

## Testing Custom Hooks

```typescript
import { renderHook, act } from '@testing-library/react';
import { useToggle } from '../useToggle';

describe('useToggle', () => {
  it('initializes with false by default', () => {
    const { result } = renderHook(() => useToggle());

    expect(result.current.value).toBe(false);
  });

  it('toggles value', () => {
    const { result } = renderHook(() => useToggle());

    act(() => {
      result.current.toggle();
    });

    expect(result.current.value).toBe(true);
  });
});
```

## Best Practices Summary

1. **Extract reusable logic** - Create custom hooks
2. **Include all dependencies** - Let ESLint guide you
3. **Use stable references** - useCallback, useMemo, useRef
4. **Clean up effects** - Return cleanup function
5. **Avoid premature memoization** - Profile first
6. **Name with 'use' prefix** - Convention for custom hooks
7. **Keep hooks focused** - Single responsibility

## Notes

- Use TanStack Query for data fetching (better than custom hooks)
- Use Zustand/Jotai for global state (instead of Context + hooks)
- Consider React 19's use() hook for promises and context
