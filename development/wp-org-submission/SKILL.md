---
name: wp-org-submission
description: "Use when submitting a WordPress plugin to the WP.org directory for the first time, deploying a new version via SVN (plugins.svn.wordpress.org trunk, tags, assets), fixing a reviewer rejection (17-issue catalog with exact reviewer quotes), writing or correcting readme.txt (Stable tag, Changelog, Upgrade Notice, Requires, Tested up to, External services), or preparing WP.org assets (banner-772x250.png, banner-1544x500.png, icon-128x128.png, icon-256x256.png, icon.svg, screenshot-N.png). Triggers: \"submit my plugin to WP.org\", \"SVN deploy\", \"reviewer rejected my plugin\", \"fix WP.org review feedback\", \"how do I set up the SVN repo\", \"WP.org assets\", \"prepare my plugin for the directory\", \"what does the reviewer want\", \"Stable tag\", \"readme.txt requirements\", \"WP.org banner dimensions\", \"fix this reviewer comment\", \"plugin zip for submission\", \"svn commit trunk\", \"svn cp trunk tags\", \"reviewer says missing nonce\", \"reviewer says not prefixed\", \"reviewer says missing sanitization\", \"Upgrade Notice section\", \"External services section in readme\", \"submit.wordpress.org form\", \"icon.svg for WP.org\". For WP.org guideline compliance review only, use `wp-plugin-directory-guidelines` instead."
---

# WordPress.org Plugin Submission & SVN Deploy

> **Model note:** SVN deploy steps and asset setup are mechanical (`haiku`). Pre-submission rejection-pattern scan across a real codebase (17 patterns) requires code judgment — use `sonnet`. Responding to a human reviewer rejection also needs `sonnet`.

Get a plugin into the WP.org directory and keep releasing to it. Two distinct phases — know which one applies:

- **Phase 1 — Initial submission.** Plugin not yet in the directory. One-time human review, then SVN access is granted.
- **Phase 2 — SVN deploy.** Plugin already approved. Ship a new version into the existing SVN repo.

`wp-org-submission` is about the *directory/SVN side*. Sync the version sources first with [[wp-plugin-release]] — this skill assumes the codebase already carries the target version.

## When to use

- "Submit this plugin to WordPress.org", "publish to the .org directory", "add my plugin to wp.org".
- "Deploy the new version to SVN", "push the release to wp.org", "tag a release on plugins.svn".
- "Set up screenshots / banner / icon", "why aren't my assets showing".
- "Fix a WP.org rejection", "respond to plugin review email", "they flagged trialware / source code / external service".
- Pre-submission hygiene sweep using the 17-issue rejection catalog (real reviewer quotes).

**Not for:** "will this pass WP.org review?", "check guideline violations", "is my plugin GPL-compliant?" — use the official `wp-plugin-directory-guidelines` skill for authoritative 18-guideline compliance review. This skill owns the *workflow* (SVN, assets, rejections); that skill owns the *rules*.

## Phase 1 — Initial submission

The review is done by humans and can take days to weeks. Submitting a clean plugin avoids round-trips.

1. **Slug availability** — the directory slug is derived from the plugin name in the main file header. Pick a name not already taken at `https://wordpress.org/plugins/<slug>/` (404 = free). Slug is permanent.
2. **readme.txt valid** — must parse in the official validator: `https://wordpress.org/plugins/developers/readme-validator/`. Required header fields, valid `Stable tag`, GPL-compatible `License`. See `references/submission-checklist.md`.
3. **Guidelines compliance** — sanitize input, escape output, nonce-protect actions, prefix all globals, no obfuscation/minified-only code, no external loading of scripts, no tracking or calling home without explicit opt-in consent, GPL-compatible code + assets only. Full checklist in `references/submission-checklist.md`. 17-issue catalog with exact reviewer quotes in `references/review-issues-catalog.md`.
4. **Build a clean zip** — source files (`src/`, `composer.json`, build configs) must be included; `.wordpress-org/` and `node_modules` must not. Full include/exclude lists in §4 of `references/submission-checklist.md`.
5. **Submit** at `https://wordpress.org/plugins/developers/add/`. The reviewer replies by email. Fix what they flag, reply briefly (context only, no change list), attach the updated zip. On approval, SVN access is granted at `https://plugins.svn.wordpress.org/<slug>/`.

