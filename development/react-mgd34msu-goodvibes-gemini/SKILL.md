---
name: react
description: Builds user interfaces with React using components, hooks, state management, and modern patterns. Use when creating React components, managing state, handling side effects, optimizing performance, or integrating with frameworks.
---

# React

Library for building user interfaces with components, declarative rendering, and hooks-based state management.

## Quick Start

**Create with Vite (recommended):**
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

**Or with a meta-framework:**
```bash
npx create-next-app@latest    # Next.js
npx create-remix@latest        # Remix
```

## Components

### Function Components

```tsx
// Basic component
function Greeting({ name }: { name: string }) {
  return <h1>Hello, {name}!</h1>;
}

// Arrow function with destructured props
const Button = ({ onClick, children }: {
  onClick: () => void;
  children: React.ReactNode;
}) => {
  return <button onClick={onClick}>{children}</button>;
};

// Usage
<Greeting name="World" />
<Button onClick={() => alert('Clicked!')}>Click me</Button>
```

### Props Interface Pattern

```tsx
interface CardProps {
  title: string;
  description?: string;
  children: React.ReactNode;
  variant?: 'default' | 'outlined';
}

function Card({ title, description, children, variant = 'default' }: CardProps) {
  return (
    <div className={`card card--${variant}`}>
      <h2>{title}</h2>
      {description && <p>{description}</p>}
      {children}
    </div>
  );
}
```

## JSX

### Expressions

```tsx
const name = 'React';
const items = ['Apple', 'Banana', 'Cherry'];

function App() {
  return (
    <div>
      {/* Variables */}
      <h1>{name}</h1>

      {/* Expressions */}
      <p>{2 + 2}</p>
      <p>{name.toUpperCase()}</p>

      {/* Conditional rendering */}
      {name && <p>Hello, {name}</p>}
      {items.length > 0 ? <List items={items} /> : <p>No items</p>}

      {/* Lists */}
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Fragments

```tsx
// Named fragment
import { Fragment } from 'react';

function List() {
  return (
    <Fragment>
      <li>Item 1</li>
      <li>Item 2</li>
    </Fragment>
  );
}

// Shorthand syntax
function List() {
  return (
    <>
      <li>Item 1</li>
      <li>Item 2</li>
    </>
  );
}
```

## Hooks

### useState

```tsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount((c) => c - 1)}>Decrement</button>
    </div>
  );
}

// With objects
const [user, setUser] = useState({ name: '', email: '' });
setUser((prev) => ({ ...prev, name: 'John' }));

// Lazy initialization
const [data, setData] = useState(() => expensiveComputation());
```

### useEffect

```tsx
import { useEffect, useState } from 'react';

function DataFetcher({ url }: { url: string }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      setLoading(true);
      const response = await fetch(url);
      const json = await response.json();

      if (!cancelled) {
        setData(json);
        setLoading(false);
      }
    }

    fetchData();

    // Cleanup function
    return () => {
      cancelled = true;
    };
  }, [url]); // Dependency array

  if (loading) return <p>Loading...</p>;
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
```

### useRef

```tsx
import { useRef, useEffect } from 'react';

function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Focus on mount
    inputRef.current?.focus();
  }, []);

  return <input ref={inputRef} type="text" />;
}

// Mutable ref (doesn't trigger re-render)
function Timer() {
  const countRef = useRef(0);

  useEffect(() => {
    const id = setInterval(() => {
      countRef.current += 1;
    }, 1000);
    return () => clearInterval(id);
  }, []);
}
```

### useMemo and useCallback

```tsx
import { useMemo, useCallback, useState } from 'react';

