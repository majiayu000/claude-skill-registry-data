---
name: superpowers-sage:wp-block-native
description: >
  Native Gutenberg blocks without ACF — block.json, edit.js, save.js,
  register_block_type, @wordpress/scripts, block attributes, InnerBlocks,
  useBlockProps, ServerSideRender, dynamic blocks PHP render_callback,
  block supports, block.json apiVersion 3, block variations, block styles,
  block transforms, React in block editor, wp_register_block_script_handle,
  Vite and WordPress blocks, native block vs ACF Composer block decision,
  block.json editorScript viewScript, @wordpress/block-editor
user-invocable: false
---
# Native WordPress Block Development

## When to use

When building editor blocks that require capabilities beyond what ACF Composer provides: InnerBlocks nesting, block transforms, block variations, JS-heavy editor UI, or block deprecations. Also use when you need fine-grained control over the editor experience or when a block's primary complexity is in its editor behavior rather than its field configuration.

## Inputs required

- The block's purpose and editor behavior requirements
- Whether ACF Composer could handle it (use the decision table below)
- Target WordPress version (determines apiVersion and available block supports)
- Whether the block needs InnerBlocks, transforms, or deprecations

## Procedure

### 1. Decision table: ACF Composer vs Native blocks

| Requirement | ACF Composer | Native Block |
|---|---|---|
| Complex field groups (repeaters, flexible content) | Best choice | Avoid |
| InnerBlocks (nested block areas) | Not supported | Required |
| Block transforms (convert between block types) | Not supported | Required |
| Block variations (same block, different presets) | Limited | Full support |
| JS-heavy editor controls | Limited | Full support |
| Block deprecations (safe markup changes) | Not applicable | Required |
| Quick data-entry blocks | Best choice | Overkill |

**Both can coexist in the same project.** ACF blocks and native blocks appear side by side in the inserter.

### 2. Block structure in a Sage project

```
resources/
  scripts/
    editor/
      blocks/
        hero/
          index.js          # Block registration (edit + save)
          edit.js            # Editor component
          save.js            # Save component (or null for dynamic)
          style.css          # Front-end styles
          editor.css         # Editor-only styles
          block.json        # Block metadata
```

### 3. block.json

See [`references/block-json-native.md`](references/block-json-native.md) for full field reference and attribute source types.

Use apiVersion 3 for WordPress 6.3+. Key fields: `name`, `attributes`, `supports`, `editorScript`, `render`.

### 4. edit and save functions

See [`references/edit-save.md`](references/edit-save.md) for complete `edit`/`save` examples, deprecations, and `ServerSideRender`.

- `edit` — React component; interactive; output not stored
- `save` — pure function; stored HTML; must match on re-parse
- Add deprecations whenever saved markup changes

### 5. Dynamic blocks (PHP render)

See [`references/dynamic-blocks.md`](references/dynamic-blocks.md) for PHP render templates, Blade integration, and InnerBlocks with dynamic rendering.

For blocks that query WordPress data, set `save: () => null` and use the `render` field in block.json:

```php
// render.php — receives $attributes, $content, $block
<div <?php echo get_block_wrapper_attributes(['class' => 'hero']); ?>>
    <?php echo $content; ?>
</div>
```

### 6. Vite integration

See [`references/vite-integration.md`](references/vite-integration.md) for Vite configuration, `@wordpress/*` externals, and the single-bundle vs per-block entry pattern.

Key: declare `@wordpress/*` packages as externals in Vite — do not bundle them. Enqueue via `enqueue_block_editor_assets`:

```php
add_action('enqueue_block_editor_assets', function () {
    wp_enqueue_script(
        'sage-editor-blocks',
        Vite::asset('resources/scripts/editor/index.js'),
        ['wp-blocks', 'wp-element', 'wp-block-editor', 'wp-components'],
        null,
        true
    );
});
```

### 7. InnerBlocks

```jsx
import { useBlockProps, useInnerBlocksProps } from '@wordpress/block-editor';

export default function Edit() {
    const blockProps = useBlockProps({ className: 'card-grid' });
    const innerBlocksProps = useInnerBlocksProps(blockProps, {
        allowedBlocks: ['sage/card', 'core/paragraph'],
        template: [['sage/card', {}], ['sage/card', {}]],
        templateLock: false,
    });
    return <div {...innerBlocksProps} />;
}
```

## Verification

1. Block appears in the editor inserter under the correct category.
2. Block renders correctly in the editor (edit component).
3. Block saves without validation errors (save component matches output).
4. Block renders correctly on the front end (PHP render or saved HTML).
5. Block supports (color, spacing, typography) apply styles correctly.
6. Deprecations: edit a post with an old version of the block, update the block code, and confirm the editor recovers gracefully.
7. InnerBlocks: child blocks can be added, removed, and reordered within the parent.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| "This block contains unexpected or invalid content" | Save function output does not match stored HTML | Fix save function or add a deprecation |
| Block not appearing in inserter | block.json not found or editor script not enqueued | Check file paths and script registration |
| Styles not applying | Missing `get_block_wrapper_attributes()` or `useBlockProps()` | Block supports require these wrappers |
| InnerBlocks empty on front end | `$content` variable not echoed in render template | Add `echo $content` to PHP render |
| Editor script errors | Missing WordPress script dependencies | Ensure `wp-blocks`, `wp-element`, `wp-block-editor` are listed as dependencies |

## Escalation

- If block deprecations are not recovering old content, check that the deprecated `save` function exactly reproduces the old output. Use browser console to compare expected vs actual HTML.
- If `register_block_type()` silently fails, enable `WP_DEBUG` and check for errors. Common cause: invalid block.json syntax or missing required fields.
- When the editor experience requires extensive custom JS, consider whether a plugin-based approach might be cleaner than embedding everything in the theme.
