---
name: composable-svelte-core
description: Core architecture patterns for Composable Svelte. Use when creating stores, writing reducers, working with effects, composing reducers, or implementing business logic. Covers the Store-Reducer-Effect trinity, all 12 effect types, composition strategies (scope, combineReducers, forEach), and immutable state updates.
---

# Composable Svelte Core Architecture

This skill covers the fundamental patterns for building Composable Svelte applications: stores, reducers, effects, and composition strategies.

---

## CRITICAL RULES

### Rule 1: ALL State Must Be in the Store

**Principle**: Every piece of application state, including UI state, MUST live in the store. This is non-negotiable for testability.

#### ❌ WRONG - Component State
```svelte
<script lang="ts">
  let isEditing = $state(false);      // ❌ Not testable
  let draftText = $state('');         // ❌ Not testable
  let showModal = $state(false);      // ❌ Not testable
</script>
```

#### ✅ CORRECT - Store State
```typescript
// State in store
interface TodoState {
  text: string;
  isEditing: boolean;     // ✅ Testable with TestStore
  draftText: string;      // ✅ Testable with TestStore
}

type TodoAction =
  | { type: 'startEdit' }
  | { type: 'updateDraft'; draft: string }
  | { type: 'commitEdit' };
```

**WHY**: Component state cannot be tested with TestStore. You'd need to mount components and simulate clicks. Store state can be tested with pure functions and send/receive pattern.

**What Counts as State?**
- ❌ NO `$state` for: Form values, editing flags, draft text, modal open/close, loading states, selected items, expanded/collapsed state
- ✅ YES `$derived` for: Computing values from store, filtering/mapping, formatting for display
- ✅ YES local vars for: DOM refs (`bind:this`), constants

---

### Rule 2: Pragmatic Abstraction

**Principle**: Different data structures need different patterns. Apply abstraction where value is high, use simple helpers elsewhere.

#### Decision Matrix

| Structure | Pattern | Why |
|-----------|---------|-----|
| Flat collections (todos, counters) | `forEach` + `scopeToElement` | Items independent, isolation valuable (92% boilerplate reduction) |
| Recursive trees (folders, org charts) | Helper functions + `store + ID` | Relationships matter, structure explicit |
| Optional children (modals, sheets) | `ifLet` + `PresentationAction` | State-driven navigation |
| Permanent children (sections) | `scope()` + `combineReducers` | Clear boundaries |

**WHY**: Composable Architecture's value comes from predictability and testability, not uniformity. Use the right tool for each structure.

---

## CORE PATTERNS

### Pattern 1: Store Auto-Subscription

**IMPORTANT**: Stores implement Svelte's store contract via the `subscribe()` method. This means you can use Svelte's `$store` syntax for automatic subscription - **ZERO boilerplate!**

#### ✅ CORRECT - Auto-Subscription (Recommended)

```svelte
<script lang="ts">
  import { createStore } from '@composable-svelte/core';

  const store = createStore({
    initialState: { count: 0, isLoading: false },
    reducer: counterReducer,
    dependencies: { api }
  });

  // Use $store directly - automatic subscription!
  const displayText = $derived(`Count: ${$store.count}`);
</script>

{#if $store.isLoading}
  <p>Loading...</p>
{:else}
  <p>{displayText}</p>
  <button onclick={() => store.dispatch({ type: 'increment' })}>
    Increment
  </button>
{/if}
```

#### ❌ WRONG - Manual Subscription (Unnecessary)

```svelte
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  const store = createStore({...});

  // ❌ Unnecessary manual subscription
  let state = $state(store.state);
  let unsubscribe: (() => void) | null = null;

  onMount(() => {
    unsubscribe = store.subscribe((newState) => {
      state = newState;
    });
  });

  onDestroy(() => {
    unsubscribe?.();
  });

  // Using local state variable
  const displayText = $derived(`Count: ${state.count}`);
</script>

{#if state.isLoading}
  <p>Loading...</p>
{/if}
```

**Why `$store` Works**: The store implements Svelte's store contract with a `subscribe()` method that takes a callback and returns an unsubscribe function. Svelte's compiler automatically handles subscription/unsubscription when you use the `$` prefix.

**When to Use Manual Subscription**: Only when you need to transform or wrap the store for specific integration patterns (e.g., form reactive wrappers). For normal component usage, always use `$store`.

---

### Pattern 2: Store-Reducer-Effect Trinity

