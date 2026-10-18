---
name: react-builder
description: "Build scalable React applications with proper component architecture, custom hooks, state management, and performance optimization."
category: frontend
tags: [react, javascript, typescript, components, hooks]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# React Application Builder

## Purpose
Build production React applications with clean component architecture, reusable hooks, and optimal performance.

## Project Structure
```
src/
├── components/
│   ├── ui/              # Reusable UI components (Button, Input, Modal)
│   └── features/        # Feature-specific components
├── hooks/               # Custom hooks
├── services/            # API calls
├── stores/              # State management (Zustand)
├── utils/               # Utilities
└── types/               # TypeScript types
```

## Component Patterns
```tsx
// Compound component pattern
const Select = ({ children, value, onChange }: SelectProps) => {
  return (
    <SelectContext.Provider value={{ value, onChange }}>
      <div className="select-container">{children}</div>
    </SelectContext.Provider>
  );
};

Select.Option = ({ value, children }: OptionProps) => {
  const { value: selected, onChange } = useSelectContext();
  return (
    <div
      role="option"
      aria-selected={selected === value}
      onClick={() => onChange(value)}
    >
      {children}
    </div>
  );
};

// Usage
<Select value={city} onChange={setCity}>
  <Select.Option value="nyc">New York</Select.Option>
  <Select.Option value="la">Los Angeles</Select.Option>
</Select>
```

## Custom Hooks
```tsx
// Data fetching hook with caching
function usePost(id: string) {
  const [state, setState] = useState<{
    data: Post | null;
    loading: boolean;
    error: Error | null;
  }>({ data: null, loading: true, error: null });

  useEffect(() => {
    const controller = new AbortController();
    
    api.getPost(id, controller.signal)
      .then(data => setState({ data, loading: false, error: null }))
      .catch(error => {
        if (!controller.signal.aborted) {
          setState({ data: null, loading: false, error });
        }
      });
    
    return () => controller.abort();
  }, [id]);

  return state;
}
```

## Performance
```tsx
// Memoization
const ExpensiveComponent = memo(({ data }: Props) => {
  const processed = useMemo(() => processData(data), [data]);
  const handleClick = useCallback(() => doSomething(data), [data]);
  return <div onClick={handleClick}>{processed}</div>;
});

// Lazy loading
const HeavyChart = lazy(() => import('./HeavyChart'));

<Suspense fallback={<ChartSkeleton />}>
  <HeavyChart data={data} />
</Suspense>
```

## Outputs
1. Component library structure
2. Custom hooks for data fetching, forms, auth
3. State management setup (Zustand/React Query)
4. Performance optimization patterns
5. Testing setup with React Testing Library
