---
name: wp-plugin-testing
description: "Use when writing or setting up tests for a WordPress plugin — PHPUnit integration tests using WP_UnitTestCase with the WP test suite (bin/install-wp-tests.sh, phpunit.xml.dist, tests/bootstrap.php), unit tests with Brain Monkey (when() / expect() / Mockery) or WP_Mock, test factories (factory()->post->create(), ->user->create(), ->term->create()), HTTP request mocking with add_filter pre_http_request, AJAX testing with WP_Ajax_UnitTestCase, redirect/exit testing via exception-throwing pattern, multisite tests (WP_MULTISITE=1), acceptance tests with Codeception + wp-browser, or GitHub Actions CI matrix for PHP x WP versions. Triggers: \"write a test for this\", \"unit test this function\", \"set up PHPUnit for my plugin\", \"mock this WP function\", \"Brain Monkey setup\", \"WP_Mock\", \"test is failing\", \"how do I test a hook\", \"test my REST endpoint\", \"factory()->post->create()\", \"install the WP test suite\", \"test my wp_mail call\", \"integration test setup\", \"bin/install-wp-tests.sh\", \"phpunit.xml.dist\", \"WP_UnitTestCase\", \"WP_Ajax_UnitTestCase\", \"pre_http_request mock\", \"test a redirect\", \"WP_MULTISITE=1 test\", \"Codeception wp-browser\", \"Brain Monkey setUp tearDown\", \"PHP x WP version matrix in CI\", \"test a wp_schedule_event\", \"assert hook was called\". Not for: E2E browser tests — use `wp-admin-browser` for those."
---

# WordPress Plugin Testing

> **Model note:** Bootstrap and CI config setup are mechanical (`haiku`). Writing meaningful test cases (choosing fixtures, mocking the right layer, testing edge cases) requires understanding the plugin's code — use `sonnet`. Redirect/exit harness setup is a one-time pattern and works on `haiku`.

Set up and write automated tests for WordPress plugins: PHPUnit integration tests (real WP + DB), pure unit tests (no WP loaded), and acceptance/E2E tests with Codeception.

## When to use

- "Set up PHPUnit tests for my plugin", "bootstrap a WP test suite", "scaffold plugin tests".
- "Write a unit test for this function", "mock WordPress functions without loading WP".
- "Set up Codeception / wp-browser", "write acceptance tests".
- "Test a hook callback", "assert a filter changes the output", "test AJAX handlers".
- "Add tests to CI", "run tests on GitHub Actions".

**Not for:** PHPStan static analysis — use the official `wp-phpstan` skill. Scaffolding a stubs package for a third-party library — use `wp-phpstan-stubs`. Debugging CI failures on an existing suite — use `wp-ci-qa`.

## Method

### 1. Choose test type

| Type | Tool | WP loaded | DB | Speed |
|---|---|---|---|---|
| Integration | PHPUnit + WP test suite (`WP_UnitTestCase`) | ✅ Full | ✅ Real (temp) | Slow |
| Unit | PHPUnit + Brain\Monkey (recommended) or WP_Mock | ❌ | ❌ | Fast |
| Acceptance | Codeception + wp-browser | ✅ Browser | ✅ Real | Slowest |

Start with integration tests for hooks/filters; unit tests for pure business logic; acceptance only for critical user flows.

### 2. Integration test setup (WP test suite)

**Install test suite:**
```bash
# WP-CLI method (recommended)
wp scaffold plugin-tests my-plugin

# Manual — install WP test library
bash bin/install-wp-tests.sh wordpress_test root '' localhost latest
```

`bin/install-wp-tests.sh` creates a temp WP installation and the `wordpress-tests-lib`. Add `tests/` dir to `.gitignore` if downloading WP inline, or commit the bootstrap only.

**`composer.json` additions:**
```json
{
    "require-dev": {
        "phpunit/phpunit": "^9.0 || ^10.0",
        "yoast/phpunit-polyfills": "^2.0"
    },
    "scripts": {
        "test": "phpunit",
        "test:unit": "phpunit --testsuite=unit",
        "test:integration": "phpunit --testsuite=integration"
    }
}
```

**`phpunit.xml.dist`:**
```xml
<?xml version="1.0"?>
<phpunit bootstrap="tests/bootstrap.php" colors="true">
    <testsuites>
        <testsuite name="integration">
            <directory>tests/integration</directory>
        </testsuite>
        <testsuite name="unit">
            <directory>tests/unit</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

**`tests/bootstrap.php` (integration):**
```php
<?php
$_tests_dir = getenv( 'WP_TESTS_DIR' ) ?: '/tmp/wordpress-tests-lib';
require_once $_tests_dir . '/includes/functions.php';

tests_add_filter( 'muplugins_loaded', function() {
    require dirname( __DIR__ ) . '/my-plugin.php';
} );