The fundamental pattern for every feature.

#### Complete Template

```typescript
// 1. Define State (ALL application state)
interface FeatureState {
  items: Item[];
  isLoading: boolean;
  error: string | null;
  selectedId: string | null;
}

// 2. Define Actions (Discriminated Union)
type FeatureAction =
  | { type: 'loadItems' }
  | { type: 'itemsLoaded'; items: Item[] }
  | { type: 'loadFailed'; error: string }
  | { type: 'selectItem'; id: string }
  | { type: 'clearSelection' };

// 3. Define Dependencies
interface FeatureDependencies {
  api: APIClient;
  clock: Clock;
}

// 4. Reducer (Pure Function)
const featureReducer: Reducer<FeatureState, FeatureAction, FeatureDependencies> = (
  state,
  action,
  deps
) => {
  switch (action.type) {
    case 'loadItems':
      return [
        { ...state, isLoading: true, error: null },
        Effect.run(async (dispatch) => {
          const result = await deps.api.get<Item[]>('/items');
          if (result.ok) {
            dispatch({ type: 'itemsLoaded', items: result.data });
          } else {
            dispatch({ type: 'loadFailed', error: result.error });
          }
        })
      ];

    case 'itemsLoaded':
      return [
        { ...state, items: action.items, isLoading: false },
        Effect.none()
      ];

    case 'loadFailed':
      return [
        { ...state, error: action.error, isLoading: false },
        Effect.none()
      ];

    case 'selectItem':
      return [
        { ...state, selectedId: action.id },
        Effect.none()
      ];

    case 'clearSelection':
      return [
        { ...state, selectedId: null },
        Effect.none()
      ];

    default:
      // Exhaustiveness check
      const _never: never = action;
      return [state, Effect.none()];
  }
};

// 5. Component
// Feature.svelte
<script lang="ts">
  import { createStore } from '@composable-svelte/core';
  import { featureReducer } from './reducer';

  const store = createStore({
    initialState: {
      items: [],
      isLoading: false,
      error: null,
      selectedId: null
    },
    reducer: featureReducer,
    dependencies: {
      api: createAPIClient(),
      clock: new SystemClock()
    }
  });

  // Load on mount
  $effect(() => {
    store.dispatch({ type: 'loadItems' });
  });
</script>

{#if $store.isLoading}
  <p>Loading...</p>
{:else if $store.error}
  <p class="error">{$store.error}</p>
{:else}
  <ul>
    {#each $store.items as item (item.id)}
      <li
        class:selected={$store.selectedId === item.id}
        onclick={() => store.dispatch({ type: 'selectItem', id: item.id })}
      >
        {item.name}
      </li>
    {/each}
  </ul>
{/if}
```

#### Checklist
- [ ] State interface defines ALL application state
- [ ] Actions are discriminated union with `type` field
- [ ] Reducer is pure function (no side effects)
- [ ] Immutable updates (`{ ...state, field: newValue }`)
- [ ] Effects return data structures, not executed in reducer
- [ ] Exhaustiveness check in default case
- [ ] Component has NO `$state` for application state
- [ ] Component reads from `$store`, dispatches actions

---

## EFFECT SYSTEM (12 Types)

### Effect Decision Tree

```
What kind of side effect do you need?
│
├─ Pure state update → Effect.none()
├─ Async operation that dispatches → Effect.run()
├─ Fire-and-forget (analytics, logging) → Effect.fireAndForget()
├─ Multiple parallel effects → Effect.batch()
├─ Cancel previous effect → Effect.cancel() + Effect.cancellable()
├─ Delay user input (search-as-you-type) → Effect.debounced()
├─ Limit frequency (scroll events) → Effect.throttled()
├─ Wait before dispatching → Effect.afterDelay()
├─ Long-running (WebSocket, SSE) → Effect.subscription()
├─ Animation timing → Effect.animated()
└─ PresentationState lifecycle → Effect.transition()
```

### Effect.none() - Pure State Update
```typescript
case 'selectItem':
  return [
    { ...state, selectedId: action.id },
    Effect.none() // No side effects
  ];
```

### Effect.run() - Async with Dispatch
```typescript
case 'loadData':
  return [
    { ...state, isLoading: true },
    Effect.run(async (dispatch) => {
      const result = await api.getData();
      if (result.ok) {
        dispatch({ type: 'dataLoaded', data: result.data });
      } else {
        dispatch({ type: 'loadFailed', error: result.error });
      }
    })
  ];
```

