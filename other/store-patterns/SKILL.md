---
name: TanStack Store Patterns (Alpha)
description: >-
  TanStack Store patterns for framework-agnostic reactive state. Activates when
  implementing client-side state, global stores, or reactive state management
  in React applications. NOTE: Alpha library - API may change.
version: 1.0.0
---

# TanStack Store Patterns (Alpha)

> **Alpha Library**: TanStack Store is in alpha. APIs may change between versions.

This skill covers TanStack Store for framework-agnostic reactive state management.

## Basic Store

```typescript
// lib/stores/counter-store.ts
import { Store } from '@tanstack/store'

export const counterStore = new Store({
  count: 0,
})

// Actions
export const increment = () => {
  counterStore.setState((state) => ({
    ...state,
    count: state.count + 1,
  }))
}

export const decrement = () => {
  counterStore.setState((state) => ({
    ...state,
    count: state.count - 1,
  }))
}

export const reset = () => {
  counterStore.setState((state) => ({
    ...state,
    count: 0,
  }))
}
```

## Using Store in React

```typescript
import { useStore } from '@tanstack/react-store'
import { counterStore, increment, decrement, reset } from '@/lib/stores/counter-store'

function Counter() {
  const count = useStore(counterStore, (state) => state.count)

  return (
    <div>
      <span>Count: {count}</span>
      <button onClick={decrement}>-</button>
      <button onClick={increment}>+</button>
      <button onClick={reset}>Reset</button>
    </div>
  )
}
```

## Complex Store with Derived State

```typescript
// lib/stores/cart-store.ts
import { Store } from '@tanstack/store'

interface CartItem {
  id: string
  name: string
  price: number
  quantity: number
}

interface CartState {
  items: CartItem[]
}

export const cartStore = new Store<CartState>({
  items: [],
})

// Derived selectors
export const selectCartItems = (state: CartState) => state.items

export const selectCartTotal = (state: CartState) =>
  state.items.reduce((sum, item) => sum + item.price * item.quantity, 0)

export const selectCartCount = (state: CartState) =>
  state.items.reduce((sum, item) => sum + item.quantity, 0)

// Actions
export const addToCart = (item: Omit<CartItem, 'quantity'>) => {
  cartStore.setState((state) => {
    const existing = state.items.find((i) => i.id === item.id)
    if (existing) {
      return {
        ...state,
        items: state.items.map((i) =>
          i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
        ),
      }
    }
    return {
      ...state,
      items: [...state.items, { ...item, quantity: 1 }],
    }
  })
}

export const removeFromCart = (itemId: string) => {
  cartStore.setState((state) => ({
    ...state,
    items: state.items.filter((i) => i.id !== itemId),
  }))
}

export const updateQuantity = (itemId: string, quantity: number) => {
  if (quantity <= 0) {
    removeFromCart(itemId)
    return
  }
  cartStore.setState((state) => ({
    ...state,
    items: state.items.map((i) =>
      i.id === itemId ? { ...i, quantity } : i
    ),
  }))
}

export const clearCart = () => {
  cartStore.setState(() => ({ items: [] }))
}
```

## Using Complex Store

```typescript
import { useStore } from '@tanstack/react-store'
import {
  cartStore,
  selectCartItems,
  selectCartTotal,
  selectCartCount,
  updateQuantity,
  removeFromCart,
} from '@/lib/stores/cart-store'

function CartSummary() {
  const count = useStore(cartStore, selectCartCount)
  const total = useStore(cartStore, selectCartTotal)

  return (
    <div>
      <span>{count} items</span>
      <span>${total.toFixed(2)}</span>
    </div>
  )
}

function CartItems() {
  const items = useStore(cartStore, selectCartItems)

  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          <span>{item.name}</span>
          <input
            type="number"
            value={item.quantity}
            onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
            min={0}
          />
          <button onClick={() => removeFromCart(item.id)}>Remove</button>
        </li>
      ))}
    </ul>
  )
}
```

## Store with Persistence

