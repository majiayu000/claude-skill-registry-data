---
name: orbit-uat-elementor
description: UAT (User Acceptance Testing) template + Playwright spec scaffolds specifically for Elementor addon plugins — drag widget into editor, configure via inspector, save, verify frontend output, test responsive breakpoints, test live preview, test in Elementor Pro Theme Builder context. Use when the user says "UAT for Elementor", "test my Elementor widget", "Elementor end-to-end".
---

# 🪐 orbit-uat-elementor — Elementor addon UAT template

End-to-end UAT specs purpose-built for Elementor addons. Drag → configure → save → frontend → repeat.

---

## Quick start

```bash
PLUGIN_SLUG=my-elementor-addon \
  npx playwright test --project=uat-elementor
```

Or scaffold from scratch:
```bash
bash ~/Claude/orbit/scripts/scaffold-uat-elementor.sh ~/plugins/my-elementor-addon
```

---

## What the UAT covers

### 1. Editor flow
```js
test('Drag My Hero into a page', async ({ page }) => {
  // Login + create new page
  await page.goto('/wp-admin/post-new.php?post_type=page');
  await page.fill('#title', 'UAT Page');

  // Open Elementor editor
  await page.click('#elementor-switch-mode-button');
  await page.waitForFunction(() => window.elementor?.documents?.getCurrent());

  // Search panel for the widget
  await page.fill('#elementor-panel-search-input', 'My Hero');
  const widget = page.locator('[data-element_type="widget"][data-widget-type="my-hero"]').first();
  await expect(widget).toBeVisible();

  // Drag to canvas
  await widget.dragTo(page.locator('#elementor-preview-iframe').contentFrame().locator('.elementor-section-wrap'));

  // Verify in canvas
  const canvas = page.locator('#elementor-preview-iframe').contentFrame();
  await expect(canvas.locator('.my-hero')).toBeVisible();
});
```

### 2. Inspector control validation
- Every control declared in `register_controls()` works
- `selectors` cause live update in canvas
- Conditional controls show/hide correctly

### 3. Responsive breakpoints
```js
// Switch to mobile view
await page.click('button[data-tooltip="Mobile"]');
// Verify mobile-specific control changes apply
```

### 4. Save + view frontend
```js
await page.click('#elementor-panel-saver-button-publish');
await page.waitForSelector('.elementor-saver-success');

await page.goto('/uat-page/');
await expect(page.locator('.my-hero')).toBeVisible();
await expect(page.locator('.my-hero h2')).toContainText('Hello');
```

### 5. Theme Builder context (if Pro)
Test the widget inside a Theme Builder template (header / footer / single template).

### 6. Console error guard
```js
const errors = [];
page.on('console', msg => msg.type() === 'error' && errors.push(msg.text()));
expect(errors.filter(e => e.includes('my-elementor-addon'))).toHaveLength(0);
```

### 7. Common edge cases
- Widget on a page with NO Elementor — fallback render?
- Widget with EMPTY attributes — graceful render or "configure me"?
- Widget on a draft preview vs published page
- Widget inside a Container (3.6+) vs Section/Column

---

## Output

```markdown
# Elementor UAT — my-elementor-addon

## Suite: 24 tests, 22 passed, 2 failed

❌ "Drag Hero — verify in canvas" — widget not found in panel after fresh activation
   → InspectorControls registered but get_categories() returns invalid category

❌ "Mobile breakpoint — padding" — mobile padding not respected
   → selectors use {{WRAPPER}} but missing for mobile-specific control

✓ Save + frontend — passes
✓ Console errors — 0 plugin-specific errors
```

---

## Pair with

- `/orbit-elementor-dev` — code-side audit
- `/orbit-elementor-controls` — control implementation
- `/orbit-uat-compare` — vs competitor Elementor addons

---

## Sources & Evergreen References

### Canonical docs
- [Elementor Editor Internals](https://github.com/elementor/elementor/tree/main/assets/dev/js/editor) — Editor V3 source
- [Playwright + WordPress](https://playwright.dev/docs/intro) — base patterns
- [Test Selectors Guide](https://developers.elementor.com/docs/widgets/widget-controls/) — `data-element_type`, `data-widget-type`

### Rule lineage
- Editor selectors stable since Elementor 3.0 (older addons may target deprecated selectors)
- Container layout selectors — Elementor 3.6+

### Last reviewed
- 2026-04-29 — re-review on Elementor Editor V4 release (will change DOM)
