---
name: vsa-build-and-env
description: Load when setting up the VSA website dev environment from scratch, or when setup-shaped things break — npm install/ci problems, "Missing Supabase environment variables" on boot, Jest failing with "Unexpected token 'export'" from zod, TypeScript syntax that won't compile, node version confusion, .env.local questions, Docker local run, or Supabase CLI/migrations/Edge Function first-time provisioning. Provides the from-zero runbook, every known setup trap, and a verify-your-setup checklist.
---

# vsa-build-and-env — Recreate the dev environment from scratch

**What this skill is for.** A zero-context engineer or AI session lands on this repo (Create React App + TypeScript frontend, Supabase backend) and needs a working development environment: correct Node, dependencies installed, `.env.local` populated (or deliberately stubbed), and — for full-fidelity work — a Supabase project with migrations and Edge Functions. This skill is the single home for setup steps and setup traps. "CRA" = Create React App, the framework wrapping this project's build tooling (`react-scripts`).

**When NOT to use this skill:**

| You actually want | Go to |
|---|---|
| Deploying, the real deploy path, applying migrations to prod, Edge Function deploy procedure, image-migration pipeline operation | `vsa-run-and-operate` |
| The full catalog of every env var, Edge Function secret, GitHub secret, and settings table | `vsa-config-and-flags` |
| Why degraded mode exists and the invariants around it | `vsa-architecture-contract` |
| Writing new migrations safely (RLS, view grants) | `vsa-supabase-security-reference` |
| What counts as passing verification / evidence standards | `vsa-validation-and-qa` |
| A bug that isn't setup-shaped | `vsa-debugging-playbook` |

---

## 1. From-zero setup runbook

### 1.1 Node version

| Source | Says |
|---|---|
| `README.md` ("Prerequisites") | Node.js 22 (points at `.nvmrc`) |
| `.github/workflows/deploy.yml` (`NODE_VERSION: '22'`, line 17) | CI lints/tests/builds on Node 22 |
| `.github/workflows/migrate-images.yml`, `migrate-event-images.yml` | Node 22 |
| `Dockerfile` (line 2) | `node:22-alpine` (container build only) |

