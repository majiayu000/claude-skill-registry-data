---
name: react-frontend
description: React frontend standards covering hooks (useState, useEffect, useContext, custom hooks), state management (Context API, Redux, Zustand), performance optimization (memoization, lazy loading, code splitting), testing with React Testing Library, and accessibility (WCAG 2.1, ARIA) for modern SPAs
---

# React Frontend Development Standards

## Quick Reference

### Essential Hooks

```tsx
// State Hook
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);

// Effect Hook
useEffect(() => {
  // Side effect
  return () => {/* cleanup */};
}, [dependencies]);

// Context Hook
const theme = useContext(ThemeContext);

// Ref Hook
const inputRef = useRef<HTMLInputElement>(null);

// Memo Hooks
const value = useMemo(() => expensiveCalc(a, b), [a, b]);
const callback = useCallback(() => doSomething(a), [a]);
```

### State Management Decision Tree

```
Is state needed in >2 components?
  NO  -> Use local state (useState)
  YES -> Is it global UI state (theme, auth)?
    YES -> Use Context API
    NO  -> Is it server data (API responses)?
      YES -> Use React Query/TanStack Query
      NO  -> Complex state with many actions?
        YES -> Use Redux Toolkit or Zustand
        NO  -> Use Context API + useReducer
```

### Component Checklist

- [ ] Use functional components with hooks
- [ ] Destructure props with TypeScript types
- [ ] Use semantic HTML elements
- [ ] Add proper ARIA labels where needed
- [ ] Memoize expensive computations with useMemo
- [ ] Memoize callbacks passed to children with useCallback
- [ ] Add loading and error states
- [ ] Clean up effects with return function
- [ ] Keep components under 300 lines

### Performance Checklist

- [ ] Use React.lazy() for code splitting
- [ ] Wrap expensive components in React.memo()
- [ ] Implement virtual scrolling for long lists
- [ ] Lazy load images with loading="lazy"
- [ ] Avoid inline object/array creation in JSX

### Quick Start

```bash
# Create React app with TypeScript
npx create-react-app my-app --template typescript

# Install testing library
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Install React Query for server state
npm install @tanstack/react-query

# State management (choose one)
npm install zustand          # Lightweight
npm install @reduxjs/toolkit # Enterprise
```

---

## Core Hooks Patterns

### useState

```tsx
// Lazy initialization for expensive initial state
const [data, setData] = useState(() => computeExpensiveValue());

// Functional updates when new state depends on old
setCount(prevCount => prevCount + 1);
```

### useEffect

```tsx
// Component mount (runs once)
useEffect(() => {
  console.log('Component mounted');
}, []);

// Cleanup pattern for async operations
useEffect(() => {
  let isMounted = true;

  async function fetchData() {
    const result = await api.getData();
    if (isMounted) setData(result);
  }

  fetchData();
  return () => { isMounted = false; };
}, []);

// Subscription cleanup
useEffect(() => {
  const subscription = api.subscribe(userId);
  return () => subscription.unsubscribe();
}, [userId]);
```

### useContext

```tsx
// Create context with TypeScript
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Custom hook for consuming context (always use this pattern)
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
};
```

### useReducer

```tsx
type Action = { type: 'increment' } | { type: 'decrement' } | { type: 'reset' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { count: state.count + 1 };
    case 'decrement': return { count: state.count - 1 };
    case 'reset': return { count: 0 };
    default: return state;
  }
}

const [state, dispatch] = useReducer(reducer, { count: 0 });
```

### Custom Hooks

```tsx
// Always prefix with 'use'
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let isMounted = true;

    fetch(url)
      .then(res => res.json())
      .then(data => { if (isMounted) { setData(data); setLoading(false); }})
      .catch(err => { if (isMounted) { setError(err); setLoading(false); }});

    return () => { isMounted = false; };
  }, [url]);

  return { data, loading, error };
}
```

---

## State Management

### Context API (Theme, Auth, Locale)

