---
name: vsa-run-and-operate
description: Load when running or deploying the VSA website, or operating its production machinery — "how do I deploy this?", "what actually ships to production?", applying supabase/migrations/ to prod, deploying Edge Functions (supabase functions deploy), running the image-migration pipeline (npm run migrate:images:*, migrate-images.yml, migrate-event-images.yml), operating scripts/ helpers, or figuring out where an artifact (build/, public/images/, ghcr image, Vercel deployment) lands. Provides the real deploy path (Vercel, not Docker), the migrations→frontend→edge-function ordering rule, and the never-delete-Storage-originals rule.
---

# VSA Run & Operate

**What this is for.** The operations manual for the VSA website: what `npm start`/`npm run build` actually produce, what REALLY deploys production (resolved with evidence — it's Vercel; the Docker image is a dead end), how schema migrations reach the production database (manually, in a strict order), how the five Supabase Edge Functions are deployed and configured, and how to run the image-migration pipeline that exists because of the Supabase egress crisis ("egress" = data transferred out of Supabase, which is billed/quota'd; serving images from Supabase Storage burned through the free-tier egress quota).

**When NOT to use this skill:**

| If you need... | Load instead |
|---|---|
| Setting up a dev environment from zero, `.env.local`, npm/jest/node traps | `vsa-build-and-env` |
| Whether a change is even allowed, PR/branch conventions, the manual-migration *policy* and freeze windows | `vsa-change-control` |
| Writing migration SQL safely (RLS, grants, view gotchas) | `vsa-supabase-security-reference` |
| Full incident narratives (egress crisis, RLS recursion) | `vsa-failure-archaeology` |
| Env var / secret *catalog* (every axis of configuration) | `vsa-config-and-flags` |
| Verifying a change works (test/lint/build evidence bar) | `vsa-validation-and-qa` |
| Something is broken and you don't know why | `vsa-debugging-playbook` |

---

## 1. Local run

`npm start` serves the CRA (Create React App) dev server on `http://localhost:3000`. `npm run build` emits a static bundle into `build/` (`npm run build:production` is an identical alias — both run `react-scripts build`, see `package.json`). Both need `REACT_APP_SUPABASE_URL` and `REACT_APP_SUPABASE_ANON_KEY` in `.env.local`; without them the app boots into degraded mode or errors — see `vsa-build-and-env` for the from-zero runbook and setup traps. An optional Docker path exists (`Dockerfile`: node:22-alpine build stage → nginx stage serving `build/` on port 80 with an SPA `try_files $uri $uri/ /index.html` fallback in `nginx.conf`; `docker-compose.yml` wraps it) — useful for a local prod-like check, **not** part of the production deploy path (see §2).

```bash
npm start                        # dev server on :3000
npm run build                    # static bundle → build/
npx serve -s build               # quick local check of the prod bundle (optional)
```

## 2. THE production deploy path (resolved, as of 2026-07-06)

**Production is a static Vercel deployment of `build/`. Nothing else serves production.** Evidence trail:

`vercel.json` configures security/cache headers and an SPA fallback while relying on Vercel zero-config for the CRA build (abridged; it uses the current `headers`/`rewrites` format, not the old `routes`):

```json
{
  "version": 2,
  "headers": [
    { "source": "/((?!static/)[^.]*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }] }
  ],
  "rewrites": [{ "source": "/((?!static/).*)", "destination": "/index.html" }]
}
```

Rewrites run after the filesystem check, so real files are served first and any other URL serves `index.html` for React Router. The rewrite deliberately **excludes `/static/`**: a stale tab asking for a chunk a newer deploy removed must get a 404, not `200 text/html` (which surfaces as MIME/`Unexpected token '<'` errors). Security headers (HSTS, X-Frame-Options DENY, nosniff) apply to every route in the same file. `AGENTS.md` (line 13) confirms: "Deployed to: Vercel (zero-config CRA build, SPA fallback in `vercel.json`)".

Re-verify: `cat vercel.json`

### What `.github/workflows/deploy.yml` actually does

