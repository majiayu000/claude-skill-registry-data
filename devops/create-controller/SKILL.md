---
description: Scaffold a controller with its FormRequest, route, and feature test
argument-hint: "<Module>/<Name>"
disable-model-invocation: true
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash(vendor/bin/phpunit *), Bash(composer *), Bash(php artisan route:list *)"
---

# New Controller

Create the controller named in `$ARGUMENTS` (e.g. `Chat/DeleteChat`, `Payment/Invoice`).

Read `modules/Chat/Infrastructure/Http/Controller/ChatController.php` and its request class first, and mirror them.

## Files

```
modules/<Module>/Infrastructure/Http/Request/<Name>Request.php
modules/<Module>/Infrastructure/Http/Controller/<Name>Controller.php
routes/<file>.php                                      # route entry
tests/Feature/<Module>/<Name>ControllerTest.php
```

## FormRequest — all validation lives here

```php
<?php

declare(strict_types=1);

namespace Modules\<Module>\Infrastructure\Http\Request;

use Illuminate\Foundation\Http\FormRequest;
use Override;

final class <Name>Request extends FormRequest
{
    /** @return array<string, mixed> */
    #[Override]
    public function rules(): array
    {
        return [
            // 'txid' => ['required', 'string', 'size:64'],
        ];
    }
}
```

Never validate inline in the controller.

## Controller — three lines of responsibility

```php
<?php

declare(strict_types=1);

namespace Modules\<Module>\Infrastructure\Http\Controller;

use Modules\<Module>\Domain\<Name>ActionInterface;

final readonly class <Name>Controller
{
    public function __construct(
        private <Name>ActionInterface $action,
    ) {
    }

    public function __invoke(<Name>Request $request): RedirectResponse
    {
        $result = $this->action->execute(
            new <Name>Transfer(...$request->validated()),
        );

        return redirect()->route('...');
    }
}
```

A controller may only: accept a validated request → call an Action or Facade → return a response or view. Anything else belongs in `Application/`.

## Route

Add it under `routes/`, wired by `modules/Shared/RouteServiceProvider.php`. Controller mappings only — no closures, no inline logic:

```php
Route::post('/chat/{chat}/delete', DeleteChatController::class)->name('chat.delete');
```

Verify:

```bash
php artisan route:list --path=<segment>
```

## Feature test

Controllers need the framework, so the test goes in `tests/Feature/`:

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

final class <Name>ControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_post_with_valid_input_redirects(): void { /* … */ }

    public function test_post_with_invalid_input_returns_validation_error(): void { /* … */ }

    public function test_post_without_auth_is_rejected(): void { /* … */ }
}
```

Cover the happy path, the validation failure, and the auth boundary.

## Constraints

- No Eloquent, no `DB::`, no business conditionals in the controller — the pre-write hook blocks these
- Inject Action or Facade **interfaces**, never concrete classes
- Rate-limited or auth'd routes get the middleware from `modules/Shared/`
- Never register the controller manually — the container resolves it

## Gate

```bash
composer test
```
