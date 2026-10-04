---
name: api-communication
description: Best practices for talking to a backend from a web app — a single typed HTTP layer, TanStack Query for server state, auth token injection with a refresh-token queue, endpoint/query-key constants, and consistent error + loading/empty states. Auto-activates when calling an endpoint, writing a data-fetch or mutation hook, or handling auth tokens and API errors. Works with axios or fetch.
---

# API Communication

Goal: all HTTP goes through one typed layer, server state lives in a query cache (not `useEffect`), auth is handled centrally, and errors surface consistently. **Never inline raw `fetch`/`axios` calls in feature/UI code.**

## Layered architecture

1. **One client instance** (axios instance or a `fetch` wrapper) configured with the base URL and an interceptor/middleware that injects shared headers and the auth token.
2. **Thin typed request wrappers** (`get/post/put/patch/delete`) that return the parsed body (`response.data`) and carry generics for request/response types.
3. **Query/mutation hooks** built on **TanStack Query** (`useQuery`/`useMutation`) — feature code calls these, not the client directly.

```ts
// wrappers
export const api = {
  get:  <T, P = unknown>(url: string, params?: P, cfg?: ReqConfig) => client.get<T>(url, { params, ...cfg }).then(r => r.data),
  post: <T, D = unknown>(url: string, data?: D, cfg?: ReqConfig) => client.post<T>(url, data, cfg).then(r => r.data),
  // put / patch / delete …
}
```

## Server state via TanStack Query (not useEffect)

```ts
const { data, isLoading, isError, refetch } = useQuery({
  queryKey: [QUERY_KEYS.RESOURCE, params],         // params in the key → auto refetch on change
  queryFn: ({ signal }) => api.get<Res, Params>(ENDPOINTS.RESOURCE, params, { signal }),
})

const { mutate, isPending } = useMutation({
  mutationFn: (vars) => api.post<Res, Vars>(ENDPOINTS.RESOURCE, vars),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.RESOURCE] }),
  onError: (err) => showError(getApiErrorMessage(err, 'Something went wrong')),
})
```
- Pass the query `signal` to the request so cancelled queries abort in-flight calls.
- Invalidate the relevant query key on mutation success rather than manually refetching.
- Tune `staleTime`/`gcTime`/`enabled` per query; gate dependent queries with `enabled`.

## Constants — never hardcode strings

- **Endpoints** live in a constants module (an enum/object), grouped by area. Replace path params at call time (`ENDPOINTS.ITEM_BY_ID.replace(':id', id)`). Never inline `/v1/...` paths in feature code.
- **Query keys** live in a constants module too; compose stable keys as arrays (`[KEY, scope, params]`) so invalidation is precise.

## Auth: token injection + refresh-token queue

- Inject the access token in a request interceptor; read auth state via the **store's `getState()`**, never a React hook (interceptors run outside React).
- On `401`, run a **single refresh** while **queuing** concurrent failed requests; when the refresh resolves, replay the queued requests with the new token. Guard each request with a one-shot retry flag (e.g. `_retry`) to prevent infinite loops; clear the session and redirect if refresh fails.
- Support **multiple auth contexts** (e.g. user vs admin) with a request-config `authMode` flag that selects which token store/refresh routine to use; use `'none'` for public endpoints.
- Route token persistence through a small storage service — never read/write token keys in `localStorage` directly. Bump a session counter on auth transitions so dependent caches/streams reset cleanly.

## Headers

Inject shared headers centrally (client/app token, device type, language — see [[localization]], and `Authorization` when authenticated). Keep them in the interceptor, not at call sites.

## Error handling & UX

- Centralize message extraction: a `getApiErrorMessage(error, fallback)` that reads the server body (`description` → `message` → field `errors`) and returns the fallback for network/opaque errors.
- Surface errors through the app's notification system in `onError`; provide an opt-out flag (e.g. `unhandled`) for callers that fully own error handling.
- **Every data fetch handles loading, error, and empty states** — no exceptions.

## Don'ts

- Don't inline `fetch`/`axios` in components or feature hooks — use the wrappers/hooks.
- Don't use `useEffect` as the primary data-fetch mechanism — use the query cache.
- Don't hardcode endpoint or query-key strings, and don't touch token storage directly.
- Don't call a React store hook inside an interceptor — use `getState()`.
- Don't roll per-request refresh logic — use the shared refresh queue.

## Project overrides

Always defer to the project's CLAUDE.md/AGENTS.md and its existing client (`fetch` vs axios) and hooks. Match the established wrappers and conventions instead of introducing a parallel approach.
