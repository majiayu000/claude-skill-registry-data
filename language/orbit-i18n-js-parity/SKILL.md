---
name: orbit-i18n-js-parity
description: PHP↔JS label parity audit — verifies every label key consumed by JS via `wp_localize_script` / `wp_set_script_translations` is actually emitted from PHP. Catches the silent-English-fallback bug where JS reads `myObject.someLabel` but PHP never put `someLabel` into the localized object. Use when the user says "JS label", "wp_localize_script", "Elementor editor label", "Gutenberg block label", "missing translation in JS", or before any release that touches block editor / Elementor / admin JS.
---

# 🪐 orbit-i18n-js-parity — JS↔PHP label parity

The skill that catches the bug `orbit-i18n` cannot see: **the PHP side wraps every string in `__()` correctly, but the JS side reads a key the PHP never localizes.** Result: JS falls back to English (or `undefined`), and no warning, no error, no test fails. The string just silently never translates.

**Why this skill exists:** example-plugin's Elementor editor showed an English "Generate FAQ" button in every language because `class-rnrd-elementor.php` localized `rnrdElEditor.generateSummary` but not `rnrdElEditor.generateFaq` — the JS read the missing key, defaulted to a hardcoded English fallback, and shipped to production. Plugin-agnostic — applies to any plugin with PHP-localized JS labels.

---

## What this skill checks

### 1. Collect every `wp_localize_script` emit

Scan every PHP file for:
```bash
grep -rn 'wp_localize_script' --include='*.php' . | grep -v 'tests/'
```

For each call, extract:
- The script handle (arg 1)
- The JS object name (arg 2)
- The array of keys (arg 3)

Build a table:
```
HANDLE                 JS OBJECT          KEYS EMITTED
rnrd-elementor-editor  rnrdElEditor       generateSummary, regenerateSummary, generatingSummary
```

### 2. Collect every `wp_set_script_translations` emit

```bash
grep -rn 'wp_set_script_translations' --include='*.php' .
```

For each: handle + textdomain + path. Required for `wp.i18n.__()` calls in JS to resolve.

### 3. Collect every JS read of the localized object

For each JS object name discovered in §1, grep the JS sources:
```bash
grep -rn 'rnrdElEditor\.\w\+\|window\.rnrdElEditor\.\w\+' --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' assets/ src/ build/ 2>/dev/null
```

Build a table:
```
JS OBJECT          KEYS READ
rnrdElEditor       generateSummary, regenerateSummary, generatingSummary,
                   generateFaq, regenerateFaq, generatingFaq        ← extra keys
```

### 4. Diff EMITTED vs READ

```
ORPHAN KEYS (JS reads, PHP doesn't emit):
  rnrdElEditor.generateFaq            ← FAIL — JS shows fallback / undefined
  rnrdElEditor.regenerateFaq          ← FAIL
  rnrdElEditor.generatingFaq          ← FAIL

UNUSED KEYS (PHP emits, JS never reads):
  rnrdElEditor.legacyButton           ← cleanup candidate (low priority)
```

Every orphan key is a Critical i18n bug.

### 5. JS `wp.i18n.__()` calls without script translations

For every JS file using `__('Some string', 'plugin-textdomain')` or `import { __ } from '@wordpress/i18n'`:
- Trace the JS file back to its enqueued script handle (via `wp_enqueue_script` + script path)
- Confirm a matching `wp_set_script_translations( $handle, 'plugin-textdomain', $languages_path )` call exists

If the handle isn't covered → `wp.i18n.__()` silently returns the English source string. Critical.

### 6. Object name collision check

Multiple `wp_localize_script` calls writing to the same JS object name on different handles → only the last one wins on the page where both scripts load. Catches the "I added the keys, why are they still missing?" bug.

```bash
# Sort by JS object name, count occurrences > 1
grep -rn 'wp_localize_script' --include='*.php' . \
  | awk -F"'" '{print $4}' | sort | uniq -c | sort -rn
```

Collisions need either a single localization point or distinct object names per handle.

### 7. Translator comment coverage in JS

Every `__()` / `_x()` in JS must be preceded by a translator comment if the string has placeholders or context ambiguity:
```js
// translators: %d is the number of items found
const label = sprintf( __( '%d items found', 'myplugin' ), count );
```

Same rule as `orbit-i18n` step 4, but on the JS side. POT extraction (`wp i18n make-pot`) scans JS — translator comments must be on the line directly above.

---

## Report format

```markdown
# i18n JS Parity Audit — [Plugin]

## Summary
- wp_localize_script calls:          <N>
- wp_set_script_translations calls:  <N>
- JS object names in use:            <N>
- Orphan JS reads (Critical):        <N>   ← list each
- Unused PHP emits (Info):           <N>
- JS handles missing translations:   <N>   ← list each
- Object-name collisions:            <N>
- JS strings without translator cmt: <N>

## Critical findings

### Orphan key: rnrdElEditor.generateFaq
**JS file:** assets/elementor-editor.js:142
**Read:** `rnrdElEditor.generateFaq`
**PHP localize site:** includes/class-rnrd-elementor.php:88
**Emitted keys:** generateSummary, regenerateSummary, generatingSummary
**Fix:** add `'generateFaq' => esc_html__( 'Generate FAQ', 'plugin-textdomain' )` to the array.

[Continue for every orphan]
```

---

## Plugin-agnostic detection algorithm

```
INPUT: plugin root directory
STEP 1: PHP_EMITS  = parse all wp_localize_script(handle, obj, keys[])
STEP 2: JS_READS   = parse all <obj>.<key> across JS files
STEP 3: ORPHANS    = JS_READS \ PHP_EMITS  (set difference)
STEP 4: UNUSED     = PHP_EMITS \ JS_READS  (set difference, low severity)
STEP 5: HANDLES_NO_TRANS = JS files using wp.i18n.__ \ wp_set_script_translations(handle)
STEP 6: OBJECT_COLLISIONS = JS objects emitted by >1 handle, both enqueued on same page
OUTPUT: severity-ranked finding list
```

---

## Cross-references

- **`orbit-i18n`** — gettext side (every `__()` call). Run both. Different surfaces.
- **`orbit-i18n-runtime`** — JSON encoding flags (different bug class).
- **WP.org Plugin Check** — has a similar but coarser scan; this skill catches more.
- **§10.10 in orbit-code-reviewer** — Tab/REST route slug mismatch (analogous bug class for navigation).

---

## Severity

- Orphan JS read (key absent in PHP):   **Critical** (silent English/undefined fallback)
- JS file using `__()` with no `wp_set_script_translations`: **Critical**
- Object-name collision on same page:   **High**
- JS string without translator comment (placeholder/context): **Medium**
- Unused PHP-emitted key:                **Info** (cleanup, not blocking)
