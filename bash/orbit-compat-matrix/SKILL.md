---
name: orbit-compat-matrix
description: Multi-version compatibility matrix for a WordPress plugin — runs the gauntlet against PHP 7.4 / 8.1 / 8.3 / 8.5 × WP 6.3 / 6.5 / latest, plus modern-WP feature adoption check (block-template-parts, theme.json schema 3, Interactivity API, etc.). Use when the user says "PHP 7.4 vs 8.x", "WP 6.5 compat", "compatibility matrix", "drop PHP 7 support", "after WP core update", or before bumping `Requires PHP:` / `Requires at least:` in the plugin header.
---

# 🪐 orbit-compat-matrix — PHP × WP version testing

Your plugin runs on the user's site, not yours. Test every version your `Requires PHP:` and `Requires at least:` claim to support.

---

## Quick start — full matrix

```bash
# Auto: runs gauntlet against PHP 7.4 / 8.1 / 8.3 + WP 6.3 / 6.5 / latest
bash ~/Claude/orbit/scripts/gauntlet.sh --plugin . --mode full --matrix

# Manual: explicit versions
for php in 7.4 8.1 8.3 8.5; do
  for wp in 6.3 6.5 latest; do
    WP_PHP_VERSION=$php WP_VERSION=$wp \
      bash scripts/gauntlet.sh --plugin . --mode full
    mv reports reports-php${php}-wp${wp}
  done
done
```

Output: one report set per (PHP, WP) combination. Compare to find version-specific failures.

---

## Phase 1 — Static PHP compatibility

Without booting WP, scan every PHP file for syntax that's invalid on a target version:

```bash
bash ~/Claude/orbit/scripts/check-php-compat.sh ~/plugins/my-plugin
```

Catches:
- PHP 8.0+ named arguments used in 7.4 codebase
- PHP 8.1+ `readonly` properties used where 7.4 support claimed
- PHP 8.2+ `#[\Override]` attribute
- PHP 8.0+ match expressions
- Removed APIs: `each()`, `create_function()`, `mb_ereg_replace_callback` flag

Powered by `phpcompatibility/phpcompatibility-wp` (PHPCS sniffs).

---

## Phase 2 — Modern WP feature adoption

```bash
bash ~/Claude/orbit/scripts/check-modern-wp.sh ~/plugins/my-plugin
```

Reports both:
- **Incompatibilities** with current `Requires at least:`
- **Modernization opportunities** — features your version supports but you're not using

Examples of modernisation flags:
- WP 6.5+: `block.json` `viewScriptModule` for native ES modules
- WP 6.5+: Block Bindings API (avoid custom render filters)
- WP 6.4+: Interactivity API for dynamic blocks (replaces vanilla JS)
- WP 6.3+: `theme.json` schema 3 features
- WP 6.0+: Block patterns (replaces hardcoded HTML in shortcodes)

---

## Phase 3 — Live multi-version gauntlet

```bash
# Spin up multiple wp-env sites in parallel
for ph in 7.4 8.1 8.3; do
  for wp in 6.3 6.5 latest; do
    port=$((8880 + RANDOM % 100))
    bash scripts/create-test-site.sh --plugin . --port $port \
      --php $ph --wp $wp &
  done
done
wait

# Run gauntlet against each
# (the --matrix flag automates this)
bash scripts/gauntlet.sh --plugin . --mode full --matrix
```

Reports written to `reports-matrix/php<x>-wp<y>/`.

---

## Decision rules — bump or hold

After matrix:

| Failures across | Action |
|---|---|
| All PHP 7.4 runs only | Either fix the 7.4-specific bugs or bump `Requires PHP: 8.0` |
| Latest WP only | Compatibility issue with new WP core — file a Trac ticket if it's a regression, fix forward otherwise |
| One specific cell (PHP 8.1 + WP 6.3) | Edge case — check changelog of dependency between those versions |
| Random / flaky | Re-run on isolated site — likely test setup, not real bug |

---

## Bumping minimum PHP — checklist

Before changing `Requires PHP: 7.4` → `8.0` in your plugin header:

```bash
# 1. See what 7.4 features you'd gain by dropping
bash scripts/check-php-compat.sh . --target 8.0
# → Lists: typed properties, named args, nullsafe, etc.

# 2. Run full matrix with new floor
bash scripts/gauntlet.sh --plugin . --mode full --matrix --min-php 8.0

# 3. Update plugin header + readme.txt
# Plugin Name: My Plugin
# Requires PHP: 8.0      ← bumped

# 4. Add upgrade notice in readme.txt:
== Upgrade Notice ==
= 2.0 =
This release requires PHP 8.0+. If your site runs PHP 7.x,
update PHP via your host or stay on 1.x.

# 5. Notify users via in-plugin admin notice for one minor cycle BEFORE removing 7.x support
```

---

## After WP core releases

When WordPress 6.X or 7.X drops:

```bash
# 1. Check if existing API calls are deprecated
bash scripts/check-wp-compat.sh .

# 2. Spin up test site on the new version
bash scripts/create-test-site.sh --plugin . --port 8881 --wp 6.6

# 3. Run full gauntlet
bash scripts/gauntlet.sh --plugin . --mode full

# 4. If clean → bump `Tested up to:` in plugin header + readme.txt
# 5. If issues → patch + emergency release
```

`Tested up to:` should always be the latest stable WP. WP.org demotes plugins where it's > 2 versions stale.

---

## Common compatibility gotchas

### `array_filter` callback signature
PHP 7.4 vs 8.1 — same code, different behaviour with `null` callback. Test both.

### `WP_Query` `meta_query` operators
Some operators added in WP 5.x that fail silently on older versions. If your plugin claims `Requires at least: 5.0`, verify.

### Block API version
WP 6.5 expects `apiVersion: 3` in block.json. WP 6.0 only supports `apiVersion: 2`. If you set 3, you must also bump `Requires at least: 6.5`.

### REST API namespace conflicts
WP 6.4+ enforces stricter namespace validation. Old plugins with namespace `myplugin` (no slash, no version) get warnings.

### HPOS (WooCommerce)
WC 8.x flipped HPOS to default. Plugins reading `wp_posts` directly for orders break. Declare `wc_hpos_compatible` in plugin header — see `/orbit-block-json-validate` (covers HPOS too).

---

## Output

`reports-matrix/` (one folder per cell):

```
reports-matrix/
├── php7.4-wp6.3/qa-report-*.md
├── php7.4-wp6.5/qa-report-*.md
├── php7.4-wp-latest/qa-report-*.md
├── php8.1-wp6.3/qa-report-*.md
├── php8.1-wp6.5/qa-report-*.md
├── php8.1-wp-latest/qa-report-*.md
├── php8.3-wp6.3/qa-report-*.md
├── php8.3-wp6.5/qa-report-*.md
├── php8.3-wp-latest/qa-report-*.md
└── matrix-summary.html        ← generated last — green/red per cell
```

The summary HTML shows a 4×3 grid — one click on any red cell jumps to its full report.
