---
name: orbit-block-patterns
description: Audit and test block patterns shipped by a WordPress plugin — pattern category registration, preview rendering, `block_pattern_categories` filter usage, locked patterns, synced patterns (WP 6.3+), and Pattern Directory submission readiness. Use when the user says "block patterns", "register_block_pattern", "pattern preview", "synced patterns", or before submitting patterns to wordpress.org/patterns.
---

# 🪐 orbit-block-patterns — Block patterns audit

Patterns are the easiest content win for plugin teams — pre-built layouts users insert and adapt. Most plugins ship them wrong.

---

## Quick start

```bash
claude "/orbit-block-patterns Audit ~/plugins/my-plugin's block patterns."
```

---

## What it checks

### 1. Patterns registered with `register_block_pattern()`
```php
register_block_pattern( 'my-plugin/hero', [
  'title'       => __( 'Hero', 'my-plugin' ),
  'description' => __( 'Big hero with CTA', 'my-plugin' ),
  'categories'  => [ 'my-plugin' ],
  'keywords'    => [ 'hero', 'banner' ],
  'content'     => '<!-- wp:cover --><!-- /wp:cover -->',
  'viewportWidth' => 1280,
] );
```

### 2. Custom category registered
```php
register_block_pattern_category( 'my-plugin', [
  'label' => __( 'My Plugin', 'my-plugin' ),
] );
```

### 3. Pattern content uses correct block names
**Whitepaper intent:** Patterns reference block names. If your plugin's block is `my-plugin/example`, the pattern's content must use exactly that — typos fail silently and the pattern shows blank.

### 4. `viewportWidth` set
Without it, patterns get cropped in the inserter preview. Set `viewportWidth: 1280` (or 1440 for desktop-only).

### 5. Synced patterns (WP 6.3+)
Synced patterns share data across all uses. Useful for footers / headers / CTAs.

```php
register_block_pattern( 'my-plugin/synced-cta', [
  'content'  => '...',
  'inserter' => true,
  // synced via Pattern Directory or wp_block CPT
] );
```

### 6. Locked patterns
Use `templateLock` in the pattern content to prevent users from breaking the layout:
```html
<!-- wp:group {"templateLock":"all"} -->
```

---

## Output

```markdown
# Block Patterns Audit — my-plugin

## Patterns registered: 4

### my-plugin/hero
- ✓ Title, description, categories, keywords
- ✓ viewportWidth: 1280
- ⚠ Pattern uses `my-plugin/cta-button` — block doesn't exist (typo for `my-plugin/cta`?)

### my-plugin/footer
- ✓ Valid
- ⚠ No translatable strings in content — won't translate for non-English sites

## Pattern category
- ✓ Registered "my-plugin" category

## Recommendations
- Add `viewportWidth` to every pattern
- Consider 1 synced pattern (footer) for site-wide consistency
```

---

## Pair with

- `/orbit-gutenberg-dev` — overall block audit
- `/orbit-fse-test` — FSE + theme.json compat
- `/orbit-i18n` — pattern strings translated

---

## Sources & Evergreen References

### Canonical docs
- [Block Patterns API](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-patterns/) — `register_block_pattern`, categories
- [Patterns Directory](https://wordpress.org/patterns/) — submission flow
- [theme.json patterns](https://developer.wordpress.org/themes/global-settings-and-styles/patterns/) — theme-defined patterns
- [Synced Patterns (WP 6.3)](https://make.wordpress.org/core/2023/07/05/introducing-synced-patterns/) — release post

### Rule lineage
- `register_block_pattern_category` — added WP 5.5
- `viewportWidth` — added WP 5.9
- Synced Patterns — WP 6.3 (was "Reusable Blocks", renamed)
- `templateLock` — pattern-level support added WP 6.0

### Last reviewed
- 2026-04-29 — re-review on every WP minor release (patterns API evolves)
