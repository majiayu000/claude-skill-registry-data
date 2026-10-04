---
name: plugin-test
description: Writes PHPUnit tests in `tests/` using the stub pattern from `tests/bootstrap.php`. Use when user says 'add test', 'test this function', 'write phpunit', 'cover this', or modifies `src/Plugin.php` or `src/parallels.inc.php`. Covers Plugin static properties/hooks via ReflectionClass and inc function signatures via ReflectionFunction. Do NOT use for integration tests that call live KA API or external services. For a plugin's contract or behavioral tests (tests/ContractTest.php, the shared harness, composer myadmin:scaffold-tests) use the plugin-contract-tests skill instead — this skill's reflection-only guidance predates that harness.
---
<!-- myadmin-contract-harness-notice -->
> ### ⚠️ Read this before the rest of the file
>
> This package is on the **shared plugin contract harness**. Parts of the guidance below
> predate it and are now wrong in one specific way:
>
> **Any instruction here that a plugin's `getHooks()` / `getSettings()` / `getActivate()` /
> `getDeactivate()` / `getQueue()` must not be *called* — that only its existence, visibility
> or parameter count may be checked through `ReflectionClass` — no longer applies.** That rule
> existed because those methods reference bare constants (`PRORATE_BILLING` and friends) that
> only a live MyAdmin request defines, so calling them from a test used to fatal. The harness
> defines them first. It then executes the handlers for real, in a process of its own.
>
> A reflection-only assertion passes whether or not the thing works: `getActivate()` can exist,
> be public, be static, take one argument, and still fatal the moment it runs. Three real
> production bugs in this fleet were sitting behind assertions of exactly that shape.
>
> **Use the `plugin-contract-tests` skill** for anything touching `tests/ContractTest.php`,
> the contract inspectors, or `composer myadmin:scaffold-tests`.
>
> **Everything else in this file is still accurate and still applies** — this package's own
> classes, its API wrappers, its fixtures, its bootstrap, and the reasons certain classes must
> not be constructed. Nothing below has been removed.

# plugin-test

## Critical

- **Never call live KA API** — all tests must run without network access. Use Reflection to inspect signatures; do not instantiate `\Detain\Parallels\Parallels` in tests.
- **Always guard new global stubs** with `if (!function_exists(...))` in `tests/bootstrap.php` — the bootstrap runs once for the whole suite.
- Test files go in `tests/`, namespace `Detain\MyAdminParallels\Tests`, extend `PHPUnit\Framework\TestCase`, use `declare(strict_types=1)`.
- Run `composer test` to verify before considering a task done.

## Instructions

1. **Identify what needs covering.** For `src/Plugin.php` → create or update `tests/PluginTest.php`. For `src/parallels.inc.php` → create or update `tests/ParallelsIncTest.php`.

2. **Check `tests/bootstrap.php` for missing stubs.** Open `src/` file being tested and list every bare function call that is a MyAdmin global (`myadmin_log`, `get_service_define`, `function_requirements`, `request_log`, `get_module_settings`, etc.). For each one not already stubbed, add to `tests/bootstrap.php`:
   ```php
   if (!function_exists('new_global_fn')) {
       function new_global_fn(): void {}
   }
   ```
   Verify stub was added before writing tests that depend on it.

3. **Write Plugin tests** (`tests/PluginTest.php`). Use `ReflectionClass` — never mock `Plugin`. Required test groups:
   - Static properties (`$name`, `$description`, `$module`, `$type`, `$help`) — assert type string and expected values.
   - `getHooks()` returns array with keys prefixed by `Plugin::$module . '.'` plus `'function.requirements'`.
   - Each hook value is `[Plugin::class, 'methodName']` (2-element array).
   - Each referenced method exists, is `public` and `static`, accepts exactly one `GenericEvent` parameter.
   - Handler aliases are identical: `licenses.activate === licenses.reactivate`, `licenses.deactivate === licenses.deactivate_ip`.

   ```php
   use Detain\MyAdminParallels\Plugin;
   use PHPUnit\Framework\TestCase;
   use ReflectionClass;
   use Symfony\Component\EventDispatcher\GenericEvent;

   class PluginTest extends TestCase {
       public function testModuleProperty(): void {
           $this->assertSame('licenses', Plugin::$module);
       }
       public function testHookMethodsArePublicAndStatic(): void {
           $hooks = Plugin::getHooks();
           $rc = new ReflectionClass(Plugin::class);
           foreach ($hooks as [$class, $method]) {
               $m = $rc->getMethod($method);
               $this->assertTrue($m->isPublic());
               $this->assertTrue($m->isStatic());
           }
       }
   }
   ```

