---
type: Skill
name: mcp-ai-wpoos-wporg-submission
description: "Operational guide for WordPress.org submission readiness of NV oOS standalone plugins (nvoos-docs-hub live; nvoos-design-system next in the pipeline — issue #6811). Covers the 18 wp.org guidelines, the Plugin Check (PCP) gate in CI and Docker, PCP finding triage, the reviewer-reply loop (findings taxonomy from the real 0.4.3 review, related-issue sweep checklist, reply-email template), packaging exclusion tri-sync, readme.txt standards, and .wordpress-org listing assets. Use when preparing a wp.org submission, responding to a reviewer email, fixing the plugin-check CI job, or triaging PCP findings."
license: Proprietary. See LICENSE.txt
metadata:
  plugin: mcp-ai-wpoos
  plugin-version: "1.1.71"
  plugin-version-tested: "1.1.71"
  last-updated: "2026-09-29"
---

# NV oOS WordPress.org Submission — Readiness Playbook

Playbook distilled from four executed passes: the Docs Hub 0.4.3
submission-readiness pass (PR #6403), the base-plugin gate repair, the first
real reviewer-reply pass (0.4.3 → 0.4.4, PR #6606 — all findings fixed plus
a related-issue sweep), the second reviewer-reply pass (0.4.4 → 0.4.5 —
remote-call service framing + the initial-dir symlink residual), and the
third reviewer-reply pass (0.4.6 → 0.4.7 — readme-only "Tested up to" +
cron-on-init fix). Covers everything between "this plugin should ship to
wp.org" and "the reviewer approves it".

## When to use this skill

- "Prepare <plugin> for wp.org submission" / "run the 18-point checklist"
- **A reviewer reply email arrives** (the submission is pended) — fix the
  findings and upload a new version (see "The reviewer reply pass" below)
- The `plugin-check` CI job fails (any workflow) or a release gate is red
- "Capture the wp.org listing screenshots" / "refresh the .wordpress-org assets"
- Triaging `wp plugin check` findings (ERROR vs WARNING, false positives)
- Adding/fixing the packaging exclusions for a standalone ZIP
- Reviewing readme.txt against wp.org standards

## The 18 official wp.org guidelines (with repo mapping)

The authoritative list is
https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/
(18 numbered points, last updated 2026-03-11). Some third-party "20-point"
checklists add security and listing-assets items — those live in separate
wp.org handbooks and are covered by this skill's other sections (PCP gate,
`.wordpress-org` assets). Work the 18 below top-down for any submission;
"where verified" tells you which artifact proves compliance for this repo.

| # | Guideline (condensed) | Where verified in this repo |
|---|---|---|
| 1 | GPL-compatible licensing (GPLv2+ recommended); all bundled code/data/images licensed compatibly | `License: GPLv3 or later` header, `LICENSE` copied into ZIPs by `release.yml`/`build-nvdigital-oos-wporg.yml`, PCP readme license check |
| 2 | Developer is responsible for all contents and actions; verify third-party licenses before SVN upload | `SUBMISSION.md` manifest; `wp-org-compliance-auditor` agent scope |
| 3 | A stable version must always be available from the directory page | SVN `trunk` + `tags/<ver>` discipline (`.wordpress-org/README.md` runbook) |
| 4 | Code must be (mostly) human readable — no obfuscation/packer/mangled names; ship source or link build tooling | Audit row R-Q-06 (every `.min.js` has a sibling source/map); PCP code-quality checks |
| 5 | No trialware — no locked/paywalled features inside the plugin | Pro features ship in the separate Pro addon; base ZIP has no locked functionality (`SUBMISSION.md`) |
| 6 | SaaS is permitted — the service must provide real functionality and be documented with ToS links | AI providers are services; `readme.txt == External Services ==` (ToS + privacy URLs per host); the docs-hub `OffloadedContent` PCP allowlist rationale |
| 7 | No tracking without explicit, informed consent; no phone-home; document data collection | All remote fetches are server-side and only after admin config (readme wording); auditor agent flags new `wp_remote_*` without disclosure |
| 8 | No executable code via third-party systems; no CDN-loaded JS/CSS (fonts excepted); no remote update/install | Auditor agent: "no remote JS/CSS" rule; `release.yml` `BASE_ONLY_EXCLUDES` strips the langchain/transformers/web-worker CDN enqueue files from the wp.org ZIP |
| 9 | Nothing illegal, dishonest, or morally offensive; no fake reviews/black-hat SEO | Manual audit scope (`wp-org-compliance-auditor`) |
| 10 | No embedded links/credits on public site without explicit opt-in; "Powered by" must default OFF | Auditor agent success criteria: no unsolicited attribution |
| 11 | No admin-dashboard hijacking — dismissible, contextual notices only; resolve-and-remove errors | Auditor agent success criteria; docs-hub settings page limits notices to its own page |
| 12 | Readmes must not spam — ≤ 5 tags, no keyword stuffing, no affiliate links, written for people | Docs-hub readme trimmed to 3 standard tags; PCP flags tag/keyword issues |
| 13 | Use WordPress' bundled libraries (jQuery, SimplePie, PHPMailer…) — don't ship your own copies | PCP `library_core_files` finding (present in the base-plugin report); bundle only non-WP deps in `vendor/` |
| 14 | Avoid frequent SVN commits; descriptive commit messages; releases only | Process note — commit per release, not per change (`.wordpress-org/README.md`) |
| 15 | Version must increment each release; trunk readme must reflect current version | Version-bump commits per release; PCP readme checks (`Stable tag` == header `Version`, `Tested up to` fresh) |
| 16 | A complete plugin must exist at submission — no slug reservations/placeholders | PCP `no_plugin_readme` ERROR (readme.txt must be at the ZIP root); no empty-dir submissions |
| 17 | Respect trademarks — no other product's term as the slug's initial term | PCP `trademarked_term` (base plugin: `wp-mcp-ai` contains "wp" → warning; the chosen slug `nvdigital-open-operator-system-oos` avoids it) |
| 18 | The directory team reserves maintenance rights (updates to rules, removals, exceptions) | Informational — factor review feedback loops into the submission timeline |

