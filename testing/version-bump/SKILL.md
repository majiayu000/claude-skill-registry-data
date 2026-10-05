---
name: version-bump
description: Bump the seQura WooCommerce plugin version across the two coupled locations (sequra/sequra.php header and sequra/readme.txt stable tag + changelog), keeping them in sync and writing the changelog entry. Use when releasing a new plugin version.
---

# Version bump (seQura Payment Gateway for WooCommerce)

The plugin version lives in **two files that must stay in sync**. Bumping one
without the other ships a broken release: WordPress reads the `Version:` header
to detect updates, and the `Stable tag:` in `readme.txt` is what wordpress.org
serves. Always change both, plus add a changelog entry.

## The two coupled locations

1. **`sequra/sequra.php`** — the plugin header:
   ```php
    * Version:           4.3.2
   ```
2. **`sequra/readme.txt`** — the WordPress.org readme:
   - The stable tag near the top:
     ```
     Stable tag: 4.3.2
     ```
   - A new entry under `== Changelog ==` (entries are newest-first):
     ```
     = 4.3.3	=
     * Fixed: <what changed>.
     * Changed: <what changed>.
     ```
     Note: the existing entries use a literal TAB between the version and the
     trailing `=` (`= 4.3.2\t=`). Match that exact format.

There is **no** PHP version constant — these two files are the only sources of
truth. Do not invent a `SEQURA_VERSION` define.

## Procedure

Given a target version `X.Y.Z`:

1. **Confirm the current version and the target.** Read the current value from
   `sequra/sequra.php` (`Version:`) and `sequra/readme.txt` (`Stable tag:`) and
   make sure they already agree. If they don't, surface the mismatch before
   touching anything — that's an existing bug, not something to silently paper
   over.

2. **Decide the bump** (semver): patch for fixes, minor for backwards-compatible
   features, major for breaking changes. If the user didn't specify, ask.

3. **Edit `sequra/sequra.php`** — update the `Version:` header to `X.Y.Z`.

4. **Edit `sequra/readme.txt`**:
   - Update `Stable tag:` to `X.Y.Z`.
   - Insert a new `= X.Y.Z\t=` block at the **top** of the `== Changelog ==`
     section (above the previous newest entry). Summarise the changes since the
     last release as `* Fixed:` / `* Changed:` / `* Added:` bullets. If an
     `integration-core` upgrade is part of the release, include a
     `* Changed: Update integration-core library to version vA.B.C.` line, as
     prior entries do.
   - If WordPress / WooCommerce "Tested up to" versions changed this release,
     also update `Tested up to:` near the top and mention it in the changelog.

5. **Verify the two files agree.** Re-read both; the version string must be
   byte-identical in `sequra.php` (`Version:`) and `readme.txt` (`Stable tag:`),
   and the new changelog block's version must match too.

6. **Sanity-check the build** doesn't break: `bin/make_zip` reads the version
   from the `sequra.php` `Version:` header (`grep "Version:" sequra.php`) to
   name the artifact, so the header format must stay `Version:           X.Y.Z`.

## Tagging / release

Committing and tagging is a separate, deliberate step — do it only when the user
asks to release:

- Commit the version bump (use the `sq-git:commit` skill).
- The git tag convention for this repo is the bare version `X.Y.Z` (check
  `git tag` for the existing pattern before tagging).
- Publishing to wordpress.org is handled separately by
  `bin/publish_to_wordpress.sh` — do not run it as part of a routine bump unless
  explicitly asked.

## Checklist

- [ ] `sequra/sequra.php` `Version:` = `X.Y.Z`
- [ ] `sequra/readme.txt` `Stable tag:` = `X.Y.Z`
- [ ] New `= X.Y.Z	=` changelog block added at the top of `== Changelog ==`
- [ ] `Tested up to:` updated if WP/WC support changed
- [ ] Both version strings verified identical
