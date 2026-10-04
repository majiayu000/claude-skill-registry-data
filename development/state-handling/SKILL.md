---
name: state-handling
version: 1.0.0
description: >
  Standard patterns for loading, error, and empty states in React with TanStack Query.
  Covers query state (Loading → Error → Empty → Data), Skeleton/ErrorState/EmptyState
  components, mutation state, Suspense boundaries, server prefetch with HydrateClient,
  parallel Suspense boundaries, and React.cache() deduplication. Use when building
  data-fetching UIs in T3 stack projects.
user-invocable: false
allowed-tools: Read, Glob, Grep
paths: ["**/*.tsx"]
---


# State Handling — React + TanStack Query

<when_to_use>

- Building components that fetch data with `useQuery` or `useSuspenseQuery`
- Implementing loading skeletons, error states, or empty states
- Setting up Suspense boundaries (single or parallel)
- Server prefetching with `HydrateClient` to avoid loading spinners on first paint
- Deduplicating RSC data fetches with `React.cache()`
- Reviewing mutation forms for proper pending/error handling

NOT for: routing, caching strategies, Server Actions, auth (use nextjs-app-router skill)
NOT for: useEffect decisions, React 19 APIs (use react-dev skill)

</when_to_use>

## Query State Pattern

The canonical order — always handle states in this sequence:

```tsx
function EntityList() {
  const { data, isLoading, error, refetch } = useQuery(
    trpc.entity.getAll.queryOptions(),
  );

  // 1. Loading state first
  if (isLoading) return <Skeleton />;

  // 2. Error state second
  if (error) return <ErrorState message={error.message} onRetry={refetch} />;

  // 3. Empty state third
  if (!data?.length) return <EmptyState onCreate={handleCreate} />;

  // 4. Success state last
  return <DataList items={data} />;
}
```

## Component Patterns

### Skeleton

Match the layout of the loaded content — same number of rows, similar height:

```tsx
function EntityListSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 5 }).map((_, i) => (
        <div key={i} className="h-16 animate-pulse rounded-lg bg-muted" />
      ))}
    </div>
  );
}
```

### ErrorState

```tsx
interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
}

function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center gap-4 py-12">
      <AlertCircle className="h-12 w-12 text-destructive" />
      <p className="text-muted-foreground">{message}</p>
      {onRetry && (
        <Button variant="outline" onClick={onRetry}>
          Try Again
        </Button>
      )}
    </div>
  );
}
```

### EmptyState

```tsx
interface EmptyStateProps {
  title?: string;
  description?: string;
  onCreate?: () => void;
}

function EmptyState({
  title = "No items yet",
  description = "Get started by creating your first item.",
  onCreate,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center gap-4 py-12">
      <Inbox className="h-12 w-12 text-muted-foreground" />
      <div className="text-center">
        <h3 className="font-semibold">{title}</h3>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
      {onCreate && <Button onClick={onCreate}>Create First Item</Button>}
    </div>
  );
}
```

## Mutation State Pattern

```tsx
function CreateEntityForm() {
  const queryClient = useQueryClient();

  const { mutate, isPending, error } = useMutation(
    trpc.entity.create.mutationOptions({
      onSuccess: () => {
        queryClient.invalidateQueries({
          queryKey: trpc.entity.getAll.queryKey(),
        });
        toast.success("Entity created");
      },
    }),
  );

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}

      {error && <p className="text-sm text-destructive">{error.message}</p>}

      <Button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create"}
      </Button>
    </form>
  );
}
```

## Suspense Pattern

Use `useSuspenseQuery` + a Suspense boundary to eliminate explicit loading checks in the child:

```tsx
// Parent component with Suspense boundary
function EntityPage() {
  return (
    <Suspense fallback={<EntityListSkeleton />}>
      <EntityList />
    </Suspense>
  );
}

// Child uses useSuspenseQuery — no loading check needed
function EntityList() {
  const { data } = useSuspenseQuery(trpc.entity.getAll.queryOptions());

  if (!data.length) return <EmptyState />;
  return <DataList items={data} />;
}
```

