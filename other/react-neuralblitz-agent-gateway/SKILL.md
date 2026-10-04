---
name: react
description: React development best practices and patterns
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: frameworks
---
## What I do
- Write modern React with hooks (useState, useEffect, useCallback, useMemo)
- Use TypeScript for type safety
- Follow component composition patterns
- Implement proper state management
- Handle forms with React Hook Form
- Use React Query for data fetching
- Optimize performance with memo and lazy loading
- Write integration tests with React Testing Library

## When to use me
When creating React components, hooks, or applications.

## Component Patterns
```typescript
import React, { useState, useCallback, useMemo } from 'react';

interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  onDelete?: (userId: string) => void;
  isSelected?: boolean;
}

export const UserCard: React.FC<UserCardProps> = ({
  user,
  onEdit,
  onDelete,
  isSelected = false,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleEdit = useCallback(() => {
    onEdit?.(user);
  }, [user, onEdit]);

  const handleDelete = useCallback(() => {
    onDelete?.(user.id);
  }, [user.id, onDelete]);

  return (
    <div className={`user-card ${isSelected ? 'selected' : ''}`}>
      <div className="user-header" onClick={() => setIsExpanded(!isExpanded)}>
        <img src={user.avatarUrl} alt={user.name} />
        <div>
          <h3>{user.name}</h3>
          <p>{user.email}</p>
        </div>
        <button onClick={handleEdit}>Edit</button>
        <button onClick={handleDelete} disabled={user.isProtected}>
          Delete
        </button>
      </div>

      {isExpanded && (
        <div className="user-details">
          <p>Role: {user.role}</p>
          <p>Created: {new Date(user.createdAt).toLocaleDateString()}</p>
        </div>
      )}
    </div>
  );
};

// Compound components
interface TabsProps {
  defaultTab: string;
  children: React.ReactNode;
}

export function Tabs({ defaultTab, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  const context = useMemo(() => ({ activeTab, setActiveTab }), [activeTab]);

  return <TabsContext.Provider value={context}>{children}</TabsContext.Provider>;
}

Tabs.Tab = function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  return (
    <button onClick={() => setActiveTab(id)} className={activeTab === id ? 'active' : ''}>
      {children}
    </button>
  );
};

Tabs.Panel = function Panel({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab } = useContext(TabsContext);
  return activeTab === id ? <div>{children}</div> : null;
};
```

## Custom Hooks
```typescript
import { useState, useEffect, useCallback } from 'react';

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}
```

## Performance Optimization
```typescript
// Use React.memo for component memoization
export const ExpensiveList = React.memo<ExpensiveListProps>(({ items, onSelect }) => {
  return (
    <ul>
      {items.map(item => (
        <ListItem key={item.id} item={item} onSelect={onSelect} />
      ))}
    </ul>
  );
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.items.length === nextProps.items.length;
});

// Use useMemo for expensive calculations
const sortedItems = useMemo(() => {
  return [...items].sort((a, b) => b.score - a.score);
}, [items]);

// Use useCallback for stable function references
const handleSelect = useCallback((id: string) => {
  onSelect(id);
}, [onSelect]);

// Lazy loading
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```