| Job | Runs when | Does |
|---|---|---|
| `test` | every push to `main`/`develop` AND every PR to `main` | `npm ci` → `npm run lint` → `CI=true npm test -- --coverage --watchAll=false` → `npm run build` |
| `security` | same triggers, needs `test` | CodeQL init + Trivy filesystem scan → SARIF upload |
| `build` (Docker) | **only `main`**, needs test+security | builds the `Dockerfile`, pushes to `ghcr.io/hhavynn/vsa-website` |
| `deploy-vercel` | **only `main`**, needs test+security | `npx vercel@latest --prod --token=$VERCEL_TOKEN` — **skipped entirely if the `VERCEL_TOKEN` secret is unset** (explicit check step) |

Resolved facts you must internalize:

1. **The ghcr Docker image is built but consumed by nothing.** `grep -rn ghcr` across the repo hits only `deploy.yml` itself. `scripts/deploy.sh` targets AWS EKS (`aws`/`kubectl`, cluster `vsa-website-cluster`) — there is no EKS cluster referenced anywhere else in the repo; treat that script as legacy/aspirational, never run it against production.
2. **CI runs tests but does not gate anything.** `main` has **no branch protection** (verified 2026-07-06: `gh api repos/hhavynn/vsa-website/branches/main/protection` → HTTP 404 "Branch not protected"). The jobs run, but a failing run blocks neither merges nor the push that already landed. Before pushing, run the proportional final gate assigned by `vsa-validation-and-qa`; application/runtime changes commonly need lint, relevant tests, and build, while docs-only changes use targeted documentation/reference checks. A red CI run is still blocking by convention.
3. **UNVERIFIED — the operative production trigger.** Strong repo evidence says Vercel's *git integration* auto-deploys pushes to `main` independently of deploy.yml: image-migration workflow commits use `[skip ci]` (which skips GitHub Actions, including the `deploy-vercel` job) yet `docs/event-image-migration.md` step 7 says "Wait for Vercel to redeploy (usually 1–3 minutes)" after that push, and `docs/DEPLOYMENT_GUIDE.md` says pushes auto-update the site. That only works if Vercel watches the repo directly. **Question a maintainer must answer:** in the Vercel dashboard (project → Settings → Git), is the GitHub integration connected and deploying `main` to production, and is the `VERCEL_TOKEN` GitHub secret set (making the Actions deploy a redundant second deploy) or unset (making git integration the only path)?

**Manual production deploy** (when you must): `npx vercel --prod` from repo root with the project linked, or trigger a redeploy from the Vercel dashboard. Env vars (`REACT_APP_SUPABASE_URL`, `REACT_APP_SUPABASE_ANON_KEY`) live in Vercel project settings, not in the repo.

## 3. Database operations runbook (migrations)

`supabase/migrations/*.sql` is the **source of truth for schema** (`AGENTS.md` line 162), but nothing applies them automatically — no workflow touches the database schema. **Migrations are applied manually to production, one file at a time, only with owner approval** (policy owned by `vsa-change-control`; SQL-authoring safety owned by `vsa-supabase-security-reference`).

### Do NOT run `supabase db push` against production

Production's migration history does not match the repo, so the CLI cannot tell which files are "pending". Read-only check on 2026-10-08 (project `sxephkrekdztmkptyzca`):

| | Count |
|---|---|
| `.sql` files in `supabase/migrations/` | 122 (112 distinct versions — 10 versions are shared by two files) |
| Rows in prod `supabase_migrations.schema_migrations` | 41 (oldest `20260317084519`, newest `20261009000026`) |
| File versions that match a prod row | 16 |
| File versions with **no** prod row | 96. That includes the 21 renamed-mismatch files below. The other 75 are mostly older files applied by hand in the SQL Editor, which records nothing. |
| Prod rows recorded under a **different** version than the repo file (same name) | 21 — e.g. file `20260704000000_ai_knowledge_v2_schema.sql` is recorded as `20261004225717` |
| Prod rows with **no** repo file | 4 — `add_google_photos_to_gallery_events`, `create_members_and_member_event_attendance`, `members_computed_points_and_merge`, `update_uvsa_school_instagram_urls` |

