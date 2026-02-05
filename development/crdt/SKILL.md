---
name: crdt
description: Loro CRDT state management with loro-mirror. Use when working on files in src/lib/crdt/.
---

# CRDT Guidelines

## Critical: Draft-Style Mutations Only

```typescript
// CORRECT - mutate in place
setState((state) => {
  state.transactions[id] = transaction;
});

// WRONG - returning new objects breaks change tracking
setState((state) => ({
  ...state,
  transactions: { ...state.transactions, [id]: transaction },
}));
```

## Rules

- Import types from `schema.ts`, don't redeclare
- **Soft deletes**: Set `deletedAt` timestamp, never remove from document
- Use `crypto.randomUUID()` for IDs, `Date.now()` for timestamps

## Schema Pattern

```typescript
export const entitySchema = schema.LoroMap({
  id: schema.String({ required: true }),
  // ... fields
  deletedAt: schema.Number(), // 0 = not deleted, >0 = timestamp
});
```

## React Hooks

- `useActiveTransactions()` - excludes soft-deleted
- `useTransactions()` - includes soft-deleted  
- `useVaultAction()` - for mutations

## Sync

- Updates encrypted before leaving client
- Loro handles versioning via version vectors
- Conflicts: last-write-wins per field
