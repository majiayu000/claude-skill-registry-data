---
description: Scaffold a repository — interface in Domain, Eloquent implementation in Infrastructure, plus binding and test
argument-hint: "<Module>/<Entity>"
disable-model-invocation: true
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash(vendor/bin/phpunit *), Bash(composer *)"
---

# New Repository

Create the repository in `$ARGUMENTS` (e.g. `Chat/Message`). Repositories are the **only** place Eloquent may appear.

Read `modules/Chat/Infrastructure/Repository/ChatRepository.php` and mirror it. Layer rules: `.claude/rules/architecture.md`.

## Files

```
modules/<Module>/Domain/Repository/<Entity>RepositoryInterface.php
modules/<Module>/Infrastructure/Repository/<Entity>Repository.php
tests/Feature/<Module>/<Entity>RepositoryTest.php
modules/<Module>/<Module>ServiceProvider.php          # binding
```

## Interface (Domain)

```php
namespace Modules\<Module>\Domain\Repository;

interface <Entity>RepositoryInterface
{
    public function find(int $id): ?<Entity>;

    public function save(<Entity> $entity): <Entity>;

    public function delete(<Entity> $entity): void;

    // public function findActiveByUser(string $npub): array;
}
```

Method names describe **domain intent** (`findActiveByUser`), not query mechanics (`findByStatusAndDate`).

## Implementation (Infrastructure)

```php
namespace Modules\<Module>\Infrastructure\Repository;

use App\Models\<Entity>;

final readonly class <Entity>Repository implements <Entity>RepositoryInterface
{
    public function find(int $id): ?<Entity>
    {
        return <Entity>::find($id);
    }

    public function save(<Entity> $entity): <Entity>
    {
        $entity->save();

        return $entity;
    }
}
```

## Binding

```php
<Entity>RepositoryInterface::class => <Entity>Repository::class,
```

## Test — Feature suite, needs a real DB

```php
final class <Entity>RepositoryTest extends TestCase
{
    use RefreshDatabase;

    public function test_find_with_existing_id_returns_entity(): void { /* … */ }

    public function test_find_with_unknown_id_returns_null(): void { /* … */ }
}
```

Consumers (Actions, Services) mock the **interface** in their own unit tests.

## Specific to repositories

- Queries live here, never in Actions, Services, or Controllers
- Return models or domain objects — never a query builder
- Eager-load relations here so callers can't cause N+1
- Missing model? Create it in `app/Models/` plus a migration

```bash
composer test
```
