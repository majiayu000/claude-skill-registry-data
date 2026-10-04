---
name: orbit-db-profile
description: Database query profiling for a WordPress plugin — query count per page, slow queries (>100ms), N+1 detection, autoload bloat (`wp_options` autoload size), transient explosion, missing indexes, and cron-induced churn. Uses Query Monitor + MySQL `performance_schema` against a wp-env site. Use when the user says "DB profile", "query count", "N+1", "slow query", "autoload bloat", "Query Monitor", or after any feature that adds DB writes/reads.
---

# 🪐 orbit-db-profile — Query profiling

The DB layer most plugins ignore. 67 queries on the homepage isn't unusual — it's just preventable.

---

## Quick start

```bash
# Default — profiles the homepage on wp-env port 8881
bash ~/Claude/orbit/scripts/db-profile.sh

# Custom URL list
WP_TEST_URL="http://localhost:8881" \
TEST_PAGES="/,/sample-page/,/wp-admin/admin.php?page=my-plugin" \
  bash scripts/db-profile.sh
```

Or via gauntlet (Step 8):
```bash
bash scripts/gauntlet.sh --plugin . --mode full
```

Output: `reports/db-profile-<timestamp>.txt`.

---

## What it measures

| Metric | Target | Bad |
|---|---|---|
| Queries per frontend page | < 30 | > 60 |
| Queries per admin page | < 50 | > 100 |
| Slow queries (>100ms) | 0 | any |
| Slowest single query | < 50ms | > 200ms |
| Autoload size (wp_options) | < 1MB | > 4MB |
| N+1 patterns | 0 | any |
| Cron tasks running on every request | 0 | > 0 |
| Transients written per request | < 5 | > 20 |

Each is a release-blocker if exceeded.

---

## How it works

1. Activate Query Monitor in wp-env
2. Visit each URL via headless Chrome (Playwright)
3. Read the QM panel output via WP-CLI
4. Parse + rank queries
5. Cross-reference against `performance_schema.events_statements_summary_by_digest` for slow-query stats

---

## Common findings + fixes

### N+1 queries
```php
// BAD — 1 query for posts, then 1 query per post for meta
$posts = get_posts(['post_type' => 'product']);
foreach ($posts as $p) {
  $price = get_post_meta($p->ID, '_price', true);   // ← N+1
}

// GOOD — single batched meta query
$posts = get_posts([
  'post_type' => 'product',
  'fields' => 'ids',
]);
$prices = $wpdb->get_results(
  "SELECT post_id, meta_value FROM {$wpdb->postmeta} WHERE meta_key='_price' AND post_id IN (" .
  implode(',', array_map('intval', $posts)) . ")",
  OBJECT_K
);
```

Or use `update_postmeta_cache($posts)` + `get_post_meta()` — it primes the cache.

### Autoload bloat
```bash
# Check what's autoloaded
wp-env run cli wp db query \
  "SELECT option_name, LENGTH(option_value) AS size
   FROM wp_options WHERE autoload='yes' ORDER BY size DESC LIMIT 20"

# Plugins commonly bloat this with: full settings JSON, log arrays, cache data
```

```php
// BAD
add_option('my_plugin_huge_log', $bigArray);  // autoloaded by default

// GOOD
add_option('my_plugin_huge_log', $bigArray, '', 'no');  // explicit no-autoload
// Or use a transient for cache data
set_transient('my_plugin_cache', $cache, HOUR_IN_SECONDS);
```

### Slow query (>100ms)
```php
// BAD — full-table scan
$wpdb->get_results("SELECT * FROM {$wpdb->prefix}myplugin_log WHERE message LIKE '%error%'");

// GOOD — add an index
// In activation hook:
$wpdb->query("CREATE INDEX idx_message ON {$wpdb->prefix}myplugin_log (message(50))");
```

### Cron storm
```php
// BAD — schedules a task on every page load
add_action('init', function() {
  if (!wp_next_scheduled('my_task')) wp_schedule_event(time(), 'hourly', 'my_task');
});
// Logic looks idempotent but `wp_next_scheduled` itself queries the DB

// GOOD — schedule once, on activation
register_activation_hook(__FILE__, function() {
  if (!wp_next_scheduled('my_task')) wp_schedule_event(time(), 'hourly', 'my_task');
});
```

### Transient flood
```php
// BAD — write a transient per item
foreach ($items as $i) set_transient("my_plugin_item_$i->id", $i->data, HOUR_IN_SECONDS);

// GOOD — one transient with the whole array
set_transient('my_plugin_items', $items, HOUR_IN_SECONDS);
```

---

## Read the report

```
[DB Profile] Page: /sample-page/

  Queries:    47   (target: < 30)        ⚠
  Slow:       1    (target: 0)           ❌
  Slowest:    240ms — SELECT * FROM wp_postmeta WHERE meta_key='_price'
  Autoload:   3.2MB                      ⚠
  N+1:        2 patterns detected        ❌
  Cron now:   0
  Transients: 4

❌ N+1 #1: 25 queries to wp_postmeta with consecutive post_ids
   → Source: includes/class-product-list.php:42
   → Fix: use update_postmeta_cache() or batched IN query

❌ Slow query: SELECT * FROM wp_postmeta WHERE meta_key='_price' (240ms)
   → 14,000 rows, no index on meta_key
   → Fix: add (post_id, meta_key) compound index — WP doesn't add this by default
```

---

## Performance schema deep-dive

```bash
wp-env run cli wp db query \
  "SELECT digest_text, count_star, sum_timer_wait/1e9 AS sum_ms, avg_timer_wait/1e9 AS avg_ms
   FROM performance_schema.events_statements_summary_by_digest
   ORDER BY sum_timer_wait DESC LIMIT 20"
```

Shows: which query patterns ran most, how many times, total time spent. Identifies **hot queries** that aren't slow individually but eat budget cumulatively.

---

## When to run

| Trigger | Run? |
|---|---|
| New feature with DB writes | ✅ Yes |
| Refactor of `WP_Query` / `$wpdb` | ✅ Yes |
| Before any release | ✅ Yes (auto via `--mode full`) |
| User reports "site slow on plugin install" | ✅ Yes — start here |

---

## Pair with `/orbit-wp-database`

This skill **measures** runtime DB behaviour. `/orbit-wp-database` **reviews code** for DB anti-patterns. Run both — the measure tells you "you have N+1", the code review tells you "in this file at this line".
