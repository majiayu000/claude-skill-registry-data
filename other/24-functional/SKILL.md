---
name: "functional"
description: "What every delivered app must DO — anti-placeholder, complete features, working forms, psnotify notifications, feature flags, embarrassingly-easy UX, the feature catalog."
triggers:
  - "feature"
  - "build"
  - "form"
  - "functionality"
priority: 2
pack: "core"
stage: stable
---

# Functional — what every delivered app must DO

## Anti-placeholder (NON-NEGOTIABLE)

- No lorem ipsum · no TODO/FIXME/TBD in shipped user-visible strings · no gray placeholder boxes/silhouettes · no "coming soon" without a firm date · no stub/generic images · no "John Doe"/"example.com" · no `[bracket placeholders]` · no single-char labels. Real content, real images, real interactions only.

## Every feature complete (vertical slice)

- Ships end-to-end (UI → API → DB → tests → deploy) — never half a feature across passes. Homepage first (real H1/meta/OG/JSON-LD), deployed before any other route.
- Each feature carries: typed + Zod-validated boundaries · all four states (loading · empty · error · success) · tenant isolation (`org_id` on every row + query; 404 on mismatch, never 403).

## Forms

- Every form submits to a real endpoint (Turnstile + Zod + Amazon SES or D1) and CONFIRMS success. Test an ACTUAL submission — a form that silently fails is a broken feature.

## Notifications

- In-app via psnotify: bell + unread count + center (history/filter/mark-read) + per-channel/per-category preferences. Trigger at meaningful state transitions (build/deploy/domain/AI/billing/team). Toasts ephemeral; the center is the durable record.

## Feature flags

- Every non-trivial / post-launch feature ships behind a typed flag (`enabled=0, rollout=0, stage='experimental'`). Admin promotes via `/admin/feature-flags`. Server guard returns 404 (never 403) when off; UI renders nothing.

## Embarrassingly easy (SUPREME)

- A busy non-technical owner succeeds first try, no manual. ≤3 steps to any outcome · one primary CTA per screen · empty states are first-action launchpads · instant feedback + undo · never a doomed/dead control (disable with the reason + fix, or hide) · the user's words, never internal jargon. Every change leaves the surface easier, never harder.

## Feature catalog (build blocks, as the app needs)

- Admin dashboard · blog/content engine · data tables · site search · file uploads · i18n · PWA (manifest + offline + A2HS) · realtime/websockets · rich-text editor · onboarding/first-run · Cmd+K command palette (every clickable action has a shortcut) · webhooks (signed, verified) · AI chat/copilot · branded 404/500 · custom domains (`{slug}.projectsites.dev` + custom, SSL).

## Real content

- Real photos > AI-generated brand-aligned > none. Real data (API / Workers AI / D1) > mocked. Real testimonials with attribution; cited stats. Never fabricated.
