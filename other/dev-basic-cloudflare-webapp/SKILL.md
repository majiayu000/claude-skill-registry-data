---
name: dev-basic-cloudflare-webapp
description: "The house tech stack for a new web project on Cloudflare — framework, lint, test, CI, docs, and repo conventions, with copy-ready config templates. Cloudflare is the default infra and backend (Workers, D1, KV, R2, Durable Objects); AWS is not. Use this whenever a new web app, site, API, or worker is being started or scaffolded, whenever someone asks 'what stack should we use', 'what should I pick for X', 'set up CI/lint/test for this project', or 'scaffold a new project' — even if Cloudflare is never named, because Cloudflare is the assumed target. Also use when adding CI, lint, formatting, git hooks, deploy workflows, or a docs site to an existing project so it matches the other repos. Keywords: new project, scaffold, boilerplate, starter, tech stack, tech choice, Cloudflare, Workers, wrangler, D1, KV, R2, Durable Objects, zfb, zudo-doc, pnpm, lefthook, vitest, playwright, GitHub Actions, b4push."
argument-hint: "[project description] [--scaffold]"
---

# Cloudflare Web App — House Stack

The reference for what to pick when starting a new web project. Every choice
here is already running in production across the other repos, so matching it
means CI, hooks, deploy, and agent workflows all behave the way they do
elsewhere.

**Cloudflare is the infra and the backend.** Workers, D1, KV, R2, Durable
Objects, Workers AI, Queues. Not AWS, not Vercel, not Netlify, not Supabase.
Reach outside Cloudflare only for something Cloudflare genuinely lacks (Stripe,
Resend, npm registry) and say so explicitly.

## Two modes

**Reference mode (default)** — the user described a project and wants the stack.
Read the tables below, pick the project shape, read the reference files that
matter for that shape, and report the recommended stack with concrete versions
and file names. Do not write files.

**Scaffold mode** — the user passed `--scaffold` or asked to actually create the
project. Do reference mode first, confirm the shape, then copy from
`assets/templates/` and adapt. See "Scaffolding" below.

## Step 1 — Pick the project shape

| Shape | When | Frontend | Deploy target |
| --- | --- | --- | --- |
| **Content site** | Marketing, blog, portfolio, landing | zfb + Preact + Tailwind v4 | Workers Static Assets |
| **Docs site** | Reference docs, manuals, changelog | zudo-doc (a zfb preset) | Workers Static Assets |
| **SSR app** | Auth, forms, DB-backed pages | zfb SSR routes (`prerender = false`) + CF adapter | Workers Static Assets + bindings |
| **API / worker** | JSON API, webhook, proxy, cron, agent | Hono on Workers, no frontend | Workers |
| **Interactive app** | Editor, dashboard, canvas, heavy client state | Vite + React + Tailwind v4 | Workers Static Assets (+ separate API worker) |
| **Library / CLI** | Publishable npm package | none | npm — use `/dev-npm-package` instead |

Mixed projects are normal: a pnpm workspace with a zfb site at the root and
worker packages under `workers/*`. Split when the deploy units differ.

## Step 2 — The non-negotiable base

Every repo gets these regardless of shape. Details and rationale in
[references/tooling.md](references/tooling.md).

| Concern | Choice |
| --- | --- |
| Package manager | pnpm, `packageManager` pinned in package.json, `engines.node >= 22` |
| Language | TypeScript, `strict: true` |
| Unit tests | vitest |
| Worker tests | `@cloudflare/vitest-pool-workers` |
| E2E | Playwright |
| Format | Prettier for code, `@takazudo/mdx-formatter` for `.md`/`.mdx` |
| Lint | ESLint flat config (`eslint.config.js`) |
| Git hooks | lefthook (`lefthook.yml`) + `prepare` script |
| Pre-push gate | `pnpm b4push` — mirrors CI locally |
| CI | GitHub Actions, SHA-pinned actions |
| Deploy | `wrangler deploy` from GitHub Actions |
| Dep updates | Renovate (preferred) or Dependabot |