### Effect.fireAndForget() - No Dispatch Needed
```typescript
case 'buttonClicked':
  return [
    { ...state, clickCount: state.clickCount + 1 },
    Effect.fireAndForget(async () => {
      await analytics.track('button_clicked');
    })
  ];
```

### Effect.batch() - Multiple Parallel Effects
```typescript
case 'pageLoaded':
  return [
    { ...state, isLoading: true },
    Effect.batch(
      Effect.run(async (d) => {
        const user = await api.getUser();
        d({ type: 'userLoaded', user });
      }),
      Effect.run(async (d) => {
        const settings = await api.getSettings();
        d({ type: 'settingsLoaded', settings });
      })
    )
  ];
```

### Effect.debounced() - Search as You Type
```typescript
case 'searchTextChanged':
  return [
    { ...state, searchText: action.text },
    Effect.debounced('search', 300, async (dispatch) => {
      const results = await api.search(action.text);
      dispatch({ type: 'searchResults', results });
    })
  ];
```

### Effect.cancellable() - Cancel Previous Request
```typescript
case 'search':
  return [
    { ...state, query: action.query, isSearching: true },
    Effect.cancellable('search-request', async (dispatch) => {
      const results = await api.search(action.query);
      dispatch({ type: 'searchCompleted', results });
    })
  ];

case 'clearSearch':
  return [
    { ...state, query: '', results: [], isSearching: false },
    Effect.cancel('search-request')
  ];
```

### Effect.throttled() - Limit Frequency
```typescript
case 'scrolled':
  return [
    { ...state, scrollY: action.y },
    Effect.throttled('scroll-handler', 100, async (dispatch) => {
      // Heavy computation
      const visibleItems = computeVisibleItems(action.y);
      dispatch({ type: 'visibleItemsChanged', items: visibleItems });
    })
  ];
```

### Effect.afterDelay() - Timed Dispatch
```typescript
case 'showToast':
  return [
    { ...state, toast: action.message },
    Effect.afterDelay(3000, (dispatch) => {
      dispatch({ type: 'hideToast' });
    })
  ];
```

### Effect.subscription() - Long-Running
```typescript
case 'connectWebSocket':
  return [
    { ...state, connectionStatus: 'connecting' },
    Effect.subscription('ws', (dispatch) => {
      const ws = new WebSocket('wss://api.example.com');

      ws.onopen = () => {
        dispatch({ type: 'connected' });
      };

      ws.onmessage = (event) => {
        dispatch({ type: 'messageReceived', data: JSON.parse(event.data) });
      };

      // Cleanup function
      return () => {
        ws.close();
      };
    })
  ];

case 'disconnect':
  return [
    { ...state, connectionStatus: 'disconnected' },
    Effect.cancel('ws')
  ];
```

### Effect.transition() - PresentationState Lifecycle

**Best for**: PresentationState-based animations (modals, sheets, drawers)

**What it does**: Returns `{ present, dismiss }` effects configured with durations. Simplifies PresentationState lifecycle management.

```typescript
// Define transition once
const transition = Effect.transition({
  presentDuration: 300,
  dismissDuration: 200,
  createPresentationEvent: (event) => ({
    type: 'presentation',
    event
  })
});

// Use in reducer
case 'showModal':
  return [
    {
      ...state,
      content,
      presentation: { status: 'presenting', content, duration: 0.3 }
    },
    transition.present  // Dispatches presentationCompleted after 300ms
  ];

case 'hideModal':
  return [
    {
      ...state,
      presentation: { status: 'dismissing', content: state.presentation.content, duration: 0.2 }
    },
    transition.dismiss  // Dispatches dismissalCompleted after 200ms
  ];

case 'presentation':
  if (action.event.type === 'presentationCompleted') {
    return [
      { ...state, presentation: { status: 'presented', content: state.presentation.content } },
      Effect.none()
    ];
  }
  if (action.event.type === 'dismissalCompleted') {
    return [
      { ...state, content: null, presentation: { status: 'idle' } },
      Effect.none()
    ];
  }
  return [state, Effect.none()];
```

**Why use transition()**: Cleaner than manual `Effect.afterDelay()` for PresentationState. Encapsulates the timing logic.

---

## COMPOSITION STRATEGIES

### Strategy 1: scope() - Permanent Child