4. **Write inc function tests** (`tests/ParallelsIncTest.php`). Load the file once in `setUpBeforeClass()`, then use `ReflectionFunction` for all assertions — do not call the functions.

   ```php
   public static function setUpBeforeClass(): void {
       if (!function_exists('activate_parallels')) {
           require_once dirname(__DIR__) . '/src/parallels.inc.php';
       }
   }

   public function testActivateParallelsSignature(): void {
       $ref = new \ReflectionFunction('activate_parallels');
       $params = $ref->getParameters();
       $this->assertCount(3, $params);
       $this->assertSame('ipAddress', $params[0]->getName());
       $this->assertSame('type',      $params[1]->getName());
       $this->assertSame('addons',    $params[2]->getName());
       $this->assertTrue($params[2]->isDefaultValueAvailable());
       $this->assertSame('', $params[2]->getDefaultValue());
       $this->assertSame(2, $ref->getNumberOfRequiredParameters());
   }
   ```

   Standard assertions for every new inc function: `function_exists`, parameter count, parameter names, required parameter count, `hasReturnType() === false` (inc functions are untyped legacy style).

5. **Run and verify:**
   ```bash
   composer test
   ```
   All tests must pass with no errors or warnings before finishing.

## Examples

**User says:** "Add tests for a new `reactivate_parallels($ipAddress, $key)` function I just added to `src/parallels.inc.php`"

**Actions taken:**
1. Check `tests/bootstrap.php` — `myadmin_log` and `request_log` already stubbed. No new globals needed.
2. In `tests/ParallelsIncTest.php`, add inside `ParallelsIncTest`:
   ```php
   public function testReactivateParallelsFunctionExists(): void {
       $this->assertTrue(function_exists('reactivate_parallels'));
   }
   public function testReactivateParallelsSignature(): void {
       $ref = new \ReflectionFunction('reactivate_parallels');
       $params = $ref->getParameters();
       $this->assertCount(2, $params);
       $this->assertSame('ipAddress', $params[0]->getName());
       $this->assertSame('key',       $params[1]->getName());
       $this->assertSame(2, $ref->getNumberOfRequiredParameters());
       $this->assertFalse($ref->hasReturnType());
   }
   ```
3. Run `composer test` — passes.

**Result:** Two new tests in `tests/ParallelsIncTest.php` verifying existence and signature without touching the KA API.

## Common Issues

- **"Call to undefined function myadmin_log()"** — the src file calls a global not stubbed yet. Add `if (!function_exists('myadmin_log')) { function myadmin_log(): void {} }` to `tests/bootstrap.php`.
- **"Cannot find autoloader"** — bootstrap tries two paths (`__DIR__.'/../vendor/autoload.php'` then `__DIR__.'/../../../../vendor/autoload.php'`). Run `composer install` from the plugin root so `vendor/autoload.php` exists.
- **"Class Symfony\\Component\\EventDispatcher\\GenericEvent not found"** — run `composer install`; it's pulled in via `symfony/event-dispatcher`.
- **ReflectionFunction throws "Function activate_parallels() does not exist"** — the `setUpBeforeClass` guard `if (!function_exists(...))` skipped the `require_once`. Either the function was never added to the file, or a typo in the function name. Grep: `grep -n 'function activate_parallels' src/parallels.inc.php`.
- **Tests pass locally but fail in CI** — CI may not have the inner `vendor/` path. Confirm `phpunit.xml.dist` `bootstrap` attribute points to `tests/bootstrap.php` and that `composer install` runs before the test step.
