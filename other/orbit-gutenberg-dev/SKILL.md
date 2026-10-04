---
name: orbit-gutenberg-dev
description: Block editor (Gutenberg) plugin development workflow audit — block.json schema, server-side render via render.php (apiVersion 3), edit-time JS in edit.js, block.json textdomain, supports config, attributes types, and the ServerSideRender deprecation path. Use when the user says "Gutenberg dev", "block development", "register a block", "apiVersion 3 migration", or before a release that adds/edits any Gutenberg block.
---

# 🪐 orbit-gutenberg-dev — Block development audit

The reviewer for "is this block plugin set up the way modern WP expects?" Read every block.json + render.php + edit.js, audit against the current Block Editor Handbook.

---

## Quick start

```bash
claude "/orbit-gutenberg-dev Audit ~/plugins/my-plugin's blocks for current best practices."
```

Output: `reports/gutenberg-dev-<timestamp>.md`.

---

## What it checks (whitepaper intent)

### 1. apiVersion is current (3 as of WP 6.5+)

**Why:** apiVersion 3 lets blocks use `viewScriptModule` for native ES modules and the Interactivity API. apiVersion 2 still works but is legacy. apiVersion 1 throws warnings in WP 6.5+.

```json
{ "apiVersion": 3, "name": "my-plugin/example" }
```

**Source:** [Block API Versions](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-api-versions/)

### 2. Server-side render preferred over JS save()

**Why:** Server-side render (`render: "file:./render.php"`) ships less JS, allows dynamic content, and survives content migrations. The old approach (defining `save()` in JS) freezes content into the post and breaks if you change the markup.

```json
{ "render": "file:./render.php" }
```

```php
// render.php
<div <?php echo get_block_wrapper_attributes(); ?>>
  <?php echo esc_html( $attributes['title'] ?? '' ); ?>
</div>
```

**Source:** [Dynamic blocks](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-metadata/#render)

### 3. block.json `supports` are explicit

**Why:** Default `supports` give you very little. Modern blocks declare what they support so the editor inspector renders the right controls.

```json
"supports": {
  "html": false,
  "align": ["wide", "full"],
  "anchor": true,
  "color": { "background": true, "text": true, "gradients": true },
  "spacing": { "padding": true, "margin": true, "blockGap": true },
  "typography": { "fontSize": true, "lineHeight": true },
  "shadow": true,
  "interactivity": true
}
```

### 4. textdomain matches plugin

**Why:** `block.json` titles + descriptions get auto-translated only if `textdomain` matches the plugin's text domain.

```json
{ "textdomain": "my-plugin" }
```

### 5. ServerSideRender component is ONLY a stop-gap

**Why:** `ServerSideRender` in edit.js is a render preview shortcut. Production blocks should use `render` field for output and a proper React `edit` component for the editor experience.

```jsx
// ❌ Lazy — re-renders via REST on every edit
import ServerSideRender from '@wordpress/server-side-render';

// ✅ Real edit component
export default function Edit({ attributes, setAttributes }) {
  return <div className="my-block-edit">...</div>;
}
```

### 6. Use modern @wordpress/scripts build

```bash
npm i -D @wordpress/scripts
# In package.json:
"scripts": {
  "build": "wp-scripts build",
  "start": "wp-scripts start"
}
```

Auto-generates `build/index.asset.php` for cache-busting + dependency manifest.

---

## Output

```markdown
# Gutenberg Dev Audit — [Plugin]

## Blocks discovered: 8

### my-plugin/example (blocks/example/block.json)
- apiVersion: 3 ✓
- render: file:./render.php ✓
- textdomain: my-plugin ✓
- supports: html=false, align=[wide,full], color=true, spacing=true ✓
- ⚠ Missing: shadow, interactivity (consider for WP 6.5+)

### my-plugin/legacy (blocks/legacy/block.json)
- apiVersion: 1 ❌ (deprecated — migrate to 3)
- save() in edit.js ❌ (migrate to render.php)
- supports.color: true (should be object) ⚠

[Continue for all blocks]
```

---

## Pair with

- `/orbit-block-render-test` — server-side render coverage
- `/orbit-block-edit-test` — Playwright tests for the editor experience
- `/orbit-block-json-validate` — schema-level validation
- `/orbit-fse-test` — full-site-editing compat
- `/orbit-block-bindings` — Block Bindings API (the modern way to add data sources)
- `/orbit-interactivity-api` — modern dynamic blocks without React-Editor JS

---

## Sources & Evergreen References

> **Always pull these before auditing** — the Block Editor evolves every WP minor release.

### Canonical docs (fetch on every run)
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/) — root of truth for everything Gutenberg
- [Block API Reference](https://developer.wordpress.org/block-editor/reference-guides/block-api/) — block.json schema
- [Dynamic Blocks](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-metadata/#render) — render.php pattern
- [@wordpress/scripts](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-scripts/) — build tooling
- [Make WordPress Core](https://make.wordpress.org/core/category/gutenberg/) — every release announcement

### Live data
- [block.json schema](https://schemas.wp.org/trunk/block.json) — JSON Schema, validate against this URL on every run
- [WP version registry](https://api.wordpress.org/core/version-check/1.7/) — current `Tested up to:` baseline

### Rule lineage
- apiVersion 3 — required for `viewScriptModule` (WP 6.5, March 2024)
- Render field — preferred since WP 5.8, mandatory style since WP 6.0
- Block Bindings API — WP 6.5 introduced, replaces custom render filters

### Last reviewed
- 2026-04-29 — by [the maintainers](https://github.com/adityaarsharma)
- Re-review trigger: any of (WP minor release · `wp-scripts` major bump · 90-day rolling)
- Stale rule? Open issue: [github.com/adityaarsharma/orbit/issues](https://github.com/adityaarsharma/orbit/issues)
