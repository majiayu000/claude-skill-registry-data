---
name: solidjs
description: SolidJS fine-grained reactivity, signals, JSX without Virtual DOM, and SolidStart. Use when building SolidJS apps, components, or reactive UIs.
---

## solidjs

### Core Concepts
- Signals: createSignal for reactive state, createEffect for side effects
- createMemo for derived values, createResource for async data fetching
- JSX compiles to real DOM bindings, no Virtual DOM overhead
- Control flow: <Show>, <For>, <Switch>/<Match>, <Index> as components

### Common Patterns
- SolidStart for file-based routing with server functions
- createContext/useContext for dependency injection without prop drilling
- createStore for nested reactive objects with path setters
- createDeferred for batching updates on idle callback
- Error boundaries with <ErrorBoundary> fallback prop

### Best Practices
- Read signals in effects, not in render for proper tracking
- Destructure props carefully to not lose reactivity
- Use createMemo for expensive computations
- Prefer stores over deeply nested signals
- Use createResource with refetch for data synchronization

### Common Code Patterns
- Signal-based counter with createEffect for localStorage sync
- Async resource fetching with Suspense and <ErrorBoundary>
- Store for form state with path-based updates
