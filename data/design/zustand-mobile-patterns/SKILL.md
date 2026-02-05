---
name: zustand-mobile-patterns
description: Zustand state management for React Native. Use when implementing client-side state.
---

# Zustand Mobile Patterns Skill

This skill covers Zustand state management for React Native apps.

## When to Use

Use this skill when:
- Managing global client state
- Authentication state
- User preferences/settings
- Shopping cart
- Theme management

## Core Principle

**SIMPLE AND MINIMAL** - Zustand is lightweight. Keep stores focused.

## Installation

```bash
npm install zustand
```

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
    <TouchableOpacity onPress={increment}>
      <Text>Count: {count}</Text>
    </TouchableOpacity>
  );
}
```

## Authentication Store

```typescript
import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loadStoredAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (email, password) => {
    set({ isLoading: true });
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) throw new Error('Login failed');

      const { user, token } = await response.json();

      await SecureStore.setItemAsync('authToken', token);
      await SecureStore.setItemAsync('user', JSON.stringify(user));

      set({ user, token, isAuthenticated: true, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  logout: async () => {
    await SecureStore.deleteItemAsync('authToken');
    await SecureStore.deleteItemAsync('user');
    set({ user: null, token: null, isAuthenticated: false });
  },

  loadStoredAuth: async () => {
    try {
      const token = await SecureStore.getItemAsync('authToken');
      const userStr = await SecureStore.getItemAsync('user');

      if (token && userStr) {
        const user = JSON.parse(userStr);
        set({ user, token, isAuthenticated: true, isLoading: false });
      } else {
        set({ isLoading: false });
      }
    } catch {
      set({ isLoading: false });
    }
  },
}));
```

## Settings Store with Persistence

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface SettingsState {
  theme: 'light' | 'dark' | 'system';
  notifications: boolean;
  language: string;
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  setNotifications: (enabled: boolean) => void;
  setLanguage: (language: string) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      theme: 'system',
      notifications: true,
      language: 'en',
      setTheme: (theme) => set({ theme }),
      setNotifications: (notifications) => set({ notifications }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'settings-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

## Cart Store

```typescript
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  total: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],

  addItem: (item) =>
    set((state) => {
      const existing = state.items.find((i) => i.id === item.id);
      if (existing) {
        return {
          items: state.items.map((i) =>
            i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
          ),
        };
      }
      return { items: [...state.items, { ...item, quantity: 1 }] };
    }),

  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),

  updateQuantity: (id, quantity) =>
    set((state) => ({
      items:
        quantity <= 0
          ? state.items.filter((item) => item.id !== id)
          : state.items.map((item) =>
              item.id === id ? { ...item, quantity } : item
            ),
    })),

  clearCart: () => set({ items: [] }),

  total: () => {
    const state = get();
    return state.items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );
  },
}));
```

## Selectors for Performance

```typescript
// ❌ Bad: Subscribes to entire store
function Component(): React.ReactElement {
  const store = useCartStore();
  return <Text>{store.items.length}</Text>;
}

// ✅ Good: Only subscribes to items.length
function Component(): React.ReactElement {
  const itemCount = useCartStore((state) => state.items.length);
  return <Text>{itemCount}</Text>;
}

// ✅ Good: Multiple selectors
function CartSummary(): React.ReactElement {
  const itemCount = useCartStore((state) => state.items.length);
  const total = useCartStore((state) => state.total());

  return (
    <View>
      <Text>Items: {itemCount}</Text>
      <Text>Total: ${total.toFixed(2)}</Text>
    </View>
  );
}
```

## Combining with React Query

```typescript
// Zustand for client state
const useAuthStore = create<AuthState>(...);

// React Query for server state
function useUser() {
  const token = useAuthStore((state) => state.token);

  return useQuery({
    queryKey: ['user'],
    queryFn: () => fetchUser(token),
    enabled: !!token,
  });
}
```

## DevTools (Development)

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

## Testing Stores

```typescript
import { useAuthStore } from '../authStore';

describe('authStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useAuthStore.setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  });

  it('logs out correctly', () => {
    useAuthStore.setState({
      user: { id: '1', email: 'test@test.com', name: 'Test' },
      isAuthenticated: true,
    });

    useAuthStore.getState().logout();

    expect(useAuthStore.getState().user).toBeNull();
    expect(useAuthStore.getState().isAuthenticated).toBe(false);
  });
});
```

## Notes

- Use selectors to prevent unnecessary re-renders
- Persist only necessary state
- Use SecureStore for sensitive data
- Keep stores focused on single concerns
- Zustand works outside React components
- Compatible with React 18 concurrent features
