---
name: wp-coding-standards
description: "Use when setting up PHPCS with WordPress Coding Standards (WPCS), configuring phpcs.xml.dist, running phpcs/phpcbf, fixing sniff violations, adding PHPCS to CI (GitHub Actions), configuring IDE integration, or verifying a plugin meets WP.org code style requirements. Covers squizlabs/php_codesniffer, wp-coding-standards/wpcs, dealerdirect/phpcodesniffer-composer-installer, WordPress-Extra, WordPress-Docs, WooCommerce-Core rulesets. Triggers: \"phpcs error\", \"WPCS violation\", \"fix my code style\", \"set up PHPCS\", \"configure phpcs.xml.dist\", \"my code fails PHPCS\", \"add linting to CI\", \"WordPress.Security.EscapeOutput sniff\", \"WordPress.WP.I18n error\", \"WordPress.NamingConventions sniff\", \"how do I ignore a phpcs rule\", \"phpcbf auto-fix\", \"phpcs in GitHub Actions\", \"add PHPCS to pre-commit hook\", \"vendor/bin/phpcs -i\", \"WordPress-Extra ruleset\", \"WordPress-Docs ruleset\", \"WooCommerce sniff\", \"phpcs.xml.dist example\", \"phpcs says my spacing is wrong\", \"fix indentation for WP standards\", \"PHPCS not finding WPCS\", \"dealerdirect installer\". Not for: PHPStan type analysis — use `wp-phpstan-stubs`."
---

# WordPress Coding Standards (PHPCS + WPCS)

> **Model note:** Setup and config steps are mechanical (`haiku`). Fixing sniff violations across many files works fine on `haiku`. Only reach for `sonnet`/`opus` when violations involve subtle logic (e.g. escaping inside complex SQL builders).

Configure and enforce the WordPress Coding Standards via PHP_CodeSniffer. WPCS is required for WP.org submission and is the canonical style guide for all WordPress PHP code.

## When to use

- "Set up PHPCS for my plugin", "add WordPress coding standards", "configure phpcs.xml".
- "Fix sniff violations", "run phpcbf", "auto-fix coding standards".
- "Add PHPCS to GitHub Actions / CI".
- "Why is PHPCS flagging X?", "suppress a false-positive sniff".
- Pre-submission audit: "is my code style WP.org–compliant?"

**Not for:** PHPStan static analysis or type checking — use `wp-phpstan-stubs`. Security auditing beyond style issues — use `wp-plugin-audit`.

## Method

### 1. Install

```bash
composer require --dev squizlabs/php_codesniffer wp-coding-standards/wpcs dealerdirect/phpcodesniffer-composer-installer
```

Current **WPCS is 3.1** (July 2026) — requires PHP 7.4+ and PHP_CodeSniffer 3.9+. Leave the requirement unpinned (as above) or pin `wp-coding-standards/wpcs:"^3.1"`; the 3.x line recognizes pluggable functions and reserved post types through WP 6.4/6.5 and defaults `minimum_supported_wp_version` to 6.2.

`dealerdirect/phpcodesniffer-composer-installer` auto-registers WPCS paths so no manual `--config-set` is needed. Verify:

```bash
vendor/bin/phpcs -i
# should list: WordPress, WordPress-Core, WordPress-Docs, WordPress-Extra
```

### 2. Configure `phpcs.xml.dist`

Place at project root. This is the canonical config file (`.dist` allows local `phpcs.xml` override).

```xml
<?xml version="1.0"?>
<ruleset name="My Plugin">
    <description>WordPress Coding Standards for My Plugin</description>

    <!-- What to scan -->
    <file>.</file>
    <exclude-pattern>vendor/*</exclude-pattern>
    <exclude-pattern>node_modules/*</exclude-pattern>
    <exclude-pattern>build/*</exclude-pattern>
    <exclude-pattern>*.min.js</exclude-pattern>
    <exclude-pattern>*.min.css</exclude-pattern>
    <exclude-pattern>tests/bootstrap.php</exclude-pattern>

    <!-- PHP version target -->
    <config name="testVersion" value="7.4-"/>

    <!-- Ruleset -->
    <rule ref="WordPress-Extra">
        <!-- Suppress if you use short array syntax (WP allows it since WP 5.5) -->
        <!-- <exclude name="Generic.Arrays.DisallowShortArraySyntax"/> -->
    </rule>
    <rule ref="WordPress-Docs"/>

    <!-- Text domain for i18n sniffs -->
    <rule ref="WordPress.WP.I18n">
        <properties>
            <property name="text_domain" type="array" value="my-plugin"/>
        </properties>
    </rule>

    <!-- Minimum WP version for deprecated functions -->
    <rule ref="WordPress.WP.DeprecatedFunctions">
        <properties>
            <property name="minimum_supported_version" value="5.9"/>
        </properties>
    </rule>

    <!-- Prefix all globals -->
    <rule ref="WordPress.NamingConventions.PrefixAllGlobals">
        <properties>
            <property name="prefixes" type="array" value="my_plugin,MyPlugin"/>
        </properties>
    </rule>

    <!-- Show sniff codes in output (for targeted suppression) -->
    <arg value="ps"/>
    <arg name="extensions" value="php"/>
    <arg name="colors"/>
</ruleset>
```