## Next.js: Public RSC + ISR (Dual-Context Split)

Codified from a production T3 monorepo pattern. A representative implementation belongs in
`apps/nextjs/src/trpc/server.tsx`.

Next.js auto-promotes any page that reads `headers()` / `cookies()` to Dynamic, defeating `export const revalidate = N` (ISR). For T3 projects shipping ISR-cached public pages (marketing, blog, public event listings), the tRPC RSC context MUST be split into two factories:

```typescript
// apps/nextjs/src/trpc/server.tsx shape:
import { cache } from "react";
import { headers } from "next/headers";

// AUTH-RESOLVING: reads headers, resolves session, blocks ISR
export const createContext = cache(async () => {
  const heads = await headers();
  const auth = await initAuth(heads);
  return { auth, db, /* ... */ };
});

// AUTH-SKIPPING: synthesizes empty headers, never blocks ISR
export const createPublicContext = cache(async () => {
  return { auth: null, db, /* ... */ };
});

// Two proxies share the same getQueryClient
export const trpc = createTRPCOptionsProxy({ /* uses createContext */ });
export const publicTrpc = createTRPCOptionsProxy({ /* uses createPublicContext */ });
```

**Rule:** Any T3 project shipping ISR public pages MUST split the RSC context. Public-route RSCs MUST import from `publicTrpc`, not `trpc`. The failure mode is silent: page logs as `f Dynamic` instead of `o Static` and ISR cache never warms.

**Detection:** Run `pnpm build` and grep the route table for `o` (static) vs `f` (dynamic) markers on any route with `export const revalidate`. A revalidate route showing `f` means the seam was broken — usually because someone imported `trpc` instead of `publicTrpc` from a public RSC.

**Why this is non-obvious:** The headers() read happens transitively through tRPC's createCaller, not in the page file itself. Engineers trace `revalidate` → page → tRPC call and see no obvious headers/cookies usage. The fix only becomes clear after a production incident where ISR pages started taking 800ms instead of 50ms (Next.js silently downgraded them to Dynamic).

---

## Next.js: Server Prefetch Pattern

Prefetch on the server so the client renders from cache on first paint — no
loading spinner on initial load.

```tsx
// app/entities/page.tsx (RSC)
import { HydrateClient, trpc } from "@/trpc/server";

export default async function Page() {
  // Fire-and-forget: prefetches into the dehydrated state passed to HydrateClient
  void trpc.entity.getAll.prefetch();

  return (
    <HydrateClient>
      <Suspense fallback={<EntityListSkeleton />}>
        <EntityList />
      </Suspense>
    </HydrateClient>
  );
}

// Client component — useQuery resolves from cache synchronously on first render
"use client";
function EntityList() {
  const { data } = useSuspenseQuery(trpc.entity.getAll.queryOptions());

  if (!data.length) return <EmptyState />;
  return <DataList items={data} />;
}
```