### Checklist source documents (read before executing)

- `SUBMISSION.md` (repo root) — base-plugin submission state + per-finding
  reviewer-reply table
- `.github/agents/wp-org-compliance-auditor.agent.md` — PR-level auditor
  (set_time_limit, attribution, do_shortcode wrap, CLI write paths, External
  Services disclosure, CDN ban)
- `docs/operations/compliance/WORDPRESS_ORG_SUBMISSION_CHECKLIST.md` —
  pre-submission requirements + SVN process (account → review → SVN)
- `docs/project/audits/2026-04/wp-org-submission-checklist.md` — executed
  audit with per-row status + IDs (R-D-01, R-Q-01…, R-S-01…, R-T-04…)

## Running the official Plugin Check locally (Docker)

The QA stack (`oos-wp`, http://localhost:8000) has `plugin-check` active, but
PCP's runtime checks crash on the heavy plugin stack. Use a **fresh WP install**
(one-off container on the `oos-wp_default` network, scratch DB in `oos-wp-db`):

```bash
# 1. Scratch DB + grants (the MYSQL_DATABASE env does this in CI; locally the
#    wordpress user needs explicit grants on any DB beyond `wordpress`).
docker exec oos-wp-db sh -c 'mysql -uroot -pwordpress -e "CREATE DATABASE IF NOT EXISTS wordpress_pluginchk CHARACTER SET utf8mb4; GRANT ALL PRIVILEGES ON wordpress_pluginchk.* TO '\''wordpress'\''@'\''%'\''; FLUSH PRIVILEGES;"'

# 2. One-off WP install + PCP run. Mount the plugin source and a scratch dir.
#    --user 33:33 matters when writing into the wp_core volume (uploads are
#    owned by uid 33; the cli image runs as uid 82).
MSYS_NO_PATHCONV=1 docker run --rm --user 33:33 --network oos-wp_default \
  -v oos-wp_wp_core:/var/www/html \
  -v F:/GITHUB/worktrees/mcp-ai-wpoos/<worktree>/mcp-ai-wpoos:/var/www/html/wp-content/plugins/mcp-ai-wpoos \
  -e WORDPRESS_DB_HOST=oos-wp-db -e WORDPRESS_DB_NAME=wordpress \
  -e WORDPRESS_DB_USER=wordpress -e WORDPRESS_DB_PASSWORD=wordpress \
  wordpress:cli-php8.2 sh -c \
  'php -d memory_limit=1G /usr/local/bin/wp plugin check <slug> --format=json --severity=5 --path=/var/www/html > /tmp/report.json 2>/dev/null; echo EXIT:$?'
```

Hard rules learned the expensive way:

1. **WordPress cannot boot without a DB.** `wp plugin install` and
   `wp plugin check` load WP — a DB-less bootstrap dies with "Error
   establishing a database connection". Always provision MySQL (service
   container in CI; scratch DB locally).
2. **Activate plugin-check; never `--require` it.** `--require=.../
   plugin-check/plugin.php` loads PCP before WP boots and fatal-errors with
   `Call to undefined function plugin_dir_path()`. `wp plugin install
   plugin-check --activate` is the only working invocation.
3. **`wordpress:cli-php8.2` runs as uid 82** (the Apache image's www-data is
   uid 33). Files in the shared `wp_core` volume are owned by 33 — pass
   `--user 33:33` for any run that writes uploads/cache.
4. **The CLI image's `wp` shim ignores `WP_CLI_PHP_ARGS`.** Memory errors
   (128M cap while loading WooCommerce et al) → prefix every call with
   `php -d memory_limit=512M /usr/local/bin/wp`.