### 3. Run

```bash
# Check
vendor/bin/phpcs

# Auto-fix (safe mechanical fixes only — review after)
vendor/bin/phpcbf

# Single file or directory
vendor/bin/phpcs includes/class-my-class.php

# Show full sniff code for each violation (useful for writing suppressions)
vendor/bin/phpcs --report=full -s
```

### 4. Inline suppression

Suppress only when the sniff is a genuine false positive, not to hide real issues.

```php
// phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- escaped in template
echo $pre_escaped_html;

// phpcs:disable WordPress.DB.DirectDatabaseQuery
$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->prefix}my_table WHERE id = %d", $id ) );
// phpcs:enable WordPress.DB.DirectDatabaseQuery
```

Common false positives and correct suppression codes:

| Situation | Sniff to ignore |
|---|---|
| Pre-escaped variable via custom escaper | `WordPress.Security.EscapeOutput.OutputNotEscaped` |
| Intentional direct DB query with `prepare()` | `WordPress.DB.DirectDatabaseQuery.DirectQuery` |
| Custom DB cache managed explicitly | `WordPress.DB.DirectDatabaseQuery.NoCaching` |
| `__FILE__` used in `plugin_dir_url()` | `WordPress.Security.PluginMenuSlug` (rare) |
| Slow DB query that is intentional | `WordPress.DB.SlowDBQuery.slow_db_query_meta_query` |

### 5. Common sniff violations and fixes

**Missing nonce verification:**
```php
// Bad
$value = sanitize_text_field( $_POST['field'] );

// Good
if ( ! isset( $_POST['my_plugin_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['my_plugin_nonce'] ), 'my_action' ) ) {
    wp_die( esc_html__( 'Security check failed.', 'my-plugin' ) );
}
$value = sanitize_text_field( wp_unslash( $_POST['field'] ) );
```

**Missing `wp_unslash()` before sanitize:**
```php
// Bad  — sanitize_text_field on slashed data
$val = sanitize_text_field( $_POST['field'] );

// Good
$val = sanitize_text_field( wp_unslash( $_POST['field'] ) );
```

**Unescaped output:**
```php
echo $title;                            // Bad
echo esc_html( $title );               // Good
echo wp_kses_post( $html_content );    // Good for HTML
```

**Yoda conditions:**
```php
if ( $value == true ) {}   // Bad
if ( true == $value ) {}   // Good (Yoda)
if ( $value ) {}           // Also fine
```

**Incorrect hook comment spacing:**
```php
add_action('init', 'my_fn');             // Bad — no spaces inside parens
add_action( 'init', 'my_fn' );          // Good
```

**Misaligned array `=>` / assignment blocks:**
```php
// Bad — WPCS flags Generic.Formatting.MultipleStatementAlignment
$args = array(
    'id' => 1,
    'post_type' => 'post',
);

// Good — double arrows aligned within the block
$args = array(
    'id'        => 1,
    'post_type' => 'post',
);
```
**Always** keep `=>` (and consecutive `=`) aligned within a block — `phpcbf` fixes this automatically. **Never** hand-collapse them to single spaces to "tidy" the code; WPCS just re-flags it.

### 6. GitHub Actions CI

```yaml
# .github/workflows/phpcs.yml
name: PHPCS

on: [push, pull_request]

jobs:
  phpcs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '7.4'
          tools: composer
      - run: composer install --no-interaction --prefer-dist
      - run: vendor/bin/phpcs
```

### 7. IDE integration

**PHPStorm:** Settings → PHP → Quality Tools → PHP_CodeSniffer → set path to `vendor/bin/phpcs`. Enable "Inspections → PHP → PHP Code Sniffer validation".

**VS Code:** Install `shevaua.phpcs` extension. Set `phpcs.executablePath` to `./vendor/bin/phpcs` in workspace settings.

## Notes

- `WordPress-Extra` is a superset of `WordPress-Core`; always use `WordPress-Extra` unless you have a specific reason to be less strict.
- `WordPress-Docs` is separate — it enforces PHPDoc blocks. Include it for WP.org submissions.
- WPCS sniffs for i18n (`WordPress.WP.I18n`) catch missing text domains and non-translatable strings — complement to `wp-plugin-audit` Dimension B.
- WP.org review does **not** run PHPCS automatically, but reviewers check style manually and will reject poorly formatted code. PHPCS passing is a strong signal of submission readiness.
- For WooCommerce extensions, add `WooCommerce-Core` ruleset if available (`woocommerce/woocommerce-sniffs`).

## References

- `references/ci-phpcs.md` — PHPCS in GitHub Actions: minimal workflow, PHP×WP matrix, caching, and failure triage
- `references/phpcs-config-examples.md` — `phpcs.xml.dist` configurations: WP.org-ready minimal, WooCommerce extension, and custom sniff exclusion patterns
- `references/wpcs-sniffs.md` — WordPress Coding Standards sniff reference: ruleset hierarchy, key sniff descriptions, and common `// phpcs:ignore` patterns