**When**: Child is always present (counter in app, settings panel, permanent UI section)

```typescript
// Parent state
interface AppState {
  counter: CounterState;
  theme: 'light' | 'dark';
}

// Parent actions
type AppAction =
  | { type: 'counter'; action: CounterAction }
  | { type: 'toggleTheme' };

// Compose with scope()
import { scope } from '@composable-svelte/core';

const appReducer: Reducer<AppState, AppAction> = (state, action, deps) => {
  switch (action.type) {
    case 'counter':
      // Delegate to child via scope()
      return scope(
        (s) => s.counter,                    // Get child state
        (s, c) => ({ ...s, counter: c }),    // Set child state
        (a) => a.type === 'counter' ? a.action : null, // Extract child action
        (ca) => ({ type: 'counter', action: ca }),     // Lift child action
        counterReducer
      )(state, action, deps);

    case 'toggleTheme':
      return [
        { ...state, theme: state.theme === 'light' ? 'dark' : 'light' },
        Effect.none()
      ];

    default:
      const _never: never = action;
      return [state, Effect.none()];
  }
};
```

### Strategy 2: combineReducers() - Multiple Slices

**When**: Multiple independent sections sharing the same action type (Redux-style slices)

```typescript
import { combineReducers } from '@composable-svelte/core';

interface AppState {
  user: UserState;
  posts: PostsState;
  comments: CommentsState;
}

const appReducer = combineReducers<AppState, AppAction>({
  user: userReducer,
  posts: postsReducer,
  comments: commentsReducer
});
```

### Strategy 3: forEach() - Flat Collection

**When**: Independent items that don't know about each other (todo list, product grid)

```typescript
// State
interface TodosState {
  todos: TodoState[];
}

interface TodoState {
  id: string;
  text: string;
  completed: boolean;
}

type TodoAction =
  | { type: 'toggle' }
  | { type: 'delete' };

// Single todo reducer
const todoReducer: Reducer<TodoState, TodoAction> = (state, action) => {
  switch (action.type) {
    case 'toggle':
      return [{ ...state, completed: !state.completed }, Effect.none()];
    case 'delete':
      // Parent will handle removal
      return [state, Effect.none()];
    default:
      return [state, Effect.none()];
  }
};

// Collection reducer with forEach()
import { integrate } from '@composable-svelte/core';

const todosReducer = integrate<TodosState, any, Deps>()
  .forEach('todo', s => s.todos, (s, todos) => ({ ...s, todos }), todoReducer)
  .build();

// Component
import { scopeToElement } from '@composable-svelte/core';

{#each $store.todos as todo (todo.id)}
  {@const todoStore = scopeToElement(store, 'todo', todo.id)}
  <Todo store={todoStore} />
{/each}
```

### Strategy 4: Tree Utilities - Recursive Structures

**When**: Hierarchical data with parent-child relationships (file systems, org charts, nested menus)

**Why NOT forEach**: Trees have relationships between nodes, structure needs to be explicit. Per DESIGN-PRINCIPLES.md, use simple helpers over complex abstractions for trees.

```typescript
// 1. Define tree node types
type FileNode = { type: 'file'; id: string; name: string };
type FolderNode = { type: 'folder'; id: string; name: string; children: Node[]; isExpanded: boolean };
type Node = FileNode | FolderNode;

// 2. Create tree helpers
import { createTreeHelpers } from '@composable-svelte/core/utils/tree';

const treeHelpers = createTreeHelpers<Node>({
  getId: (node) => node.id,
  getChildren: (node) => node.type === 'folder' ? node.children : undefined,
  setChildren: (node, children) =>
    node.type === 'folder' ? { ...node, children } : node
});

// 3. Use in reducer with node ID
interface FileSystemState {
  root: Node[];
  selectedId: string | null;
}

type FileSystemAction =
  | { type: 'toggleExpand'; folderId: string }
  | { type: 'renameNode'; nodeId: string; newName: string }
  | { type: 'deleteNode'; nodeId: string };

const fileSystemReducer: Reducer<FileSystemState, FileSystemAction> = (state, action) => {
  switch (action.type) {
    case 'toggleExpand': {
      const updated = treeHelpers.updateNode(state.root, action.folderId, (node) =>
        node.type === 'folder' ? { ...node, isExpanded: !node.isExpanded } : node
      );
      return [{ ...state, root: updated || state.root }, Effect.none()];
    }

    case 'renameNode': {
      const updated = treeHelpers.updateNode(state.root, action.nodeId, (node) => ({
        ...node,
        name: action.newName
      }));
      return [{ ...state, root: updated || state.root }, Effect.none()];
    }

    case 'deleteNode': {
      const updated = treeHelpers.deleteNode(state.root, action.nodeId);
      return [{ ...state, root: updated || state.root }, Effect.none()];
    }

    default:
      return [state, Effect.none()];
  }
};

// 4. Component passes ID, not scoped store
// Folder.svelte
<script lang="ts">
  export let store: Store<FileSystemState, FileSystemAction>;
  export let folderId: string;  // Component knows its ID

  const folder = $derived(treeHelpers.findNode($store.root, folderId) as FolderNode);
</script>

<div>
  <button onclick={() => store.dispatch({ type: 'toggleExpand', folderId })}>
    {folder.isExpanded ? '▼' : '▶'}
  </button>
  <span>{folder.name}</span>

  {#if folder.isExpanded}
    <div class="children">
      {#each folder.children as child (child.id)}
        {#if child.type === 'folder'}
          <svelte:self store={store} folderId={child.id} />
        {:else}
          <File store={store} fileId={child.id} />
        {/if}
      {/each}
    </div>
  {/if}
</div>
```

