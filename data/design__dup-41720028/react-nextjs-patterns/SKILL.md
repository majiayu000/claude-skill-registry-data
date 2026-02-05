---
name: react-nextjs-patterns
description: React and Next.js implementation patterns for performance and maintainability. Use when building frontend components, pages, and applications with React ecosystem.
---

This skill provides React and Next.js specific patterns for building performant, maintainable frontend applications.

## When to Invoke This Skill

Automatically activate for:
- React component implementation
- Next.js page and API routes
- State management patterns
- Performance optimization
- Server/Client component decisions

## Next.js App Router Patterns

### Server vs Client Components

```tsx
// Server Component (default) - data fetching, no interactivity
// app/users/page.tsx
export default async function UsersPage() {
  const users = await getUsers(); // Runs on server

  return (
    <div>
      <h1>Users</h1>
      <UserList users={users} />
    </div>
  );
}

// Client Component - interactivity required
// components/user-search.tsx
'use client';

import { useState } from 'react';

export function UserSearch({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('');

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyDown={(e) => e.key === 'Enter' && onSearch(query)}
    />
  );
}
```

### Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Fast data loads first */}
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection />
      </Suspense>

      {/* Slow data streams in */}
      <Suspense fallback={<ChartSkeleton />}>
        <AnalyticsChart />
      </Suspense>
    </div>
  );
}

// Async component that streams
async function StatsSection() {
  const stats = await getStats(); // Can be slow
  return <Stats data={stats} />;
}
```

### Data Fetching Patterns

```tsx
// Parallel data fetching
async function DashboardPage() {
  // Fetch in parallel, not sequentially
  const [users, orders, stats] = await Promise.all([
    getUsers(),
    getOrders(),
    getStats(),
  ]);

  return <Dashboard users={users} orders={orders} stats={stats} />;
}

// With error boundary
import { notFound } from 'next/navigation';

async function UserPage({ params }: { params: { id: string } }) {
  const user = await getUser(params.id);

  if (!user) {
    notFound(); // Renders not-found.tsx
  }

  return <UserProfile user={user} />;
}
```

## React Performance Patterns

### Component Decomposition

```tsx
// BAD: Large component with all state
function BadUserList() {
  const [filter, setFilter] = useState('');
  const [users, setUsers] = useState<User[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // All users re-render on any state change
  return (
    <div>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      {users.map(user => (
        <div
          key={user.id}
          onClick={() => setSelectedId(user.id)}
          className={selectedId === user.id ? 'selected' : ''}
        >
          {user.name}
        </div>
      ))}
    </div>
  );
}

// GOOD: Push state down to where it's needed
function GoodUserList() {
  const [users] = useState<User[]>([]);
  return <FilterableUserList users={users} />;
}

function FilterableUserList({ users }: { users: User[] }) {
  const [filter, setFilter] = useState('');
  const filtered = useMemo(
    () => users.filter(u => u.name.includes(filter)),
    [users, filter]
  );

  return (
    <div>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      <SelectableList users={filtered} />
    </div>
  );
}

function SelectableList({ users }: { users: User[] }) {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  return users.map(user => (
    <UserItem
      key={user.id}
      user={user}
      selected={selectedId === user.id}
      onSelect={() => setSelectedId(user.id)}
    />
  ));
}
```

### Memoization Strategies

```tsx
// Only memo when there's a measurable benefit
const UserItem = memo(function UserItem({
  user,
  selected,
  onSelect
}: {
  user: User;
  selected: boolean;
  onSelect: () => void;
}) {
  return (
    <div
      onClick={onSelect}
      className={selected ? 'selected' : ''}
    >
      {user.name}
    </div>
  );
});

// useMemo for expensive computations
function ExpensiveList({ items }: { items: Item[] }) {
  const processed = useMemo(() => {
    return items
      .filter(complexFilter)
      .sort(complexSort)
      .map(complexTransform);
  }, [items]);

  return <List items={processed} />;
}

// useCallback for stable references passed to children
function Parent() {
  const [items, setItems] = useState<Item[]>([]);

  const handleDelete = useCallback((id: string) => {
    setItems(prev => prev.filter(item => item.id !== id));
  }, []);

  return <ItemList items={items} onDelete={handleDelete} />;
}
```

## State Management Patterns

### Context with Reducer

```tsx
// types
interface State {
  user: User | null;
  isLoading: boolean;
  error: Error | null;
}

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; user: User }
  | { type: 'FETCH_ERROR'; error: Error }
  | { type: 'LOGOUT' };