What `db push` would do against that history (Supabase CLI 2.x behavior; deliberately not executed here): it refuses first, because remote versions are missing locally, and prints a suggested `supabase migration repair --status reverted …`. If someone follows that hint and retries with `--include-all`, the CLI replays every unrecorded file (around 96) against live data. That includes old seed and data migrations, and the duplicated versions conflict on the `schema_migrations` primary key. Do not follow the CLI's repair hint; it is not a routine step (see "Repairing the history" below).

### The real production path (convention since 2026-09-27)

1. **Owner approval** for this specific migration. The PR must already be reviewed. Stub-DB or staging verification follows `supabase/migrations/MIGRATION_CHECKLIST.md`.
2. **Apply the file verbatim** with the Supabase MCP `apply_migration`, one migration per call: `project_id = sxephkrekdztmkptyzca`, `name = <file name without the timestamp prefix or .sql>`, `query = <exact file contents>`. Apply from `main` or the reviewed PR head, and record the file's sha256. If several unapplied files depend on each other (e.g. `20260704000000_ai_knowledge_v2_schema` → `…000001_dedupe` → `…000002_expansion`), apply the **whole chain in one sitting, in filename order**, so their recorded versions keep the same relative order.
   - **SQL Editor is a last resort**, only when the MCP is unavailable. It records **nothing** in `schema_migrations`, so steps 3–4 don't apply. Instead, the same owner approval must cover recording the history right after the apply: `supabase migration repair --linked --status applied <file version>`. That inserts the history row under the file's **existing** version without running the SQL again, so no rename is needed. Skipping this step is how the 75 unrecorded files in the table above came about.
3. **Read the recorded version** (read-only):
   ```sql
   select version, name from supabase_migrations.schema_migrations order by version desc limit 5;
   ```
   `apply_migration` stamps the apply time (UTC, `YYYYMMDDHHMMSS`) as the version, so it almost never equals the file's timestamp.
4. **Check replay order, then rename the repo file to the recorded version.** The recorded version is "now", so the rename moves the file to the end of the replay order (`supabase db reset` and fresh projects replay files in filename order). First confirm that no file sorting between the old and new versions uses objects this migration creates: `ls supabase/migrations | awk '$0 > "<old>" && $0 < "<recorded>"'`, then grep those files for the tables, columns and functions it creates. If one does, **don't rename**. Keep the file name and, with owner approval, repoint the history instead: `supabase migration repair --linked --status reverted <recorded>`, then `--status applied <file version>`. Where a clean local replay is possible, run `supabase db reset --local` to confirm. Today the 10 duplicated versions (see below) may block that, so the grep is the minimum check. When the check passes: `git mv supabase/migrations/<old>_<name>.sql supabase/migrations/<recorded>_<name>.sql`). Leave the contents unchanged. Update every reference (`grep -rn "<old version>" .`), and add an `Applied to production YYYY-MM-DD (schema_migrations version …)` line to the header comment. Ship this as its own small PR, e.g. `chore(migrations): rename <name> migration to its recorded prod version`. Precedents: PR #528 (`20261009000026_historical_attendance_recovery.sql`) and `20260930053224_admin_publish_member_photo.sql`.
5. **Verify after apply**, read-only: check grants, RLS, and function overloads with `docs/rls-verification-checklist.md` / `scripts/verify-rls-security.mjs`.

The 21 mismatches above exist because those files were never renamed to their recorded versions; some predate this convention, and the 2026-10-04 batch skipped step 4. They are history drift, not schema drift. Do not "fix" them by re-applying SQL.

### Repairing the history (owner decision only — not done, not routine)

`supabase migration repair --linked --status applied|reverted <version…>` only inserts or deletes rows in `supabase_migrations.schema_migrations`. It runs no schema SQL, but it **is** a production write, so treat it like any other production mutation: owner approval, a written plan, and a read-only before/after snapshot of `schema_migrations`. A repair that would make `db push` safe again needs:

1. **Prove which files are actually applied.** For each of the ~96 unrecorded files, check the objects it creates against the live catalog. This is read-only. Missing history does not prove a file was applied, and some old files may never have run in production.
2. **Reconcile the 21 version mismatches.** Prefer repointing the history to the existing file versions: mark the recorded rows `reverted` and the file versions `applied`. This leaves filename order, and therefore replay order, untouched. Renaming them in bulk would move files such as `20260704000000_create_uvsa_network_page_settings.sql` by months (to `20260926042952`), past other files that would each need the step-4 order check. Rename only files that pass that check.
3. **Handle the 4 prod-only rows.** Pull their SQL with `supabase migration fetch --linked`, or from `supabase_migrations.schema_migrations.statements`, into repo files. Do not mark them `reverted`, because their changes are live.
4. **Resolve the 10 duplicated file versions** by giving one file of each pair a new unique version. They are forward-only, so the file contents stay the same.
5. Mark the proven-applied files `--status applied`. Then confirm `supabase db push --linked --dry-run` lists **only** genuinely unapplied migrations before anyone uses `db push` for real.

Until all five steps are done and this section is updated, the manual path above is the only supported way to change the production schema. `supabase db push` remains fine against a local stack (`--local`) or a disposable project you created yourself (see `vsa-build-and-env`).

### The iron ordering rule for schema-coupled releases

**Migrations → frontend deploy → Edge Function deploy.** Never invert it.

Why, proven by the Ask VSA v2 case (all in-repo, as of 2026-07-06):

- `supabase/migrations/20260704000000_ai_knowledge_v2_schema.sql` adds columns to `ai_knowledge_base`: `aliases text[]`, `confidence`, `freshness`, `academic_year`, `valid_until` (lines 6–11).
- The admin frontend **writes those exact columns on every save**: `src/data/repos/aiKnowledge.ts` builds its payload with `aliases`, `confidence`, `freshness`, `academic_year`, `valid_until` (lines 80–87; types at lines 29–36). Ship this frontend before the migration and every admin knowledge save fails on unknown columns.
- The Edge Function **reads them**: `supabase/functions/vsa-ai-assistant/index.ts` selects/renders `confidence`, `freshness`, `academic_year` (lines 118–120, 227–229) and its `SYSTEM_PROMPT` (line 34+) instructs archive-language handling for `confidence: medium/low` entries. Deploy the function before the migration and it queries columns that don't exist.

So for any release where frontend or Edge Function code touches new schema: **(1)** apply the migration to production via the manual path above (`apply_migration`, then confirm the recorded version), **(2)** merge/push frontend to `main` and wait for the Vercel deploy, **(3)** `supabase functions deploy <name>`. Additive-only migrations (like `add column if not exists` above) are safe to run ahead of the code; that is exactly why this ordering works without downtime.

Follow-up data migrations `20260704000001_ai_knowledge_v2_dedupe.sql` and `20260704000002_ai_knowledge_v2_expansion.sql` run after the schema file (timestamp order). Note the dedupe deactivates rows (`is_active=false`) rather than deleting — preserve that convention.

## 4. Edge Function operations

Four Deno Edge Functions live in `supabase/functions/` (verify: `ls supabase/functions`). "Edge Function" = Deno TypeScript deployed to Supabase's runtime, invoked at `https://<project-ref>.supabase.co/functions/v1/<name>`.

| Function | Purpose | Secrets it reads (`Deno.env.get`) |
|---|---|---|
| `vsa-ai-assistant` | Current "Ask VSA" public assistant, Gemini-backed; behavior rules in its `SYSTEM_PROMPT`, volatile facts from `ai_knowledge_base` rows | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (auto-provided), `GEMINI_API_KEY`, `GEMINI_MODEL` (optional override), `VSA_AI_ASSISTANT_ENABLED` (kill switch — set to `"false"` to disable) |
| `analytics-proxy` | Serves GA4 report data to `/admin/analytics` (`src/pages/Admin/Analytics.tsx` invokes it) | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (OAuth refresh-token flow, NOT a service account), `GA4_PROPERTY_ID` (numeric ID, not `G-…`), `SUPABASE_URL`, `SUPABASE_ANON_KEY` |
| `trigger-event-image-migration` | DB-webhook receiver: validates secret, checks `events.image_url` changed and points at Supabase Storage, fires GitHub `repository_dispatch` | `IMAGE_MIGRATION_WEBHOOK_SECRET`, `GITHUB_REPOSITORY`, `GITHUB_DISPATCH_TOKEN`, `GITHUB_DISPATCH_EVENT_TYPE` (optional, default `event-image-migration-requested`) |
| `trigger-house-event-image-migration` | Same, for `house_events` | `IMAGE_MIGRATION_WEBHOOK_SECRET`, `GITHUB_REPOSITORY`, `GITHUB_DISPATCH_TOKEN`, `GITHUB_DISPATCH_EVENT_TYPE_HOUSE` (optional, default `house-event-image-migration-requested`) |

