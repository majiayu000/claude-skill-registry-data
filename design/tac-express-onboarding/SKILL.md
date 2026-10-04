---
name: tac-express-onboarding
description: >-
  MANDATORY at the start of every tac-express task. Load this skill FIRST. Provides a 60-second project orientation: monorepo layout, design system identity (Violet Grid v5.0), the Fourteen Laws summary, package boundaries, and a routing table to the correct specialist skill.
---

# TAC Express — Agent Onboarding (60-Second Orientation)

> **DO NOT SKIP THIS DOCUMENT.** Every task starts here, regardless of how small.

---

## Step 0 — The GBrain enforcement gate (MANDATORY)

After this onboarding, your very next action is:

1. **Open [`.claude/skills/RESOLVER.md`](../RESOLVER.md)** — the intent→skill dispatch table.
2. Match the user's request to a specialist skill (or two).
3. Load the matched skill BEFORE writing any code.
4. Apply the cross-cutting rules in [`.claude/skills/conventions/`](../conventions/):
   - `quality-gates.md` (5 must-pass commands)
   - `architecture-flow.md` (UI → services → database)
   - `brain-first.md` (codebase + skills + memory FIRST)
   - `test-before-bulk.md` (test on 1 before bulk)
   - `subagent-routing.md` (Agent tool vs inline)
   - `friction-protocol.md` (refusal format when asked to violate a law)
5. If the same fix recurs 2+ times → load [`tac-skillify`](../tac-skillify/SKILL.md)
   and turn it into a permanent skill. The 10-item conformance audit is the gate.

> Skipping the resolver = non-conforming task. Restart from step 1.

---

## What is TAC Express?

A **logistics mission-control platform** for the North-East corridor. Public marketing site (`apps/web`) + operations dashboard (`apps/dashboard`) + shared monorepo packages.

**Domain:** AWBs, manifests, exceptions, hub scanning, customer accounts, rate cards, invoicing, real-time tracking, COD/payments, audit trail. Touch `tac-domain-logistics` whenever any of these come up.

---

## Design System — TAC Express v5.0 Violet Grid

| Aspect | Value |
|---|---|
| **Identity** | Mission-control density + brutalist offset shadows + NASA FUI utilities |
| **Mode** | Dark-first (light mode supported but secondary) |
| **Primary** | Violet — `oklch(0.5393 0.2713 286.7462)` light / `oklch(0.6132 0.2294 291.7437)` dark |
| **Status** | Green success / amber warning / red danger / violet info |
| **Radius** | `0rem` everywhere (LAW 13) |
| **Shadows** | Brutalist offset only — `shadow-sm`..`shadow-2xl` resolve to `Npx Npx 0 0 var(--border)` |
| **Fonts** | Plus Jakarta Sans (sans) · IBM Plex Mono (mono) · Lora (serif) |
| **Forbidden** | Glassmorphism · soft drop shadows · curves · `rounded-full` · indigo / cyan / orange / Inter / Geist / Space Grotesk |

> **Authoritative source of truth:** `packages/ui/src/styles/globals.css`. If a doc and the CSS disagree, the CSS wins and the doc is updated.

Full spec: [`DESIGN_SYSTEM.md`](../../../DESIGN_SYSTEM.md).

---

## The 5 Things You Must Never Do

1. Never use arbitrary Tailwind values (`w-[347px]`) or raw colors (`bg-[#11161C]`). Use semantic tokens.
2. Never install `lucide-react`, `framer-motion` (legacy), `gsap`, `@motionone/react`, `@tabler/icons-react`, `react-icons`, `clsx`, `axios`, `lodash`, `moment`, `classnames`.
3. Never put UI components in `apps/web/components/` or `apps/dashboard/components/`. They go in `packages/ui/src/components/`.
4. Never call Supabase directly from a component. Route through `packages/services` (and `packages/database` is the only place `@supabase/*` SDKs are imported).
5. Never use curved lines, `rounded-full`, soft drop shadows, or wavy SVG paths. Straight lines and 90° angles only.

---

## Monorepo Layout

```
apps/
  web/          Public landing page (port 3000) — Next.js 16 (Turbopack)
  dashboard/    Logistics operations app (port 3001) — Next.js 16 (Turbopack)

packages/
  ui/           @workspace/ui — shared components, tokens, icons (THIS is where every component lives)
  auth/         @workspace/auth — Supabase auth wrapper, RBAC helpers (signIn / signOut / getSession / role checks)
  database/     @workspace/database — Supabase SSR client factories (browser, server, middleware, admin)
  services/     @workspace/services — business logic per domain (createXxxService(db) factories)
  types/        @workspace/types — branded types, enums, zod schemas
  eslint-config/        Shared ESLint config
  typescript-config/    Shared TS config

supabase/
  migrations/   Versioned DDL (5 files, init schema dated Apr 30, 2026)
  functions/    Edge functions: dispatch-webhook, generate-pdf, send-notification, scheduled-sla-monitor
  seed.sql      Hub + rate card seed data
```

