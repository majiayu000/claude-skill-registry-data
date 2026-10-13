---
name: kyle-vibe-coding
metadata:
  version: "2.0.0"
description: >
  Rapidly prototype and build complete web apps on Kyle's production stack — React 19, Vite,
  TypeScript, Tailwind, Supabase (auth, RLS, Postgres), Cloudflare Workers/Pages, Resend,
  Stripe, PostHog. Enforces security-first defaults, the no-placeholder rule, and a mandatory
  6-persona audit loop before any deploy or hand-off. Activates on vibe code, prototype, spin
  up, new app, scaffold, demo, internal tool, MVP, greenfield, build this idea. Not for
  credential rotation or audits (use managing-credential-lifecycle) and not for production
  incident response or pure infra ops.
---

## When to Use / When NOT

**Use when** — "spin up a quick internal tool to track client onboarding" — scaffold then audit loop. "build a new SaaS feature from scratch with Supabase auth" — full build with the RLS gate.

**Do NOT use when** — "rotate the Stripe API key, it may be compromised" — credential lifecycle, not a build.

# Kyle Vibe Coding Skill

## Purpose
Rapid prototyping using Kyle's exact stack. Production-seed codebases — real auth, real DB, security defaults baked in, 6-persona audit loop before anything ships.

## Stack (Defaults — Flag Any Deviation)
| Layer | Technology |
|---|---|
| Frontend | React 19 + Vite + TypeScript (strict, functional only) |
| Styling | Tailwind CSS (utility-first, no CSS modules) |
| Backend | Cloudflare Workers (edge-first) or Express 5 (Node) |
| Database | Supabase — Postgres + RLS + real-time |
| Auth | Supabase Auth — email/password + magic link |
| Email | Resend (transactional) |
| Payments | Stripe (when required) |
| Analytics | PostHog (every app) |
| Deploy | Vercel + Cloudflare Workers + GitHub Actions CI |
| State | Zustand (client) + TanStack Query v5 (server) |
| Forms | React Hook Form + Zod |
| Testing | Vitest (unit) + Playwright (E2E) |

---

## Security Hard Rules (Zero Tolerance)
- **NEVER** put `service_role`, API keys, or DB strings in frontend code
- **ALWAYS** `VITE_*` for client env vars; Cloudflare secrets for Workers
- **ALWAYS** enable RLS on every Supabase table before any INSERT/SELECT
- **NEVER** commit `.env` — `.env.example` with placeholders only
- **VERIFY**: `grep -r 'service_role\|apiKey' src/` empty before any deploy

---

## Quick Start
```bash
npm create vite@latest [app-name] -- --template react-ts && cd [app-name]
npm install @supabase/supabase-js @supabase/auth-helpers-react
npm install @tanstack/react-query zustand react-hook-form zod @hookform/resolvers
npm install tailwindcss postcss autoprefixer posthog-js && npx tailwindcss init -p
npm install -D vitest @testing-library/react @testing-library/jest-dom @playwright/test
```
See [REFERENCE-templates.md](REFERENCE-templates.md) for core file templates (supabase.ts, RLS policies, auth entry point, architecture patterns).

---

## THE 6-PERSONA AUDIT LOOP
**Invoke with: `RUN AUDIT LOOP` — runs before every deploy, demo share, or hand-off.**

Each persona runs in sequence. Each outputs:
`| Finding | Severity | Location | Recommended Fix | Accept Risk? |`

| Persona | Core Domain | Key Catches |
|---|---|---|
| 1 — Security Auditor | Secrets, RLS, attack surface | Exposed keys, missing RLS, injection vectors, CORS, over-permissioned tokens |
| 2 — Staff Architect | Boundaries, coupling, failure modes | Wrong abstractions, missing error/loading/empty states, tight coupling, no retry |
| 3 — QA / Test Engineer | Coverage, edge cases, async | Untested branches, no E2E smoke, race conditions, happy-path-only |
| 4 — Performance Engineer | Latency, bundle, DB cost | N+1 queries, no pagination, oversized bundle, unthrottled realtime |
| 5 — DevOps / Infra | Deploy risk, env hygiene, CI | Missing .env.example entries, no CI check, hardcoded URLs, no rollback |
| 6 — Accessibility / UX | a11y WCAG 2.2 AA, task-first IA | Missing aria-labels, broken focus management, contrast failures, no keyboard nav |

