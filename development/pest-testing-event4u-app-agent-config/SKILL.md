---
model_tier: medium
name: pest-testing
description: "Use when writing, generating, or improving Pest tests for Laravel — clear intent, good coverage, maintainable structure, and alignment with project testing conventions."
domain: quality
workspaces:
  - engineering
packs:
  - laravel
trust:
  level: professional
install:
  default: false
  removable: true
triggers:
  - phrase: "pest test"
  - phrase: "pest suite"
---

# pest-testing

## When to use

Use this skill for all Laravel testing tasks, especially when working with:

- Feature tests
- Unit tests
- API endpoint tests
- Model tests
- Service tests
- Authorization tests
- Validation tests
- Database interaction tests
- Factories, fakes, mocks, and test setup

This skill extends `php-coder`, `laravel`, and `eloquent`.

For prevention layers that fire **before** writing a test — TDD
discipline, mock-isolation gates, and the 12 process rationalizations
("I'll add the test after", "patch first, test later") — see
[`test-driven-development`](../test-driven-development/SKILL.md),
[`testing-anti-patterns`](../testing-anti-patterns/SKILL.md), and
[`process-anti-patterns.md`](../testing-anti-patterns/process-anti-patterns.md).

## Procedure: Write Pest tests

1. **Read the base skills first** — apply `php-coder`, `laravel`, and `eloquent` where relevant.
2. **Check the project's test framework** — confirm Pest is used and inspect existing tests.
3. **Match the current test style** — naming, helpers, datasets, expectations, setup, traits, and folder structure.
4. **Check available factories and seeders** — reuse existing test data patterns.
5. **Understand the behavior under test** — inspect controllers, services, requests, policies, jobs, and models before writing tests.
6. **Prefer existing helpers** — authentication helpers, custom assertions, base test classes, and shared setup.

## Core testing principles

- Test behavior, not implementation details.
- Prefer clear, intention-revealing tests over overly clever abstractions.
- One test should verify one meaningful behavior.
- Keep setup minimal and relevant.
- Favor confidence and maintainability over excessive mocking.
- Cover happy path, validation failures, authorization failures, and important edge cases.
- Enumerate the cases BEFORE writing — run the [`test-case-discovery`](../test-case-discovery/SKILL.md) funnel; floor per behavior: 1 happy + 1 boundary + 1 error (+1 abuse on security paths).

## TDD workflow (Red-Green-Refactor)

For bug fixes and new features, prefer test-driven development:

1. **RED** — Write a failing test that describes the expected behavior.
2. **Verify RED** — Run the test, confirm it fails for the expected reason (missing feature,
   not a typo or syntax error). If the test passes immediately, it tests existing behavior — fix it.
3. **GREEN** — Write the **minimal** code to make the test pass. No extras, no "while I'm here".
4. **Verify GREEN** — Run all tests, confirm the new test passes and nothing else broke.
5. **REFACTOR** — Clean up code while keeping tests green.

### Why test-first matters

Tests written **after** implementation pass immediately. Passing immediately proves nothing:
- The test might test the wrong thing.
- The test might test implementation, not behavior.
- You never saw it catch the bug — so you don't know if it would.

### Bug fix TDD

For every bug fix: write a failing test that reproduces the bug FIRST, then fix it.
The test proves the fix works AND prevents regression.

### TDD rationalization prevention

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Manual test is faster" | Manual doesn't prevent regression. You'll re-test every change. |
| "Test is hard to write" | Hard to test = hard to use. Simplify the design. |
| "Need to explore first" | Fine — throw away exploration code, start fresh with TDD. |
| "Existing code has no tests" | You're improving it. Add tests for what you touch. |

## Laravel testing rules

- Use **Feature tests** for HTTP endpoints, request validation, middleware behavior, authorization, and end-to-end application flow.
- Use **Unit tests** for isolated services or pure logic when true isolation adds value.
- Prefer Feature tests over Unit tests when framework integration is part of the behavior.
- Use `RefreshDatabase` or the project's standard database reset strategy where appropriate.
- Reuse factories instead of manually creating large fixture arrays.

## Pest style rules

- Write descriptive test names in plain language.
- Use `it()` / `test()` according to existing project conventions.
- Group related tests logically.
- Use datasets when they improve readability and reduce duplication.
- Keep each test focused and concise.

## Pest-specific PHP rules

