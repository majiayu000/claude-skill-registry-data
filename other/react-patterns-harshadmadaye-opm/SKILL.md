---
name: react-patterns
description: Provides idiomatic React 18/19 and Next.js App Router patterns covering hooks discipline, composition, state colocation, server/client boundaries, Suspense and error boundaries, forms, data fetching, list keys, effects hygiene, and measurement-first performance work. Use when writing, reviewing, or refactoring React components, custom hooks, or Next.js routes.
---

# React Patterns

React rewards code that keeps render pure, puts state where it is used, and reaches for
optimisation only after measuring. This skill is the checklist for that.

## When to use

- Writing or modifying function components, custom hooks, or component trees.
- Reviewing JSX/TSX diffs.
- Choosing where state should live or how components should compose.
- Working across Server and Client Components in the Next.js App Router.
- Diagnosing slow renders, waterfalls, or oversized bundles.

## Core rules

**Render is a pure function of props and state.** Derive during render; do not store derived values.

```tsx
// Good
function Cart({ items }: { items: CartItem[] }) {
  const total = items.reduce((sum, i) => sum + i.price * i.qty, 0);
  return <span>{formatMoney(total)}</span>;
}

// Bad: an extra render, a chance to desync, and hidden data flow
function Cart({ items }: { items: CartItem[] }) {
  const [total, setTotal] = useState(0);
  useEffect(() => setTotal(items.reduce((s, i) => s + i.price * i.qty, 0)), [items]);
  return <span>{formatMoney(total)}</span>;
}
```

**Side effects live in event handlers or `useEffect`, never in the render body.**

**Compose, do not inherit.** `children`, slot props, and compound components cover every case.

**Do not define components inside components.** A new component type on every render remounts
its subtree and loses state.

## Hooks discipline

- Call hooks at the top level only; never inside conditions, loops, or after early returns.
- Every subscription, timer, and listener returns a cleanup.
- Use the functional updater when new state depends on old: `setCount(c => c + 1)`.
- Dependencies are honest: list what the effect reads. If the list is painful, the effect is
  doing too much or the value should be a ref or an event handler.
- Extract a custom hook when the same hook sequence appears in two or more components, not before.
- Expensive initial state uses the lazy initialiser: `useState(() => parse(bigInput))`.

## Effects hygiene

Most `useEffect` calls in application code are one of these mistakes:

| You wrote an effect to... | Do this instead |
|---|---|
| Compute a value from props/state | Derive during render (or `useMemo` if measured) |
| Respond to a user action | Put the logic in the event handler |
| Fetch application data | Use a server-state library or RSC (see Data fetching) |
| Reset state when a prop changes | Give the component a `key` tied to that prop |
| Notify a parent of state change | Lift the state, or call the parent's callback in the handler |
| Initialise something once per app | Module-scope guard, not an effect |

Legitimate effects synchronise with something outside React: DOM measurement, subscriptions,
third-party widgets, analytics on mount. Use primitive dependencies (`[id, name]`), not fresh
objects (`[{ id, name }]`).

## State location

```
Used by one component?                     -> useState inside it
Shared by a parent and a few children?     -> lift to the nearest common ancestor
Low-frequency, tree-wide (theme, auth)?    -> Context, one context per concern
High-frequency, tree-wide?                 -> external store (Zustand, Jotai, Redux Toolkit)
Comes from a server?                       -> server-state library or RSC, not useState
```

Colocate by default. Most pages need neither context nor a global store. Split contexts so a
change to notifications does not re-render every theme consumer. When subscribing to a store,
select the narrowest value (`useStore(s => s.cart.length > 0)`), not the whole object.

## Composition recipes

```tsx
// Slot via children
<Layout><Header /><Main>{content}</Main></Layout>

// Named slots
<Page header={<Nav />} sidebar={<Filters />}><Results /></Page>

// Compound components sharing state through context
<Tabs defaultValue="profile">
  <Tabs.List>
    <Tabs.Trigger value="profile">Profile</Tabs.Trigger>
    <Tabs.Trigger value="settings">Settings</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Panel value="profile"><Profile /></Tabs.Panel>
  <Tabs.Panel value="settings"><Settings /></Tabs.Panel>
</Tabs>
```

Render props still work but a hook returning the same shape (`useData(id)`) is usually cleaner.

## Lists and keys

- Keys are stable identities from the data (`item.id`), never the array index for lists that
  reorder, filter, or insert.
- A `key` change deliberately remounts; use it to reset form state when the edited entity changes.
- Render conditionally with a ternary, not `&&`, when the left side can be `0` or `""`:
  `{count > 0 ? <Badge>{count}</Badge> : null}`.
- Virtualise (`@tanstack/react-virtual`, `react-window`) once visible rows exceed roughly fifty
  with non-trivial content; before that, `content-visibility: auto` on rows is often enough.

## Server / Client boundaries (Next.js App Router)

```tsx
// Server Component: default, async, ships no JS for itself
export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await db.product.findUnique({ where: { id: params.id } });
  if (!product) notFound();
  return <ProductView product={product} action={<AddToCart productId={product.id} />} />;
}

// Client Component: opt in
"use client";
export function AddToCart({ productId }: { productId: string }) {
  const [pending, startTransition] = useTransition();
  return (
    <button disabled={pending} onClick={() => startTransition(() => addToCart(productId))}>
      {pending ? "Adding..." : "Add to cart"}
    </button>
  );
}
```

Rules at the boundary:

- Server -> Client: pass serialisable props or `children`. Never a function, class instance, or Date without serialising.
- Client -> Server: call Server Actions from `<form action>` or event handlers.
- A Client Component cannot import a Server Component; compose via `children` instead.
- Push `"use client"` as far down the tree as possible so layouts and data-heavy parents stay on the server.
- Pass Client Components only the fields they render; project at the query layer.
- No mutable module-level state on the server: it is shared across requests.

Server Actions are public endpoints. Authenticate and authorise inside the action itself:

```ts
"use server";
export async function deleteItem(formData: FormData) {
  const session = await getSession();
  if (!session?.user) throw new Error("Unauthorized");
  const id = String(formData.get("id"));
  const item = await db.item.findUnique({ where: { id } });
  if (item?.ownerId !== session.user.id) throw new Error("Forbidden");
  await db.item.delete({ where: { id } });
}
```

## Data fetching

| Need | Use |
|---|---|
| Per-request data in the App Router | `await` in a Server Component |
| Client cache, mutations, invalidation | TanStack Query |
| Lightweight client cache | SWR |
| Real-time | SSE, WebSocket, or the library's subscription API |
| Fire-and-forget on interaction | `fetch` inside the handler |

Do not fetch application data with `useEffect` + `fetch`: races, no cache, no dedupe, no retry,
no Suspense. Two components that need the same data should share one request; a query library
does that for free.

Avoid waterfalls on the server:

```ts
// Sequential: three round trips
const user = await getUser(id);
const posts = await getPosts(id);

// Parallel
const [user, posts] = await Promise.all([getUser(id), getPosts(id)]);

// Or split into sibling Server Components; React renders them concurrently
```

Check cheap synchronous conditions before awaiting; move an `await` into the branch that needs
it. Wrap per-request loaders in `React.cache()` so three components asking for the same user
produce one query.

## Suspense and error boundaries

```tsx
<ErrorBoundary fallback={<ErrorView />}>
  <Suspense fallback={<UserSkeleton />}>
    <UserDetail id={id} />
  </Suspense>
</ErrorBoundary>
```

- Put Suspense close to the data so the rest of the page paints while it streams. Reserve space
  in the fallback to avoid layout shift.
- Error boundaries catch render errors, not event-handler or async errors; handle those locally.
- `react-error-boundary` gives a hook-friendly wrapper around the class API.

## Forms

React 19 actions for new code:

```tsx
"use client";
import { useActionState } from "react";

export function UserForm() {
  const [state, formAction, pending] = useActionState(updateUser, { error: null as string | null });
  return (
    <form action={formAction}>
      <label htmlFor="name">Name</label>
      <input id="name" name="name" required />
      <button type="submit" disabled={pending}>Save</button>
      {state.error && <p role="alert">{state.error}</p>}
    </form>
  );
}
```

Validate on the server with a schema (zod or similar) before touching the database. Use
controlled inputs when the value drives other UI or needs per-keystroke formatting. Multi-step
forms, field arrays, and cross-field validation belong in React Hook Form or TanStack Form.
`useOptimistic` gives instant feedback for mutations that almost always succeed.

## Performance: measure first

Default: do not memoise. Add `useMemo`, `useCallback`, or `React.memo` only when the React
profiler shows a component re-rendering often with unchanged props and a measurable cost.
If the project ships React Compiler, manual memoisation is noise.

When measurement says yes:

- `React.memo` a leaf that is expensive and receives stable props. Hoist default non-primitive
  props (`const EMPTY: Item[] = []`) so the memo is not defeated by fresh identities.
- `useMemo` for expensive derivations or objects passed to memoised children; never for `x + 1`.
- `useCallback` with functional updaters so the callback needs no dependencies.
- `startTransition` / `useDeferredValue` to keep typing responsive while expensive UI updates.
- Do not subscribe to store state that is only read inside a callback; read it on call instead.

Bundle and load:

- Import directly (`@/components/Button`), not from barrel files, unless Next.js
  `optimizePackageImports` covers the package.
- `next/dynamic` for heavy client-only components; `next/script` with `afterInteractive` or
  `lazyOnload` for third-party scripts.
- Keep dynamic import paths statically analysable: no template strings in `import()`.

Rendering:

- Animate wrappers with transforms, not layout properties.
- Inline a tiny script for pre-hydration values (theme) to avoid flicker; use
  `suppressHydrationWarning` only on the single leaf that legitimately differs.

## Accessibility baseline

- Semantic elements first (`<button>`, `<a>`, `<nav>`, `<main>`); `role` is a fallback.
- Every interactive element is keyboard reachable and has a visible focus state.
- Inputs have labels (`<label htmlFor>` or `aria-label`).
- Manage focus on route change and on modal open/close.
- Run `axe` in component tests.

## Review checklist

- [ ] No derived state in `useState` + `useEffect`.
- [ ] Every effect has a reason to exist and a cleanup if it subscribes.
- [ ] Keys are stable ids; conditionals use ternaries where `0` could leak.
- [ ] State lives at the lowest component that needs it.
- [ ] `"use client"` is at the leaves, not the layout.
- [ ] Server Actions authenticate and authorise internally.
- [ ] Independent awaits run in parallel.
- [ ] Memoisation is justified by a profile or removed.
- [ ] Forms validate on the server; errors are announced (`role="alert"`).

## Related skills

- `opm:tdd-workflow` - component behaviour tests with Testing Library before implementation.
- `opm:verification-loop` - build, `tsc --noEmit`, lint, tests before claiming done.

<!-- Adapted from affaan-m/ecc (MIT) -->