**Synthesis:**
```
AUDIT SUMMARY — [Build] — [Date]
P0 (Blockers): N | P1 (Backlog): N | P2 (Accept risk): N
Fix order: 1. [P0 + fix] 2. [P0 + fix]
Risk decisions: [P1/P2] → Accept / Defer / Fix now?
```

**Severity:** P0 = does not ship | P1 = backlog + ship with note | P2 = accept + document

**Audit scope by build type:**
| Build Type | Personas |
|---|---|
| Prod deploy / real users | All 6 |
| Internal demo / preview URL | 1, 2, 3 |
| Local throwaway (< 48h) | 1 only |
| Decision PoC | 1 + 2 |

---

## Build Acceptance Criteria
- [ ] `.env.example` committed, all vars documented, no real values
- [ ] RLS enabled + tested on all Supabase tables
- [ ] `grep -r 'service_role\|apiKey' src/` returns empty
- [ ] PostHog initialized with ≥1 custom event
- [ ] README: setup, env vars, deploy target, known limits
- [ ] ≥3 Vitest unit tests on core logic
- [ ] `npm run dev` works on first checkout (beyond filling .env)
- [ ] **Audit loop complete. 0 P0 findings open.**

---

## Integration
→ **elite-ui-design** — design direction pre-build
→ **staff-engineer-v4** — architecture review for complex features
→ **sparc-methodology-coach** — for non-trivial features
→ **loxihart-data-analyst** — instrument PostHog events, analyze post-launch

---

## Reference Files
- [REFERENCE-templates.md](REFERENCE-templates.md) — Core file templates, RLS patterns, architecture layouts, PostHog setup, .env.example

---

## CLAIMS / COUNTEREXAMPLE / CONTRADICTIONS
- [GENERATED] Stack patterns — verify react.dev, supabase.com/docs before use; both evolve
- COUNTEREXAMPLE: 6-persona audit is overhead on throwaway experiments — use scope table above
- RISK: Vite exposes `VITE_` vars in bundle — audit via devtools Network tab before real deploy
- CONTRADICTION: `@supabase/auth-helpers-react` may be deprecated in favour of `@supabase/ssr` — check for deprecation warnings and follow current Supabase docs


## FAIL Conditions

Named failure modes for this skill. Each is a hard stop, not a warning.

- **Shipping with service_role or any secret in the client bundle** → full database compromise — the grep gate (grep -r 'service_role\|apiKey' src/) must be empty before deploy; service_role stays server-side.
- **Querying a new Supabase table before RLS is enabled** → cross-tenant data leak — enable RLS and write policies before the first INSERT or SELECT, then probe with the anon key.
- **Marking a build done with TODO stubs or empty catch blocks** → violates the no-placeholder rule — every catch handles or rethrows, no TODOs ship, the smoke test runs green.
- **Deploying, sharing, or handing off before the 6-persona audit loop passes** → unreviewed attack surface ships — RUN AUDIT LOOP is a hard gate.
- **Stripe keys or webhook secrets in client code or committed env** → payment fraud and key theft — server-side only, env vars, .env.example placeholders only.
- **Writing features before modeling auth, data flow, and failure modes** → rework plus security gaps — architecture first, per the decision defaults.

## Evals

- ✅ **SHOULD TRIGGER** — "spin up a quick internal tool to track client onboarding" — scaffold then audit loop.
- ✅ **SHOULD TRIGGER** — "build a new SaaS feature from scratch with Supabase auth" — full build with the RLS gate.
- ❌ **SHOULD NOT TRIGGER** — "rotate the Stripe API key, it may be compromised" — credential lifecycle, not a build.
