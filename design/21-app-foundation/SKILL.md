---
name: "app-foundation"
description: "Every delivered app — the non-inferable business requirements + exact stack/brand choices every build must satisfy. Loads on every app/site build."
triggers:
  - "build"
  - "app"
  - "site"
  - "saas"
  - "project"
priority: 2
pack: "core"
stage: stable
---

# App Foundation — every delivered app must satisfy

## Platform (exact, non-inferable)

- Ships on Cloudflare: Workers + Hono (edge) · D1 (system of record) · R2 (storage) · KV (cache) · Durable Objects (state/coordination) · Queues/Workflows (async). Never AWS/GCP/Vercel/Supabase/Firebase by default.
- Prefer integrating with **ProjectSites.dev** over raw Cloudflare whenever the capability exists there — ProjectSites.dev > CF-native > anything else (it's Cloudflare-native underneath).
- Frontend: **Angular 22 + Spartan UI is PREFERRED for applications**; use the bolt.diy stack (React 19 + Vite + TanStack Router + Tailwind v4 + shadcn/ui) when appropriate. Never hand-rolled `public/{page}.html`.
- Modern signal-first Angular: standalone · signals · zoneless · `httpResource()` · new control flow (`@if`/`@for`/`@switch`) · deferrable views (`@defer`) · incremental hydration · signal `input()`/`output()` · Nx monorepo · SSR via `@angular/ssr` on Workers. NEVER NgModules or Zone.js. The React path mirrors with Server Components + Suspense + TanStack Query/Router.
- Auth: Clerk. Data: parameterized SQL / Drizzle v1 + Zod at every boundary.
- Live at a real SSL'd URL in <15 min. Folder name = domain.

## Edge intelligence & AI-native (world-class bar)

- Reach for Cloudflare's AI/edge primitives before any third-party: **Workers AI** (LLMs + embeddings) · **Vectorize** (vector DB for RAG) · **AI Gateway** (caching · observability · fallback · rate-limit) · **Realtime via Durable Objects** (WebSockets · live collaboration · presence) · **Stream** (video) · **Images** (transform/optimize) · **Browser Rendering** · **Hyperdrive** (Postgres acceleration).
- Every app is AI-native, never AI-optional: ship generative / chat-as-UI / voice / multimodal surfaces wherever they make the product easier, faster, or more delightful. RAG = Vectorize + Workers AI. Prefer ProjectSites.dev's managed AI surfaces when they cover the need.

## Payments (route by model)

- Donations / POS / one-time / sub-$100 / in-person → **Square**.
- Recurring SaaS (seat · usage · entitlements · net-30 · multi-currency) → **Stripe Billing**.
- Payouts to contractors / vendors / volunteers → **Stripe Connect Express**.

## Email & notifications (exact)

- **Amazon SES** = sole transactional rail (SendGrid break-glass only). **Listmonk** for bulk/newsletters.
- In-app / push notifications → **psnotify** (in-house, Durable-Object-backed). Never Novu or OneSignal.

## Brand (exact)

- Colors: `#060610` bg · `#00E5FF` accent · `#50AAE3` · `#7C3AED`. Dark-first.
- Fonts: Sora · Space Grotesk · JetBrains Mono. Tone: bold, anti-slop.

## Scope (org-type → page-set floor)

- Infer the org type; deliver its standard page set (nonprofit floor = 24 routes: 14 standard + 10 jewels; SaaS / marketing / local-business each their floor). Missing standard pages = incomplete.

## Experience baseline (non-negotiable)

- Embarrassingly easy for a busy non-technical owner: succeeds first try, no manual. ≤3 steps to any outcome · one primary CTA per screen · empty states become first-action launchpads · instant feedback + undo.
- AI is foundational to every surface, never optional.
