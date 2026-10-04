---
name: react-dev
version: 2.1.0
category: UI
level: library
engineer: ui-engineer
gate: "pnpm tsc --noEmit"
bundles: []
description: >
  React 18-19 expert patterns for TypeScript. Use when building React components,
  typing hooks/events, using React 19 features (Actions, Server Components, use()),
  writing/reviewing useEffect or useState for derived values, data fetching, or state
  synchronization. Covers generic components, discriminated union props, and when NOT
  to use Effect.
source: ~/.agents/skills@2026-07-13
user-invocable: false
---


# React TypeScript — Expert Patterns

<when_to_use>

- React 19 migration (ref as prop, useActionState, use())
- Generic components with type inference
- Server Components + Server Actions
- useEffect decisions (when to use, when NOT to)
- Derived state vs. effect-based state

NOT for: non-React TypeScript, vanilla JS React, styling/CSS, routing (use nextjs-app-router skill)

</when_to_use>

<effect_decision_tree>

Effects are an **escape hatch**. If no external system is involved, you don't need one.

```
Need to respond to something?
├── User interaction (click, submit, drag)?
│   └── EVENT HANDLER — not useEffect
├── Value derived from props/state?
│   └── CALCULATE DURING RENDER
│       └── Expensive? useMemo
├── Reset state when identity prop changes?
│   └── KEY PROP — not useEffect + setState
├── Component appeared on screen?
│   └── useEffect (external sync, analytics)
└── Subscribe to external store?
    └── useSyncExternalStore
```

| Situation | DON'T | DO |
|-----------|-------|-----|
| Derived state | `useState` + `useEffect` | Compute during render |
| Expensive calc | `useEffect` to cache | `useMemo` |
| Reset state on prop change | `useEffect` + `setState` | `key` prop |
| User event response | `useEffect` watching state | Event handler |
| Notify parent | `useEffect` calling `onChange` | Call in event handler |
| Fetch data | `useEffect` without cleanup | cleanup + `ignore` flag OR framework |

**Quick fixes — the 3 most common effect removals:**

```typescript
// 1. Derived state: DELETE the effect, compute during render
// ❌ const [fullName, setFullName] = useState('');
//    useEffect(() => setFullName(first + ' ' + last), [first, last]);
// ✅
const fullName = first + ' ' + last;  // Just compute it

// 2. Reset on prop change: DELETE the effect, use key prop
// ❌ useEffect(() => { setComment(''); }, [userId]);
// ✅ <CommentForm key={userId} />  // React remounts, state resets

// 3. Event response: DELETE the effect, call in handler
// ❌ useEffect(() => { if (submitted) showToast(); }, [submitted]);
// ✅ function handleSubmit() { submit(); showToast(); }
```

See [effect-anti-patterns.md](references/effect-anti-patterns.md) for 9 anti-patterns with BAD/GOOD code pairs.
See [effect-alternatives.md](references/effect-alternatives.md) for useMemo, key prop, useSyncExternalStore, lifting state.

</effect_decision_tree>

<react_19_changes>

React 19 breaking changes — the patterns Claude may not default to:

**ref as prop** — forwardRef is deprecated:

```typescript
// React 19: ref is a regular prop
function Button({ ref, children, ...props }: {
  ref?: React.Ref<HTMLButtonElement>;
} & React.ComponentPropsWithoutRef<'button'>) {
  return <button ref={ref} {...props}>{children}</button>;
}
```

**useActionState** — replaces useFormState:

```typescript
const [state, formAction, isPending] = useActionState(submitAction, {});
return <form action={formAction}>...</form>;
```

**use()** — unwraps promises/context (suspends until resolved):

```typescript
// Server: pass promise WITHOUT await
async function Page() {
  const userPromise = fetchUser('123'); // Don't await!
  return <UserProfile userPromise={userPromise} />;
}

// Client: unwrap with use()
'use client';
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <div>{user.name}</div>;
}
```

See [react-19-patterns.md](references/react-19-patterns.md) for useOptimistic, useTransition, migration checklist.

</react_19_changes>

<generic_components>

Generic components infer types from props — no manual annotations at call site.

**Three patterns** — use the simplest that fits:

```typescript
// 1. Constrained generic — require an id field
function List<T extends { id: string | number }>({ items }: { items: T[] }) {
  return <ul>{items.map(item => <li key={item.id}>...</li>)}</ul>;
}

// 2. keyof T — type-safe column/field access
type Column<T> = { key: keyof T; header: string; render?: (v: T[keyof T], item: T) => React.ReactNode };
function Table<T extends { id: string | number }>({ data, columns }: { data: T[]; columns: Column<T>[] }) { ... }

// 3. Discriminated unions — mutually exclusive prop sets
type Props = { variant: 'link'; href: string } | { variant: 'button'; onClick: () => void };
```

See [generic-components.md](examples/generic-components.md) for full Table, Select, List, Modal, FormField implementations.

</generic_components>

<component_selection>

## When to Use Which Pattern

