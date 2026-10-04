---
name: orbit-host-kinsta
description: Kinsta hosting compat audit — fetches Kinsta's CURRENT banned-plugins list + cache rules + Redis availability AT RUNTIME (not from a snapshot). Auto-stays-current with Kinsta's policy changes. Use when the user says "Kinsta", "managed WP Kinsta", "is my plugin Kinsta-compatible", "Kinsta banned plugins", or before customer hosts on Kinsta.
---

# 🪐 orbit-host-kinsta — Runtime-evergreen Kinsta compat

> Banned-plugins lists change. Cache rules change. Redis add-on terms change.
> This skill fetches what's true today — not what was true when the SKILL.md was written.

---

## Runtime — fetch live before auditing (DO THIS FIRST)

When this skill is invoked:

1. **Fetch in parallel**:
   - https://kinsta.com/blog/banned-plugins-kinsta/ → CURRENT banned-plugins list
   - https://kinsta.com/help/edge-caching/ → current edge-caching rules + cookie behaviour
   - https://kinsta.com/help/redis-cache/ → Redis add-on availability + plans
   - https://kinsta.com/help/multidev-environments/ → staging / multidev setup
   - https://kinsta.com/changelog/ → recent platform changes

2. **Synthesize current state**:
   - "Is my plugin (or any of its bundled deps) on the banned list as of today?"
   - "What cache rules apply on Kinsta right now? What cookie patterns bust the edge cache?"
   - "Is Redis included or paid add-on on the customer's plan tier?"
   - "Has Kinsta added any new restrictions / detection patterns this quarter?"

3. **Audit the plugin** against today's fetched rules.

---

## What gets checked

### A. Banned-plugins list match
The live-fetched banned list. The skill greps `composer.json`, `package.json`, and includes for any banned dependency. As of last fetch, common bans include:
- WP Rocket conflicts with Kinsta Cache (use one)
- Some backup plugins conflict with native daily backups
- Some security plugins that try to write to wp-config

If the user's plugin BUNDLES a banned plugin as a dependency or is itself banned — flag.

### B. Cloudflare Enterprise edge cache
Kinsta runs Cloudflare Enterprise. Custom plugin cookies bust the edge cache for everyone unless declared.

```php
// ❌ Sets a unique cookie per visitor — kills cache hit rate
setcookie( 'my_plugin_visitor_id', wp_generate_uuid4(), ... );

// ✅ Only set cookie when needed (logged-in users, specific contexts)
if ( is_user_logged_in() ) setcookie( 'my_plugin_visitor_id', ... );

// Or document for users that they need to add the cookie name to Kinsta's
// cache exclusion list via MyKinsta → Cache → Page Cache → Cookies to Bypass.
```

### C. Redis availability detection
Kinsta's Redis is an add-on (~$100/mo). Default plans don't have Redis = no persistent object cache.

```php
// Detect persistent cache
if ( wp_using_ext_object_cache() ) {
  // Persistent — safe to cache aggressively
} else {
  // Transient-only — short TTLs
}
```

### D. KINSTA_CACHE_ZONE constant detection
Kinsta sets `KINSTA_CACHE_ZONE` constant; plugins can detect:
```php
if ( defined( 'KINSTA_CACHE_ZONE' ) ) {
  // Running on Kinsta — adjust if needed
}
```

### E. Multidev / staging awareness
```php
$env = wp_get_environment_type();
if ( $env === 'staging' ) {
  // Disable production-only behaviour (analytics, payment live mode)
}
```

### F. Disk write performance
Kinsta uses GCP persistent disks — slower than local SSD. Plugins writing many small files (logs, cache) should batch.

### G. NEW restrictions discovered live
Whatever the fetched changelog / banned-plugins list has added since the embedded rules were last verified — automatically applied. The skill doesn't need to be manually updated.

---

## Output

```markdown
# Kinsta Compat — my-plugin · 2026-04-30

> Per kinsta.com/blog/banned-plugins-kinsta (fetched 2026-04-30 14:32 UTC):
> Banned-plugins list as of today: 14 entries
> My plugin or its deps on banned list: 0 ✓

## Edge cache (Cloudflare Enterprise)
- ⚠ Plugin sets `my_plugin_visitor_id` cookie on every page load
   → Per kinsta.com/help/edge-caching (fetched today):
     non-WP cookies bust cache for the entire visitor session
   → Either restrict to logged-in users OR document for customers to add to bypass list

## Redis
- ✓ Plugin uses wp_cache_set/get (works on Redis-add-on plans)
- ⚠ Default-plan customers (no Redis): plugin will be slow on these
  → Document this; OR add transient fallback for hot paths

## Multidev / staging
- ✓ Plugin honours wp_get_environment_type
- ✓ Live-mode payment skipped on staging

## NEW (since last skill check, per fetched changelog 2026-04-22):
- Kinsta tightened CSP defaults — your inline-script in admin/footer.php
  may need a nonce now. Verify on the customer's site.
```

---

## Pair with

- `/orbit-cache-compat` — broader cache strategy
- `/orbit-host-wpengine` — similar managed-host concerns
- `/orbit-host-cloudways` / `/orbit-host-pantheon` — alt managed hosts

---

## Smoke test

Input: a plugin with `setcookie('my_visitor_id', ...)` on every page.
Expected:
- ⚠ MEDIUM finding — cookie busts edge cache
- Cites kinsta.com/help/edge-caching with today's fetch
- Banned-plugin check returns 0 matches

---

## Embedded fallback rules (offline)
- Bundled banned-plugin overlap → flag
- Cookie-busting edge cache → flag
- Assume Redis only on paid plans
- Use `KINSTA_CACHE_ZONE` constant for detection
- `wp_get_environment_type()` for staging detection

## Sources & Evergreen References

### Live sources (fetched on every run)
- [Kinsta Help](https://kinsta.com/help/) — root
- [Banned Plugins List](https://kinsta.com/blog/banned-plugins-kinsta/) — current list
- [Edge Caching](https://kinsta.com/help/edge-caching/) — rules
- [Redis Add-on](https://kinsta.com/help/redis-cache/) — availability
- [Multidev](https://kinsta.com/help/multidev-environments/) — staging
- [Kinsta Changelog](https://kinsta.com/changelog/) — recent platform changes

### Last reviewed
2026-04-30 — runtime-evergreen; banned list re-fetched on every run
