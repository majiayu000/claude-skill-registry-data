---
name: jotai-reactive-atoms
description: Implement reactive state management with Jotai atoms in Electron renderer. Use when creating atoms, implementing real-time updates via IPC, or setting up hybrid stream + HTTP fallback patterns. Covers event subscription optimization, debouncing, and Suspense integration.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Jotai Reactive Atoms for Electron

## Overview

This skill documents the Jotai atom patterns for Electron applications with IPC-based real-time updates.

## Key Patterns

| Pattern | Use Case | Description |
|---------|----------|-------------|
| Hybrid Atom | Real-time data | Stream + HTTP fallback |
| Stream Atom | IPC subscriptions | onMount with subscription |
| Single Fetch Atom | Initial data | HTTP-only async atom |
| Event Subscription | IPC optimization | Shared IPC listeners |
| Write Atom | Mutations (CRUD) | Create, Update, Delete operations |

## Quick Reference

### Hybrid Atom Pattern

```typescript
// 1. HTTP fallback (initial load)
const singleFetchAtom = atomWithRefresh(async () => {
  const res = await client.users.$get();
  return res.json();
});

// 2. Stream atom (IPC updates) - NO initial fetch
const streamAtom = atom<{ value: User[] }>();
streamAtom.onMount = (set) => {
  const handleUpdate = debounce(async () => {
    const res = await client.users.$get();
    if (res.ok) set({ value: await res.json() });
  }, 300);
  return usersSource.subscribe(handleUpdate);
};

// 3. Hybrid selector (exported) - NOT async
export const usersAtom = atom((get) => {
  const stream = get(streamAtom);
  if (stream !== undefined) return stream.value;
  return get(singleFetchAtom);
});
```

### Write Atom Pattern

```typescript
export const createUserAtom = atom(
  null,  // No read value
  async (_get, set, data: CreateUserData) => {
    const res = await client.users.$post({ json: data });
    switch (res.status) {
      case 201: {
        set(singleFetchAtom);  // Refresh read atom
        return res.json();
      }
      default:
        throw new Error('Failed');
    }
  }
);

// Usage: const [, createUser] = useAtom(createUserAtom);
```

### Component Usage

```tsx
const UserList = () => {
  const users = useAtomValue(usersAtom);
  const [, createUser] = useAtom(createUserAtom);
  // ...
};

export const UsersPage = () => (
  <Suspense fallback={<Loading />}>
    <UserList />
  </Suspense>
);
```

## When to Use Each Pattern

### Hybrid Atom (Stream + HTTP Fallback)
Use for data that:
- Changes frequently
- Needs real-time updates
- Is shared across components

Examples: Users, Notifications, Active Event

### Stream-Only Atom
Use for data that:
- Is append-only (like logs)
- Doesn't need initial fetch

### Single Fetch Atom
Use for data that:
- Rarely changes
- Doesn't need real-time updates

## Key Rules

1. **Hybrid atom getter must NOT be async** - See [Why not use async](HYBRID-ATOM.md#why-not-use-async---understanding-suspense-behavior)
2. **No initial fetch in onMount** - singleFetchAtom handles initial load
3. **Always debounce IPC handlers** - prevents excessive fetches
4. **Use switch(res.status)** - not res.ok
5. **Refresh read atoms after mutations** - `set(singleFetchAtom)`

## Detailed Documentation

- [HYBRID-ATOM.md](HYBRID-ATOM.md) - Full hybrid pattern with diagrams
- [WRITE-ATOM.md](WRITE-ATOM.md) - Write atom patterns (create, update, delete)
- [EVENT-SUBSCRIPTION.md](EVENT-SUBSCRIPTION.md) - IPC subscription optimization
- [examples/hybrid-atom.ts](examples/hybrid-atom.ts) - Read atom implementation
- [examples/write-atom.ts](examples/write-atom.ts) - Write atom implementation
- [examples/use-optimistic-value.ts](examples/use-optimistic-value.ts) - Optimistic update hook

## Related Skills

- [suspense-boundary-design](../suspense-boundary-design/SKILL.md) - Suspense boundary placement and ErrorBoundary patterns
