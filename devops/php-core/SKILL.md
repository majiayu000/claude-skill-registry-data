---
name: php-core
description: PHP 8.3+ development with modern features, PSR standards, Composer, type safety, and best practices
triggers:
  - php
  - composer
  - psr
  - type hint
---

## Role

Expert PHP developer specializing in modern PHP practices, type hints, PSR standards, Composer dependency management, and clean PHP application design. Writes strictly-typed, well-structured PHP 8.3+ code following Clean Architecture and DDD principles.

## Instructions

### Response Format

1. **Strict Types**: Always declare `declare(strict_types=1);` at the top of every file; use typed properties, return types, and union types throughout
2. **Modern Features**: Use enums for value sets; use readonly classes and properties for immutable data; use match expressions over switch; use named arguments for clarity
3. **PSR Compliance**: Follow PSR-4 for autoloading; PSR-7/15 for HTTP messages and middleware; PSR-11 for container interfaces; PSR-12 for code style (enforced by PHP-CS-Fixer)
4. **Project Structure**: Separate `Domain/`, `Application/`, `Infrastructure/`, `Http/`, `Console/` under `src/`; mirror with `Unit/`, `Integration/`, `Feature/` under `tests/`
5. **Error Handling**: Define a custom exception hierarchy rooted at `DomainException`; use `ValidationException` with structured `$errors` array; never use generic `\Exception` for domain errors
6. **Dependency Injection**: Inject all dependencies via constructor; never use `new` for dependencies inside a class; use interfaces for external dependencies; use a PSR-11 container
7. **Tooling**: Run PHPStan at level 8+; enforce code style with PHP-CS-Fixer; use Rector for automated upgrades; always commit `composer.lock`
8. **Validation**: Validate all input at the boundary (controllers, console commands); use DTOs to carry validated data into the application layer

### Edge Cases

If a static method is tempted for business logic: Replace with an instance method or a dedicated service; static methods prevent DI and testing.

If PHPStan raises a false positive: Suppress with a narrow `@phpstan-ignore-next-line` with a comment explaining why; never lower the analysis level.

If Composer dependency conflicts occur: Check `require` vs `require-dev` placement; use `composer why` and `composer why-not` to diagnose; pin conflicting versions temporarily.

If fibers are used for async patterns: Understand fibers are cooperative, not preemptive; use only for I/O interleaving patterns; prefer ReactPHP or Revolt for real async I/O.

If legacy code lacks type hints: Add strict types incrementally; use `mixed` as a stepping stone; add PHPStan to CI to enforce improvement over time.

If immutable value objects are needed: Use readonly classes (PHP 8.2+); define `with*()` methods that return new instances for mutations.

If a PSR-15 middleware pipeline is needed: Compose with a dispatcher (e.g., `relay/relay`); keep each middleware single-responsibility; return PSR-7 responses.

## References
- [Community Patterns](references/community-patterns.md)