**Key Helpers**:
- `findNode(nodes, id)` - Find node by ID (depth-first search)
- `updateNode(nodes, id, updater)` - Immutably update node
- `deleteNode(nodes, id)` - Immutably delete node
- `addChild(nodes, parentId, child)` - Add child to parent

**Decision**: Use tree helpers when:
- Nodes have parent-child relationships
- Structure needs to be traversable (find parent of node)
- Knowing the ID is natural (recursive components)

**Avoid**: scopeToTreeNode or other complex abstractions - simple helpers provide 80% of value with 20% of complexity.

---

## COMMON ANTI-PATTERNS

### 1. Component $state for Application State

#### ❌ WRONG
```svelte
<script lang="ts">
  let isEditing = $state(false);
  let draftText = $state('');

  function save() {
    // Can't test this with TestStore
  }
</script>
```

#### ✅ CORRECT
```typescript
interface State {
  isEditing: boolean;
  draftText: string;
}

type Action =
  | { type: 'startEdit' }
  | { type: 'updateDraft'; text: string }
  | { type: 'save' };

// Now testable with TestStore
await store.send({ type: 'startEdit' }, (state) => {
  expect(state.isEditing).toBe(true);
});
```

**WHY**: Component state is not testable with TestStore. All application state must be in store for exhaustive testing.

---

### 2. Mutation Instead of Immutable Updates

#### ❌ WRONG
```typescript
case 'addItem':
  state.items.push(action.item); // Mutation!
  return [state, Effect.none()];
```

#### ✅ CORRECT
```typescript
case 'addItem':
  return [
    { ...state, items: [...state.items, action.item] },
    Effect.none()
  ];
```

**WHY**: Svelte 5 runes depend on new object references to detect changes. Mutation breaks reactivity.

---

### 3. Async Reducer (Side Effects in Reducer)

#### ❌ WRONG
```typescript
const reducer = async (state, action) => {
  const data = await fetch('/api/data');
  return [{ ...state, data }, Effect.none()];
};
```

#### ✅ CORRECT
```typescript
const reducer = (state, action) => {
  return [
    { ...state, isLoading: true },
    Effect.run(async (dispatch) => {
      const data = await fetch('/api/data');
      dispatch({ type: 'dataLoaded', data });
    })
  ];
};
```

**WHY**: Reducers must be pure functions. Side effects belong in Effect system.

---

### 4. Not Handling API Errors

#### ❌ WRONG
```typescript
Effect.run(async (dispatch) => {
  const result = await api.getData();
  dispatch({ type: 'dataLoaded', data: result.data }); // What if result.ok is false?
});
```

#### ✅ CORRECT
```typescript
Effect.run(async (dispatch) => {
  const result = await api.getData();
  if (result.ok) {
    dispatch({ type: 'dataLoaded', data: result.data });
  } else {
    dispatch({ type: 'loadFailed', error: result.error });
  }
});
```

**WHY**: Always handle both success and error cases for robust applications.

---

### 5. Missing Exhaustiveness Check

