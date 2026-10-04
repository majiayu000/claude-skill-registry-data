---
name: orbit-editor-perf
description: Editor performance harness for Elementor / Gutenberg / Beaver Builder / WPBakery — measures editor-ready time, widget panel populated, widget insert→render, memory growth after 20+ widgets, console error spam. Catches the perf bugs Lighthouse can't see (most addon plugin issues live here). Use when the user says "Elementor slow", "Gutenberg lag", "editor performance", "widget insert timing", "panel freezing".
---

# 🪐 orbit-editor-perf — Page-builder editor profiling

Most Elementor / Gutenberg addon bugs aren't on the frontend — they're in the editor. Slow widget insert, frozen panel, 200MB memory after 5 minutes. This skill catches them.

---

## Quick start

```bash
bash ~/Claude/orbit/scripts/editor-perf.sh
# → reports/editor-perf-<timestamp>.json
```

Or via gauntlet (Step 10):
```bash
bash scripts/gauntlet.sh --plugin . --mode full
```

---

## What it measures

| Metric | Target | Bad |
|---|---|---|
| **Editor ready time** (open-to-interactive) | < 3s | > 5s |
| **Widget panel populated** | < 500ms after ready | > 2s |
| **Widget insert → rendered in canvas** | < 300ms | > 1s |
| **Memory after 20 widgets inserted** | < 100MB growth | > 250MB |
| **Console error spam** (per session) | 0 | any |
| **Long tasks** (>50ms blocks main thread) | < 5 | > 20 |
| **Layout shift in editor** | < 0.05 | > 0.1 |

Each is a release-blocker if exceeded.

---

## Elementor-specific spec

```js
// tests/playwright/editor-perf/elementor.spec.js
test('Editor ready in <3s', async ({ page }) => {
  await page.goto('/wp-admin/post-new.php?post_type=page');
  const t0 = Date.now();
  await page.click('#elementor-switch-mode-button');
  await page.waitForSelector('#elementor-editor-wrapper', { state: 'visible' });
  await page.waitForFunction(() => window.elementor?.documents?.getCurrent());
  const ready = Date.now() - t0;
  console.log(`Editor ready: ${ready}ms`);
  expect(ready).toBeLessThan(3000);
});

test('Insert 20 of my widget — measure each', async ({ page }) => {
  await openElementorEditor(page);

  for (let i = 1; i <= 20; i++) {
    const t0 = Date.now();
    await page.dragAndDrop('#elementor-panel [data-widget="my-widget"]',
                          '#elementor-preview-iframe');
    await page.waitForFunction(() => document.querySelectorAll('.my-widget').length === i);
    const insertTime = Date.now() - t0;
    expect(insertTime).toBeLessThan(300);
  }

  // Check memory after the run
  const mem = await page.evaluate(() => performance.memory?.usedJSHeapSize);
  expect(mem).toBeLessThan(100 * 1024 * 1024);  // 100MB cap
});
```

---

## Gutenberg-specific spec

```js
test('Block panel ready < 2s', async ({ page }) => {
  await page.goto('/wp-admin/post-new.php');
  const t0 = Date.now();
  await page.click('button[aria-label="Toggle block inserter"]');
  await page.waitForSelector('.block-editor-inserter__menu');
  await page.waitForFunction(() =>
    document.querySelectorAll('.block-editor-block-types-list__item').length > 0
  );
  expect(Date.now() - t0).toBeLessThan(2000);
});

test('Insert my-block — render < 300ms', async ({ page }) => {
  // ... insert via REST or click ...
  const t0 = Date.now();
  await page.click('[data-type="my-plugin/my-block"]');
  await page.waitForSelector('.my-block-rendered');
  expect(Date.now() - t0).toBeLessThan(300);
});
```

---

## After-run analysis

Feed JSON to the perf skill:

```bash
claude "/orbit-wp-performance Analyze reports/editor-perf-*.json for ~/plugins/my-plugin. Rank widgets by insertMs, find heavy operations, suggest fixes."
```

Output: ranked widget list + suggested optimisations.

---

## Common findings + fixes

### Widget panel slow (>2s)
```php
// BAD — iterating all widgets, doing DB calls per widget
foreach ( $widgets as $w ) {
  $count = $wpdb->get_var( $wpdb->prepare( "...", $w['id'] ) );
}

// GOOD — single batched query
$counts = $wpdb->get_results( "SELECT id, COUNT(*) ...", OBJECT_K );
```

### Widget insert slow (>1s)
```js
// BAD — inserts trigger expensive remote API calls
elementor.hooks.addAction('panel/open_editor', () => fetch('/expensive-api'));

// GOOD — defer + cache
elementor.hooks.addAction('panel/open_editor', () => {
  if (cache) return; cache = fetch('/api').then(r => r.json());
});
```

### Memory leak (memory grows linearly with widget inserts)
```js
// BAD — event listener never removed
elementor.channels.editor.on('change', updateState);

// GOOD — remove on widget destroy
elementor.channels.editor.on('change', updateState);
this.destroy = () => elementor.channels.editor.off('change', updateState);
```

### Console spam (>0 plugin-specific errors)
Every error is a real bug. Use the Playwright console capture to find them:
```js
const errors = [];
page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
expect(errors.filter(e => e.includes('my-plugin'))).toHaveLength(0);
```

---

## Report

```json
{
  "editorReadyMs": 2840,
  "panelPopulatedMs": 412,
  "widgets": [
    { "name": "my-widget-1", "insertMs": 245, "renderMs": 180 },
    { "name": "my-widget-2", "insertMs": 1240, "renderMs": 980 }  ← slow
  ],
  "memoryGrowthMB": 42.7,
  "consoleErrors": [],
  "longTasks": [
    { "duration": 380, "name": "Render <my-widget-2>", "url": "..." }
  ]
}
```

---

## Pair with `/orbit-wp-performance`

This skill is **measurement** — it produces numbers. `/orbit-wp-performance` is **diagnosis** — it reads code and explains *why* the numbers are bad. Run both back-to-back when the harness flags a regression.