- Do NOT use `readonly` or `final` on Pest test classes.
- Do NOT mark classes `final` if they need to be mocked via `Mockery::mock()`.
- Pest test files (without a `namespace` declaration) treat all PHP built-in classes as global.
  Do **NOT** add `use` statements for global classes like `DateTimeImmutable`, `Exception`,
  `stdClass`, etc. — PHP will warn: *"The use statement with non-compound name has no effect"*.
- Only `use` statements for **namespaced** classes (e.g., `use App\Models\...`) are needed.

## Avoiding flaky tests

- **Time-dependent tests:** Use `$this->travel(5)->seconds()` (Laravel's time travel) to create
  a clear gap between "before" and "after" timestamps. Never rely on `now()` being different
  between two lines of code — on fast hardware, they can be identical.
- **Database-dependent tests:** Don't assume column values are `null` just because the seeder
  doesn't set them — previous tests in parallel may have modified the same record.
- **Parallel testing:** The project may use parallel testing (8+ processes). Avoid relying on
  global state, specific row counts, or auto-increment IDs.

## HTTP and API tests

- Test:
    - status codes
    - response structure
    - validation errors
    - authorization behavior
    - persistence side effects
- For JSON APIs, assert:
    - exact relevant fields
    - error structure when applicable
    - database state after the request
- Do not only assert `200` — verify meaningful behavior.

## Validation tests

- Validate important request rules explicitly.
- Cover required fields, invalid formats, boundary values, and business-critical constraints.
- Prefer focused validation tests over giant "all fields invalid" tests unless the project already uses that pattern.

## Authorization tests

- Always test protected actions for:
    - guest users
    - unauthorized users
    - authorized users
- Match the project's auth setup and policy usage.
- Do not assume authorization works just because a policy exists.

## Database assertions

- Assert persistence effects with:
    - `assertDatabaseHas`
    - `assertDatabaseMissing`
    - relation checks where relevant
- Keep assertions focused on meaningful fields.
- Do not assert every column unless necessary.

## Snapshot testing with `coduo/php-matcher`

This project uses [`coduo/php-matcher`](https://github.com/coduo/php-matcher) for flexible snapshot assertions.
Pattern files live in `snapshots/` directories next to the test files.

### Pattern variables

Use pattern variables instead of hardcoded values in snapshot files.
This makes snapshots resilient to data changes while still enforcing type correctness.

| Pattern | Matches | Example |
|---|---|---|
| `@boolean@` | `true` or `false` | `'is_active' => '@boolean@'` |
| `@integer@` | Any integer | `'id' => '@integer@'` |
| `@string@` | Any string | `'name' => '@string@'` |
| `@null@` | `null` | `'deleted_at' => '@null@'` |
| `@datetime@` | ISO datetime string | `'created_at' => '@datetime@'` |
| `@uuid@` | UUID string | `'uuid' => '@uuid@'` |
| `@array@` | Any array | `'items' => '@array@'` |
| `@double@` | Any float | `'amount' => '@double@'` |
| `@wildcard@` | Anything | `'data' => '@wildcard@'` |

Combine with `||` for nullable fields: `'deleted_at' => '@null@||@datetime@'`

### Rules

- **Never hardcode dynamic values** (IDs, timestamps, UUIDs) in snapshots — use pattern variables or `$replacements`.
- **Never hardcode boolean defaults** (e.g., `false`) when other booleans in the same file use `@boolean@` — be consistent.
- Use `$variable ?? '@pattern@'` syntax to allow test-specific overrides via `replacements` parameter.
- Use `PhpMatcherHelper::ruleBackedEnum(EnumClass::class, 'string')` for enum fields.

### Example snapshot file

```php
// snapshots/user-resource.php
return [
    'id' => $id ?? '@integer@',
    'name' => $name ?? '@string@',
    'email' => $email ?? '@string@',
    'is_active' => $is_active ?? '@boolean@',
    'created_at' => $created_at ?? '@datetime@',
    'deleted_at' => $deleted_at ?? '@null@||@datetime@',
];
```

### Example test usage

```php
expect($response->json())
    ->toMatchPhpPatternFile(
        patternFile: __DIR__ . '/snapshots/user-resource.php',
        replacements: ['id' => $user->getId()],
    );
```

## Fakes, mocks, and external boundaries

- Use Laravel fakes for framework integrations when appropriate:
    - `Queue::fake()`
    - `Bus::fake()`
    - `Event::fake()`
    - `Mail::fake()`
    - `Notification::fake()`
    - `Storage::fake()`
- Mock only true external boundaries or expensive dependencies.
- Avoid mocking internal application code unless isolation is necessary for the specific test.

## Factories and fixtures

- Prefer factories with explicit state over large inline setup.
- Use named states for meaningful scenarios.
- Keep test data realistic and minimal.
- Do not create unnecessary records.

## Test quality analysis

When reviewing or auditing existing tests, check for these anti-patterns:

### Test smells to detect

| Smell | Description | Fix |
|---|---|---|
| **Overmocking** | Too many mocks disconnect the test from reality | Replace mocks with real implementations or fakes |
| **Fragile tests** | Tests break with unrelated changes (e.g., asserting exact JSON structure) | Assert only meaningful fields |
| **Flaky tests** | Non-deterministic results (time, ordering, parallel state) | Use time travel, explicit ordering, isolated data |
| **Giant tests** | One test covers 5+ behaviors | Split into focused tests |
| **Missing assertions** | Test runs code but doesn't verify outcomes | Add meaningful assertions |
| **Test duplication** | Same scenario tested in multiple places | Consolidate or use datasets |
| **Assertion roulette** | Many assertions without clear failure messages | Use named assertions or split tests |
| **Eager test** | Tests too many things, making failures hard to diagnose | One behavior per test |

### FIRST principles

- **Fast** — Tests should run quickly. Avoid unnecessary DB operations.
- **Isolated** — Tests should not depend on each other or shared state.
- **Repeatable** — Same result every time, regardless of environment or order.
- **Self-validating** — Pass or fail, no manual inspection needed.
- **Timely** — Written close to the code they test.

### Mock usage guidelines

- Mock **external boundaries** (APIs, file systems, third-party services).
- Use Laravel fakes (`Queue::fake()`, `Http::fake()`) over manual mocks.
- Do NOT mock the class under test.
- Do NOT mock value objects or DTOs.
- If a test needs 3+ mocks, consider testing at a higher level (Feature test).

## What NOT to do

- Do not test private methods directly.
- Do not over-mock Laravel internals.
- Do not assert implementation details when behavior assertions are enough.
- Do not write brittle tests tied to formatting or irrelevant response noise.
- Do not create giant tests that cover many behaviors at once.
- Do not skip authorization or validation coverage for important endpoints.

## Output expectations

When generating Pest tests:

- follow the existing folder and naming conventions
- test behavior clearly and directly
- cover success, failure, and authorization paths
- use factories and Laravel test helpers
- assert both response and side effects where relevant
- keep tests readable, isolated, and maintainable

### Filter Pest output

When triaging a verbose run, narrow the output with `--filter` (Pest)
plus targeted `grep`/`rg` instead of re-running the whole suite or
echoing all logs:

```bash
# Only run failing tests in one file
vendor/bin/pest tests/Feature/InvoiceTest.php --filter='creates invoice'

# Scan the test log for failures only
rg --color=never '^FAIL|Tests:' storage/logs/pest.log

# Inspect JSON output from data-driven tests
vendor/bin/pest --log-junit=pest.xml && rg '<failure' pest.xml
```


## Output format

1. Pest test file with descriptive test names and clear assertions
2. Tests organized by happy path, validation, edge cases

## Gotcha

- Don't use `readonly` or `final` on Pest test helper classes — it breaks mocking.
- Don't add `use` statements for global classes (`Exception`, `DateTimeImmutable`) in Pest files — they're auto-imported.
- The model forgets `$this->travel(5)->seconds()` for time-dependent tests — never rely on `now()` differing between lines.
- Parallel tests share the database — don't assume column values are null unless you explicitly set them.

## Do NOT

- Do NOT mark classes final if they need to be mocked via Mockery.
- Do NOT use PHPUnit class-based syntax — use Pest syntax.

## What to test (generation checklist)

When generating new tests, focus on:
- **Business logic**: calculations, status transitions, validation rules, data transformations
- **Edge cases**: null, empty string, zero, negative numbers, boundary values, max length
- **Error paths**: invalid input, missing dependencies, exception handling
- **Different code branches**: if/else, early returns, fallback behavior

What NOT to test:
- Trivial getters/setters without logic
- Parameter counts, method existence, class names
- Framework internals (Eloquent, routing)
- Private methods directly — test through public API

**Quality over quantity** — 5 meaningful tests beat 20 trivial ones.

## Auto-trigger keywords

- Pest test
- PHPUnit
- test writing
- test quality
- TDD
- generate tests
- write tests
- test coverage
- test scenarios
