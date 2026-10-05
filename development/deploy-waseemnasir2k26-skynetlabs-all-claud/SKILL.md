---
name: deploy
version: 1.0.0
description: |
  Multi-target deploy router for SkynetLabs with deploy gotchas baked in as hard
  rules. Detect the deploy target from the repo, route to the correct procedure,
  and BLOCK the wrong path before it ships.

  Targets in active use:
    - Vercel — React/Next sites (your-site-react, your-app) via `vercel` CLI / git push
    - Hostinger manual ZIP — example.com (Next.js standalone on Hostinger Node app).
      HARD RULE: deploys via manual ZIP archive upload, NOT GitHub auto-deploy,
      NOT Vercel. Warn + refuse if anyone routes it to GitHub push or Vercel.
    - WordPress theme/plugin — ZIP upload or Hostinger MCP deployWordpressTheme/Plugin
    - Static site — plain HTML/CSS via Hostinger MCP deployStaticWebsite

  Runs a pre-deploy gate (build passes, no exposed secrets, security review,
  git committed), executes the routed procedure, then verifies the URL is live
  and records the rollback path.

  Trigger when user says: "deploy", "ship to prod", "push live", "/deploy",
  "deploy my site", "deploy to vercel/hostinger", "upload the theme",
  "publish the site", or asks how to get a build live.
license: MIT
compatibility: claude-code
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# deploy

Route a repo to the RIGHT deploy target and enforce the gotcha so the wrong path
never ships. This skill is opinionated on purpose — it's easy to lose time deploying
a Hostinger Node app to the wrong target. The detection + hard rules below exist to stop that.

## When to use

USE when the user wants to get a build live (any of: Vercel, Hostinger ZIP, WordPress
theme/plugin, static site) and isn't sure of the procedure, OR when the target carries
a gotcha (a Hostinger Node app like example.com).

For the full versioned release flow (merge main → tests → VERSION bump → CHANGELOG →
PR), run `/ship` FIRST, then `/deploy` the resulting build. `/deploy` is about the
last mile (build → host), `/ship` is about the git release.

## Step 0 — Detect the target (run this first, always)

```bash
cd <repo>                          # absolute repo path, e.g. ~/GITHUB/your-site-react
git rev-parse --show-toplevel      # confirm it's a repo
git remote -v                      # capture origin (used for the Hostinger-app identity check)
ls                                 # top-level inventory
```

Detection order (FIRST match wins — the Hostinger-app override beats generic Vercel):

| Signal (check in this order)                                                                                         | Target                                        |
| -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| Repo is the **Hostinger Node app** (dir name, origin URL, or `package.json` name matches your Hostinger-hosted site) | **Hostinger manual ZIP** (HARD RULE — see §A) |
| `style.css` with a `Theme Name:` header, OR a `<plugin>.php` with `Plugin Name:` header                              | **WordPress theme/plugin** (§C)               |
| `next.config.{js,mjs,ts}` OR `vercel.json` OR `.vercel/` present                                                     | **Vercel** (§B)                               |
| `index.html` at root, no build step, no framework config                                                             | **Static site** (§D)                          |
| Ambiguous / multiple matches                                                                                         | STOP, ask via AskUserQuestion                 |

```bash
# Hostinger-app identity (override gate)
git remote -v | grep -i your-site ; grep -i '"name"' package.json 2>/dev/null
# WP theme/plugin headers
grep -RIl -m1 -E "Theme Name:|Plugin Name:" --include=style.css --include=*.php . 2>/dev/null | head
# Vercel / Next
ls next.config.* vercel.json .vercel 2>/dev/null
```

State the detected target and the reason out loud BEFORE deploying. If it's the Hostinger Node app,
say so explicitly and confirm Hostinger ZIP (not Vercel, not GitHub auto-deploy).

## Pre-deploy gate (ALL targets — run before any upload)

Do NOT proceed past a failing gate without explicit user override.

1. **Git committed.** `git status` clean (or user explicitly says deploy WIP). Uncommitted
   prod deploys are unreproducible — you can't roll back to a commit that doesn't exist.
2. **Build passes locally.** Run the real build, don't assume:
   - Next/React: `npm ci && npm run build` (Vercel/Hostinger). Build red = STOP.
   - WP/static: N/A (no build) — instead lint the files load.
3. **No exposed secrets in the artifact.** This is the #1 ZIP gotcha.
   ```bash
   git ls-files | grep -E '(^|/)\.env' ; ls -a | grep -E '\.env'
   grep -RIl -E "API_TOKEN|SECRET|PRIVATE_KEY|sk-[A-Za-z0-9]|AKIA[0-9A-Z]{16}" . \
     --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.next 2>/dev/null | head
   ```
   `.env*` MUST NOT be in the ZIP/commit. If `git archive` is the packer it respects
   `.gitignore` (good). For manual ZIPs, exclude `.env`, `.git`, `node_modules`, `.next`.
