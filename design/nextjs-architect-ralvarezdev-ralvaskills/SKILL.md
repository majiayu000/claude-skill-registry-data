---
name: nextjs-architect
version: 1.0.1
description: Next.js 16 standards — App Router only, server components by default with explicit `"use client"` boundaries, server actions for mutations, streaming Suspense, edge vs node runtime, Image/Font/Metadata APIs. Pairs with react-architect. Use when scaffolding or reviewing a Next.js app or auditing server/client boundaries.
---

# Next.js Architecture

Targets **Next.js 16** with **React 19**, **TypeScript strict**, **App Router only**. Builds on [react-architect](../react-architect/SKILL.md) for client-side patterns; this skill covers the Next-specific layers — server components, server actions, routing, data fetching, edge vs node, deployment. Concrete skeletons in [RECIPES.md](RECIPES.md); pinned dependencies in [STACK.md](STACK.md).

## 1. App Router only

The Pages Router is legacy. New code lives in `app/`; if you inherit a Pages Router app, **don't mix** unless mid-migration. Folder layout reference in [RECIPES § App Router folder layout](RECIPES.md#app-router-folder-layout).

Key conventions:

- **`page.tsx`** = the route's UI. **`layout.tsx`** wraps it. Both default to server components.
- **`loading.tsx`** wraps the route in Suspense automatically.
- **`error.tsx`** is a client component that wraps the route in an ErrorBoundary.
- **Route groups (`(name)`)** organize without adding URL segments.
- **`@slot`** is a parallel route — independent loading/error states, rendered into named slots in the parent layout.

## 2. Server components by default, client when needed

Every component is a **server component** unless you opt out with `"use client"`. The choice belongs to the leaf component that needs the client behavior — not the root.

### When to stay server

- Pure rendering — no state, no effects, no event handlers.
- Data fetching — `await db.query(...)`, `await fetch(...)`.
- Secrets / server-only logic — `process.env.STRIPE_SECRET_KEY` *only* loaded in server components.
- Markdown rendering, syntax highlighting, large dependencies you don't want shipped to the browser.

### When to flip to `"use client"`

- `useState`, `useEffect`, `useReducer`, any other hook.
- Browser-only APIs (`window`, `localStorage`, `IntersectionObserver`).
- Event handlers (`onClick`, `onChange`, etc.) — must be in a client boundary.
- Third-party libraries that use any of the above (most chart libraries, animation libraries).

### The boundary rule

- **Server passes data to client as props** — props must be JSON-serializable. Pass IDs, not class instances; pass plain objects, not Date (use ISO strings).
- **One `"use client"` directive** at the top of a file makes that *file* and everything imported into it run client-side. Hoist the directive to the smallest leaf.
- **Don't nest client → server.** Server components can be rendered inside client trees only as `children` props (slot pattern).

