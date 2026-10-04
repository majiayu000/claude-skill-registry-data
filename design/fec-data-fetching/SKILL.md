---
name: fec-data-fetching
description: "Use when implementing or reviewing frontend server-state flows: typed queries, request caching, invalidation, mutations, optimistic updates, infinite queries, prefetch, SSR hydration, or API-layer integration. Do not use for local UI state or Service Worker caching; Chinese triggers include data fetch, cache, optimistic updates."
---

# Server State data acquisition

## Purpose

Establish clear data acquisition, caching, invalidation and submission boundaries for front-end server state to avoid request state being scattered among page components.

## Procedure

1. Determine the source of the state: use the request caching scheme when it comes from the server and needs caching, deduplication, refreshing, paging or mutation; use component state or store for purely local UI state.
2. First use the existing data acquisition library of the project; when adding dependencies, you can consider TanStack Query for React/Vue/Solid/Svelte, or you can also use SWR, Nuxt/Nitro data acquisition or project encapsulation.
3. Stable design cache key/query key: The structure contains entities, actions and all parameters that affect the results.
4. The API function remains a pure request function, and the data hook/composable is responsible for cache, select, loading/error/empty status.
5. Invalidation after mutation succeeds; use optimistic update when immediate feedback is needed and rollback when failure occurs.

## React Quick Start

```tsx
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function UserList({ keyword }: { keyword: string }) {
  const query = useQuery({
    queryKey: ["users", "list", { keyword }],
    queryFn: () => getUserList({ keyword, page: 1, pageSize: 20 }),
    select: (response) => response.list,
  });

  if (query.isLoading) return <Skeleton />;
  if (query.isError) return <ErrorFallback onRetry={() => query.refetch()} />;
  if (!query.data?.length) return <EmptyState />;

  return query.data.map((user) => <UserRow key={user.id} user={user} />);
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createUser,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }),
  });
}
```

## Detailed reference

Load [references/query-patterns.md](references/query-patterns.md) when it comes to whether you need a query library, QueryClient default configuration, Vue adapter, optimistic updates, infinite scroll queries, prefetching, SSR hydration, and API layer integration.

## Constraints

- The same data must reuse the same cache key/query key; missing parameters will cause cache string reading.
- If `staleTime` is too long, old data will be displayed, and if it is too short, it will cause frequent requests.
- The request cache library does not manage local UI state; do not put modal and input box values into the query cache.
- Optimistic updates must save snapshots and rollback on failure.
- SSR/SSG scenarios must use framework-supported prefetching, hydration, or server-side data boundaries.

## Expected Output

The data acquisition layer has loading/error/empty/data status, repeated requests are automatically deduplicated, the cache is correctly invalidated or rolled back after mutation, and the boundary between the API layer and the UI layer is clear.
