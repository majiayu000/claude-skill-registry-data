---
name: poc-deploy
layer: stack
description: Give a pocs/ app a Cloudflare Workers preview deploy so a PR returns a testable staging URL (auth-working). Use when wiring a POC for previews, or when "build X as a poc" needs to end at a clickable link. For launched apps/ apps use the /deploy skill instead.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# POC preview deploy

Makes the **endpoint of a POC a live, testable Cloudflare Workers preview URL** — the goal of epic #265. A POC lives in `pocs/<name>` (safe-to-break incubator; see root `CLAUDE.md`). This skill gives it a deploy workflow so **every PR that touches the POC deploys an isolated, auto-provisioned staging env and posts the preview URL on the PR**.

For **launched `apps/` apps** (production counterpart, two-domain deploy) use the **`/deploy`** skill instead — this one is the lighter, staging-only POC path.

## How it works

```
PR touches pocs/<name>/** (POC has a deploy.config.json)  →  deploy-pocs.yml (generic; detects
   the changed/dispatched opted-in POCs)  →  deploy-app.yml (reusable, workspace: pocs, enable-review: true)
   →  build (cloudflare_module, NUXT_PUBLIC_CROUTON_REVIEW=true) → wrangler deploy --env staging
   →  auto-provision id-less D1/KV → sync review bridge secrets → sync ids → remote D1 migrate
   →  sticky PR comment: 🚀 <name> staging deployed: <url> + overlay usage instructions
```

> **Review overlay is ON by default for all POC staging deploys (#596).** `deploy-pocs.yml` passes
> `enable-review: true` to `deploy-app.yml`, so every POC preview is built with
> `NUXT_PUBLIC_CROUTON_REVIEW=true` (the `@fyit/crouton-devtools` overlay + source stamper + `/api/_feedback`
> bridge). The PR comment includes overlay usage instructions. For the bridge to post `🎯 Preview feedback`
> comments, set the `NUXT_CROUTON_REVIEW_GITHUB_APP_*` repo-level secrets (see
> `writeups/setup/review-bridge-token-setup.md`); the overlay still renders without them.

> **One generic workflow, no per-POC file (#481).** There is a single committed
> `.github/workflows/deploy-pocs.yml`; a POC opts in with `pocs/<name>/deploy.config.json`
> (which the agent pipeline **can** push — it's under `pocs/`, not `.github/workflows/`, which
> needs the `workflows` scope the bot lacks). Do **not** generate a per-POC `deploy-<name>.yml`.

- The reusable `deploy-app.yml` takes a **`workspace`** input (`apps` default, or `pocs`) — that's the only thing that lets a `pocs/` app reuse the same pipeline as `apps/`.
- The preview is stable at **`https://<name>.pmcp.dev`** (the #133 staging domain), so `BETTER_AUTH_URL` is predictable and **auth works on the preview**.

## Wire a POC for previews

1. **Scaffold the POC first** (it must exist at `pocs/<name>` with a `wrangler.jsonc` that has an `env.staging` block: id-less `<name>-staging-db` + route `<name>.pmcp.dev`, and `cf:staging` in its `package.json` — the app scaffold produces these, mirroring `apps/velo`).
   > **Add `cf:version` alongside `cf:staging`** (#1836). The `mode: version` dispatch — immutable side-by-side previews — runs the POC's own `cf:version`, and **nothing generates it**: a POC wired for deploy but missing it fails the dispatch. Copy the POC's own `cf:staging` and swap `wrangler deploy` for `wrangler versions upload`, dropping the id-sync and migrate steps (a version upload activates nothing, so there's no DB to migrate). Mirror *that* POC's script, not a template — `loop-station`, for one, prepares data first and skips `inject-wrangler-env`. `deploy-pocs.yml` now fails fast and tells you if it's missing.
2. **Generate + commit the initial D1 migrations.** Collections are **not** migrated by `crouton config`/`crouton init`, so a fresh POC has none — and the deploy's remote-migrate step then fails with *"No migrations present"*. Use the **`db-migrations`** build-first workaround: `NITRO_PRESET=node-server nuxt build` until `.nuxt/hub/db/schema.mjs` appears → `pnpm db:generate` → **commit** `pocs/<name>/server/db/migrations/sqlite/**`. (Don't skip this — it's the step that bit library-catalog, #457.)
3. **Opt the POC in — config only, NO workflow file:**
   ```bash
   pnpm poc:scaffold-deploy <name>      # → pocs/<name>/deploy.config.json  (NOT a workflow file)
   ```
   It writes `pocs/<name>/deploy.config.json` (`{ stagingUrl, layerPackages }`), read by the shared `deploy-pocs.yml`.
4. **Open a PR touching `pocs/<name>/**`** (e.g. the `deploy.config.json` + migrations). `deploy-pocs.yml` — which must be on the PR's **base** branch (an epic branch must carry it; see #481) — auto-fires → CI deploys the staging Worker and posts the preview URL. First deploy auto-provisions D1/KV. (`workflow_dispatch(app=<name>)` also works if the token has `actions` scope.)

## Auth on a fresh preview (so it's testable)

A freshly deployed Worker has no users. To make the preview testable *with auth*, the POC's **`seed` script provisions a known admin** against the remote D1 (run it post-deploy, or have CI do it), and the admin creds are handed back alongside the URL. (Self-registration on the preview also works if the POC enables it.) See the per-app `seed`/`shots` scripts.

## Requirements / gotchas

- **CI-only:** real Cloudflare deploys run in GitHub Actions — the `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN` repo secrets must exist (same as the `apps/` deploys), and the token needs account Workers/D1/KV **and** zone Workers-Routes/DNS edit for the `<name>.pmcp.dev` custom domain. There are no CF creds in the dev sandbox; you cannot produce the URL locally — open the PR and let CI do it, then babysit to green.
- **Staging only.** No production block — pocs are previews. Promote `pocs/<name>` → `apps/<name>` and use `/deploy` for production.
- **Worker secrets** (e.g. `BETTER_AUTH_SECRET`) persist across deploys; set them once via `WORKER_SECRETS_JSON` (an Environment secret) or `wrangler secret bulk --env staging`.
- The POC opts in via `pocs/<name>/deploy.config.json` (re-run `pnpm poc:scaffold-deploy <name>` to refresh it). The generic `deploy-pocs.yml` is **shared** — never add a per-POC workflow file. For a `pull_request` deploy to fire, that workflow must be present on the PR's **base** branch (cut/refresh epic branches from current `main` so they carry it — #500/WS3).
- **Migrations must be committed** (`pocs/<name>/server/db/migrations/sqlite/**`) before the deploy, or the remote-migrate step fails — see step 2.
