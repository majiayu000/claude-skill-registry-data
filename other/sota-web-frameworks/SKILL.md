---
name: sota-web-frameworks
description: >-
  State-of-the-art engineering rules (2026) for the JavaScript SSR meta-frameworks:
  React 19 + Next.js (App Router, React Server Components, Server Actions) and Vue 3 +
  Nuxt 4 (Nitro server routes, composables) — plus the cross-cutting concerns of
  server rendering: hydration correctness, SSR state serialization, the server/client
  trust boundary, and framework-specific security and CVEs. Use when building or
  auditing any React/Next or Vue/Nuxt app — components, RSC/client boundaries, Server
  Actions or Nitro routes, data fetching and caching, hydration mismatches, SSR/SSG/ISR
  strategy, or framework CVE exposure. Complements sota-javascript-typescript,
  sota-frontend-design, sota-code-security, and sota-performance. Trigger keywords:
  React, Next.js, App Router, React
  Server Components, RSC, Server Actions, use client, use server, Vue, Nuxt, Nitro,
  Pinia, composable, script setup, SSR, hydration, hydration mismatch, use cache, PPR,
  ISR, proxy.ts, middleware, useFetch, useState, runtimeConfig, CSP nonce, devalue.
---

# SOTA Web Frameworks (2026)

## Purpose

This skill encodes the 2026 state of the art for the two dominant JavaScript SSR
stacks — **React + Next.js** and **Vue + Nuxt** — and the server-rendering concerns
they share. It is deliberately framework-specific: the traps that matter here
(the RSC server/client boundary, Server Actions as public endpoints, hydration
mismatches, SSR state leaking across requests, `runtimeConfig`/`NEXT_PUBLIC_`
secret boundaries) do not exist at the plain-language level.

Two modes:

- **BUILD** — writing or modifying components, routes, and data-fetching to this standard.
- **AUDIT** — reviewing an existing app and reporting findings.

Read SKILL.md fully; load `rules/*.md` on demand per the index below. **Verify every
version/CVE claim at use time** — this file's facts were primary-sourced 2026-07 but
framework security moves weekly (see the 2025-12 React Server Components RCE).

## Scope boundaries (what lives elsewhere)

This skill stacks *on top of* the general skills — load them together, don't duplicate:

- **`sota-javascript-typescript`** — strict `tsconfig`, type design, promises,
  Node hardening, npm supply chain. The *language*; this skill is the *framework*.
- **`sota-frontend-design`** — visual design, layout, components-as-UX, WCAG 2.2
  accessibility, motion. This skill covers component *engineering*, not *design*.
- **`sota-code-security`** — generic XSS/CSRF/SSRF/authn/authz/crypto theory. This
  skill covers the *framework-specific* expression of those (RSC data exposure,
  Server Action authz, `v-html`, next/image SSRF).
- **`sota-performance`** rules/06 — Core Web Vitals, bundle budgets, image/font
  loading. This skill covers render-strategy choice (SSR/SSG/ISR/PPR) and hydration.
- **`sota-api-design`** — REST/GraphQL contract design for the routes themselves.

## BUILD mode

1. **Establish context first.** Read `package.json` for the exact React/Next or
   Vue/Nuxt majors and the render mode in use (App vs Pages Router; Nuxt SSR vs
   `ssr: false`). Match the project's baseline — no Server Actions on a Pages-Router
   app, no `defineModel` below Vue 3.4. Confirm the versions are supported and
   patched against the CVE tables in `rules/03`/`rules/05`. (`rules/01`)