> **Caveat — this only works if NO `"use client"` layout gates the subtree.** If any
> ancestor layout is a client component that defers `{children}` behind client-only
> state (e.g. an auth/burn gate using `useState(null)` + a `useEffect`), the island
> never renders server-side and hydration is deferred to the client — so the feed is
> absent from raw SSR HTML and `useSuspenseQuery` races hydration into one stray
> first-paint refetch (`refetchOnMount: false` alone won't close it; add `initialData`).
> The prefetch still ships settled data, but "no loading spinner / zero refetch" needs
> the gating layout to be a **server component**. Full diagnosis + tell: see
> `nextjs-app-router` skill § Client-component layouts kill RSC SSR + prefetch.

Split independent data into separate Suspense boundaries so they stream
concurrently instead of sequentially.

```tsx
// Sequential — Orders waits on UserProfile to settle before fetching
<Suspense fallback={<Skeleton />}>
  <UserProfile />
  <Orders />
</Suspense>

// Parallel — both stream independently
<Suspense fallback={<ProfileSkeleton />}>
  <UserProfile />
</Suspense>
<Suspense fallback={<OrdersSkeleton />}>
  <Orders />
</Suspense>
```

Combine with server prefetching to start both fetches before the page renders:

```tsx
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  void trpc.user.getById.prefetch({ id });
  void trpc.order.getByUser.prefetch({ userId: id });

  return (
    <HydrateClient>
      <Suspense fallback={<ProfileSkeleton />}>
        <UserProfile userId={id} />
      </Suspense>
      <Suspense fallback={<OrdersSkeleton />}>
        <Orders userId={id} />
      </Suspense>
    </HydrateClient>
  );
}
```

## Next.js: React.cache() Deduplication

When multiple RSC components in one render tree fetch the same data,
`React.cache()` executes the underlying call only once per request.

```tsx
// lib/queries/entity.ts
import { cache } from "react";
import { db } from "@{workspace}/db/client";

export const getEntity = cache(async (id: string) => {
  return db.query.entity.findFirst({ where: (t, { eq }) => eq(t.id, id) });
});

// EntityHeader and EntityDetail both call getEntity(id) — one DB round-trip
```

> Use this for server-only queries. Client-side dedup is handled by TanStack
> Query's built-in request deduplication.

## Anti-Patterns

| Avoid | Why It Fails | Do Instead |
| --- | --- | --- |
| `data && data.map(...)` | An empty array is truthy in JS, so `data && data.map(...)` renders `[]` — the map produces nothing, but the empty-state branch never runs and the user sees a blank div instead of an "add your first item" prompt. | Check `!data?.length` for empty |
| Nested ternaries | Each nested `? :` forces the reader to hold every prior branch's condition in their head to know which one currently applies — a state bug (e.g. showing stale data during a background refetch) hides inside a branch nobody re-reads carefully. | Sequential if returns |
| Loading spinner in every component | Every component that owns its own spinner mounts and unmounts independently as its query settles, so a page with 3 queries flashes 3 spinners at 3 different times instead of one coordinated fallback — visible layout jank, not just "less clean code". | Suspense boundaries |
| Inline error messages | Each call site re-decides styling, retry affordance, and copy from scratch, so error UX silently drifts (some show a retry button, some don't, some use red text, some don't) as the component count grows. | Dedicated `ErrorState` component |
| `isLoading ? <Spinner /> : data.map()` | This two-branch check has no error branch — when the query fails, `isLoading` is `false` and `data` is `undefined`, so `data.map()` either throws or (with optional chaining) silently renders as if the list were empty. A real fetch failure looks identical to "no data yet". | Full state pattern (Loading → Error → Empty → Data) |
| `useQuery` loading spinner on page load | Without a server prefetch, the client issues the fetch after hydration, so first paint always blocks on a round-trip the server already had time to make — a spinner appears on every cold load even though the data was fetchable before the page ever reached the browser. | Server prefetch + `HydrateClient` |
| Single `<Suspense>` for unrelated data | One boundary serializes rendering of everything inside it — the whole subtree waits for the *slowest* fetch to settle before *any* of it paints, even when the fetches are otherwise fully independent (e.g. `UserProfile` blocks `Orders` from appearing). | Parallel Suspense boundaries |
| Duplicate DB calls across RSC tree | Without `cache()`, every component that needs the same record (e.g. `EntityHeader` and `EntityDetail` both calling `getEntity(id)`) issues its own DB round-trip — the query count for one request scales with how many components read the data, not with how much data there is. | `React.cache()` per-request dedup |

## Related Skills

- `react-dev` — useEffect decisions, React 19 APIs, generic components, Server Actions
- `nextjs-app-router` — routing, caching strategies (`fetch()`, ISR, `unstable_cache`), middleware, auth
- `trpc-patterns` — `queryOptions()` / `mutationOptions()` wrappers (required for the patterns above)
