---
name: nextjs-best-practices
description: Use when structuring Next.js App Router code — deciding Server vs Client Components, data fetching, folder layout, error/loading states, env access, naming. Enforces clean-code conventions.
---

# Next.js Best Practices

## Server vs Client Components

- Server Components are the default. Add `"use client"` only when a component
  needs interactivity, React hooks, or browser-only APIs.
- Push `"use client"` as far down the tree as possible — keep pages and layouts
  as Server Components and isolate client behavior in small leaf components.

## Directory layout

- `app/` — routes, layouts, route handlers only.
- `components/{ui,features,layouts}` — `ui` for generic presentational pieces,
  `features` for feature-specific composites, `layouts` for page shells/nav.
- `lib/` — framework-agnostic helpers and pure logic.
- `hooks/` — reusable client-side hooks (`use*`).
- `services/` — data-fetching / API-integration layer, called from Server
  Components or Route Handlers.
- `types/` — shared TypeScript types.

## Data fetching & caching

- Fetch data from the service layer, not ad hoc inside components.
- Be explicit about caching intent on every fetch: `no-store` (always fresh),
  `force-cache` (static), or `revalidate: <seconds>` (ISR). Don't rely on the
  implicit default.

## Error & loading states

- Provide `error.tsx` and `loading.tsx` at the route-segment level where a route
  can fail or take noticeable time.

## Environment & config

- Validate environment variables at boot (fail fast on missing/invalid config),
  and centralize access through a single config module rather than scattering
  `process.env.X` reads.

## Naming conventions

- Components: `PascalCase`.
- Hooks: `use*` camelCase.
- Utility functions: `camelCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Types/interfaces: `PascalCase`.

## Misc

- Use `next/image` for images and `next/dynamic` for code-splitting heavy or
  optional client components.
- Lint with `next/core-web-vitals` (ESLint) and format with Prettier.
- Keep components under roughly 200 lines; split when they grow past that.

---
Source: dev.to (sizan) — nextjs-clean-code-best-practices-for-scalable-applications
