---
name: launch-plan
description: Build a full launch playbook for a product — PH, HN, X, LinkedIn, email warm-up, cold outreach, pricing, brand assets. Sequenced for compounding signal.
---

# /launch-plan

Usage: `/launch-plan <product-slug>` `[--date=YYYY-MM-DD]`

## What this does
Runs the Launch-stage agents in sequence:
1. **`launch/brand-story-builder`** — positioning, voice, naming
2. **`launch/landing-page-copywriter`** — landing copy
3. **`launch/seo-strategist`** + **`launch/keyword-researcher`** — content + SEO foundation
4. **`launch/pricing-strategist`** — initial pricing
5. **`launch/launch-strategist`** — day-by-day plan with assets
6. **`launch/cold-outreach`** — first-100 outreach templates
7. **`launch/community-builder`** — community decision + plan

Outputs go to `products/<slug>/launch/`.

## What you do as the assistant
1. Resolve `<product-slug>`. Confirm it's at the right stage (`launch` or post-MVP).
2. Read all relevant product context (`prd.md`, `metrics.md`, recent interview synthesis).
3. Run the 7 agents. Some in parallel: brand → (landing + seo + pricing) → launch-strategist → (cold-outreach + community).
4. After all done: produce a "launch readiness checklist" — what's done, what's missing, what's blocking.

## Pre-flight blockers (must clear before launch)
- ✅ Metrics framework wired (PostHog events live in prod)
- ✅ Sentry catching real errors
- ✅ Stripe test card flow works end-to-end
- ✅ Brand assets locked
- ✅ Landing page tested on mobile + desktop
- ✅ Warm list ≥ 50

If any blocker is unmet, the launch plan ships with a "launch blocked, here's what's missing" header.
