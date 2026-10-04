---
name: wp-i18n-workflow
description: "Use when managing the full translation workflow for a WordPress plugin — registering text domain with load_plugin_textdomain, wrapping strings with __(), _e(), esc_html__(), esc_attr__(), _n(), _x(), _ex(), _nx(), generating POT with wp i18n make-pot, compiling .po to .mo (wp i18n make-mo / msgfmt) and .json (wp i18n make-json), wiring JS translations with wp_set_script_translations and @wordpress/i18n (__, _n, _x, sprintf), adding translator comments, submitting to translate.wordpress.org / GlotPress, automating in GitHub Actions, or debugging missing translations. Triggers: \"make this string translatable\", \"generate POT file\", \"strings not translating\", \"wp i18n make-pot\", \"JS translations not loading\", \"wp_set_script_translations\", \"how do I translate my block\", \"RTL language support\", \"missing translation\", \"submit to GlotPress\", \"translation missing in JS\", \"update my .po files\", \"load_plugin_textdomain\", \"__ vs esc_html__\", \"_n() plural strings\", \"_x() context string\", \"translator comment format\", \"wp i18n make-json\", \"msgfmt compile\", \"translate.wordpress.org submission\", \"language pack\", \"text domain mismatch\", \"i18n automation in CI\". Not for: theme translation (paths differ, but logic is the same)."
---

# WordPress Plugin i18n Workflow

> **Model note:** Fully mechanical — POT generation, PO/MO compilation, and script registration are tool invocations. `haiku` handles all steps; no cross-file reasoning needed.

Full translation pipeline for WordPress plugins: POT generation, PO/MO compilation, JavaScript translations, translate.wordpress.org GlotPress, and language pack distribution. Covers the coding conventions and the tooling workflow.

## When to use

- "Generate a POT file for my plugin", "update translation strings".
- "Set up JavaScript translations", "translate strings in React/block editor".
- "Submit to translate.wordpress.org", "set up language packs".
- "Why aren't my translations loading?", "debug missing .mo file".
- "Add translator comments", "handle plurals and context strings".

**Not for:** PHPCS i18n sniff violations — use `wp-coding-standards`. Checking i18n completeness in an audit — use `wp-plugin-audit` Dimension B.

## Method

### 1. PHP i18n conventions

All translatable strings must use the plugin's **text domain** consistently. The text domain must match the `Text Domain:` header and the `load_plugin_textdomain()` call.

```php
// Basic translation
__( 'Settings', 'my-plugin' )
_e( 'Save Changes', 'my-plugin' )        // echo version

// With HTML context (escape + translate combined)
esc_html__( 'Error message', 'my-plugin' )
esc_attr__( 'Tooltip text', 'my-plugin' )

// Plurals
_n( '%d item', '%d items', $count, 'my-plugin' )
sprintf( _n( '%d item', '%d items', $count, 'my-plugin' ), $count )

// Context strings (disambiguation for translators)
_x( 'Post', 'noun: a blog post', 'my-plugin' )
_ex( 'Draft', 'verb: save as draft', 'my-plugin' )

// Plural with context
_nx( '%d reply', '%d replies', $count, 'comment count', 'my-plugin' )
```

**Translator comments** — required for strings with placeholders:
```php
/* translators: %s: plugin version number */
sprintf( __( 'Version %s', 'my-plugin' ), MY_PLUGIN_VERSION )

/* translators: 1: post title, 2: author name */
sprintf( __( '"%1$s" by %2$s', 'my-plugin' ), $title, $author )
```
Comment must be on the line immediately before the function call and start with `translators:`.

### 2. Load text domain

```php
add_action( 'init', function() {
    load_plugin_textdomain(
        'my-plugin',
        false,
        dirname( plugin_basename( __FILE__ ) ) . '/languages/'
    );
} );
```

For WP.org plugins, language packs are auto-loaded from `translate.wordpress.org` — `load_plugin_textdomain()` only needed for bundled `.mo` files or local development.

### 3. Generate POT file

```bash
# WP-CLI (preferred)
wp i18n make-pot . languages/my-plugin.pot \
  --domain=my-plugin \
  --exclude=vendor,node_modules,tests,build \
  --headers='{"Project-Id-Version":"My Plugin 1.0.0","Report-Msgid-Bugs-To":"https://github.com/my-org/my-plugin/issues"}'

# Update existing POT (merges new strings, marks removed as obsolete)
wp i18n make-pot . languages/my-plugin.pot --domain=my-plugin
```

Commit `languages/my-plugin.pot` to git. Translators use this as the source.

### 4. Compile PO → MO

`.po` files are human-editable; `.mo` are compiled binary files loaded by PHP.

```bash
# Single file
wp i18n make-mo languages/my-plugin-fr_FR.po

# All PO files in the directory
wp i18n make-mo languages/

# Using msgfmt (gettext tools)
msgfmt languages/my-plugin-fr_FR.po -o languages/my-plugin-fr_FR.mo
```

