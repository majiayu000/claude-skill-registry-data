---
name: server-state-tanstack-query
description: Conventions for fetching, caching, and mutating server state with TanStack Query — query key shape, Suspense vs plain queries, and optimistic updates.
paths: ["src/lib/queries.ts", "src/lib/**/*queries*"]
---

- Query keys are arrays, most-generic segment first, defined once as a `const ... as const`
  next to the query itself (see `SUBSCRIBERS_KEY` in `src/lib/queries.ts`) — never inline a
  raw array literal at each call site, or cache invalidation will silently miss.
- Default to `useSuspenseQuery` (not `useQuery`) for data a component cannot render without —
  it removes the `isLoading`/`data is possibly undefined` branch entirely at the type level.
  Wrap the consuming component in `<Suspense fallback={...}>` one level up (see
  `src/routes/index.tsx`). Use plain `useQuery` only when the component has a meaningful
  "no data yet" UI state of its own.
- Mutations validate their input against the same Zod schema used at the API boundary
  (`src/lib/schemas.ts`) inside `mutationFn`, not in the calling component — the mutation
  hook is the trust boundary, not the form.
- On mutation success, prefer `queryClient.setQueryData` with the server's actual response
  (see `useSubscribeMutation`) over `invalidateQueries` when the mutation response already
  contains the new state — one fewer network round-trip.
- Every fetch goes through `fetch()` against a relative `/api/...` path with an MSW handler in
  `src/mocks/handlers.ts` backing it in dev and tests (`testing-rtl-msw` skill) — never call an
  absolute external URL directly from a component or hook.
