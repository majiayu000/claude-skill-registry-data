---
name: orbit-block-bindings
description: Audit Block Bindings API usage — the WP 6.5+ way to bind block attributes to dynamic data sources (post meta, options, custom sources) without writing custom render filters or hacks. Catches plugins still using the old `render_block` filter pattern that should migrate. Use when the user says "block bindings", "bind block attribute", "post meta in block", "WP 6.5 block API", or modernising a custom-render filter.
---

# 🪐 orbit-block-bindings — Block Bindings API audit

Pre-WP 6.5 you wrote a `render_block` filter to inject post-meta into a block. WP 6.5 ships the Block Bindings API — declarative, performant, and works in the editor too. This skill catches code that should migrate.

---

## Quick start

```bash
claude "/orbit-block-bindings Audit ~/plugins/my-plugin for legacy render_block filter patterns that should migrate to Block Bindings."
```

---

## What it checks

### 1. Legacy `render_block` patterns
**Whitepaper intent:** A filter that finds-and-replaces text in `$block_content` is brittle (markup changes break it), slow (runs on every block render), and invisible to the editor (preview shows the wrong content).

```php
// ❌ Legacy approach
add_filter( 'render_block', function( $block_content, $block ) {
  if ( $block['blockName'] === 'core/paragraph' ) {
    $price = get_post_meta( get_the_ID(), 'price', true );
    return str_replace( '{{price}}', esc_html( $price ), $block_content );
  }
  return $block_content;
}, 10, 2 );

// ✅ Block Bindings (WP 6.5+)
add_action( 'init', function() {
  register_block_bindings_source( 'my-plugin/post-price', [
    'label' => __( 'Post Price', 'my-plugin' ),
    'get_value_callback' => function( $args, $block ) {
      return get_post_meta( $block->context['postId'], 'price', true );
    },
    'uses_context' => [ 'postId' ],
  ] );
} );
```

The block then references it:
```html
<!-- wp:paragraph {"metadata":{"bindings":{"content":{"source":"my-plugin/post-price"}}}} -->
<p>$0</p>
<!-- /wp:paragraph -->
```

### 2. Bindings registered on `init` (not earlier)
```php
// ❌ Wrong — too early
register_block_bindings_source( ... );

// ✅ Right
add_action( 'init', function() {
  register_block_bindings_source( ... );
} );
```

### 3. `uses_context` declared
```php
register_block_bindings_source( 'my-plugin/source', [
  'uses_context' => [ 'postId', 'queryId' ],  // ← must declare what context you read
  'get_value_callback' => function( $args, $block ) {
    return get_post_meta( $block->context['postId'], $args['key'], true );
  },
] );
```

Without `uses_context`, the callback gets an empty `$block->context`.

### 4. Sanitization in `get_value_callback`
```php
'get_value_callback' => function( $args, $block ) {
  $value = get_post_meta( $block->context['postId'], $args['key'], true );
  return is_string( $value ) ? sanitize_text_field( $value ) : '';
}
```

### 5. Editor experience (label, get_value_callback for editor)
```php
register_block_bindings_source( 'my-plugin/source', [
  'label' => __( 'My Source', 'my-plugin' ),  // ← shows in editor binding picker
  'get_value_callback' => '...',
] );
```

---

## Output

```markdown
# Block Bindings Audit — my-plugin

## Legacy render_block filters: 3 (should migrate)
- includes/class-render.php:42 — replaces `{{price}}` in core/paragraph
  → Migrate to bindings source `my-plugin/price`
- includes/class-render.php:78 — replaces `{{author}}`
- includes/class-meta-render.php:15 — replaces 5 different placeholders

## Bindings sources registered: 0 (consider adding)

## Recommendation
Bump `Requires at least: 6.5` and migrate the 3 legacy filters to Block Bindings.
Net gain: editor preview shows real values, render is faster, markup-agnostic.
```

---

## Pair with

- `/orbit-gutenberg-dev` — overall block audit
- `/orbit-interactivity-api` — for client-side dynamic data
- `/orbit-wp-performance` — hook weight from filter chains

---

## Sources & Evergreen References

### Canonical docs
- [Block Bindings API](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-bindings/) — root reference
- [register_block_bindings_source()](https://developer.wordpress.org/reference/functions/register_block_bindings_source/) — function ref
- [WP 6.5 Block Bindings introduction](https://make.wordpress.org/core/2024/03/06/new-feature-the-block-bindings-api/) — release post

### Rule lineage
- Block Bindings API — WP 6.5 (March 2024) — major addition
- WP 6.6 — added editor binding picker UI
- WP 6.7 — extended to `core/button` href, `core/image` src

### Last reviewed
- 2026-04-29 — re-review on WP minor releases (API expanding rapidly)
