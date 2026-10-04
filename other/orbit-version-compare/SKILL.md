---
name: orbit-version-compare
description: Compare two versions of the same WordPress plugin (typically v(N-1).zip vs v(N).zip) — diffs PHPCS errors, asset weight, function adds/removes, hook adds/removes, and sets up the visual baseline diff for the new version. Use when the user says "v1 vs v2", "before vs after release", "diff two zips", "what changed since the last release", or runs the regression-pass workflow.
---

# 🪐 orbit-version-compare — Old version vs new version

The "what changed and is anything worse" check. Run before tagging any release.

---

## Quick start

```bash
bash ~/Claude/orbit/scripts/compare-versions.sh \
  --old ~/downloads/my-plugin-v2.3.zip \
  --new ~/downloads/my-plugin-v2.4.zip
```

Output: `reports/version-compare-<timestamp>.md`.

---

## What it diffs

| Check | What it shows |
|---|---|
| PHPCS errors | Δ count + new violations introduced |
| Asset weight | JS / CSS bundle size change |
| Functions added | Every new global function (good for changelog) |
| Functions removed | Removed functions still referenced in calling code? |
| Hooks added | New `add_action` / `add_filter` calls |
| Hooks removed | Removed hooks — back-compat risk |
| Classes added / removed | API-surface drift |
| Files added / removed | What's new, what's gone |
| Tests added | More coverage = good |
| Visual diff baseline | Sets up screenshot diff for new version |

---

## Example output

```
[Version Compare] my-plugin v2.3 → v2.4

PHPCS errors:
  v2.3:  12
  v2.4:   3            -9 (-75%)        ✓ Improved

Asset weight:
  JS    v2.3: 238 KB  →  v2.4: 287 KB    +49 KB (+20.6%)  ⚠ review
  CSS   v2.3:  42 KB  →  v2.4:  51 KB    +9 KB (+21.4%)   ⚠

Functions:
  Added (12):
    + my_plugin_render_block_v2()
    + my_plugin_get_settings_with_cache()
    ...
  Removed (2):
    - my_plugin_legacy_helper()    ⚠ still called in 3 places — back-compat risk
    - my_plugin_old_render()       ✓ unused

Hooks:
  Added (4):
    + 'my_plugin_pre_render' (filter)
    + 'my_plugin_post_save'  (action)
  Removed (1):
    - 'my_plugin_legacy_init'      ⚠ public hook removal — needs migration notice

Files:
  Added (3):  includes/class-block-v2.php, ...
  Removed (1): includes/class-legacy.php
  Modified (47)

Tests:
  v2.3:  142 specs
  v2.4:  168 specs                +26 (+18%)        ✓
```

---

## Visual baseline diff

After `compare-versions.sh`, set up the new version's visual baseline:

```bash
PLUGIN_PREV_TAG=v2.3.0 \
PLUGIN_VISUAL_URLS='["/wp-admin/admin.php?page=my-plugin","/wp-admin/admin.php?page=my-plugin-settings"]' \
  npx playwright test --project=visual-release
```

This:
1. `git checkout v2.3.0` → captures baselines from old version
2. `git checkout main` (or your current branch) → captures new screenshots
3. Diffs them
4. Restores HEAD

Any URL with > 2% pixel diff = unintended visual regression → review before release.

---

## Decision rules

| Diff | Action |
|---|---|
| PHPCS errors increased | Block release — fix new violations |
| Asset weight up > 10% | Review what added the bytes — `/orbit-bundle-analysis` |
| Removed function still called externally | Add a deprecation shim for one minor cycle |
| Removed hook (public) | Document in changelog; add migration guide |
| Visual diff > 2% on any URL | Confirm intentional or fix; never ship "we'll see" |

---

## Public API surface

If your plugin exposes hooks for theme / other-plugin developers, the **Removed Hooks** section is critical. Removing a public hook is a breaking change.

```php
// BAD — silently remove
// (in v2.3 you had:)
do_action( 'my_plugin_render_started' );
// (in v2.4 you removed it entirely)

// GOOD — deprecate first, remove later
do_action_deprecated(
  'my_plugin_render_started',
  [],
  '2.4',
  'my_plugin_pre_render',
  'Renamed for consistency. Will be removed in 3.0.'
);
```

`do_action_deprecated` and `apply_filters_deprecated` log warnings for theme/plugin authors who use the old hook, giving them time to migrate.

---

## Pair with `/orbit-changelog-test`

`compare-versions.sh` shows you **what changed**. `/orbit-changelog-test` builds a **test plan** for each changelog entry. Both run in `/orbit-release-gate`.

---

## Handy: a one-liner regression pass

```bash
# Before tagging v2.4, run from the plugin repo root:
git tag -l 'v*' | tail -1 | xargs -I {} \
  bash ~/Claude/orbit/scripts/compare-versions.sh --old-tag {} --new-current
```

Compares the latest tag against your current working tree — no need to build a zip first.
