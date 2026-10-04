---
name: orbit-host-cloudways
description: Cloudways compatibility audit — Breeze caching plugin, Object Cache Pro support, Varnish caching, server-level vs application-level caching, SSH access, multiple PHP versions, multiple stacks (Apache + NGINX, NGINX-only). Use when the user says "Cloudways", "DO + WP", "Vultr WP", or customer is on Cloudways.
---

# 🪐 orbit-host-cloudways — Cloudways compat

Cloudways is a managed-but-flexible host — DigitalOcean / Vultr / Linode + their stack on top. More flexibility than WPE/Kinsta, more responsibility on the user.

---

## What this skill checks

### 1. Breeze plugin (Cloudways' default caching)
Customers usually have Breeze installed by default. Conflicts arise when:
- Your plugin sets its own `Cache-Control` headers Breeze ignores
- Your plugin caches object data Breeze expects to clear

### 2. Object Cache Pro (paid add-on)
If the customer pays for OCP, Redis is persistent + reliable. Without it, no object cache at all on default plans.

### 3. Varnish (server-level cache)
Cloudways stack uses Varnish in front of Apache/NGINX. Same cookie rules — non-WP cookies bust the cache for all visitors.

```vcl
# Cloudways' default Varnish config respects:
# - Cookies starting with wp_, wordpress_, comment_author_
# - Cache exclusion via DONOTCACHEPAGE constant
```

```php
// Trigger Varnish bypass for a specific request
if ( my_plugin_needs_fresh_data() ) {
  if ( ! defined( 'DONOTCACHEPAGE' ) ) define( 'DONOTCACHEPAGE', true );
}
```

### 4. SSH access (yes)
Customers can SSH in via Cloudways portal. Your plugin's WP-CLI commands work fine.

### 5. PHP version (configurable per server)
Cloudways supports PHP 7.4 / 8.0 / 8.1 / 8.2 / 8.3. Customer changes via Cloudways portal.

### 6. Server stack
Default: NGINX-only. Older sites on Apache + NGINX hybrid. .htaccess works on Apache but not the NGINX-only stack — your plugin shouldn't depend on .htaccess rewrites.

```php
// ❌ Assumes Apache
file_put_contents( ABSPATH . '.htaccess', ... );

// ✅ Use WP API which handles both
flush_rewrite_rules( false );
```

### 7. Disk + bandwidth limits
Lower-tier plans have small disk + bandwidth quotas. Plugins that bloat the DB or generate large media files need to warn customers.

---

## Output

```markdown
# Cloudways Compat — my-plugin

✓ Detected: customer running Cloudways stack (server inspection)
✓ No .htaccess writes
✓ Triggers DONOTCACHEPAGE for dynamic endpoints
⚠ Plugin caches via wp_cache_* — works only on plans with Redis (OCP add-on)
   Document this limitation in plugin docs.
```

---

## Pair with

- `/orbit-cache-compat` — broader cache patterns
- `/orbit-host-shared` — similar disk-write concerns

---

## Sources & Evergreen References

### Canonical docs
- [Cloudways Help](https://support.cloudways.com/) — root
- [Breeze Plugin Docs](https://wordpress.org/plugins/breeze/) — caching plugin reference
- [Varnish Cache](https://varnish-cache.org/docs/) — server cache spec
- [Object Cache Pro](https://objectcache.pro/docs) — add-on reference

### Last reviewed
- 2026-04-29
