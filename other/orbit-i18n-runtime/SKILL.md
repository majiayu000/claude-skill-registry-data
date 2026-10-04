---
name: orbit-i18n-runtime
description: Runtime i18n correctness audit — catches the non-Latin data corruption bugs that gettext-style audits miss. Scans every wp_json_encode / json_encode call in paths that store post_meta, options, REST output, or LLM/external-API request bodies; flags any missing JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES flag. Also verifies Content-Type charset=utf-8 on REST responses. Use when the user says "i18n runtime", "Unicode encoding", "non-Latin characters", "Turkish broken", "CJK garbage", "data corruption on save", or before any release that ships to non-English locales.
---

# 🪐 orbit-i18n-runtime — Runtime data i18n correctness

`orbit-i18n` is gettext-only — it checks UI strings get wrapped in `__()`. This skill checks the **other half of i18n**: when the plugin writes Turkish, CJK, Arabic, Hindi, Cyrillic, or any non-Latin data into post_meta / options / REST responses / outgoing API bodies, does it survive the round-trip without corruption?

**Why this skill exists:** example-plugin shipped v1.0.x storing non-Latin content as `\uXXXX` escape sequences via default `wp_json_encode()`. WordPress's sanitization filters dropped the backslashes; "Yatırım" became visible garbage "Yu0131lu0131" in the database. The fix required patching 4 modules + 4 LLM provider classes + a 1-shot migration to repair existing data. `orbit-i18n` did not catch it because it was looking at `__()` wrapping, not JSON encoding flags. Plugin-agnostic — applies to any WP plugin that stores or transmits user-supplied content.

---

## What this skill checks

### 1. `wp_json_encode()` / `json_encode()` in storage paths

Scan every call site. If the encoded value flows into:
- `update_post_meta()`, `add_post_meta()`, `update_metadata()`, `update_user_meta()`, `update_term_meta()`
- `update_option()`, `update_site_option()`, `set_transient()`
- A REST response body (`rest_ensure_response`, `WP_REST_Response`)
- A `wp_remote_post()` / `wp_remote_request()` body posted to any external HTTP endpoint

Then it MUST include both flags:
```php
wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
```

#### ❌ Bad
```php
update_post_meta( $post_id, '_my_summary', wp_json_encode( $summary ) );
// "Yatırım" → "Yatırım" in DB → backslash-stripped → "Yu0131ru0131m" garbage
```

#### ✅ Good
```php
update_post_meta(
    $post_id,
    '_my_summary',
    wp_json_encode( $summary, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES )
);
```

### 2. LLM / external-API outgoing bodies

Every `wp_remote_post( $url, [ 'body' => ... ] )` where the body is JSON-encoded must use the flags. Without them:
- Wire bytes inflate ~6× for CJK / Arabic / Hindi content
- Token billing inflates proportionally
- Some upstream providers reject `\uXXXX` sequences in specific fields

#### Detection grep
```bash
# Files using wp_json_encode without UNESCAPED_UNICODE on the same line or next line
grep -rn 'wp_json_encode\|json_encode' --include='*.php' . \
  | grep -v 'JSON_UNESCAPED_UNICODE' \
  | grep -v 'tests/'
```
Every hit is a candidate. Inspect each: is the encoded value persisted or sent externally? If yes → flag.

### 3. REST response `Content-Type` charset

Custom REST routes that ship translated content MUST set `charset=utf-8` explicitly. Default WP responses do this, but custom output paths via `wp_die()`, `echo`, or direct `header()` calls often forget.

#### ❌ Bad
```php
header( 'Content-Type: text/markdown' );
echo $markdown;  // browser guesses encoding → mangles non-Latin
```

#### ✅ Good
```php
header( 'Content-Type: text/markdown; charset=utf-8' );
echo $markdown;
```

#### Detection grep
```bash
grep -rn "header(.*Content-Type" --include='*.php' . \
  | grep -v 'charset=utf-8' \
  | grep -v 'tests/'
```

