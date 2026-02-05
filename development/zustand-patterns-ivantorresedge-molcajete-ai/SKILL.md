---
name: zustand-patterns
description: Zustand state management patterns. Use when implementing client-side state with Zustand.
---

# Zustand Patterns Skill

This skill covers Zustand state management patterns for React applications.

## When to Use

Use this skill when:
- Managing global client state
- Implementing authentication state
- Creating shopping cart functionality
- Building theme/settings management

## Core Principle

**SIMPLE BY DEFAULT** - Zustand is minimal. Keep stores focused and use selectors for performance.

## Basic Store

```typescript
import { create } from 'zustand';

interface CounterState {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

export const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

// Usage
function Counter(): React.ReactElement {
  const count = useCounterStore((state) => state.count);
  const increment = useCounterStore((state) => state.increment);

  return (
    <button onClick={increment}>Count: {count}</button>
  );
}
```

## Typed Store with Actions

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: { email: string; password: string }) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,

  login: async (credentials) => {
    set({ isLoading: true });
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
      const user = await response.json();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch {
      set({ isLoading: false });
      throw new Error('Login failed');
    }
  },

  logout: () => {
    set({ user: null, isAuthenticated: false });
  },

  setUser: (user) => {
    set({ user, isAuthenticated: true });
  },
}));
```

## Selectors for Performance

```typescript
// ❌ Re-renders on any state change
function Component(): React.ReactElement {
  const store = useAuthStore(); // Subscribes to entire store
  return <span>{store.user?.name}</span>;
}

// ✅ Re-renders only when user changes
function Component(): React.ReactElement {
  const user = useAuthStore((state) => state.user);
  return <span>{user?.name}</span>;
}

// ✅ Multiple selectors
function Component(): React.ReactElement {
  const user = useAuthStore((state) => state.user);
  const isLoading = useAuthStore((state) => state.isLoading);
  return isLoading ? <Loading /> : <span>{user?.name}</span>;
}

// ✅ Computed selector
function Component(): React.ReactElement {
  const userName = useAuthStore((state) => state.user?.name ?? 'Guest');
  return <span>{userName}</span>;
}
```

## Middleware

### Persist Middleware

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface SettingsState {
  theme: 'light' | 'dark';
  language: string;
  setTheme: (theme: 'light' | 'dark') => void;
  setLanguage: (language: string) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'en',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'settings-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        theme: state.theme,
        language: state.language,
      }),
    }
  )
);
```

### DevTools Middleware

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export const useStore = create<StoreState>()(
  devtools(
    (set) => ({
      // state and actions
    }),
    { name: 'MyStore' }
  )
);
```

### Combined Middleware

```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

export const useStore = create<StoreState>()(
  devtools(
    persist(
      (set) => ({
        // state and actions
      }),
      { name: 'storage-key' }
    ),
    { name: 'DevToolsName' }
  )
);
```

## Slices Pattern

Split large stores into slices:

```typescript
// slices/userSlice.ts
import { StateCreator } from 'zustand';

export interface UserSlice {
  user: User | null;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const createUserSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  UserSlice
> = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
});

// slices/cartSlice.ts
export interface CartSlice {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
}

export const createCartSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  CartSlice
> = (set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({
    items: state.items.filter((item) => item.id !== id),
  })),
  clearCart: () => set({ items: [] }),
});

// store.ts
import { create } from 'zustand';
import { createUserSlice, UserSlice } from './slices/userSlice';
import { createCartSlice, CartSlice } from './slices/cartSlice';

type StoreState = UserSlice & CartSlice;

export const useStore = create<StoreState>()((...a) => ({
  ...createUserSlice(...a),
  ...createCartSlice(...a),
}));
```

## Async Actions

```typescript
interface TodoState {
  todos: Todo[];
  isLoading: boolean;
  error: string | null;
  fetchTodos: () => Promise<void>;
  addTodo: (text: string) => Promise<void>;
}

export const useTodoStore = create<TodoState>((set, get) => ({
  todos: [],
  isLoading: false,
  error: null,

  fetchTodos: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('/api/todos');
      const todos = await response.json();
      set({ todos, isLoading: false });
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch',
        isLoading: false,
      });
    }
  },

  addTodo: async (text) => {
    const optimisticTodo: Todo = {
      id: crypto.randomUUID(),
      text,
      completed: false,
    };

    // Optimistic update
    set((state) => ({ todos: [...state.todos, optimisticTodo] }));

    try {
      const response = await fetch('/api/todos', {
        method: 'POST',
        body: JSON.stringify({ text }),
      });
      const savedTodo = await response.json();

      // Replace optimistic with real
      set((state) => ({
        todos: state.todos.map((t) =>
          t.id === optimisticTodo.id ? savedTodo : t
        ),
      }));
    } catch {
      // Rollback on error
      set((state) => ({
        todos: state.todos.filter((t) => t.id !== optimisticTodo.id),
      }));
    }
  },
}));
```

## Testing Stores

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { useAuthStore } from '../authStore';

describe('authStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useAuthStore.setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
    });
  });

  it('sets user on login', async () => {
    const user = { id: '1', name: 'Test', email: 'test@test.com' };

    useAuthStore.getState().setUser(user);

    expect(useAuthStore.getState().user).toEqual(user);
    expect(useAuthStore.getState().isAuthenticated).toBe(true);
  });

  it('clears user on logout', () => {
    useAuthStore.setState({ user: { id: '1' }, isAuthenticated: true });

    useAuthStore.getState().logout();

    expect(useAuthStore.getState().user).toBeNull();
    expect(useAuthStore.getState().isAuthenticated).toBe(false);
  });
});
```

## Best Practices

1. **Use selectors** - Always select specific state
2. **Keep stores focused** - One concern per store
3. **Use TypeScript** - Full type safety
4. **Persist wisely** - Only persist what's needed
5. **Devtools in development** - Easier debugging
6. **Test store logic** - Unit test actions

## When NOT to Use Zustand

- Server state → Use TanStack Query
- Form state → Use React Hook Form
- URL state → Use router params
- Local component state → Use useState

## Notes

- Zustand is 1KB (smaller than Redux)
- No providers needed (unlike Context)
- Works outside React components
- Compatible with React 19
