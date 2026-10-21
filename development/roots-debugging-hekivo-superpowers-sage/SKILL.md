---
name: roots-debugging
description: Use when something is broken on a Roots/Acorn WordPress project and the cause is unknown - 500 or white screen, Acorn boot failure, "class not found", stale Blade, missing ACF blocks, assets 404, Livewire not mounting. Also when it works locally but not on staging or production, or a change is not visible after a deploy - old HTML, Livewire 419 or RangeError right after a deploy, edge/CDN, object cache or OPcache holding old state. Read-only on shared environments. For new features use the building skill; for Lando container problems use lando-wp.
---

# Debugging Roots and Acorn projects

Follow the `systematic-debugging` discipline: reproduce, gather evidence, form one hypothesis, test it, then fix. No fix without a root cause you can show (a log line, a header, a command output).

Runner placeholders (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.composer}}`, `{{runner.node}}`, `{{runner.cache}}`, `{{runner.logs}}`) come from the session context. On Lando the defaults are `lando wp`, `lando wp acorn`, `lando composer` and so on; the `lando-wp` skill documents the wiring and the container-level symptoms (DNS, certificates, ports, database service). Do not repeat that table here: if the symptom is "the site does not even resolve", "port already allocated" or "tooling command unknown", switch to `lando-wp`.

## When to use

- A request returns 500, a blank page or a Whoops/ignition style error page.
- `{{runner.acorn}} <command>` fails, prints nothing, or the command is missing.
- A Blade change, a new class, a new block or a config edit does not show up.
- Styles or scripts are missing, return 404, or point to a dev server that is not running.
- Behaviour differs between local and a deployed environment.

Not for building a feature (use the profile's building skill) or for performance tuning (use `wp-performance`).

## Inputs required

1. The profile and its Acorn base path (session context): theme folder, mu-plugin folder, or project root.
2. Where it fails: local, review, staging or production. Remote environments are read-only for you: observe and report; flushing, purging or restarting needs an explicit request.
3. What changed: branch switch, `composer.lock` or lockfile change, deploy, database sync, new class, config edit.
4. Scope: every request, one URL, one block, logged-in only, one language, only cached pages.

### Where things live per profile

| Item | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Acorn base path | the theme folder | the plugin folder (`ACORN_BASEPATH`) | the project root |
| Application logs | `storage/logs/` in the theme if `storage/` exists, otherwise `wp-content/cache/acorn/logs/` (Bedrock: `web/app/cache/acorn/logs/`) | `storage/logs/` in the plugin if present, otherwise the WordPress cache folder as for a theme | `storage/logs/` at the root |
| Compiled views | `storage/framework/views/` (same base as the logs) | same | same |
| Config, route, package caches | `storage/framework/cache/` (or `.laravel/` when that folder exists in the base path) | same | same |
| WordPress `debug.log` | `<content dir>/debug.log` when `WP_DEBUG_LOG` is true | same | same (content dir is under the webroot) |
| Composer autoload | the theme's own `vendor/` | the plugin's own `vendor/` | the root `vendor/` |
| Provider registration | `withProviders([...])` in the theme's `functions.php` (plus packages auto-discovered from Composer) | provider list in the boot code (`withProviders`) | `composer.json` `extra.acorn.providers` |
| Livewire, ACF Composer, Poet | present only if installed | usually present | not installed by default |

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run on a remote host, in CI or in a deploy script go in a separate block labelled with where they run and who runs them.

Shared environments (staging, review, production) are read-only for you: diagnose first with requests, headers, page source and logs; any purge, flush, cache clear, restart or redeploy there is proposed with the exact command and the owner of that layer, never run and never presented as the first step.

1. **Locate.** Answer the four inputs before touching code. "Works locally, broken after a deploy" goes straight to the deploy-staleness check below before any code reading; that check still includes the log read in step 2 (the Acorn log under the base path's `storage/logs/`, or the container log on a remote environment).
2. **Collect evidence.**
   - Tail the Acorn log and the WordPress `debug.log` (paths above). If neither file exists, logging is not configured or the folder is not writable; that is itself a finding.
   - Check the web server/PHP log through the runner (`{{runner.logs}}`; see `lando-wp`). On a remote environment read the container or platform log. Logs live under the Acorn base path (the plugin's or app's `storage/logs/`), not in a theme folder unless the profile is `sage-theme`.
   - Print the effective debug flags: `{{runner.wp}} eval 'var_dump(WP_DEBUG, WP_DEBUG_LOG, WP_DEBUG_DISPLAY, WP_ENVIRONMENT_TYPE);'`. Acorn's exception page is shown only when `WP_DEBUG` and `WP_DEBUG_DISPLAY` are both true; otherwise errors go only to the log. Ask the user to enable them in the environment file rather than editing it yourself.
   - Request the URL with `curl -sI` and read status and cache headers.
   - Does Acorn boot at all? `{{runner.acorn}} list`. If this fails, the problem is boot-level (autoload, provider, storage permissions), not a view.
3. **Categorize** with the table below, then run the targeted check.
4. **Form one hypothesis**, change one thing, observe. If two hypotheses fail, stop, summarise the evidence and ask.
5. **Fix** with the smallest change at the root cause, using the native WordPress/Acorn mechanism first.
6. **Verify** by repeating the original reproduction, then `{{runner.cache}}`, the project's test runner and linter.
7. **Report** with four headings in this order: **Evidence** (what you observed or what the user should run to observe it), **Root cause**, **Fix** (local commands through the runner; remote actions as proposals with an owner), **Prevention** (deploy step, cache rule, test).

### Categories and first checks

| Category | Symptoms | First check |
|---|---|---|
| Stale caches | Old markup or behaviour after a PHP, Blade or config change | Clear the layers in [references/cache-layers.md](references/cache-layers.md), cheapest first |
| Boot failure | Fatal on every request, every Acorn command fails | Last lines of the log; `vendor/` present for the base path; provider class exists and namespace matches `composer.json` autoload; `storage/` writable |
| Class or file not found | `Class "X" not found`, `View [x] not found` | Namespace-to-folder match, `{{runner.composer}} dump-autoload` in the right working directory, view file name and location |
| Blade rendering | Raw `{{ }}` shown, double-escaped text, wrong template | Open the compiled file in `storage/framework/views/`: its last line is a `PATH ... ENDPATH` comment that names the source view |
| Routes | 404 on an Acorn route, route works in CLI but not in browser | `{{runner.acorn}} route:list`; Acorn matches routes during `do_parse_request`; check path, method and trailing slash, cached routes (`route:clear`), and that routing is registered in the boot code. `rewrite flush` is for WordPress rewrites only |
| ACF | Block missing from the inserter, fields not saving or not showing | Class location and `$name`, location rules, ACF Composer cache (`acf:clear` then `acf:cache`), field group JSON/DB sync state |
| Livewire | Not mounting, update returns 404/419/500, props mismatch | `{{runner.acorn}} route:list` for the Livewire routes, scripts printed in the layout, stale cached HTML at the edge, then the livewire skill |
| Assets | Unstyled, JS missing, 404 on `build/` files, requests to a dev-server URL | Manifest exists; `public/hot` is a leftover from a stopped dev server; URL base. See `tailwind-vite-assets` |
| Object cache | Options, menus or counts wrong; survives restarts and deploys | `{{runner.wp}} cache type`; flush locally; remote: tell the user |
| Hooks | Filter or action has no effect | Timing and load order; see `wp-hooks-lifecycle` |
| Database | Connection refused, migration errors | Environment file host/credentials; `{{runner.acorn}} migrate:status` |
| Deploy staleness | Local works, remote shows old HTML or assets; Livewire 404/419/checksum errors right after a deploy | Read-only first: `curl -sI <url>` for `age`, `cf-cache-status`/`x-cache`/`x-proxy-cache`; compare the asset hashes and the Livewire script/update URL in the served HTML with a cache-busted request and with the new build. Old HTML carries old snapshots, tokens and hashed URLs. Then name each layer that can hold old state and who clears it: edge/CDN/page cache (deploy or infra owner), object cache (`{{runner.wp}} cache flush`, environment owner), OPcache (PHP service restart), compiled views and Acorn caches (`{{runner.acorn}} optimize:clear`, deploy script). See [references/cache-layers.md](references/cache-layers.md) |

Symptom-by-symptom causes and fixes: [references/symptoms.md](references/symptoms.md).

## Verification

- The original reproduction now behaves correctly and the log shows no new error for it.
- You can name the root cause and show the evidence that confirmed it, not only that the symptom vanished.
- The cache layers you cleared are listed in the report (a fix that only works until the next cache build is not a fix).
- The project's tests and linter pass through the runner.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Requests fail right after `optimize:clear` (seen on a project using ACF Composer) | A package manifest was deleted and not rebuilt | Run `{{runner.acorn}} optimize` (or the package's own cache command) and retry; prefer `view:clear` and `cache:clear` over `optimize:clear` when you only need views gone |
| Change visible in CLI but not in the browser | PHP-FPM OPcache differs from CLI OPcache | Restart the PHP service (Lando: `lando restart`) |
| `{{runner.acorn}}` prints "command not found" for a package command | Package discovery cache is stale | `{{runner.acorn}} package:discover`, then retry |
| Blade error points to a hashed filename | The error is reported in the compiled file | Read the `PATH` comment at the end of that file to find the source view |
| Fix works locally, not on the remote | A cache layer outside the code (object cache, edge, opcache) holds the old state | Ask the user to flush that layer; do not do it yourself on shared infrastructure |
| Log file empty while the page fails | `WP_DEBUG_LOG` false or logging channel writes to stdout in that environment | Check `WP_DEBUG_LOG` and the Acorn logging channel; in containers read the container log |
| Exception page not shown | `WP_DEBUG` or `WP_DEBUG_DISPLAY` false | Enable in the environment file (ask the user), reload |

## Escalation

- Evidence points to infrastructure (container runtime, database server, CDN, orchestration), a third-party plugin's code, or a vendor theme: report the evidence and stop.
- The fix needs edits to environment files, `wp-config.php`, CI or production data: ask first.
- Two hypotheses failed: summarise what you ruled out and ask the user.
- Do not commit, push or run remote cache purges, restarts or database syncs unless the user asked.

<!-- verified: refs/roots-sage/functions.php:35-39 — Application::configure()->withProviders([...])->boot() in functions.php;
refs/roots-acorn/config/app.php:45 — 'debug' => WP_DEBUG && WP_DEBUG_DISPLAY;
wp/wp-includes/load.php:569-575,622-625 — WP_DEBUG_LOG true writes WP_CONTENT_DIR/debug.log, or to a given path;
refs/roots-docs/acorn/logging.md:20 and directory-structure.md:14-27 — logs at [wp-content]/cache/acorn/logs zero-config, storage/logs traditional;
refs/roots-acorn/src/Roots/Acorn/Application.php:184-186,201 — bootstrap path is .laravel when that folder exists, else storage/framework;
storage/framework/cache in the reference acorn-mu-plugin project — config.php, routes-v7.php, packages.php, services.php, acf-composer/, blade-icons.php present;
storage/framework/views/*.php last line — PATH ... ENDPATH comment with the source view;
vendor/roots/acorn/src/Illuminate/Foundation/Console/OptimizeClearCommand.php:59-70 — optimize:clear runs config, cache, compiled, event, route, view clears plus package clears;
vendor/log1x/acf-composer/src/Providers/AcfComposerServiceProvider.php:67-72 — optimizes(optimize: acf:cache, clear: acf:clear);
refs/roots-acorn/src/Roots/Acorn/Application/Concerns/Bootable.php:230-244 — Acorn routes handled via do_parse_request/parse_request, unmatched fall through;
vendor/roots/acorn/src/Illuminate/Foundation/Vite.php:1221-1224 — isRunningHot() is is_file(hotFile);
lando wp acorn list (the reference acorn-mu-plugin project) — view:clear, view:cache, optimize, optimize:clear, clear-compiled, icons:cache exist;
unverified: that deleting the ACF Composer manifest causes 500s on every request is an observation from one project, not read in package source -->
