---
name: php
description: Use when building PHP applications with Laravel — models and migrations on MySQL, validation, money and unit calculations, Artisan commands, Pest or PHPUnit tests, and running the stack in Docker. Also use when choosing between Laravel and a micro-framework, or when results differ between the local PHP version and the container.
---

# PHP with Laravel

Default: the current PHP 8.x, Laravel (the mainstream framework — choose a micro-framework only with a written reason, "it is lighter" is not one), MySQL 8 or SQLite for tests, Composer, PHPUnit or Pest, Docker Compose to run everything.

## Setup

1. `composer create-project laravel/laravel app` inside a PHP container, so the host needs only Docker.
2. Keep local settings in the environment file Laravel reads at start-up, commit only the example file without secrets, and generate `APP_KEY` per environment.
3. Compose services: `app` (php-fpm or `php artisan serve` for development), `db` (MySQL with a named volume), optional `queue`.

## Modelling

- One migration per schema change; never edit a migration that has run anywhere else — add a new one.
- Use Eloquent casts for types (`'price' => 'integer'`, `'bought_at' => 'immutable_datetime'`).
- Store money in integer minor units and quantities with explicit units (grams, millilitres). Convert at the edge.
- Validate input with Form Requests; keep controllers thin and put calculations in plain service classes you can unit-test.

## Calculations people check by hand

For price-per-unit, discounts and point rebates:

- Compute in integers or `bcmath`; floats produce off-by-one-yen style errors.
- Write down the rounding rule (floor, round half up, banker's) and test the boundary cases.
- Keep the history of inputs so a result can be explained later ("previous price", "change since last time").

## Testing

- `php artisan test` with an in-memory SQLite database (`DB_CONNECTION=sqlite`, `DB_DATABASE=:memory:`) for speed, plus a CI job against MySQL if you use MySQL-specific features.
- Use factories for test data and `RefreshDatabase` to isolate tests.
- Feature tests over HTTP for routes, unit tests for services.

## Verification loop

1. `composer validate` and `php -l` on changed files.
2. `vendor/bin/pint --test` (formatting) and a static analyser (Larastan/PHPStan) at a level you keep green.
3. `php artisan test`.
4. `docker compose up` from a clean checkout to prove the setup instructions work.

## Pitfalls

- **Mass assignment:** define `$fillable` (or `$guarded`) on every model.
- **N+1 queries:** eager-load relations with `with()`; enable `Model::preventLazyLoading()` in development.
- **Time zones:** set `APP_TIMEZONE` and store UTC in the database; MySQL `TIMESTAMP` converts, `DATETIME` does not.
- **Strict mode in MySQL** rejects invalid dates and truncation that older setups accepted; keep it on and fix the data.
- **Config cache:** after `php artisan config:cache`, `env()` outside config files returns null. Read settings through `config()`.
- **Composer platform:** set `config.platform.php` to the production PHP version so dependency resolution matches.
