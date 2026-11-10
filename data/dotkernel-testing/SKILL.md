---
name: dotkernel-testing
description: >
  Use when writing, running or fixing tests in a Dotkernel project — unit tests, functional
  route tests, mocking repositories and services, authenticating a test request, seeding data, or
  diagnosing failures inside setUp such as "test mode is NOT enabled" or "non in-memory
  database". Also use when deciding what coverage a new route needs.
---

# Testing

```text
Applies to
  Projects:  - all
  Packages:  - none
```

```bash
composer test
php ./vendor/bin/phpunit --testsuite UnitTests
php ./vendor/bin/phpunit --testsuite FunctionalTests
php ./vendor/bin/phpunit --filter BookTest
```

Dotkernel `phpunit.xml` files commonly set `stopOnError` and `stopOnFailure`, so the run halts at
the first red test. Fix them one at a time.

## Prerequisite: the test config

Functional tests need a test-specific local config — commonly
`config/autoload/local.test.php`, copied from its `.dist` — pointing Doctrine at an in-memory
SQLite database. Without it, the base test case aborts with a message like:

- *"test mode is NOT enabled"* → the test config file is missing.
- *"running tests in a non in-memory database"* → present but not configured for memory.

**Never "fix" either by pointing tests at a real database.** That is the guard working.

The stock Frontend also ships `local.test.php.dist`, but it has no functional suite, and no base
class in its `test/Common/` enforces test mode, so its unit tests do not need the copy.

## Unit tests

`test/Unit/<Module>/<Layer>/<Class>Test.php`, namespace per `autoload-dev`.

Target services, middleware, attributes and helpers. Mock the repository; assert behaviour and
the exceptions:

```php
$repository = $this->createMock(BookRepository::class);
$repository->method('find')->willReturn(null);

$this->expectException(NotFoundException::class);
(new BookService($repository))->findBook('…');
```

Do not boot the container in a unit test. If you need the container, it is a functional test.

## Functional tests

Only the stock API and Admin ship a functional suite. Frontend and Light have unit tests only, and
Queue keeps its tests in `test/App/` and `test/Swoole/`. Do not add a functional suite to those
without asking — it means new base classes and test config.

`test/Functional/<Module>Test.php`, extending the repo's functional base class. **Read it before
writing anything** — the two stock base classes differ a lot.

**Admin** (`test/Functional/FunctionalTest.php` on the stock `7.0` branch) boots the container and
pipeline and offers only a `get()` request helper, `getContainer()`, `getEntityManager()` and
`runMigrations()`, which builds the schema from entity metadata. It has no status assertions,
entity factories, fixtures, login helper or service-replacement helper: assert on the response
directly and create data through the entity manager. Ask before adding helpers to the base class.

**API** (`test/Functional/AbstractFunctionalTest.php` on the stock `7.0` branch) boots the real
container, pipeline and routes, then builds the schema and loads every fixture in `setUp()` —
isolated per test, but not free. Keep tests purposeful. It provides:

- Request helpers per verb, pre-setting the right `Accept` header and attaching auth when logged
  in.
- Named status assertions (ok, created, no-content, bad-request, unauthorized, forbidden,
  not-found, conflict, gone) — use these rather than raw status comparisons.
- Entity factories and valid/invalid data builders for the project's core entities.
- Credential builders for the project's auth mechanism, plus deliberately invalid twins.
- A service-replacement helper for swapping container services — **use it so tests never send
  real email or make real outbound calls.**
- Direct entity-manager access for persistence setup.

Shape:

```php
class BookTest extends AbstractFunctionalTest
{
    public function testUserCanListBooks(): void
    {
        $identity = $this->createUser()->getIdentity();
        $this->loginAs($identity, self::DEFAULT_PASSWORD);

        $this->assertResponseOk($this->get('/book'));
    }

    public function testGuestCannotListBooks(): void
    {
        $this->assertResponseForbidden($this->get('/book'));
    }
}
```

## Required coverage for a new route

| Case | Expected |
| --- | --- |
| Happy path | 200 / 201 / 204 / rendered page — assert the payload or output, not just the status |
| Validation failure | 400 with the errors payload, or the form re-rendered with messages |
| Not authenticated | API: 403 — a request without a token runs as guest and is refused unless the route is granted to guest. Session-based project: a redirect to login |
| Authenticated, wrong role | 403 — **the case people skip.** Admin / Frontend: this is the test that catches a missing guard rule, because an unlisted route is open to everyone. API: a missing entry denies every role, so the happy path fails instead; this test catches a route granted to too many roles |
| Unknown identifier | 404 |
| Duplicate / conflicting write | 409 where applicable |

For a deprecated API route, also assert the `Sunset` header; for a templated page moved to a new
URL, assert the permanent redirect from the old one. For a form, also assert that a missing or
invalid CSRF token is rejected.

## Conventions

- Test method names read as sentences: `testAdminCannotDeleteOwnAccount`.
- Assert with `StatusCodeInterface::STATUS_*`, never bare integers.
- `test/` is covered by phpcs and phpstan too — tests must pass the same style and type checks.
- Never `markTestSkipped()` a test you broke, and never weaken an assertion to get green.
