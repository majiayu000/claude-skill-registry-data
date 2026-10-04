---
name: inc-function
description: Adds a new procedural function to `src/parallels.inc.php` wrapping a `\Detain\Parallels\Parallels` KA API method with the standard `myadmin_log` + `request_log` + try/catch pattern. Use when user says 'add function', 'new API call', 'call parallels method', or needs to expose a KA API method. Do NOT use for Plugin.php static event handlers or bin/ scripts. For a plugin's contract or behavioral tests (tests/ContractTest.php, the shared harness, composer myadmin:scaffold-tests) use the plugin-contract-tests skill instead — this skill's reflection-only guidance predates that harness.
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

# inc-function

## Critical

- **No type hints on parameters, no return type declarations** — existing functions are untyped legacy PHP style; `ReflectionFunction` tests enforce this.
- **No PHP namespace declaration** in `src/parallels.inc.php` — it is a plain procedural include file.
- **Always catch `\XML_RPC2_CurlException`** (not `\Exception`) and return `false` on failure — this is the only exception the KA API client throws.
- **Always call `request_log()`** for both success and failure paths with identical `'licenses'` module and `'parallels'` service arguments.
- The `use \Detain\Parallels\Parallels;` statement already exists at the top of the file — do not add a second one.

## Instructions

1. **Identify the KA API method** to wrap. Check `\Detain\Parallels\Parallels` for the exact method name and signature (e.g., `getKeyInfo($keyNumber)`, `retrieveKey($keyNumber)`, `getAvailableUpgrades($keyNumber)`).

2. **Add the PHPDoc block** immediately before the function:
   ```php
   /**
    * parallels_<action>()
    * @param mixed $param1
    * @return mixed
    */
   ```
   Use `@param mixed` — no concrete types. Verify the block is present before proceeding.

3. **Write the function signature** — no type hints, no return type:
   ```php
   function parallels_<action>($param1)
   ```
   Name must be `parallels_` prefixed + snake_case action (e.g., `parallels_get_key_info`).

4. **Open with `myadmin_log`** describing the call:
   ```php
   myadmin_log('licenses', 'info', "Parallels <Action> ({$param1})", __LINE__, __FILE__);
   ```

5. **Instantiate the client and build `$request`:**
   ```php
   $parallels = new \Detain\Parallels\Parallels();
   $request = [$param1];   // mirror the args passed to the API method
   ```

6. **Wrap the API call in try/catch:**
   ```php
   try {
       $response = $parallels->apiMethodName($param1);
       request_log('licenses', false, __FUNCTION__, 'parallels', 'apiMethodName', $request, $response);
       myadmin_log('licenses', 'info', "parallels_<action>({$param1}) Response: ".json_encode($response), __LINE__, __FILE__);
   } catch (\XML_RPC2_CurlException $e) {
       request_log('licenses', false, __FUNCTION__, 'parallels', 'apiMethodName', $request, $e->getMessage());
       return false;
   }
   return $response;
   ```
   Verify `request_log()` is called in **both** the try and catch blocks before proceeding.

7. **Register the function in `tests/bootstrap.php`** only if the function calls any new MyAdmin globals not already stubbed. Check existing stubs: `myadmin_log`, `get_service_define`, `function_requirements`, `request_log`, `get_module_settings`.

8. **Add a test** in `tests/ParallelsIncTest.php` following the existing `testActivateParallelsFunctionExists` pattern — at minimum assert `function_exists('parallels_<action>')`.

9. **Run tests** to confirm nothing broke:
   ```bash
   vendor/bin/phpunit tests/ParallelsIncTest.php
   ```

## Examples

**User says:** "Add a function that calls `getKeyInfo` on a key number"

**Actions taken:**
1. Confirm `\Detain\Parallels\Parallels::getKeyInfo($keyNumber)` exists in the client.
2. Append to `src/parallels.inc.php`:

```php
/**
 * parallels_get_key_info()
 * @param mixed $keyNumber
 * @return mixed
 */
function parallels_get_key_info($keyNumber)
{
    myadmin_log('licenses', 'info', "Parallels Get Key Info ({$keyNumber})", __LINE__, __FILE__);
    $parallels = new \Detain\Parallels\Parallels();
    $request = [$keyNumber];
    try {
        $response = $parallels->getKeyInfo($keyNumber);
        request_log('licenses', false, __FUNCTION__, 'parallels', 'getKeyInfo', $request, $response);
        myadmin_log('licenses', 'info', "parallels_get_key_info({$keyNumber}) Response: ".json_encode($response), __LINE__, __FILE__);
    } catch (\XML_RPC2_CurlException $e) {
        request_log('licenses', false, __FUNCTION__, 'parallels', 'getKeyInfo', $request, $e->getMessage());
        return false;
    }
    return $response;
}
```

3. Add `testParallelsGetKeyInfoFunctionExists` to `tests/ParallelsIncTest.php`.
4. Run `vendor/bin/phpunit tests/ParallelsIncTest.php` — all green.

**Result:** New function appears in `src/parallels.inc.php`, test passes.

## Common Issues

- **`Call to undefined function myadmin_log()`** during tests: add `function myadmin_log() {}` stub to `tests/bootstrap.php` — it must be defined before `require_once` of the inc file.
- **`Call to undefined function request_log()`** during tests: same fix — add `function request_log() {}` to `tests/bootstrap.php`.
- **`Class 'XML_RPC2_CurlException' not found`** at runtime: the class lives in the `detain/parallels-licensing` package; run `composer install` to ensure it is present.
- **Test fails with `Function parallels_<action>() should be defined`**: the function name in the `function_exists()` assertion must exactly match the PHP function name including the `parallels_` prefix.
- **Duplicate `use` statement error**: `use \Detain\Parallels\Parallels;` is already at line 10 of `src/parallels.inc.php`; never add it again.