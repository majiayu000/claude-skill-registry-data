---
name: headless-ui
description: |
  Build headless UI hooks that encapsulate data fetching, state management, routing, and mutations without UI rendering. The presenter layer in MVP architecture.

  Use when: building page-level hooks, creating domain-specific data hooks, separating application concerns from presentation, implementing the presenter layer, composing multiple data sources.
---

# Headless UI

Build headless UI hooks that encapsulate all application concerns (data fetching, state, routing, mutations) without any UI rendering logic. The hook is "headless" because it provides behavior without prescribing UI implementation.

## Overview

A headless UI hook is a custom React hook that returns a structured object containing data, state, actions, and pending states. Pages consume these hooks and compose pure view components.

```typescript
// The pattern: hook provides behavior, component provides UI
const { todos, handleCreate, isPending } = useTodosPage();

return <TodoList todos={todos} onCreate={handleCreate} isCreating={isPending.create} />;
```

## Quick Start

### 1. Create a Presenter Hook

```typescript
// src/lib/hooks/use-todos-page.ts
export function useTodosPage() {
  const { data: todos, isLoading } = useFetchTodos();
  const createMutation = useCreateTodo();
  
  const handleCreate = useCallback(async (title: string) => {
    await createMutation.mutateAsync({ title });
  }, [createMutation]);
  
  return useMemo(() => ({
    todos: todos ?? [],
    isLoading,
    handleCreate,
    isPending: { create: createMutation.isPending },
  }), [todos, isLoading, handleCreate, createMutation.isPending]);
}
```

### 2. Consume in Page

```typescript
// src/app/todos/page.tsx
export default function TodosPage() {
  const { todos, isLoading, handleCreate, isPending } = useTodosPage();
  
  return (
    <TodoList 
      todos={todos} 
      isLoading={isLoading}
      onCreate={handleCreate}
      isCreating={isPending.create}
    />
  );
}
```

## Return Object Structure

Organize returns into clear sections:

| Section | Contents | Example |
|---------|----------|---------|
| **Data** | Fetched data, computed values | `todos`, `filteredTodos`, `selectedTodo` |
| **State** | Local/URL state, loading/error | `searchQuery`, `isEditing`, `isLoading` |
| **Actions** | Async callbacks for mutations | `handleCreate`, `handleSave`, `handleDelete` |
| **Pending** | Loading states per mutation | `isPending.create`, `isPending.update` |

## Hook Types

### Atomic Hooks
Domain-specific hooks handling a single domain's concerns:
- `useTodos()` - todo data and mutations
- `useNotes()` - note data and mutations

### Aggregate Hooks
Compose multiple atomic hooks into unified APIs:
- `useApp({ enabled: { todos: true, notes: true } })`

### Page Hooks
Full presenter hooks for specific pages:
- `useTodosPage()` - everything needed for /todos
- `useNotesPage()` - everything needed for /notes

## Topics

For deeper understanding, explore these focused topics:

### [`topics/hooks.md`](./topics/hooks.md)
**Presenter Hooks**

The foundational pattern for creating headless UI hooks. Covers hook structure, return object design, responsibilities, and API principles.

**Start here if:** You're new to headless UI or building your first presenter hook.

---

### [`topics/composition.md`](./topics/composition.md)
**Hook Composition**

Compose multiple atomic hooks into aggregate hooks with opt-in enabled pattern. Covers atomic vs aggregate hooks, namespaced returns, and the enabled options object.

**Start here if:** You need to combine data from multiple domains on one page.

---

### [`topics/conditional-fetching.md`](./topics/conditional-fetching.md)
**Conditional Fetching**

Control when hooks fetch data using the enabled parameter. Covers React Query integration, lazy loading, and preventing over-fetching.

**Start here if:** You need to defer or conditionally load data.

---

### [`topics/memoization.md`](./topics/memoization.md)
**Hook Memoization**

Properly memoize return values and callbacks for stable references. Covers useMemo, useCallback, dependency management, and when NOT to memoize.

**Start here if:** You're seeing unnecessary re-renders or need to optimize hook performance.

---

## File Templates

See `templates/` for starter code:
- `presenter-hook.ts` - Full presenter hook template

## Key Principles

1. **No UI in hooks** - Return data and callbacks, not JSX
2. **Structured returns** - Organize by data/state/actions/pending
3. **Stable references** - Memoize objects and callbacks
4. **Promise-based actions** - Return promises for async operations
5. **Opt-in fetching** - Support enabled parameter for conditional loading
