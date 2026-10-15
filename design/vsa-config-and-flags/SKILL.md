---
name: vsa-config-and-flags
description: Load when you need to know how ANY behavior of the VSA website is configured or toggled — frontend REACT_APP_* env vars, script env vars (RLS_TEST_*, SUPABASE_SERVICE_ROLE_KEY, CONFIRM_DELETE), Supabase Edge Function secrets (GEMINI_API_KEY, VSA_AI_ASSISTANT_ENABLED, GITHUB_DISPATCH_TOKEN…), GitHub Actions secrets, vercel.json headers/caching, or admin-editable database config (application_links windows, event is_published, site_settings, uvsa_network_page_settings, ai_knowledge_base knobs). Also load when ADDING a new configuration axis (env var vs DB row vs constant) or when a feature "works locally but not in prod" and you suspect a missing secret.
---

# VSA Config and Flags Catalog

**What this skill is for.** This is the single catalog of every configuration axis in the VSA website: what each knob is, where it is set, who consumes it, what happens when it is absent, and whether it is production-load-bearing or experimental/legacy. It also contains the checklist for adding a new configuration axis. Because flags drift, every section carries a one-line re-verification command — run it before trusting the table.

**When NOT to use this skill:**

| If you need… | Load instead |
|---|---|
| How to create `.env.local` from scratch, setup traps, node version | `vsa-build-and-env` |
| How to deploy, apply migrations, set secrets in prod, run image migration | `vsa-run-and-operate` |
| RLS policy mechanics, revoke-then-grant view pattern, check-in secrets design | `vsa-supabase-security-reference` |
| Whether a config change is allowed / gated (protected domains, freeze windows) | `vsa-change-control` |
| Seasonal-state policy (what changes when, House reveals, application season) | `vsa-seasonal-operations` |
| Tailwind design tokens themselves (colors, spacing, dark mode) | `vsa-design-system-reference` |
| Running `verify-rls-security.mjs` and interpreting its output | `vsa-diagnostics-and-measurement` |

Jargon used below: **CRA** = Create React App (only env vars prefixed `REACT_APP_` are inlined into the JS bundle at build time — they are PUBLIC, never put secrets in them). **Edge Function** = Deno function under `supabase/functions/`, whose secrets live in Supabase (dashboard/CLI), NOT in this repo. **RLS** = Row Level Security, Postgres per-row access policies.

---

## 1. Frontend env vars (`REACT_APP_*`)

Set in `.env.local` for dev; in GitHub/Vercel secrets for builds. Baked into the bundle at `npm run build` — changing them requires a rebuild, and they are visible to anyone with browser devtools.

Re-verify: `grep -rn "process.env.REACT_APP" src --include="*.ts" --include="*.tsx"` and `cat .env.example`

| Var | Required? | Consumed by | Behavior when absent | Status |
|---|---|---|---|---|
| `REACT_APP_SUPABASE_URL` | YES | `src/lib/supabase.ts` (singleton client), `src/components/features/ai/VsaAiAssistant.tsx` (Edge Function URL), `src/scripts/migrateCabinet.ts` | `supabase.ts` throws `Error('Missing Supabase environment variables')` at module import time (`export const supabase = getSupabaseClient()` runs on load) — the app fails at boot | Production |
| `REACT_APP_SUPABASE_ANON_KEY` | YES | Same three files as above | Same boot failure | Production |
| `REACT_APP_GA4_MEASUREMENT_ID` | No | `src/lib/analytics.ts` (`GA_ID`) | `initGA()` returns early — analytics silently disabled | Production (optional) |
| `REACT_APP_SUPABASE_IMAGE_TRANSFORMS` | No | `src/lib/supabaseImages.ts` (`ENABLE_IMAGE_TRANSFORMS = === 'true'`) | Defaults OFF — plain URLs, no render/image transform params | Experimental flag, default-off (egress guard; see `vsa-failure-archaeology`) |
| `REACT_APP_OPENAI_API_KEY` | No | **NOTHING in code.** Removed from public setup docs in 2026-07 and never needed by the current Ask VSA assistant, which runs server-side via `vsa-ai-assistant`. | No effect | Legacy — safe to omit everywhere. Do NOT reintroduce a client-side AI key |

