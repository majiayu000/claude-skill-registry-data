---
name: "cf-integrations-reference"
description: "The consolidated, world-class Cloudflare + integrations reference — CF platform/data/AI-edge patterns, media pipeline, observability/growth, payments, and the site-generation pipeline. The non-inferable choices that build the greatest web apps."
triggers:
  - "cloudflare"
  - "integration"
  - "media"
  - "analytics"
  - "site generation"
  - "vectorize"
  - "durable object"
priority: 2
pack: "infra"
stage: stable
---

# CF Integrations Reference — the world-class edge stack

> Consolidated reference (merged from the former architecture/media/observability/site-gen packs). The non-inferable Cloudflare-specific + vendor choices. Requirements own the "what"; this owns the "which CF primitive + which vendor."

## Cloudflare platform + data

- Data: **D1** (Sessions API + read replicas; dynamic sitemap from D1) · **R2** · **KV** (60s host/config cache) · **Hyperdrive** (accelerate Neon/Postgres when a CF primitive can't) · **Drizzle ORM** + migrations at the boundary.
- Compute + coordination: **Durable Objects** patterns — rate-limiter · WebSocket/realtime + presence · agent-DO; **Workflows** (durable multi-step) · **Queues** (fallback to Workflows when unbound) · **Browser Rendering** (headless jobs + E2E journeys).
- API: **Hono** RPC-mode + **OpenAPI generation** from Hono. Zod at every boundary.
- Auth + tenancy: **Clerk** (M2M JWT) · Zero Trust Access · enterprise multi-tenancy · multi-tenant subdomain provisioning (`{slug}.projectsites.dev`).
- Provisioning: CF-native products are API-provisionable with the global key (Turnstile/DNS/custom-domains) — never hand-create in the dashboard.

## AI / edge intelligence

- **Workers AI** (Llama + embeddings, FP8) via **AI Gateway** (cache · observability · fallback · rate-limit). **Vectorize** = the vector DB for RAG (RAG = Vectorize + Workers AI).
- Every app is AI-native (per app-foundation): generative / chat-as-UI / voice / multimodal where they add value.

## Media pipeline

- Generation: **Ideogram** (logo · hero · wordmark — tight banner, alpha) + GPT-Image; brand-hex registry per platform.
- Optimization: AVIF + WebP targets, compression pipeline, tiered image profiling, lightbox classifier. Never gray placeholder boxes — every media slot filled (media-slot manifest).
- OG: edge-rendered per-route 1200×630 (og-card / og-image pipeline).
- Rich: **NotebookLM** per-site podcast + infographics; technical diagramming (ASCII / Mermaid / SVG).

## Observability & growth

- Analytics: **PostHog** (server-side; PLG activation funnel; feature-flags + experiments/A-B) — cloud-hosted (never self-host). GA4 only when enterprise.
- Tracing / errors: **Workers Tracing** (OTLP) · **Sentry** alert rules (HTTP API).
- Growth: conversion-optimization patterns; in-app user-feedback widget.
- Bulk email: **Listmonk** (newsletters/campaigns) — the bulk rail (Amazon SES = transactional per app-foundation).

## Payments (route by model — see app-foundation)

- **Stripe Billing** (recurring SaaS: seat/usage/entitlements) · **Stripe Connect** (payouts) · **Square** (donations / POS / one-time / in-person). Never roll your own cart/checkout/inventory (Medusa.js headless when e-commerce).

## Site-generation pipeline

- Flow: research (Google Places / web) → build-prompts → homepage block library → media acquisition → **quality gates** (AI-vision + SEO audits) → source-fidelity loop.
- Coverage: org-type → standard page-set expansion; per-vertical domain features; pSEO templates; local SEO (Google Business Profile + citations).
- Owner UX: non-technical-owner onboarding (zero-code edits); small-business rebuild mode.
- Export/template: bolt-artifact XML envelope; template system = the bolt.diy stack (Vite + React + Tailwind + shadcn) OR Angular per app-foundation.
