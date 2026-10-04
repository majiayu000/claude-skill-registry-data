---
name: wp-deploy
description: Deploy the skyyrose-flagship-2 WordPress theme ("SkyyRose Flagship 2") to staging (scripts/deploy-staging.sh) or skyyrose.co (scripts/deploy-production.sh) through the gated engine (scripts/deploy-theme.sh, never run directly). Use when a theme change is built, verified, and ready to ship, or when previewing a deploy with --dry-run. Do NOT use for editing theme code, running verify during development, MU-plugin deploys (scripts/deploy-mu-plugin.sh), WooCommerce data writes, the V1 theme wordpress-theme/skyyrose-flagship (not a deploy target), or the Vercel dashboard — those have their own paths.
disable-model-invocation: true
---

# WordPress Theme Deploy

Deploy `wordpress-theme/skyyrose-flagship-2/` ("SkyyRose Flagship 2", text domain
`skyyrose-flagship-2`, `SKYYROSE2_VERSION`) to staging or the live SkyyRose site. The V1 theme
`wordpress-theme/skyyrose-flagship/` ("SkyyRose", `skyyrose`, `SKYYROSE_VERSION`) is NOT a deploy
target — `[live 2026-09-18]` skyyrose.co already serves the Flagship 2 lineage (v2.3.1, inside folder
`skyyrose-flagship`) and staging `staging-7e48-skyyrose.wpcomstaging.com` serves folder
`skyyrose-flagship-2` v2.4.4; deploying V1 would roll production back. Two wrappers, one engine:

- `bash scripts/deploy-staging.sh [--dry-run]` — env `.env.wordpress.staging`, staging host.
- `bash scripts/deploy-production.sh [--dry-run]` — env `.env.wordpress`, skyyrose.co; refuses until
  `.env.wordpress` `WP_THEME_PATH` points at the `-2` folder.