require $_tests_dir . '/includes/bootstrap.php';
```

### 3. Write integration tests

Extend `WP_UnitTestCase` (provided by WP test suite). It wraps each test in a DB transaction and rolls back — no teardown needed for posts/users/terms.

```php
class Test_My_Feature extends WP_UnitTestCase {

    public function test_filter_changes_title() {
        $post_id = self::factory()->post->create( [ 'post_title' => 'Original' ] );

        // Activate the plugin feature
        add_filter( 'the_title', 'my_plugin_modify_title', 10, 2 );

        $title = get_the_title( $post_id );

        $this->assertStringContainsString( 'Modified', $title );
    }

    public function test_option_saved_on_activation() {
        do_action( 'activate_my-plugin/my-plugin.php' );

        $this->assertSame( '1.0.0', get_option( 'my_plugin_version' ) );
    }

    public function test_ajax_handler_returns_json() {
        // Simulate AJAX call
        $_POST['_wpnonce'] = wp_create_nonce( 'my_action' );
        $_POST['data']     = 'test';

        try {
            $this->_handleAjax( 'my_plugin_action' );
        } catch ( WPAjaxDieContinueException $e ) {
            // Normal for wp_send_json_success
        }

        $response = json_decode( $this->_last_response, true );
        $this->assertTrue( $response['success'] );
    }
}
```

**Factory helpers:**
```php
$user_id    = self::factory()->user->create( [ 'role' => 'editor' ] );
$term_id    = self::factory()->term->create( [ 'taxonomy' => 'category', 'name' => 'News' ] );
$post_ids   = self::factory()->post->create_many( 5, [ 'post_status' => 'publish' ] );
$attachment = self::factory()->attachment->create_upload_object( '/path/to/image.jpg' );
```

### 4. Unit tests with Brain\Monkey (or WP_Mock)

For pure functions that don't need a real WP environment. **Brain\Monkey** is the recommended choice — it includes Mockery, has first-class `stubEscapeFunctions()` / `stubTranslationFunctions()` helpers, and richer hook assertion API. WP_Mock (10up) is a lighter alternative.

```bash
# Brain\Monkey (recommended)
composer require --dev brain/monkey mockery/mockery yoast/phpunit-polyfills

# WP_Mock (alternative)
composer require --dev 10up/wp_mock
```

See `references/brain-monkey-patterns.md` for the full base-class pattern (including `ReflectsObjects` for testing private/protected members) that matches real-world complex plugin structures.

**`tests/bootstrap-unit.php`:**
```php
<?php
WP_Mock::bootstrap();
require dirname( __DIR__ ) . '/includes/functions.php'; // file under test
```

**Test:**
```php
use WP_Mock\Tools\TestCase;

class Test_Pure_Function extends TestCase {

    public function setUp(): void {
        parent::setUp();
        WP_Mock::setUp();
    }

    public function tearDown(): void {
        WP_Mock::tearDown();
        parent::tearDown();
    }

    public function test_get_plugin_option_returns_default() {
        WP_Mock::userFunction( 'get_option' )
            ->with( 'my_plugin_setting', 'default_value' )
            ->andReturn( 'default_value' );

        $result = my_plugin_get_setting();

        $this->assertSame( 'default_value', $result );
        WP_Mock::assertActionsCalled();
    }

    public function test_action_fires_on_save() {
        WP_Mock::expectAction( 'my_plugin_after_save', 42 );
        WP_Mock::userFunction( 'update_option' )->andReturn( true );

        my_plugin_save_data( 42 );
    }
}
```

### 5. HTTP request mocking

Intercept `wp_remote_get/post` in integration tests:

```php
// In setUp or individual test
add_filter( 'pre_http_request', function( $preempt, $args, $url ) {
    if ( str_contains( $url, 'api.example.com' ) ) {
        return [
            'response' => [ 'code' => 200, 'message' => 'OK' ],
            'body'     => wp_json_encode( [ 'status' => 'ok', 'data' => [] ] ),
            'headers'  => [],
            'cookies'  => [],
        ];
    }
    return $preempt;
}, 10, 3 );
```

### 6. Multisite tests

```php
class Test_Network_Feature extends WP_UnitTestCase {

    public static function setUpBeforeClass(): void {
        parent::setUpBeforeClass();
        if ( ! is_multisite() ) {
            self::markTestSkipped( 'Multisite required.' );
        }
    }

