---
name: superpowers-sage:wp-performance
description: >
  WordPress performance optimization: performance, slow query, N+1 query, Query Monitor,
  autoload audit, autoload options, object cache, Redis, wp_cache, transient, cache invalidation,
  Core Web Vitals, LCP, CLS, INP, FID, profiling, Xdebug, microtime, pre_get_posts,
  database query optimization, TTFB, page load, Vite bundle, lazy loading, critical CSS —
  benchmark before/after, never optimize blind.
  Invoke for: slow page load, N+1 query problem, caching strategy, transient API,
  dequeue unused scripts, performance profiling, Core Web Vitals improvement.
user-invocable: false
---

# WordPress Performance Optimization

## When to Use

- Page load times are slow or degrading
- Core Web Vitals scores are poor (LCP > 2.5s, INP > 200ms, CLS > 0.1)
- Database queries are excessive or slow (QM shows > 50 queries or queries > 50ms)
- Object cache hit rates are low (< 90%)
- Autoloaded options table is bloated (> 500KB total)
- N+1 query patterns detected in Eloquent models
- Hook execution is slow or excessive
- REST API responses are slow

## Scripts

```bash
# Dump Query Monitor data (pass optional URL, defaults to <dirname>.lndo.site)
bash skills/wp-performance/scripts/query-monitor-dump.sh
bash skills/wp-performance/scripts/query-monitor-dump.sh https://mysite.lndo.site

# Audit autoloaded options (sorted by size, top 20)
bash skills/wp-performance/scripts/autoload-audit.sh
```

Scripts: [`scripts/query-monitor-dump.sh`](scripts/query-monitor-dump.sh) · [`scripts/autoload-audit.sh`](scripts/autoload-audit.sh)

---

## Procedure

### Step 1 — Install Query Monitor

**Always profile before optimizing. Never optimize blind.**

```bash
lando wp plugin install query-monitor --activate
```

If the `db.php` symlink fails (permissions):

```bash
lando ssh -c "ln -sf /app/wp/wp-content/plugins/query-monitor/wp-content/db.php /app/wp/wp-content/db.php"
```

Key constants (Bedrock `config/application.php`):

```php
Config::define('QM_DB_EXPENSIVE', 0.05);   // seconds threshold for slow queries
Config::define('QM_ENABLE_CAPS_PANEL', true);
```

See [`references/query-monitor.md`](references/query-monitor.md) for all panels,
QM timers, custom logging, and how to export data as JSON.

---

### Step 2 — Identify the Bottleneck

Follow this isolation sequence:

1. **Bootstrap** — plugins_loaded, Acorn boot, autoloaded options
2. **Main query** — WP_Query execution time, parameter validation
3. **Template rendering** — Blade, view composers, ACF block `with()` queries
4. **Frontend** — Vite bundle size, image loading, paint timing

QM toolbar shows: page generation time, peak memory, SQL duration, query count.

---

### Step 3 — Fix the Top Issues

#### N+1 Queries (most common)

Enable lazy loading prevention in development:

```php
// app/Providers/AppServiceProvider.php
Model::preventLazyLoading(! app()->isProduction());
```

Fix with eager loading:

```php
// Bad (N+1)
$posts = Post::all();
foreach ($posts as $post) { echo $post->author->name; }

// Good (2 queries total)
$posts = Post::with('author')->get();
```

For native WP meta loops:

```php
update_post_meta_cache($postIds);  // batch-load all meta in one query
foreach ($postIds as $id) {
    $price = get_post_meta($id, 'price', true);  // served from cache
}
```

See [`references/n-plus-one.md`](references/n-plus-one.md) for IN query batching,
ACF block patterns, and full detection workflow.

#### Autoloaded Options Bloat

```bash
bash skills/wp-performance/scripts/autoload-audit.sh
```

Fix oversized options:

```bash
lando wp option update <option_name> --autoload=no
```

Target: total autoloaded size < 500KB.

See [`references/autoload.md`](references/autoload.md) for audit workflow, common plugin culprits, and when to set `autoload=no`.

#### Object Cache / Redis

```bash
lando redis-cli ping   # → PONG
```

Monitor hit rates in QM's Object Cache panel. Target: > 90%.

```php
$posts = wp_cache_get("category-posts-{$id}", 'my-plugin');
if (false === $posts) {
    $posts = get_posts(['category' => $id, 'posts_per_page' => 10]);
    wp_cache_set("category-posts-{$id}", $posts, 'my-plugin', HOUR_IN_SECONDS);
}
```

**Every cache write requires a documented invalidation strategy.** Bust on `save_post`,
`edited_term`, or the relevant update hook.

See [`references/caching.md`](references/caching.md) for transients, `Cache::remember()`,
full-page caching, and group invalidation.

#### Database Query Optimization

