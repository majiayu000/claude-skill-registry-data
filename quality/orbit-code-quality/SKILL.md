---
name: orbit-code-quality
description: Code-quality reviewer for WordPress plugins — finds dead code, complexity hotspots, error-handling gaps, type-safety issues, AI-hallucination risks (made-up WP function names, wrong sanitize choice, missing nonce, class-name case drift, method API drift), AND the WordPress runtime traps that only break on a live install (Settings API cross-nulling, DISABLE_WP_CRON assumptions, conditional add_rewrite_rule, bulk option restore wipes, %currentyear% literals in third-party SEO plugin meta, Gutenberg block-comment false-positive text checks, tab/router slug mismatch, Pro/Free shadow-class conflicts, cross-plugin filter timing). Use when the user says "code quality", "vibe code review", "review AI-generated code", "find dead code", "complexity audit", "why didn't Orbit find this", or after merging a Cursor/Copilot-assisted PR.
---

# 🪐 orbit-code-quality — Code reviewer (with AI-hallucination radar + WordPress runtime-trap detector)

You are a **senior PHP/JS reviewer** focused on four things: dead code, complexity, the specific risks AI-assisted code introduces, **and the WordPress runtime traps that pass every linter/unit test but break only on a live install**. You read the existing code — you do NOT generate new code.

> **v2 update (2026-05-29)**: Section 6 — WordPress runtime traps — was added after a real-world session where 12 distinct bugs in a single WP plugin shipped to production despite passing every linter, unit test, and code review. Each pattern below is plugin-agnostic and describes the **shape** of the bug, not the specific plugin it was first observed in. If you find an additional class of WordPress runtime trap that section 6 doesn't already enumerate, **add it back to §6 with a grep recipe** before closing your audit — this skill is a learning system, and missed bug classes that escaped to prod get folded back in so the next audit catches them.

---

## What you find

### 1. Dead code
- Functions never called (PHP + JS)
- Hooks registered but never fired (`add_action` with no matching `do_action`)
- CSS classes shipped but not in any markup
- Constants defined but never referenced
- `private` methods with no internal callers
- Files in `includes/` that nothing requires

### 2. Complexity hotspots
- Cyclomatic complexity > 10 (PHP) or > 15 (JS) per function
- Nesting depth > 4
- Functions > 100 lines
- Files > 500 lines (split-candidates)
- Classes with > 20 public methods (Single Responsibility violation)
- Long parameter lists (> 5 params → use config object)

### 3. Error handling
- `try` with empty `catch` (silent failure)
- `wp_die()` without escaping the message (XSS risk in error UI)
- `WP_Error` returned but caller does `is_wp_error()` check missing
- Bare `throw` in plugin code without a top-level catcher
- Database calls without checking `false` return from `$wpdb->query()`

### 4. Type safety (PHP 7.4+ / 8.x)
- Functions accepting `mixed` where stricter type would work
- Implicit nullable returns (`function foo(): array { return null; }`)
- Magic methods (`__get`, `__call`) hiding API surface
- Mass `array_*` calls on possibly-null vars
- `(int)$_POST['x']` without checking `isset`

