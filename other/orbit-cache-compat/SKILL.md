---
name: orbit-cache-compat
description: Verify WordPress plugin compatibility with object cache (Redis / Memcached) and page cache (W3 Total Cache, WP Rocket, LiteSpeed, Varnish). Catches plugins that store mutable data in transients without invalidation, set cookies that bust page cache for everyone, or read from `wp_options` without honouring `wp_cache_get`. Use when the user says "object cache", "Redis", "page cache", "WP Rocket", "LiteSpeed", "cache compat".
---

# 🪐 orbit-cache-compat — Cache layer compatibility

WP plugins that misuse caching are responsible for half of the "site slow" support tickets. This skill catches incompatibilities before they hit the user.

---

## Quick start

```bash
bash ~/Claude/orbit/scripts/check-object-cache.sh ~/plugins/my-plugin
```

Plus a live test against an object-cache-enabled wp-env site:
```bash
# Spin up wp-env with Redis
bash scripts/create-test-site.sh --plugin . --port 8881 --object-cache redis

# Run gauntlet — DB-profile step now reflects cached vs uncached
bash scripts/gauntlet.sh --plugin . --mode full
```

---

## What this skill checks

### 1. Object cache awareness

```php
// ❌ Bypass object cache — slow on Redis/Memcached sites
$value = $wpdb->get_var( "SELECT meta_value FROM wp_options WHERE option_name='my_plugin_data'" );

// ✅ Use WP API — automatically uses object cache if available
$value = get_option( 'my_plugin_data' );

// ❌ Reading user meta directly
$value = $wpdb->get_var( $wpdb->prepare(
  "SELECT meta_value FROM wp_usermeta WHERE user_id=%d AND meta_key=%s", $u, 'my_meta'
) );

// ✅ Use the API
$value = get_user_meta( $u, 'my_meta', true );
```

### 2. Cache invalidation on writes

```php
// ❌ Reading from transient, writing to DB directly — cache stale
function get_thing() {
  $cached = get_transient( 'my_thing' );
  if ( $cached !== false ) return $cached;
  $val = $wpdb->get_var( "..." );
  set_transient( 'my_thing', $val, HOUR_IN_SECONDS );
  return $val;
}

function update_thing( $val ) {
  $wpdb->update( "...", [...] );
  // BUG: cached value is now stale until transient expires
}

// ✅ Invalidate the cache on every write
function update_thing( $val ) {
  $wpdb->update( "...", [...] );
  delete_transient( 'my_thing' );
}
```

### 3. Page-cache busting cookies

```php
// ❌ Setting a unique cookie per visitor on EVERY request
// → kills page cache because each visitor gets a unique cache key
setcookie( 'my_plugin_visitor_id', wp_generate_uuid4(), time() + YEAR_IN_SECONDS, '/' );

// ✅ Set the cookie only once, conditionally
if ( ! isset( $_COOKIE['my_plugin_visitor_id'] ) ) {
  setcookie( 'my_plugin_visitor_id', wp_generate_uuid4(), ... );
}

// ✅ Or skip the cookie for cached requests
if ( defined( 'WP_CACHE' ) && WP_CACHE ) return;
```

### 4. `nocache_headers()` overuse

```php
// ❌ Disables page cache for the whole site
function my_plugin_init() {
  nocache_headers();  // Sends Cache-Control: no-cache for every page
}
add_action( 'init', 'my_plugin_init' );

// ✅ Only disable for specific contexts (admin AJAX, REST endpoints)
add_action( 'wp_ajax_my_action', function() {
  nocache_headers();
  // ...
} );
```

### 5. Transient explosion

```php
// ❌ Per-user, per-key transients — millions on a busy site
foreach ( $items as $i ) set_transient( "my_plugin_$user_id_$i", ..., HOUR_IN_SECONDS );

// ✅ Aggregate
set_transient( "my_plugin_user_$user_id", $items, HOUR_IN_SECONDS );
```

Each transient is 2 rows in `wp_options` (value + timeout). 100 transients per user × 1000 users = 200,000 rows. DB death by a thousand cuts.

### 6. Object cache key collisions

```php
// ❌ Generic key — collides with other plugins
wp_cache_set( 'data', $val );

// ✅ Always namespace
wp_cache_set( 'my_plugin_data', $val, 'my-plugin-group' );
// ↑ key is namespaced + uses a group for easier flush
```

### 7. Honour `WP_CACHE` constant

```php
// ❌ Always store in transient, even when caching is disabled
set_transient( 'my_data', $val, HOUR_IN_SECONDS );

// ✅
if ( defined( 'WP_CACHE' ) && WP_CACHE ) {
  set_transient( 'my_data', $val, HOUR_IN_SECONDS );
} else {
  // skip cache layer in dev or test
}
```

---

## Page-cache plugin compat

### W3 Total Cache
- Plugins setting `nocache_headers()` get bypassed (correct)
- Plugins writing custom session cookies → must declare them in W3TC's "session cookies" config

### WP Rocket
- Reads `Cache-Control` headers
- Aborts cache for `?` query strings unless explicitly allowed
- DONOTCACHEPAGE constant respected

### LiteSpeed Cache
- Has its own ESI integration — block-level cache exclusion possible
- Plugins can hook `litespeed_excluded_url` filter

### Varnish (server-level)
- Doesn't see WP at all — pure HTTP-level caching
- Cookies starting with `wp_` or `wordpress_` bust the cache automatically (correct)
- Custom plugin cookies break this without `vcl` config

Recommend: provide a **DOCS section** for users on integrating with their cache plugin.

---

## Test on object cache

```bash
# Enable Redis in wp-env
echo '{"WP_CACHE": true, "WP_REDIS_HOST": "redis"}' > .wp-env-overrides.json
wp-env destroy && wp-env start

# Verify cache is active
wp-env run cli wp redis status

# Now run gauntlet — DB profile shows cached vs uncached query counts
bash scripts/gauntlet.sh --plugin . --mode full
```

Expected: query counts drop dramatically with object cache. If they don't, your plugin isn't using `get_option` / `get_transient` — it's hitting the DB directly.

---

## Output

```markdown
# Cache Compat — my-plugin

## Object cache compatibility
✓ Uses `get_option` / `update_option` (cache-friendly)
❌ Direct $wpdb->get_var on wp_postmeta in includes/class-meta.php:42
   → Replace with `get_post_meta`

## Cache invalidation
✓ delete_transient called in update_settings()
❌ Custom DB write in `update_status()` — no cache invalidation
   → Add: `wp_cache_delete( 'my_plugin_status', 'my-plugin-group' )`

## Page cache compatibility
✓ No `nocache_headers()` calls on init
✓ Cookies set only when needed
⚠ Sets `?my_plugin_v=1.0` query param on enqueue → may bust cache for some configs

## Severity: MEDIUM (1 missing invalidation, 1 direct query)
```

---

## Pair with `/orbit-db-profile`

`/orbit-db-profile` measures runtime DB query counts. This skill verifies the **architectural** patterns. Run together: profile shows the "what", cache-compat shows the "why".