- Add indexes for columns in `WHERE`, `ORDER BY`, `JOIN`
- Always use `$wpdb->prepare()` for raw queries
- Avoid `SELECT *` — specify columns
- Use Eloquent query scopes to encapsulate reusable logic
- `$wpdb->show_errors()` in development only — never in production

#### Vite Bundle Size

```bash
lando theme-build -- --analyze   # open bundle analyser
```

- Dynamic imports: `const m = await import('./heavy-module.js')`
- Split large vendor libraries via `manualChunks` in `vite.config.js`
- Target: no single chunk > 200KB gzipped

#### Core Web Vitals

| Metric | Target | Common Sage causes |
|---|---|---|
| **LCP** | < 2.5s | Large hero image, render-blocking CSS, slow TTFB |
| **INP** | < 200ms | Heavy JS bundle, long main-thread tasks, Livewire hydration |
| **CLS** | < 0.1 | Images without dimensions, dynamically injected content |

Always declare `width` and `height` on images. Preload the LCP image:

```html
<link rel="preload" as="image" href="{{ $heroImageUrl }}" fetchpriority="high">
```

See [`references/core-web-vitals.md`](references/core-web-vitals.md) for full LCP/INP/CLS
remediation, critical CSS with Vite, and third-party script strategies.

---

### Step 4 — Deep Profiling (if bottleneck unclear)

Use QM timers for targeted code sections:

```php
do_action('qm/start', 'my-operation');
$result = $this->expensiveComputation();
do_action('qm/stop', 'my-operation');
```

For call-graph analysis, use Xdebug profiler in Lando:

```yaml
# .lando.yml
services:
  appserver:
    xdebug: profile
```

Trigger: append `?XDEBUG_PROFILE=1` to the URL.

See [`references/profiling.md`](references/profiling.md) for Xdebug setup,
`microtime()` patterns, and WP hook profiling (`pre_get_posts`, `save_post`).

---

## Cron: Action Scheduler vs wp-cron

- **wp-cron**: triggered by page visits, unreliable under low traffic
- **Action Scheduler**: queue-based, retries, logging, concurrent processing
- Development: `lando wp cron event run --due-now`
- Production: disable wp-cron (`DISABLE_WP_CRON=true`) and use real system cron

---

## Critical Rules

1. **Check Query Monitor before optimizing.** Profile first — never optimize blind.
2. **Benchmark before and after every change.** Record QM query count, page time,
   and memory before the fix; verify improvement after.
3. **`$wpdb->show_errors()` only in development.** Never leave error display enabled
   in staging or production — it leaks sensitive schema information.
4. **Every cache write requires an invalidation strategy.** Document the hook and
   timing for every `wp_cache_set`, `set_transient`, or `Cache::remember()`.
5. **Do not use `$wpdb->show_errors()` in production.** Use QM logging instead.

---

## Verification

- [ ] QM shows no duplicate queries and no queries > 50ms
- [ ] Autoloaded options total size < 500KB
- [ ] No N+1 patterns (`Model::preventLazyLoading()` throws no exceptions)
- [ ] Redis object cache hit rate > 90%
- [ ] Core Web Vitals pass: LCP < 2.5s, INP < 200ms, CLS < 0.1
- [ ] Page load time improved from baseline measurement
- [ ] Vite bundle sizes reasonable (no single chunk > 200KB gzipped)
- [ ] QM PHP Errors panel clean — no warnings or deprecations from theme
- [ ] QM HTTP API Calls panel shows no timeouts or errors

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| TTFB > 1s | No object cache or slow queries | Enable Redis; audit autoloaded options |
| Query count > 50 per page | N+1 or missing eager loading | `->with()`, `update_post_meta_cache()` |
| LCP > 4s | Large unoptimized hero image | Compress, WebP, preload hint |
| CLS > 0.25 | Images without explicit dimensions | Add `width`/`height` |
| Redis connection refused | Redis not running in Lando | Check `.lando.yml`, `lando rebuild` |
| Object cache not working | Drop-in not installed | Cross-ref acorn-redis skill |
| Stale cached data | No invalidation on update | Add `wp_cache_delete` to save hooks |
| QM toolbar not visible | Not logged in as admin | Set QM auth cookie via Settings |
| QM db.php symlink missing | Permissions issue | Manually symlink (see Step 1) |
| QM panels empty | `QM_DISABLED` is true | Check `config/application.php` constants |
| Slow hooks detected | Expensive callbacks on frequent hooks | Queue async; use QM timers to measure |

### Escalation

- Performance issues persist after all fixes → profile with Xdebug or Blackfire
- Database bottlenecks beyond query optimization → DBA for schema/read replica
- CWV blocked by third-party scripts → document constraint, escalate to project lead
- Infrastructure-level issues (server response time, CDN) → hosting/DevOps