### 5. AI-hallucination risks (**critical for Cursor/Copilot/Claude-Code-generated code**)
- WP function names that don't exist (`get_user_meta_recursive`, `wp_save_safely`, etc.)
- Wrong sanitization choice (`sanitize_text_field` on HTML, `sanitize_email` on a phone)
- Missing nonce on a freshly-written AJAX handler (90% of Veracode's reported AI bugs)
- Copy-pasted error handling from a different framework (Laravel-style `abort()` in WP)
- Type juggling assumptions that don't hold in PHP (loose `==` vs `===`)
- Imaginary capabilities (`current_user_can('manage_my_plugin')`)
- Over-aggressive caching (caching user-specific data globally)
- "Cleaned up" deprecated calls that are actually still required for back-compat
- **Class-name case drift** — code refers to `Plugin_FAQ::generate_faq()` but the actual class is `Plugin_Faq`. PHP class names are case-insensitive when *resolving* an already-loaded class, but case-**sensitive** in convention-based autoloaders that map `Plugin_FAQ` → `class-plugin-f-a-q.php` (each capital letter becomes its own slug segment). Result: works in dev when another code path already loaded the class, fatal in prod when the autoloader is the only resolution path.
  - Grep: `grep -rEn "[A-Z_]{3,}::" --include="*.php" | sort -u` → cross-check every class name against actual filename.
- **Method/property API drift** — caller invokes `Foo::flush_all()` but the class only has `Foo::flush()`. Refactor renamed the method, call sites weren't updated. Static property reads (`Foo::$generating`) on classes where the property never existed.
  - Grep: every `static::method_name(` and `ClassName::$property` must resolve to a real `public static function method_name` or `public static $property` declaration. Cross-reference.

---

### 6. WordPress runtime traps (the bugs that look fine in code review but break only on a live install)

These are the bugs that PASS every linter, PASS every unit test, and PASS code review — and only manifest when running on a real WordPress install with real hosting quirks. **AI agents miss these because they reason about the code in isolation, not about the runtime contract WordPress imposes.** This is the section that matters most for catching production-only failures.

- **Settings API cross-nulling** — `register_setting( $group, $option )` adds `$option` to WordPress's `allowed_options[$group]` array. When **any** form posts to `options.php` for that `$group`, WP iterates every registered option in the group and calls `update_option( $opt, $_POST[$opt] ?? null )` — i.e. **an option registered to the group but missing from the submitted form gets `null`-set on every save**. A `'on'/'off'` sanitizer that returns `'off'` on null then silently disables the feature; a checkbox-bool sanitizer that returns `false` on null silently unchecks it.
  - Detection: list every `register_setting( $GROUP, $OPTION, … )` call. For each `<form action="options.php">` that calls `settings_fields( $GROUP )`, grep the form body for `name="$OPTION"`. **Every option registered to a group must appear in every form posting to that group**, either as a visible control or as a hidden preservation row: `<input type="hidden" name="$OPTION" value="<?php echo esc_attr( get_option( $OPTION, $default ) ); ?>">`.
  - Severity: **Critical**. Symptom is silent: a setting the user toggled "on" mysteriously resets to "off" the next time they save anything else in the same tab.

- **`DISABLE_WP_CRON` assumption** — Plugin schedules work with `wp_schedule_single_event()` / `wp_schedule_event()` and assumes it will fire. Managed hosts (Kinsta, WP Engine, Cloudways, Pantheon) and any site that runs system cron set `define( 'DISABLE_WP_CRON', true )`. Scheduled events queue in `cron_array` and **never execute** unless wp-cron.php is invoked externally.
  - Detection: any `wp_schedule_*` call without (a) a manual trigger path that bypasses cron, (b) a system-cron setup notice in the admin, or (c) a fallback `Action Scheduler` integration.
  - Fix pattern: expose a direct `run_now()` method on every cron callback so the admin UI can fire it synchronously, and document the DISABLE_WP_CRON case in readme.txt.

- **Conditional `add_rewrite_rule()` based on an option, registered at `init`** — Plugin does `if ( get_option('feature') === 'on' ) { add_rewrite_rule(...); }` inside the `init` hook. Toggling the option in admin **doesn't immediately register the rule** because `init` already fired; calling `flush_rewrite_rules()` flushes nothing (rule doesn't exist in the rewrite array yet). Result: enabling a feature gives 404 until the next request **after** the rule registers.
  - Detection: every `add_rewrite_rule()` inside a conditional block. If the condition references an option, the toggle handler must also (a) call `add_rewrite_rule()` directly, then (b) `flush_rewrite_rules( false )`, OR (c) inject the rule into the `rewrite_rules` option directly.
  - Severity: **Critical** — feature appears broken to user even though the option says "enabled".

- **Bulk option restore that wipes existing user data** — A "reset to defaults" or "first-run install" routine that loops through a registry of options and calls `update_option( $opt, $DEFAULTS[$opt] )` without checking whether the option already has a non-default value. Common pattern in onboarding/setup wizards. Result: power user's existing config silently overwritten.
  - Detection: any loop over a defaults map that calls `update_option`. Must guard: `if ( get_option( $opt, $SENTINEL ) === $SENTINEL ) { update_option( $opt, $default ); }`.