```tsx
// Split contexts to reduce re-renders
<AuthProvider>
  <ThemeProvider>
    <LocaleProvider>
      <App />
    </LocaleProvider>
  </ThemeProvider>
</AuthProvider>
```

### React Query (Server State)

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function Users() {
  const { data, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
}
```

### Zustand (Lightweight Global State)

```tsx
import create from 'zustand';

const useBearStore = create<BearState>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
}));

// Usage (no Provider needed!)
const bears = useBearStore((state) => state.bears);
```

---

## Performance Optimization

### React.memo

```tsx
const ExpensiveComponent = React.memo(({ data }: Props) => {
  return <div>{/* Expensive render */}</div>;
});
```

### Code Splitting

```tsx
const Home = lazy(() => import('./pages/Home'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Suspense>
  );
}
```

### Virtual Scrolling

```tsx
import { FixedSizeList } from 'react-window';

<FixedSizeList height={600} itemCount={10000} itemSize={35} width="100%">
  {({ index, style }) => <div style={style}>Row {index}</div>}
</FixedSizeList>
```

---

## Component Patterns

### Props with Defaults

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Button({ variant = 'primary', size = 'md', children }: ButtonProps) {
  return <button className={`btn-${variant} btn-${size}`}>{children}</button>;
}
```

### Compound Components

```tsx
const TabsContext = createContext<TabsContextType | undefined>(undefined);

export function Tabs({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState('tab1');
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.Tab = function Tab({ id, children }: TabProps) {
  const context = useContext(TabsContext);
  return (
    <button onClick={() => context?.setActiveTab(id)}>
      {children}
    </button>
  );
};
```

---

## Testing with React Testing Library

### User-Centric Testing

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('user can submit form', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();

  render(<ContactForm onSubmit={onSubmit} />);

  const nameInput = screen.getByRole('textbox', { name: /name/i });
  await user.type(nameInput, 'John Doe');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({ name: 'John Doe' });
  });
});
```

### Testing Hooks

```tsx
import { renderHook, act } from '@testing-library/react';

test('useCounter increments', () => {
  const { result } = renderHook(() => useCounter());
  expect(result.current.count).toBe(0);

  act(() => { result.current.increment(); });
  expect(result.current.count).toBe(1);
});
```

### Coverage Targets

- Components: 80%+
- Hooks: 90%+
- Utils: 95%+

---

## Accessibility (WCAG 2.1 AA)

### Semantic HTML

```tsx
<nav><ul><li><a href="/">Home</a></li></ul></nav>
<main><article><h1>Title</h1><section><h2>Section</h2></section></article></main>
<footer>&copy; 2024 Company</footer>
```

### ARIA and Keyboard Navigation

```tsx
<button aria-label="Close dialog" onClick={onClose}>X</button>

<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirm Action</h2>
</div>

<div role="alert" aria-live="assertive">{error}</div>
```

### Form Accessibility

```tsx
<label htmlFor="email">Email</label>
<input
  id="email"
  type="email"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : undefined}
/>
{errors.email && <span id="email-error" role="alert">{errors.email}</span>}
```

---

## Security

### XSS Prevention

```tsx
// React escapes by default - safe
<div>{userInput}</div>

// If dangerouslySetInnerHTML needed, use DOMPurify
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(dirtyHTML);
```

### Secure Token Storage

```tsx
// Prefer httpOnly cookies (backend sets it)
// If localStorage required: short expiry, refresh tokens, clear on logout
```

---

## Summary

1. **Hooks mastery** for state and side effects
2. **Appropriate state management** (local -> Context -> external library)
3. **Performance optimization** with memoization and code splitting
4. **User-centric testing** with React Testing Library
5. **Accessibility** (WCAG 2.1 AA) with semantic HTML and ARIA
6. **Security** through XSS prevention and secure auth patterns

---

## Resources

See [REFERENCE.md](./REFERENCE.md) for:

- Complete component templates
- Advanced hooks patterns (useReducer, usePrevious)
- Redux Toolkit implementation
- Compound component examples
- Comprehensive testing patterns
- Full accessibility checklists
- Production optimization examples
