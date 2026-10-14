---
name: nextjs
description: "Next.js App Router: Server/Client components, Server Actions, Route Handlers, middleware, loading/error/layout, cache/revalidation/streaming. Feature-first, ports-adapters, mappers, contracts."
---

# nextjs

App Router by generation: detect the major, then follow its rules — Server by default, client at the leaves.
## Inspection

Confirm the Next.js major, router generation (App vs Pages), rendering per route, data-fetching sites, and cache/revalidation config.

## Decision rules

App Router rules for App projects (never mix generations); Server Components default; fetch on server with explicit cache policy; metadata per route.


## Activate when

- Building or changing Next.js apps: routing, fetching, caching, actions, middleware, deployment.

## Do NOT activate for

- Plain React without Next.js (see react); Pages-vs-App generation choice without version facts (research first).

## Procedure

1. Version: detect Next.js major from package.json; research in https://nextjs.org/docs for THAT major (Pages vs App patterns never mix; middleware/proxy naming is generation-sensitive).
2. Components: Server Components default; `"use client"` at interactive leaves; server data passed as props/children, never mirrored into state.
3. Data: fetch on the server with cache/revalidation chosen per route; Server Actions for mutations with validation; Route Handlers for API surface.
4. UX states: loading/error/not-found boundaries per segment; streaming for slow sections; metadata per route (see frontend/technical-seo).
5. Structure: `app/` holds routing files only; domain code in feature modules (see architecture/language-modularity).
6. Deploy: environment parity, ISR/cache semantics understood, bundle measured.
7. Verify: build clean, no client-only APIs on server paths, cache behavior demonstrated, states rendered.

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (nextjs, vercel, react).

## Failure modes

Pages patterns pasted into App Router; client components at page root killing streaming; uncached fetches on hot routes; middleware as sole authz.

## Escalation

Rendering/architecture → frameworks/react; SEO specifics → frontend/technical-seo.
