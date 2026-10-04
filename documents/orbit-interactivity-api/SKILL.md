---
name: orbit-interactivity-api
description: Audit Interactivity API usage (WP 6.5+) — the modern way to add client-side dynamic behaviour to blocks without bundling React for the frontend. Catches plugins still using vanilla JS / jQuery / custom React mounts that should migrate. Use when the user says "Interactivity API", "wp-interactive", "modern dynamic block", "replace jQuery in block", or "frontend block JS".
---

# 🪐 orbit-interactivity-api — Modern client-side block behaviour

WP 6.5 ships the Interactivity API — declarative, lightweight, no React on frontend. Plugins shipping a Like button still using jQuery in 2026 are leaving performance on the table.

---

## Quick start

```bash
claude "/orbit-interactivity-api Audit ~/plugins/my-plugin for blocks that should adopt the Interactivity API."
```

---

## What it checks

### 1. Block declares `interactivity` support
```json
"supports": { "interactivity": true }
```

### 2. `viewScriptModule` (apiVersion 3 + ES module)
```json
"viewScriptModule": "file:./view.js"
```

### 3. Directives in markup
```php
// render.php
<button
  data-wp-on--click="actions.toggle"
  data-wp-class--is-open="state.isOpen"
>
  Toggle
</button>
```

### 4. Store registered in JS
```js
// view.js
import { store, getContext } from '@wordpress/interactivity';

store( 'my-plugin', {
  state: { isOpen: false },
  actions: {
    toggle() {
      const ctx = getContext();
      ctx.isOpen = !ctx.isOpen;
    },
  },
} );
```

### 5. Legacy patterns to migrate
**Whitepaper intent:** Loading jQuery for a single block adds ~30KB + render-blocking. Interactivity API ships ~4KB minified, runs after first paint, and integrates with WP server state.

```js
// ❌ Legacy — separate jQuery script, custom event binding, global handler
jQuery( '.my-block-toggle' ).on( 'click', function() { ... } );

// ✅ Interactivity API
data-wp-on--click="actions.toggle"
```

---

## Output

```markdown
# Interactivity API Audit — my-plugin

## Blocks with interactivity: 1/8 (12%)

### Migrate candidates
- my-plugin/accordion (assets/js/accordion.js — 320 LOC of vanilla JS)
- my-plugin/tabs (assets/js/tabs.js — 240 LOC)
- my-plugin/slider (assets/js/slider.js — uses jQuery + Slick)

### Already migrated
- ✓ my-plugin/like-button — uses Interactivity API ✓

### Recommendation
Migrating 3 blocks would drop ~80KB from frontend bundle and remove jQuery dependency.
Estimated effort: 4-6 hours per block.
```

---

## Pair with

- `/orbit-block-bindings` — server-side data binding
- `/orbit-bundle-analysis` — measure JS savings after migration
- `/orbit-gutenberg-dev` — overall block audit

---

## Sources & Evergreen References

### Canonical docs
- [Interactivity API](https://developer.wordpress.org/block-editor/reference-guides/interactivity-api/) — root reference
- [@wordpress/interactivity package](https://www.npmjs.com/package/@wordpress/interactivity) — store API
- [Directives reference](https://developer.wordpress.org/block-editor/reference-guides/interactivity-api/api-reference/) — `data-wp-*`
- [Migrating to Interactivity API](https://developer.wordpress.org/news/2024/04/03/from-the-frontend-of-a-block-to-interactivity-api/) — migration tutorial

### Rule lineage
- Interactivity API — WP 6.5 (March 2024)
- Native ES modules (`viewScriptModule`) — WP 6.5
- Server state hydration — WP 6.6 added `wp_interactivity_state()`

### Last reviewed
- 2026-04-29 — re-review on WP minor (API stabilising but new directives still being added)
