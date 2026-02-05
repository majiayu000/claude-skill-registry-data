---
name: "state patterns"
description: "A practical skill for managing state in React prototypes without heavyweight libraries."
license: Proprietary
---

# State Patterns for Prototypes

A practical skill for managing state in React prototypes without heavyweight libraries.

## Core Principles

1. **Separate what happened from what to show** - Actions describe events, state describes current reality, derived values compute display
2. **Colocate related state** - Group state by feature/domain, not by type
3. **Use the simplest tool that works** - useState → useReducer → Context → (rarely) external library

## Pattern Library

### 1. Standard Reducer Shape

Use this consistent pattern across prototypes for predictable structure:

```tsx
// State shape - keep flat when possible
type State = {
  status: 'idle' | 'loading' | 'error' | 'success'
  data: YourDataType | null
  error: string | null
  // UI-specific state separate from data state
  ui: {
    selectedId: string | null
    filterText: string
    isDialogOpen: boolean
  }
}

// Action union - explicit event types
type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: YourDataType }
  | { type: 'FETCH_ERROR'; error: string }
  | { type: 'UI_SELECT'; id: string }
  | { type: 'UI_FILTER'; text: string }
  | { type: 'UI_TOGGLE_DIALOG' }

// Reducer - pure state transitions
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, status: 'loading', error: null }
    case 'FETCH_SUCCESS':
      return { ...state, status: 'success', data: action.payload, error: null }
    case 'FETCH_ERROR':
      return { ...state, status: 'error', error: action.error }
    case 'UI_SELECT':
      return { ...state, ui: { ...state.ui, selectedId: action.id } }
    case 'UI_FILTER':
      return { ...state, ui: { ...state.ui, filterText: action.text } }
    case 'UI_TOGGLE_DIALOG':
      return { ...state, ui: { ...state.ui, isDialogOpen: !state.ui.isDialogOpen } }
    default:
      return state
  }
}
```

**When to use:** 3+ related pieces of state, or when state updates depend on previous state.

### 2. Separation Layers

Organize state into three clear layers:

```tsx
// Layer 1: Server/Data State (what exists)
type DataState = {
  items: Item[]
  status: 'idle' | 'loading' | 'error' | 'success'
  error: string | null
}

// Layer 2: UI State (what the user is doing)
type UIState = {
  selectedIds: Set<string>
  searchQuery: string
  sortBy: 'name' | 'date'
  viewMode: 'grid' | 'list'
}

// Layer 3: Derived State (computed for display)
// Never store these - always compute them
const filteredItems = items.filter(item =>
  item.name.toLowerCase().includes(searchQuery.toLowerCase())
)
const selectedItems = items.filter(item => selectedIds.has(item.id))
const sortedItems = [...filteredItems].sort((a, b) =>
  sortBy === 'name' ? a.name.localeCompare(b.name) : b.date - a.date
)
```

**Rule:** If you can compute it from existing state, don't store it.

### 3. Minimal State Machine Helper

When you need state machine clarity without XState ceremony:

```tsx
// Define your states and valid transitions
const machine = {
  idle: {
    START: 'loading'
  },
  loading: {
    SUCCESS: 'success',
    ERROR: 'error',
    CANCEL: 'idle'
  },
  success: {
    REFRESH: 'loading',
    RESET: 'idle'
  },
  error: {
    RETRY: 'loading',
    RESET: 'idle'
  }
} as const

// Simple hook to enforce valid transitions
function useStateMachine<T extends typeof machine>(
  machine: T,
  initial: keyof T
) {
  const [state, setState] = useState<keyof T>(initial)

  const send = (event: string) => {
    const transitions = machine[state] as Record<string, keyof T>
    const nextState = transitions?.[event]
    if (nextState) {
      setState(nextState)
    } else {
      console.warn(`Invalid transition: ${String(state)} -> ${event}`)
    }
  }

  return [state, send] as const
}

// Usage
const [state, send] = useStateMachine(machine, 'idle')
send('START') // -> 'loading'
send('CANCEL') // -> 'idle'
send('INVALID') // -> warns, stays 'idle'
```

**When to use:** When invalid state transitions cause bugs (e.g., "can't load while already loading").

### 4. Feature-Scoped Context Pattern

Avoid prop drilling while keeping state scoped to where it's needed:

```tsx
// Example: Card collection with selection and filtering
type CollectionState = {
  items: Item[]
  selectedIds: Set<string>
  filterText: string
  viewMode: 'grid' | 'list'
}

type CollectionActions = {
  addItem: (item: Item) => void
  removeItem: (id: string) => void
  toggleSelection: (id: string) => void
  setFilter: (text: string) => void
  setViewMode: (mode: 'grid' | 'list') => void
}

const CollectionStateContext = createContext<CollectionState | null>(null)
const CollectionActionsContext = createContext<CollectionActions | null>(null)

// Provider combines state and actions
export function CollectionProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, initialState)

  // Actions as stable callbacks
  const actions = useMemo((): CollectionActions => ({
    addItem: (item) => dispatch({ type: 'ADD_ITEM', item }),
    removeItem: (id) => dispatch({ type: 'REMOVE_ITEM', id }),
    toggleSelection: (id) => dispatch({ type: 'TOGGLE_SELECTION', id }),
    setFilter: (text) => dispatch({ type: 'SET_FILTER', text }),
    setViewMode: (mode) => dispatch({ type: 'SET_VIEW_MODE', mode })
  }), [])

  return (
    <CollectionStateContext.Provider value={state}>
      <CollectionActionsContext.Provider value={actions}>
        {children}
      </CollectionActionsContext.Provider>
    </CollectionStateContext.Provider>
  )
}

// Separate hooks for state and actions
export function useCollectionState() {
  const context = useContext(CollectionStateContext)
  if (!context) throw new Error('useCollectionState must be used within CollectionProvider')
  return context
}

export function useCollectionActions() {
  const context = useContext(CollectionActionsContext)
  if (!context) throw new Error('useCollectionActions must be used within CollectionProvider')
  return context
}

// Usage in components
function ItemCard({ id }: { id: string }) {
  const { selectedIds } = useCollectionState() // Only re-renders when selection changes
  const { toggleSelection } = useCollectionActions() // Never causes re-render

  return (
    <Card
      selected={selectedIds.has(id)}
      onClick={() => toggleSelection(id)}
    />
  )
}
```