Historical cleanup: `secure-ai` was removed from the repository in issue #353. Deleting the directory does not undeploy a Supabase Edge Function; after merge, run `supabase functions delete secure-ai` and `supabase secrets unset OPENAI_API_KEY`.

Operations:

```bash
supabase functions deploy <name>                 # deploy one function (e.g. vsa-ai-assistant)
supabase functions list                          # confirm deployed versions
supabase secrets set GEMINI_API_KEY="..."        # secrets are project-wide, set once
supabase secrets list                            # names only, never prints values
```

Logs: Supabase Dashboard → Edge Functions → *function* → Logs (this is the path the runbooks in `docs/event-image-migration.md` and `docs/admin-analytics-setup.md` use). Deploy order relative to schema changes: see §3.

## 5. The image-migration pipeline (egress-crisis machinery)

This is the most operationally important system in the repo. Background: serving event/House/cabinet images straight from Supabase Storage blew the Supabase egress quota (full story: `vsa-failure-archaeology`). The fix: admin uploads still land in Supabase Storage (browsers cannot write into the repo), then a pipeline downloads, compresses to WebP (≤1200×1200, q80, via `sharp`), commits them under `public/images/…`, and — only after production is confirmed to serve each file — rewrites the DB `image_url`/`thumbnail_url` to `/images/...` so Vercel's edge serves them with zero Supabase egress (two phases, #454: `--apply` writes files + a relink plan and never touches the DB; `--relink` verifies, then does conditional updates). Doc of record: `docs/event-image-migration.md`.

### THE IRON RULE

**NEVER delete the Supabase Storage originals after migration.** `docs/event-image-migration.md` ("Why old Supabase files are not deleted"): deleting immediately breaks CDN/browser caches still pointing at the old URL. Storage is the intentional staging buffer. Cleanup, if ever, is a manual, delayed, human decision after confirming all DB rows point at `/images/...` and caches have expired.

### The script and npm entrypoints

`scripts/migrate-supabase-images-to-public.ts` (run via `tsx`). **Dry run is the default; `--apply` is the only thing that writes.** Categories: `cabinet`, `events`, `gallery`, `houses`, `home`, `house-events`.

```bash
npm run migrate:images:dry                                    # scan ALL categories, read-only
npm run migrate:images:apply                                  # apply ALL categories
npm run migrate:house-assets:dry                              # = --category houses, dry
npm run migrate:house-assets:apply                            # = --category houses --apply
npm run migrate:images:dry -- --category events --event-id <uuid>
npm run migrate:images:apply -- --category events                  # phase 1: files + plan, NO DB writes
npm run migrate:images:relink -- --relink scripts/reports/image-relink-plan.json --base-url https://www.vsaatucsd.com   # phase 2 (after push + deploy); add --verify-only to check without writing
```

Flags (see the script header): `--apply` (files + plan, no DB writes), `--plan-out <file>`, `--relink <plan>`, `--base-url <origin>`, `--wait-seconds <n>`, `--verify-only`, `--overwrite` (re-download existing files), `--category <c>`, `--limit <n>`, `--event-id <uuid>`, `--house-event-id <uuid>`, `--force-apply`. Env (auto-loaded from `.env.local`): `REACT_APP_SUPABASE_URL` + `REACT_APP_SUPABASE_ANON_KEY` required for phase 1; `SUPABASE_SERVICE_ROLE_KEY` needed for `--relink` (bypasses RLS — Row Level Security, Postgres per-row access policies). **Verification** (`scripts/lib/imageRelink.ts`): an asset counts as served only on HTTP 200 + `image/*` content-type + exact byte length + SHA-256 — `vercel.json`'s SPA fallback returns 200 + `index.html` for missing paths, so status alone proves nothing. **Branch guard**: in CI, `--relink` refuses to run off `main` unless `--force-apply` (only `main`'s files are what production serves). A failed push or deploy leaves rows on their working Storage URLs.

