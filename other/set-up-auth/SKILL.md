---
name: set-up-auth
description: Use when adding authentication to a frontend SPA — current user as TanStack Query server state, tokens never in localStorage (httpOnly cookies, or in-memory access + refresh cookie), login/logout mutations, one 401-refresh in the fetcher, route guards.
---

# Set Up Auth

## 1. Audit current state

```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null   # frontend.framework, backend.track, package_manager
grep -rn "localStorage.*token\|sessionStorage.*token" src/ 2>/dev/null   # red flag — see step 4
grep -rn "auth/me\|currentUser\|useAuth" src/ 2>/dev/null | head
```

Read `frontend.framework` (guard and hook flavour) and `backend.track`: if the backend is Supabase or another identity provider, use its SDK for the token lifecycle and keep the rest of this skill (see `auth-patterns.md`, When to deviate). **Prerequisites:** `set-up-state-management` (the `fetcher` seam + query-key factory) and `set-up-routing` (guards live in `beforeLoad`/`beforeEach`). Finding tokens in `localStorage` is itself an audit finding — fix it (step 4).

## 2. Decide what to do
- No auth → full setup.
- Tokens in `localStorage` → migrate to cookies / in-memory (step 4) — that's an XSS hole.
- Auth present, no route guards → wire the guard (step 7).

## 3. Detect framework
React → hooks + TanStack Router guard. Vue → composables + Vue Router guard. The token strategy and "user is server state" rule are framework-agnostic.

## 4. Token strategy — never `localStorage`

| Strategy | Where the token lives | Use when | Why |
|---|---|---|---|
| **httpOnly cookie** (preferred) | server-set cookie, JS can't read it | you control the API/domain | XSS cannot read it, so a script injection cannot exfiltrate the session |
| **In-memory access + httpOnly refresh** | access token in a JS variable; refresh token in an httpOnly cookie | cross-domain token API | the long-lived secret is unreadable by JS; the short-lived one dies on reload |

**Never** `localStorage`/`sessionStorage` for tokens — any XSS reads them. With cookies, the `fetcher` sends credentials automatically; add CSRF protection (SameSite=Lax + a CSRF token on unsafe methods). Cookie flags: `HttpOnly; Secure; SameSite=Lax`, `__Host-` prefix where the API shares the origin ([security baseline](../../core/_shared/security-baseline.md)).

Upgrade `src/libs/fetcher.ts` to the **auth version** in [`../_shared/fetcher.md`](../_shared/fetcher.md): `credentials: 'include'` for the cookie, an `X-CSRF-Token` header on unsafe methods, and the 401 refresh from step 8. It builds headers from `new Headers(init?.headers)` *after* spreading `init`, so a caller's own headers can never erase the CSRF token.

## 5. The current user is server state

Define shared query options (usable by both the hook and the route guard). First extend the query-key factory with an `auth` group:

```ts
// src/libs/queryKeys.ts — add alongside the existing `todos` group
export const queryKeys = {
  todos: { /* …existing… */ },
  auth: {
    all: ['auth'] as const,
    me: () => [...queryKeys.auth.all, 'me'] as const,
  },
} as const;
```

```ts
// src/libs/auth.ts  (Vue: import queryOptions from '@tanstack/vue-query')
import { queryOptions } from '@tanstack/react-query';
import { fetcher, HttpError } from '@/libs/fetcher';
import { queryKeys } from '@/libs/queryKeys';

export type User = { id: string; name: string };

export const currentUserQueryOptions = queryOptions({
  queryKey: queryKeys.auth.me(),
  // 401 = signed out, not an error: the guard needs `null` to redirect.
  queryFn: () =>
    fetcher<User>('/auth/me').catch((e: unknown) => {
      if (e instanceof HttpError && e.status === 401) return null;
      throw e;
    }),
  retry: false,
  staleTime: Infinity, // session rarely changes; invalidate on login/logout
});
```
```ts
// src/hooks/useCurrentUser.ts
import { useQuery } from '@tanstack/react-query';
import { currentUserQueryOptions } from '@/libs/auth';

export function useCurrentUser() {
  const query = useQuery(currentUserQueryOptions);
  return { ...query, isAuthenticated: !!query.data };
}
```

## 6. Login / logout as mutations

```ts
// src/hooks/useLogin.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { fetcher } from '@/libs/fetcher';
import { queryKeys } from '@/libs/queryKeys';

export function useLogin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (creds: { email: string; password: string }) =>
      fetcher('/auth/login', { method: 'POST', body: JSON.stringify(creds) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.auth.all }),
  });
}
// useLogout: POST /auth/logout, then queryClient.clear() (drop all cached user data)
```

## 7. Guard routes via the user query

```tsx
// React (TanStack Router): src/routes/dashboard.tsx
import { createFileRoute, redirect } from '@tanstack/react-router';
import { currentUserQueryOptions } from '@/libs/auth';

export const Route = createFileRoute('/dashboard')({
  beforeLoad: async ({ context, location }) => {
    const user = await context.queryClient.ensureQueryData(currentUserQueryOptions);
    if (!user) throw redirect({ to: '/login', search: { redirect: location.href } });
  },
  component: () => <h1>Dashboard</h1>,
});
```
After login, send the user to `redirect` only if it is a same-origin path: starts with `/`, no backslash, and its normalised path does not start with `//` (`/.//evil.com` becomes `//evil.com`). An unchecked value is an open redirect that phishing links abuse.
```ts
// src/libs/safeRedirect.ts
export function safeRedirect(target: unknown, fallback = '/'): string {
  if (typeof target !== 'string' || !target.startsWith('/') || target.includes('\\')) return fallback;
  // Check the path a browser will actually use: '/.//evil.com' normalises to '//evil.com' (protocol-relative).
  const { pathname, search, hash } = new URL(target, 'https://placeholder.invalid');
  return pathname.startsWith('//') ? fallback : `${pathname}${search}${hash}`;
}
```
Vue: in `router.beforeEach`, `await queryClient.ensureQueryData(currentUserQueryOptions)` (or read a Pinia auth store hydrated from it) and redirect if absent.

## 8. Transparent refresh (in-memory token strategy)

On a 401, the `fetcher` calls `/auth/refresh` once, retries the original request, and on failure throws `HttpError(401)` — the guard, not the fetcher, redirects to login. Keep the refresh in the fetcher so call sites never handle expiry — see `auth-patterns.md`.

The code is the `refreshSession` / `retried` part of the auth version in [`../_shared/fetcher.md`](../_shared/fetcher.md). Concurrent 401s share one in-flight refresh promise instead of stampeding, and the original request is retried once. When the refresh fails, the fetcher throws `HttpError(401)`; `currentUserQueryOptions` maps that to `null`, so the guard in step 7 redirects instead of crashing.

## 9. Verify
```bash
pnpm typecheck
```
Log in → protected route loads and `/auth/me` is cached; log out → `queryClient.clear()` empties it and the guard bounces to `/login`. Confirm no token is in `localStorage`/`sessionStorage` (DevTools → Application).

## References
- ./auth-patterns.md — token storage threat model, user-is-server-state, guard-at-the-boundary, 401 refresh, CSRF, third-party providers.
- ../_shared/fetcher.md — the canonical `fetcher`, base and auth versions.
- ../set-up-state-management/SKILL.md — the `fetcher` seam + query-key factory this extends.
- ../set-up-routing/SKILL.md — the guard hook points.
