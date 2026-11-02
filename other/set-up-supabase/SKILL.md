---
name: set-up-supabase
description: Use when a project starts using Supabase or its supabase/ folder is missing or half-set-up — wires the CLI local stack, migrations as the only schema path, generated types, per-environment config, and one client seam per context so the secret key never reaches a bundle.
---

# Set Up Supabase

## 1. Audit current state

Read `.claude/stack-profile.md` if present (`backend.track`, `database.orm`, `hosting`, `package_manager`, `frontend.meta`). If absent, detect; ask one question only when the answer changes the output (for example Drizzle owning DDL, see step 3).

```bash
ls supabase/config.toml supabase/migrations supabase/seed.sql supabase/tests 2>/dev/null
grep -n "pgdelta\|schema_paths" supabase/config.toml 2>/dev/null     # diff engine in use
grep -rn "createClient\|createBrowserClient\|createServerClient" src app lib --include=*.ts --include=*.tsx 2>/dev/null | head -20
grep -rn "service_role\|SERVICE_ROLE\|sb_secret_\|SUPABASE_SECRET" --include=*.ts --include=*.tsx --include=.env* . 2>/dev/null | grep -v node_modules | head
git ls-files | grep -E "\.env($|\.)" | grep -v example                # committed env files = finding
ls .github/workflows 2>/dev/null; cat package.json 2>/dev/null | grep -n "supabase"
```

Findings to record: secret/`service_role` key outside a server-only file, `anon`/`service_role` legacy names, a Dashboard-edited remote with no migrations, a client created inline in a component.

## 2. Decide what to do

- No `supabase/` → full setup (steps 4–8).
- `supabase/` exists, no migrations but a live remote → baseline pull first (step 4, "existing project").
- Clients scattered or secret key in a client-reachable file → step 7 plus rotate the key if it was ever committed ([security-baseline.md](../../core/_shared/security-baseline.md), rule 1).
- Everything present and `supabase db reset` passes → report "already in place" and stop.

## 3. Detect track and pick the schema workflow

| Signal | Track |
|---|---|
| `frontend.meta: next` or `next` in `package.json` | Next.js: cookie clients come from [set-up-nextjs-supabase-auth](../set-up-nextjs-supabase-auth/SKILL.md) |
| `backend.track: hono` / Node server | server client with the publishable key plus the caller's JWT |
| Vite SPA only | browser client only; admin work goes to an Edge Function ([build-supabase-edge-function](../build-supabase-edge-function/SKILL.md)) |

Schema workflow: **plain migrations** (`supabase migration new`) are the default. Declarative schemas (`supabase/schemas/` + `db schema declarative sync`) are opt-in: they need the `pg-delta` engine, which is pre-1.0 and still under `[experimental.pgdelta]`. Both end in files under `supabase/migrations/`, and only those reach a remote. Reasons and the switch: [supabase-patterns.md](./supabase-patterns.md).

If `database.orm: drizzle`: Supabase migrations stay the only DDL path (RLS, grants, triggers and functions are SQL). Drizzle reads the schema; do not run `drizzle-kit push` against a remote.

## 4. Install only what's missing

```bash
pnpm add -D supabase                      # CLI as a project dependency, pinned by the lockfile
pnpm add @supabase/supabase-js            # + @supabase/ssr on Next/SSR (set-up-nextjs-supabase-auth)
pnpm supabase init                        # only if supabase/config.toml is missing
```

Docker (or a compatible runtime) must run for `supabase start`. Use the package runner form (`pnpm supabase …`) everywhere below. Versions: [stack-versions.md](../_shared/stack-versions.md).

**Existing remote project** (tables made in the Dashboard):

```bash
pnpm supabase login && pnpm supabase link --project-ref <project-ref>
pnpm supabase db pull          # writes supabase/migrations/<ts>_remote_schema.sql; accept "mark as applied"
```

Read the generated file before committing: extensions you enabled yourself can appear as `DROP EXTENSION`.

## 5. Generate the seams: folder, first migration, seed

```
supabase/
  config.toml          # committed; secrets only via env("NAME")
  migrations/          # committed; applied in order; never edited once pushed
  seed.sql             # committed; fake data only, never a production dump
  tests/               # pgTAP, see secure-supabase-rls
  functions/           # see build-supabase-edge-function
```

First migration closes the default-grant hole before any table exists:

```bash
pnpm supabase migration new baseline_privileges < /dev/null   # closed stdin: the command waits for input in a non-TTY shell
```

