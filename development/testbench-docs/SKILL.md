---
name: testbench-package-testing
description: "Develops and tests Laravel packages using Orchestra Testbench. Activates when writing package tests, configuring testbench.yaml, managing migrations, defining routes/environment for tests, using Testbench Dusk for browser tests, or working with Workbench for package preview."
license: MIT
metadata:
    author: coderstm
applyTo:
    - "tests/**/*.php"
    - "testbench.yaml"
    - "phpunit.xml*"
    - "workbench/**/*"
---

# Testbench Documentation Skill

## Purpose

This skill provides comprehensive knowledge of **Orchestra Testbench** — the standard tool for testing, developing, and previewing Laravel packages. It covers Testbench, Testbench Dusk, and Workbench components.

## Key Components

- **Testbench** — Write feature/integration tests for Laravel packages by extending `Orchestra\Testbench\TestCase`
- **Testbench Dusk** — Browser-based testing via `Orchestra\Testbench\Dusk\TestCase`
- **Workbench** — Preview and interact with packages during development via `serve` command
- **CLI** — `vendor/bin/testbench` provides artisan-like commands for the stub Laravel skeleton

## Quick Reference

### Installation

```bash
composer require --dev "orchestra/testbench"        # Testbench
composer require --dev "orchestra/testbench-dusk"   # Dusk support
vendor/bin/testbench workbench:install              # Scaffold package
```

### Testbench YAML Configuration

| Key             | Type     | Description                                                                                     |
| --------------- | -------- | ----------------------------------------------------------------------------------------------- |
| `laravel`       | `string` | Path to Laravel skeleton                                                                        |
| `providers`     | `array`  | Service providers to load                                                                       |
| `migrations`    | `array`  | Migration paths                                                                                 |
| `seeders`       | `array`  | Seeder classes                                                                                  |
| `dont-discover` | `array`  | Packages to ignore                                                                              |
| `bootstrappers` | `array`  | Bootstrapper classes                                                                            |
| `env`           | `array`  | CLI environment variables                                                                       |
| `purge`         | `array`  | Files/directories to prune                                                                      |
| `workbench`     | `object` | Workbench settings (welcome, install, start, user, auth, guard, sync, build, assets, discovers) |

### Base TestCase Setup

```php
class TestCase extends \Orchestra\Testbench\TestCase
{
    use Orchestra\Testbench\Concerns\WithWorkbench;
}
```

### Key TestCase Methods

| Method                                  | Purpose                      |
| --------------------------------------- | ---------------------------- |
| `getPackageProviders($app)`             | Register service providers   |
| `getPackageAliases($app)`               | Register facades             |
| `defineEnvironment($app)`               | Set config/env before boot   |
| `defineRoutes($router)`                 | Define routes early          |
| `defineDatabaseMigrations()`            | Configure DB migrations      |
| `applicationBasePath()`                 | Custom Laravel skeleton path |
| `ignorePackageDiscoveriesFrom()`        | Exclude package discovery    |
| `resolveApplicationConsoleKernel($app)` | Swap console kernel          |
| `resolveApplicationHttpKernel($app)`    | Swap HTTP kernel             |

### Database Testing

```php
// In-memory SQLite
#[WithEnv('DB_CONNECTION', 'testing')]
// or in phpunit.xml:
<env name="DB_CONNECTION" value="testing"/>

// RefreshDatabase — runs package migrations only
use Illuminate\Foundation\Testing\RefreshDatabase;

// Run Laravel default migrations
#[WithMigration]
#[WithMigration('laravel', 'cache', 'queue')] // specific tables

// Custom migrations from workbench
use function Orchestra\Testbench\workbench_path;
$this->loadMigrationsFrom(workbench_path('database/migrations'));
```

### Route Testing

```php
// Inline route definition
protected function defineRoutes($router)
{
    $router->get('hello', fn () => 'Hello World');
}

// Per-test route via attribute
#[DefineRoute('usesAuthRoutes')]
public function it_loads_auth_routes() { }

// Per-test via annotation (deprecated)
/** @define-route usesAuthRoutes */
```

### Environment Overrides

```php
// In phpunit.xml
<env name="APP_KEY" value="AckfSECXIvnK5r28GVIWUAxmbBSjTsmF"/>

// In TestCase
protected $loadEnvironmentVariables = false;

// Per-test via attribute
#[DefineEnvironment('usesMySqlConnection')]

// Via config repository
protected function defineEnvironment($app)
{
    $app['config']->set('database.default', 'testing');
}
```

### CLI Commands

```bash
vendor/bin/testbench migrate                  # Run migrations
vendor/bin/testbench package:create-sqlite-db # Create SQLite DB
vendor/bin/testbench package:drop-sqlite-db   # Drop SQLite DB
vendor/bin/testbench package:purge-skeleton   # Reset skeleton
vendor/bin/testbench package:test             # Run tests (with Collision)
vendor/bin/testbench package:test --parallel  # Parallel testing
vendor/bin/testbench workbench:install        # Scaffold workbench
vendor/bin/testbench serve                    # Preview package
composer run serve                            # Workbench serve alias
```

### Testbench Dusk

```php
class DuskTestCase extends \Orchestra\Testbench\Dusk\TestCase
{
    use WithWorkbench;

    protected static $baseServeHost = '127.0.0.1';
    protected static $baseServePort = 9000;
}

// With/without UI
use Orchestra\Testbench\Dusk\Options;
Options::withUI();
Options::withoutUI();

// Per-test app config changes
$this->beforeServingApplication(function ($app, $config) {
    $config->set('mail.default', 'log');
});
```

## Version Compatibility

| Laravel | Testbench | Testbench Dusk | Workbench |
| ------- | --------- | -------------- | --------- |
| 8.x     | 6.x       | 6.x            | —         |
| 9.x     | 7.x       | 7.x            | 7.x       |
| 10.x    | 8.x       | 8.x            | 8.x       |
| 11.x    | 9.x       | 9.x            | 9.x       |
| 12.x    | 10.x      | 10.x           | 10.x      |

## Common Pitfalls

- **DB_CONNECTION** — Use `testing` for in-memory SQLite (declares `sqlite` driver with `:memory:`)
- **APP_KEY** — Required if app uses encryption; set in `phpunit.xml`
- **Dusk + Testbench in same suite** — Override `applicationBasePath()` to use Dusk's skeleton for all test classes
- **ChromeDriver errors** — Run `vendor/bin/dusk-updater update`
- **Legacy factories** — Require `laravel/legacy-factories` when supporting Laravel < 8
- **No auto-discovery by default** — Use `$enablesPackageDiscoveries = true` or explicit providers

## Related Files

- **Config** — `testbench.yaml`
- **Test Base** — `tests/TestCase.php`
- **Workbench** — `workbench/` directory (app, routes, database, config)
- **Docs** — `.agent/skills/testbench-docs/`
