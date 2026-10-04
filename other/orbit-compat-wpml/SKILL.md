---
name: orbit-compat-wpml
description: WPML compatibility audit — translatable strings via icl_t / wpml_register_string, custom-post-type translation, taxonomy translation, language switcher hooks, current-language detection, sitemap-per-language, and the wpml-config.xml registration file. Use when the user says "WPML compat", "WPML translate strings", "translation plugin", or before customer asks "does this work with WPML?".
---

# 🪐 orbit-compat-wpml — WPML compatibility

WPML is the dominant paid translation plugin (~1M sites). Plugins that store/output translatable text need WPML hooks or strings stay in default-language only.

---

## What this skill checks

### 1. wpml-config.xml registration
**Whitepaper intent:** WPML reads `wpml-config.xml` from your plugin directory to know which custom fields, options, and CPTs to translate. Without it, WPML can't translate your plugin's content.

```xml
<!-- wpml-config.xml -->
<wpml-config>
  <custom-fields>
    <custom-field action="translate">my_plugin_subtitle</custom-field>
    <custom-field action="copy">my_plugin_color</custom-field>
  </custom-fields>
  <admin-texts>
    <key name="my_plugin_settings">
      <key name="welcome_text" />
    </key>
  </admin-texts>
  <custom-types>
    <custom-type translate="1">my_plugin_post</custom-type>
  </custom-types>
  <taxonomies>
    <taxonomy translate="1">my_plugin_taxonomy</taxonomy>
  </taxonomies>
</wpml-config>
```

### 2. Translatable strings via WPML String API
```php
// Register strings WPML should pick up
do_action( 'wpml_register_single_string', 'my-plugin', 'Settings Title', 'Settings' );

// Retrieve
$translated = apply_filters( 'wpml_translate_single_string', 'Settings', 'my-plugin', 'Settings Title' );
```

### 3. Get current language
```php
$lang = apply_filters( 'wpml_current_language', null );  // 'en', 'fr', etc.
```

### 4. Switch language programmatically
```php
do_action( 'wpml_switch_language', 'fr' );
// ... do stuff in French context ...
do_action( 'wpml_switch_language', null );  // restore
```

### 5. Get translated post
```php
$translated_id = apply_filters( 'wpml_object_id', $post_id, 'post', true, 'fr' );
```

### 6. URL handling
WPML supports 3 URL modes: directory (`/fr/`), subdomain (`fr.site.com`), parameter (`?lang=fr`). Your plugin's URL builders must respect:
```php
$url = apply_filters( 'wpml_permalink', $url, 'fr' );
```

### 7. Detect WPML active
```php
if ( function_exists( 'icl_object_id' ) || class_exists( 'SitePress' ) ) {
  // WPML is active
}
```

### 8. Sitemap per language
If you generate sitemaps, generate one per language. WPML provides hooks.

---

## Output

```markdown
# WPML Compat — my-plugin

❌ Missing wpml-config.xml — WPML can't find your custom fields / CPTs
   → Generate from wpml-config.xml template
✓ Strings registered via wpml_register_single_string
✓ Current-language detection via wpml_current_language filter
⚠ URL builder in includes/class-link.php:42 doesn't filter through wpml_permalink
✓ Detects SitePress before applying logic
```

---

## Pair with

- `/orbit-compat-polylang` — alt translation plugin (different API)
- `/orbit-i18n` — base i18n
- `/orbit-designer-rtl` — RTL languages need direction handling

---

## Language-aware custom endpoints (REST, rewrite, AJAX)

**The bug that ships when this check is missing:** plugin exposes `/{slug}.md` or `/wp-json/myplugin/v1/foo`. User has WPML active with EN→ES translation. Request hits the ES URL — endpoint returns EN content because the handler never consulted WPML.

### Required checks

For every custom REST route, rewrite rule, or AJAX handler that returns post content:

#### 1. Resolve current language

```php
$lang = apply_filters( 'wpml_current_language', null );
if ( ! $lang ) {
    $lang = isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : 'en';
}
```

#### 2. Translate the target post to the requested language

```php
$translated_id = apply_filters( 'wpml_object_id', $post_id, get_post_type( $post_id ), false, $lang );

if ( ! $translated_id || $translated_id === $post_id ) {
    // No translation exists OR translation === source. Decide: fall back or 404.
}
```

#### 3. Set response headers

```php
header( 'Content-Type: text/markdown; charset=utf-8' );
header( 'Content-Language: ' . $lang );
header( 'Vary: Accept-Language' );
```

### Detection grep

```bash
# Custom REST routes
grep -rn 'register_rest_route' --include='*.php' . | grep -v 'tests/'

# Rewrite rules
grep -rn 'add_rewrite_rule\|template_redirect' --include='*.php' . | grep -v 'tests/'

# AJAX handlers
grep -rn "add_action.*wp_ajax" --include='*.php' . | grep -v 'tests/'
```

For each handler that returns post content, search its body for `wpml_current_language\|wpml_object_id\|apply_filters.*wpml\|?lang=\|Accept-Language`. If absent → multilingual gap. **High severity** when WPML is in the plugin's compatibility matrix.

### wpml-config.xml currency

Every new option, post-meta key, term-meta key, or custom field shipped in the release must be reflected in `wpml-config.xml` so WPML's translation editor picks it up. Run after every release-touching commit:

```bash
diff <(grep '<custom-field\|<custom-type\|<admin-text' wpml-config.xml | sort) \
     <(grep -rh 'update_post_meta\|register_post_type\|update_option' --include='*.php' . | sort -u)
```

Any new meta key in code that isn't listed in `wpml-config.xml` → translators can't translate it. **High severity** on customer-facing keys.

### Caching gotcha

WPML's URL modes (`/es/`, `?lang=es`, subdomain) affect cache key shape. If the endpoint is cacheable, document which WPML URL mode the cache plan assumes. If `Vary: Accept-Language` is the strategy, note that Cloudflare APO ignores it.

## Sources & Evergreen References

### Canonical docs
- [WPML Documentation](https://wpml.org/documentation/) — root
- [Plugin Compatibility Guide](https://wpml.org/documentation/support/wpml-coding-api/) — coding API
- [wpml-config.xml Format](https://wpml.org/documentation/support/language-configuration-files/) — config schema
- [String Translation API](https://wpml.org/documentation/support/wpml-coding-api/wpml-hooks-reference/) — hooks reference

### Last reviewed
- 2026-04-29 (original) · 2026-06-02 (added §7 language-aware custom endpoints + wpml-config.xml currency)
