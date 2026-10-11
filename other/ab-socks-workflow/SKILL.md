---
name: ab-socks-workflow
description: >
  Comprehensive engineering workflow for the AB-Socks project: the release &
  versioning SOP, the layered architecture guide (controller / service /
  core / view), and the shared-hosting debugging playbook. Load this skill
  whenever the user asks to ship a release, bump the version, add a new
  controller/service/migration, refactor a bloated file, or debug a
  production issue on the shared host (500 errors, PDO errors, cache,
  uploads, WebP, sessions). This skill is procedural — it complements
  AGENTS.md and CONTRIBUTING.md, it does not replace their rules.
---

# AB-Socks Workflow Skill

This skill is the "how" that sits on top of `AGENTS.md` (the "what must
never break") and `CONTRIBUTING.md` (commit/versioning conventions). Read
`AGENTS.md` first if you haven't in this session — this skill assumes its
critical rules (money never written outside a service, snapshots, row
locking, CSRF, `config.php` untouched, English comments/Persian UI) are
already in effect.

---

## 1. Release & Versioning SOP

Follow this checklist, in order, for every change beyond a trivial typo fix.
Skipping a step is how the "tag-less releases" and "inconsistent commit
titles" problems this skill exists to prevent happened in the first place.

1. **Classify the change** (see `CONTRIBUTING.md` → Versioning):
   - `PATCH` — bug fix, no schema change, no new user-facing behavior.
     Also use `PATCH` for a pure internal refactor (behavior-preserving) —
     it changes shipped code, so it still needs a version bump.
   - `MINOR` — a new feature or a schema addition.
   - `MAJOR` — breaks an existing integration or removes something (rare
     for a single-deployment store).
   - Pure documentation/governance edits (`AGENTS.md`, `CONTRIBUTING.md`,
     `docs/*.md`, this skill file) do **not** need a version bump or a
     `Release:` line — they aren't shipped application behavior.
2. **Write the code.** Follow the layered architecture guide (§2) and the
   Boy Scout Rule in `AGENTS.md` — don't let a new bloated file ship
   alongside a release that's supposed to be paying down that same debt.
3. **Schema change? Add a migration.**
   - New file: `database/migrations/NNN_vX.Y.Z_short-description.sql`,
     `NNN` = next sequential number (check the highest existing one in
     `database/migrations/` first — never reuse or edit a past number).
   - Must be safe to re-run: `CREATE TABLE IF NOT EXISTS`, `INSERT IGNORE`,
     guarded `ALTER TABLE` (check `information_schema` before adding a
     column, or use `ADD COLUMN IF NOT EXISTS` where the MySQL/MariaDB
     version supports it). Never `DROP`/`TRUNCATE` existing data.
   - Mirror the exact same schema change into `database/schema.sql` (the
     fresh-install baseline) in the same commit — the two must never drift.
4. **Bump `APP_VERSION`** in `app/bootstrap.php` (semver, per step 1).
5. **Update changelog**: add a new dated entry at the top of
   `docs/CHANGELOG.md` in English. Match the existing heading style:
   `## X.Y.Z — YYYY-MM-DD` followed by a bold summary line and bullet groups.
   Keep only the most recent ~5 versions in `docs/CHANGELOG.md`; archive
   older releases in `docs/CHANGELOG-ARCHIVE.md`.
6. **Update architecture docs if system design changed**: if a new architectural
   invariant, service responsibility, or storage pattern was introduced,
   update the relevant domain file in `docs/architecture/<domain>.md` in place.
   Do not add historical bug diaries.
7. **Run the Quality Gate Verifier**:
   ```
   php tools/verify.php
   ```
   This runs syntax checks across all PHP files, validates that controllers
   remain within line-count limits (soft ceiling 80, hard ceiling 120),
   ensures views contain 0 SQL queries, verifies `.htaccess` DirectAdmin
   compliance, checks that `APP_VERSION` matches `docs/CHANGELOG.md`, verifies
   changelog compact size (<= 7 versions), verifies all modular architecture
   domain docs are present, and enforces the Anti-Duplication & Front-end Ratchet
   Baseline (zero new clone functions, inline script budget <= 20 lines in views,
   and :root CSS variable discipline). Zero errors are required before committing.
8. **Re-read money/stock logic once more** if you touched anything in
   `PricingService.php`, `GiftService.php`, `OrderService.php`,
   `AccountingService.php`, cart/checkout, or any `SELECT ... FOR UPDATE` /
   conditional stock `UPDATE` — specifically for the concurrent-request
   case (two customers, or an admin + a customer, acting at the same
   moment).
9. **Commit** using the Conventional Commits format from `CONTRIBUTING.md`:
   ```
   type(scope): concise description

   Release: vX.Y.Z

   - what changed and why, one bullet per notable change
   - Migration: NNN_vX.Y.Z_description.sql   (if applicable)
   ```
10. **Tag and push**:
    ```
    git tag -a vX.Y.Z -m "Release vX.Y.Z"
    git push origin main --follow-tags
    ```
    Do this in the same sitting as the commit — a version bump commit
    without a matching tag is an incomplete release.
11. **Create the GitHub Release via GitHub CLI (`gh`)**:
    Run `gh release create` directly from terminal:
    ```
    gh release create vX.Y.Z --title "Release vX.Y.Z" --notes "### Release vX.Y.Z summary here..."
    ```
    Or point to a temporary release notes markdown file extracted from `docs/CHANGELOG.md`:
    ```
    gh release create vX.Y.Z --title "Release vX.Y.Z" --notes-file release_notes.md
    ```
    *Note: `gh` is installed on the machine at `C:\Program Files\GitHub CLI\gh.exe`. If not in PATH, invoke directly.*

### Quick reference: full command sequence

```powershell
# 1. Verify syntax and architecture
php tools/verify.php

# 2. Stage and commit
git add -A
git commit -m "feat(scope): concise description" -m "Release: vX.Y.Z" -m "- bullet 1" -m "- bullet 2"

# 3. Tag and push to GitHub
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin main --follow-tags

# 4. Create GitHub Release
gh release create vX.Y.Z --title "Release vX.Y.Z" --notes "Release notes from CHANGELOG..."
```

---

## 2. Layered Architecture Guide

AB-Socks is framework-free but not layer-free. Four layers, one direction of
dependency (top depends on bottom, never the reverse):

```
Front controller (index.php / admin/*.php / ajax/*.php / payment/*.php)
        │  routes by $_GET['route'] or filename, no logic
        ▼
Controller (app/controllers/site|admin/*.php)
        │  reads $_GET/$_POST/$_FILES/$_SESSION, calls services/helpers,
        │  hands variables to a view. Soft ceiling 80 lines, hard ceiling
        │  120 (see AGENTS.md Boy Scout Rule).
        ▼
Service / Core helper (app/services/*.php, app/core/*.php)
        │  all business logic, all SQL, all validation rules live here.
        │  Plain global functions grouped by filename — NOT PHP classes
        │  (e.g. PricingService.php defines global functions like
        │  recordPriceChange(), not a class with static methods).
        ▼
View (views/site|admin/*.php)
           pure presentation: loops, e()-escaped output, no queries,
           no business logic, no $_POST handling.
```

### Where new code goes

| You're adding...                                   | Goes in |
|------------------------------------------------------|---------|
| A new site page (e.g. `/faq`)                       | Route in `index.php`, controller in `app/controllers/site/`, view in `views/site/` |
| A new admin page                                    | Controller in `app/controllers/admin/`, view in `views/admin/`, link it from `views/admin/layout/` nav |
| A new AJAX endpoint                                 | `ajax/*.php` — still requires `app/bootstrap.php`, still needs `requireAdmin()`/CSRF/prepared statements |
| Logic touching money, stock, gifts, shipping, orders, accounting | The matching existing service (`PricingService`, `GiftService`, `ShippingService`, `OrderService`, `AccountingService`) — never inline in a controller |
| A generic, domain-agnostic helper (formatting, slugs, uploads, tags, theme tokens) | `app/core/` — see the existing split: `functions.php` (generic), `uploads.php` (image upload/rename), `tags.php` (product tags), `theme.php` (storefront theme tokens) |
| A brand-new domain concern (e.g. a future loyalty-points system) | A new `app/services/XxxService.php`, following the existing pattern: global functions, a file-level doc comment explaining the concurrency/snapshot model up front |

### Controller pattern (copy this shape for new CRUD pages)

```php
<?php
$id = (int) ($_GET['id'] ?? 0);
$record = $id ? getRecordById($id) : null; // from a service/helper
if ($id && !$record) redirect('list.php');

$pageTitle = $record ? 'ویرایش ...' : '... جدید';
$errors = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $result = saveRecordFromRequest($record, $id); // service function does the work
    $errors = $result['errors'];
    $record = $result['record']; // repopulated on error, for re-rendering the form
}

renderView('admin/record_edit', compact('pageTitle', 'record', 'errors'));
```

The service function (`saveRecordFromRequest` above) owns: `verifyCsrf()`,
field parsing, validation, the DB write (transaction if it touches
stock/price), and either `redirect()`s on success (matching existing
controllers' behavior) or returns the errors/repopulated data for the
controller to hand to the view. This is the exact shape used by
`ProductService::saveProductFromRequest()`/`app/services/ProductService.php`
— read it as the canonical example before writing a new one.

### Service function conventions

- Return `['ok' => bool, 'error' => string]` (or `errors` plural) for
  operations that can fail — never throw for an expected validation
  failure; reserve exceptions for truly unexpected states inside a
  transaction (see `GiftService::assignGiftToOrder()` for the pattern:
  `beginTransaction()` → validate with row locks → `commit()`/`rollBack()`
  in a `try/catch(Throwable)`).
- Every function gets a one-line (or short doc-block) comment explaining
  *why*, not *what* — the code already says what.
- Snapshot financial/inventory fields into the target row at write time
  (see `AGENTS.md` critical rule 2) — never store just a foreign key you
  intend to resolve later.

---

## 3. Shared-Hosting Debugging Playbook

Production is Nginx (proxy) → Apache + PHP-FPM (backend) under DirectAdmin,
1.5 GB disk / 200 MB DB / 80 GB bandwidth per month, no shell access implied
for the site owner. Keep this playbook in mind before proposing any fix that
assumes a VPS-like environment.

### "It works locally but 500s in production"

1. **Suspect `.htaccess` first.** DirectAdmin's `AllowOverride` is
   restricted to `AuthConfig FileInfo Indexes Limit
   Options=Indexes,...`. Anything using `Options -ExecCGI`, `php_flag`,
   `ForceType`, or an `<IfModule>` nested inside `<FilesMatch>` will 500
   the *entire directory*, not just the offending request. Check
   `uploads/.htaccess` and the root `.htaccess` for anything beyond script
   execution blocking (`<FilesMatch "\.(php|php[3-8]?|phtml|pl|py|cgi|asp|sh)$">`)
   and `Options -Indexes`.
2. **Check PHP version compatibility.** Production is PHP 8.x only —
   verify no PHP 7-only or PHP 8.something-too-new syntax slipped in
   (`readonly` properties, enums, etc. need version confirmation against
   the actual host's PHP version before use).
3. **Check `app/vendor/` is intact.** No Composer runs in production —
   PHPMailer and any other vendored library must be present as committed
   files, not installed via a build step that never runs there.

### PDO / database errors

- Every query is a prepared statement via `db()` (`app/core/db.php`).
  A raw PDOException reaching the browser means a `try/catch` boundary is
  missing — wrap it, log the detail server-side, and show a generic
  Persian error to the user (see `AGENTS.md` → Boy Scout Rule → defensive
  programming).
- "Table doesn't exist" after a claimed-successful deploy almost always
  means a migration `.sql` file was never actually run through
  phpMyAdmin's SQL tab — there's no automatic migration runner. Confirm
  with the site owner which numbered files have actually been applied.
- A stock/price race condition bug always traces back to a missing
  `SELECT ... FOR UPDATE` or a plain `UPDATE` instead of the conditional
  `UPDATE ... SET stock = stock - ? WHERE stock >= ?` pattern. Grep for the
  table name across `app/services/` before assuming new code is the cause.

### Uploads & images

- `.webp` requests are routed through `/img.php?f=/uploads/...` because
  shared-hosting MIME tables often lack `image/webp`, and
  `X-Content-Type-Options: nosniff` makes browsers refuse a mislabeled
  file. If a newly uploaded `.webp` doesn't render, check the root
  `.htaccess` rewrite rule is intact and that `img.php` is being hit (not
  a direct `/uploads/xxx.webp` URL bypassing the proxy).
- All new image-upload code should call `handleImageUpload()` in
  `app/core/uploads.php` (or one of its thin wrappers,
  `handleProductImageUpload()` / `handleBrandingImageUpload()`) instead of
  hand-rolling MIME/size validation again — this exact duplication (byte
  for byte, in two different controllers) has happened once already.
- Uploaded files must never be trusted by extension alone — validated via
  `finfo_file()` real MIME type, then `getimagesize()` (or an explicit
  `<svg>`/no-`<script>` check for SVG) before being written to disk.

### Cache / sessions

- Sessions are cookie-based (`session.cookie_httponly`,
  `session.cookie_samesite=Lax`, `session.cookie_secure` when HTTPS) — set
  in `app/bootstrap.php` before `session_start()`. Don't add a second
  `session_start()` anywhere else; it's already global via bootstrap.
- Browser caching for static assets and `img.php` responses is
  intentionally aggressive (1-year headers + ETag/304 for `img.php`). If a
  content change (e.g. a replaced logo) doesn't show up for the store
  owner, it's almost always a caching issue, not a code bug — confirm with
  a hard refresh / incognito window before debugging further.

### When you genuinely cannot verify a fix

There is no staging environment. Say so plainly rather than asserting a
production-only issue is fixed. `php -l` only catches syntax errors — it
proves nothing about `.htaccess` behavior, live MIME handling, or
concurrency. Where possible, reason through the two-request-at-once case on
paper before shipping a concurrency-sensitive fix.
