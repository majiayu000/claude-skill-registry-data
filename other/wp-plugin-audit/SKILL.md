---
name: wp-plugin-audit
description: "Use when auditing a WordPress plugin for security issues, code inconsistencies, or quality gaps — fans out parallel checks across four dimensions: A (version/metadata sync), B (naming/prefix/i18n), C (docs vs code), D (code conventions/security), verifies every finding with file:line references before reporting, and routes confirmed issues to the correct fix skill. Security patterns checked: XSS (missing esc_html/esc_attr), SQL injection (raw $wpdb), CSRF (missing nonce), missing capability checks, file upload validation, object unserialize, open redirect, path traversal, REST auth hardening. Triggers: \"audit this plugin\", \"find inconsistencies in my plugin\", \"security review\", \"check my plugin for XSS\", \"is my escaping correct\", \"find missing nonces\", \"check capabilities in my plugin\", \"audit readme.txt\", \"find security issues\", \"plugin quality sweep\", \"are there SQL injection risks\", \"review my plugin before submission\", \"missing esc_html()\", \"raw wpdb query without prepare()\", \"missing current_user_can()\", \"unprotected AJAX handler\", \"plugin prefix inconsistency\", \"version out of sync\", \"i18n audit\", \"missing translator comment\", \"file upload not validated\", \"open redirect risk\". Not for: PHPStan type analysis — use `wp-phpstan`; WP.org pre-submission checklist — use `wp-org-submission`."
---

# WordPress Plugin Consistency Audit

Read-only audit that surfaces inconsistencies across a WP plugin's code, config, and docs. Optimised for **recall with low false-positive rate**: every candidate is verified against the actual code before it reaches the report.

## When to use

- "Audit the plugin", "find inconsistencies", "consistency/quality sweep".
- Before a release, or after a large refactor, to catch drift.

**Not for:** PHPStan type checking or baseline generation — use `wp-phpstan` (official). WP.org pre-submission review (17 rejection patterns) — use `wp-org-submission` which has that checklist.

## Method

### 1. Fan out — 4 independent dimensions (parallel agents)

Dispatch one read-only agent per dimension (`Explore` type, `model: haiku`), in a single message so they run concurrently. Each returns findings with `file:line`, the inconsistent value, and the expected/canonical form.

> **Model note:** Dimension agents are pure grep/read with no synthesis — `haiku` is faster and cheaper. The main thread (whatever model the user has active) does all verification and reporting.

