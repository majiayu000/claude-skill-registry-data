---
name: plugin-hook
description: Adds a new event hook to src/Plugin.php — registers in getHooks() and creates the static GenericEvent handler. Use when user says 'add hook', 'handle event', 'new plugin event', or adds a lifecycle action (activate/deactivate/change IP/reactivate). Do NOT use for modifying existing handlers or adding inc functions.
---
# plugin-hook

## Critical

- All handler methods MUST be `public static` and accept exactly one `GenericEvent $event` parameter — `testHookMethodsArePublicAndStatic` and `testEventHandlerMethodSignatures` will fail otherwise.
- Always guard the handler body with `if ($event['category'] == get_service_define('PARALLELS'))` before any logic.
- Always call `$event->stopPropagation()` as the last statement inside the category guard.
- Hook keys use `self::$module . '.event_name'` (e.g. `'licenses.change_ip'`) — never hardcode the module string.
- The one exception is `'function.requirements'` which uses a literal key, not the module prefix.
- Run `composer test` after every change — a missing method or wrong signature will break `testAllHookMethodsExist` and `testClassMethodCount`.

## Instructions

1. **Decide the event name and handler name.** Event name is snake_case (e.g. `change_ip`). Handler is PascalCase prefixed with `get` (e.g. `getChangeIp`). Verify no existing entry in `getHooks()` already covers this event.

2. **Register the hook in `getHooks()` inside `src/Plugin.php`.**
   Add one line to the returned array:
   ```php
   self::$module.'.change_ip' => [__CLASS__, 'getChangeIp'],
   ```
   If the new event should share an existing handler (like `reactivate` → `getActivate`), point to the existing method name instead of creating a new one. Verify the array key is unique before proceeding.

3. **Add the handler method to `src/Plugin.php`** after the last existing handler, before the closing `}`:
   ```php
   /**
    * @param \Symfony\Component\EventDispatcher\GenericEvent $event
    */
   public static function getChangeIp(GenericEvent $event)
   {
       if ($event['category'] == get_service_define('PARALLELS')) {
           $serviceClass = $event->getSubject();
           myadmin_log(self::$module, 'info', 'Parallels <Action Description>', __LINE__, __FILE__, self::$module, $serviceClass->getId());
           // ... call function_requirements() then the inc function ...
           $event->stopPropagation();
       }
   }
   ```
   The `use Symfony\Component\EventDispatcher\GenericEvent;` import is already present at the top — do not add it again.

4. **If the handler calls an inc function**, add `function_requirements('your_function')` before the call and register the function path in `getRequirements()`:
   ```php
   $loader->add_requirement('your_function', '/../src/parallels.inc.php');
   ```
   Verify the function exists in `src/parallels.inc.php` before registering.

5. **Update `tests/PluginTest.php`** — add the new hook key to the `$expectedKeys` array in `testGetHooksContainsExpectedKeys()` and bump the count in `testClassMethodCount()` if a new method was added. Run `composer test` to confirm all tests pass.

## Examples

**User says:** "Add a hook for `licenses.change_ip` that logs the old and new IP"

**Actions taken:**

`getHooks()` addition in `src/Plugin.php`:
```php
self::$module.'.change_ip' => [__CLASS__, 'getChangeIp'],
```

New handler method in `src/Plugin.php`:
```php
public static function getChangeIp(GenericEvent $event)
{
    if ($event['category'] == get_service_define('PARALLELS')) {
        $serviceClass = $event->getSubject();
        myadmin_log(self::$module, 'info', 'IP Change - (OLD:'.$serviceClass->getIp().") (NEW:{$event['newip']})", __LINE__, __FILE__, self::$module, $serviceClass->getId());
        // perform IP change logic here
        $event['status'] = 'ok';
        $event['status_text'] = 'The IP Address has been changed.';
        $event->stopPropagation();
    }
}
```

**Result:** `composer test` passes; `testGetHooksContainsExpectedKeys` and `testAllHookMethodsExist` both green.

## Common Issues

- **`testClassMethodCount` fails with "Expected 7, got 8"**: You added a new handler but did not update the count assertion in `tests/PluginTest.php`. Change the `assertCount(7, ...)` to the new total.
- **`testAllHookMethodsExist` fails**: The method name string in `getHooks()` does not exactly match the declared method name. Check spelling and PascalCase — `getChangeIp` ≠ `getChangeIP`.
- **`testEventHandlerMethodSignatures` fails with "parameter should be GenericEvent"**: The handler is missing the `GenericEvent $event` type hint, or the `use` statement is absent (it lives at the top of `src/Plugin.php` — do not remove it).
- **`stopPropagation` not called**: Event will continue dispatching to other plugins and produce duplicate side-effects. Always place `$event->stopPropagation()` as the final statement inside the category guard.
- **`function_requirements` not registered**: If `activate_parallels` or a new inc function is called but not registered in `getRequirements()`, it will throw a fatal error at runtime. Verify `$loader->add_requirement('fn_name', '...')` is present.