4. **Run a security review.** For any code-bearing deploy, prompt: "Run a security review
   before this goes live?" — offer `/security-review` (or `/review`). Mandatory pre-delivery
   gate per SkynetLabs policy. Skippable only for static-HTML-only changes.
5. **Version + changelog.** Confirm VERSION bumped + CHANGELOG entry exists (this is
   `/ship`'s job — if not shipped yet, suggest `/ship` first). Tag the deploy with the
   commit SHA so rollback is `git`-addressable.

---

## §A — Hostinger manual ZIP (example.com Node app) — HARD RULE

> example.com = Next.js (`output: standalone`, node 20) on **Hostinger Node.js Web App**,
> account `<HOSTINGER_ACCOUNT_ID>`. Confirmed via live headers: `X-Powered-By: Next.js`, `Server: hcdn`
> (Hostinger CDN). **NOT Vercel.**
>
> **Deploy = manual ZIP archive upload via Hostinger MCP `hosting_deployJsApplication`.
> NOT GitHub auto-deploy.** The repo's `DEPLOY_HOSTINGER.md` claims GitHub auto-deploy is
> wired — it is FALSE / never connected. Pushing to GitHub `main` deploys NOTHING.
>
> If the user/agent tries `vercel deploy`, "just push to GitHub", or wires GitHub
> auto-deploy for this app → STOP and warn. Wrong target. Use the ZIP path below.

**Deploy path (verified live):**

```bash
cd <node-app repo>
# 1. Archive SOURCE ONLY (no node_modules/.next/.git — server runs the build).
#    git archive respects .gitignore and excludes .git automatically.
git archive --format=zip -o site-deploy.zip HEAD
```

2. Deploy via Hostinger MCP tool **`hosting_deployJsApplication`** (this skill's allowed-tools
   don't include MCP — load it via ToolSearch `select:mcp__hostinger-mcp__hosting_deployJsApplication`
   then call it):
   ```json
   {
     "domain": "example.com",
     "archivePath": "<ABSOLUTE path to site-deploy.zip>"
   }
   ```
3. Server runs `npm install && npm run build` (build_script `build`, output `.next`). ~2 min.
4. Track / debug:
   - `hosting_listJsDeployments` — deploy status
   - `hosting_showJsDeploymentLogs` — needs the build uuid from the deploy/list response

**Env gotcha:** `NEXT_PUBLIC_SITE_URL` MUST be `https://example.com` in the Hostinger
panel — it drives canonicals/OG via `SITE.url` → `metadataBase`. A leftover example
(`your-personal-site.com`) is wrong and points canonicals at the wrong domain.

**MCP-dropped fallback** (Hostinger MCP is a stdio server `npx hostinger-api-mcp@latest`,
config `~/.mcp.json`, env `API_TOKEN`). If it disconnects mid-session and `/mcp` reconnect
isn't available, drive it directly with the repo's one-shot client:

```bash
# from the node-app repo (uses the exact tested TUS-upload code path)
API_TOKEN=<tok> node scripts/mcp-deploy.mjs hosting_deployJsApplication \
  '{"domain":"example.com","archivePath":"<ABS zip path>"}'
```

Or spawn the cached package main `node <npx-cache>/hostinger-api-mcp/src/servers/all.js`
with `API_TOKEN` and speak newline-delimited JSON-RPC over stdio
(initialize → notifications/initialized → tools/call).

**Rollback:** re-archive an OLDER commit and redeploy.

```bash
git archive --format=zip -o site-rollback.zip <good-sha>   # then hosting_deployJsApplication
```

Track your own known-good SHAs (last good before a risky ship, a stable pre-redesign
baseline, and the SHA currently live) so rollback is a single re-archive + redeploy.

---

## §B — Vercel (React/Next: your-site-react, your-app, generic)

> Only for repos that are NOT the Hostinger Node app. example.com is Hostinger (§A).

Two valid paths — prefer git-integration if the project is linked, else CLI.

**Path 1 — git integration (preferred for linked projects):**
Vercel auto-builds on push to the production branch. After `/ship` merges to `main`:

```bash
git push origin main          # triggers Vercel production build
```

Then verify the deployment in the Vercel dashboard / via `vercel ls`.

**Path 2 — CLI (unlinked, or force a manual prod deploy):**

```bash
cd <repo>
npm ci && npm run build        # gate: build must pass
npx vercel pull --yes          # sync env + project settings
npx vercel build --prod
npx vercel deploy --prebuilt --prod   # prints the production URL
```

**Env:** set via `npx vercel env add <NAME> production` or the dashboard. Never commit `.env`.
Confirm prod env vars exist BEFORE deploy (missing env = runtime 500, not a build fail).

**Rollback:** `npx vercel rollback <previous-deployment-url>` (instant), or re-deploy a
prior commit. Vercel keeps every deploy immutable — rollback is the safest of all targets.

---

## §C — WordPress theme / plugin

> Detected via `Theme Name:` in `style.css` (theme) or `Plugin Name:` header in a `.php`
> (plugin). E.g. a travel client's login styler plugin.

**Package the ZIP** (the theme/plugin folder must be the single top-level dir inside the ZIP):

```bash
cd <parent of theme/plugin folder>
# exclude dev cruft + secrets
zip -r my-theme.zip my-theme -x "*/.git/*" "*/node_modules/*" "*/.env" "*.map"
```

**Deploy — two routes:**

- **Hostinger MCP (preferred when site is on Hostinger):**
  - Theme: `hosting_deployWordpressTheme`
  - Plugin: `hosting_deployWordpressPlugin`
  - (Load via ToolSearch `select:mcp__hostinger-mcp__hosting_deployWordpressTheme` /
    `...deployWordpressPlugin`.) Pass the domain + absolute ZIP path.
- **Manual:** WP Admin → Appearance → Themes → Add New → Upload (or Plugins → Add New →
  Upload) → Activate. Or SFTP the unzipped folder into `wp-content/themes|plugins/`.

**WP gotchas:**

- Bump the version header in `style.css` / plugin main file — WP caches by version; an
  unchanged version may not refresh.
- Coexistence rules apply for login/register styling (see `loginpress-coexistence` memory):
  style via CSS, translate via gettext, never DOM-surgery the register form.
- Test on STAGING first for auth/register flows before prod.

**Rollback:** keep the prior ZIP. Re-upload + reactivate, or restore the folder via SFTP.
For Hostinger-managed sites, a hosting snapshot/backup restore is the nuclear option.

---

## §D — Static site (plain HTML/CSS/JS, no build)

**Deploy via Hostinger MCP `hosting_deployStaticWebsite`** (load via ToolSearch
`select:mcp__hostinger-mcp__hosting_deployStaticWebsite`): pass the domain + the
source directory / ZIP per the tool schema.

Gate: confirm `index.html` exists at the served root and no `.env`/secret files are in
the upload set. Static is the lowest-risk target — no build, no server runtime.

**Rollback:** redeploy the previous folder/ZIP, or Hostinger hosting snapshot restore.

---

## Post-deploy verification (ALL targets)

Never call a deploy done until the live URL is confirmed serving the new build.

```bash
curl -I https://<domain>          # 200 OK; for the Hostinger Node app expect X-Powered-By: Next.js + Server: hcdn
```

- For interactive / visual verification, run `/browse` or `/qa` against the live URL —
  load the page, confirm the changed content renders, check console for errors.
- Diff a known-changed element (a new section, version string, copy change) to prove the
  NEW build is live and not a CDN-cached old one. If stale, purge cache / re-verify.
- **Record the rollback path** for THIS deploy in your final report: the prior known-good
  commit SHA (Vercel/Hostinger ZIP) or prior ZIP artifact (WP/static), and the exact
  command to revert.

## Hard rules (do not violate)

- ❌ NEVER deploy the example.com Node app to Vercel. It's Hostinger. (§A)
- ❌ NEVER rely on GitHub auto-deploy for the example.com Node app — it is not wired; push deploys nothing.
- ❌ NEVER ship a ZIP/commit containing `.env` or secrets. Gate step 3 blocks this.
- ❌ NEVER skip the build-passes check by assuming. Run `npm run build`.
- ❌ NEVER call a deploy complete without curling/visiting the live URL.
- ✅ ALWAYS detect target FIRST and state it + the reason before uploading.
- ✅ ALWAYS run/offer a security review for code-bearing deploys.
- ✅ ALWAYS record the rollback path in the final report.

## Failure modes + fixes

| Failure                                   | Cause                                       | Fix                                                 |
| ----------------------------------------- | ------------------------------------------- | --------------------------------------------------- |
| Node-app push deploys nothing             | GitHub auto-deploy not wired (it never was) | Use §A manual ZIP via `hosting_deployJsApplication` |
| Node-app canonicals point to wrong domain | `NEXT_PUBLIC_SITE_URL` wrong in panel       | Set `https://example.com` in Hostinger env          |
| Hostinger MCP disconnects mid-deploy      | stdio server dropped                        | Use `scripts/mcp-deploy.mjs` fallback (§A)          |
| Vercel runtime 500 after deploy           | missing prod env var                        | `vercel env add <NAME> production`, redeploy        |
| Live URL shows old build                  | CDN cache                                   | purge cache, re-curl, diff a changed element        |
| WP theme update not reflected             | version header unchanged (WP cache)         | bump version in style.css / plugin header           |
| Secret leaked in ZIP                      | manual zip included `.env`                  | repack excluding `.env`/`.git`; rotate the secret   |
