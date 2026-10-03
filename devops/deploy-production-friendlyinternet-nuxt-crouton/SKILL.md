---
name: deploy-production
layer: stack
description: Deploy a crouton app to Cloudflare Workers PRODUCTION (<app>.friendlyinter.net). A deliberate, human-initiated action — separate from the default staging /deploy skill. Use ONLY when explicitly asked to ship/release to production. Never run as part of routine work or an automated flow.
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

# Deploy to Production — Cloudflare Workers (deliberate)

The **only** place a crouton app ships to **production**. Everything routine goes to
**staging** via the **`/deploy`** skill; production is split out here so it can never
happen by accident or as a side effect of an agent flow.

> **🛑 Gate — run this skill ONLY on an explicit human request to deploy to production**
> ("ship X to prod", "release to production", "promote to prod"). If the ask is just
> "deploy", that means **staging** → use `/deploy`. Before running anything, confirm:
> (1) which app, and (2) that production is genuinely intended. When in doubt, ask.

## Target

| Env | wrangler env | Worker | Domain | Script |
|-----|--------------|--------|--------|--------|
| **production** | top-level | `<app>` | `<app>.friendlyinter.net` | `cf:deploy` |

(Staging — `env.staging` / `<app>.pmcp.dev` / `cf:staging` — is **not** here; that's `/deploy`.)

## Pre-flight (confirm before deploying)

1. **The change is already on staging and verified there.** Deploy to production only
   what staging has proven — never straight to prod. **CI enforces this** (#1107, the
   Rung 3 confidence gate): the production dispatch first smokes the app's live staging
   URL and **refuses to deploy while it's red**. Staging red → fix staging (merge to
   `main` redeploys it), see the smoke go green, re-dispatch. Genuine emergency with
   staging itself down → re-dispatch with `skip_staging_smoke=true` (loud warning on
   the run; never routine). The gate applies to the CI path — a local `cf:deploy`
   bypasses it, so hold yourself to the same bar there.
2. **App is Workers-ready** — same checks as `/deploy` Step 2 (the shared mechanics live
   in that skill; don't duplicate them).
3. **Production Worker secrets are set** — `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL` = the
   **production** domain (`https://<app>.friendlyinter.net`), `NUXT_*`. Worker secrets
   persist across deploys, so this is a one-time bootstrap per worker:
   `npx wrangler secret bulk secrets.json` (no `--env` = production).
4. **Credentials** — `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN` present (see `/deploy` → Credentials).

## Deploy (both paths are explicit, human-initiated)

- **CI (preferred, canonical):** GitHub → the app's deploy workflow → **Run workflow**
  (`workflow_dispatch`) with **`environment = production`**. Push/PR never deploys prod —
  only this manual dispatch does.
- **Local:** from the app dir:
  ```bash
  cd apps/{app}
  pnpm cf:deploy   # build → wrangler deploy (auto-provision) → sync:ids → d1 migrations apply --remote
  # first bootstrap only — commit the written-back ids:
  git add apps/{app}/wrangler.jsonc && git commit -m "chore({app}): commit provisioned prod D1/KV ids"
  ```

> **Sandbox / no Cloudflare egress:** you CANNOT run a production deploy. Prepare and verify
> the config, then hand the `workflow_dispatch` (or `cf:deploy`) to the user to run, and
> confirm the result with them.

## After

- Verify `<app>.friendlyinter.net` is live and the remote migration applied.
- Production is **never demo-seeded** — the seed's known admin (`--with-staff`) is a
  staging/local-only login and must never run against the prod DB.

## Shared mechanics

Pipeline scripts, auto-provisioning, Pages→Workers migration, credentials, and
troubleshooting are documented once in the **`/deploy`** skill. This skill only adds the
**production trigger** and its **human gate**.