#### ❌ WRONG
```typescript
const reducer = (state, action) => {
  switch (action.type) {
    case 'increment':
      return [{ ...state, count: state.count + 1 }, Effect.none()];
    // Missing default case - TypeScript won't catch new actions
  }
};
```

#### ✅ CORRECT
```typescript
const reducer = (state, action) => {
  switch (action.type) {
    case 'increment':
      return [{ ...state, count: state.count + 1 }, Effect.none()];

    default:
      const _never: never = action; // TypeScript error if action not handled
      return [state, Effect.none()];
  }
};
```

**WHY**: Exhaustiveness check ensures all actions are handled, caught at compile time.

---

## DECISION TOOLS

### Composition Strategy Matrix

| Question | Answer | Strategy |
|----------|--------|----------|
| Is child always present? | Yes | `scope()` |
| Is child optional (navigation)? | Yes | `ifLet()` + `PresentationAction` (see composable-svelte-navigation) |
| Is it a list of independent items? | Yes | `forEach()` + `scopeToElement()` |
| Multiple slices, same action type? | Yes | `combineReducers()` |
| Is it a tree structure? | Yes | Helper functions + `store + ID` |

### Effect Type Decision Tree

```
What kind of side effect?
│
├─ Pure state change (no async, no external calls)
│  └─ Effect.none()
│
├─ Async operation that needs to dispatch back
│  ├─ Single async call → Effect.run()
│  ├─ Fire-and-forget (analytics, logging) → Effect.fireAndForget()
│  └─ Multiple parallel operations → Effect.batch()
│
├─ User input that changes frequently
│  ├─ Search-as-you-type (wait for pause) → Effect.debounced()
│  ├─ Cancel previous request → Effect.cancellable()
│  └─ Limit frequency (scroll, resize) → Effect.throttled()
│
├─ Time-based
│  ├─ Wait then dispatch → Effect.afterDelay()
│  └─ Animation timing → Effect.animated()
│
└─ Long-running connection
   └─ WebSocket, SSE, interval → Effect.subscription()
```

### Abstraction Value Matrix (from DESIGN-PRINCIPLES.md)

**Core Principle**: Apply abstraction where value is high, use simple helpers elsewhere.

| Value | Complexity | Decision |
|-------|------------|----------|
| High | Low | ✅ **ADD** - Clear win, add to library |
| High | High | ⚠️ **CONSIDER** - Explore simpler alternatives first |
| Low | Low | ⚠️ **MAYBE** - Only if it rounds out the API |
| Low | High | ❌ **DON'T ADD** - Use simple helpers instead |

**Examples**:

| Pattern | Value | Complexity | Decision |
|---------|-------|------------|----------|
| `forEach` for flat collections | High (92% boilerplate reduction) | Medium (~160 LOC) | ✅ Added |
| `scopeToElement` simplification | High (80% less boilerplate) | Low (small API change) | ✅ Added |
| `scopeToTreeNode` for trees | Low (marginal benefit) | High (~500 LOC, 3 concepts) | ❌ Not added |
| Tree helper functions | Medium-High (eliminates recursive boilerplate) | Low (~100 LOC pure functions) | ✅ Added |

**Decision Process**:
1. **Value Question**: Does this eliminate significant boilerplate? Prevent common bugs? Make code clearer?
2. **Complexity Question**: How many lines? How many new concepts? How hard to debug?
3. **Trade-off Question**: What do we gain? What do we lose? Is it worth it?
4. **Alternative Question**: Could simple helpers achieve 80% of the value?

**Key Insight**: Better to have 5 powerful abstractions that users love + simple helpers for other cases, than 20 abstractions that cover every case but are hard to learn.

---

## CHECKLIST

### Starting New Feature
- [ ] 1. Define State interface with ALL application state
- [ ] 2. Define Actions as discriminated union
- [ ] 3. Define Dependencies interface
- [ ] 4. Write Reducer as pure function
- [ ] 5. Use immutable updates (`{ ...state }`)
- [ ] 6. Return Effects as data structures
- [ ] 7. Add exhaustiveness check in default case
- [ ] 8. Create TestStore tests (NOT component tests) - See composable-svelte-testing skill
- [ ] 9. Test all actions with send/receive
- [ ] 10. Component has NO `$state` for app state

---

## TEMPLATES

### Basic Feature Template