2. **Default to the current idiom:** React function components + hooks (let the React
   Compiler memoize — don't hand-write `useMemo` everywhere); Vue Composition API with
   `<script setup>`. Server Components by default in Next App Router, `"use client"`
   only at the leaves that need interactivity. (`rules/02`, `rules/04`)
3. **The server/client boundary is a security boundary, not just a perf one.** Every
   prop crossing server→client is serialized into the HTML/RSC payload and is public.
   Authorization lives *next to the data* (a Data Access Layer / validated server
   route), never only in middleware or a layout. (`rules/03`, `rules/07`)
4. **Treat every Server Action and Nitro route as a public, unauthenticated HTTP
   endpoint** until it validates input and checks authz itself — even if it looks
   internal or is never imported. (`rules/03`, `rules/05`, `rules/07`)
5. **Get hydration right by construction:** deterministic render (no `Date.now()`,
   `Math.random()`, or `window` in render), stable IDs via `useId`, SSR-safe shared
   state (`useState`/per-request instances, never module-level refs). (`rules/06`)
6. **Serialize SSR state safely** (framework serializer or escaped JSON, never naked
   `JSON.stringify` into `<script>`) and **wire CSP** (nonce or hash) knowing it forces
   dynamic rendering in Next. (`rules/06`, `rules/07`)
7. **Tests accompany code** (`sota-testing`): component tests plus at least one test
   that exercises the server/client boundary or a server route's authz.

## AUDIT mode

1. **Fingerprint + patch-check first.** Pin exact framework/loader versions from the
   lockfile and diff them against the CVE tables in `rules/03` and `rules/05`. An
   unpatched React2Shell (CVE-2025-55182) or middleware bypass (CVE-2025-29927) is
   CRITICAL on its own, before any code is read.
2. **Trace the trust boundary.** Grep `"use client"`/`"use server"`, `defineProps`,
   `runtimeConfig`, `NEXT_PUBLIC_`/`NUXT_PUBLIC_`; find where server data crosses to
   the client and where authz is enforced. Middleware/layout-only authz is a finding.
3. **Run each relevant rules file's Audit checklist** (grep-driven), then read for
   design: hydration determinism, SSR state isolation, caching of personalized pages.
4. **Verify every finding** — a `v-html` fed a constant is not XSS; a Server Action
   that re-checks the session is not IDOR. Note mitigations already present.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| CRITICAL | Exploitable now / RCE / data loss | Unpatched RSC deserialization RCE; middleware-bypass auth on the only authz layer; secret in `NEXT_PUBLIC_`/`public` runtimeConfig; `unserialize`-class sink |
| HIGH | Exploitable with preconditions | Server Action / Nitro route with no authz (IDOR); SSRF via next/image `**` or user-URL fetch; `dangerouslySetInnerHTML`/`v-html` of user data; whole-DB-row as a client prop |
| MEDIUM | Real but bounded, or reliability | Personalized SSR page cacheable at a shared CDN; hydration mismatch on user data; missing CSP; module-level SSR state; unpatched non-critical CVE |
| LOW | Deviation from SOTA | Pages Router for greenfield; hand-rolled memoization vs React Compiler; `$fetch` double-fetch in setup; Options API for a new app |
| INFO | Worth knowing | Newer render mode available; migration opportunities |

### Finding format

```
file:line | rule violated (rules/NN §S) | severity | effort | fix
```

Effort: trivial · small · medium · large. Group by severity, CRITICAL first.
Borderline severities state the deciding assumption; unconfirmed findings are
marked "needs verification", never asserted. End with per-severity counts, the
sweep commands run, and explicit "checked and clean" areas.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-baseline.md` | choosing or verifying a stack and version floor (React/Next/Vue/Nuxt support+EOL matrix), picking a render mode (CSR/SSR/SSG/ISR/PPR), project setup, React Compiler |
| `rules/02-react.md` | writing React components: hooks rules, `useId`/`useEffect`/refs, Suspense & error boundaries, `use()`/Actions/`useActionState`, memoization & the React Compiler, `dangerouslySetInnerHTML` |
| `rules/03-nextjs.md` | Next.js App Router: Server vs Client Components, Server Actions, the caching model (`use cache`/Cache Components/PPR/ISR/`revalidate`), `proxy.ts`/middleware, the Data Access Layer, and Next CVEs |
| `rules/04-vue.md` | writing Vue: Composition API & `<script setup>`, reactivity pitfalls (props destructure, `shallowRef`, watchers, `effectScope`), `defineModel`, TypeScript, and Vue XSS (`v-html`, template injection) |
| `rules/05-nuxt.md` | Nuxt 4: data fetching (`useFetch`/`useAsyncData`/`$fetch`), `useState`, `runtimeConfig`, Nitro server routes & auth, `routeRules`/hybrid rendering, islands, and Nuxt/Nitro/h3/IPX CVEs |
| `rules/06-ssr-hydration.md` | anything SSR: hydration mismatches & determinism, SSR state-serialization XSS, cross-request state pollution, caching personalized pages safely, CSP with streaming SSR |
| `rules/07-security.md` | a security pass: the server/client secret boundary, authorization placement (post-CVE-2025-29927), SSRF surfaces, the consolidated framework CVE reference, and supply-chain notes |

## Top-10 non-negotiables

1. **Run supported, patched majors.** React ≥ 19.x, Next ≥ 16.x for new code (15.x
   Maintenance LTS ends 2026-10-21), Vue ≥ 3.5, Nuxt ≥ 4.x (Nuxt 3 EOL since
   2026-07-31). Cross-check the CVE
   tables — an unpatched RSC RCE (CVE-2025-55182) or middleware bypass
   (CVE-2025-29927) is a ship-stopper. (`rules/01`, `rules/03`, `rules/05`)
2. **Authorization lives next to the data, never only in middleware or a layout.**
   `proxy.ts`/middleware is an optimization, not the auth layer; each Server Action,
   Route Handler, and Nitro route re-checks authn + authz. (`rules/03`, `rules/07`)
3. **Every prop that crosses server→client is public.** It's serialized into the RSC
   payload / HTML. Pass minimal DTOs, never raw DB rows, tokens, or `process.env`.
   (`rules/03`, `rules/07`)
4. **Server Components by default; `"use client"` only where interactivity requires
   it.** Keep secrets and data access in Server Components / server-only modules
   (`import 'server-only'`). (`rules/02`, `rules/03`)
5. **Secrets never reach the client bundle.** Nothing sensitive in `NEXT_PUBLIC_*`,
   `VITE_*`, or `runtimeConfig.public` — those are inlined at build time. (`rules/07`)
6. **Validate every server-route/action input with a schema** (`getValidatedBody`/Zod;
   never trust `formData`, `searchParams`, or headers), and check resource ownership
   to prevent IDOR. (`rules/03`, `rules/05`)
7. **Hydrate deterministically:** no `Date`/random/`window` in render, stable IDs via
   `useId`, SSR-safe shared state — and never "fix" a mismatch by injecting
   server-side user HTML. (`rules/06`)
8. **Serialize SSR state safely.** Framework serializer (devalue) or `<`-escaped JSON
   in `<script>`; naked `JSON.stringify` into a script tag is XSS. (`rules/06`)
9. **User HTML is dangerous HTML.** `dangerouslySetInnerHTML`/`v-html` only on
   sanitizer output; validate `href`/URL schemes (`javascript:`); lock `next/image`
   `remotePatterns` to explicit hosts (no `**`). (`rules/02`, `rules/04`, `rules/07`)
10. **Don't cache personalized SSR at a shared cache.** `Cache-Control: private` for
    per-user pages; know that CDNs drop `Vary`; wire CSP nonces knowing they force
    dynamic rendering. (`rules/06`)