### 4. Round-trip safety: writer/reader flag parity

If the writer uses `JSON_UNESCAPED_UNICODE`, the reader's `json_decode()` works on either format — no change needed. BUT: if you mix writers (some flagged, some not) on the same meta key, you get garbled data depending on which writer last wrote.

**Audit pattern:**
1. Find every plugin-namespaced meta key written via JSON encoding.
2. List every call site for that key.
3. All writers must use the same flag set.

### 5. Migration / repair routine for legacy data

If the plugin previously shipped without the flags, an upgrade routine must re-encode existing rows:

```php
add_action( 'plugins_loaded', function() {
    if ( get_option( 'myplugin_unicode_meta_migrated_v_X_Y_Z' ) ) {
        return;
    }
    // Query postmeta for rows containing \uXXXX patterns, json_decode + wp_json_encode
    // with new flags, $wpdb->update. Batch-cap at 2000 rows per request.
    // Set the option flag when row count < 2000.
} );
```

The skill flags the ABSENCE of this routine when the plugin's version history shows a pre-flag → post-flag transition.

### 6. Magic-quotes / `wp_unslash` interaction

After reading `$_POST` content destined for JSON encoding, `wp_unslash()` is mandatory BEFORE encoding. Without it, backslashes from slash-escaping survive into the encoded payload and combine with `\uXXXX` sequences to produce double-corrupted output.

```php
// ❌
$data = $_POST['data'];
update_post_meta( $id, '_my_data', wp_json_encode( $data ) );

// ✅
$data = wp_unslash( $_POST['data'] );
update_post_meta(
    $id, '_my_data',
    wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES )
);
```

---

## Report format

```markdown
# i18n Runtime Audit — [Plugin]

## Summary
- wp_json_encode calls missing UNESCAPED_UNICODE: <N>
  - Persisted (post_meta/options): <X>     ← Critical
  - External API bodies:           <Y>     ← High
  - REST responses:                <Z>     ← High
  - Read-only / logs:              <W>     ← Low
- REST routes missing charset=utf-8: <N>
- Mixed writer/reader flag sets:     <N>
- Missing legacy-repair migration:    <Y/N>
- $_POST → wp_json_encode without wp_unslash: <N>

## Critical (block release)

### Persisted non-Latin corruption risk
**File:** includes/class-foo.php:305
**Code:**
```php
update_post_meta( $post_id, '_foo_data', wp_json_encode( $data ) );
```
**Fix:** add `JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES` to the second arg.
**Why:** stored \uXXXX → WP filter strips backslashes → "Yatırım" becomes "Yu0131ru0131m"

[Continue for every finding]
```

---

## Plug-in agnostic

This skill never references example-plugin or any specific plugin. It scans for **patterns**, not bugs. If a future plugin (example-plugin, example-plugin, example-plugin, third-party) ships any of the call shapes above without the flags, this skill flags it.

---

## Cross-references

- **`orbit-i18n`** — covers gettext wrapping. Run both. Different surfaces.
- **`orbit-i18n-js-parity`** — JS↔PHP label mismatches (different bug class).
- **`orbit-compat-polylang` / `orbit-compat-wpml`** — language-aware custom endpoints (different bug class — see §7 in each).
- **§10.6 in orbit-code-reviewer** — `$_POST` reads without `wp_unslash()` (related, broader scope).
- **CTO brain `orbit/00-cto`** — promote new corruption patterns here when discovered.

---

## Severity

- Persisted-meta corruption: **Critical** (silent data loss; multi-version migration to fix)
- External API body without flag: **High** (token inflation + potential upstream rejection)
- REST response without charset: **High** (consumer-side display corruption)
- Mixed flag sets across writers: **High** (last-writer-wins data corruption)
- Missing legacy-repair migration: **High** (existing installs stay broken after fix)
- `$_POST` without `wp_unslash` before encode: **High**

Block release on any Critical or High that isn't an explicit accepted risk in `orbit/00-cto`.