Notes:
- `src/setupTests.ts` injects fake `REACT_APP_SUPABASE_URL/_ANON_KEY` values so Jest never needs a real `.env.local`.
- **Drift resolved (2026-07-28):** `.env.example` previously omitted the required `REACT_APP_SUPABASE_ANON_KEY` and listed four dead `REACT_APP_PLAUSIBLE_*` vars. Both are fixed — the file now lists the required URL + ANON_KEY pair and GA4 only. **GA4 is the analytics system; Plausible was never wired to anything and has been removed repo-wide** (owner-confirmed 2026-07-28). Re-verify: `grep -c "ANON_KEY" .env.example` (expect 1) and `grep -ric plausible .env.example README.md` (expect 0).
- `process.env.NODE_ENV` is used in `src/components/common/PageError.tsx` and `ErrorBoundary.tsx` (dev-only error detail) — set by CRA automatically, never set it yourself.

## 2. Script/tooling env vars (Node scripts in `scripts/`)

All three main scripts self-load `.env.local` (they parse it into `process.env` if keys are unset).

Re-verify: `grep -n "process.env" scripts/*.mjs scripts/*.ts`

### `scripts/verify-rls-security.mjs` (RLS smoke test)
| Var | Required? | Purpose / default |
|---|---|---|
| `VITE_SUPABASE_URL` OR `REACT_APP_SUPABASE_URL` | YES | Target project (VITE_ checked first, line ~31) |
| `VITE_SUPABASE_ANON_KEY` OR `REACT_APP_SUPABASE_ANON_KEY` | YES | Anon client |
| `RLS_TEST_USER_EMAIL` / `RLS_TEST_USER_PASSWORD` | No | Enables authenticated-member checks; skipped if unset |
| `RLS_TEST_ADMIN_EMAIL` / `RLS_TEST_ADMIN_PASSWORD` | No | Enables admin checks; skipped if unset |
| `RLS_TEST_EVENT_ID`, `RLS_TEST_MEMBER_ID`, `RLS_TEST_DATA_RIGHTS_REQUEST_ID` | No | Real row IDs for targeted probes; dummy UUID used otherwise |
| `RLS_ALLOW_MUTATION_TESTS` | No | Must be exactly `'true'` to run write-path tests. **Guard: leave unset against prod** |

### `scripts/migrate-supabase-images-to-public.ts` (image egress pipeline)
| Var | Required? | Purpose |
|---|---|---|
| `REACT_APP_SUPABASE_URL` | YES | Target project |
| `SUPABASE_SERVICE_ROLE_KEY` (falls back to `REACT_APP_SUPABASE_ANON_KEY` for dry-run reads) | YES for `--apply` | **Guard: script refuses `--apply` without the service key.** Service role bypasses RLS — never put it in `.env.example`, frontend vars, or client code |
| `GITHUB_REF`, `CI` / `GITHUB_ACTIONS` | Auto | CI-detection for branch-safety behavior |

### `scripts/cleanup-stale-photo-requests.mjs`
| Var | Required? | Purpose |
|---|---|---|
| `REACT_APP_SUPABASE_URL` OR `SUPABASE_URL` | YES | Target project |
| `SUPABASE_SERVICE_ROLE_KEY` | YES | Admin deletes |
| `CONFIRM_DELETE` | No | Dry-run unless exactly `'true'` — the guard IS the default |

`scripts/verify-ace-import.mjs` reads no env vars (as of 2026-07-06). Operation runbooks for these scripts live in `vsa-run-and-operate` / `vsa-diagnostics-and-measurement`.

## 3. Edge Function secrets (Supabase-side, never in this repo)

Set via Supabase dashboard or `supabase secrets set`. `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` are auto-injected by the platform into every function.

Re-verify: `grep -rn "Deno.env.get" supabase/functions`

| Secret | Function | Purpose / behavior when absent |
|---|---|---|
| `GEMINI_API_KEY` | `vsa-ai-assistant` | Ask VSA LLM calls; absent → assistant errors |
| `GEMINI_MODEL` | `vsa-ai-assistant` | Model override; defaults to `DEFAULT_GEMINI_MODEL = "gemini-3.1-flash-lite"` (`index.ts` line ~32, as of 2026-07-06) |
| `VSA_AI_ASSISTANT_ENABLED` | `vsa-ai-assistant` | **Kill switch**: set to string `"false"` to disable the assistant; any other value (or unset) = enabled |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `GA4_PROPERTY_ID` | `analytics-proxy` | GA4 Data API OAuth quartet; each is `getRequiredEnv` — absent → structured error (`GOOGLE_OAUTH_*` / `GA4_*` codes) returned to admin dashboard |
| `IMAGE_MIGRATION_WEBHOOK_SECRET` | `trigger-event-image-migration`, `trigger-house-event-image-migration` | Shared secret the caller must present; absent/mismatch → request rejected |
| `GITHUB_DISPATCH_TOKEN` | both trigger-* functions | PAT used to fire `repository_dispatch` to GitHub |
| `GITHUB_REPOSITORY` | both trigger-* functions | `owner/repo` target for dispatch |
| `GITHUB_DISPATCH_EVENT_TYPE` | `trigger-event-image-migration` | Defaults to `event-image-migration-requested` |
| `GITHUB_DISPATCH_EVENT_TYPE_HOUSE` | `trigger-house-event-image-migration` | Defaults to `house-event-image-migration-requested` |

