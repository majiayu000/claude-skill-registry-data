---
name: superpowers-sage:acorn-redis
description: >
  Redis caching, sessions, and queue driver in WordPress via Acorn — lando redis-cli,
  Cache::remember(), Cache::tags(), cache invalidation, WP object cache drop-in,
  wp_cache_set, wp_cache_get, Redis facade, session driver redis, REDIS_HOST,
  REDIS_PORT, Lando Redis service, predis, phpredis, queue connection redis,
  cache tags group invalidation, WP transient replacement, cache hit rate,
  lando wp cache type, object-cache.php drop-in
user-invocable: false
---

# Redis with Acorn in WordPress

## When to use

- Object cache for WordPress (`wp_cache_*`) backed by Redis instead of ephemeral in-process cache
- Laravel cache / session / queue driver inside theme code
- Cross-request rate limiting, lock coordination, or atomic counters
- High-traffic sites where `wp_options` autoload pressure needs relief
- Queue backend for `acorn-queues` when jobs need durable storage beyond sync driver

## When NOT to use

- Small dev-only sites with no performance pressure — array/file cache is fine
- Shared hosting without Redis — use `file` or `database` cache driver instead
- As a database — Redis is cache; persistent data belongs in MySQL
- When `wp_cache_*` calls are rare and localized — flushing coordination overhead may exceed benefit

## Prerequisites

- Lando config includes a `redis` service (setup shown below)
- `predis/predis` or phpredis extension available
- `wp-redis` or `object-cache.php` drop-in installed for WordPress object cache integration
- `REDIS_HOST` / `REDIS_PORT` set in `.env`

## Redis in the Stack

Lando provides Redis as a service. Acorn connects to it through Laravel's Redis integration (`illuminate/redis`). Three primary uses:

- **Cache driver** — store computed values, query results, rendered partials
- **Session driver** — user sessions backed by Redis instead of filesystem
- **Queue driver** — background job processing (see `sage:acorn-queues`)

See [`references/cache-config.md`](references/cache-config.md) for full Lando service config, `config/cache.php`, and `Cache::remember()` patterns.
See [`references/cache-tags.md`](references/cache-tags.md) for tag-based invalidation with `save_post` and `edited_term`.
See [`references/session-queue.md`](references/session-queue.md) for session driver and queue connection wiring.
See [`references/troubleshooting.md`](references/troubleshooting.md) for connection refused, drop-in not installed, cache not persisting, session issues.

Scripts: [`scripts/redis-health.sh`](scripts/redis-health.sh)

## WordPress Object Cache

Acorn's `Cache` facade and WordPress's object cache (`wp_cache_get`, `wp_cache_set`) are separate layers.

For WordPress core and plugins to use Redis, install an object cache drop-in:

- **`wp-redis`** — adds `object-cache.php` drop-in to `wp-content/`
- **`redis-cache`** — popular alternative with admin UI

This is independent of Acorn. Both can coexist pointing at the same Redis instance on different databases.

```env
# For wp-redis (in .env or wp-config.php)
WP_REDIS_HOST=cache
WP_REDIS_PORT=6379
WP_REDIS_DATABASE=2
```

Use database `2` to isolate WordPress object cache from Acorn cache (`1`) and sessions (`0`).

## Direct Redis Usage

When the Cache facade abstractions are not enough — pub/sub, Lua scripts, atomic pipelines:

```php
use Illuminate\Support\Facades\Redis;

// Direct key operations
Redis::set('lock:import', 'running', 'EX', 300);
$status = Redis::get('lock:import');
Redis::del('lock:import');

// Pipeline for batch operations
Redis::pipeline(function ($pipe): void {
    for ($i = 0; $i < 100; $i++) {
        $pipe->set("batch:{$i}", "value-{$i}");
    }
});

// Pub/sub (useful for inter-process signaling)
Redis::publish('cache-cleared', json_encode(['by' => 'deploy']));
```

Prefer the `Cache` facade for standard get/set/remember. Use `Redis` directly only for operations the Cache API does not support.

## Lando Redis CLI

```bash
# Open interactive Redis CLI
lando redis-cli -h cache

# Watch all commands in real time (useful for debugging cache hits/misses)
lando redis-cli -h cache MONITOR

# List all keys (dev only — never in production)
lando redis-cli -h cache KEYS '*'

# Inspect a key's TTL
lando redis-cli -h cache TTL "sage_cache:homepage:featured"

# Flush a specific database
lando redis-cli -h cache -n 1 FLUSHDB

# Check memory usage
lando redis-cli -h cache INFO memory
```

## Verification

- Run `lando redis-cli -h cache PING` and confirm it returns `PONG` -- this verifies the Redis service is running and accessible.
- Test cache operations by setting and retrieving a value: `Cache::put('test', 'hello', 60)` then `Cache::get('test')` should return `'hello'`.
- Run `lando redis-cli -h cache INFO memory` to confirm Redis is accepting connections and check memory usage.

## Failure modes

### Problem: Connection refused (Redis not running)
- **Cause:** The Redis service in Lando is not started, or the `REDIS_HOST` in `.env` does not match the Lando service name.
- **Fix:** Run `lando restart` to restart all services including Redis. Verify `.env` has `REDIS_HOST=cache` (matching the service name in `.lando.yml`). Check that `.lando.yml` includes a `cache` service with `type: redis`. Run `lando info` to confirm the Redis service is listed and running.

### Problem: Serialization errors when caching objects
- **Cause:** The value being cached contains non-serializable data (closures, resource handles, `WP_Query` objects with database connections).
- **Fix:** Cache only scalar values, arrays, or objects that implement `Serializable` / `JsonSerializable`. Extract the needed data from complex objects into a plain array before caching. Use `Cache::remember()` with a closure that returns clean data.

## Escalation

- If the Redis service will not start at all (exits immediately or crashes), this is an infrastructure issue -- check `lando logs -s cache` for error output, verify Lando and Docker are running correctly, and try `lando rebuild`.
- If Redis is running but queue jobs are failing, consult the `sage:acorn-queues` skill for queue driver configuration and failed job troubleshooting.
