---
name: "emdash-skills"
description: "23-category product-building OS. CF Workers+Hono, React 19+Vite / Angular 22+Spartan, D1, Drizzle, Clerk, Square/Stripe. 149 reference docs, 28 agents."
---
# Emdash Skills for Devin

Load CONVENTIONS.md for stack defaults. Load _router.md for skill routing.
23 categories, 149 reference docs, 28 agents.

## Stack
CF Workers + Hono | React 19 + Vite + shadcn/ui (sites) / Angular 22 + Spartan UI (apps) | D1/Neon | Drizzle v1 | Clerk | Square + Stripe Billing/Connect | Inngest | Amazon SES | Bun | Playwright v1.59+ | PostHog | Sentry

## Rules
- TypeScript strict, never `any`, prefer `interface` over `type`
- Hono inline handlers for RPC type inference
- Zod validation on all inputs
- TDD: failing test first, Playwright 6 breakpoints
- Dark-first design, #060610 bg, #00E5FF accent
- Deploy to CF Workers, purge CDN after every deploy

See CONVENTIONS.md for full patterns.
