---
name: routing-tanstack-router
description: File-based routing conventions with TanStack Router — route files, search param validation, loaders, and error boundaries.
paths: ["src/routes/**"]
---

- Routes are files under `src/routes/`; `src/routes/__root.tsx` is the shared layout
  (`createRootRoute`, renders `<Outlet />`). A new top-level page is
  `src/routes/<name>.tsx` using `createFileRoute("/<name>")({ component })`.
- The route tree (`src/routeTree.gen.ts`) is **generated** by the `@tanstack/router-plugin`
  Vite plugin on every `dev`/`build` run — never hand-edit it. It is committed to the repo
  (not gitignored) so a fresh clone type-checks before the first `vite build` regenerates it.
- Search params: validate with a Standard-Schema-compatible library (Zod ≥3.24 or Arktype) —
  no adapter package needed, TanStack Router reads the schema directly via `validateSearch`.
  Never read `location.search` manually.
- Data fetching belongs in TanStack Query hooks (`server-state-tanstack-query` skill) called
  from the route's component, not in a router `loader`, unless the data must block navigation
  (e.g., an auth guard) — prefer `useSuspenseQuery` + a `<Suspense>` boundary in the component
  for everything else, matching `src/routes/index.tsx`.
- Every route component needs an `aria-labelledby`'d landmark and an `<h1>` matching the page
  purpose (see `src/routes/index.tsx`, `about.tsx`) — a11y-auditor checks this on route-level
  scans.
