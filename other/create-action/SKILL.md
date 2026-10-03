---
description: Scaffold a new Action (use case) test-first, with interface, test, implementation, and binding
argument-hint: "<Module>/<ActionName>"
disable-model-invocation: true
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash(vendor/bin/phpunit *), Bash(composer *)"
---

# New Action

Create the use case in `$ARGUMENTS` (e.g. `Chat/DeleteChat`). Validate the module exists; ask if the argument is missing.

Conventions live in `.claude/rules/php.md` (style, DTO naming) and `.claude/rules/testing.md` (mocking, suites). Read `modules/Chat/Application/CreateChatAction.php` and mirror it.

## Order — test before implementation

```
1. modules/<Module>/Domain/<Name>ActionInterface.php     # contract
2. tests/Unit/<Module>/<Name>ActionTest.php              # failing test
3. modules/<Module>/Application/<Name>Action.php         # minimal impl
4. modules/<Module>/<Module>ServiceProvider.php          # $singletons binding
```

## 1. Interface

```php
namespace Modules\<Module>\Domain;

interface <Name>ActionInterface
{
    public function execute(<Name>Transfer $transfer): <Name>Result;
}
```

Input DTO → `Transfer`. Output DTO → `Result`. Both in `Domain/Data/`.

## 2. Test (RED)

```php
public function test_execute_with_valid_input_returns_result(): void
{
    $repository = mock(<X>RepositoryInterface::class);
    $repository->shouldReceive('save')->once()->andReturn($entity);

    $result = (new <Name>Action($repository))->execute(new <Name>Transfer(/* … */));

    self::assertSame($entity, $result->entity);
}
```

```bash
vendor/bin/phpunit tests/Unit/<Module>/<Name>ActionTest.php
```

Confirm it fails for the right reason before writing any implementation.

## 3. Implementation (GREEN)

```php
namespace Modules\<Module>\Application;

final readonly class <Name>Action implements <Name>ActionInterface
{
    public function __construct(
        private <X>RepositoryInterface $repository,
    ) {
    }

    public function execute(<Name>Transfer $transfer): <Name>Result
    {
        // minimal code to pass the test
    }
}
```

## 4. Binding — forget this and it fails at runtime, not in phpstan

```php
<Name>ActionInterface::class => <Name>Action::class,
```

## 5. Gate

```bash
composer test
```

## Specific to Actions

- One public method: `execute()`. Name is verb + noun (`CreateChat`), never `ChatManager`
- No Eloquent here — inject a repository interface. The `pre-write` hook blocks it in new files
- Cross-module needs go through the other module's Facade interface
- Add the error-path test before calling it done
