---
name: orbit-uat-gutenberg
description: UAT (User Acceptance Testing) template + Playwright spec scaffolds for Gutenberg block plugins — insert via inserter, configure via InspectorControls, save post, verify frontend render, test inside reusable patterns + synced patterns, test transforms, test in Site Editor template context. Use when the user says "UAT for Gutenberg", "block plugin UAT", "test my block end-to-end".
---

# 🪐 orbit-uat-gutenberg — Gutenberg block plugin UAT

End-to-end UAT for block plugins. Insert → configure → save → frontend → repeat across viewports + Site Editor.

---

## Quick start

```bash
PLUGIN_SLUG=my-block-plugin npx playwright test --project=uat-gutenberg
```

Uses `@wordpress/e2e-test-utils-playwright` — the official Gutenberg test utils.

---

## What the UAT covers

### 1. Insert via block inserter
```js
import { test, expect } from '@wordpress/e2e-test-utils-playwright';

test('Insert my-plugin/example', async ({ admin, editor, page }) => {
  await admin.createNewPost();
  await editor.insertBlock({ name: 'my-plugin/example' });
  await expect(page.locator('[data-type="my-plugin/example"]')).toBeVisible();
});
```

### 2. Configure attributes via inspector
```js
await page.getByRole('textbox', { name: 'Title' }).fill('Hello UAT');
await page.getByRole('button', { name: 'Color: Background' }).click();
await page.getByRole('option', { name: 'Vivid Cyan Blue' }).click();
```

### 3. Save + verify frontend
```js
const postId = await editor.publishPost();
await page.goto(`/?p=${postId}`);
await expect(page.locator('.wp-block-my-plugin-example')).toContainText('Hello UAT');
```

### 4. Inside a pattern
```js
await editor.insertPattern({ name: 'my-plugin/hero' });
await expect(editor.canvas.locator('.wp-block-my-plugin-example')).toBeVisible();
```

### 5. Inside Site Editor (FSE templates)
```js
await page.goto('/wp-admin/site-editor.php');
// Edit the single template
await editor.insertBlock({ name: 'my-plugin/example' });
await page.click('button:has-text("Save")');
```

### 6. Block transforms
```js
await editor.transformBlockTo('core/paragraph');
await expect(page.locator('p[data-block]')).toBeVisible();
```

### 7. Console error guard
Same pattern as Elementor UAT — fail any test producing plugin-specific console errors.

### 8. Edge cases
- Block on a page in REST API context (preview via `?preview=true`)
- Block with empty/null attributes
- Block inside Query Loop (`core/query`)
- Block inside Reusable / Synced Pattern
- Block in classic-editor Convert-to-Blocks flow

---

## Output

```markdown
# Gutenberg UAT — my-block-plugin

## 28 tests, 26 passed, 2 failed

❌ "Inside Query Loop" — block doesn't render in loop context
   → render.php uses get_the_ID() but needs get_the_ID() inside loop

❌ "Synced pattern propagation" — edit in one place doesn't update others
   → block uses static save() instead of render.php
```

---

## Pair with

- `/orbit-gutenberg-dev` — code audit
- `/orbit-block-render-test` — frontend output
- `/orbit-block-edit-test` — editor experience
- `/orbit-fse-test` — Site Editor compat

---

## Sources & Evergreen References

### Canonical docs
- [@wordpress/e2e-test-utils-playwright](https://github.com/WordPress/gutenberg/tree/trunk/packages/e2e-test-utils-playwright) — official utils
- [E2E Testing Guide](https://developer.wordpress.org/block-editor/contributors/code/e2e/) — Gutenberg's own approach
- [Test Patterns Repo](https://github.com/WordPress/gutenberg/tree/trunk/test/e2e) — examples

### Rule lineage
- e2e-test-utils-playwright stable since WP 6.4
- Pattern API for testing — WP 6.0+

### Last reviewed
- 2026-04-29 — re-review on @wordpress/scripts major release