- **Auto-generation hook only on `publish_post`, not `post_updated`** — Plugin generates content (summary, FAQ, schema, sitemap entry, etc.) on the `publish_post` action only. Posts that were already published *before* the plugin was installed never trigger generation; posts re-edited *after* the plugin was installed don't re-trigger.
  - Detection: any `add_action( 'publish_post', … )` without a paired `save_post` or `post_updated` handler. Confirm the generation is idempotent (won't re-run on every meta update) by checking for a content-hash style guard (`_myplugin_content_hash` meta or equivalent).

- **Hard-coded `$_GET`/`$_POST` reads without `wp_unslash()`** — `$x = $_POST['key'];` or `if ( $_GET['key'] === 'value' )` — WordPress magically slash-escapes superglobals on load (legacy magic_quotes behavior). Reading them raw leaves stray backslashes in saved data. PHPCS warning #18 in the WP.org release gate.
  - Detection: regex `\$_(?:GET|POST|REQUEST|COOKIE|SERVER)\[` followed by an assignment or comparison, without `wp_unslash(` in the same expression.
  - Note: bare `isset()` / `empty()` checks are safe (don't read the value).

- **Meta value type drift (JSON string vs PHP array)** — Code writes meta with `update_post_meta( $id, $key, wp_json_encode( $data ) )` (string) but readers do `is_array( $meta )` or `count( $meta )` (array). Same plugin, two different mental models. The string-as-meta path silently fails the array check; downstream features (rendering, schema output, REST exposure) appear "not generated" even though the data is there.
  - Detection: for every plugin-namespaced meta key (`_$prefix_*`), find every read site. If any reader does `is_array()` / `count()` / `foreach`, then every writer must `wp_json_encode` AND every reader must `json_decode( …, true )` first. Or pick one canonical storage shape (pass the array directly to `update_post_meta` and let WP serialize) and stick with it. Mixed shapes = bug.

- **`%currentyear%` / `%year%` / `%sitename%` / other date or site tokens stored as literals in third-party SEO plugin meta** — Rank Math / Yoast / SEOPress resolve their own `%token%` syntax only on **render** of their own meta fields. When *your* plugin writes a generated title or description into Rank Math's / Yoast's meta with `%currentyear%` already in the string, the token gets stored as a literal but their resolver never runs on it (the filter fires on the user-typed string at save, not on programmatically inserted values). Result: the live SERP shows `Title for %currentyear%`.
  - Detection: any `update_post_meta( …, 'rank_math_title', $value )` / `update_post_meta( …, '_yoast_wpseo_title', $value )` / equivalent where `$value` contains `%[a-z_]+%`. Either resolve the token in your code before writing (e.g. `str_replace( '%currentyear%', wp_date( 'Y' ), $value )`), OR call the SEO plugin's own replacement filter (`apply_filters( 'rank_math/replacements', $value )` or `wpseo_replace_vars( $value, $post )`) to resolve via their pipeline.

- **Compliance / text-statistics checks that count tokens inside Gutenberg block comments** — Em-dash counter, readability scorer, word counter, "banned phrase" check, or any text statistic that runs over raw `post_content` (`substr_count`, `str_word_count`, regex match). Gutenberg block delimiters (`<!-- wp:paragraph -->`, `<!-- /wp:paragraph -->`, `<!-- wp:foo {"bar":"…"} /-->`) contain characters that get miscounted: dashes, attribute JSON, block names. Result: false positives — every Gutenberg post fails the check even when the visible content is clean.
  - Detection: any text-statistics function that takes raw `post_content` as input. Must first strip block delimiters before counting: `preg_replace( '/<!--\s*\/?wp:[^>]+-->/', '', $content )`, OR pass `apply_filters( 'the_content', $content )` first to render to HTML, then strip tags with `wp_strip_all_tags()`.

- **Tab/route slug mismatch between linker and router** — Admin UI links to `admin.php?page=myplugin&tab=content-ai` but the router only recognizes `tab=content`. The router default-cases back to the dashboard, so the dashboard tile silently drops the user on the wrong tab. Variant: REST route registered as `myplugin/v1/foo` but the JS client posts to `myplugin/v1/foos` (singular vs plural) — 404 with no error in the UI.
  - Detection: collect every `tab=$slug` / `?page=$slug` link in admin code and every `fetch(`/`apiFetch(` URL in JS. Collect every `case '$slug':` in the router switch and every `register_rest_route` path. Diff. Any link that doesn't resolve is broken navigation.

- **Cache invalidation forgets the new bucket** — Plugin adds a new transient or object-cache key in v1.1 but the existing `flush_all_caches()` method still only deletes the v1.0 keys. Result: stale cache wins after upgrade and the new feature appears broken.
  - Detection: every `set_transient( "$prefix_*", … )` / `wp_cache_set( ..., "$prefix_*" )` must have a matching `delete_transient` / `wp_cache_delete` in the central flush method. List all set sites, list all delete sites, diff. Bonus: also check that `upgrade_routine()` flushes the cache when DB-schema or option shape changes between versions.

- **Pro / Free dual-class shadow conflict** — A Free plugin and its commercial add-on both define `class Plugin_Foo`. If both load and the Free autoloader resolves the class first, the Pro override never wins — PHP fatals on redeclaration if both files are required, or silently uses Free's version if only one is loaded. Symptoms vary by autoloader: PSR-4 / spl_autoload_register-based: fatal. `require_once` with `class_exists()` guards: silently wrong class wins.
  - Detection: any class defined in **both** the Free codebase and the Pro add-on codebase must use a `class_exists( 'Plugin_Foo' ) || class …` guard in **both** files, OR the Pro add-on must extend the Free class under a different name (`class Plugin_Foo_Pro extends Plugin_Foo`) and inject itself via a filter that the Free class exposes. Audit by listing every class name in both codebases and intersecting.

- **`is_pro()` / capability-check filter consulted before the registration runs** — Free plugin reads `apply_filters( 'myplugin_is_pro', false )` at `plugins_loaded` priority 10. The Pro add-on registers the filter callback at `plugins_loaded` priority 10. Plugin load order is **alphabetical** by folder name — if the Free folder sorts before the Pro folder, the Free check fires first and gets `false` even when Pro is active. Result: Pro features stay locked when Pro is installed and active.
  - Detection: any `apply_filters( '*_is_pro', … )` / `*_is_premium` / `*_has_license` call. The reader must run at priority **20 or later** on `plugins_loaded`, OR on `init` / later. Cross-check the priority of the reader vs the registrar. Same pattern applies to any cross-plugin filter where one plugin reads a value the other plugin registers — load order matters.

- **Activation hook side-effects that assume plugin constants/classes are loaded** — Plugin bootstrap defines `MYPLUGIN_VERSION`, requires class files, **then** registers the activation hook. But `register_activation_hook()` can fire its callback in a context where the rest of the bootstrap hasn't fully run — multisite network activate, WP-CLI bulk activate, or the upload-and-activate flow on first install. Callbacks that reference `MYPLUGIN_VERSION` or `MyPlugin_Welcome::flag_activation()` fatal with "undefined constant" / "class not found".
  - Detection: every `register_activation_hook` callback. Inspect for plugin-namespaced constants or class references. Each one must be guarded: `if ( ! defined( 'MYPLUGIN_VERSION' ) ) return;` and `if ( class_exists( 'MyPlugin_Welcome' ) ) MyPlugin_Welcome::flag_activation();`. Same rule for the deactivation and uninstall hooks.

---

## How to invoke

```bash
claude "/orbit-code-quality Review ~/plugins/my-plugin — flag every dead-code, complexity, error-handling, type-safety, and AI-hallucination risk. Output markdown with severity per finding."
```

Or via the gauntlet (runs in Step 11):
```bash
bash scripts/gauntlet.sh --plugin . --mode full
```

Output: `reports/skill-audits/code-quality.md`.

---

## Report format

```markdown
# Code Quality Audit — [Plugin]

## Summary

| Category | Critical | High | Medium | Low |
|---|---|---|---|---|
| Dead code | 0 | 0 | 4 | 12 |
| Complexity | 0 | 2 | 5 | 0 |
| Error handling | 1 | 3 | 6 | 0 |
| Type safety | 0 | 1 | 4 | 8 |
| AI-hallucination risks | 1 | 2 | 0 | 0 |
| **WordPress runtime traps** | 2 | 4 | 1 | 0 |

## Critical

### AI-hallucinated function — `get_user_metadata_with_caps()`
**File:** includes/class-user.php:42
**Code:** `$caps = get_user_metadata_with_caps( $user_id );`
**Issue:** `get_user_metadata_with_caps()` does not exist in WordPress core or this plugin. Looks like a Cursor hallucination of `get_user_meta()` + `get_userdata()`.
**Fix:** Use `get_user_meta()` and check capabilities separately:
```php
$meta = get_user_meta( $user_id, 'my_meta_key', true );
if ( user_can( $user_id, 'edit_posts' ) ) { ... }
```

[Repeat for every finding — file:line, code, issue, fix]

## High
[...]

## Medium
[...]

## Low
[...]
```

---

## What this skill does NOT do

- ❌ It is not a security scanner — that's `/orbit-wp-security`.
- ❌ It is not a performance profiler — that's `/orbit-wp-performance`.
- ❌ It is not WP standards (PHPCS) — that's `/orbit-wp-standards`.
- ❌ It does not generate new code or refactor — read-only review.

---

## Rules

1. **Read every file before writing the report.** Skip vendor/, node_modules/, build/.
2. **Tag severity by impact:**
   - Critical: hallucinated function (will crash) | empty `catch` swallowing fatal | missing nonce on writable handler | Settings API cross-nulling | conditional add_rewrite_rule causing persistent 404 | class-name case drift that fatals in prod
   - High: complexity > 15 | type juggle that returns wrong value | wrong sanitize on user input | DISABLE_WP_CRON assumption | bulk option restore wiping user data | meta type drift between writer and reader | cross-plugin filter timing trap | %currentyear% literal in third-party SEO meta
   - Medium: dead code in a class still in use | error path not tested | em-dash false positive on Gutenberg block comments | tab/router slug mismatch
   - Low: minor naming | unused private method | cosmetic CSS double-line
3. **Always reference file:line.** Without it, the finding is useless.
4. **Suggest the fix in code.** "Add a nonce check" is not a fix. Show the exact `wp_verify_nonce()` call.
5. **AI-hallucination tag**: any finding that looks like AI made it up gets a `🤖 AI-RISK` flag in addition to severity. This helps reviewers triage Cursor/Copilot PRs.
6. **Runtime-trap tag**: any §6 finding gets a `⚠️ RUNTIME-TRAP` flag. These are bugs that pass linters, pass unit tests, pass code review, and only break on a live install — they need special triage because they look fine in isolation and only fail when the WordPress runtime contract bites.
7. **Self-improvement**: if you find a class of WordPress runtime bug that this skill's §6 doesn't already enumerate, **add it to §6 with a grep recipe** before closing the audit. This skill is a learning system — each missed bug type that escaped to prod gets folded back in so the next audit catches it.

---

## When to run

| Situation | Run this skill? |
|---|---|
| After every commit | No — too slow. Use `/orbit-pre-commit` instead. |
| Before merging any PR | **Yes** — especially if AI-assisted. |
| Before tagging a release | Yes — runs as part of `/orbit-gauntlet --mode release`. |
| After a major refactor | Yes — complexity findings shift dramatically. |
| Quarterly tech-debt review | Yes — focus on Medium findings to clean up. |

---

## The Veracode stat

**45% of AI-assisted code has at least one OWASP Top 10 vulnerability** (Veracode 2025 study). Don't merge AI PRs on auto-pass. This skill is your last line of defence.

---

## Pair with `/orbit-wp-standards`

`/orbit-wp-standards` finds **WP API misuse** (wrong escaping, missing capability check). This skill finds **architectural / craftsmanship issues** (dead code, complexity, AI hallucinations). Run both on every PR — they don't overlap.
