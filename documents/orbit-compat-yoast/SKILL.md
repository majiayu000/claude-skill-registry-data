---
name: orbit-compat-yoast
description: Coexistence audit with Yoast SEO — schema-output collision, meta-tag duplication, title-tag conflicts, sitemap merging, breadcrumb integration, custom-post-type registration order, REST-API endpoint conflicts. Use when the user says "Yoast compat", "Yoast SEO conflict", "schema duplicate", "meta tag conflict".
---

# 🪐 orbit-compat-yoast — Yoast SEO coexistence

Yoast is on 13M+ sites. Any plugin that touches SEO output (meta tags, schema, sitemaps, breadcrumbs, titles) coexists with Yoast or breaks customer trust.

---

## What this skill checks

### 1. Title-tag collision
**Whitepaper intent:** Two plugins setting `<title>` results in duplicate or empty `<title>`. Yoast adds `add_theme_support( 'title-tag' )` and runs at priority 1. Your plugin shouldn't override `<title>` unless gating with `function_exists( 'YoastSEO' ) === false`.

```php
// ❌ Conflicts with Yoast
add_filter( 'document_title_parts', 'my_plugin_title', 10 );

// ✅ Defer to Yoast if present
add_filter( 'document_title_parts', function( $parts ) {
  if ( defined( 'WPSEO_VERSION' ) ) return $parts;  // let Yoast handle
  // your title logic
  return $parts;
}, 10 );
```

### 2. Schema duplication
Yoast ships JSON-LD schema. Plugins that also output schema cause duplicates → search engines confused.

```php
// Detect Yoast schema and skip yours, OR hook into Yoast's pipeline:
add_filter( 'wpseo_schema_graph', 'my_plugin_extend_yoast_schema', 10, 2 );
```

### 3. Meta description collision
Same pattern — let Yoast win, OR hook into its filter:
```php
add_filter( 'wpseo_metadesc', 'my_plugin_alter_yoast_metadesc' );
```

### 4. Sitemap collision
Yoast generates `sitemap_index.xml`. If your plugin also generates a sitemap → 2 sitemaps fighting for `robots.txt` / Search Console.

```php
// ✅ Hook into Yoast's sitemap to add your URLs
add_filter( 'wpseo_sitemap_index', 'my_plugin_add_to_yoast_sitemap_index' );
```

### 5. Breadcrumb collision
```php
if ( function_exists( 'yoast_breadcrumb' ) ) {
  yoast_breadcrumb( '<nav class="breadcrumbs">', '</nav>' );
} else {
  // Your fallback breadcrumbs
}
```

### 6. Custom post type registration timing
Yoast registers its CPTs late. If your plugin registers earlier and uses similar names, conflict. Use unique prefixes.

### 7. REST API endpoint
`/wp-json/yoast/v1/` is Yoast's namespace. Don't shadow.

---

## Output

```markdown
# Yoast Coexistence — my-plugin

✓ document_title_parts filter checks WPSEO_VERSION before applying
❌ Schema output: duplicates Yoast's Article schema
   → Hook into wpseo_schema_graph instead
⚠ Sitemap: yours at /sitemap.xml, Yoast's at /sitemap_index.xml — search engines may pick wrong one
✓ Breadcrumbs defer to yoast_breadcrumb() when available
```

---

## Pair with

- `/orbit-compat-rankmath` — same patterns, different competitor
- `/orbit-seo-schema` — schema-specific
- `/orbit-conflict-matrix` — full conflict-matrix run

---

## Sources & Evergreen References

### Canonical docs
- [Yoast Developer Docs](https://developer.yoast.com/) — root
- [Yoast Filters](https://developer.yoast.com/customization/yoast-seo/filters/) — full filter reference
- [Yoast Schema Documentation](https://developer.yoast.com/customization/yoast-seo/adapting-schema/) — extend schema

### Last reviewed
- 2026-04-29