Retired secret: `OPENAI_API_KEY` belonged to the legacy `secure-ai` path, which was removed from repo source in issue #353 after source search found no callers. No current `supabase/functions` code reads it. Deleting the directory does not undeploy the function or unset the Supabase secret; those remain manual production cleanup steps.

## 4. GitHub Actions secrets

Re-verify: `grep -n "secrets\." .github/workflows/*.yml`

| Secret | Workflow(s) | Purpose |
|---|---|---|
| `REACT_APP_SUPABASE_URL` | `deploy.yml` (build + Docker build-args), `migrate-images.yml`, `migrate-event-images.yml` | Baked into CI builds; project target for migration scripts |
| `REACT_APP_SUPABASE_ANON_KEY` | `deploy.yml` (build + Docker build-args) | Same |
| `SUPABASE_SERVICE_ROLE_KEY` | `migrate-images.yml`, `migrate-event-images.yml` | Image-migration `--apply` runs (RLS bypass) |
| `VERCEL_TOKEN` | `deploy.yml` | Prod deploy via `npx vercel --prod`; **guard: the deploy step checks `if [ -z VERCEL_TOKEN ]` and skips deploy if unset** |
| `ORG_ID`, `PROJECT_ID` | `deploy.yml` | Exported as `VERCEL_ORG_ID` / `VERCEL_PROJECT_ID` for the Vercel CLI |
| `GITHUB_TOKEN` | `deploy.yml` | Built-in token; ghcr.io Docker registry login |

## 5. `vercel.json` (hosting config)

Re-verify: `cat vercel.json`

