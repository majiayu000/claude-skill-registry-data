---
name: orbit-block-variations
description: Audit block variations — alternative configurations of an existing block (e.g. core/group's "Row" variation), `transforms` between blocks, and the variation picker UI in the inserter. Use when the user says "block variation", "registerBlockVariation", "transform between blocks", or has multiple similar custom blocks that should be variations of one.
---

# 🪐 orbit-block-variations — Block variations + transforms

Variations let one block do many things. Many plugins ship 5 nearly-identical blocks when one + 5 variations would be cleaner.

---

## Quick start

```bash
claude "/orbit-block-variations Audit ~/plugins/my-plugin for over-blocking — places where multiple blocks should be variations of one."
```

---

## What it checks

### 1. Variations registered in JS
```js
// edit.js or variations.js
import { registerBlockVariation } from '@wordpress/blocks';

registerBlockVariation( 'my-plugin/container', {
  name: 'card',
  title: __( 'Card', 'my-plugin' ),
  icon: 'card',
  attributes: { layout: 'card', padding: 'large' },
  innerBlocks: [
    [ 'core/heading', { level: 3 } ],
    [ 'core/paragraph' ],
  ],
  scope: [ 'inserter' ],  // also: 'block', 'transform'
} );
```

### 2. Use cases for variations vs separate blocks

| Use variation when | Use separate block when |
|---|---|
| Same render, different default attributes | Genuinely different render logic |
| Same edit UI | Different InspectorControls |
| Same allowed inner blocks | Different inner-block contracts |

### 3. Transform registered (so users can switch)
```json
// block.json
"transforms": {
  "from": [
    { "type": "block", "blocks": ["core/paragraph"], "transform": "..." }
  ],
  "to": [
    { "type": "block", "blocks": ["core/quote"], "transform": "..." }
  ]
}
```

### 4. Variation icons + labels are translatable
**Whitepaper intent:** Variations show up in the inserter with their `title`. Untranslated titles look amateur in non-English locales.

### 5. `scope: ['inserter']` for inserter-discoverable variations
Without `scope: ['inserter']`, the variation only shows up via "Transform to" — users won't find it via the block picker.

### 6. Default variation
```js
registerBlockVariation( 'my-plugin/container', {
  name: 'card',
  isDefault: true,  // makes this the default when block is inserted
  attributes: {},
} );
```

---

## Output

```markdown
# Block Variations Audit — my-plugin

## Variations registered: 4
- my-plugin/container — Card, Hero, Sidebar (3 variations)
- my-plugin/list — Numbered, Bullet (2 variations) — ✓ both have `scope: ['inserter']`

## Over-blocking candidates (consider migrating to variations)
- my-plugin/card-block + my-plugin/feature-card — 90% identical render. Merge as variations of `my-plugin/container`.

## Missing
- ⚠ my-plugin/list-numbered — registered as separate block, should be a variation
- ⚠ my-plugin/container — has no `isDefault` variation, inserter shows blank
```

---

## Pair with

- `/orbit-gutenberg-dev` — overall block audit
- `/orbit-block-patterns` — vs patterns (different concept, both reduce duplication)
- `/orbit-block-edit-test` — test variations work in the editor

---

## Sources & Evergreen References

### Canonical docs
- [Block Variations](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-variations/) — full reference
- [`registerBlockVariation()`](https://developer.wordpress.org/block-editor/reference-guides/data/data-core-blocks/#registerblockvariation) — JS API
- [Block Transforms](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-transforms/) — convert blocks

### Rule lineage
- Block Variations API — WP 5.4
- `scope` attribute — WP 5.8
- `isActive` (WP 6.0) — better default-detection

### Last reviewed
- 2026-04-29 — re-review on WP minor releases
