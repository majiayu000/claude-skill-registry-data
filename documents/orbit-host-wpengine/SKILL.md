---
name: orbit-host-wpengine
description: WP Engine compat audit — fetches WP Engine's CURRENT disallowed-plugins list + EverCache rules + filesystem restrictions AT RUNTIME. Auto-stays-current with WPE policy. Use when the user says "WP Engine", "WPE", "is my plugin WPE-compatible", "WPE banned plugins", or before a customer hosts on WP Engine.
---

# 🪐 orbit-host-wpengine — Runtime-evergreen WP Engine compat

> WPE's disallowed-plugins list and EverCache rules update regularly. This skill fetches what's true today.

---

## Runtime — fetch live before auditing (DO THIS FIRST)

When this skill is invoked:

1. **Fetch in parallel**:
   - https://wpengine.com/support/disallowed-plugins/ → CURRENT disallowed list
   - https://wpengine.com/support/cache/ → EverCache rules + cookie patterns
   - https://wpengine.com/developers/ → environment specs (PHP versions, file paths)
   - https://wpengine.com/changelog/ → recent platform changes
   - https://wpengine.com/support/git/ → Git push deploy patterns

2. **Synthesize current state**:
   - "Is my plugin (or any dep) on WPE's disallowed list right now?"
   - "What cookie patterns bypass EverCache today?"
   - "What's the current PHP / WP version range supported on WPE?"
   - "Has WPE added any new restrictions / detection patterns?"

3. **Audit the plugin** against today's rules.

---

## What gets checked

### A. Disallowed-plugins match (the big one)
WPE bans plugins that conflict with their stack. As of last fetch:
- Caching: W3 Total Cache, WP Super Cache, WP Rocket (use EverCache)
- Backup: BackupBuddy, BackUpWordPress (use native snapshots)
- Hit counter: WP Postviews, etc.
- Some security plugins that conflict with their built-in firewall

The fetched list grows; the skill matches the user's plugin + its bundled deps.

### B. EverCache cookie rules
**Whitepaper intent:** EverCache caches by URL. Cookies starting with `wp_*` or `wordpress_*` automatically bypass. Custom plugin cookies don't — they bust cache for everyone.

```php
// ❌
setcookie( 'my_plugin_visitor_id', wp_generate_uuid4(), ... );

// ✅ Logged-in only
if ( is_user_logged_in() ) setcookie( 'my_plugin_visitor_id', ... );
```

### C. Filesystem write restrictions
WPE locks `wp-config.php` and certain root files. Plugins that try to write there silently fail.

```php
// ❌ Will fail silently
file_put_contents( ABSPATH . 'wp-config.php', $patched );

// ✅ Use uploads dir
$uploads = wp_upload_dir();
file_put_contents( $uploads['basedir'] . '/my-plugin/foo.txt', $data );
```

### D. Memcached available; use wp_cache_*
```php
wp_cache_set( 'my_key', $value, 'my-plugin', HOUR_IN_SECONDS );
```

### E. PHP / WP version constraints
WPE's currently-supported PHP versions (per fetched docs). Customers are typically 1 minor behind PHP main. If your plugin requires PHP 8.4 today and WPE only ships 8.3 → customers can't run yours yet.

### F. Detect WPE
```php
if ( defined( 'WPE_APIKEY' ) || defined( 'IS_WPE' ) ) {
  // Running on WP Engine
}
```

### G. Staging vs production
```php
$env = wp_get_environment_type();
if ( $env === 'staging' ) { /* skip live-mode ... */ }
```

---

## Output

```markdown
# WP Engine Compat — my-plugin · 2026-04-30

> Per wpengine.com/support/disallowed-plugins (fetched 2026-04-30 14:32 UTC):
> Disallowed list as of today: 17 entries
> Match: 0 ✓

## EverCache cookie rules
- ⚠ Plugin sets `my_plugin_visitor_id` on every visit — busts EverCache
  → Per wpengine.com/support/cache (fetched today): only `wp_*` / `wordpress_*` cookies bypass
  → Restrict to logged-in users OR document for WPE customers to add via User Portal

## Filesystem
- ✓ Plugin doesn't try to write wp-config.php or other locked paths

## Memcached
- ✓ Plugin uses wp_cache_set/get
- ✓ Compatible with WPE's Memcached

## PHP versions
- WPE supports: 7.4, 8.0, 8.1, 8.2, 8.3 (per fetched docs)
- Plugin's Requires PHP: 7.4 ✓ (compatible with all)

## Severity: MEDIUM (cookie issue only)
```

---

## Pair with

- `/orbit-host-kinsta` / `-cloudways` / `-pantheon` — peer hosts
- `/orbit-cache-compat` — broader cache strategy

---

## Smoke test

Input: a plugin with no special host requirements.
Expected:
- 0 disallowed-plugin matches
- ✓ on cookie / filesystem / Memcached patterns
- Cites wpengine.com docs with today's fetch timestamp

---

## Embedded fallback rules (offline)
- Disallowed-plugin overlap → flag
- Custom cookies on every page → cache buster
- wp-config.php writes → fail silently on WPE
- Use wp_cache_* for Memcached
- Detect via IS_WPE / WPE_APIKEY constants

## Sources & Evergreen References

### Live sources (fetched on every run)
- [WP Engine Support](https://wpengine.com/support/) — root
- [Disallowed Plugins](https://wpengine.com/support/disallowed-plugins/) — current list
- [Cache Rules](https://wpengine.com/support/cache/) — EverCache
- [Developers](https://wpengine.com/developers/) — environment specs
- [WPE Changelog](https://wpengine.com/changelog/) — recent platform changes

### Last reviewed
2026-04-30 — runtime-evergreen