// reducer
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, isLoading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, isLoading: false, user: action.user };
    case 'FETCH_ERROR':
      return { ...state, isLoading: false, error: action.error };
    case 'LOGOUT':
      return { ...state, user: null };
  }
}

// context
const AuthContext = createContext<{
  state: State;
  dispatch: Dispatch<Action>;
} | null>(null);

// provider
function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, {
    user: null,
    isLoading: true,
    error: null,
  });

  return (
    <AuthContext.Provider value={{ state, dispatch }}>
      {children}
    </AuthContext.Provider>
  );
}

// hook
function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### Custom Hooks

```tsx
// Data fetching hook
function useQuery<T>(
  key: string,
  fetcher: () => Promise<T>
): { data: T | null; isLoading: boolean; error: Error | null; refetch: () => void } {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await fetcher();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, [fetcher]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, isLoading, error, refetch: fetchData };
}

// Debounced value hook
function useDebouncedValue<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}

// Local storage hook
function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue;
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((prev: T) => T)) => {
    setStoredValue(prev => {
      const newValue = value instanceof Function ? value(prev) : value;
      localStorage.setItem(key, JSON.stringify(newValue));
      return newValue;
    });
  }, [key]);

  return [storedValue, setValue];
}
```

## Component Patterns

### Compound Components

```tsx
// Flexible API with compound components
const Tabs = ({ children, defaultValue }: { children: ReactNode; defaultValue: string }) => {
  const [activeTab, setActiveTab] = useState(defaultValue);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
};

Tabs.List = function TabsList({ children }: { children: ReactNode }) {
  return <div className="tabs-list">{children}</div>;
};

Tabs.Tab = function Tab({ value, children }: { value: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button
      className={activeTab === value ? 'active' : ''}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function TabsPanel({ value, children }: { value: string; children: ReactNode }) {
  const { activeTab } = useTabsContext();
  if (activeTab !== value) return null;
  return <div className="tabs-panel">{children}</div>;
};

// Usage
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Tab value="tab1">Tab 1</Tabs.Tab>
    <Tabs.Tab value="tab2">Tab 2</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="tab1">Content 1</Tabs.Panel>
  <Tabs.Panel value="tab2">Content 2</Tabs.Panel>
</Tabs>
```

### Render Props & Children as Function

```tsx
// Data provider with render prop
function DataProvider<T>({
  fetcher,
  children,
}: {
  fetcher: () => Promise<T>;
  children: (data: T | null, isLoading: boolean) => ReactNode;
}) {
  const { data, isLoading } = useQuery('data', fetcher);
  return <>{children(data, isLoading)}</>;
}

// Usage
<DataProvider fetcher={getUsers}>
  {(users, isLoading) => (
    isLoading ? <Spinner /> : <UserList users={users} />
  )}
</DataProvider>
```

## Best Practices Checklist

- [ ] Use Server Components by default, Client Components only when needed
- [ ] Push state down to the lowest component that needs it
- [ ] Break large components into smaller, focused ones
- [ ] Use Suspense boundaries for async operations
- [ ] Memoize only when profiling shows benefit
- [ ] Create custom hooks for reusable stateful logic
- [ ] Use discriminated unions for component state
- [ ] Implement proper error boundaries
- [ ] Ensure accessibility (ARIA, keyboard navigation)
- [ ] Use proper loading and error states
