---
name: set-up-routing
description: Use when adding client-side routing to a frontend SPA — wires TanStack Router (typed, file-based, React) or Vue Router (Vue) with lazy route code-splitting, loaders that prefetch into the TanStack Query cache, per-route error + pending UI, and a guard pattern for protected routes.
---

# Set Up Routing

## 1. Audit current state

```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null   # frontend.framework, frontend.meta, package_manager
grep -E '"(@tanstack/react-router|react-router|vue-router|@tanstack/router-plugin)"' package.json 2>/dev/null
ls src/routes src/router src/routeTree.gen.ts 2>/dev/null
```

Read `frontend.framework` (react → TanStack Router, vue → Vue Router) and `package_manager` (commands below use pnpm; translate). `frontend.meta` of `nuxt` or `next` means the framework owns routing: stop and say so, this skill is for Vite SPAs. Detect an existing router (react-router, TanStack Router, vue-router). **Prerequisites:** `@/` alias, `set-up-state-management` (loaders prefetch into its query cache), and ideally `set-up-error-boundaries` (route `errorComponent` reuses its `ErrorFallback`).

## 2. Decide what to do
- No router → full setup.
- react-router present, migrating → see `routing-patterns.md` (migration is deliberate, not silent).
- Router present → add the missing pieces (loaders, guards, per-route error UI).

## 3. Detect framework
React → **TanStack Router** (file-based, fully typed). Vue → **Vue Router 5** (typed file-based routing is built in via `vue-router/vite`; opt in per `routing-patterns.md`). Why each: `routing-patterns.md`.

## 4. Install

### React
```bash
pnpm add @tanstack/react-router
pnpm add -D @tanstack/router-plugin
```

### Vue
```bash
pnpm add vue-router
```

## 5. React — TanStack Router (file-based)

Add the router plugin **before** the React plugin in `vite.config.ts`:
```ts
import { defineConfig } from 'vite';
import { tanstackRouter } from '@tanstack/router-plugin/vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    tanstackRouter({ target: 'react', autoCodeSplitting: true }),
    react(),
    tailwindcss(),
  ],
});
```

Root route carries the `queryClient` in typed context:
```tsx
// src/routes/__root.tsx
import { createRootRouteWithContext, Outlet } from '@tanstack/react-router';
import type { QueryClient } from '@tanstack/react-query';

export interface RouterContext {
  queryClient: QueryClient;
}

export const Route = createRootRouteWithContext<RouterContext>()({
  component: () => <Outlet />,
});
```

A route prefetches its data in a loader (warming the same cache `useTodos` reads) and renders error/pending UI itself:
```tsx
// src/routes/index.tsx
import { createFileRoute } from '@tanstack/react-router';
import type { TodoFilters } from '@/libs/queryKeys';
import { todosQueryOptions } from '@/hooks/useTodos';
import { ErrorFallback } from '@/components/atoms/ErrorFallback';

const filters: TodoFilters = { status: 'all' };

export const Route = createFileRoute('/')({
  loader: ({ context }) =>
    context.queryClient.ensureQueryData(todosQueryOptions(filters)), // same object the hook uses
  errorComponent: ({ error }) => <ErrorFallback error={error} />,
  component: () => <h1 className="text-3xl font-bold">Todos</h1>,
});
```

Wire the generated route tree, inject context, and register the type:
```tsx
// src/main.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider, createRouter } from '@tanstack/react-router';
import { QueryClientProvider } from '@tanstack/react-query';
import { routeTree } from './routeTree.gen';
import { queryClient } from '@/libs/queryClient';

const router = createRouter({
  routeTree,
  context: { queryClient },
  defaultPreload: 'intent', // preload on hover/focus — instant navigation
  defaultPreloadStaleTime: 0, // Query owns freshness; the router must not keep a second cache
  scrollRestoration: true,
});

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>,
);
```

`autoCodeSplitting` lazy-loads each route; the file-based plugin generates `routeTree.gen.ts`. **Commit it** and exclude it from Biome: `tsc` in CI runs before any build and needs the file (`configure-ci`).

## 6. Vue — Vue Router (lazy + guards)

```ts
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: () => import('@/components/pages/HomePage.vue') },
    {
      path: '/dashboard',
      name: 'dashboard',
      meta: { requiresAuth: true },
      component: () => import('@/components/pages/DashboardPage.vue'), // lazy
    },
  ],
});
```
```ts
// src/main.ts
app.use(router);
```
Components fetch with the `useTodos` composable. Optional, still experimental in Vue Router 5: typed file-based routes (`vue-router/vite` plugin, replaces `unplugin-vue-router`) and Data Loaders (`vue-router/experimental`).

## 7. Protected routes — guard, don't gate in components

```tsx
// React: src/routes/dashboard.tsx
import { createFileRoute, redirect } from '@tanstack/react-router';
import { currentUserQueryOptions } from '@/libs/auth'; // provided by set-up-auth

export const Route = createFileRoute('/dashboard')({
  beforeLoad: async ({ context, location }) => {
    const user = await context.queryClient.ensureQueryData(currentUserQueryOptions);
    if (!user) throw redirect({ to: '/login', search: { redirect: location.href } });
  },
  component: () => <h1>Dashboard</h1>,
});
```
```ts
// Vue: src/router/index.ts
import { queryClient } from '@/libs/queryClient';
import { currentUserQueryOptions } from '@/libs/auth'; // provided by set-up-auth

router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) return true;
  const user = await queryClient.ensureQueryData(currentUserQueryOptions);
  return user ? true : { name: 'login', query: { redirect: to.fullPath } };
});
```
`currentUserQueryOptions` comes from `set-up-auth`; the guard reads the user through the query cache (deduped with the component's `useCurrentUser`). This skill defines the guard *shape*; auth wires the source. A guard only hides UI: the API must enforce authorization too.

## 8. Verify
```bash
pnpm typecheck   # typed routes compile
pnpm dev            # navigate; loaders prefetch, hover preloads
```

## References
- ./routing-patterns.md — typed routes, lazy splitting, loader↔Query, guards, per-route error/pending UI, the routes/-vs-atomic-pages decision, react-router migration.
- ../_shared/conventions.md — `@/` alias; the `pages/` vs `routes/` note.
- ../_shared/stack-versions.md — runtime-dep versioning.
