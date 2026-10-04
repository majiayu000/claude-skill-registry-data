---
name: orbit-compat-polylang
description: Polylang compatibility audit — pll_register_string, pll_current_language, custom-post-type translation, language switcher hooks, REST + WP-CLI integration. Polylang has free + Pro versions; covers both. Use when the user says "Polylang compat", "Polylang translate", "WPML alternative", or coexisting with Polylang.
---

# 🪐 orbit-compat-polylang — Polylang compatibility

Polylang is the open-source WPML alternative (~700K sites). Different API than WPML — both must be supported separately, since users pick one based on price/preference.

---

## What this skill checks

### 1. Register translatable strings
```php
// Register on init
add_action( 'init', function() {
  if ( function_exists( 'pll_register_string' ) ) {
    pll_register_string( 'welcome_text', 'Welcome to my plugin', 'My Plugin', false );
  }
} );

// Retrieve
$translated = function_exists( 'pll__' )
  ? pll__( 'Welcome to my plugin' )
  : 'Welcome to my plugin';
```

### 2. Current language
```php
$lang = function_exists( 'pll_current_language' ) ? pll_current_language() : 'en';
```

### 3. Translate post ID
```php
$translated_id = function_exists( 'pll_get_post' )
  ? pll_get_post( $post_id, 'fr' )
  : $post_id;
```

### 4. Custom post type registration
**Whitepaper intent:** Polylang reads CPT settings — your plugin should register CPTs with `'show_in_rest' => true` AND let Polylang's settings UI mark them translatable.

```php
register_post_type( 'my_plugin_post', [
  'public' => true,
  'show_in_rest' => true,
  // Polylang admin → Languages → Settings → Custom post types and Taxonomies
  // user enables "translate" for this CPT
] );
```

### 5. Detect active
```php
if ( function_exists( 'pll_register_string' ) || class_exists( 'Polylang' ) ) {
  // Polylang is active
}
```

### 6. URL handling (3 URL modes like WPML)
```php
// Get URL for a specific language
$url_fr = function_exists( 'pll_home_url' ) ? pll_home_url( 'fr' ) : home_url();
```

### 7. Pro features (paid)
Polylang Pro adds:
- Strings translation export/import
- Slug translation
- Duplicate post in another language

If your plugin generates URLs from slugs, it must handle Pro's slug translation.

---

## Output

```markdown
# Polylang Compat — my-plugin

✓ Detects Polylang via class_exists check
✓ pll_register_string called for admin notices
⚠ Hard-coded strings in includes/templates/welcome.php — not registered
✓ pll_current_language used for current-language detection
❌ URL builder doesn't use pll_home_url — generates EN URLs in FR context
```

---

## Pair with

- `/orbit-compat-wpml` — alt translation plugin (different API)
- `/orbit-i18n` — base i18n

---

## 7. Language-aware custom endpoints (REST, rewrite, AJAX)

**The bug that ships when this check is missing:** plugin exposes a custom URL like `/{slug}.md` or `/wp-json/myplugin/v1/foo`. User has Polylang active with EN/ES translations linked. Request comes in for the ES translation — endpoint returns the EN content because the handler never consulted Polylang.

### Required checks

For every custom REST route, rewrite rule, or AJAX handler that returns post content:

#### 7.1 Resolve current language

```php
$lang = function_exists( 'pll_current_language' )
    ? pll_current_language()
    : ( isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : 'en' );
```

Sources of truth, in order:
1. `pll_current_language()` (Polylang's resolved language)
2. `?lang=xx` query parameter
3. `Accept-Language` request header (parse via `WP::parse_request()` or manual)

#### 7.2 Translate the target post to the requested language

```php
$translated_id = function_exists( 'pll_get_post' )
    ? pll_get_post( $post_id, $lang )
    : $post_id;

if ( ! $translated_id ) {
    // No translation exists for this language → fall back to source, OR 404
    // Document the choice in the endpoint's response headers
}
```

#### 7.3 Set response headers correctly

```php
header( 'Content-Type: text/markdown; charset=utf-8' );  // charset always
header( 'Content-Language: ' . $lang );                  // tell client what we served
header( 'Vary: Accept-Language' );                       // tell caches the response varies by language
```

### Detection grep

```bash
# Find custom REST routes
grep -rn 'register_rest_route' --include='*.php' . | grep -v 'tests/'

# Find rewrite rules
grep -rn 'add_rewrite_rule\|template_redirect' --include='*.php' . | grep -v 'tests/'

# Find AJAX handlers
grep -rn "add_action.*wp_ajax" --include='*.php' . | grep -v 'tests/'
```

For each result, inspect the handler body. If the handler returns content tied to a `$post_id` or a slug, search the handler body for `pll_current_language\|pll_get_post\|wpml_current_language\|wpml_object_id\|Accept-Language\|?lang=`. If none present → multilingual gap. **High severity** when Polylang/WPML is in the plugin's compatibility matrix.

### Caching gotcha

If the endpoint is cacheable (sets `Cache-Control: public, max-age=...`), the cache key MUST include language — either via distinct URL per language (`/es/{slug}.md`) or via `Vary: Accept-Language` (which most CDNs ignore by default; Cloudflare APO ignores Vary entirely). Document the chosen strategy in the endpoint header.

## Sources & Evergreen References

### Canonical docs
- [Polylang Documentation](https://polylang.pro/doc/) — root
- [Polylang for Developers](https://polylang.pro/doc/developpers-how-to/) — API reference
- [Functions Reference](https://polylang.pro/doc/category/developers/) — pll_* functions

### Last reviewed
- 2026-04-29 (original) · 2026-06-02 (added §7 language-aware custom endpoints)