| Field | Value | Why |
|---|---|---|
| `version: 2` | — | Vercel platform v2 config schema |
| `zero-config` | Vercel automatically detects CRA | Runs `npm run build` (CRA) and serves the static `build/` directory — this is a static SPA, no server functions on Vercel |
| `headers` `/(.*)` | Security headers on every response | `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` (denies camera/mic/geolocation/etc.), `X-Frame-Options: DENY`, `Strict-Transport-Security: max-age=31536000; includeSubDomains`. Do not weaken these |
| `/static/**` | no explicit `Cache-Control` | Deliberate: an explicit immutable header could also be applied to a missing-chunk 404 and pin it for a year. Hashed assets use Vercel's built-in static caching |
| `headers` SPA routes and `/index.html` | `Cache-Control: public, max-age=0, must-revalidate` | The HTML references the hashed bundles, so browsers must revalidate it on every navigation (matches Vercel's default; pinned so it cannot silently regress) |
| `rewrites` `/((?!static/).*)` → `/index.html` | — | SPA fallback so React Router handles deep links. Excludes `/static/` so a missing chunk 404s instead of returning HTML. Rewrites run after the filesystem, so real files (images, manifest) are served first |
| `src/utils/chunkLoadRecovery.ts` | One automatic reload per 60s on a stale-chunk error | Self-heals tabs opened before a deploy; guarded by `sessionStorage` so it cannot loop |

## 6. Database-resident config (admin-editable "flags")

These are runtime knobs living in Postgres rows — changeable without a deploy, via `/admin` UI or SQL. Schema source of truth: `supabase/migrations/`.

Re-verify: `ls supabase/migrations | grep -i "setting\|application_link\|publish\|knowledge"`

### `application_links` — application/interest-form windows
Source: `supabase/migrations/20260604000000_create_application_links.sql`.

- Nine allowed keys (CHECK constraint): `ace_application`, `house_fall`, `house_winter`, `house_spring`, `intern_application`, `cabinet_application`, `vcn_stage_ninja_interest`, `vcn_props_team_interest`, `wnc_team_form`.
- Per-row knobs: `open_at` / `due_at` (window; CHECK `due_at > open_at`), `is_enabled`, `title`, `description`, `button_label`, `target_url`, `before_open_message`, `after_close_message`, `sort_order`.
- **Privacy invariant**: base table has NO public read policy (admin-only CRUD). Public reads go through the `public_application_links` view (defined at line ~125 of the migration): `target_url` is `null` unless `is_enabled AND now() BETWEEN open_at AND due_at`, and a computed `status` column returns `'disabled' | 'not_open' | 'closed' | 'open'`. Closed/future URLs must never be exposed publicly — do not "simplify" this into a public-select policy on the base table. (View grant mechanics: `vsa-supabase-security-reference`.)
- Audit trigger auto-fills `created_by`/`updated_by` from `auth.uid()`.

### `events.is_published` — event draft/publish flag
Source: `supabase/migrations/20260602000000_add_event_publish_status.sql`. Boolean, default `true` (pre-existing events stayed public). Public select policy is `using (is_published = true)`; a separate admin policy sees all. Every public consumer must exclude drafts — the RLS policy enforces it even if frontend code forgets.

### `site_settings` — global site row
Source: `supabase/migrations/20260424000000_create_site_settings.sql` (+ `..._fix_site_settings_rls.sql`). Singleton row `id='global'` with `logo_url`, `logo_alt`. Public read, admin update via `/admin/settings`. Also creates the public `site_assets` storage bucket (admin upload/delete).

### `uvsa_network_page_settings` — UVSA Network page copy
Source: `supabase/migrations/20260704000000_create_uvsa_network_page_settings.sql`. Singleton row `id='main'` (CHECK-enforced) holding ~15 text columns of hero/intro/stats/showcase/empty-state copy, each with a sensible default. Public read, admin manage. Pattern to copy when making page copy admin-editable.

### `ai_knowledge_base` — Ask VSA v2 knobs
Sources: table + `is_active`/`is_public` (both default `true`) created in `supabase/migrations/20260526000002_create_ai_assistant_tables.sql`; v2 columns added in `20260704000000_ai_knowledge_v2_schema.sql`: `aliases text[]`, `confidence` (default `'high'`), `freshness` (default `'stable'`), `academic_year`, `valid_until timestamptz`. Public read policy requires `is_public = true AND is_active = true`. Dedupe convention (`20260704000001_ai_knowledge_v2_dedupe.sql`): deactivate rows (`is_active=false`), never delete. Behavior rules live in the Edge Function `SYSTEM_PROMPT`; only volatile FACTS belong in these rows. Deploy ordering (migrations → frontend → edge function) is owned by `vsa-run-and-operate`.

### Seasonal state — computed, NOT configured
`src/utils/seasonalState.ts`: season is **derived from the date** (America/Los_Angeles): `summer_break` between June 15 and Sept 15 (constants `SUMMER_BREAK_START/END`), else `active_year`. There is no DB flag or env var for it — to change the window you edit the constants and ship a build. Policy for what each season means: `vsa-seasonal-operations`.

## 7. Build-time config files

Re-verify: `node -e "const p=require('./package.json');console.log(Object.keys(p.jest),p.browserslist)"` and `head -5 tailwind.config.js tsconfig.json`

| File | Config that matters |
|---|---|
| `tailwind.config.js` | `darkMode: 'class'`; `content: ['./src/**/*.{js,jsx,ts,tsx}']`; brand token scales (`brand`, `coral`, gold…). Token semantics live in `vsa-design-system-reference` |
| `tsconfig.json` | `strict: true`, `noEmit: true` (CRA's Babel does the emitting), `jsx: react-jsx`, `target: es5`, `isolatedModules: true` |
| `package.json » jest` | `transformIgnorePatterns: ["node_modules/(?!(zod|@hookform/resolvers)/)"]` — the fix for zod's ESM "Unexpected token 'export'" in Jest. Extend the parenthesized list if a new ESM-only dep breaks tests (traps: `vsa-build-and-env`) |
| `package.json » browserslist` | production: `>0.2%, not dead, not op_mini all`; development: last 1 chrome/firefox/safari |
| `supabase/config.toml` | Local Supabase CLI stack config; line 74 still contains Supabase Studio's `openai_api_key = "env(OPENAI_API_KEY)"`. This is not a VSA Edge Function consumer; no current `supabase/functions` code reads it after issue #353. |

## 8. How to add a new configuration axis — checklist

First decide WHERE it lives:

| Choose | When | Existing pattern to copy |
|---|---|---|
| **DB row (admin-editable)** | Non-engineers must change it without a deploy (copy, links, windows, on/off per content item) | Singleton table: `uvsa_network_page_settings` (CHECK-locked single id, defaults, public read + admin manage). Windowed/masked: `application_links` (no public base-table read, masking view) |
| **Env var / secret** | Differs per environment, or is secret | Frontend behavior flag: `REACT_APP_SUPABASE_IMAGE_TRANSFORMS` (`=== 'true'`, default off). Server secret: Edge Function `Deno.env.get` with explicit `getRequiredEnv`-style failure |
| **Code constant** | Changes at most yearly and needs tests | `seasonalState.ts` date constants (has a test file) |

Then:

1. **Secrets never go client-side.** Anything `REACT_APP_*` ships in the public bundle. Service-role keys, API keys, webhook secrets → Edge Function secrets or GitHub Actions secrets only.
2. **Default to safe.** Flags that guard risky behavior must require the explicit string `'true'` to activate (pattern: `CONFIRM_DELETE`, `RLS_ALLOW_MUTATION_TESTS`, `REACT_APP_SUPABASE_IMAGE_TRANSFORMS`). Kill switches should disable only on explicit `"false"` (pattern: `VSA_AI_ASSISTANT_ENABLED`).
3. **New config TABLE ⇒ full RLS treatment**: enable RLS, admin policies via `user_profiles.is_admin`, and if you add any VIEW, apply revoke-all-then-grant-SELECT (the ALTER DEFAULT PRIVILEGES / auto-updatable-view gotcha — see `vsa-supabase-security-reference` before writing the migration).
4. **Never publicly expose inactive/closed values** (application_links masking is the precedent).
5. **Update `.env.example`** for any new frontend/script env var (placeholder value + comment; never a real value). Note the existing drift in §1 — don't make it worse.
6. **Wire every consumer or don't add it**: the `REACT_APP_PLAUSIBLE_*` block sat in `.env.example` for months reading nothing, and was removed 2026-07-28 — that is what unconsumed config drift costs.
7. **Classify the change** with `vsa-change-control` (config touching points/attendance/leaderboard/RLS is gated).
8. **Update THIS skill's catalog** and its re-verification command.

## Provenance and maintenance

All facts verified against the repo on branch `codex/reactbits-ui`, 2026-07-06. Sources: `.env.example`, `vercel.json`, `package.json`, `tsconfig.json`, `tailwind.config.js`, `src/lib/{supabase,analytics,supabaseImages}.ts`, `src/setupTests.ts`, `src/utils/seasonalState.ts`, `src/components/features/ai/VsaAiAssistant.tsx`, `scripts/{verify-rls-security,cleanup-stale-photo-requests}.mjs`, `scripts/migrate-supabase-images-to-public.ts`, `supabase/functions/*/index.ts`, `supabase/config.toml`, `.github/workflows/{deploy,migrate-images,migrate-event-images}.yml`, `supabase/migrations/{20260424000000_create_site_settings,20260602000000_add_event_publish_status,20260604000000_create_application_links,20260704000000_create_uvsa_network_page_settings,20260526000002_create_ai_assistant_tables,20260704000000_ai_knowledge_v2_schema,20260704000001_ai_knowledge_v2_dedupe}.sql`, `README.md`.

Drift re-verification one-liners (run all before relying on a section):

```bash
grep -rn "process.env.REACT_APP" src --include="*.ts" --include="*.tsx"   # §1 frontend vars
cat .env.example                                                          # §1 example drift
grep -n "process.env" scripts/*.mjs scripts/*.ts                          # §2 script vars
grep -rn "Deno.env.get" supabase/functions                                # §3 edge secrets
grep -n "secrets\." .github/workflows/*.yml                               # §4 CI secrets
cat vercel.json                                                           # §5 hosting
ls supabase/migrations | grep -i "setting\|application_link\|publish\|knowledge\|ai_assistant"  # §6 DB config
grep -n "application_key in" -A 12 supabase/migrations/20260604000000_create_application_links.sql  # §6 nine keys
node -e "console.log(require('./package.json').jest, require('./package.json').browserslist)"       # §7 build config
grep -rn "PLAUSIBLE\|REACT_APP_OPENAI" src scripts public .env.example 2>/dev/null  # §1 dead client config (expect no hits; .env.example documents the server-side OPENAI_API_KEY on purpose)
```
