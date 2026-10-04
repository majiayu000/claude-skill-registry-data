---
name: build-fullstack
description: Build a complete, production-ready full-stack application with Next.js, Cloudflare Workers, Supabase, and Stripe. Use when Rick asks to build an app, system, or platform.
---

# Build Full-Stack Application

Build a complete, production-ready application for RJ Business Solutions.

**IMPORTANT**: Before scaffolding, see @project-scaffolding.md for the complete master project template.
All new projects MUST use the full monorepo structure with all critical config files.

## Required Stack
- Frontend: Next.js 15 App Router + React 19 + Tailwind + shadcn/ui + Framer Motion
- Backend: Hono on Cloudflare Workers (or Next.js API routes)
- Database: Supabase PostgreSQL with RLS policies
- Auth: Supabase Auth (email/password + OAuth)
- Payments: Stripe (checkout, subscriptions, webhooks)
- Deployment: Cloudflare Pages + Workers

## Required Files
Every build MUST include:
- `wrangler.toml` — Cloudflare config
- `package.json` with all dependencies
- `tsconfig.json` (strict mode)
- `tailwind.config.ts`
- `.env.example` with all required variables
- `Dockerfile` and `docker-compose.yml`
- `.github/workflows/deploy.yml` — CI/CD
- `README.md` with company branding and logo

## Required Features
- Complete auth flow (register, login, password reset, email verification)
- Dashboard with real-time data
- Admin panel with CRUD operations
- Responsive design (mobile-first)
- Dark mode
- Error boundaries and loading states
- Input validation (zod) on all forms and API routes
- Rate limiting on API endpoints
- SEO meta tags and Open Graph

## After Building
1. Run `pnpm build` to verify clean build
2. Use the code-reviewer subagent to review
3. Use the security-auditor subagent to audit
4. Use the deployer subagent to deploy to Cloudflare
5. Push to GitHub (rjbizsolution23-wq)
