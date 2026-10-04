---
name: zustand
description: Best practices for Zustand (v5) state management — store creation, TypeScript typing, selectors, middleware (persist, devtools, immer), slices, SSR/Next.js per-request stores, and using getState outside React. Auto-activates when creating or editing a Zustand store, useStore selector, or client global state.
---

# Zustand (v5)

Minimal, hook-based client state. Use it for **client/UI/session state** — not server state (that's TanStack Query). Keep stores small and domain-scoped; split by concern rather than one mega-store.

## Creating a typed store

```ts
import { create } from 'zustand'

type BearState = {
  bears: number
  increase: (by: number) => void
  reset: () => void
}

export const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((s) => ({ bears: s.bears + by })),
  reset: () => set({ bears: 0 }),
}))
```
- v5 requires the **curried** form `create<T>()(...)` for correct inference with middleware.
- Co-locate actions inside the store. Don't store derived state — compute it in selectors/components.

## Selectors — subscribe narrowly

```ts
const bears = useBearStore((s) => s.bears)                 // re-renders only when bears changes
```
- **Never** `const { a, b } = useBearStore()` (subscribes to the whole store → re-renders on every change).
- Selecting multiple values? Return an object/array **with `useShallow`** to avoid an infinite/extra render:
```ts
import { useShallow } from 'zustand/react/shallow'
const { a, b } = useBearStore(useShallow((s) => ({ a: s.a, b: s.b })))
```
- Returning a new object/array without `useShallow` is the #1 Zustand bug.

## Middleware (compose order matters: `devtools(persist(immer(...)))`)

```ts
import { create } from 'zustand'
import { devtools, persist, createJSONStorage } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

export const useStore = create<State>()(
  devtools(
    persist(
      immer((set) => ({ /* ... set((s) => { s.x = 1 }) with immer ... */ })),
      {
        name: 'my-store',
        storage: createJSONStorage(() => localStorage),
        partialize: (s) => ({ x: s.x }),     // persist only what you need
        version: 1,
        migrate: (persisted, version) => persisted as State,
      },
    ),
    { name: 'MyStore' },
  ),
)
```
- `persist`: always `partialize` (don't persist functions/transient flags); set `version` + `migrate` when the shape can change.
- `immer`: lets you write mutating `set((s) => { s.nested.k = v })`. Without it, return new objects.
- `devtools`: name each store so Redux DevTools is readable.

## Outside React (interceptors, utils, event handlers)

Use `getState()` / `setState()` — never call the hook outside a component.
```ts
useAuthStore.getState().clearAuth()
const token = useAuthStore.getState().token
```

## Slices pattern (large stores)

```ts
const createFishSlice = (set) => ({ fishes: 0, addFish: () => set((s) => ({ fishes: s.fishes + 1 })) })
const createBearSlice = (set) => ({ bears: 0, addBear: () => set((s) => ({ bears: s.bears + 1 })) })
export const useStore = create((...a) => ({ ...createFishSlice(...a), ...createBearSlice(...a) }))
```

## SSR / Next.js App Router

- **Do not** create a module-level store that holds request/user data on the server — it leaks state across requests.
- Create the store **per request** and pass it via React Context (vanilla `createStore` + a provider), or keep server-data in TanStack Query and use Zustand only for client UI state.
- Reading store state during render of a Server Component is a mistake — stores are client-only (`"use client"`).

## Cross-tab sync

Either rely on `persist` (storage syncs) or add a `window.addEventListener('storage', …)` listener that calls a `sync()` action. Bump a session counter on auth transitions so dependent data resets cleanly.

## Don'ts

- Don't subscribe to the whole store; don't return fresh objects without `useShallow`.
- Don't put server/async cache state in Zustand — use a query library.
- Don't mutate state outside `set` (unless using immer).
- Don't share one server store instance across requests in SSR.