5. **Windows bind-mount readdir truncation.** After heavy writes (e.g. tar
   extraction) through a Windows bind mount, Docker Desktop can serve a
   truncated directory listing to containers (host `find` sees 9365 files,
   container sees 4583). Symptom: PCP report is absurdly small and
   `no_plugin_readme` fires even though readme.txt exists. For full-tree PCP
   sims use **Linux-native docker volumes** (`docker volume create`,
   `chown -R 82:82` first) and verify the file count INSIDE the run container
   before trusting the report. Small plugin trees (docs-hub scale, `cp -r`
   in-container) are unaffected.
6. **PCP CLI caching.** Results can look stale across re-runs; bump the
   plugin's `Version:` header in the sim tree to force fresh results when a
   report doesn't change after fixing files.
7. **Exit code + report shape.** `wp plugin check --format=json` emits one
   `FILE: <path>` header + JSON array **per file with findings** (chunked
   stream, not one array). Gate with the slurp form:
   `jq -s '[.[][] | select(.type=="ERROR" and .code!="<allowlist>")] | length'`.
   The report is NOT a single valid JSON document — `json_decode()` of the
   whole file returns null, and a run with zero findings produces an EMPTY
   report. In `bin/run-docs-hub-plugin-check.sh` the gate is grep-based
   (`"type":"ERROR"` — no space after the colon in PCP's output) so no jq
   is needed.
8. **The `--help` trap:** `wp plugin check --help` fatal-errors (PCP's
   mu-plugin hook runs without a plugin arg). Don't use it; read the source
   under `wp-content/plugins/plugin-check/includes/`.
9. **The report is ephemeral.** `/tmp/pcp-report.json` lives in the one-off
   container's filesystem and is gone when the run exits — a second `docker
   run` to inspect it finds nothing. Compute the gate (and copy the report
   to a mounted host dir) INSIDE the same `sh -c` that ran the check.
10. **No `jq` in `wordpress:cli-php8.2` (current image), and host-shell
   quoting mangles inline gates.** `sh: jq: not found` aborts the documented
   one-liner, and nested `$(php -r '…$f["type"]…')` through the Windows
   host shell dies with `syntax error near unexpected token`. Both were hit
   on the 0.4.7 pass. Use `bin/run-docs-hub-plugin-check.sh` — it writes the
   runner as a heredoc (LF endings, no quoting trap), copies it into the
   container before executing (the bind mount is read-only, so in-place
   `sed -i 's/\r$//'` on a Windows-host script fails with "Resource busy"),
   and counts blocking errors with grep instead of jq.

For small plugin trees (docs-hub scale) a fully isolated variant avoids the
QA volume entirely — build the stage tree on the host with the CI's exact
`tar --exclude` list, mount it read-only, download WP core into the
container, and `cp -r` the plugin in.

**Preferred: `bin/run-docs-hub-plugin-check.sh`** (repo root) does the
staging + scratch DB + one-off PCP run + grep-based gate in one shot,
handling pitfalls 9 and 10. The raw commands below are the fallback when
that script needs adapting:

```bash
# Host: stage the ZIP-shaped tree (mirrors build-spa-addons.yml EXCLUDES +
# docs-hub's `--exclude='*.md'`).
mkdir -p /f/GITHUB/tmp-dh-pcp/nvoos-docs-hub
tar -C addons/docs-hub -cf - --exclude='./node_modules' --exclude='./src' \
  --exclude='./tests' --exclude='./vendor' --exclude='./docs' \
  --exclude='./.wordpress-org' --exclude='*.md' \
  --exclude='./composer.json' --exclude='./composer.lock' \
  --exclude='./package.json' --exclude='./package-lock.json' \
  --exclude='./tsconfig.json' --exclude='./esbuild.config.js' \
  --exclude='./eslint.config.js' --exclude='./vitest.config.ts' \
  --exclude='./.gitignore' --exclude='./.distignore' . | \
  tar -C /f/GITHUB/tmp-dh-pcp/nvoos-docs-hub -xf -

# Container: bootstrap → activate PCP → cp plugin → check → gate, all in one
# run (pitfall 9). No --user needed (nothing written to the wp_core volume).
MSYS_NO_PATHCONV=1 docker run --rm --network oos-wp_default \
  -v F:/GITHUB/tmp-dh-pcp:/plugin-src \
  -e WORDPRESS_DB_HOST=oos-wp-db -e WORDPRESS_DB_NAME=wordpress_pluginchk \
  -e WORDPRESS_DB_USER=wordpress -e WORDPRESS_DB_PASSWORD=wordpress \
  wordpress:cli-php8.2 sh -c 'set -e; \
    php -d memory_limit=512M /usr/local/bin/wp core download --version=latest --skip-content --path=/tmp/wp --quiet; \
    php -d memory_limit=512M /usr/local/bin/wp config create --dbname=wordpress_pluginchk --dbuser=wordpress --dbpass=wordpress --dbhost=oos-wp-db --path=/tmp/wp --quiet; \
    php -d memory_limit=512M /usr/local/bin/wp core install --url=http://127.0.0.1 --title=PCP --admin_user=admin --admin_password=admin --admin_email=a@a.com --path=/tmp/wp --quiet 2>/dev/null || true; \
    php -d memory_limit=512M /usr/local/bin/wp plugin install plugin-check --activate --path=/tmp/wp --quiet; \
    cp -r /plugin-src/nvoos-docs-hub /tmp/wp/wp-content/plugins/nvoos-docs-hub; \
    php -d memory_limit=1G /usr/local/bin/wp plugin check nvoos-docs-hub --path=/tmp/wp --format=json --severity=5 > /tmp/pcp-report.json 2>/tmp/pcp-stderr.log; \
    echo PCP_EXIT:$?; \
    ERRORS=$(cat /tmp/pcp-report.json | jq -s "[.[][] | select(.type==\"ERROR\" and .code!=\"PluginCheck.CodeAnalysis.Offloading.OffloadedContent\")] | length"); \
    echo BLOCKING_ERRORS:$ERRORS; cat /tmp/pcp-report.json; \
    cp /tmp/pcp-report.json /plugin-src/pcp-report.json'
```

Notes: `wp core install` prints a sendmail warning (no MTA in the container)
— harmless, and `|| true` covers the idempotent re-run case. Expected healthy
output: `PCP_EXIT:0`, `BLOCKING_ERRORS:0`, with only the two allowlisted
`OffloadedContent` rows and the `NonPrefixedTraitFound` warning in the
report.

## The CI gate

Two workflows carry the gate:

- `.github/workflows/build-spa-addons.yml` → `plugin-check` job (docs-hub
  ZIP; active). Runs on PRs touching `addons/docs-hub/**`, gates on
  `ERROR`-severity findings minus the allowlisted `OffloadedContent`, and
  documents the one non-blocking `NonPrefixedTraitFound` warning.
- `.github/workflows/release.yml` → `plugin-check` job (LEGACY `v*` tag
  path, slug `wp-mcp-ai`). Fixed mechanically (DB + activate + no
  `--require` + slurped jq) but **the active release path is
  `build-nvdigital-oos-wporg.yml`** (`nvdigital-oos-v*` tags, slug
  `nvdigital-open-operator-system-oos`, text-domain transform at packaging
  time). The legacy gate will report the TextDomainMismatch backlog below —
  that's the point of the gate; see R-T-04.

Job anatomy (copy this shape, not the old DB-less one):

```yaml
services:
  mysql:
    image: mysql:8.0
    env:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: wordpress_pluginchk
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    ports: ["3306:3306"]
    options: >-
      --health-cmd="mysqladmin ping --silent"
      --health-interval=10s --health-timeout=5s --health-retries=5
# steps: wp core download → wp config create (real creds) → wp core install
# → wp plugin install plugin-check --activate → unzip target ZIP →
# wp plugin check <slug> --format=json --severity=5 → jq -s gate
```

The base-plugin current PCP state (measured on WP 7.1 + PCP 2.1.0 against a
ZIP-shaped tree, Linux volume): **~31k ERRORs, ~3.9k WARNINGs**, dominated by
`WordPress.WP.I18n.TextDomainMismatch` (~30.9k — repo domain `mcp-ai-wpoos`
vs expected `wp-mcp-ai`/wp.org slug). This is a known backlog for the
submission track, NOT something to allowlist. The docs-hub ZIP is clean
(0 blocking errors, 1 documented warning).

### Known PCP findings triage

| Code | Verdict | Handling |
|---|---|---|
| `PluginCheck.CodeAnalysis.Offloading.OffloadedContent` | False positive | Allowlist — flags literal `raw.githubusercontent.com` hosts in the SSRF-hardened, host-allowlisted remote fetcher (disclosed in `readme.txt == External Services ==`) |
| `WordPress.NamingConventions.PrefixAllGlobals.NonPrefixedTraitFound` | Intentional (docs-hub) | Warning only — the `WP_MCP_AI_Inline_Async_Tick_Trait` stub must carry the BASE plugin's trait name so the real trait replaces it when NV oOS is active |
| `WordPress.WP.I18n.TextDomainMismatch` | Real blocker (base) | Text domain must equal the wp.org slug/dir name; the repo domain is `mcp-ai-wpoos`. Needs the slug migration track — do not allowlist |
| `no_plugin_readme` | Real or mount artifact | readme.txt must sit at the ZIP root. If it does and PCP still fires, suspect the bind-mount truncation (pitfall 5) |
| CodeAnalysis — core function newer than the declared `Requires at least` | Real | PCP flags any WP function whose `@since` is newer than the plugin's minimum (e.g. `wp_generate_uuid4()` is WP 6.7+ under `Requires at least: 6.0`). Fix: a `function_exists()`-guarded polyfill (keeps the floor) or bump `Requires at least`. Add the same check for any WP API used by new standalone plugins |

### Second plugin in the pipeline (nvoos-design-system, issue #6811)

The addon is functionally standalone (all base-plugin touchpoints gated:
tools behind `wp_mcp_ai_register_tools` + `interface_exists`, Paper Store
behind `class_exists`, AI keys behind `function_exists`, WooCommerce behind
`class_exists`) but still needs the docs-hub packaging set before PCP:
`readme.txt` (Stable tag == header Version), `LICENSE`, `CHANGELOG.md`,
`.distignore` tri-synced with `bin/build-addon-zips.sh` (docs-hub ships only
`readme.txt`, no `*.md`), `languages/<slug>.pot`, `.wordpress-org/` assets,
the `wp_generate_uuid4()` polyfill above, and a `plugin-check` CI job — plus
owner-side steps: standalone repo, subtree-sync workflow + deploy token
(mirror `sync-nvoos-docs-hub.yml`), wp.org slug request, SVN submission.

## The reviewer reply pass (0.4.3 → 0.4.4, PR #6606)

The first real wp.org review pended the docs-hub submission. Below is the
findings taxonomy (reviewer + AI flags), the fix applied, and the
related-issue sweep that found two more leaks. Reuse this map whenever the
next reviewer email lands — the same categories recur across plugins.

### Findings taxonomy → fixes applied

| Review finding | Root cause | Fix pattern (docs-hub) |
|---|---|---|
| "Add yourself to Contributors" — the listed name must be a **wp.org username**, not the GitHub org | `Contributors: nvdigitalsolutions` but the account is `vsamtani` | `Contributors: vsamtani` — only real wp.org usernames; drop org names with no account |
| Minified `assets/dist/docs-hub.js` has no bundled source and no repo link (Guideline 4) | `src/` is excluded from the ZIP; no readme disclosure | Add `== Source Code ==` readme section (public repo URL + `npm install && npm run build` steps + where dev files live), AND make the bundle self-describing: esbuild `banner: { js: …, css: … }` with `/*!`-style source/build/license header. Do **both** JS and CSS banners — the CSS bundle is generated too |
| `permission_callback` — `/search` is public but leaks `source: "context"` excerpts to non-admins | Named public permission callback is fine; the *data* was the leak — `get_manifest()` and `get_page()` filtered context but `search()` did not | In every public endpoint, filter `source === 'context'` for `! current_user_can('manage_options')`. Verify **all** context surfaces: manifest, pages, search, **and the sitemap** (docs-hub's sitemap provider was exposing context slugs — caught by the sweep, not the review) |
| `load_plugin_textdomain()` unnecessary (WP ≥ 4.6) | Redundant since plugin requires 6.0; wp.org loads translations automatically | Remove the call; keep the `Text Domain`/`Domain Path` header. (Keep only if the plugin supports WP < 4.6.) |
| "Plugins should not hijack the admin dashboard" (Guideline 11) | Site-wide `admin_notices` warning rendered on every admin page | Scope notices to the plugin's own screen via `get_current_screen()` (docs-hub: `settings_page_nvoos-docs-hub`). Action-result notices (rebuild success/fail) that fire once after a form POST on the settings page are contextual and fine |
| Staging transients: `set_transient` on page write (L168) + live transient read (L149) break staging isolation | `get_manifest`/`get_search_index` honoured the staging toggle; `get_page`/`set_page` did not | Mirror the manifest pattern: skip transient read when `$this->staging`, only set transient when `! $this->staging` |
| `uninstall.php` recursive delete follows symlinks | `rm_rf` recursed via `is_dir()` without link checks or containment | Check `is_link()` **before** `is_dir()` (delete the link, never the target), and verify `realpath()` stays inside the cache root before recursing. Apply to **every** recursive delete in the codebase — `Cache::rm_rf()` had the same bug |

### Second reviewer pass (0.4.4 → 0.4.5, review P0TDX367696HGN)

The 0.4.4 fixes passed except two residuals — one a *category* the reviewer
wanted re-framed, one an AI-flagged corner of the previous symlink fix:

| Review finding | Root cause | Fix pattern (docs-hub) |
|---|---|---|
| "Calling files remotely" — flagged `raw.githubusercontent.com` in `class-nvoos-docs-hub-remote-repo.php` (ALLOWED_HOSTS + raw URL build) | The remote fetcher IS the plugin's service (like Akismet/oEmbed) — server-side only, host-allowlisted, admin-triggered — but the readme didn't say so in reviewer terms | Do **not** rip out the service. Rewrite `== External Services ==` to state it is a *documentation-import service*: what it does, the servers called (`api.github.com`, `raw.githubusercontent.com`), that **no account is required** (optional token only raises rate limits), that fetches are server-side/cached, and that rendered pages may contain content-authored links/images to github.com domains loaded by the *browser*, not the server. Reply explaining the service exception (Guideline 6) |
| "The initial cache directory can itself be a symlink: realpath() treats its external target as the containment root" (uninstall.php:112) | The 0.4.4 containment guard resolves the root *from the path being deleted* — when the top-level cache dir is a symlink, target == root and the guard passes trivially | `is_link()`-check the **top-level** cache dir before recursing and delete only the link. Same class of bug in `Cache::get_live_dir()`: a symlinked cache dir would receive `.htaccess`/`index.php`/`pages/` writes and make `clear()`'s `glob()` deletes touch external files — unlink the link and recreate a real dir there. Keep `is_link()`-first guards at every recursion entry. Regression tests: symlink the cache dir → `Cache::clear()` and `require uninstall.php` must leave the external target's sentinel file intact |

### Third reviewer pass (0.4.6 → 0.4.7, review P0TDX367696HGN)

The 0.4.5 fixes passed but the automated gate flagged two new items — one
packaging rule and one WP 6.7+ timing bug:

| Review finding | Root cause | Fix pattern (docs-hub) |
|---|---|---|
| "Please declare 'Tested up to' only in your readme file" — the value is also in the main PHP file's plugin headers | wp.org's readme header list is the ONLY supported place for `Tested up to`; declaring it in the PHP header risks the wrong compatibility version being shown | Remove the `* Tested up to:` line from the main PHP file; keep it in `readme.txt` only. `Requires at least`/`Requires PHP`/`Text Domain`/`Domain Path` ARE valid PHP headers — only `Tested up to` is readme-only. Sweep: the base plugin `mcp-ai-wpoos.php` and several addons also carry the header — fix each before ITS submission |
| "The plugin has problems when it is activated… early WooCommerce translation-loading notice before init" | `Rebuild_Job::schedule()` ran `wp_schedule_event()` on `plugins_loaded`. `wp_schedule_event()` consults `wp_get_schedules()`, which applies the `cron_schedules` filter — WooCommerce registers a TRANSLATED interval there (`__( 'Once monthly', 'woocommerce' )`), and on WP 6.7+ translations load on `init`, so the call triggers the "translation loading triggered too early" notice on the first dashboard load after activation | Move cron scheduling to `init` (never call `wp_schedule_event()` or translation functions before `init`). Related sweep: (a) add `register_deactivation_hook()` → `unschedule()` clearing the daily cron AND pending pipeline tick events (ghost-event cleanup), (b) on self-deactivation clear the cache but do NOT re-enqueue an async rebuild — the tick callbacks no longer exist once inactive, (c) grep the whole plugin for other pre-`init` scheduling/translation — none remained. Regression tests: schedule/unschedule round-trip + self-vs-related deactivation behavior |

### Related-issue sweep checklist (always run after fixing the flagged items)

Each review item is a category — grep the whole plugin for siblings:

1. **Context/sensitive-data leaks** — every surface that serves indexed
   content to guests: REST endpoints, sitemap providers, feeds, shortcode
   data attributes. docs-hub sweep caught the **sitemap** leaking context
   slugs (fixed alongside search).
2. **Transient staleness around staging** — after promotion, md5-keyed page
   transients can still serve stale (or deleted) pages until TTL. Fix:
   `promote_staging()` deletes page transients for every swapped slug
   (+ best-effort orphan slugs via `--`→`/` reversal — lossy but a wrong-key
   delete is a harmless miss), and `clear()`/`uninstall.php` wildcard-clean
   `_transient_<prefix>p_*` rows with `$wpdb->prepare` + `esc_like`.
3. **Symlink traversal in deletion** — grep `rmdir|unlink|RecursiveDirectoryIterator|
   rm_rf`. Every recursive delete needs the is_link + realpath-containment
   guard (see fixes above). **Also guard the containment root itself**: when
   the root being deleted IS the containment root (uninstall's cache dir),
   `is_link()`-check it first or the external target becomes the root (the
   0.4.4 → 0.4.5 finding). Sweep `glob(`+`wp_delete_file` cleanup and
   `wp_mkdir_p`+guard-file writes too — those follow a symlinked cache dir
   into external targets as well (`get_live_dir()` fix).
4. **Secrets in localized/admin output** — grep `wp_localize_script` and
   form renders for settings blobs. docs-hub localized the FULL settings
   (including GitHub PATs in `remote_repos[].token`) into the page DOM; the
   JS only stripped tokens at export time. Fix: strip server-side before
   localizing (`settings_without_tokens()`). The PHP form was already safe
   (password input, value never echoed — "(saved — enter new value to
   change)" placeholder).
5. **Remote host disclosure (Guidelines 6/7)** — every `wp_remote_*`/curl
   call must match the `== External Services ==` readme section exactly.
   docs-hub: allowlist is exactly `api.github.com` +
   `raw.githubusercontent.com` — matches the readme.
6. **Frontend data paths** — verify the SPA only hits the permission-checked
   endpoints (docs-hub: `manifest` + `pages/{slug}` + `search` only;
   FlexSearch fallback indexes the already-filtered manifest).
7. **Other notice/admin-surface scans** — grep `admin_notices` and confirm
   each render is either on-page (settings screen) or a one-shot
   action-result; grep `$_GET/$_POST/$_REQUEST` and confirm cap + nonce +
   sanitize on every handler.

### Reviewer reply email (template)

Keep it brief, factual, no filler (the review explicitly asks for this).
Reply to the thread, list each finding as resolved, state the new version,
and confirm validation. State the permalink only if changing it.

```text
Hi,

Thanks for the detailed review. All reported issues are fixed and version
0.4.7 has been uploaded:

- Removed the "Tested up to" header from nvoos-docs-hub.php — it is now
  declared only in readme.txt.
- The daily rebuild cron is now scheduled on init instead of plugins_loaded,
  so wp_schedule_event() no longer runs before translations load (the cause
  of the "translation loading triggered too early" notice with WooCommerce
  active).
- Related sweep: rebuild cron events are cleared on plugin deactivation, and
  deactivating the plugin no longer enqueues a rebuild that cannot run.

Validated on a clean WordPress install with WP_DEBUG on: activation is
clean, wp plugin check reports 0 errors (only the documented allowlisted
items), and the full PHPUnit suite passes on WordPress 6.9 and 7.1.

Keeping the permalink nvoos-docs-hub.

Thanks,
[Your name]
```

Process notes from the pass:

- **Version bump is mandatory per release** (Guideline 15): header `Version`,
  `NVOOS_DOCS_HUB_VERSION`, readme `Stable tag`, changelog, upgrade notice,
  POT `Project-Id-Version`, `.wordpress-org/README.md` example versions.
- **One review round = one commit cluster**; PR against `alpha-working`
  (`fix/docs-hub-wporg-review-044` → PR #6606). CI runs the docs-hub
  plugin-check job on PRs touching `addons/docs-hub/**`; tagging
  `docs-hub-vX.Y.Z` after merge builds the ZIP; `sync-nvoos-docs-hub.yml`
  mirrors the addon to the standalone public repo.
- **Unrelated working-tree changes** (e.g. stale `vendor/composer/*` from a
  `composer install`) stay unstaged — commit only the addon paths.
- After merge: upload the ZIP, then reply to the same email thread.

### Running the docs-hub PHPUnit tests

Docs-hub tests are NOT in the root `phpunit.xml.dist` testsuite — passing the
`addons/docs-hub/tests` directory to phpunit runs nothing. Pass the files
explicitly:

```bash
vendor/bin/phpunit -c phpunit.xml.dist --no-coverage \
  addons/docs-hub/tests/test-cache-staging.php \
  addons/docs-hub/tests/test-rest-manifest.php \
  addons/docs-hub/tests/test-rebuild-chunked.php \
  addons/docs-hub/tests/test-rebuild-job.php \
  addons/docs-hub/tests/test-rebuild-pipeline-inline-kick.php \
  # … (all files except test-fnmatch-polyfill.php)
```

- `test-fnmatch-polyfill.php` is a **standalone script**, not PHPUnit —
  passing it errors with "Class test-fnmatch-polyfill cannot be found".
- **Run them through the Docker runner, not the host vendor** — see
  `.agents/skills/mcp-ai-wpoos-test-suite/SKILL.md` → "Cross-worktree runs".
  The host `vendor/` is frequently a pruned copy whose classmap has zero
  PHPUnit entries (`Class "PHPUnit\\TextUI\\Application" not found` on BOTH
  host and container); the Linux vendor volume is the reliable path. The
  0.4.7 pass validated the full docs-hub set on **WP 6.9 and WP 7.1** with
  an isolated DB (`wordpress_test_moth*`) — 107 tests, 0 failures each.
- Known pre-existing **Windows-only failure**:
  `Test_Docs_Hub_Scanner::test_path_traversal_prevented` (realpath behavior
  differs on Windows; passes on Linux CI). Don't chase it in local runs.
- The suite boots the full base plugin, so expect `wp_is_block_theme`
  notices and Pro module warnings in the output — cosmetic.

## Packaging exclusions (tri-sync)

Standalone plugin ZIPs keep dev files out via **three lists that must stay in
sync**: the addon's `.distignore`, the `docs-hub` step of
`bin/build-addon-zips.sh`, and the rsync/tar excludes in the CI workflow
(`build-spa-addons.yml` assemble step). Current sets exclude: `node_modules/`,
`src/`, `tests/`, `vendor/`, `composer.json|lock`, `package*.json`,
esbuild/eslint/tsconfig/vitest configs, `docs/`, `.wordpress-org/`,
`.gitignore`, `.distignore`, `.DS_Store`. Any new dev-only path must be added
to all three.

The same trap bit the content-graph workflow (`build-nvoos-content-graph.yml`)
in PR #6662: its inline rsync list drifted from `.distignore`, a dev
`blueprints/` folder shipped in the ZIP, and PCP failed on the leaked PHP
file. Playground-demo dev folders and their exclusion checklist live in the
`mcp-ai-wpoos-playground-demos` skill.

## .wordpress-org assets

Layout mirrors `plugins/nvoos-content-graph/.wordpress-org/`:

```
.wordpress-org/
├── README.md        # asset checklist + SVN upload runbook
├── assets/          # icon-128x128/256x256.png, banner-772x250/1544x500.png,
│                    # screenshot-{1..N}.png  (committed, excluded from ZIP)
└── source/          # artwork masters (1024x1024 icon, 1344x768 banner)
```

- `.wordpress-org/` maps to the plugin's SVN `assets/` dir — it never ships
  inside the ZIP.
- PNGs are gitignored locally via `.git/info/exclude` (`*.png`) — stage with
  `git add -f` (content-graph precedent).

### Screenshot capture (Playwright)

Templates in `bin/`: `capture-nvoos-content-graph-screenshots.js` (origin),
`capture-nvoos-docs-hub-screenshots.js` (newer, docs-hub specific). Workflow:

1. QA stack up (`docker compose up -d`), plugin active, data seeded
   (docs-hub: remote repo configured + `wp nvoos-docs rebuild --sync`,
   published `[nvoos_docs]` page).
2. Login as admin (`admin`/`password`) for admin shots; guest context for
   frontend (public access). Set generous timeouts — the QA site serves pages
   in 20–60s (`setDefaultTimeout(240000)`).
3. Element captures for settings widgets; viewport/fullPage for the frontend.
4. Verify with a pixel-level QA pass (sub-agent can decode text/layout
   without vision) before committing.

Capture pitfalls (all hit in practice):

- **fullPage texture limit** — Chromium fails `page.screenshot` on very tall
  pages ("Unable to capture screenshot"); use viewport captures for shots
  with overlay UI (search dropdowns).
- **Theme content width** — default themes constrain content to ~620px,
  dropping the docs app below its sidebar/TOC breakpoints. Inject
  `:root { --wp--style--global--content-size: 1240px !important;
  --wp--style--global--wide-size: 1400px !important; }` for the capture.
- **Wait for real content** — the SPA shell paints long before the REST page
  fetch lands; wait for `.dh-content` textContent length (not just the
  container) or you capture a "Loading…" screen.
- **Duplicate roots** — the shortcode emits an empty container div AND the
  rendered app root; select the live one via `[data-theme]`.
- **`locator.screenshot({clip})` is unreliable** — use `page.screenshot`
  with viewport-relative `clip` from `locator.boundingBox()`.
- **Red error rows in listing shots** — clip admin captures to exclude
  broken-link tables (they read negatively at thumbnail size).
- **Icon/banner artwork is manual** — screenshots are scripted; icons and
  banners still need design work (documented in the `.wordpress-org/README.md`).

## readme.txt standards

- `Contributors:` is a case-sensitive, comma-separated list of **wp.org
  usernames** — not GitHub orgs (the review flagged `nvdigitalsolutions`
  because the account is `vsamtani`). Only list accounts that exist; drop
  org names with no wp.org account.
- `== External Services ==` section: every third-party host contacted,
  server-side-only wording, data-sent statement, Terms + Privacy URLs. The
  host list must match the code's allowlist exactly (docs-hub: `api.github.com`
  + `raw.githubusercontent.com`).
- `== Source Code ==` section (Guideline 4): public repo URL, where the
  frontend source lives (`src/`), the exact build steps (`npm install &&
  npm run build`), and where dev-only files live. The bundled dist files
  should be self-describing too: esbuild `banner: { js, css }` with a
  `/*!`-style header (source URL + build command + license).
- `== Screenshots ==` section with `1. Alt text` lines matching
  `screenshot-{N}.png` in SVN assets; add when the PNGs land.
- `Stable tag` must equal the plugin header `Version`; `Tested up to` latest WP.
  `Tested up to` must be **major.minor only** (`7.1`) — when the value
  matches the latest stable, a patch-level value (`7.1.1`) is a PCP ERROR
  `invalid_tested_upto_minor` ("The version number should only include major
  versions"). A major.minor `7.1` against latest `7.1.x` is NOT stale (PCP
  compares major.minor). Validate the suite against the patch release anyway
  — declare major.minor, back it with the patch run.
- Trim tags to directory-standard tags (PCP flags exotic tags).
- Text Domain header must equal the slug for the ZIP dir name on wp.org.

## Skill bookkeeping (when adding skills like this one)

Adding a coding-time skill requires count updates in: `AGENTS.md` §1
(inventory table row + coding-time-vs-runtime paragraph),
`.github/copilot-instructions.md` (multi-agent-awareness bullet + repo-tree
comment), and the `README.md` repo-map row. Executed-release lines are left
untouched; the next docs catch-up (`.agents/skills/mcp-ai-wpoos-updates`)
folds the new skill into the next release notes.

## References

- Docker one-off runner patterns: `.agents/skills/mcp-ai-wpoos-test-suite/SKILL.md`
  (cross-worktree runs, shared-DB etiquette)
- Plugin operational guide: `.agents/skills/mcp-ai-wpoos-plugin/SKILL.md`
- Maintenance tracks: `.agents/skills/mcp-ai-wpoos-updates/SKILL.md`
- Capture scripts: `bin/capture-nvoos-docs-hub-screenshots.js`,
  `bin/capture-nvoos-content-graph-screenshots.js`,
  `bin/README-SCREENSHOT-TOOLS.md`
