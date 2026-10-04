---
name: orbit-compat-acf
description: ACF (Advanced Custom Fields) integration audit — get_field / the_field usage, ACF Blocks (Gutenberg), Field Groups loaded via PHP / JSON sync, ACF location rules, REST API exposure, ACF + Polylang/WPML interactions. Use when the user says "ACF compat", "Advanced Custom Fields integration", "ACF block", "get_field usage".
---

# 🪐 orbit-compat-acf — ACF integration

ACF is on 2M+ sites and is the de-facto custom-fields plugin. Plugins integrating with ACF (or that ship ACF Blocks) need careful handling.

---

## What this skill checks

### 1. get_field()/the_field() defensive use
**Whitepaper intent:** `get_field()` returns `false` if ACF isn't active. Plugins assuming a value crash. Always check `function_exists`:

```php
// ❌ Crashes if ACF deactivated
$price = get_field( 'price' );

// ✅
$price = function_exists( 'get_field' ) ? get_field( 'price' ) : null;
```

### 2. ACF Blocks (Gutenberg)
ACF can register Gutenberg blocks via PHP. Modern (5.8+) approach uses block.json + a render callback.

```php
register_block_type( __DIR__ . '/blocks/my-block/block.json', [
  'render_callback' => 'my_plugin_render_block',
] );
```

**Whitepaper intent:** ACF Blocks bypass the JS edit/save split — render is server-side. Pair perfectly with the WP Block Bindings approach.

### 3. Field Group registration — PHP vs JSON sync
- **PHP-registered groups** ship with the plugin code (recommended for plugin distribution)
- **JSON sync** auto-saves admin UI changes to disk (useful in dev workflows)

```php
acf_add_local_field_group([
  'key' => 'group_my_plugin_main',
  'title' => 'My Plugin Settings',
  'fields' => [
    [ 'key' => 'field_x', 'label' => 'X', 'name' => 'x', 'type' => 'text' ],
  ],
  'location' => [[
    [ 'param' => 'post_type', 'operator' => '==', 'value' => 'post' ],
  ]],
]);
```

### 4. REST API exposure
ACF fields aren't in REST by default. Set `show_in_rest` on each field (ACF 5.11+):
```php
'show_in_rest' => true,
```

Without this, your plugin's REST endpoints can't return ACF data.

### 5. ACF + WPML/Polylang
ACF fields can be marked "translate" via WPML / Polylang. Your plugin's docs should mention:
- Which fields to translate
- Which fields to copy (not translate)

### 6. Pro features
ACF Pro adds: Repeater, Flexible Content, Gallery, Clone, Options Pages. If your plugin requires Pro features, declare it.

### 7. ACF Blocks v3 (ACF 6.x)
ACF Blocks v3 (~ACF 6.0) is closer to native Gutenberg blocks. Your plugin's blocks should use v3 mode:
```json
"acf": { "mode": "preview" }
```

---

## Output

```markdown
# ACF Compat — my-plugin

✓ All get_field calls guarded by function_exists
⚠ Field group registered via JSON sync — recommend PHP for distribution
✓ ACF Blocks use v3 mode + block.json
⚠ Custom field "price" not exposed in REST (`show_in_rest: false`)
   → REST endpoint returns null for price; either expose or document
```

---

## Pair with

- `/orbit-gutenberg-dev` — block dev (ACF blocks are still blocks)
- `/orbit-compat-wpml` / `/orbit-compat-polylang` — translation
- `/orbit-rest-fuzzer` — REST endpoints exposing ACF data

---

## Sources & Evergreen References

### Canonical docs
- [ACF Documentation](https://www.advancedcustomfields.com/resources/) — root
- [ACF Functions](https://www.advancedcustomfields.com/resources/functions/) — `get_field` etc.
- [ACF Blocks](https://www.advancedcustomfields.com/resources/blocks/) — block registration
- [Local JSON](https://www.advancedcustomfields.com/resources/local-json/) — sync to disk

### Last reviewed
- 2026-04-29
