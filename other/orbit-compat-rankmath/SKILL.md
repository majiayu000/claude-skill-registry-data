---
name: orbit-compat-rankmath
description: Coexistence audit with RankMath SEO — schema-output collision (RankMath's schema is more aggressive than Yoast), meta-tag duplication, title-tag conflicts, sitemap merging, REST endpoint conflicts. Use when the user says "RankMath compat", "RankMath conflict", or coexisting with RM.
---

# 🪐 orbit-compat-rankmath — RankMath SEO coexistence

RankMath grew to ~3M sites in ~5 years. More aggressive default-on features than Yoast — schema, breadcrumbs, redirections, all enabled by default.

---

## What this skill checks

### 1. Schema graph (RankMath ships ALL schema types by default)
RankMath registers schema for Article, Organization, WebSite, Product, Recipe, Event, etc. — most are on by default. Your plugin's schema duplicates.

```php
// Hook into RankMath's pipeline instead
add_filter( 'rank_math/schema/snippet', 'my_plugin_extend_rm_schema' );
add_filter( 'rank_math/schema/data', 'my_plugin_alter_rm_schema_data' );
```

### 2. Title + meta description
**Whitepaper intent:** RankMath replaces `<title>` and `<meta name="description">`. Don't double-output. Detect and defer:

```php
if ( class_exists( 'RankMath' ) || defined( 'RANK_MATH_VERSION' ) ) {
  // Don't output title / meta description
}
```

### 3. Sitemap (RankMath ships sitemap.xml)
Same conflict as Yoast — RM generates `/sitemap_index.xml`. Hook in instead of duplicating.

### 4. Redirections
RankMath has a "Redirections" module (404 → URL mapping). Plugins that ALSO redirect (membership plugins, multilingual) conflict on the same URL.

Order of precedence:
- WP core `template_redirect` action
- RankMath redirections (priority 11)
- Other plugins

Document where your plugin sits in the priority chain.

### 5. REST namespace `/wp-json/rankmath/v1/` — don't shadow.

### 6. Breadcrumb function
```php
if ( function_exists( 'rank_math_the_breadcrumbs' ) ) {
  rank_math_the_breadcrumbs();
} elseif ( function_exists( 'yoast_breadcrumb' ) ) {
  yoast_breadcrumb();
} else {
  // Plugin fallback
}
```

### 7. Wizard collision
RankMath's first-run wizard claims onboarding flow. Your plugin's first-activation tour shouldn't conflict — defer if RankMath wizard is incomplete.

---

## Output

```markdown
# RankMath Coexistence — my-plugin

✓ Defers title-tag to RankMath
❌ Schema Article output duplicates RankMath
   → Use rank_math/schema/snippet filter
⚠ Both your plugin and RankMath have a "redirect 404 → home" rule
   → Document precedence in your README
✓ Breadcrumbs detect rank_math_the_breadcrumbs first
```

---

## Pair with

- `/orbit-compat-yoast` — same SEO-coexistence concerns
- `/orbit-seo-schema` — schema specifics

---

## Sources & Evergreen References

### Canonical docs
- [RankMath Developer Docs](https://rankmath.com/kb/category/developer-and-technical/) — root
- [RankMath Filters & Hooks](https://rankmath.com/kb/filters-hooks-api-developer/) — extension API
- [Schema Customisation](https://rankmath.com/kb/customize-schema/) — extending schema

### Last reviewed
- 2026-04-29
