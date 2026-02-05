---
name: symfony:using-symfony-superpowers
description: Entry point for Symfony Superpowers - essential workflows, philosophy, and interactive commands for productive Symfony development
---

# Symfony Superpowers

This plugin delivers Symfony-specific guidance while remaining **environment-agnostic**, functioning in any Symfony application whether using Docker Compose, Symfony Docker (FrankenPHP), or host tools directly.

## Runner Selection

Prefer Docker if configured, otherwise fall back to host:

| Docker Type | Command Prefix | Console |
|-------------|----------------|---------|
| Symfony Docker | `docker compose exec php` | `docker compose exec php bin/console` |
| Docker Compose | `docker compose exec app` | `docker compose exec app bin/console` |
| Host | `php` | `php bin/console` |

## Essential Workflows

1. **TDD** - `symfony:tdd-with-pest` or `symfony:tdd-with-phpunit`
2. **Doctrine** - `symfony:doctrine-migrations`, `symfony:doctrine-fixtures-foundry`
3. **Quality** - `symfony:quality-checks` (PHP-CS-Fixer, PHPStan)
4. **Async** - `symfony:symfony-messenger`, `symfony:symfony-scheduler`
5. **Architecture** - `symfony:ports-and-adapters`, `symfony:cqrs-and-handlers`
6. **API** - `symfony:api-platform-resources`, `symfony:api-platform-filters`

## Philosophy

- **Lean controllers**: max 5-10 lines, delegate to services
- **DTOs & Value Objects**: typed data structures with Serializer
- **Voters**: granular authorization, not controller logic
- **Foundry factories**: realistic test data, not fixtures soup
- **Messenger**: async by default, sync for debugging

## Interactive Commands

- `/superpowers-symfony:brainstorm` - structured ideation
- `/superpowers-symfony:write-plan` - implementation planning
- `/superpowers-symfony:execute-plan` - methodical execution
- `/superpowers-symfony:symfony-check` - quality validation
- `/superpowers-symfony:symfony-tdd-pest` - TDD workflow

## Version Support

| Symfony | Status | Notes |
|---------|--------|-------|
| 6.4 LTS | Supported | LTS until Nov 2027 |
| 7.x | Supported | Current stable |
| 8.0 | Supported | Latest features |

| API Platform | Status |
|--------------|--------|
| 3.x | Supported |
| 4.x | Supported |

## Quick Reference

### Console Commands

```bash
# Clear cache
bin/console cache:clear

# Database
bin/console doctrine:migrations:migrate
bin/console doctrine:fixtures:load

# Messenger
bin/console messenger:consume async -vv

# Debug
bin/console debug:router
bin/console debug:container
bin/console debug:autowiring
```

### Test Commands

```bash
# PHPUnit
./vendor/bin/phpunit

# Pest
./vendor/bin/pest --parallel

# With coverage
./vendor/bin/pest --coverage --min=80
```

### Quality Commands

```bash
# PHP-CS-Fixer
./vendor/bin/php-cs-fixer fix

# PHPStan
./vendor/bin/phpstan analyse

# All checks
composer run-script check
```
