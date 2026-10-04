---
name: orbit-release-meta
description: Validate the release metadata of a WordPress plugin — plugin header completeness, readme.txt validity (Stable tag, Tested up to, Requires PHP), version parity across all files, license compliance (GPL-compatible), POT file freshness, RTL stylesheet presence. Use when the user says "validate plugin header", "readme.txt check", "version parity", "Stable tag mismatch", "license check", or before tagging any release.
---

# 🪐 orbit-release-meta — Release metadata validator

The metadata WP.org rejects on. Catches it before you submit.

---

## Quick start — run all checks

```bash
bash ~/Claude/orbit/scripts/check-plugin-header.sh ~/plugins/my-plugin
bash ~/Claude/orbit/scripts/check-readme-txt.sh ~/plugins/my-plugin
bash ~/Claude/orbit/scripts/check-version-parity.sh ~/plugins/my-plugin v2.4.0
bash ~/Claude/orbit/scripts/check-license.sh ~/plugins/my-plugin
bash ~/Claude/orbit/scripts/check-pot-file.sh ~/plugins/my-plugin
bash ~/Claude/orbit/scripts/check-rtl-readiness.sh ~/plugins/my-plugin
```

Or via gauntlet (Step 1a, runs in `quick`/`full`/`release`):
```bash
bash scripts/gauntlet.sh --plugin . --mode quick
```

---

## What each script checks

### Plugin header (main `.php` file)
Required fields:
```php
/**
 * Plugin Name:       My Plugin                  ← required
 * Plugin URI:        https://example.com         ← required for WP.org
 * Description:       What it does.               ← required
 * Version:           2.4.0                       ← MUST match git tag + readme.txt Stable tag
 * Requires at least: 6.0                         ← required for WP.org
 * Requires PHP:      7.4                         ← required for WP.org
 * Author:            Your Name                ← required
 * Author URI:        https://yoursite.com  ← required
 * License:           GPL-2.0-or-later            ← MUST be GPL-compatible
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       my-plugin                   ← MUST match folder name
 * Domain Path:       /languages
 *
 * (WC plugins only:)
 * Requires Plugins:  woocommerce
 * WC requires at least: 8.0
 * WC tested up to:   8.5
 */
```

Flags missing fields, mismatched text domain, License URI not pointing to a GPL-compatible URL.

### readme.txt (the WP.org-facing one)
```
=== My Plugin ===
Contributors: yourname
Tags: elementor, addons, widgets       ← max 12, no trademarks
Requires at least: 6.0
Tested up to: 6.5                       ← bump on every WP minor release
Stable tag: 2.4.0                       ← MUST match Version: header AND git tag
Requires PHP: 7.4
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

== Description ==
...

== Changelog ==
= 2.4.0 =
- ...
```

Catches: missing fields, stable-tag mismatch, trademark in tags (e.g. "elementor pro"), changelog missing entry for this version.

### Version parity
Three numbers must match:
```bash
# Plugin header Version:
Version: 2.4.0

# readme.txt Stable tag:
Stable tag: 2.4.0

# Git tag
git tag v2.4.0
```

Script enforces all three. WP.org won't index an SVN tag whose Stable tag in trunk doesn't point at it.

### License compliance
Must be GPL-2.0-or-later (or another GPL-compatible: MIT, Apache 2.0 ***IF*** explicitly compatible-with-GPL by author).
- Flags non-GPL licenses (proprietary, BSL, AGPL — incompatible)
- Flags missing LICENSE file
- Flags License URI not pointing to a real license text
- Verifies vendor/composer dependencies are also GPL-compatible

### POT file freshness
```bash
wp i18n make-pot . tmp.pot --slug=my-plugin
diff tmp.pot languages/my-plugin.pot
# → Any non-trivial diff = strings changed, regen POT before release
```

Flags: stale POT, strings in code that are NOT in the POT file.

### RTL readiness
- Has `rtl.css` if any non-trivial admin styles exist?
- Or uses logical properties (`margin-inline-start`) instead of `margin-left`?
- Loads RTL stylesheet via `wp_enqueue_style` with `rtl => 'replace'` or `'supplement'`?

---

## Common failures + fixes

### `Stable tag mismatch — readme.txt says 2.3.0, you're tagging v2.4.0`
```diff
- Stable tag: 2.3.0
+ Stable tag: 2.4.0
```

### `Tested up to: 6.3 — current WP is 6.5`
Bump on every WP minor release. WP.org de-prioritises plugins where this is > 2 versions stale.

### `Text Domain mismatch — folder name "my-plugin", header says "myplugin"`
Either rename the folder or update the header. **Folder name wins** — change the header to match.

### `Trademark in tags — "elementor pro"`
WP.org rejects on third-party trademark abuse. Use `elementor`, `addons` instead of `elementor pro`.

### `License URI 404`
Use the canonical GPL URI:
```
License URI: https://www.gnu.org/licenses/gpl-2.0.html
```

### `POT file stale — 14 new strings`
```bash
wp i18n make-pot . languages/my-plugin.pot --slug=my-plugin
git add languages/ && git commit -m "chore: regen POT for v2.4.0"
```

### `Vendor library is non-GPL`
Replace it. Common offenders: ChartJS (MIT — OK), Stripe SDK (MIT — OK), proprietary fonts (NOT OK in GPL plugin).

### `Missing == External Services == section`
Any plugin that makes external HTTP calls (wp_remote_get/post, curl, any API) must document every service in readme.txt:
```
== External Services ==

This plugin connects to Example API (https://example.com) to [purpose].
Data sent: [what data, when].
Terms of Service: https://example.com/tos
Privacy Policy: https://example.com/privacy
```
One block per external service. Missing this section is a WP.org rejection reason.

### `Dead links in readme.txt (404)`
All URLs in readme.txt must return HTTP 200. Check with:
```bash
# Quick link audit
grep -oP 'https?://[^\s\)>]+' readme.txt | while read url; do
    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")
    [ "$status" != "200" ] && echo "FAIL $status $url"
done
```
Failing links: Plugin URI, Author URI, License URI, Terms of Service, Privacy Policy in External Services section.

---

## When to run

- **Pre-release gate** — runs in `/orbit-release-gate` (mandatory)
- **After bumping version** — verify parity instantly
- **After regen POT** — verify it landed
- **Before WP.org SVN commit** — final check

---

## CI

```yaml
- run: bash ~/Claude/orbit/scripts/check-plugin-header.sh .
- run: bash ~/Claude/orbit/scripts/check-readme-txt.sh .
- run: bash ~/Claude/orbit/scripts/check-version-parity.sh . ${{ github.ref_name }}
- run: bash ~/Claude/orbit/scripts/check-license.sh .
```

Each script exits 0 on pass, 1 on fail. Wire into your release workflow.

---

## Pair with `/orbit-zip-hygiene`

This skill validates the *content* of files. `/orbit-zip-hygiene` validates the *contents of the release zip* (no `.git/`, no source maps, no dev deps). Both run in `/orbit-release-gate`.
