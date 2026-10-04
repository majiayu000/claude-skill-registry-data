---
name: orbit-i18n
description: Internationalization (i18n) audit for a WordPress plugin — checks every user-facing string is wrapped in `__()`/`_e()`/etc., text domain matches the plugin slug, POT file is fresh, locale-loading hook is on `init`/`plugins_loaded` (not earlier), placeholders use `%1$s` for translator-friendly word order, and pluralization uses `_n()`. Use when the user says "i18n", "translation", "POT", "text domain", "make plugin translatable", or before a release with new strings.
---

# 🪐 orbit-i18n — Translation readiness audit

A plugin that ships with hardcoded English strings is broken for 60% of WordPress users. This skill catches every gap.

---

## Quick start

```bash
# Auto-fix path: regenerate the POT file
wp i18n make-pot ~/plugins/my-plugin languages/my-plugin.pot --slug=my-plugin

# Audit path: find every untranslated string
claude "/orbit-i18n Audit ~/plugins/my-plugin — find every user-facing string, verify text domain, check POT freshness."
```

Runs in `/orbit-gauntlet --mode full` (Step 5).

---

## What this skill checks

### 1. Every user-facing string is wrapped

```php
// ❌ BAD
echo 'Settings saved';
echo '<h2>My Plugin Settings</h2>';
return new WP_Error( 'fail', 'Could not save' );

// ✅ GOOD
echo esc_html__( 'Settings saved', 'my-plugin' );
echo '<h2>' . esc_html__( 'My Plugin Settings', 'my-plugin' ) . '</h2>';
return new WP_Error( 'fail', __( 'Could not save', 'my-plugin' ) );
```

Catches strings in: `echo`, `print`, `?>...<?php`, `wp_die()`, `WP_Error` messages, admin notices, `sprintf()` template, JS `wp.i18n.__()`.

### 2. Text domain matches plugin folder name

```php
// Plugin folder: my-plugin/
// Plugin header: Text Domain: my-plugin

// ❌ Mismatch
__( 'Hello', 'myplugin' )      // Wrong (no dash)
__( 'Hello', 'my_plugin' )     // Wrong (underscore)
__( 'Hello', 'MyPlugin' )      // Wrong (camel-case)

// ✅ Exact match
__( 'Hello', 'my-plugin' )
```

WP.org **rejects** plugins with text domain mismatches. This is non-negotiable.

### 3. Locale-loading hook timing

```php
// ❌ Too early — locale isn't ready
load_plugin_textdomain( 'my-plugin', false, basename( __DIR__ ) . '/languages' );

// ❌ Too early in `muplugins_loaded`
add_action( 'muplugins_loaded', 'my_plugin_load_textdomain' );

// ✅ Right hook — `init` (preferred) or `plugins_loaded`
add_action( 'init', 'my_plugin_load_textdomain' );

function my_plugin_load_textdomain() {
    load_plugin_textdomain(
        'my-plugin',
        false,
        dirname( plugin_basename( __FILE__ ) ) . '/languages'
    );
}
```

Note: WP 6.5+ preloads textdomains automatically — the manual call is a fallback for back-compat.

### 4. Translator-friendly placeholders

```php
// ❌ Hard for translators (German word order is different)
sprintf( __( '%s users found in %s seconds', 'my-plugin' ), $count, $time );

// ✅ Numbered placeholders + translator comment
sprintf(
    /* translators: 1: number of users, 2: number of seconds */
    __( '%1$d users found in %2$.2f seconds', 'my-plugin' ),
    $count,
    $time
);
```

### 5. Pluralization uses `_n()`

```php
// ❌ Doesn't work in languages with multiple plural forms (Russian, Polish, Arabic)
echo $count . ' ' . __( 'item' . ( $count === 1 ? '' : 's' ), 'my-plugin' );

// ✅ Correct — handles all 6 plural forms across languages
echo sprintf(
    _n( '%d item', '%d items', $count, 'my-plugin' ),
    $count
);
```

### 6. Context disambiguation with `_x()`

```php
// "Post" can mean noun (blog post) or verb (to post). Translators need context:
echo _x( 'Post', 'noun, blog post', 'my-plugin' );
echo _x( 'Post', 'verb, to publish', 'my-plugin' );
```

