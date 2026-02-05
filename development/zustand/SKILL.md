---
name: zustand
description: Zustand 5+ state management. Use when creating stores, selectors, middleware, or persisting state.
---

# Zustand 5+

## Create store — named import

```ts
import { create } from 'zustand'

const useStore = create<State>()((set, get) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
  reset: () => set({ count: 0 })
}))

// NOT default import — that's v4
```

## Selectors with useShallow

```ts
import { useShallow } from 'zustand/shallow'

// Single value — no useShallow needed
const count = useStore((s) => s.count)

// Multiple values — use useShallow to prevent re-renders
const { name, email } = useStore(
  useShallow((s) => ({ name: s.name, email: s.email }))
)

// NOT custom equality in create() — that's v4
```

## Custom equality (if needed)

```ts
import { createWithEqualityFn } from 'zustand/traditional'
import { shallow } from 'zustand/shallow'

const useStore = createWithEqualityFn<State>()(
  (set) => ({ ... }),
  shallow
)

// NOT create(fn, shallow) — that's v4
```

## Persist middleware

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useStore = create<State>()(
  persist(
    (set) => ({
      theme: 'dark',
      setTheme: (t) => set({ theme: t })
    }),
    { name: 'app-storage' }
  )
)

// v5: Initial state NOT auto-persisted on creation
// Hydration happens async — handle loading state
```

## Persist with partialize

```ts
persist(
  (set) => ({ ... }),
  {
    name: 'app-storage',
    partialize: (state) => ({ theme: state.theme })  // only persist theme
  }
)
```

## setState with replace

```ts
// Partial update (default)
set({ count: 5 })

// Full replace — must provide complete state
set({ count: 5, name: 'New', items: [] }, true)

// v5: replace=true requires ALL fields
```

## Combine middleware

```ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

const useStore = create<State>()(
  devtools(
    persist(
      (set) => ({ ... }),
      { name: 'storage' }
    ),
    { name: 'MyStore' }
  )
)
```

## Access outside React

```ts
// Get current state
const count = useStore.getState().count

// Subscribe to changes
const unsub = useStore.subscribe((state) => console.log(state))

// Set state directly
useStore.setState({ count: 10 })
```

## Slices pattern

```ts
const createUserSlice = (set) => ({
  user: null,
  setUser: (user) => set({ user })
})

const createCartSlice = (set) => ({
  items: [],
  addItem: (item) => set((s) => ({ items: [...s.items, item] }))
})

const useStore = create((...a) => ({
  ...createUserSlice(...a),
  ...createCartSlice(...a)
}))
```

## Avoid

- Default import → named `import { create }`
- `create(fn, shallow)` → `createWithEqualityFn` from `zustand/traditional`
- Object selector without `useShallow` → causes re-renders
- `setState({}, true)` → replace requires complete state
- Assuming persist hydrates sync → handle loading state