**Use Node 22** — CI, `.nvmrc`, `engines`, the Dockerfile, and the devcontainer all agree as of 2026-07-29 (#324). `.nvmrc` exists, so `nvm use` inside the repo resolves it; `engines: ">=22"` makes npm warn on a mismatch (advisory, not enforced). Verified 2026-07-29 on Node 22.22.2: `npm ci`, `npm run build`, `npm run lint`, and all 15 test suites / 126 tests pass.

### 1.2 Install dependencies

```bash
cd /path/to/vsa-website
npm ci        # exact lockfile install — use this for a clean/reproducible env (CI and Dockerfile use it)
# or
npm install   # fine for day-to-day; may update package-lock.json — don't commit lockfile churn you didn't intend
```

Do NOT run `npm audit fix --force` or upgrade `typescript`/`react-scripts` casually — see the traps table (section 4).

### 1.3 Create `.env.local`

```bash
cp .env.example .env.local
```

**Fixed 2026-07-29:** `.env.example` previously omitted `REACT_APP_SUPABASE_ANON_KEY`, so copying it produced an app that crashed on boot. It now lists both required vars and marks them as required. Final `.env.local` for normal development:

```env
REACT_APP_SUPABASE_URL=https://<project-ref>.supabase.co
REACT_APP_SUPABASE_ANON_KEY=<anon public key>

# Optional analytics (consumed only in src/lib/analytics.ts)
REACT_APP_GA4_MEASUREMENT_ID=
```

Where each credential comes from:

| Variable | Source | Required? |
|---|---|---|
| `REACT_APP_SUPABASE_URL` | Supabase dashboard → Project Settings → API → Project URL | Yes — app throws on boot without it (`src/lib/supabase.ts` L9–13) |
| `REACT_APP_SUPABASE_ANON_KEY` | Same page → `anon` `public` API key (safe for browsers; RLS enforces access) | Yes — same throw |
| `REACT_APP_GA4_MEASUREMENT_ID` | Google Analytics 4 property | No |
| `REACT_APP_OPENAI_API_KEY` | **Removed from `README.md`, `CLAUDE.md`, and `AGENTS.md` on 2026-07-29** and consumed nowhere in `src/`. `OPENAI_API_KEY` (no `REACT_APP_` prefix) has no current repo consumer after issue #353 removed the legacy `secure-ai` Edge Function. Never reintroduce a client-side AI key — `REACT_APP_*` ships in the public bundle. | No |

CRA only exposes env vars prefixed `REACT_APP_` to the browser bundle, and they are **baked in at build time** — after editing `.env.local`, restart `npm start`. Never commit `.env*` files (`.gitignore` lines 16–23 cover them; committing secrets is on the AGENTS.md never-do list). Full config-axis catalog: `vsa-config-and-flags`.

### 1.4 Start the dev server

```bash
npm start     # http://localhost:3000
```

Note the script is `node ./node_modules/react-scripts/bin/react-scripts.js start`, not bare `react-scripts start` — deliberate, see traps table.

---

## 2. What runs WITHOUT Supabase credentials (degraded mode)

"Degraded mode" = public pages render static fallback content instead of crashing when Supabase calls fail (outage, egress/bandwidth quota exhaustion, network failure). It is an architectural invariant (AGENTS.md "Degraded mode"; rationale in `vsa-architecture-contract`).

**How it actually works — verified in code 2026-07-06:**

- `src/lib/supabase.ts` throws `Missing Supabase environment variables` **at module load** if either `REACT_APP_SUPABASE_URL` or `REACT_APP_SUPABASE_ANON_KEY` is empty/absent (L9–13, and `export const supabase = getSupabaseClient()` at L29 runs on import). Because `AuthContext` imports it, **the app does NOT boot with a truly empty env.** Degraded mode is about *failing calls*, not *missing credentials*.
- `src/utils/isSupabaseUnavailable.ts` classifies an error as an outage on HTTP 402/429/503/504, `TypeError` (network/CORS), or message/code fragments like `fetch failed`, `quota`, `egress`, `bandwidth`.
- 12+ public surfaces import it (Events, Leaderboard, Cabinet, Gallery, Calendar, House/HouseDetail, FindMyPoints, Points, UVSANetwork, VcnCurrent/VcnArchive, ApplicationCTA — per graphify) and fall back to `src/config/publicFallbackContent.ts` or render `ContentUnavailableState`.

**Contributor-without-keys recipe** — start working before you have real credentials by supplying syntactically valid placeholders:

```env
REACT_APP_SUPABASE_URL=https://placeholder.supabase.co
REACT_APP_SUPABASE_ANON_KEY=placeholder-anon-key
```

The client constructor only needs a well-formed URL and a non-empty key; every query then fails at the network layer, `isSupabaseUnavailable()` returns true, and public pages show fallback content. Auth-dependent surfaces (`/profile`, `/points` check-in, `/admin/*`) will not function. (Behavior derived from reading `src/lib/supabase.ts` + `isSupabaseUnavailable.ts`; not runtime-tested in the session that wrote this — if it misbehaves, re-verify and update this section.)

---

## 3. Supabase side for full-fidelity work

For real data, auth, and admin flows you need an actual Supabase project. (Applying migrations to the shared production project is a deploy/ops action — procedure and ordering rules live in `vsa-run-and-operate`. This section is about provisioning your own project or local stack.)

1. **Create a project** at supabase.com (or run the local stack: `supabase/config.toml` exists with `project_id = "vsa-website"`, Postgres major version 15, local ports API 54321 / DB 54322 / Studio 54323 — a `supabase start` local stack is configured but was not runtime-verified here).
2. **Apply migrations in filename-timestamp order.** `supabase/migrations/` is the source of truth for the schema — 89 files as of 2026-07-06, from `20240320000000_create_user_profiles.sql` onward. The Supabase CLI (`supabase db push --local`, `supabase migration up`, `supabase db reset`) applies them in order — **only against your own local stack or a disposable project you created**. Never point `db push` at the shared production project: its migration history has drifted from the repo (41 recorded versions vs 122 files, checked 2026-10-08), so the CLI would try to replay already-applied migrations. The production path is in `vsa-run-and-operate` §3. Migration *authoring* rules (RLS, the view-grants gotcha): `vsa-supabase-security-reference`.
3. **Deploy Edge Functions you need** (Deno functions in `supabase/functions/`) and set their secrets. Secret names verified in each function's `index.ts` (2026-07-06). `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `SUPABASE_SERVICE_ROLE_KEY` are auto-injected by the platform — you do not set those.

| Function | Secrets you must set | Purpose |
|---|---|---|
| `vsa-ai-assistant` | `GEMINI_API_KEY` (required); `GEMINI_MODEL`, `VSA_AI_ASSISTANT_ENABLED` (optional; `"false"` = kill switch) | Ask VSA chat |
| `analytics-proxy` | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `GA4_PROPERTY_ID` | Admin analytics dashboard |
| `trigger-event-image-migration` / `trigger-house-event-image-migration` | `IMAGE_MIGRATION_WEBHOOK_SECRET`, `GITHUB_REPOSITORY`, `GITHUB_DISPATCH_TOKEN`; optional `GITHUB_DISPATCH_EVENT_TYPE` / `GITHUB_DISPATCH_EVENT_TYPE_HOUSE` | Kick image-migration GitHub workflows |

`secure-ai` was removed from the repo in issue #353. Removing the directory does not undeploy the Supabase function; a human still needs to delete the deployed function and unset `OPENAI_API_KEY`.

```bash
supabase functions deploy vsa-ai-assistant
supabase secrets set GEMINI_API_KEY=<key>
```

(Exact deploy procedure, ordering with migrations/frontend, and ops: `vsa-run-and-operate`. Full secret catalog: `vsa-config-and-flags`.)

4. **AGENTS.md hard rule:** never touch `supabase/.temp/cli-latest` (a CLI-managed marker file that exists in this repo). Don't stage it, don't delete it, don't "clean it up".

---

## 4. Known traps table

| Trap | Observable fact | Symptom if you break it | Rule |
|---|---|---|---|
| npm scripts wrap react-scripts in `node` | All CRA scripts in `package.json` are `node ./node_modules/react-scripts/bin/react-scripts.js <cmd>` | Reverting to bare `react-scripts build` breaks the Vercel build with a bin-permission error (commits `96ba2eee`, `edd9c161` "run react-scripts via node to bypass vercel bin permissions"; `Dockerfile` needs `chmod +x node_modules/.bin/*` for the same reason) | Never "simplify" these scripts |
| Jest `transformIgnorePatterns` | `package.json` jest block: `node_modules/(?!(zod|@hookform/resolvers)/)` | Without it, tests importing zod/resolvers die with `SyntaxError: Unexpected token 'export'` or `Cannot use import statement outside a module` from `node_modules/` (Jest doesn't transform ESM deps by default) | Extend the allowlist if a new ESM-only dep breaks tests; don't delete it |
| TypeScript pinned at `^4.9.5` | `package.json` dependency; react-scripts 5.0.1 tooling | TS 5.x-only syntax (`const` type parameters, `using` declarations, standard decorators, import attributes) fails to compile; `satisfies` is fine (it's 4.9) | Don't upgrade TS as a drive-by; don't write TS-5-only syntax |
| CRA eject is forbidden | AGENTS.md never-do: "Don't run `npm run eject`" | Ejecting is permanent and irreversible | Never eject |
| `src/react-app-env.d.ts` is auto-generated | One line: `/// <reference types="react-scripts" />` | AGENTS.md never-do: don't touch it; CRA regenerates it | Never edit |
| `.gitignore` may carry local-only edits | AGENTS.md startup rule | Staging it commits someone's local setup | Never stage `.gitignore` unless explicitly requested |
| Tests default to watch mode | `npm test` is CRA watch mode; CI runs `CI=true npm test -- --coverage --watchAll=false` (deploy.yml line 42) | A bare `npm test` hangs an agent/CI session forever | Always `CI=true npm test -- --watchAll=false` in non-interactive contexts |
| ~~`.env.example` is incomplete~~ | RESOLVED 2026-07-29 (#323) — the anon key line is present and required vars are marked | Was a `Missing Supabase environment variables` crash after a faithful `cp` | `cp .env.example .env.local` now works as documented |
| Env vars baked at build time | CRA inlines `REACT_APP_*` during build; Docker bakes them via build `ARG`s | Editing `.env.local` does nothing to a running dev server or an existing Docker image | Restart `npm start` / rebuild the image |
| Node version mismatch across sources | RESOLVED 2026-07-29 — CI, `.nvmrc`, `engines`, Dockerfile, devcontainer all say 22 | Was a local-vs-CI build difference | `nvm use` in the repo root |
| `npm install` rewrites the lockfile | `package-lock.json` churn in diffs | Noisy/unreviewable PRs | Use `npm ci` for clean envs; don't commit unintended lockfile changes |

---

## 5. Optional paths

### 5.1 Optional: Docker/nginx local run

Not needed for daily dev (`npm start` is faster); useful for verifying the production container. Multi-stage `Dockerfile` (node:22-alpine build → nginx:alpine serving `build/` with `nginx.conf`); `docker-compose.yml` maps host 3000 → container 80 and passes the two Supabase vars as build args:

```bash
REACT_APP_SUPABASE_URL=... REACT_APP_SUPABASE_ANON_KEY=... docker compose up --build
# → http://localhost:3000
```

Credentials are baked into the image at build time — changing them requires `--build` again.

### 5.2 Optional: Graphify (codebase knowledge graph)

The repo enforces query-first exploration (`AGENTS.md` "Graphify: Query-First Workflow"). Install per AGENTS.md:

```bash
uv tool install graphifyy    # or: pipx install graphifyy
```

Always invoke via the wrapper — subagent/hook PATH typically excludes `~/.local/bin`:

```bash
./scripts/graphify-run query "<question>"
./scripts/graphify-run hook status
```

Orientation doc: `graphify-out/GRAPH_REPORT.md`. Never commit `graphify-out/cost.json` or the cache dir. Do not install/rebuild Graphify inside a feature PR.

---

## 6. Verify-your-setup checklist

Run all three; each must exit 0 (`echo $?` prints the exit code of the last command).

```bash
npm run lint
# Acceptable: exits 0, little or no output. ESLint over src/**/*.{ts,tsx}.

npm run build
# Acceptable: exits 0, "Compiled successfully" (or "Compiled with warnings"),
# build/ directory created with static/js and static/css bundles.

CI=true npm test -- --watchAll=false
# Acceptable when the full suite is the assigned check: exits 0, all suites pass.
# Derive the current files with: find src -name "*.test.ts*" | sort.
# The canonical inventory and verification-ownership rules live in
# vsa-validation-and-qa sections 1-2.
# jsdom, ThemeProvider, and Framer Motion console warnings are ACCEPTABLE when
# the exit code is 0 (AGENTS.md "Testing").
```

Then boot the app:

```bash
npm start
# http://localhost:3000 — with real credentials, the home page loads live content;
# with placeholder credentials, public pages render fallback content (section 2).
```

If lint/build/test standards or "what counts as evidence" are the question, see `vsa-validation-and-qa`.

---

## Provenance and maintenance

Written 2026-07-06 against branch `codex/reactbits-ui` (clean tree, HEAD `368fbf63`). All claims verified by reading repo files on that date. Sources: `package.json`, `.env.example`, `tsconfig.json`, `README.md`, `AGENTS.md`, `Dockerfile`, `docker-compose.yml`, `nginx.conf`, `supabase/config.toml`, `supabase/migrations/` (listing), `supabase/functions/*/index.ts` (secret names), `.github/workflows/deploy.yml` + `migrate-images.yml` + `migrate-event-images.yml`, `.gitignore`, `src/lib/supabase.ts`, `src/utils/isSupabaseUnavailable.ts`, `src/react-app-env.d.ts`, git commits `96ba2eee` and `edd9c161`.

Re-verify before trusting drift-prone facts:

```bash
grep -n -A 15 '"scripts"' package.json                          # script definitions, node-wrapped react-scripts
grep -n -A 3 'transformIgnorePatterns' package.json             # jest ESM allowlist
grep -n '"typescript"' package.json                             # TS pin (4.9.5)
cat .env.example                                                # still missing ANON_KEY?
grep -n 'REACT_APP_' src/lib/supabase.ts src/lib/analytics.ts   # env vars actually consumed
grep -rn 'REACT_APP_OPENAI' src/ || echo "still unused"         # legacy key still unused?
grep -n 'NODE_VERSION' .github/workflows/deploy.yml             # CI node version
grep -rn 'Deno.env.get' supabase/functions/*/index.ts           # Edge Function secret names
ls supabase/migrations | wc -l                                  # migration count (89 as of 2026-07-06)
ls supabase/functions                                           # function list
git log --oneline -3 -- Dockerfile docker-compose.yml           # container setup drift
```
