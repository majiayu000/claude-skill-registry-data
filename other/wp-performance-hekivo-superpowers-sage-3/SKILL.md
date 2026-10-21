---
name: wp-performance
description: Use when a WordPress page, query or request is slow or needs profiling - TTFB, slow or N+1 queries, Query Monitor, Server-Timing, wp profile and wp doctor, autoloaded options, Redis object cache hit rate, transients, WP_CACHE_KEY_SALT. Adds the runner and Redis notes on top of the official procedure. For Eloquent query design use acorn-data; for PHP type errors use wp-phpstan.
---

# WordPress performance (wrapper)

Full procedure: `third-party/wp-performance/SKILL.upstream.md` (official WordPress skill, GPL-2.0-or-later, see `third-party/UPSTREAM.md`). Read it first; this file only adds what is specific to Roots projects run through a container runner. Paths starting with `third-party/` are relative to the kivo-wise plugin root, two levels above this skill's folder (`<skill dir>/../../third-party/...`), not inside the skill folder. In your answer, point the user to that full procedure by its resolved absolute path, and use the same resolution for any other `third-party/` path you name.

## When to use

- A page, REST route or admin screen is slow, or the query count looks high.
- You need a backend-only baseline before changing anything: autoloaded options size, object-cache drop-in, `wp doctor`, `wp profile`.
- The Redis object cache is suspected (stale data, low hit rate, flush behaviour).
- You are about to add a transient, a cache layer or an index and want evidence first.

## Inputs required

- Active profile and runner from the session context (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.cache}}`). Lando default: `lando wp`, `lando wp acorn`, the project's cache-clear tooling command.
- The URL to measure and the WordPress path as seen **inside the container** (not the host path).
- Whether the object cache is enabled in this environment (a project may disable Redis through an environment constant).

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`php`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run in CI or a deploy script go in a separate block labelled with where they run.

1. **Measure before touching code.** Never optimize blind. Record a baseline twice for the same URL: **cold** (right after `{{runner.cache}}` and, locally, `{{runner.wp}} cache flush`) and **warm** (the next request), each with time, query count and cache state, and keep both for the comparison. Point the user to the official procedure file (resolved path of `third-party/wp-performance/SKILL.upstream.md`) for the full checklist.
2. **Run the deterministic report through the runner.** The official script reads the runner from `WP_RUNNER` (a local patch, listed in `third-party/UPSTREAM.md`):

   ```
   WP_RUNNER="{{runner.wp}}" node third-party/wp-performance/scripts/perf_inspect.mjs --path=<container path> [--url=<url>]
   ```

   On Lando `{{runner.wp}}` is `lando wp`, so the value is `WP_RUNNER="lando wp"`. Without it the script calls a bare `wp` on the host and fails.
3. **Check the object cache** before suggesting any cache code. WordPress loads a `wp-content/object-cache.php` drop-in when present, and `wp_using_ext_object_cache()` reports it; with no drop-in the cache lives only for one request. Confirm with `{{runner.wp}} cache type` and, for a Redis plugin, its status subcommand. Name the native API that a fix would use (`wp_cache_get()`/`wp_cache_set()` with a group, `get_transient()`/`set_transient()`); a persistent drop-in makes those calls survive across requests without new code. If the project sets a key salt or prefix constant, a flush from one environment must not touch another.
4. **Profile with WP-CLI.** `{{runner.wp}} doctor check --all`, then `{{runner.wp}} profile stage --all` and `profile hook`. Pass `--url` so the right site is loaded (see the profile table for multisite and language-per-domain setups).
5. **Pick the fix from the official references** (`third-party/wp-performance/references/`: `database.md`, `object-cache.md`, `autoload-options.md`, `http-api.md`, `cron.md`, `server-timing.md`). Native first: use `wp_cache_get/set` with a group, `get_transient`, `WP_Query` arguments (`no_found_rows`, `fields => 'ids'`, `update_post_term_cache`) before a custom cache class.
6. **Acorn specifics.** `config:cache`, `view:cache` and `optimize` speed up the Laravel side only; they do not change WordPress queries. After a PHP change run `{{runner.cache}}` so a stale compiled view or manifest does not distort the measurement.
7. **Re-measure** with the same URL and cache state (cold and warm) and report the delta.

### Profile differences

| Topic | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
| --- | --- | --- | --- |
| Where to look for slow code | theme `app/`, composers on every view | plugin `app/`, providers booted on `after_setup_theme` | root `app/`, providers from `composer.json` `extra.acorn.providers` |
| `--path` for the runner | the WordPress core dir inside the container | same | the Bedrock-style core dir (often `public/wp`) |
| Object cache | project-chosen drop-in | project-chosen drop-in; global cache groups matter on multisite | Redis service in the landofile when present |
| Livewire cost | not present | present: each component adds a request and a hydration | absent by default |

## Verification

- `perf_inspect.mjs` prints JSON with `wpCli.available: true` (otherwise the runner value is wrong or the containers are down).
- The same URL measured twice with the same cache state gives a comparable baseline and a smaller number after the change.
- `{{runner.wp}} cache type` names the expected backend; a persistent backend survives two consecutive CLI calls.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `perf_inspect.mjs` reports `wpCli.available: false` or ENOENT | Script ran a bare `wp` on the host | Set `WP_RUNNER="{{runner.wp}}"`; start the containers |
| `WordPress not detected at the given --path` | Host path passed to a containerised WP-CLI | Use the path as the container sees it |
| Numbers differ wildly between runs | Cold vs warm object cache, or compiled views rebuilt | Run `{{runner.cache}}` once, then measure warm twice |
| Data stays stale after a fix | Persistent cache kept the old value, or an edge cache answers | `{{runner.wp}} cache flush`; check response headers for an edge cache age |
| Speed-up disappears in another environment | Object cache disabled there by a constant or env value | Compare the cache type in both environments before concluding |
| `wp profile` shows nothing | Package missing in the container | Install the package through the runner, or fall back to Query Monitor headless (official `query-monitor-headless.md`) |

## Escalation

- Cloud or APM-level evidence (traces, edge cache behaviour) is outside this skill: ask for the APM export or the response headers instead of guessing.
- A slow query that needs a new index or schema change: stop and ask for approval; write the proposal, not the migration.
- If a project-level guideline contradicts an official reference, follow the project and say so.

<!-- verified: wp/wp-includes/load.php:810 — wp_using_ext_object_cache(); load.php:860 — object-cache.php drop-in is required from WP_CONTENT_DIR; third-party/wp-performance/scripts/perf_inspect.mjs:32-34 — WP_RUNNER split on spaces, default wp; third-party/wp-performance/SKILL.upstream.md:45 — script path and flags; WP-CLI subcommands (cache type, doctor, profile) taken from the official skill references, not run here -->