---

## Architecture Flow (Inviolable — LAW 6/7/8)

```
UI Component
   ↓  (props / hooks only)
packages/services/   ← business logic lives here
   ↓  (typed function calls only)
packages/database/   ← Supabase client lives here
   ↓
Supabase (cloud)
```

Components NEVER import `@supabase/*`. Components NEVER contain business logic beyond display state.

---

## The Fourteen Laws (One-Liner Reference)

| # | Law |
|---|-----|
| 1 | No color outside `globals.css` |
| 2 | Icons via `@workspace/ui/icons` (Remix Icon) only |
| 3 | Animation via `motion` (motion/react) or `tw-animate-css` or `@keyframes` in globals.css |
| 4 | Fonts declared only in `apps/*/app/layout.tsx` |
| 5 | UI components only in `packages/ui` |
| 6 | No DB calls in components — only via `packages/services` |
| 7 | No business logic in components |
| 8 | `@supabase/supabase-js` only in `packages/database` |
| 9 | No hardcoded spacing/radius/shadow |
| 10 | No Tailwind color classes (`bg-blue-500`) |
| 11 | No arbitrary Tailwind values (`w-[347px]`) |
| 12 | `pnpm` only — no `npm` / `yarn` |
| 13 | Straight lines only — no curves |
| 14 | Wrap shadcn primitives — never rebuild |

Full text + violation patterns: load `tac-fourteen-laws`.

---

## Skill Activation Routing

Match your task to the right specialist. Load it BEFORE writing code.

| Task | Required skill |
|---|---|
| Any non-trivial implementation | `tac-karpathy-discipline` (always — Think → Simplify → Surgical → Goal) |
| New feature / component | `tac-brainstorming` first → produce written spec |
| Writing UI / components | `tac-ui-authoring` |
| Premium token reference / motion / type scale | `tac-design-tokens` |
| Forms / validation / server actions | `tac-forms` |
| Services / business logic / hooks | `tac-data-layer` |
| Auth / session / middleware / RBAC | `tac-auth` |
| Schema / RLS / migrations / RPC | `tac-supabase-schema` |
| Shipments / manifests / AWBs / domain | `tac-domain-logistics` |
| Route handlers / server actions / edge functions | `tac-api-surface` |
| Test writing | `tac-tdd` (RED → GREEN → REFACTOR) |
| Bug / failure / unexpected behavior | `tac-debug` (root cause first, no guessing) |
| A11y review | `tac-accessibility` |
| Pre-merge / post-feature | `tac-code-review` |

> When in doubt: load `tac-fourteen-laws` and `tac-karpathy-discipline` together. They cover most situations.

---

## Quick Reference Card

```
ICONS:      import { RiX } from "@workspace/ui/icons"  (@remixicon/react via wrapper)
COMPONENTS: import { ... } from "@workspace/ui"  (shadcn radix-lyra)
COLORS:     bg-primary · text-foreground · border-border · bg-accent-{success,warning,danger,info}
FONTS:      font-sans (Plus Jakarta Sans) · font-mono (IBM Plex Mono) · font-serif (Lora)
ANIMATION:  motion components OR animate-in fade-in slide-in-from-* duration-* (tw-animate-css)
            + CSS @keyframes in globals.css (shimmer, scanline, blink, marquee-x/y)
DATA:       via packages/services → packages/database  (NEVER direct Supabase in components)
RADIUS:     var(--radius-sm/md/lg/xl) — all resolve to 0  (NOT rounded-lg, NOT rounded-full)
SHADOWS:    shadow-sm / shadow / shadow-md / shadow-lg / shadow-xl  (brutalist offset, sharp)
SPACING:    Tailwind scale (p-4, m-6)  (NO arbitrary [px] values)
PACKAGES:   pnpm ONLY  (NO npm, NO yarn)
GEOMETRY:   ZERO curves — all straight lines, sharp corners
TYPE:       .t-display / .t-h1..h4 / .t-data / .t-overline / .t-mono — premium scale in globals.css
```

---

## Quality Gates (Before Every Commit)

```bash
pnpm lint --max-warnings 0     # Zero lint warnings
pnpm typecheck                 # Zero TS errors
pnpm build                     # Both apps build
pnpm test                      # All tests pass
pnpm audit:all                 # governance + auth-boundary + skills + design-spec
```

If any of these fail, stop. Diagnose root cause (use `tac-debug`). Don't suppress, don't bypass, don't `--no-verify`.