    public function test_option_per_site() {
        $site_id = self::factory()->blog->create();

        switch_to_blog( $site_id );
        update_option( 'my_plugin_setting', 'site-value' );
        restore_current_blog();

        switch_to_blog( $site_id );
        $value = get_option( 'my_plugin_setting' );
        restore_current_blog();

        $this->assertSame( 'site-value', $value );
    }
}
```

Run multisite tests: `WP_MULTISITE=1 vendor/bin/phpunit`

### 7. Testing redirect + exit paths

Production code commonly ends with:

```php
wp_safe_redirect( $url );
exit;
```

`add_filter( 'wp_redirect', '__return_false' )` stops the header but **not** `exit` — the PHP process dies, PHPUnit prints no summary, and all subsequent tests never run.

**Fix: throw from the filter to unwind the stack before `exit` is reached.**

```php
// tests/Support/Redirect.php — own PSR-4 file so every test class can catch it
namespace MyPlugin\Test;
class Redirect extends \Exception {
    public string $location;
    public function __construct( string $location ) {
        parent::__construct( 'redirect' );
        $this->location = $location;
    }
}
```

```php
class Test_With_Redirect extends WP_UnitTestCase {

    private $redirect_filter;

    public function setUp(): void {
        parent::setUp();
        // Whitelist external hosts exactly as production does
        add_filter( 'allowed_redirect_hosts', fn( $h ) => array_merge( $h, [ 'dashboard.example.com' ] ) );
        $this->redirect_filter = static fn( $loc ) => throw new \MyPlugin\Test\Redirect( $loc );
        add_filter( 'wp_redirect', $this->redirect_filter );
    }

    public function tearDown(): void {
        remove_filter( 'wp_redirect', $this->redirect_filter );
        parent::tearDown();
    }

    private function run(): ?string {
        try {
            my_plugin_do_thing_that_may_redirect();
        } catch ( \MyPlugin\Test\Redirect $e ) {
            return $e->location;
        }
        return null;
    }

    public function test_redirects_on_success(): void {
        $location = $this->run();
        $this->assertSame( 'https://dashboard.example.com/', $location );
        $this->assertSame( $user_id, get_current_user_id() ); // side effects before exit
    }

    public function test_no_redirect_on_error(): void {
        $this->assertNull( $this->run() );
    }
}
```

Copy-paste harness: `references/example-test.php`. AJAX / REST / `wp_die()` patterns: `references/redirect-assertions.md`.

### 8. GitHub Actions CI

```yaml
# .github/workflows/phpunit.yml
name: PHPUnit

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: wordpress_test
        options: --health-cmd="mysqladmin ping" --health-interval=10s

    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.1'
          extensions: mysqli
          tools: composer, wp-cli

      - run: composer install --no-interaction --prefer-dist

      - name: Install WP test suite
        run: bash bin/install-wp-tests.sh wordpress_test root root 127.0.0.1 latest

      - run: vendor/bin/phpunit --testsuite=integration
      - run: vendor/bin/phpunit --testsuite=unit
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Listing a file containing `defined('ABSPATH') \|\| exit` in Composer `files` autoload | **Never** put WP-guarded files in `files` autoload — Composer loads them before WP bootstraps, silently killing PHPUnit with no output. Use `--prepend` to define `ABSPATH` first (add to `composer.json` test script: `vendor/bin/phpunit --prepend tests/php/prepend.php`), or remove from `files` and require explicitly in the plugin's main file after the ABSPATH guard |

## Notes

- `WP_UnitTestCase` rolls back DB after each test — use `self::factory()`, not raw `wp_insert_post()`, so rollback is tracked.
- Integration tests require a real MySQL database; they're slow in CI. Separate unit and integration into distinct test suites and run unit suite on every push, integration suite on PRs only.
- For WooCommerce plugin tests, include WC's test helpers: `require WC_ABSPATH . 'tests/legacy/includes/wc-helper-product.php'`.
- Codeception + wp-browser is the recommended path for acceptance tests; see `https://wpbrowser.wptestkit.dev` for full docs.
- `references/redirect-assertions.md` covers AJAX (`WP_Ajax_UnitTestCase`), REST, and `wp_die()` assertion patterns. `references/phpunit-bootstrap.md` has the full bootstrap + CI setup.

## References

- `references/brain-monkey-patterns.md` — Brain\Monkey unit testing patterns: `when()`, `expect()`, Mockery integration, and WP function stubs without loading WordPress
- `references/example-test.php` — Complete copy-paste-ready test harness for code that uses `wp_redirect()`, `wp_die()`, and WP AJAX — includes bootstrap and assertion setup
- `references/factory-methods.md` — `WP_UnitTest_Factory` methods: post, user, term, comment, attachment, and network sub-factories with rollback behaviour
- `references/phpunit-bootstrap.md` — Full PHPUnit bootstrap setup: `install-wp-tests.sh`, suite configuration, CI matrix, and test runner commands
- `references/redirect-assertions.md` — Redirect assertion patterns: `WP_Ajax_UnitTestCase`, REST response assertions, `wp_die()` capture, and status-code testing
- `references/test-patterns.md` — WordPress plugin test patterns: hook/filter tests, option tests, shortcode tests, and cron scheduling assertions
- `references/wp-mock-patterns.md` — WP_Mock unit testing patterns: mock setup, teardown, function expectations, filter/action mocking, and test isolation