## Step 3 — Read the reference for what you're deciding

Load only what the current decision needs.

- [references/stack.md](references/stack.md) — every library choice with its

  rationale, plus the explicit **do-not-use** list (Pages, Next.js, AWS SDK,
  Prisma, Jest, styled-components, …). Read this for any "what should we use
  for X" question.

- [references/cloudflare.md](references/cloudflare.md) — `wrangler.toml`

  anatomy, Workers Static Assets, bindings (D1/KV/R2/DO/AI/Queues/services),
  named environments, preview aliases, secrets vs vars, and the TOML/config
  gotchas that cost real debugging time.

- [references/ci.md](references/ci.md) — the standard workflow set, SHA pinning,

  concurrency, self-skipping deploy jobs, PR preview comments, actionlint,
  security audit.

- [references/tooling.md](references/tooling.md) — pnpm settings, workspace

  layout, lefthook, prettier, eslint, mdx-formatter, design-token-lint,
  tsconfig, the b4push script.

- [references/testing.md](references/testing.md) — test levels and tiers, what

  runs in b4push vs CI vs nightly, Playwright conventions.

- [references/conventions.md](references/conventions.md) — directory layout,

  `CLAUDE.md`, docs site, README, worktrees, `.gitignore`, scratch dirs.

For Cloudflare **platform** API detail (exact binding APIs, runtime limits,
current wrangler flags), defer to the Cloudflare plugin skills — `/cloudflare:cloudflare`,
`/cloudflare:wrangler`, `/cloudflare:workers-best-practices`,
`/cloudflare:durable-objects`, and `/cloudflare:agents-sdk` — they
retrieve live docs. This skill owns the *opinion*; those own the *facts*.

## Step 4 — Report

Report as a short stack table (shape, framework, styling, data, tests, CI,
deploy target) plus the list of files the project needs. Name the Cloudflare
resources that must be provisioned (D1 database, KV namespace, R2 bucket,
custom domain) and the secrets that must be set — these are manual, one-time,
and easy to forget.

## Scaffolding

Only in scaffold mode. Copy from `assets/templates/` and adapt — every file
carries comments explaining the traps, so keep them.

| Template | Copy to | Notes |
| --- | --- | --- |
| `package.json` | `package.json` | Replace `latest` with resolved versions after the first install |
| `pnpm-workspace.yaml` | same | Delete if single-package |
| `npmrc` | `.npmrc` | |
| `gitignore` | `.gitignore` | |
| `prettierignore` | `.prettierignore` | |
| `.prettierrc.json` | same | |
| `tsconfig.json` | same | |
| `lefthook.yml` | same | |
| `wrangler.toml` | same | Strip unused binding blocks |
| `.github/workflows/*.yml` | same | `ci.yml`, `deploy.yml`, `actionlint.yml` |
| `scripts/run-b4push.sh` | same | `chmod +x`; keep steps identical to `ci.yml` |
| `scripts/smoke.mjs` | same | Fill in `EXPECTED` with real page markers |
| `scripts/install-git-hooks.sh`, `scripts/hooks/pre-push` | same | `chmod +x` both |
| `cloudflare-setup.md` | `docs/cloudflare-setup.md` | |

Three templates ship without their leading dot (`npmrc`, `gitignore`,
`prettierignore`) so they stay inert inside this skill's own repo — rename on
copy.

Then:

1. Replace every `__PROJECT_NAME__` and `__DOMAIN__` placeholder
2. Write `README.md` and `CLAUDE.md` (outline in

   [references/conventions.md](references/conventions.md))

3. `pnpm install`, then confirm `pnpm b4push` passes before the first push

Do not invent Cloudflare resource ids. Leave `REPLACE_ME` plus the
`wrangler ... create` command that produces it — the deploy job self-skips until
the real id is committed.