- `scripts/deploy-theme.sh` is the engine and refuses direct runs. Its preflight `check_theme_identity`
  refuses when the live theme's Name/Text Domain differs from the source. The engine does not yet
  support deploying `skyyrose-flagship-2` (PR #918's V2 deploy changes are a follow-up).
- Cutover = deploy + `wp theme activate skyyrose-flagship-2`, each its own STOP-AND-SHOW; after cutover
  production runs folder `skyyrose-flagship-2`.

The theme deploy is an
**atomic hot-swap**: production ends up with exactly what the source tree contains — anything the
source lacks gets DELETED live (bug-252: v1.10.3 shipped without its tracked signature emblem →
live 404).

## When to use

- A theme change is complete: built, lint-clean, `npm run verify` green (run in `wordpress-theme/skyyrose-flagship-2`; `verify:theme` is the V1 gate), and the founder wants it live.
- You need a deploy preview (`--dry-run`) to see the exact file manifest before asking for approval.
- Post-deploy verification of a deploy that just ran.

**When NOT to use:**

- Mid-development checks — run `npm run verify` / `npm run check:assets` in the theme folder directly, no deploy involved.
- MU-plugins — `STOPSHOW_ACK=1 bash scripts/deploy-mu-plugin.sh` is a separate, separately-gated path.
- WooCommerce REST writes, WP Media uploads, cache purges — production-touching but not theme deploys.
- Any worktree with a sparse checkout — a sparse tree is NEVER a valid deploy source (see Inputs).

## Inputs

Every item must exist before proceeding. **Absent input = STOP — never proceed with a substitute.**

1. **`.env.wordpress` (production) / `.env.wordpress.staging` (staging) at the repo root** — SFTP
   credentials (key `~/.ssh/skyyrose-deploy`, host `sftp.wp.com`); the wrapper picks the file. Observed
   2026-07-28: these files are ABSENT in worktrees `[repro]` — deploys run from the main checkout
   `/Users/theceo/DevSkyy`, not from worktrees. Absent → stop and switch to the main checkout; do not
   reconstruct credentials. `WP_THEME_PATH` in the chosen env file must end in `skyyrose-flagship-2`.
   `SSH_USER` must equal `<first label of the PUBLIC_URL host>.wordpress.com` (`SFTP_USER`, if set, must
   equal `SSH_USER`), and the engine's preflight requires `SFTP_HOST`/`SFTP_USER`/`SFTP_PASS` — the local
   `.env.wordpress.staging` lacks them `[repro 2026-09-19]`; template: `.env.wordpress.staging.example`.
2. **A COMPLETE source tree.** `preflight_completeness()` (`scripts/deploy-theme.sh`) verifies the
   version triple agrees and every **git-tracked** file exists on disk `[repo]`; `check_theme_identity`
   refuses a source whose Name/Text Domain differs from the live theme.
3. **Fresh `.min` build** — production serves `.min`; a source-only edit ships nothing.
   `cd wordpress-theme/skyyrose-flagship-2 && npm run build` before any deploy that touched CSS/JS;
   `npm run check:assets` must pass (byte-identical `.min`).
4. **Version triple bumped** when CSS/JS changed — `SKYYROSE2_VERSION` in `functions.php:10`,
   `style.css` `Version:`, `readme.txt` `Stable tag:`. It prefixes every asset `?ver=`; skipping it
   serves stale assets to returning visitors.
5. **Explicit founder approval.** This is STOP-AND-SHOW. The PreToolUse hook
   `.claude/hooks/paid-api-stopgate.sh` blocks the command — observed 2026-07-28, it blocks even
   `--dry-run` `[repro]` — until the manifest is shown, the founder answers `y`, and the call is
   re-issued with `STOPSHOW_ACK=1`.

## Procedure

1. Build minified assets: `cd wordpress-theme/skyyrose-flagship-2 && npm run build`.
2. Run the local gate: `npm run verify` + `npm run check:assets` — green (see Verification).
3. Diff what will ship: `git diff --name-only HEAD~5 -- wordpress-theme/skyyrose-flagship-2/` and
   sanity-check the version triple agrees across `functions.php` / `style.css` / `readme.txt`.
4. Preview: `bash scripts/deploy-staging.sh --dry-run` (a STOP-AND-SHOW surface itself — show
   manifest, get `y`, re-issue with `STOPSHOW_ACK=1`). Staging first, always.
5. Print the STOP-AND-SHOW manifest (target host, theme folder, file count, version before→after) and
   wait for `y` — one manifest, one `y`, one call; staging approval never carries to production.
6. Deploy — **BLOCKED until PR #918 lands: both wrappers refuse a `skyyrose-flagship-2` source, `--dry-run` included** (steps 4–6 are the contract, not a runnable path today). One-shot flags `--allow-new-theme-folder` (first deploy into a folder the site lacks) and `--allow-theme-identity-change` (replace a live theme whose Name/Text Domain differ) replace exporting `ALLOW_NEW_THEME_FOLDER` / `ALLOW_THEME_IDENTITY_CHANGE` — the wrappers refuse those if inherited. Then: `STOPSHOW_ACK=1 bash scripts/deploy-staging.sh`, verify staging, then
   `bash scripts/deploy-production.sh --dry-run` → new manifest → `y` →
   `STOPSHOW_ACK=1 bash scripts/deploy-production.sh`. Cutover activation
   (`wp theme activate skyyrose-flagship-2`) is a separate STOP-AND-SHOW.
7. Post-deploy verification (below), then Playwright eyes-on mobile + desktop.
8. **Fix everything in one batch, test all pages, deploy ONCE** — no drip-deploys.

## Verification

Every check can return "no". A gate that dies mid-run is not a gate that passed — if
`npm run verify` or the deploy script errors out, its silence is an artifact, re-run it (bug-230).
Browser/vision checks (CWV, responsive, a11y, product-fidelity) are not part of the CLI gate — the
deploying agent closes them with Playwright/vision after the deploy.

```bash
cd wordpress-theme/skyyrose-flagship-2 && npm run build && npm run verify && npm run check:assets
```
**PASS:** exit 0 on each — `verify` = php -l sweep + `jq` on `data/*.json` + font-provenance hashes;
`check:assets` = every shipped `.min` byte-identical to a fresh build. `[test]`

```bash
HOST=https://staging-7e48-skyyrose.wpcomstaging.com   # or https://skyyrose.co after the production step
curl -s -o /dev/null -w 'code=%{http_code} size=%{size_download}B\n' "$HOST/?cb=$(date +%s)"
```
**PASS:** `code=200` and size ≥ 50000B, no PHP-error markers in body. `[live]` Cache-bust is
mandatory — Batcache serves stale. NEVER WebFetch live HTML (strips `<script>`).

```bash
curl -s "$HOST/wp-content/themes/skyyrose-flagship-2/style.css?cb=$(date +%s)" | grep -m1 -E '^(Theme Name|Version|Text Domain):'
```
**PASS:** `Theme Name: SkyyRose Flagship 2`, `Text Domain: skyyrose-flagship-2`, and `Version:` equals
the `SKYYROSE2_VERSION` you just shipped. Observed 2026-09-18 `[live]`: staging folder
`skyyrose-flagship-2` → 2.4.4; production still serves the lineage from folder `skyyrose-flagship`
(2.3.1) until cutover, so before cutover probe that folder name on skyyrose.co instead. A mismatch =
the swap did not land or the edge cache is stale.

Prove the gate can fail (rule 3): once per new environment, delete one tracked theme file in a
scratch copy and run `preflight_completeness()` against it — it must go red — then restore.

## Worked example

Real invocation from this worktree, 2026-07-28:

```bash
cd /Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon/wordpress-theme
npm run verify:list
```

Observed output (excerpt) `[repro]`:

```
  php-syntax        CLI      php -l on every delivered .php — zero parse errors
  phpstan           CLI      static analysis at the configured level
  min-sync          CLI      every source css/js has a .min sibling, none stale
  cwv               BROWSER  Lighthouse LCP/CLS/TBT — runs only with --url + lighthouse CLI
  product-fidelity  VISION   garment ↔ SKU pixel match — caller/agent reads pixels vs catalog
```

Then attempting the deploy preview from this same worktree (2026-07-28, before the wrappers existed —
today the engine refuses this direct call; use `bash scripts/deploy-staging.sh --dry-run`):

```bash
bash scripts/deploy-theme.sh --dry-run
```

Observed: **blocked before execution** by `.claude/hooks/paid-api-stopgate.sh` —
`"BLOCKED — STOP-AND-SHOW required per DevSkyy CLAUDE.md … Category: WordPress deploy to
skyyrose.co (production)"` `[repro]`. That is the contract working: no deploy command runs, even
dry, without a shown manifest, a founder `y`, and `STOPSHOW_ACK=1` on the re-issued call. (This
worktree also lacks `.env.wordpress`, so the deploy itself must run from `/Users/theceo/DevSkyy`.)

## Failure modes

- **Missing rider deleted live (bug-252).** The hot-swap deletes anything the source lacks.
  `preflight_completeness()` covers git-tracked files only; untracked riders (currently the 3
  `*-v2-avatar.webp` scene files, `.gitignore:290`) pass silently. `git add -f` a rider to put it
  under the gate.
- **Fail-open override (bug-230 pattern).** `PREFLIGHT_SKIP_COMPLETENESS=1` skips the completeness
  gate with only a loud log line. Never set it to make a red gate green — an emergency override on
  an unverified tree is how riders die.
- **Version-triple drift.** Stale `?ver=` keeps the WP.com edge serving old CSS/JS after a
  successful deploy — the site "deployed fine" but returning visitors see the old design. Bump all
  three files together.
- **Scope-jump reporting (bug-287).** A clean repo tree is `[repo]` evidence only — never report
  "deployed and live" without the post-deploy `curl` + Playwright probes (`[live]`).
- **Large scene assets timing out mid-transfer** — upload separately; a partial transfer plus
  hot-swap is worse than no deploy.
- **Wrong theme.** The repo's V1 folder carries different theme headers than production;
  `check_theme_identity` refuses it. Never work around that refusal — a V1 deploy is a rollback of
  the live Flagship 2 lineage, not a fix.
- **Rollback:** `git checkout <last-good-sha> -- wordpress-theme/skyyrose-flagship-2/`, rebuild, and
  redeploy through the same wrapper (the rollback deploy is STOP-AND-SHOW too).
