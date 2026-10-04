---
name: orbit-conflict-matrix
description: Test a WordPress plugin against the top 20 most-installed WP plugins (Yoast, RankMath, WooCommerce, Elementor, Jetpack, UpdraftPlus, W3 Total Cache, WPForms, Contact Form 7, etc.) — one at a time, in isolation, looking for conflicts. Use when the user says "test plugin conflicts", "vs Yoast / WooCommerce", "compatibility with top plugins", "before major release", or has a customer report of "X plugin breaks when Y is active".
---

# 🪐 orbit-conflict-matrix — Top 20 WP plugin conflict tests

The other plugins your customers run alongside yours. If yours breaks any of them — or breaks because of them — you'll get the bug report. This skill catches it first.

---

## Quick start

```bash
PLUGIN_SLUG=my-plugin \
  npx playwright test --project=conflict
```

Runs your plugin's smoke spec against each of the top 20 plugins, one at a time. Output:

```
[Conflict] Yoast SEO          ✅ pass
[Conflict] RankMath           ✅ pass
[Conflict] WooCommerce        ❌ FAIL — admin page errors when WooCommerce active
[Conflict] Elementor          ✅ pass
[Conflict] Jetpack            ✅ pass
[Conflict] UpdraftPlus        ✅ pass
...
```

---

## Top 20 tested by default

| # | Plugin | Slug |
|---|---|---|
| 1 | Yoast SEO | `wordpress-seo` |
| 2 | RankMath SEO | `seo-by-rank-math` |
| 3 | WooCommerce | `woocommerce` |
| 4 | Elementor | `elementor` |
| 5 | Jetpack | `jetpack` |
| 6 | UpdraftPlus | `updraftplus` |
| 7 | Contact Form 7 | `contact-form-7` |
| 8 | WPForms Lite | `wpforms-lite` |
| 9 | Wordfence | `wordfence` |
| 10 | Smush | `wp-smushit` |
| 11 | W3 Total Cache | `w3-total-cache` |
| 12 | LiteSpeed Cache | `litespeed-cache` |
| 13 | All in One SEO | `all-in-one-seo-pack` |
| 14 | TablePress | `tablepress` |
| 15 | Akismet | `akismet` |
| 16 | Classic Editor | `classic-editor` |
| 17 | Advanced Custom Fields | `advanced-custom-fields` |
| 18 | MonsterInsights | `google-analytics-for-wordpress` |
| 19 | LearnDash | `sfwd-lms` (or BuddyBoss for community) |
| 20 | bbPress | `bbpress` |

Configurable in `qa.config.json`:

```json
{
  "conflictMatrix": {
    "plugins": ["wordpress-seo", "woocommerce", "elementor", ...],
    "skip": ["jetpack"],          // exclude specific
    "extraPlugins": ["my-other-plugin"]  // add custom
  }
}
```

---

## How it works

For each plugin in the matrix:
1. Spin up a fresh wp-env site (port = 8881 + i)
2. Install + activate the conflict plugin via `wp plugin install <slug> --activate`
3. Activate your plugin
4. Run your smoke spec (`tests/playwright/<your-plugin>/core.spec.js`)
5. Mark pass / fail
6. Tear down

Total time: ~30 seconds per conflict × 20 = **~10 minutes** for the full matrix.

Parallelism: configurable. Default 3 sites at once (CPU-throttled).

---

## What "fail" means

A conflict-matrix failure is one of:

| Signal | Likely cause |
|---|---|
| PHP fatal in `error_log` | Function name collision (your prefix vs theirs) |
| Admin page 500 | Hook conflict — both plugins on `init` doing incompatible things |
| Frontend 500 | Same — or shortcode collision |
| Console JS error | Asset enqueue order / global pollution |
| Visual regression | CSS specificity war |
| Save fails silently | Ajax handler conflict |
| Feature missing | Their plugin removes a hook yours depends on |

---

## Decision rules

| Failure with | Action |
|---|---|
| Top-5 plugin (Yoast, RankMath, WC, Elementor, Jetpack) | **Block release** — these are on millions of sites |
| Top 20 (rest) | Document in upgrade notice + readme.txt — known conflict |
| Long-tail / rare | Log + defer |

---

## Verbose mode — see what failed

```bash
PLUGIN_SLUG=my-plugin \
DEBUG_CONFLICT=1 \
  npx playwright test --project=conflict
```

Output includes:
- Screenshot of the failing admin page
- PHP error log from the wp-env container
- JS console capture
- Network requests during the failure

Save these to `reports/conflicts/<conflict-plugin>/` for the bug report.

---

## Add a custom conflict to test

Real-world: a customer reports "your plugin breaks when ACME-Plugin is active". Reproduce locally:

```bash
# 1. Add to qa.config.json
{
  "conflictMatrix": {
    "extraPlugins": ["acme-plugin"]
  }
}

# 2. Run just that conflict
CONFLICT_PLUGIN=acme-plugin npx playwright test --project=conflict
```

Now you have a reproducible test. Fix the conflict, the test stays — guarding against regression.

---

## Common conflicts and fixes

### Asset enqueue order
```php
// Your plugin loads jQuery 3.x — they expect 1.x via no-conflict mode
add_action( 'wp_enqueue_scripts', 'my_plugin_assets', 999 ); // High priority
```

### Function name collision
```php
// BAD — generic function name, will collide
function get_settings() { ... }

// GOOD — prefix everything
function myplugin_get_settings() { ... }
```

### Hook race condition
```php
// BAD — runs at default priority, may race with WC
add_action( 'init', 'my_plugin_init' );

// GOOD — explicit priority based on what we depend on
add_action( 'init', 'my_plugin_init', 20 ); // After WC's priority 10
```

### Global JS conflict
```js
// BAD — pollutes window
window.MyPlugin = { ... };

// GOOD — namespaced, IIFE'd
( function( $ ) {
  const MyPlugin = { ... };
  window.MyPluginNS = window.MyPluginNS || {};
  window.MyPluginNS.MyPlugin = MyPlugin;
}( jQuery ) );
```

---

## Output

`reports/conflict-matrix-<timestamp>.md`:

```markdown
# Conflict Matrix — [Plugin]

## Summary
- Tested against: 20 plugins
- Passed: 18
- Failed: 2 (1 critical, 1 medium)

## Critical

### WooCommerce
**Symptom:** Admin page 500 when both active
**Trigger:** Save settings on `/wp-admin/admin.php?page=my-plugin`
**Fatal:** `Cannot redeclare get_settings() (previously declared in vendor/woocommerce/...)`
**Fix:** Rename `get_settings()` → `myplugin_get_settings()` everywhere.

## Medium

### Wordfence
**Symptom:** False-positive firewall block on save
**Cause:** Wordfence sees AJAX call without nonce header
**Fix:** Add nonce to AJAX call (already required by WP standards) — ensures Wordfence treats it as legit.
```

---

## CI

```yaml
- run: PLUGIN_SLUG=my-plugin npx playwright test --project=conflict
- if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: conflict-failures
    path: reports/conflicts/
```

Useful as a **monthly cron**, not every commit — the matrix takes 10 min and the conflict landscape rarely changes.