```typescript
// lib/stores/theme-store.ts
import { Store } from '@tanstack/store'

type Theme = 'light' | 'dark' | 'system'

interface ThemeState {
  theme: Theme
}

const getInitialTheme = (): Theme => {
  if (typeof window === 'undefined') return 'system'
  const stored = localStorage.getItem('theme')
  if (stored === 'light' || stored === 'dark' || stored === 'system') {
    return stored
  }
  return 'system'
}

export const themeStore = new Store<ThemeState>({
  theme: getInitialTheme(),
})

// Subscribe to persist changes
themeStore.subscribe(() => {
  const { theme } = themeStore.state
  localStorage.setItem('theme', theme)

  // Apply theme to document
  const root = document.documentElement
  if (theme === 'system') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    root.classList.toggle('dark', prefersDark)
  } else {
    root.classList.toggle('dark', theme === 'dark')
  }
})

export const setTheme = (theme: Theme) => {
  themeStore.setState(() => ({ theme }))
}
```

## Store Factory Pattern

```typescript
// lib/stores/create-entity-store.ts
import { Store } from '@tanstack/store'

interface EntityState<T> {
  entities: Record<string, T>
  ids: string[]
  loading: boolean
  error: string | null
}

export function createEntityStore<T extends { id: string }>() {
  const store = new Store<EntityState<T>>({
    entities: {},
    ids: [],
    loading: false,
    error: null,
  })

  return {
    store,

    selectAll: (state: EntityState<T>) =>
      state.ids.map((id) => state.entities[id]),

    selectById: (id: string) => (state: EntityState<T>) =>
      state.entities[id],

    setMany: (items: T[]) => {
      store.setState((state) => ({
        ...state,
        entities: items.reduce((acc, item) => ({ ...acc, [item.id]: item }), state.entities),
        ids: [...new Set([...state.ids, ...items.map((i) => i.id)])],
      }))
    },

    setOne: (item: T) => {
      store.setState((state) => ({
        ...state,
        entities: { ...state.entities, [item.id]: item },
        ids: state.ids.includes(item.id) ? state.ids : [...state.ids, item.id],
      }))
    },

    removeOne: (id: string) => {
      store.setState((state) => {
        const { [id]: removed, ...entities } = state.entities
        return {
          ...state,
          entities,
          ids: state.ids.filter((i) => i !== id),
        }
      })
    },

    setLoading: (loading: boolean) => {
      store.setState((state) => ({ ...state, loading }))
    },

    setError: (error: string | null) => {
      store.setState((state) => ({ ...state, error }))
    },
  }
}

// Usage
const usersStore = createEntityStore<User>()
```

## When to Use TanStack Store vs Query

| Use Case | Solution |
|----------|----------|
| Server data | TanStack Query |
| URL state | TanStack Router |
| Form state | TanStack Form |
| Local UI state | React useState |
| Shared client state | TanStack Store |
| Theme/preferences | TanStack Store + localStorage |
| Cart/wishlist | TanStack Store |

## Conventions

1. **Separate stores by domain** - One store per feature/concern
2. **Selector functions** - Define selectors for derived state
3. **Action functions** - Export actions, don't expose setState directly
4. **Type safety** - Always type your store state
5. **Persistence** - Use subscribe for localStorage sync
6. **Prefer Query** - Use Query for server state, Store for client-only

## Anti-Patterns

```typescript
// ❌ WRONG: Mutating state directly
cartStore.state.items.push(newItem)

// ✅ CORRECT: Using setState
cartStore.setState((state) => ({
  ...state,
  items: [...state.items, newItem],
}))

// ❌ WRONG: Storing server data
const postsStore = new Store({ posts: [] })

// ✅ CORRECT: Use Query for server data
const { data: posts } = useQuery(postsQueryOptions())

// ❌ WRONG: Exposing setState directly
export { counterStore }
// Component: counterStore.setState(...)

// ✅ CORRECT: Export action functions
export const increment = () => counterStore.setState(...)
```