function ExpensiveList({ items, filter }: { items: Item[]; filter: string }) {
  // Memoize expensive computation
  const filteredItems = useMemo(() => {
    return items.filter((item) =>
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);

  // Memoize callback
  const handleClick = useCallback((id: string) => {
    console.log('Clicked:', id);
  }, []);

  return (
    <ul>
      {filteredItems.map((item) => (
        <ListItem key={item.id} item={item} onClick={handleClick} />
      ))}
    </ul>
  );
}
```

### useReducer

```tsx
import { useReducer } from 'react';

interface State {
  count: number;
  error: string | null;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset'; payload: number }
  | { type: 'error'; payload: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + 1 };
    case 'decrement':
      return { ...state, count: state.count - 1 };
    case 'reset':
      return { ...state, count: action.payload };
    case 'error':
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, error: null });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset', payload: 0 })}>Reset</button>
    </div>
  );
}
```

### useContext

```tsx
import { createContext, useContext, useState } from 'react';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Usage
function ThemedButton() {
  const { theme, toggleTheme } = useTheme();
  return (
    <button onClick={toggleTheme}>
      Current theme: {theme}
    </button>
  );
}
```

## Custom Hooks

```tsx
// useFetch
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url, { signal: controller.signal });
        if (!response.ok) throw new Error('Failed to fetch');
        const json = await response.json();
        setData(json);
      } catch (err) {
        if (err instanceof Error && err.name !== 'AbortError') {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchData();
    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}

// useLocalStorage
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

// useDebounce
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

## Event Handling

```tsx
function Form() {
  const [value, setValue] = useState('');

  // Input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
  };

  // Form submit
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Submitted:', value);
  };

  // Button click
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    console.log('Clicked at:', e.clientX, e.clientY);
  };

  // Keyboard
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      console.log('Enter pressed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
      />
      <button type="submit" onClick={handleClick}>
        Submit
      </button>
    </form>
  );
}
```

## Composition Patterns

### Children

```tsx
function Container({ children }: { children: React.ReactNode }) {
  return <div className="container">{children}</div>;
}

// Usage
<Container>
  <h1>Title</h1>
  <p>Content</p>
</Container>
```

### Render Props

```tsx
interface MousePosition {
  x: number;
  y: number;
}

function MouseTracker({
  render,
}: {
  render: (position: MousePosition) => React.ReactNode;
}) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent) => {
    setPosition({ x: e.clientX, y: e.clientY });
  };

  return <div onMouseMove={handleMouseMove}>{render(position)}</div>;
}

// Usage
<MouseTracker
  render={({ x, y }) => (
    <p>
      Mouse position: {x}, {y}
    </p>
  )}
/>
```

### Compound Components

```tsx
const TabsContext = createContext<{
  activeTab: string;
  setActiveTab: (tab: string) => void;
} | null>(null);

function Tabs({ children, defaultTab }: {
  children: React.ReactNode;
  defaultTab: string;
}) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');

  return (
    <button
      className={context.activeTab === id ? 'active' : ''}
      onClick={() => context.setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function TabPanels({ children }: { children: React.ReactNode }) {
  return <div className="tab-panels">{children}</div>;
}

function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabPanel must be used within Tabs');

  return context.activeTab === id ? <div>{children}</div> : null;
}

// Usage
<Tabs defaultTab="tab1">
  <TabList>
    <Tab id="tab1">Tab 1</Tab>
    <Tab id="tab2">Tab 2</Tab>
  </TabList>
  <TabPanels>
    <TabPanel id="tab1">Content 1</TabPanel>
    <TabPanel id="tab2">Content 2</TabPanel>
  </TabPanels>
</Tabs>
```

## Performance

### React.memo

```tsx
import { memo } from 'react';

interface ItemProps {
  item: { id: string; name: string };
  onClick: (id: string) => void;
}

const ListItem = memo(function ListItem({ item, onClick }: ItemProps) {
  console.log('Rendering:', item.name);
  return <li onClick={() => onClick(item.id)}>{item.name}</li>;
});

// With custom comparison
const ListItem = memo(
  function ListItem({ item, onClick }: ItemProps) {
    return <li onClick={() => onClick(item.id)}>{item.name}</li>;
  },
  (prevProps, nextProps) => {
    return prevProps.item.id === nextProps.item.id;
  }
);
```

### Lazy Loading

```tsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

## Error Boundaries

```tsx
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorPage />}>
  <MyComponent />
</ErrorBoundary>
```

## Best Practices

1. **Keep components small** - Single responsibility principle
2. **Lift state up** - Share state via common ancestor
3. **Use TypeScript** - Catch errors at compile time
4. **Memoize expensive operations** - useMemo, useCallback, memo
5. **Avoid inline objects/functions in JSX** - They cause re-renders
6. **Use keys correctly** - Unique, stable identifiers

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mutating state directly | Use spread operator or setState |
| Missing dependency in useEffect | Add all dependencies |
| Unnecessary useEffect | Derive state during render |
| Prop drilling | Use Context or state management |
| Not cleaning up effects | Return cleanup function |

## Reference Files

- [references/hooks.md](references/hooks.md) - Hooks deep dive
- [references/patterns.md](references/patterns.md) - Advanced patterns
- [references/performance.md](references/performance.md) - Optimization techniques
