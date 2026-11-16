---
name: react-patterns
description: React 18/19 hooks discipline, server/client component boundaries, Suspense + error boundaries, form actions, state management, and accessibility-first composition. Use when building or reviewing React/Next.js components.
license: MIT
source: https://github.com/affaan-m/ECC
---

# React Patterns

React 18/19 component patterns for correctness, performance, and maintainability.

**Trigger phrases:** "React component", "hooks", "server component", "RSC", "Suspense", "use client", "use server", "Next.js component"

---

## Hook Discipline

```tsx
// ✅ Stable dependency references
const handler = useCallback(() => doSomething(id), [id])
const value = useMemo(() => expensive(data), [data])

// ❌ New object/function every render → infinite loops
useEffect(() => {}, [{ id }])   // object literal in dep array
```

Rules of Hooks: only call at top level, never inside conditions/loops. Cleanup side effects: return cleanup from useEffect.

---

## Server / Client Boundary

```tsx
// Server Component (default in Next.js app/)
async function UserList() {
  const users = await db.users.findMany()
  return <ul>{users.map(u => <UserCard key={u.id} user={u} />)}</ul>
}

// Client Component — only when needed
'use client'
// Can: useState, useEffect, event handlers
// Cannot: async functions, server-only imports
```

Add 'use client' only for: interactive state, browser-only APIs, event listeners.

---

## Suspense + Error Boundaries

```tsx
<ErrorBoundary fallback={<ErrorCard />}>
  <Suspense fallback={<Skeleton />}>
    <UserProfile userId={id} />
  </Suspense>
</ErrorBoundary>
```

---

## Form Actions (React 19 / Next.js)

```tsx
'use server'
async function createUser(formData: FormData) {
  await db.users.create({ data: { name: formData.get('name') } })
  revalidatePath('/users')
}
<form action={createUser}><input name="name" /><button type="submit">Create</button></form>
```

---

## State Management

| Scope | Pattern |
|-------|---------|
| Component-local | useState / useReducer |
| Shared across tree | Context + useContext |
| Global / cross-page | Zustand / Jotai |
| Server state | TanStack Query / SWR |
| URL state | useSearchParams |

---

## Anti-Fake-Pass

```
❌ useEffect with no cleanup for subscriptions → memory leak
❌ key={index} on list items that reorder
❌ Calling a hook inside an if/else → Rules of Hooks violation
❌ 'use client' on every component "to be safe"
❌ useState for derived data computable from other state
```

## See Also
- react-performance, react-testing, core/agents/react-reviewer.md
