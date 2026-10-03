---
name: deploy
layer: stack
description: Deploy a crouton app to Cloudflare Workers STAGING (auto-provisioning) — the DEFAULT deploy, staging only, never production. Handles the staging bootstrap (auto-creates D1+KV, syncs ids, migrates), wiring CI, routine staging deploys, and Pages→Workers migration. For production use the separate /deploy-production skill. Use when deploying any app in apps/.
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent, AskUserQuestion
---

# Deploy Skill — Cloudflare Workers

Deploys a crouton app to **Cloudflare Workers (static assets)** — the crouton
deploy standard (#108). Wrangler **auto-provisions** the app's D1 + KV on the
first deploy, so there's no manual resource/project creation, no id-juggling.

> **🟦 STAGING ONLY — this skill never deploys to production.** "Deploy" defaults to
> **staging** here. Shipping to production is a deliberate, human-initiated action handled
> by the separate **`/deploy-production`** skill. Never deploy production as part of routine work.

> **Not Cloudflare Pages.** We do NOT use `wrangler pages …`, `pages_build_output_dir`,
> or the Pages "strip env" step anymore. If you find those, the app is on the old
> Pages path — see **Migrating a Pages app → Workers** below.

## Environment & domain convention (#133)

Two environments, two domains — kept on **separate registrable domains** so a
staging session can never authenticate against production (cookie isolation):

| Env | wrangler env | Worker | Domain |
|-----|--------------|--------|--------|
| **production** | top-level | `<app>` | `<app>.friendlyinter.net` |
| **staging** | `env.staging` | `<app>-staging` | `<app>.pmcp.dev` (public) |

The deploy-env is named **`staging`** (not `preview`): scripts are `cf:staging` /
`db:migrate:staging`, deploys use `--env staging`. (The general `crouton` CLI stays
domain-agnostic via `--domain <zone>`; the friendlyinter.net/pmcp.dev split is this
monorepo's convention, applied per app at its production cutover — #136 for triage.)

## Usage

```
/deploy              # Deploy current app to STAGING (auto-detected from cwd)
/deploy velo         # Deploy a specific app to STAGING
# production → use the separate /deploy-production skill
```

## Rules

1. **STAGING ONLY.** This skill deploys to **staging**, never production (that's the separate `/deploy-production` skill). Always confirm the target app first.
2. **Workers, not Pages** — `NITRO_PRESET=cloudflare_module`, output in `.output/`, deploy with `wrangler deploy` (never `wrangler pages deploy`).
3. **NEVER manually create D1/KV** — they auto-provision from the **id-less** `wrangler.jsonc` on first deploy. After provisioning, run `sync:ids` and **commit** the written-back ids (remote `d1 migrations apply` needs them — workers-sdk#13632).
4. **NEVER skip `nuxt prepare` before build** in CI — rolldown tsconfig bug. (Locally, the `cf:*` scripts assume `node_modules`/`.nuxt` are prepared from `pnpm install`.)
5. **`hub: { db: 'sqlite' }`** — never `hub: { database: true }`.
6. **`postinstall` must be guarded** — `nuxt prepare 2>/dev/null || true`, never bare (a bare prepare aborts the whole-monorepo install and fails every app's deploy).

## How the pipeline works (one source of truth)

The deploy logic lives in the app's **`package.json` scripts** — the same commands
you run locally and that CI runs. Don't reinvent them step-by-step:

- **`cf:deploy`** (production — run **only** via the `/deploy-production` skill): `build → wrangler deploy (auto-provision) → sync:ids → d1 migrations apply --remote`
- **`cf:staging`** (isolated staging env): `build → inject-wrangler-env → wrangler deploy --env staging → sync:ids → inject-wrangler-env → d1 migrations apply --env staging --remote`
- **`sync:ids`** — queries wrangler, writes provisioned ids back into `wrangler.jsonc`
- **`db:migrate` / `db:migrate:prod` / `db:migrate:staging`** — D1 migrations (local / remote / staging-remote)

A freshly scaffolded app (`crouton init`) already ships all of this:
`wrangler.jsonc` (id-less), `scripts/sync-wrangler-ids.mjs`,
`scripts/inject-wrangler-env.mjs`, `drizzle.config.ts`, the chained scripts, the
CF stubs + nitro aliases, and the guarded postinstall.

## Workflow

### Step 1: Detect app
- arg → `apps/{arg}/`; else if cwd is inside an app → that app; else ask.
- Verify it has `wrangler.jsonc` + `package.json`.

### Step 2: Pre-flight (run in parallel)
Confirm the app is Workers-ready:
1. **`wrangler.jsonc`** present, **Workers-style** (has `compatibility_flags: ["nodejs_compat"]`, `d1_databases`/`kv_namespaces`; **no** `pages_build_output_dir`).
2. **Scripts** `scripts/sync-wrangler-ids.mjs` + `scripts/inject-wrangler-env.mjs` exist.
3. **`drizzle.config.ts`** exists (so `db:generate` works).
4. **Package scripts** — `cf:deploy` is the Workers chain; `postinstall` is guarded.
5. **CF stubs** — `server/utils/_cf-stubs/` exists; `nuxt.config.ts` has `nitro.alias` for passkey/webauthn/papaparse stubs and pins **no** preset.
6. **Auth** — `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN` available in the environment (see **Credentials**).

If anything is missing and the app is on the old Pages setup → **Migrating a Pages app → Workers**. If it's just missing files, copy them from `apps/velo` (the reference) or re-run the scaffolder.

### Step 3: First (bootstrap) staging deploy
The id-less bindings auto-provision here. Confirm with the user, then deploy the
isolated **staging** environment (its own auto-provisioned D1+KV):

```bash
cd apps/{app}
pnpm cf:staging     # provisions + deploys the *-staging worker, migrates --env staging
```

Then **commit the written-back ids** (bootstrap → committed):
```bash
git add apps/{app}/wrangler.jsonc && git commit -m "chore({app}): commit provisioned staging D1/KV ids"
```

> The **production** bootstrap (`cf:deploy`, prod D1+KV, `<app>.friendlyinter.net`) is a
> deliberate, separate step — see the **`/deploy-production`** skill. This skill stops at staging.

> If you're an agent **without Cloudflare egress** (sandbox), you can't run these —
> verify what's verifiable (config, `pnpm sync:ids --dry-run` logic) and have the
> user run the CF-gated steps, pasting output (the #109/#113/#114 loop).

### Step 4: Wire CI (opt in via `deploy.config.json`)
There is **one generic workflow for all apps** — `.github/workflows/deploy-apps.yml`
(#481/#638; the old per-app `deploy-<app>.yml` callers are retired — don't create one).
An app opts in by adding a `deploy.config.json` next to its `package.json`. **Model on
`apps/velo/deploy.config.json`.** Set: `stagingUrl`, `productionUrl`, `layerPackages`,
and `watchPaths` (the app + its extended `crouton*` packages + lockfile). The workflow's
`detect` job matches changed files against `watchPaths` and fans out one reusable
`deploy-app.yml` call per affected app. Merge to `main`/open a PR → isolated staging
with the URL commented on the PR; manual dispatch (app + environment inputs) →
production (#347). The fan-out uses `secrets: inherit`.

Ensure **repo-level** secrets `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN` exist
(Settings → Secrets and variables → Actions).

### Step 4.5: App (Worker) secrets
The app's own secrets (`BETTER_AUTH_SECRET`/`BETTER_AUTH_URL`, `NUXT_*`, etc.) live
on the **Worker**, NOT in `wrangler.jsonc`. **Worker secrets persist across deploys**,
so this is a one-time bootstrap per worker (prod + staging), not a per-deploy step.

Two ways:
- **Manual (one-time):** `npx wrangler secret bulk secrets.json` (prod) /
  `… --env staging` (staging). `BETTER_AUTH_URL`/`BASE_URL` must be the **production
  domain** (not localhost). Pages secrets do NOT carry over — re-provide the values.
- **Automatic (CI):** store the whole bundle as a **repository-level** Actions secret
  `WORKER_SECRETS_JSON` (a JSON object of `{ "NAME": "value", … }`). It MUST be
  repo-level, NOT an Environment secret — the deploy job is reached via
  `secrets: inherit` from caller jobs that declare no `environment:`, so an
  Environment-scoped secret resolves EMPTY with no error and the Worker deploys
  without secrets (#1094). The reusable `deploy-app.yml` runs `wrangler secret bulk`
  from it on every deploy (`--env staging` for non-prod). Omit it to manage secrets
  manually. If the app depends on the bundle, set `"secrets": { "required": true }`
  in its `deploy.config.json` — an empty resolution then FAILS the deploy instead
  of silently skipping. Automation can't invent values — they must live in that
  secret once.

### Step 5: Routine deploys (staging)
- **CI (preferred):** merge to `main` (or open a PR) → the caller runs the staging pipeline (#347).
- **Local:** `pnpm cf:staging` from the app dir.
- **Production is never routine** — ship it deliberately via the **`/deploy-production`** skill.

### Auto-seeded review login on staging previews (#608)
Every **staging** deploy auto-seeds a throwaway, loginable test account on the
preview's isolated D1 so a reviewer can open the URL and be **inside the app in one
step** — no register → create-team wall. `deploy-app.yml` runs
`scripts/seed-review-login.mjs` against the deployed Worker (the app's own
`/api/auth/sign-up/email` + a team via `organization/create` when the app doesn't
auto-make one), then prints a `🔑 Test login` block in the PR's staging comment.
Creds are **deterministic per preview** (so redeploys reprint the same working login,
no user pile-up) and the step is best-effort (never fails the deploy). Optional repo
secret `REVIEW_SEED_SECRET` salts the password; **production seeds nothing**.

## Migrating a Pages app → Workers

For an app still on the Pages setup (`wrangler.toml`, `pages_build_output_dir`,
`wrangler pages deploy`):

1. **`wrangler.toml` → `wrangler.jsonc`** in the Workers shape (see `apps/velo`):
   drop `pages_build_output_dir`; keep `name`/`compatibility_*`; `d1_databases` (reuse
   the existing prod `database_id`), `kv_namespaces`; add an `env.staging` block with a
   **separate** `{app}-staging-db` + KV (id-less to auto-provision, or existing staging ids).
2. **Add** `scripts/sync-wrangler-ids.mjs`, `scripts/inject-wrangler-env.mjs`,
   `drizzle.config.ts` (copy from `apps/velo`).
3. **package.json** — replace the Pages `cf:*` scripts with the Workers chain
   (`NITRO_PRESET=cloudflare_module`, `sync:ids`, `db:migrate:staging`); keep the
   guarded `postinstall`.
4. **nuxt.config.ts** — remove `nitro.preset: 'cloudflare-pages'` (keep the `nitro.alias` stubs).
5. **CI** — replace `deploy-{app}.yml` (+ any `-preview.yml`) with the thin caller from Step 4; delete the Pages strip-env step (not needed on Workers).
6. **Deploy + commit ids** as in Step 3.

## Credentials

The job/shell needs **`CLOUDFLARE_ACCOUNT_ID`** + **`CLOUDFLARE_API_TOKEN`**.

- **`CLOUDFLARE_ACCOUNT_ID`** — dashboard → Workers & Pages → Account ID (also the hex in the dashboard URL). Not secret.
- **`CLOUDFLARE_API_TOKEN`** — My Profile → API Tokens → **Create Custom Token**. For Workers + **auto-provisioning** the token needs (Account-scoped):
  - **Workers Scripts: Edit**
  - **D1: Edit**
  - **Workers KV Storage: Edit**
  - (**Workers R2 Storage: Edit** if the app uses blob)

  Cloudflare shows a token's value **only once**, and GitHub never reveals a saved
  secret — so mint a fresh dedicated token rather than reusing one.

> Note: this differs from the old Pages token (which used *Cloudflare Pages: Edit*).
> A Pages-only token will fail to auto-provision D1/KV.

## Troubleshooting

### `Couldn't find a D1 DB … missing database_id` (on migrate)
The first deploy provisioned the DB but the id isn't in `wrangler.jsonc` yet. Run
`pnpm sync:ids` (after a deploy) and commit the result. `cf:deploy`/`cf:staging` do
this automatically.

### `Configuration file does not support "env"` / redirected config rejects env
Wrangler 4.64+ rejects `env` in a *redirected* config. `scripts/inject-wrangler-env.mjs`
(run by `cf:staging`) re-injects `env` into `.output/server/wrangler.json` and removes
the redirect so `--env staging` deploys read it directly. No manual strip step.

### `papaparse` RollupError / passkey/tsyringe errors
Add the CF stubs + `nitro.alias` (see scaffolder output / `apps/velo`).

### KV namespace not found by `sync:ids`
It matches the auto-provisioned title `<worker-name>-<binding>` (e.g.
`{app}-KV`, `{app}-staging-KV`). The script logs the available titles if no match —
adjust only if your account names them differently.

### Build OOM
Set `NODE_OPTIONS='--max-old-space-size=8192'` (CI sets this).

## Deploy Learnings Location
Per-app deploy gotchas: `docs/projects/{app}/{app}-deploy.md`. Append new fixes there.
Reference implementation for everything above: **`apps/velo`**.