Skeleton: [RECIPES § Server / client boundary](RECIPES.md#server--client-boundary).

## 3. Data fetching

### Reads — direct from server components (hybrid default)

Per the project choice: **direct DB access from RSC for reads**, API routes for writes. Cleaner UX (single round-trip), type-safe end-to-end.

- **`getUser` lives in a server-only module** (`@/lib/users.server.ts` or marked with the `"server-only"` import). Prevents accidental bundling of DB code into the client.
- **Use [sql-architect](../../databases/sql-architect/SKILL.md)'s `psycopg + .sql` pattern** when the project's backend convention matches; otherwise use the project's existing data layer.
- **`notFound()`** triggers the closest `not-found.tsx` — proper 404 with the right HTTP status.

**When to flip to API routes for reads:** any of the following — and document the choice per project:

- You want a separate microservice topology (Next is the frontend BFF, backend is its own service).
- The same data is consumed by mobile clients or other web frontends; one HTTP API beats two implementations.
- Auth requirements force the boundary (e.g. backend has access controls direct DB calls can't replicate).

Skeleton: [RECIPES § Read directly from a server component](RECIPES.md#read-directly-from-a-server-component).

### Writes — server actions

Server actions are the canonical mutation pattern. No client-side fetch, no manual JSON handling.

- **`"use server"`** at the top of a file marks every export as a server action — accessible from client components via `import`.
- **Always re-authenticate inside the action.** Don't trust the calling context; verify the session.
- **Validate with Zod** at the boundary — same discipline as REST handlers per [rest-api-architect §7](../../protocols/rest-api-architect/SKILL.md#7-error-contracts--rfc-9457-problem-details).
- **`revalidatePath` / `revalidateTag`** to refresh server-rendered data after a mutation. Without this, the user sees stale state.
- **Return discriminated unions** (`{ok: true, ...} | {ok: false, ...}`) so the client renders success vs. errors based on the field.

Skeleton: [RECIPES § Server action with Zod validation + form binding](RECIPES.md#server-action-with-zod-validation--form-binding).

### TanStack Query — when?

The [react-architect §5](../react-architect/SKILL.md#5-state-management--three-layers) recommendation stands inside client components — but in Next.js the trade-off shifts:

- **Server components fetch on the server.** TanStack Query's "server state cache" benefits don't apply when the page is server-rendered fresh.
- **TanStack Query earns its place in Next when:** there's substantial client-side data fetching (autocomplete, real-time updates, infinite scroll, polling), or you want optimistic UI for mutations beyond what server actions give.

## 4. Streaming with Suspense

Next App Router streams the HTML as RSC chunks resolve. Pair with `<Suspense>` for granular per-region loading.

- **`loading.tsx` is a route-level Suspense.** Per-region Suspense gives finer-grained streaming.
- **`error.tsx` is a route-level ErrorBoundary.** Inline `<ErrorBoundary>` (from `next/error-boundary` or a custom one) for finer scoping.
- **Don't over-stream.** A page with 12 Suspense boundaries appears janky as chunks fill in. Target the genuinely slow regions.

Skeleton: [RECIPES § Per-region streaming with Suspense](RECIPES.md#per-region-streaming-with-suspense).

## 5. Edge vs Node runtime

Each route can declare its runtime via `export const runtime = "edge" | "node"`. Defaults to `node`.

- **Default `node`** — full Node API, npm packages with native modules, deepest compatibility.
- **`runtime = "edge"`** for low-latency, geographic-edge routes — auth verification, redirects, feature flags, A/B routing.
- **Edge restrictions:** no Node-only modules, no native bindings, smaller bundle limit. DB drivers vary — standard Postgres drivers don't work on edge.

Declaration + edge-compatible driver notes in [RECIPES § Edge runtime declaration](RECIPES.md#edge-runtime-declaration).

## 6. Metadata, Images, Fonts

### Metadata

- **Per-route `generateMetadata`** — async, runs on the server, has access to params.
- **Root `metadata` export** in `app/layout.tsx` for defaults (title template, OG defaults).
- **Don't hand-write `<head>`** — Next manages it for SEO + social embed correctness.

Example in [RECIPES § Metadata via `generateMetadata`](RECIPES.md#metadata-via-generatemetadata).

### `next/image`

- **Always `next/image`**, never `<img>` in App Router code. Handles responsive sizes, modern formats (AVIF/WebP), lazy loading, no layout shift.
- **Set `width` and `height`** (or `fill` with a sized parent). Prevents CLS.
- **`priority` only on above-the-fold images.** Every image marked priority defeats the optimization.
- **Remote images need `remotePatterns`** in `next.config.ts` — strict allow-list for security.

### `next/font`

- **`next/font/google`** for Google Fonts; subsets + variable axes pinned at build time, no external request.
- **`next/font/local`** for self-hosted fonts.
- **Both eliminate FOIT/FOUT.** Don't use `@import` or `<link rel="stylesheet">` for fonts.

## 7. API routes — when

Server actions cover most mutations. API routes (`app/api/.../route.ts`) earn their place for:

- **Webhooks** — external services (Stripe, GitHub, etc.) POST to your API.
- **External clients** — mobile, public API, partner integrations.
- **Streaming responses** — server-sent events, NDJSON streams.
- **Non-React consumers** — anything that isn't a form submission from your own UI.

Inside API routes, follow [rest-api-architect](../../protocols/rest-api-architect/SKILL.md) — same conventions for status codes, errors (RFC 9457), versioning, idempotency.

## 8. Auth

- **Session-based for first-party apps** — `next-auth` (Auth.js v5) or a hand-rolled cookie session. `httpOnly`, `Secure`, `SameSite=Lax` cookies.
- **Server-side session check** in every protected `layout.tsx` or via middleware. Never trust the client.
- **`middleware.ts`** at the project root runs on every matching route — auth redirects, locale detection, feature flags. Edge runtime.
- **Server actions re-verify** the session — middleware doesn't reach into action handlers reliably.
- **External IdP** (Auth0, Cognito, Clerk) is the typical upgrade path; same [rest-api-architect §11](../../protocols/rest-api-architect/SKILL.md#11-authentication-patterns) trade-offs apply.

## 9. Caching

Next has many cache layers (fetch data cache, full route cache, client router cache, `unstable_cache`). Be deliberate; profile before tuning. Full cache layers + override syntax in [RECIPES § Cache layers reference](RECIPES.md#cache-layers-reference).

Key rules:

- **Don't cache user-specific data globally.** Use `cookies()` / `headers()` to opt out, or scope the cache to the user.
- **`revalidateTag` after mutations** so server-rendered data refreshes when the underlying data changes.
- **Most apps don't need cache surgery** — trust the defaults until something's measurably slow.

## 10. Testing

Same approach as [react-architect §10](../react-architect/SKILL.md#10-testing) plus Next-specific:

- **Component tests** with Vitest + React Testing Library. Server components are rendered to strings by Next — testable in isolation as async functions returning JSX.
- **Server action tests** are unit tests of the action function. Call it with a `FormData` object, assert the return.
- **Playwright** for end-to-end against `next start` (built app) or `next dev` (in CI: build then start).
- **API route tests** invoke the route handler directly with a `Request` object; no HTTP server needed.

## 11. Deployment

- **Vercel** is the path of least resistance — first-class App Router, edge, streaming, ISR.
- **Self-host** via `next start` behind a reverse proxy, or `output: "standalone"` for a tiny Docker image (per [docker-architect](../../infra/docker-architect/SKILL.md)).
- **Static export** (`output: "export"`) when there's no dynamic server logic — drops half of Next's features but enables static hosting.
- **Always set the `NEXT_PUBLIC_*` env conventions** correctly — anything not prefixed is server-only.

## 12. Cross-skill ties

- [react-architect](../react-architect/SKILL.md) — client patterns inside `"use client"` components.
- [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md) — Radix + Tailwind + a11y; design system tokens.
- [rest-api-architect](../../protocols/rest-api-architect/SKILL.md) — API routes follow the same conventions as backend REST services.
- [sql-architect](../../databases/sql-architect/SKILL.md) — direct DB access from RSC uses the same pattern (raw SQL + parameter binding).
- [security-reviewer](../../quality/security-reviewer/SKILL.md) — server actions and API routes are the new attack surface; same audit list applies.
- [observability-architect](../../infra/observability-architect/SKILL.md) — OpenTelemetry instrumentation via `@vercel/otel` or generic OTel SDK; trace_id propagated through RSC boundaries.