Fill it with the `alter default privileges` block from [rls-patterns.md](../secure-supabase-rls/rls-patterns.md) ("Rule: no automatic grants"). In `config.toml` keep `[api] schemas = ["public"]` unless you have a dedicated API schema, and set `[auth] site_url` and `additional_redirect_urls` per environment.

`.gitignore`: `.env*` (except `.env.example`), `supabase/.temp`, `supabase/.branches`, `supabase/functions/.env`.

## 6. Environment per environment

| Var | Where | Exposure |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` / `VITE_SUPABASE_URL` / `SUPABASE_URL` | all | public |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` / `VITE_…` / `SUPABASE_PUBLISHABLE_KEY` | all | public (`sb_publishable_…`) |
| `SUPABASE_SECRET_KEY` (`sb_secret_…`) | server runtime only | never a public prefix |

One Supabase project per environment (local stack, staging, production); keys differ per project. Never add `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_ROLE_KEY` to new code: those are the legacy keys. Validate at startup with the project's env seam ([validate-env](../../frontend/validate-env/SKILL.md) for Vite, [nextjs-backend-patterns.md](../build-nextjs-backend/nextjs-backend-patterns.md) for Next). Layout and naming: [config.md](../_shared/config.md).

## 7. Client seams — one module per context

`src/libs/supabase/` (Next/React) or the equivalent seam folder:

```ts
// browser.ts — public key, runs in the browser; Realtime and non-auth queries only, never auth
import { createBrowserClient } from '@supabase/ssr'; // Vite SPA without SSR: createClient from supabase-js
import type { Database } from './database.types';

export const createClient = () =>
  createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
  );
```

On Next.js the session cookie is httpOnly ([set-up-nextjs-supabase-auth](../set-up-nextjs-supabase-auth/SKILL.md)), so this client cannot read the session and never signs anyone in. Auth is server-side only; the browser client exists for Realtime and non-auth queries. Realtime needs a token client-side — see the pattern in that skill.

```ts
// admin.ts — secret key, bypasses RLS, server only
import 'server-only';
import { createClient } from '@supabase/supabase-js';
import type { Database } from './database.types';

export const supabaseAdmin = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SECRET_KEY!,
  { auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false } },
);
```

The per-request server client (cookies) is in [set-up-nextjs-supabase-auth](../set-up-nextjs-supabase-auth/SKILL.md). Call `supabaseAdmin` only from code that already authorized the caller: it bypasses RLS. Types:

```bash
pnpm supabase gen types --lang typescript --local > src/libs/supabase/database.types.ts
```

Add a `"db:types"` script (or a `just`/`mise` task per `task_runner`) and commit the output.

## 8. Wire CI and deploy

- PR job: `supabase start`, `supabase db reset` (proves the chain from zero), `supabase test db`, `supabase db advisors --local --fail-on error`, regenerate types and fail on `git diff`.
- Deploy: either Supabase's GitHub integration (preview branch per PR, migrations applied on merge) or a GitHub Actions job running `supabase link` + `supabase db push`. Pick one. Workflow files and token scopes: [supabase-patterns.md](./supabase-patterns.md).
- Remote changes only through merged migrations. `supabase db push --dry-run` before the first push.

## 9. Verify

`typecheck` is `tsc --noEmit` in a Next.js app (one tsconfig); add `"typecheck": "tsc --noEmit"` to package.json if it is missing.

```bash
pnpm supabase start && pnpm supabase db reset      # migrations + seed apply cleanly
pnpm supabase test db                              # pgTAP green (or "no tests" before secure-supabase-rls)
pnpm supabase db advisors --local --type security  # no ERROR-level findings
pnpm typecheck                                  # Database types resolve
pnpm build && ! grep -rEl "sb_secret_|SUPABASE_SECRET_KEY" .next/static dist 2>/dev/null   # nothing in client output
```

Expected: every command exits 0 and the last grep prints nothing.

## References
- [supabase-patterns.md](./supabase-patterns.md) — migrations vs declarative, branching, keys, types, CI.
- [../secure-supabase-rls/SKILL.md](../secure-supabase-rls/SKILL.md) — the next step for every new table.
- [../_shared/stack-versions.md](../_shared/stack-versions.md), [../_shared/service-layout.md](../_shared/service-layout.md), [../_shared/config.md](../_shared/config.md).
- [../../core/_shared/stack-profile.md](../../core/_shared/stack-profile.md), [../../core/_shared/security-baseline.md](../../core/_shared/security-baseline.md).