### 7. JavaScript translation (Gutenberg-compatible)

```php
// PHP — make strings available to JS
wp_set_script_translations( 'my-plugin-block', 'my-plugin', plugin_dir_path( __FILE__ ) . 'languages' );
```

```js
// JS — use wp.i18n
import { __ } from '@wordpress/i18n';
const label = __( 'Settings', 'my-plugin' );
```

### 8. POT file freshness

```bash
# Regenerate
wp i18n make-pot . languages/my-plugin.pot --slug=my-plugin

# Diff against committed
git diff languages/my-plugin.pot
# → Any non-trivial diff = strings changed since last regen → commit the new POT
```

The skill flags any string in code that is NOT in the POT file.

### 9. RTL readiness

```php
// In WP-Admin, use the dir-aware helpers
echo is_rtl() ? 'right-side' : 'left-side';
```

```css
/* Provide an RTL CSS file or use logical properties */
.my-button {
  margin-inline-start: 8px;  /* Auto-flips for RTL */
  /* NOT: margin-left: 8px; */
}
```

Plus ship `rtl.css` if you have any non-trivial admin styles.

---

## Report format

```markdown
# i18n Audit — [Plugin]

## Summary
- Hardcoded strings (untranslated): 47
- Text-domain mismatches: 3
- Locale-load hook issues: 1
- Placeholder issues: 8
- Pluralization issues: 2
- POT freshness: 14 strings missing from POT
- RTL readiness: ⚠ 2 hardcoded `margin-left` values

## Critical (block release)

### Text domain mismatch
**Files (3):**
- includes/class-admin.php:42 — `__( 'Save', 'myplugin' )`
- includes/class-admin.php:67 — `__( 'Cancel', 'myplugin' )`
- admin/views/settings.php:103 — `_e( 'Settings', 'myplugin' )`

**Fix:** Replace `'myplugin'` with `'my-plugin'` (matches Text Domain: header).

### Hardcoded English strings
**File:** admin/views/settings.php:18-92
**Count:** 23 strings
**Sample:**
- `<h1>My Plugin Settings</h1>`
- `<button>Save</button>`
- `<p>Configure your settings below.</p>`

[Continue for all findings]
```

---

## Common mistakes

| Anti-pattern | Why it breaks | Fix |
|---|---|---|
| `__( $variable, 'my-plugin' )` | Translator can't extract — string must be literal | Use `sprintf( __( 'Hello %s', 'my-plugin' ), $name )` |
| `__( 'a' . ' ' . 'b', 'my-plugin' )` | Concatenation hides string from POT | Single literal: `__( 'a b', 'my-plugin' )` |
| Loading text domain in plugin file root (not in a hook) | Runs before WP locale is ready | Move to `init` hook |
| Using `<a href="...">click here</a>` inside `__()` | Translators may break the HTML | Use `printf( __( 'Visit %s', 'my-plugin' ), '<a href="...">our site</a>' )` |
| Skipping `esc_html__()` and just using `__()` for output | XSS risk | Always escape on output |

---

## Block.json strings

Gutenberg block titles + descriptions are auto-translated if you set `textdomain`:

```json
{
  "apiVersion": 3,
  "name": "my-plugin/example",
  "title": "Example Block",
  "description": "Renders an example.",
  "textdomain": "my-plugin"
}
```

Run `wp i18n make-json` after updating block.json strings.

---

## Output paths

- POT file: `languages/<slug>.pot`
- Block translations: `languages/<slug>-<locale>-<handle>.json`
- RTL stylesheet: `assets/css/<file>-rtl.css` or use logical properties

---

## Test in another locale

```bash
# Switch the wp-env site to French
wp-env run cli wp language core install fr_FR
wp-env run cli wp site switch-language fr_FR
open http://localhost:8881/wp-admin
# Verify your plugin's UI is translated (or at least doesn't crash)
```

---

## Resources

- [WP Plugin Handbook — i18n](https://developer.wordpress.org/plugins/internationalization/)
- [GlotPress translation patterns](https://make.wordpress.org/polyglots/handbook/)
- [10up i18n best practices](https://10up.github.io/Engineering-Best-Practices/php/#i18n)