### The two workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `.github/workflows/migrate-images.yml` | daily cron `0 8 * * *` (midnight PT) + manual dispatch | `npm run migrate:images:apply` across ALL categories, then commits/pushes `public/images/` with `[skip ci]` |
| `.github/workflows/migrate-event-images.yml` | manual dispatch (inputs: `category` events/house-events, `apply` default **false**, optional `event_id`/`house_event_id`, `limit` default 20) + `repository_dispatch` types `event-image-migration-requested` / `house-event-image-migration-requested` | targeted migration; repository_dispatch runs always apply with `--limit 1`; guard step fails apply-mode runs not on `main`; per-event concurrency group prevents duplicate runs |

Both need GitHub secrets `REACT_APP_SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`.

### End-to-end automatic flow (Phase 3, live per docs)

Admin uploads image → Supabase Storage + DB row updated → tracked trigger `request_event_image_migration` (`private.request_image_migration()`, migration `20261010120000`; reads the URL and `x-image-migration-secret` from Vault and posts via `pg_net`; replaces the old Dashboard webhook, which stored the secret in plain text) → Edge Function `trigger-event-image-migration` (validates secret, only dispatches when `image_url` is new AND a Supabase Storage URL) → `repository_dispatch` → `migrate-event-images.yml` applies for that one event → commit to `main` → Vercel redeploys → image served from `/images/events/<slug>_<date>.webp` (+ `_thumb.webp`). Full webhook/PAT setup steps: `docs/event-image-migration.md` §Phase 3.

**Standard operating procedure for a manual run:** dry run first (Actions → "Migrate event images to static assets" → `apply=false`), read the printed plan, then re-run with `apply=true` from `main`, wait for the Vercel deploy, verify `/events` serves `/images/events/...` URLs.

## 6. Operational scripts inventory (`scripts/`)

| Script | One-liner |
|---|---|
| `migrate-supabase-images-to-public.ts` | The image-migration engine (§5) |
| `cleanup-stale-photo-requests.mjs` | Deletes pending member-photo upload files in Storage older than 7 days with no active `member_photo_requests` row; dry-run by default, real deletion requires `CONFIRM_DELETE=true node scripts/cleanup-stale-photo-requests.mjs` |
| `verify-ace-import.mjs` | Offline smoke test mirroring the `src/lib/aceFamilyImport.ts` parser against a sample JSON — sanity-check ACE family import numbers without touching Supabase (`node scripts/verify-ace-import.mjs`) |
| `restore-house-events.sql` | Hand-run restoration SQL for House events reconstructed from `public/images/house-events/` filenames; PART A runnable after fixing `-- TODO: fix date` placeholders, PART B needs real `house_profile_id` UUIDs; inserts with `is_published = false` |
| `deploy.sh` | Legacy AWS EKS deploy script (`aws`/`kubectl`) — NOT the production path (§2); do not run |
| `verify-rls-security.mjs` | RLS security probe — interpretation guide lives in `vsa-diagnostics-and-measurement` |
| `graphify-run` | Wrapper to run Graphify queries — see `graphify` skill / `vsa-docs-and-writing` |

## 7. Analytics operations (one paragraph)

Two separate systems share the word "analytics": (1) public page-view tracking in the React app, gated by user consent (`src/context/AnalyticsConsentContext.tsx` + `src/components/common/RouteTracker.tsx`) and configured via `REACT_APP_GA4_MEASUREMENT_ID`; (2) the admin reporting page `/admin/analytics`, which calls the `analytics-proxy` Edge Function to pull GA4 report data server-side using Google OAuth refresh-token secrets (§4 table; setup and failure modes in `docs/admin-analytics-setup.md` — e.g. `invalid_grant` means mint a new refresh token). The measurement ID and the reporting credentials are independent: setting one never fixes the other. Env-var catalog: `vsa-config-and-flags`; consent-UX conventions: `vsa-design-system-reference`.