**Why split contexts?** Components that only dispatch actions won't re-render when state changes.

### 5. URL as State Pattern

For prototypes with shareable state, sync with URL:

```tsx
// Custom hook to sync state with URL
function useURLState<T extends string>(
  key: string,
  defaultValue: T
): [T, (value: T) => void] {
  const [searchParams, setSearchParams] = useSearchParams()

  const value = (searchParams.get(key) as T) ?? defaultValue

  const setValue = (newValue: T) => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev)
      if (newValue === defaultValue) {
        next.delete(key)
      } else {
        next.set(key, newValue)
      }
      return next
    })
  }

  return [value, setValue]
}

// Usage - acts like useState but persists to URL
function Sidebar() {
  const [view, setView] = useURLState('view', 'grid')
  const [sort, setSort] = useURLState('sort', 'name')
  // URL: ?view=list&sort=date
}
```

**When to use:** Tabs, filters, search, view modes—anything you want shareable via URL.

### 6. Async Action Pattern

Consistent pattern for handling async operations:

```tsx
// Reusable async handler
function useAsyncAction<T, Args extends unknown[]>(
  asyncFn: (...args: Args) => Promise<T>
) {
  const [state, setState] = useState({
    status: 'idle' as 'idle' | 'loading' | 'error' | 'success',
    data: null as T | null,
    error: null as string | null
  })

  const execute = async (...args: Args) => {
    setState({ status: 'loading', data: null, error: null })
    try {
      const data = await asyncFn(...args)
      setState({ status: 'success', data, error: null })
      return { success: true, data }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error'
      setState({ status: 'error', data: null, error: message })
      return { success: false, error: message }
    }
  }

  return { ...state, execute }
}

// Usage
function DataFetcher() {
  const fetch = useAsyncAction(async (id: string) => {
    const res = await fetch(`/api/items/${id}`)
    return res.json()
  })

  return (
    <>
      <button onClick={() => fetch.execute('123')}>Load</button>
      {fetch.status === 'loading' && <Spinner />}
      {fetch.status === 'error' && <Error message={fetch.error} />}
      {fetch.status === 'success' && <Data value={fetch.data} />}
    </>
  )
}
```

## Decision Tree

**Single piece of state?** → `useState`

**2-3 related pieces, simple updates?** → `useState` multiple times

**3+ pieces, or updates depend on previous state?** → `useReducer`

**Need to share across 3+ components in a subtree?** → Context + useReducer

**Need to share across entire app?** → Reconsider—do you really? If yes, Context at root.

**Need URL persistence?** → `useURLState` pattern

**Complex state machine logic?** → Minimal state machine helper

**Async operations?** → `useAsyncAction` pattern

## Common Mistakes to Avoid

1. **Storing derived state** - If you can compute it, don't store it
2. **Context at root for everything** - Scope context to feature subtrees
3. **Mixing concerns in one reducer** - Keep data state separate from UI state
4. **Over-abstracting too early** - Start simple, refactor when pain is real
5. **Not separating state and actions contexts** - Causes unnecessary re-renders

## Quick Reference

```tsx
// Copy-paste starter for any prototype
import { useReducer, createContext, useContext, useMemo, ReactNode } from 'react'

type State = {
  // Your state shape here
}

type Action =
  | { type: 'ACTION_ONE'; payload?: unknown }
  | { type: 'ACTION_TWO'; payload?: unknown }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'ACTION_ONE':
      return { ...state /* updates */ }
    default:
      return state
  }
}

const StateContext = createContext<State | null>(null)
const DispatchContext = createContext<React.Dispatch<Action> | null>(null)

export function Provider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, /* initialState */)
  return (
    <StateContext.Provider value={state}>
      <DispatchContext.Provider value={dispatch}>
        {children}
      </DispatchContext.Provider>
    </StateContext.Provider>
  )
}

export function useState() {
  const context = useContext(StateContext)
  if (!context) throw new Error('useState must be used within Provider')
  return context
}

export function useDispatch() {
  const context = useContext(DispatchContext)
  if (!context) throw new Error('useDispatch must be used within Provider')
  return context
}
```

## When to Apply This Skill

- Starting a new prototype and need to decide state approach
- Existing prototype state is getting messy/confusing
- Need to share state across components
- Adding complex async operations or state machines
- Want consistent patterns across multiple prototypes