```typescript
// types.ts
export interface FeatureState {
  items: Item[];
  isLoading: boolean;
  error: string | null;
}

export type FeatureAction =
  | { type: 'loadItems' }
  | { type: 'itemsLoaded'; items: Item[] }
  | { type: 'loadFailed'; error: string };

export interface FeatureDependencies {
  api: APIClient;
}

// reducer.ts
import { Reducer, Effect } from '@composable-svelte/core';

export const featureReducer: Reducer<FeatureState, FeatureAction, FeatureDependencies> = (
  state,
  action,
  deps
) => {
  switch (action.type) {
    case 'loadItems':
      return [
        { ...state, isLoading: true, error: null },
        Effect.run(async (dispatch) => {
          const result = await deps.api.getItems();
          if (result.ok) {
            dispatch({ type: 'itemsLoaded', items: result.data });
          } else {
            dispatch({ type: 'loadFailed', error: result.error });
          }
        })
      ];

    case 'itemsLoaded':
      return [{ ...state, items: action.items, isLoading: false }, Effect.none()];

    case 'loadFailed':
      return [{ ...state, error: action.error, isLoading: false }, Effect.none()];

    default:
      const _never: never = action;
      return [state, Effect.none()];
  }
};

// Feature.svelte
<script lang="ts">
  import { createStore } from '@composable-svelte/core';
  import { featureReducer } from './reducer';

  const store = createStore({
    initialState: { items: [], isLoading: false, error: null },
    reducer: featureReducer,
    dependencies: { api: createAPIClient() }
  });

  $effect(() => {
    store.dispatch({ type: 'loadItems' });
  });
</script>

{#if $store.isLoading}
  <p>Loading...</p>
{:else if $store.error}
  <p class="error">{$store.error}</p>
{:else}
  <ul>
    {#each $store.items as item (item.id)}
      <li>{item.name}</li>
    {/each}
  </ul>
{/if}
```

### Todo with Inline Editing

```typescript
// State
interface TodoState {
  id: string;
  text: string;
  completed: boolean;
  isEditing: boolean;      // In store, not component $state
  editDraft: string;       // In store, not component $state
}

// Actions
type TodoAction =
  | { type: 'toggle' }
  | { type: 'startEdit' }
  | { type: 'updateDraft'; draft: string }
  | { type: 'commitEdit' }
  | { type: 'cancelEdit' };

// Reducer
case 'startEdit':
  return [
    { ...state, isEditing: true, editDraft: state.text },
    Effect.none()
  ];

case 'updateDraft':
  return [
    { ...state, editDraft: action.draft },
    Effect.none()
  ];

case 'commitEdit':
  return [
    { ...state, text: state.editDraft.trim() || state.text, isEditing: false, editDraft: '' },
    Effect.none()
  ];

case 'cancelEdit':
  return [
    { ...state, isEditing: false, editDraft: '' },
    Effect.none()
  ];
```

### Search with Debounce

```typescript
// State
interface SearchState {
  query: string;
  results: SearchResult[];
  isSearching: boolean;
}

// Actions
type SearchAction =
  | { type: 'queryChanged'; query: string }
  | { type: 'searchCompleted'; results: SearchResult[] };

// Reducer
case 'queryChanged':
  return [
    { ...state, query: action.query, isSearching: true },
    Effect.debounced('search', 300, async (dispatch) => {
      const results = await api.search(action.query);
      dispatch({ type: 'searchCompleted', results });
    })
  ];

case 'searchCompleted':
  return [
    { ...state, results: action.results, isSearching: false },
    Effect.none()
  ];
```

---

## SUMMARY

This skill covers the core architecture patterns for Composable Svelte:

1. **Critical Rules**: All state in store, pragmatic abstraction
2. **Store-Reducer-Effect Trinity**: The fundamental pattern
3. **12 Effect Types**: Complete effect system with decision tree
4. **4 Composition Strategies**: scope(), combineReducers(), forEach(), tree helpers
5. **Anti-Patterns**: 5 common mistakes with corrections
6. **Decision Tools**: Matrices and checklists
7. **Templates**: Ready-to-use code patterns

**Remember**: Testability is the core value. All state in store, test with TestStore (see composable-svelte-testing skill), use the right abstraction for each structure.

For navigation patterns (modals, sheets, drawers), see **composable-svelte-navigation** skill.
For testing patterns, see **composable-svelte-testing** skill.
For forms, see **composable-svelte-forms** skill.
For SSR, see **composable-svelte-ssr** skill.
For component library, see **composable-svelte-components** skill.
