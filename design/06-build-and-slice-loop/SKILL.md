---
name: "build-and-slice-loop"
description: "Implements features in vertical slices, always starting with homepage. Enforces anti-placeholder rules — no lorem ipsum, no TODO stubs, no gray boxes. Real content, real images, real interactions. TypeScript strict mode, Zod validation, and structured file organization."
metadata:
  version: "2.1.0"
  updated: "2026-05-03"
  effort: "high"
  model: "sonnet"
license: "Rutgers"
compatibility:
  claude-code: ">=2.0.0"
  agentskills: ">=1.0.0"
submodules:
  - admin-dashboard.md
  - ai-chat-widget.md
  - blog-and-content-engine.md
  - build-breaking-rules.md
  - chat-native-dashboard.md
  - contact-forms-and-endpoints.md
  - copilot-and-ai-features.md
  - custom-error-pages.md
  - data-tables.md
  - domain-provisioning.md
  - easter-eggs.md
  - empty-states-and-loading.md
  - file-uploads-and-storage.md
  - internationalization.md
  - keyboard-shortcuts-and-command-palette.md
  - microcopy-library.md
  - notification-center.md
  - onboarding-and-first-run.md
  - pre-digested-builds.md
  - pwa-kit.md
  - realtime-and-websockets.md
  - rich-text-editor.md
  - site-search.md
  - stripe-first-donations.md
  - web-manifest-system.md
  - webhook-system.md
priority: 2
pack: "core"
stage: stable
triggers:
  - "build feature"
  - "implement"
  - "slice"
paths:
  - "src/**"
  - "apps/**"
  - "e2e/**"
  - "package.json"
---

# 06 — Build and Slice Loop

Implement features in real vertical slices (UI→API→DB→tests→deploy) starting with the homepage; no placeholders, no stubs.

## Vertical-slice principle

Every iteration ships ONE feature end-to-end through every layer (UI → API → DB → tests → deploy). Never half a feature across two passes.

## Homepage FIRST (every project, no exceptions)

- First slice is always the homepage hero + nav + footer
- Real H1, real meta tags, real OG card, real JSON-LD
- Deploy before adding any other route — establishes design system, auth layer, analytics tier, deploy pipeline
- Per `rules/website-build-doctrine.md` Phase 0 / Phase 1

## Anti-placeholder (NON-NEGOTIABLE)

- ❌ Lorem ipsum
- ❌ TODO / FIXME / TBD in shipped user-visible strings (source-comment TODOs OK per `rules/todos-are-roadmap.md`)
- ❌ Gray placeholder boxes / silhouettes
- ❌ "Coming soon" without firm date
- ❌ Stub images / generic SVGs
- ❌ "John Doe" / "Jane Doe" / "company.com" / "example.com"
- ❌ Bracket placeholders `[Insert Name]` / `[Your Title]`
- ❌ Single-character "x" / "?" labels

Per `rules/copy-writing.md` § Production-review copy gate. Build validator greps `dist/` for these patterns.

## Slice contract (every slice ships ALL of these)

1. **Types** + **Zod schemas** at boundaries (`rules/zod-everywhere.md`)
2. **Contract-first API** (typed request/response)
3. **Loading + empty + error + success states** (4-state system per `10-experience-and-design-system`)
4. **Accessibility** (axe 0 violations + WCAG 2.2 AA per `_kernel/standards.md#wcag22`)
5. **6-breakpoint responsive** (per `_kernel/standards.md#breakpoints`)
6. **Observability** (Sentry breadcrumb + PostHog event + Workers Trace span)
7. **Tests** (Vitest unit + Playwright E2E from homepage outward per `rules/e2e-testing.md`)
8. **Feature flag** where rollout risk exists (`rules/feature-flags.md`)
9. **Tenant isolation** (`org_id` on every row + every query, 404 on mismatch)
10. **Docs** (JSDoc on exports + module README)

## File organization

### Worker (Hono)

```
src/worker/
├── index.ts              # entry — Sentry wrapper, route mounts, onError, notFound
├── db/
│   ├── schema.ts         # Drizzle source of truth
│   └── index.ts          # getDb helper
├── routes/<feature>.ts   # Hono sub-app per feature
├── lib/<feature>.ts      # business logic
├── middleware/           # auth, tenant, rate-limit
└── types.ts              # Env + Variables
```

### Frontend (React + Vite)

```
src/web/
├── main.tsx              # entry — router, providers
├── pages/<Page>.tsx      # one per route
├── components/
│   ├── ui/               # shadcn primitives
│   ├── <feature>/        # feature-specific components
│   └── shared/           # Header, Footer, ErrorBoundary
├── lib/                  # api client, auth context, hooks
└── styles.css            # Tailwind + design tokens
```

### Shared

```
src/shared/
├── plans.ts              # pricing tiers
├── design-styles.ts      # design tokens shared web + worker
└── pageLayout.ts         # shared layout helpers
```

### Tests

```
e2e/
├── FEATURES.md           # row-per-feature matrix (CI gate)
├── _fixtures/            # page objects
├── _helpers/             # snapshot, axe, breadcrumbs, visual
├── <feature>/
│   ├── happy-path.spec.ts
│   ├── edge-cases.spec.ts
│   ├── a11y.spec.ts
│   └── visual.spec.ts
└── _smoke/               # cross-feature smoke
```

## Build loop (per slice)

1. **Write failing test** (Playwright TDD-RED first per `rules/e2e-testing.md`)
2. **Author migration** (`drizzle/0NNN_<feature>.sql`) + update `db/schema.ts`
3. **Apply locally** (`npm run db:apply:local`)
4. **Implement** (route, lib, page, components)
5. **Typecheck** (`npm run typecheck` clean)
6. **Unit tests** (`npm test` green)
7. **Run dev** (`npm run dev`) — exercise in browser
8. **Deploy** (`npm run deploy`)
9. **Prod E2E** (`npm run e2e:prod` against PROD_URL)
10. **Verify console** (zero errors, zero CSP violations, zero failed resources)
11. **AI vision QA** (6bp screenshots → vision rubric ≥9/10)
12. **Commit + push** (conventional commits per `rules/main-only-branch.md`)
13. **Update `e2e/FEATURES.md`** + CHANGELOG

## Real content sourcing

- Copy: brand voice per `09-brand-and-content-system`; never AI-default phrasing
- Images: real photos > AI-generated brand-aligned > zero (skill 12)
- Data: real API / Workers AI / D1 query > mocked
- Testimonials: real attribution > none (never fabricated)
- Stats: cited per `rules/citations.md`

## When to stop adding sections

Per `rules/website-build-doctrine.md` Phase 2: keep adding until next would dilute. Stop when "next hurts," never "we have enough."

## See submodules: vertical-slice.md, file-organization.md, anti-placeholder.md.