## Phase 2 — SVN deploy

WP.org distributes via **Subversion**, not git. The SVN repo has three top-level dirs:

```
<slug>/
├── trunk/        # current development copy of the plugin
├── tags/         # one immutable dir per released version (tags/1.2.0/)
└── assets/       # directory listing images — NOT shipped in the plugin zip
```

**The `Stable tag` in `trunk/readme.txt` decides what users download** — it must name a directory under `tags/`. Set `Stable tag: 1.2.0` and ensure `tags/1.2.0/` exists. (Pointing Stable tag at `trunk` is legal but discouraged — always release from a tag.)

Deploy = copy the production build into `trunk/`, then `svn cp trunk tags/<version>`, then commit. Use the helper:

```bash
scripts/svn-deploy.sh <slug> <path-to-built-plugin-dir> <version>
```

It checks out SVN, syncs `trunk/` to the build (adding/removing files), copies `trunk` → `tags/<version>`, and prints the `svn commit` to run after review. Full manual walkthrough and the add/delete handling in `references/svn-deploy.md`.

**Assets** (banner, icon, screenshots) live only in `assets/`, never in the zip. Exact filenames and dimensions are mandatory — `banner-772x250.png`, `banner-1544x500.png` (retina), `icon-128x128.png`, `icon-256x256.png`, `icon.svg`, `screenshot-1.png` (matched to the `1.` line under `== Screenshots ==` in readme.txt). See `references/svn-deploy.md`.

## Top rejection patterns

Most frequent — not exhaustive. Full 17-issue catalog with exact reviewer quotes in `references/review-issues-catalog.md`.

- Generic or trademarked slug; "WordPress"/"Woo" in the plugin name.
- Main PHP file name doesn't match the slug (`plugin.php` instead of `<slug>.php`).
- Invalid URLs in plugin header or readme.txt — verify with `curl -I` before submission.
- External service called but not documented in `== External services ==`.
- Unsanitized `$_GET`/`$_POST`, unescaped output, missing nonces + capability checks.
- Loading JS/CSS from a CDN instead of bundling; inline `<style>` / `<script>` tags.
- No source for compiled output — `src/` not in zip and no public repo linked.
- `.wordpress-org/` or `node_modules/` in the zip.
- Generic function/class prefix or mixed prefixes across one plugin.
- **Trialware (Guideline 5)** — features gated behind license key or Pro plan check. See `references/trialware-compliance.md`.
- Admin notices on every screen, persistent nags, full-page upsell flows (Guideline 11).
- Stable tag names a tag that doesn't exist under `tags/` → users get nothing.

## References

- `references/submission-checklist.md` — comprehensive pre-submission checklist (identity, readme.txt, guidelines, zip hygiene, security pattern, automated checks).
- `references/review-issues-catalog.md` — 17-issue catalog with exact reviewer quotes and corrective actions, sourced from 8 real submissions.
- `references/trialware-compliance.md` — Guideline 5 freemium pattern, audit checklist, and step-by-step licensing-layer removal.
- `references/svn-deploy.md` — complete SVN workflow, asset spec, Stable-tag mechanics, hotfix flow.
- `scripts/svn-deploy.sh` — git/build → SVN trunk+tag deploy helper.
- **Official:** `wp-plugin-directory-guidelines` (WordPress/agent-skills) — authoritative source for the 18 WP.org Plugin Directory guidelines; use it for GPL/naming/trialware rule interpretation when our 17-issue catalog conflicts or is ambiguous.
