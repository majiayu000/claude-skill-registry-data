---
name: add-react-query
description: Add a typed useQuery or useMutation hook for an existing API endpoint, following the project's TanStack Query conventions. Use when the user asks to "fetch X from the frontend", "call the new endpoint", or "wire up the data".
---

# add-react-query

Wrap an existing API endpoint in a TanStack React Query hook so pages stay clean.

## Inputs to gather

- **Endpoint URL** (e.g. `/api/commissions`)
- **HTTP method** (GET / POST / PATCH / DELETE)
- **Request shape** (query params or body)
- **Response shape** (TypeScript type — pull from the route file or shared types)

## Steps

1. **Read** an existing hook for reference. Default: any hook used by `apps/web/src/pages/platform/leads/index.tsx`.
2. **Decide** whether this is a `useQuery` (read) or `useMutation` (write).
3. **For queries**, the convention is:
   - `queryKey: ['/api/<path>', ...params]`
   - `queryFn` uses the project's `apiClient` (or fetch wrapper) — never raw `fetch`
   - Return type is explicit (`useQuery<MyType[]>`)
4. **For mutations**, the convention is:
   - `mutationFn` calls the API
   - `onSuccess` invalidates the matching query key (`queryClient.invalidateQueries({ queryKey: ['/api/<path>'] })`)
   - `onError` shows a destructive toast (the soft `bg-destructive/10` variant)
5. **Place the hook** in `apps/web/src/hooks/api/use-{name}.ts` if the project has a hooks dir, OR colocate inside the calling page if that's the existing pattern (check before deciding).
6. **Type the response** — pull types from a shared `types/` or generate from the zod schema in the route.
7. **Run `/typecheck`**.

## Verification checklist

- [ ] Query key matches the URL exactly
- [ ] Response type is explicit, not `any`
- [ ] Mutation invalidates the right keys
- [ ] Error path shows a toast (not silent)
- [ ] `/typecheck` passes

## Anti-patterns

- Don't use raw `fetch()` — go through the project's API client so auth headers + base URL are consistent
- Don't put auth tokens in query keys (security risk + breaks caching)
- Don't skip `onSuccess` invalidation — stale lists are a common bug
