---
name: php
description: Use when writing PHP 8.2+ or working in Laravel and Symfony codebases. Covers strict types, enums, readonly classes, attributes, PSR standards, and static analysis with PHPStan.
metadata:
  category: languages
  version: 1.0.0
  tags: [php, laravel, symfony, phpstan, psr]
---

# PHP

## Purpose

Write PHP that behaves like a typed language: strict types on, enums instead of string constants, readonly value objects, and PHPStan at a level high enough to catch real defects.

## When to Use

- Writing or reviewing PHP 8.2+.
- Working in Laravel or Symfony applications.
- Introducing static analysis to a legacy PHP codebase.
- Modeling domain values and states.
- Fixing performance problems in ORM-heavy code.

## Capabilities

- Strict typing, union and intersection types, `never` and `readonly`.
- Enums with backing values and interfaces.
- Attributes for routing, validation, and DI metadata.
- PSR-4 autoloading, PSR-12 style, PSR-3 logging.
- PHPStan configuration and incremental adoption via baselines.

## Inputs

- Source tree, `composer.json`, framework and version.
- Existing analysis configuration and baseline, if any.

## Outputs

- Files opening with `declare(strict_types=1);`.
- Typed properties, parameters, and return types throughout.
- A PHPStan configuration at level 8 (or a baseline plus a plan to reach it).

## Workflow

1. **Turn on strictness** — `declare(strict_types=1)` in every file; PHPStan with a baseline to freeze existing debt.
2. **Replace magic with types** — String constants become enums; array shapes become value objects or DTOs.
3. **Implement** — Constructor promotion, readonly properties, named arguments at call sites.
4. **Eliminate ORM traps** — Eager-load relations; never query inside a loop.
5. **Gate** — PHPStan, PHP-CS-Fixer, PHPUnit or Pest.

## Best Practices

- Never use `array` as a domain type. An untyped array is a shape that no tool can check.
- Enums replace class constants and give you exhaustive `match`.
- Readonly promoted constructor properties are the shortest path to immutable value objects.
- In Eloquent, `with()` your relations. An N+1 query in a list endpoint is the single most common PHP performance defect.
- Do not catch `\Exception` broadly. Catch the specific type, or let it reach the handler.
- Keep framework types out of the domain layer — a domain service should not know what an HTTP request is.

## Examples

**Enum plus readonly value object:**

```php
<?php
declare(strict_types=1);

enum SubscriptionState: string
{
    case Trialing  = 'trialing';
    case Active    = 'active';
    case PastDue   = 'past_due';
    case Cancelled = 'cancelled';

    public function isBillable(): bool
    {
        return match ($this) {
            self::Active, self::PastDue => true,
            self::Trialing, self::Cancelled => false,
        };
    }
}

final readonly class Subscription
{
    public function __construct(
        public string $id,
        public SubscriptionState $state,
        public \DateTimeImmutable $renewsAt,
    ) {}
}
```

## Notes

- PHPStan level 8 adds null-safety checks; it is the level where the tool starts finding real bugs rather than style issues.
- `readonly` classes (8.2) make every property readonly implicitly — a cleaner default for DTOs.
- Laravel's `lazy()` and `chunk()` prevent memory exhaustion on large result sets; `get()` on an unbounded query will eventually take the process down.