File naming convention: `{text-domain}-{locale}.po` / `.mo`
Examples: `my-plugin-fr_FR.mo`, `my-plugin-de_DE.mo`, `my-plugin-pt_BR.mo`

### 5. JavaScript translations

**Block editor / React components** — use `@wordpress/i18n`:

```js
import { __, _n, _x, sprintf } from '@wordpress/i18n';

const label = __( 'Save settings', 'my-plugin' );
const count = sprintf( _n( '%d item', '%d items', total, 'my-plugin' ), total );
const ctx   = _x( 'Draft', 'button label', 'my-plugin' );
```

**Generate JSON translation files:**
```bash
# From PO file — produces my-plugin-fr_FR-{hash}.json
wp i18n make-json languages/my-plugin-fr_FR.po --no-purge
```

**Register JS translations in PHP:**
```php
function my_plugin_set_script_translations() {
    wp_set_script_translations(
        'my-plugin-editor',   // script handle (must be enqueued)
        'my-plugin',          // text domain
        plugin_dir_path( __FILE__ ) . 'languages'
    );
}
add_action( 'init', 'my_plugin_set_script_translations' );
```

For blocks registered via `block.json`, WP auto-calls `wp_set_script_translations` if `textdomain` is set in `block.json`:
```json
{
    "textdomain": "my-plugin",
    "editorScript": "file:./index.js"
}
```

### 6. translate.wordpress.org (GlotPress)

WP.org plugins get a GlotPress project automatically once approved. Language packs are built weekly and distributed via the WP update system.

**Setup steps:**
1. Plugin approved on WP.org → GlotPress project auto-created at `translate.wordpress.org/projects/wp-plugins/your-slug/`
2. Ensure `languages/` dir exists in SVN trunk with the `.pot` file
3. GlotPress imports strings from trunk automatically (or trigger via SVN commit)
4. Community translators contribute at `translate.wordpress.org`
5. At 95% translation completion, a language pack is created and distributed to users

**WP.org translation validator:** `https://i18n.svn.wordpress.org/`

**Correct POT headers for GlotPress:**
```
Project-Id-Version: My Plugin 1.0.0
Report-Msgid-Bugs-To: https://wordpress.org/support/plugin/my-plugin
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: LANGUAGE <LL@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
```

### 7. Debugging missing translations

**Checklist:**
```bash
# 1. Verify text domain matches header and load_plugin_textdomain()
grep -r "Text Domain:" *.php
grep -r "load_plugin_textdomain" includes/

# 2. Verify .mo file exists and locale matches WP locale
wp option get WPLANG   # should match e.g. fr_FR
ls languages/          # should have my-plugin-fr_FR.mo

# 3. Verify .mo can be loaded
wp eval "echo load_plugin_textdomain('my-plugin', false, 'path/to/languages/');"

# 4. Verify string is in POT
grep -A2 "your string" languages/my-plugin.pot

# 5. For JS translations — check JSON files exist
ls languages/*.json

# 6. Check wp_set_script_translations fires after script is enqueued
# (Must call AFTER wp_enqueue_script, usually on 'init' or 'enqueue_scripts')
```

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Strings show in English only | `.mo` missing or wrong locale | Run `wp i18n make-mo languages/` |
| JS strings not translated | JSON file missing or wrong handle | Run `wp i18n make-json`, verify handle |
| POT out of date | New strings not extracted | Re-run `wp i18n make-pot` |
| Translator comment not picked up | Not on immediately preceding line | Move comment to line above call |
| WP.org language pack not appearing | < 95% translated | Complete translations on translate.wordpress.org |

### 8. Automation — sync POT on release

Add to GitHub Actions or release workflow:
```yaml
- name: Generate POT
  run: wp i18n make-pot . languages/my-plugin.pot --domain=my-plugin --exclude=vendor,node_modules,build
- name: Compile MO files
  run: wp i18n make-mo languages/
- name: Generate JS JSON
  run: wp i18n make-json languages/ --no-purge
```

## Notes

- Never concatenate translatable strings: `__( 'Hello' ) . ' ' . __( 'World' )` — translators can't reorder. Use `sprintf( __( 'Hello %s', 'my-plugin' ), $name )`.
- Never use variables as the first argument: `__( $dynamic_string, 'my-plugin' )` — POT extractors can't find these strings.
- RTL languages (Arabic, Hebrew, Farsi): WordPress detects RTL from the locale and loads `rtl.css` automatically. Mirror your `style.css` in `style-rtl.css` for layout flips.
- `wp i18n` commands require WP-CLI 2.2+. In CI, install via `curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar`.

## References

- `references/js-i18n-patterns.md` — JavaScript i18n patterns using `@wordpress/i18n`: `__()`, `_n()`, `sprintf()` usage, Gutenberg block translation, and dynamic string handling
- `references/pot-commands.md` — WP-CLI i18n command reference: `make-pot`, `make-mo`, `make-json`, `update-po` with all options and CI-ready invocations
- `references/translation-debugging.md` — Translation debugging guide: common failure modes, locale loading order, `.mo` vs `.json` file issues, and `QM` debug tools