## 8. What lands where

| Artifact | Produced by | Lands | Committed to git? |
|---|---|---|---|
| `build/` | `npm run build` (locally, in CI, and by Vercel) | local dir / Vercel static deployment | No (gitignored build output) |
| `public/images/events/`, `/house-events/`, `/houses/`, etc. | image-migration pipeline (§5) | repo static asset tree, served by Vercel edge | **Yes — committed to `main` by workflow bots** |
| Production site | Vercel static build of `main` (§2) | vsaatucsd.com / *.vercel.app | n/a |
| `ghcr.io/hhavynn/vsa-website` Docker image | deploy.yml `build` job on `main` | GitHub Container Registry | n/a — built but consumed by nothing (§2) |
| Edge Function code | `supabase functions deploy <name>` | Supabase runtime | source in `supabase/functions/`, yes |
| Schema | manual per-file `apply_migration`, then an order-checked rename to the recorded version (SQL Editor only with a `migration repair` to record it) — never `supabase db push` (§3) | production Postgres | migrations in `supabase/migrations/`, yes |
| `graphify-out/` | Graphify indexing | `graph.json`, `graph.html`, `GRAPH_REPORT.md`, `manifest.json` **committed** (in a separate `chore: update graphify graph` commit); `graphify-out/cost.json` and `graphify-out/cache/` **gitignored, never commit** |

## Provenance and maintenance

Sources (all read 2026-07-06, branch `codex/reactbits-ui` @ `368fbf63`): `package.json`, `vercel.json`, `Dockerfile`, `nginx.conf`, `.github/workflows/{deploy,migrate-images,migrate-event-images}.yml`, `docs/DEPLOYMENT_GUIDE.md`, `docs/event-image-migration.md`, `docs/admin-analytics-setup.md`, `AGENTS.md` (lines 13, 162, 246), `scripts/{migrate-supabase-images-to-public.ts,cleanup-stale-photo-requests.mjs,verify-ace-import.mjs,restore-house-events.sql,deploy.sh}`, `supabase/functions/*/index.ts`, `supabase/migrations/20260704000000_ai_knowledge_v2_schema.sql`, `src/data/repos/aiKnowledge.ts`, `src/pages/Admin/Analytics.tsx`. Branch-protection check: `gh api repos/hhavynn/vsa-website/branches/main/protection` → 404 (2026-07-06). §3 migration path rewritten 2026-10-08 from a read-only query of prod `supabase_migrations.schema_migrations` (41 rows, listed by version and name) compared against `ls supabase/migrations`, plus commit `c1f81e2d` (PR #528), the `Applied to production` headers in `20260927214024`…`20260930053224`, and `supabase db push --help` / `supabase migration repair --help` (CLI 2.109.0).

Re-verify before trusting (things that drift):

```bash
grep -n '"migrate' package.json                          # npm entrypoints still match
ls supabase/functions                                    # still five functions
grep -rn "Deno.env.get" supabase/functions/ | grep -v SUPABASE_   # secret names per function
grep -n "use.*static-build\|distDir" vercel.json         # deploy mechanism unchanged
grep -n "VERCEL_TOKEN\|ghcr" .github/workflows/deploy.yml # CI deploy step + Docker job
gh api repos/hhavynn/vsa-website/branches/main/protection # branch protection still absent?
grep -n "skip ci" .github/workflows/migrate-*.yml        # bot commits still skip Actions
ls supabase/migrations | tail -5                         # newest migrations
# read-only: is prod history still drifted? (41 rows vs 122 files on 2026-10-08)
#   select count(*) from supabase_migrations.schema_migrations;   -- via MCP execute_sql
ls supabase/migrations/*.sql | wc -l
```

Open item for a maintainer (UNVERIFIED, §2.3): confirm in the Vercel dashboard whether the GitHub git integration deploys `main` to production, and whether the `VERCEL_TOKEN` GitHub secret is set. Update §2 with the answer.