- **A — Version & metadata.** Cross-reference every version/metadata source: plugin header (`Version`, `Requires at least`, `Requires PHP`, `Tested up to`, `Text Domain`), the version constant, `readme.txt` (`Stable tag` + Changelog + Upgrade Notice), `composer.json`, the `.pot` `Project-Id-Version`, and the schema/DB version. Flag every mismatch; note fields that are *intentionally* independent (schema `$db_version` ≠ plugin version) so they aren't flagged.

  Also audit the **main plugin file header format** against the canonical PHPDoc DocBlock style (preferred over plain block comment):
  ```php
  /**
   * Plugin Name
   *
   * @package           PluginPackage
   * @author            Your Name
   * @copyright         2024 Your Name or Company Name
   * @license           GPL-2.0-or-later
   *
   * @wordpress-plugin
   * Plugin Name:       Plugin Name
   * Plugin URI:        https://example.com/plugin-name
   * Description:       Description of the plugin.
   * Version:           1.0.0
   * Requires at least: 6.5
   * Requires PHP:      7.4
   * Author:            Your Name
   * Author URI:        https://example.com
   * Text Domain:       plugin-slug
   * License:           GPL v2 or later
   * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
   * Update URI:        https://example.com/my-plugin/
   * Requires Plugins:  my-plugin, yet-another-plugin
   */
  ```
  Flag: missing `@wordpress-plugin` marker (distinguishes WP header from plain PHPDoc); missing `@package`/`@author`/`@copyright`/`@license` PHPDoc fields; `Description` over 140 characters; `License` slug not matching `License URI`; missing `Text Domain` when plugin has translated strings (requires Dimension B `__()` detection to confirm strings exist); using a plain `/* */` block instead of `/** */` PHPDoc block.

  **Version currency** — WordPress and PHP baselines drift; re-verify against the live release each audit rather than trusting these numbers. As of **July 2026**: current WordPress stable is **7.0** (7.1 due Aug 2026; 6.9.x is the prior maintenance line); PHP floor is **7.4** (WP 7.0 dropped 7.2/7.3), officially recommended **8.3+**; the WP.org directory has **18 numbered guidelines** (page last updated 2026-03-11). Flag:
  - a `Tested up to` that does NOT equal a real, *released* WordPress version. A value **ahead of** the latest release (e.g. `7.9` when 7.0 is current) is as wrong as a stale one — WP.org warns on both. **Verify against the current WP release before flagging**; do not assume a high number is a typo (7.0 is a real release, not a mistyped 6.x). Confirm the live version if unsure.
  - a `Requires PHP` below **7.4** (below WordPress's own minimum), or a `Requires PHP` / `Requires at least` value that disagrees across header ↔ `readme.txt` ↔ `composer.json`.
  - `Requires Plugins` (dependency header) that names a slug not present on WP.org, or that is out of sync with an actual runtime dependency check.
- **B — Naming / prefix / i18n.** Canonical prefix (e.g. `myplugin_` / `_myplugin_`) — flag legacy prefixes outside the migration file. Text-domain consistency on every `__()`/`_e()`/`esc_html__()`/`_n()`; missing translator comments on `sprintf`/`printf` with placeholders. `@package` tag variants. Option/transient/hook/REST/cookie/nonce/AJAX/asset-handle/CSS-class prefix uniformity.
- **C — Docs ↔ code.** Path references (renamed dirs), function/class/option/table names referenced in docs that no longer match code, documented commands that don't exist (`composer test:unit` etc.), test counts, architecture trees vs real files, behavior claims that contradict code. Distinguish *historical* docs (point-in-time, leave) from *current* docs (must match).
- **D — Code conventions & security.** DB-write style (ORM vs `$wpdb` per the repo's CLAUDE.md), docblock style, `@since` tags, return-type consistency, leftover renamed-dir refs, duplicated logic, escaping/sanitization uniformity. Tag each: bug-risk / convention / cosmetic.

  Also check advanced security patterns (see `references/security.md`). By 2025 disclosure volume the top plugin classes are **XSS (~35%) > CSRF (~19%) > LFI (~13%) > broken access control (~11%) > SQLi (~7%)**, and ~43% are exploitable **unauthenticated** — prioritize accordingly:
  - **File uploads** — `move_uploaded_file()` used directly; MIME type read from `$_FILES['type']` (user-supplied); files stored outside `wp-content/uploads/`.
  - **Object injection** — `unserialize()` on any value that originated from user input or a user-writable option (incl. `phar://` deserialization via a file op on user-controlled input).
  - **SQL injection beyond `prepare()`** — dynamic `ORDER BY`, column name, or table name constructed from user input without whitelisting.
  - **Secrets exposure** — API keys hardcoded in source files or stored raw in `wp_options` when user-editable.
  - **Open redirect** — `wp_redirect()` on `$_GET['redirect_to']` without `wp_validate_redirect()`.
  - **SSRF** — `wp_remote_*`/cURL/`file_get_contents` on a user-supplied URL without `wp_safe_remote_*` + host allowlist + `redirection => 0` (can reach cloud metadata `169.254.169.254` / internal services).
  - **Broken access control (IDOR / privilege escalation)** — a state-changing handler with a nonce but **no** `current_user_can()`; a `wp_ajax_nopriv_` action doing privileged work; an object/user id acted on without an ownership check. WAF-invisible (looks like normal authenticated traffic) — grep every handler for the *capability* check, not just the nonce.
  - **Path traversal / LFI** — `include`/`require` or filesystem paths built from user input without `realpath()` + base-prefix check.
  - **REST auth gaps** — endpoints that write data with `permission_callback: '__return_true'` and no HMAC/nonce verification.
  - **Dependency CVEs** — note if `composer audit` has not been run or if `composer.lock` is missing from the repo.
  - **Trialware / locked features (Guideline 5)** — a feature whose worker exists in the **free** code but has **no free-side trigger** (e.g. an Action Scheduler handler only scheduled by the pro add-on, or a bulk method with no free REST route) is a locked feature *even though it is unreachable in free*. Grep each hooked handler / bulk method for a free caller and flag those with none. The **rule** is owned by the official `wp-plugin-directory-guidelines` skill — this audit only surfaces the code pattern to route there.

Scale dimensions to the plugin; add domain-specific ones (e.g. WooCommerce hook security, multisite option isolation) when relevant.

### 2. Verify EVERY candidate before reporting

Do not trust agent output verbatim — agents over-report. For each finding, `grep`/`Read` the exact line and confirm it is real. Kill false positives. Real example caught this way: an `action_links` `sprintf('<a href="%s">%s</a>', …)` flagged for a "missing translator comment" is **not** translatable (pure HTML markup) → drop it.

Verify *claims* the same way you verify *findings*: a changelog or readme entry that says a fix landed is **not** evidence it shipped — `grep`/`Read` the code and confirm. Real example: a `6.3.0` changelog claimed a trialware worker and a phone-home call were removed, but both were still present in the `6.3.1` source.

### 3. Report (findings only — do NOT fix unless asked)

- Group by severity: 🔴 functional → 🟠 (security/i18n) → 🟡 stale/naming → ⚪ cosmetic.
- Each finding: `file:line`, what's wrong, what's correct.
- Include a **"Checked, NOT bugs"** section listing intentional patterns (so they don't get "fixed" by mistake): e.g. webhook with no capability check (HMAC-protected), ORM `update()` that routes to `$wpdb` internally, intentional legacy prefixes in the migration file.
- End with a suggested fix priority. Then ask whether to fix all or a subset.

### 4. Route findings to fix skills

After the user confirms what to fix, consult `references/skill-routing.md` and invoke the correct skill per finding category. Do not attempt to fix all categories inline — route each to its owner:

- Version drift → `wp-plugin-release`
- Escaping / PHPCS violations → `wp-coding-standards`
- Nonce / capability gaps → `wp-plugin-development` (official)
- Advanced security gaps (file upload, unserialize, secrets, REST auth, redirect, path traversal) → `references/security.md` patterns
- i18n violations → `wp-i18n-workflow`
- PHPStan / type errors → `wp-phpstan` (official); stubs scaffolding → `wp-phpstan-stubs`
- WP.org compliance → `wp-org-submission` + `wp-plugin-directory-guidelines` (official)
- DB convention → `wp-database`
- Missing tests → `wp-plugin-testing`
- Multisite gaps → `wp-multisite`
- Background job issues → `wp-background-processing`
- Docs ↔ code mismatch → `wp-github-flow` (scoped PR)
- Performance issues → `wp-performance` (official)
- Build / asset drift → `wp-build-tools`

Full routing table with severity rules: `references/skill-routing.md`.

## Notes

- Audit is read-only. Run on the current working tree (mention if it includes unmerged changes).
- When fixing afterward: many files span multiple finding-categories — a single cohesive "fix audit findings" commit with an enumerated body is cleaner than fragile per-scope partial staging.
- For authoritative WP.org Plugin Directory guideline compliance (18 official rules: GPL, naming, trialware, external services), use the official `wp-plugin-directory-guidelines` skill (WordPress/agent-skills). This audit covers *code consistency and conventions*; that skill covers *directory submission rules*.

## References

- `references/checklist.md` — per-dimension grep commands, common false positives to kill, and the severity-grouped report template.
- `references/readme-txt.md` — readme.txt required/optional sections, field limits, Stable tag rules, common mistakes, and verification greps.
- `references/escaping-sanitization.md` — escaping functions by context, sanitization functions by input type, late-escape rule, common XSS/SQLi flags.
- `references/capability-nonce.md` — nonce creation/verification patterns, capability map, public webhook exception, false-positive patterns.
- `references/i18n-translator-comments.md` — all i18n function signatures, translator comment format and placement rules, variable/placeholder rules, common flags.
- `references/security.md` — advanced security patterns: file upload validation, object injection, SQL injection beyond `prepare()`, secrets storage, REST auth hardening, open redirect, path traversal, dependency CVE scanning.
- `references/skill-routing.md` — finding category → skill routing table with severity rules; use in Step 4 to dispatch the correct fix skill.
