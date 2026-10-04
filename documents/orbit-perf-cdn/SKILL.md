---
name: orbit-perf-cdn
description: CDN compatibility audit (Cloudflare / BunnyCDN / KeyCDN / StackPath / native AWS CloudFront / Fastly) — verifies asset URLs work via CDN rewrite, immutable cache headers, query-string handling, cross-origin (CORS) headers for fonts, edge purging on plugin update. Use when the user says "CDN compat", "Cloudflare", "asset CDN", "edge cache", "CORS for fonts".
---

# 🪐 orbit-perf-cdn — CDN compatibility

CDNs work for plugins that play nice with them. Plugins that hardcode `home_url()` for assets, set `Cache-Control: no-cache`, or skip fingerprinting break CDN benefits.

---

## What this skill checks

### 1. Asset URLs use rewrite-safe paths
**Whitepaper intent:** CDNs typically rewrite `/wp-content/...` → `cdn.example.com/wp-content/...`. Plugins hardcoding `home_url('/wp-content/...')` defeat this — the asset is fetched from origin, not edge.

```php
// ❌ Hardcoded — survives plugins' good intentions but defeats CDN
echo home_url( '/wp-content/plugins/my-plugin/assets/img/icon.svg' );

// ✅ plugins_url() — CDN-rewritten because it produces relative-ish URLs
echo plugins_url( 'assets/img/icon.svg', __FILE__ );
```

### 2. Immutable cache headers (versioned URLs)
```php
wp_enqueue_script(
  'my-plugin',
  plugins_url( 'assets/js/main.js', __FILE__ ),
  [],
  MY_PLUGIN_VERSION,  // ← appended as ?ver=2.5.0 — bust cache on plugin update
  true
);
```

For static assets that never change (icons, decorative images), use immutable URLs (file name with hash). CDN can cache forever.

### 3. CORS for cross-origin fonts
**Whitepaper intent:** CDN-served fonts on a different origin than the page need CORS. Without `Access-Control-Allow-Origin`, browsers refuse to render them.

```php
// In your plugin's font-loader hook:
add_filter( 'http_headers', function( $headers ) {
  if ( strpos( $_SERVER['REQUEST_URI'] ?? '', '.woff' ) !== false ) {
    $headers['Access-Control-Allow-Origin'] = '*';
  }
  return $headers;
});
```

Or more commonly, document for users that they need to set CORS via .htaccess / NGINX config / CDN dashboard.

### 4. Query string preservation
Some CDNs strip query strings from cache key (so `style.css?ver=2.5` and `style.css?ver=2.6` cache to the same edge entry). Plugins that depend on cache busting via query string need to test on the customer's actual CDN config.

```php
// Use file-name fingerprinting if query strings unreliable
wp_enqueue_style( 'my-plugin', plugins_url( "assets/build/main.{$hash}.css", __FILE__ ) );
```

### 5. Cache-Control headers — don't override
```php
// ❌ Plugin overriding CC is rude; defeats CDN
header( 'Cache-Control: no-cache' );

// ✅ Only set Cache-Control for dynamic endpoints (REST, AJAX), and use no-store there
```

### 6. Edge purging on plugin update
Major CDNs (Cloudflare, BunnyCDN) accept programmatic purge. If your plugin updates assets, trigger a purge:

```php
add_action( 'upgrader_process_complete', function( $upgrader, $hook_extra ) {
  if ( $hook_extra['plugin'] === 'my-plugin/my-plugin.php' ) {
    my_plugin_purge_cdn_via_api();
  }
}, 10, 2 );
```

But — most plugins shouldn't ship CDN credentials. Document the pattern instead.

### 7. CDN rewrite-aware plugins
Common rewrite plugins (Cloudflare's WP plugin, WP Rocket's CDN module) expect `wp_enqueue_*` URLs. Plugins outputting `<script src="...">` directly bypass this.

---

## Output

```markdown
# CDN Compat — my-plugin

✓ Uses plugins_url() for asset URLs (CDN-rewrite-safe)
✓ Versioned URLs (?ver=2.5.0) for cache-busting
❌ Inline `<script src="https://example.com/wp-content/...">` in includes/class-frontend.php:42
   → Use wp_enqueue_script for CDN compatibility
⚠ No CORS notice in docs for self-hosted fonts via CDN
```

---

## Pair with

- `/orbit-cache-compat` — broader cache concerns
- `/orbit-bundle-analysis` — what's in the assets

---

## Sources & Evergreen References

### Canonical docs
- [Cloudflare WP](https://www.cloudflare.com/integrations/wordpress/) — CF + WP
- [MDN — CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) — cross-origin spec
- [HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching) — Cache-Control reference
- [WP — wp_enqueue_*](https://developer.wordpress.org/themes/basics/including-css-javascript/) — proper enqueue

### Last reviewed
- 2026-04-29
