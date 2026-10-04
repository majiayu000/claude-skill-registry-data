---
name: build-saas
description: Build a complete SaaS application with auth, billing, dashboard, and admin panel. Use when Rick says build a SaaS, create a subscription app, or build a platform.
---

# Build SaaS Application

**IMPORTANT**: Before scaffolding, see @project-scaffolding.md for the complete master project template.
All new projects MUST use the full monorepo structure with all critical config files.

## Stack
- Frontend: Next.js 15 App Router + React 19 + Tailwind + shadcn/ui
- Auth: Supabase Auth (email + OAuth)
- Database: Supabase PostgreSQL with RLS
- Payments: Stripe (subscriptions + usage-based)
- Email: Resend or SendGrid
- Deploy: Cloudflare Pages + Workers

## Required Features
1. Landing page with pricing
2. Auth flow (register, login, forgot password, email verify)
3. Onboarding wizard for new users
4. Dashboard with key metrics and charts
5. Settings page (profile, billing, team)
6. Stripe subscription management (upgrade, downgrade, cancel)
7. Usage tracking and limits per plan
8. Admin panel (users, subscriptions, analytics)
9. API with rate limiting per plan tier
10. Webhook handlers (Stripe events)

## Subscription Tiers
- Free: Limited features, usage caps
- Pro: Full features, higher limits
- Enterprise: Custom limits, priority support

## Required Files
- wrangler.toml, Dockerfile, docker-compose.yml
- .github/workflows/deploy.yml
- .env.example
- README.md with RJ branding
