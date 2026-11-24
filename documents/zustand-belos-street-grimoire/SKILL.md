---
name: zustand
title: Zustand State Management
description: Modern, lightweight state management for React
icon: 🗄️
tags: [react, state-management, zustand]
---

# Zustand State Management

Zustand is a small, fast and scalable state-management solution using simplified flux principles. It has a comfy API based on hooks, isn't boilerplatey or opinionated.

## Quick Start

```bash
npm install zustand
# or
yarn add zustand
# or
pnpm add zustand
```

## Basic Usage

```ts
import { create } from 'zustand'

interface CounterState {
  count: number
  increment: () => void
  decrement: () => void
}

const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}))
```

```tsx
function Counter() {
  const { count, increment, decrement } = useCounterStore()
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  )
}
```

## Key Features

- **Minimal API**: Simple and intuitive
- **No providers needed**: Use anywhere in your app
- **TypeScript support**: Full type inference
- **Performance**: Selective re-renders with selectors
- **DevTools**: Built-in Redux DevTools integration
- **Persistence**: Easy state persistence
- **Middleware**: Composable middleware system

## Common Patterns

### Selective Subscriptions

```tsx
function Count() {
  const count = useCounterStore((state) => state.count)
  return <div>{count}</div>
}

function Controls() {
  const { increment, decrement } = useCounterStore()
  return (
    <>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </>
  )
}
```

### Async Actions

```ts
const useUserStore = create<UserState>((set) => ({
  user: null,
  isLoading: false,
  error: null,
  
  fetchUser: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await api.getUser(id)
      set({ user: response.data, isLoading: false })
    } catch (error) {
      set({ error: error as Error, isLoading: false })
    }
  },
}))
```

### With Middleware

```ts
import { persist, devtools } from 'zustand/middleware'

const useStore = create(
  devtools(
    persist(
      (set) => ({
        // store implementation
      }),
      { name: 'app-storage' }
    )
  )
)
```

## Best Practices

1. **Use selectors**: Subscribe only to what you need
2. **Keep stores focused**: One store per domain
3. **Type everything**: Leverage TypeScript
4. **Use middleware**: For persistence and devtools
5. **Avoid prop drilling**: Use stores for shared state

## Resources

- [Official Documentation](https://docs.pmnd.rs/zustand)
- [GitHub Repository](https://github.com/pmndrs/zustand)
- [Examples](https://github.com/pmndrs/zustand/tree/main/examples)