```
Building a component?
├── Needs type-safe access to item fields?
│   └── Generic with constraint: <T extends { id: string }>
├── Renders different UI based on a mode?
│   └── Discriminated union props: { variant: 'link'; href } | { variant: 'button'; onClick }
├── Wraps a native HTML element?
│   └── ComponentPropsWithoutRef<'element'> + ref as prop
├── Fetches its own data?
│   └── Server Component (async function) — no hooks needed
└── Needs interactivity (state, events)?
    └── Client Component with "use client"
```

**Common mistakes by pattern:**

| Pattern | Mistake | Fix |
|---------|---------|-----|
| Constrained generic | Forgetting empty array case — `items: T[]` with `.length === 0` | Guard with early return before `.map()` |
| Discriminated union | Missing exhaustive check — adding a new variant silently falls through | Use `satisfies never` in default case |
| ComponentPropsWithoutRef | Using `ComponentProps` (includes ref) — causes ref forwarding type conflicts | Always `WithoutRef`, pass ref as regular prop |
| Server Component | Importing a client hook (`useState`, `useEffect`) — build error | Extract interactive parts to a separate `"use client"` file |

</component_selection>

<server_components>

**Async data fetching** (server only):

```typescript
// Next.js 15: params is a Promise
export default async function UserPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const user = await fetchUser(id);
  return <div>{user.name}</div>;
}
```

**Server Actions** — 'use server' for mutations:

```typescript
'use server';
export async function updateUser(userId: string, formData: FormData) {
  await db.user.update({ where: { id: userId }, data: { ... } });
  revalidatePath(`/users/${userId}`);
}
```

**Client consuming Server Action**:

```typescript
'use client';
import { useActionState } from 'react';
import { updateUser } from '@/actions/user';

function UserForm({ userId }: { userId: string }) {
  const [state, formAction, isPending] = useActionState(
    (prev, formData) => updateUser(userId, formData), {}
  );
  return <form action={formAction}>...</form>;
}
```

See [server-components.md](examples/server-components.md) for parallel fetching, streaming, error boundaries.

</server_components>

<client_server_boundary>

## "use client" Decision

```
Does this component...
├── Use useState, useEffect, useRef, event handlers?
│   └── "use client" — interactive component
├── Use only props + JSX (no hooks, no browser APIs)?
│   └── Server Component — no directive needed
├── Mix: static layout with one interactive widget?
│   └── Split: Server Component parent + "use client" child for the widget
├── Need window, document, localStorage?
│   └── "use client" — browser-only APIs
└── Import a "use client" component?
    └── Can still be Server Component — "use client" boundary is per-module, not per-tree
```

**Key insight:** "use client" is a **module boundary**, not a component boundary. Everything imported BY a "use client" module becomes client code. Keep the boundary as deep as possible — push "use client" to leaf components.

</client_server_boundary>

<rules>

ALWAYS:
- ref as prop in React 19 (no forwardRef)
- useActionState for form actions (not useFormState)
- ComponentPropsWithoutRef for native element extension
- Discriminated unions for variant props
- as const for tuple hook returns
- Compute derived values during render (not in useEffect)
- key prop to reset component state (not useEffect + setState)
- Cleanup function in data-fetching Effects (ignore flag for race conditions)
- For component API design (props shape): prefer discriminated unions over boolean flags — boolean combos grow exponentially
- For internal implementation: choose the simplest pattern that type-checks — don't reach for generics when a concrete type works

NEVER:
- forwardRef in React 19+ — deprecated, ref is a regular prop now
- useFormState — replaced by useActionState (React 19)
- JSX.Element for children type — ReactNode includes strings, numbers, null, fragments; JSX.Element excludes them, causing false type errors on valid renders
- any for event handlers — use React.MouseEvent<T>, ChangeEvent<T>, etc. for accurate currentTarget typing
- await promises when passing to use() — defeats Suspense streaming; the server blocks until data resolves instead of streaming the shell immediately
- Mix Server/Client components in same file — 'use client' boundary applies to entire module
- useEffect for derived state, event responses, or parent notification — causes extra render pass with stale intermediate state
- useEffect chains that trigger each other via setState — N chained effects = N+1 render passes, each with stale intermediate state; calculate all next state in the event handler instead
- Data fetch in useEffect without cleanup — race condition: fast query response arrives after slow one, displaying stale results

</rules>

<references>

**MANDATORY** — load when reviewing or writing useEffect code:
- [effect-anti-patterns.md](references/effect-anti-patterns.md) - 9 useEffect anti-patterns with BAD/GOOD pairs
- [effect-alternatives.md](references/effect-alternatives.md) - useMemo, key prop, useSyncExternalStore, lifting state

**MANDATORY** — load when migrating to React 19:
- [react-19-patterns.md](references/react-19-patterns.md) - useActionState, use(), useOptimistic, migration checklist

Load on demand (match to task):
- [hooks.md](references/hooks.md) - useCallback, useMemo, useImperativeHandle, useSyncExternalStore
- [event-handlers.md](references/event-handlers.md) - all event types, generic handlers
- [generic-components.md](examples/generic-components.md) - Table, Select, List, Modal patterns
- [server-components.md](examples/server-components.md) - async components, Server Actions, streaming

</references>
