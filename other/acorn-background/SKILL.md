---
name: acorn-background
description: Use when work must run outside the request, on a schedule, or be logged in an Acorn project - WP-Cron vs Action Scheduler vs Laravel queues (make:job, ShouldQueue, queue:work, failed_jobs), console commands (make:command, wp acorn <command>), Schedule::command and schedule:run from system cron, Laravel Redis and Cache vs transients, logging channels (Log::, LOG_CHANNEL, stderr, storage/logs). For tables use acorn-data; for object cache tuning use wp-performance.
---

# Background work, cache and logs under Acorn

Acorn brings Laravel's queue, cache, Redis, console, scheduler and log components into WordPress. WordPress already has its own scheduler (WP-Cron), object cache and debug log. Pick the native piece first and add the Laravel piece only for a real gap.

Runner placeholders (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.composer}}`, `{{runner.test}}`, `{{runner.cache}}`) come from the session context; on Lando they default to `lando wp`, `lando wp acorn`, `lando composer`, the project's test tooling and its cache-clear tooling. Redis tooling and service names come from `.lando.yml` (read them, do not assume `cache` or `redis`).

## When to use

- Something slow or unreliable runs inside a request (external API call, email, image work, CRM sync).
- A recurring task (nightly cleanup, hourly sync), or a CLI command for maintenance and imports.
- Configuring Redis or the Laravel cache, or untangling it from the WordPress object cache.
- Adding a log channel, finding where logs go, or shipping logs from containers.

## Inputs required

1. Active profile, Acorn base path and namespace (session context).
2. Installed pieces: `illuminate/redis` and the PHP `redis` extension (or `predis/predis`), Action Scheduler (a plugin or `woocommerce/action-scheduler`), the WordPress Redis drop-in (`wp-content/object-cache.php`).
3. Config actually in effect: `config/queue.php`, `config/cache.php`, `config/database.php` (`redis`), `config/logging.php` in the base path, merged over Acorn's defaults.
4. Hosting: can the project run a long-lived worker (container, supervisor, systemd)? Is there a system cron? How many web instances?

### Decide the mechanism

| Need | Native first | Laravel piece when |
|---|---|---|
| Run a hook at an interval, low volume, retry not critical | WP-Cron: `wp_schedule_event()` (`wp-includes/cron.php`), triggered by traffic unless `DISABLE_WP_CRON` is set and a system cron calls `{{runner.wp}} cron event run --due-now` | — |
| Many deferred actions with per-action logs and admin UI, no worker process | Action Scheduler (`as_enqueue_async_action`, `as_schedule_single_action`, `as_schedule_recurring_action`; runs on WP-Cron) when it is already installed | — |
| Retries with backoff, timeouts, unique jobs, batches, chaining, high volume | — | Laravel queue + worker (`queue:work`) |
| Recurring Laravel commands with overlap control | WP-Cron calling a service | Scheduler (`schedule:run` every minute from system cron) |
| Cache a computed value | Transients / `wp_cache_*` (persistent when an object-cache drop-in is installed) | Laravel `Cache` for tags, locks, `remember`, or a store separate from WordPress |
| Operator command | `WP_CLI::add_command()` | Acorn command for DI, Laravel console IO, scheduling |
| Debug output | `WP_DEBUG_LOG` → `debug.log` | Laravel `Log` channels, structured context, stderr in containers |

Details and trade-offs: [references/decision-matrix.md](references/decision-matrix.md).

### Profile differences

| Item | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Jobs, commands | `app/Jobs`, `app/Console/Commands` in the theme | same folders in the plugin, plugin namespace | same folders at the root |
| `routes/console.php` | theme base path | plugin base path | project root |
| Config overrides | `config/*.php` in the theme | `config/*.php` in the plugin | `config/*.php` at the root |
| Storage (logs, file cache) | `storage/` in the theme if present, else `wp-content/cache/acorn` | `storage/` in the plugin if present, else the same fallback | `storage/` at the root |
| Worker command runs from | the site root through WP-CLI, theme active | the site root through WP-CLI (mu-plugins always load) | the project root through WP-CLI |

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`php`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run in CI or a deploy script go in a separate block labelled with where they run.

1. **Name the need and pick the mechanism** with the table. Write the reason when you choose a Laravel piece over a native one.
2. **Laravel queue** ([references/queues.md](references/queues.md)):
   - `QUEUE_CONNECTION` defaults to `sync` (runs inline, nothing is deferred). Choose `database` or `redis` per environment.
   - Database driver: `{{runner.acorn}} make:queue-table`, `make:queue-failed-table` (and `make:queue-batches-table` for batches), then `{{runner.acorn}} migrate`. Tables get the WordPress prefix.
   - `{{runner.acorn}} make:job SyncLead`; pass IDs, not objects; set `$tries`, `$backoff`, `$timeout`; make `handle()` idempotent; call `wp_set_current_user()` when capability checks run inside the job.
   - Dispatch from the WordPress hook or controller: `SyncLead::dispatch($leadId)`.
   - Run a worker: `{{runner.acorn}} queue:work --tries=3 --max-time=3600`. In production keep it alive with the platform's process manager and run `{{runner.acorn}} queue:restart` after every deploy.
3. **Commands and schedule** ([references/commands-scheduling.md](references/commands-scheduling.md)):
   - `{{runner.acorn}} make:command ImportLeads` → `app/Console/Commands`, loaded automatically; run as `{{runner.acorn}} leads:import`.
   - Schedule in `routes/console.php` (`Schedule::command('leads:import')->hourly()->withoutOverlapping()`) or with `->withSchedule(fn (Schedule $s) => …)` on the builder.
   - Trigger it every minute from a system cron: `{{runner.acorn}} schedule:run` (on a server without the local runner, the same command through that environment's WP-CLI, from the WordPress root), or keep `{{runner.acorn}} schedule:work` running.
4. **Redis and cache** ([references/redis-cache.md](references/redis-cache.md)):
   - `{{runner.composer}} require illuminate/redis` in the base path (Acorn does not require it; its provider is skipped while the class is missing) plus the `redis` PHP extension or `predis/predis`.
   - Give Laravel its own Redis databases or key prefix. The Redis Object Cache drop-in defaults to database 0 and `{{runner.wp}} cache flush` runs `FLUSHDB` on it; Acorn's Redis `default` connection is also database 0 (`REDIS_DB`), cache database 1 (`REDIS_CACHE_DB`). Put queues and sessions elsewhere, for example `REDIS_DB=2`, `REDIS_CACHE_DB=3`.
   - `{{runner.acorn}} cache:clear` empties the Laravel cache store only; `{{runner.wp}} cache flush` empties the WordPress object cache only.
5. **Logging** ([references/logging.md](references/logging.md)):
   - Default: channel `stack` → `single` → `storage/logs/laravel.log` under the app's storage path.
   - Containers: `LOG_CHANNEL=stderr` (or add `stderr` to `LOG_STACK`) so the platform collects logs.
   - A project `config/logging.php` only needs the channels it adds; Laravel merges `channels` with Acorn's defaults.
   - Always log with a context array, never secrets or full personal data.
6. **Clear caches** after PHP changes: `{{runner.cache}}`.

## Verification

- Queue: dispatch one job, then `{{runner.acorn}} queue:work --once` processes it; `{{runner.acorn}} queue:failed` is empty; with the database driver, the `jobs` table drains.
- Schedule: `{{runner.acorn}} schedule:list` shows each task with its next run; `{{runner.acorn}} schedule:test` runs one on demand.
- Commands: `{{runner.acorn}} list` shows the command; `{{runner.acorn}} help <name>` matches the signature.
- Redis: `{{runner.wp}} eval 'var_dump(app("redis")->connection()->ping());'` succeeds; `{{runner.wp}} eval 'var_dump(config("database.redis.default.database"), config("database.redis.cache.database"));'` shows databases that differ from the object cache's.
- Logs: `{{runner.wp}} eval 'logger("kivo-check", ["ok" => true]);'` writes to the expected file or stream.
- WP-Cron: `{{runner.wp}} cron event list` shows the hook and next run.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Jobs "dispatch" but run during the request | `QUEUE_CONNECTION` is `sync` (default) | Set `database` or `redis` and run a worker |
| Jobs pile up, never processed | No worker running, or the worker listens to another queue/connection | Start `queue:work` with matching `--queue`; supervise it |
| Worker runs old code after a deploy | Long-running process keeps the old classes | `{{runner.acorn}} queue:restart` (needs a cache store shared by worker and deploy) |
| Jobs behave as logged out or use stale WordPress state | Workers run in one long WP-CLI process; no request user, globals persist between jobs | `wp_set_current_user()` in `handle()`; avoid globals; `--max-jobs` / `--max-time` |
| `Class "Redis" not found` / `redis` binding missing | No `redis` extension, or `illuminate/redis` not installed so its provider was skipped | Install the extension or `predis/predis` (`REDIS_CLIENT=predis`); require `illuminate/redis` |
| Sessions, locks or queued jobs vanish after a deploy | `{{runner.wp}} cache flush` ran `FLUSHDB` on the database Laravel also uses | Separate databases (`REDIS_DB`, `REDIS_CACHE_DB`) or `WP_REDIS_SELECTIVE_FLUSH` with a prefix |
| Scheduled tasks never run | No system cron calling `schedule:run`, or it runs outside the site root | Add the cron entry; run through WP-CLI from the WordPress root |
| `onOneServer()` / `withoutOverlapping()` still overlap across servers | Cache store is per server (file) | Use Redis or database as the cache and lock store |
| WP-Cron events late or never | Low traffic, or `DISABLE_WP_CRON` without a system cron | System cron with `{{runner.wp}} cron event run --due-now` |
| No log file appears | Storage folder missing or not writable, or `LOG_CHANNEL` points to a stream | Check the storage path per profile; `stderr` output is in the container log |
| Command missing from `list` | Not under `app/Console/Commands` of the base path, or namespace mismatch with `composer.json` PSR-4 | Move it, fix the namespace, or register with `->withCommands([...])` |

## Escalation

- Adding a worker process, a cron entry, or Redis to an environment is infrastructure work: describe what is needed and ask.
- Purging queues (`queue:clear`, `queue:flush`), flushing shared caches, or changing Redis databases on a shared environment: ask first.
- Tables behind jobs or schedules: `acorn-data`. HTTP entry points that dispatch jobs: `acorn-routes-api`.

<!-- verified:
vendor/roots/acorn/config/queue.php — default QUEUE_CONNECTION 'sync'; database/redis connections; failed driver database-uuids table failed_jobs on DB_CONNECTION 'wordpress'
vendor/roots/acorn/src/Roots/Acorn/Console/Kernel.php:84-138 queue, schedule, make:job/command commands; :176-182 loads app/Console/Commands and base_path('routes/console.php')
vendor/roots/acorn/src/Illuminate/Foundation/Configuration/ApplicationBuilder.php:334-349 withCommands(); :375-383 withSchedule()
vendor/illuminate/queue/Console/TableCommand.php:10, FailedTableCommand.php:10, BatchesTableCommand.php:10 — make:queue-*-table names with queue:* aliases
vendor/roots/acorn/composer.json:44-69 — no illuminate/redis; illuminate/support/DefaultProviders.php:41 lists RedisServiceProvider; roots/acorn Application.php:328 filters providers by class_exists
vendor/roots/acorn/config/database.php:165-194 — redis client phpredis, default DB REDIS_DB 0, cache DB REDIS_CACHE_DB 1
wp-content/plugins/redis-cache/includes/object-cache.php:626 default database 0; :1633-1669 flush() runs FLUSHDB unless WP_REDIS_SELECTIVE_FLUSH with a prefix (Redis Object Cache 2.7.0)
vendor/roots/acorn/config/cache.php — default store 'file' at storage/framework/cache/data; redis store uses 'cache' connection
vendor/roots/acorn/config/logging.php:21 default 'stack'; stack -> LOG_STACK 'single'; single path storage/logs/laravel.log; stderr channel present
vendor/roots/acorn/src/Illuminate/Foundation/Bootstrap/LoadConfiguration.php — logging.channels, queue.connections, cache.stores, database.connections merged over Acorn defaults
vendor/roots/acorn/src/Roots/Acorn/Configuration/Concerns/Paths.php:115-128 — storage fallback WP_CONTENT_DIR/cache/acorn with logs/
wp/wp-includes/cron.php:48 wp_schedule_single_event, :252 wp_schedule_event, :1020-1051 wp_cron and DISABLE_WP_CRON
roots-docs acorn queues, redis, cache, logging, wp-cli and artisan-console pages
-->
