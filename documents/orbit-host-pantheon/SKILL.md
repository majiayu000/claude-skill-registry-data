---
name: orbit-host-pantheon
description: Pantheon hosting compatibility — read-only filesystem (only `wp-content/uploads` writable), Redis included, multidev environments, Quicksilver hooks, advanced CDN, NGINX-only. Use when the user says "Pantheon", "Pantheon hosting", "WP on Pantheon", or customer is on Pantheon.
---

# 🪐 orbit-host-pantheon — Pantheon compat

Pantheon's environment is uniquely restrictive: most of the file system is **read-only** at runtime, code lives in git, deploys are git-driven. Plugins that write outside `wp-content/uploads` break.

---

## What this skill checks

### 1. Read-only filesystem (the big one)

**Whitepaper intent:** Pantheon's containers are immutable. Code (incl. plugins) is read-only at runtime. The only writable path is `wp-content/uploads/`. Plugins that try to write configs, caches, or logs anywhere else fail silently → mysterious bugs.

```php
// ❌ Fails on Pantheon
file_put_contents( WP_CONTENT_DIR . '/cache/my-plugin.json', $data );
fopen( ABSPATH . 'tmp.log', 'w' );

// ✅ Always works
$uploads = wp_upload_dir();
file_put_contents( $uploads['basedir'] . '/my-plugin/cache.json', $data );
```

### 2. Redis included by default
Pantheon ships Redis on all paid plans. Use `wp_cache_*` confidently:
```php
wp_cache_set( 'my_key', $value, 'my-plugin', HOUR_IN_SECONDS );
```

### 3. Multidev environments
Pantheon supports unlimited dev/test/live + branch-based dev environments. Detect:
```php
$env = $_ENV['PANTHEON_ENVIRONMENT'] ?? null;  // 'dev', 'test', 'live', or branch name
if ( $env === 'live' ) {
  // Production-only behaviour
}
```

### 4. Quicksilver hooks
Pantheon-specific event hooks (deploy, cache-clear). Your plugin doesn't NEED to integrate but can:
```yaml
# pantheon.yml
api_version: 1
workflows:
  deploy:
    after:
      - type: webphp
        description: Run my plugin's deploy task
        script: private/scripts/post-deploy.php
```

### 5. Advanced Global CDN (Cloudflare Enterprise)
Same edge-cache rules as WPE / Kinsta. Custom cookies bust the cache.

### 6. NGINX-only stack
No `.htaccess`. Plugins that ship `.htaccess` files just include dead bytes.

### 7. Database — MariaDB
Some queries that work on MySQL fail on MariaDB. Test against both.

### 8. Drupal coexistence
Pantheon also hosts Drupal. Plugin must NOT assume the file system is exclusively WP — `wp-content/` paths are unique to WP installs.

---

## Output

```markdown
# Pantheon Compat — my-plugin

## Filesystem
- ❌ Plugin writes to wp-content/cache/my-plugin/ — Pantheon read-only outside uploads
   → Move to wp-uploads/my-plugin/cache/

## Redis
- ✓ Uses wp_cache_set/get — works with Pantheon Redis

## Environment detection
- ⚠ Plugin doesn't check $_ENV['PANTHEON_ENVIRONMENT'] — runs production behaviour on staging

## .htaccess
- ⚠ Plugin ships a .htaccess for rewrite rules — won't work, use flush_rewrite_rules()
```

---

## Pair with

- `/orbit-host-wpengine` / `/orbit-host-kinsta` — similar managed-host concerns
- `/orbit-cache-compat` — Redis usage

---

## Sources & Evergreen References

### Canonical docs
- [Pantheon Documentation](https://docs.pantheon.io/) — root
- [WordPress on Pantheon](https://docs.pantheon.io/guides/wordpress-developer) — WP-specific
- [Read-Only File System](https://docs.pantheon.io/files-on-pantheon) — restrictions
- [Quicksilver](https://docs.pantheon.io/guides/quicksilver) — webhook system

### Last reviewed
- 2026-04-29
