---
name: dotkernel-troubleshooting
description: >
  Use when something in a Dotkernel project is not working and the cause is unclear — a route
  returns 403, 404, 406, 415 or 500 unexpectedly, a service is not found in the container, a
  handler throws while building a response, config changes have no effect, routes are missing,
  tests fail in setUp, autoloading fails, a form silently rejects a submit, or CORS preflight
  fails. Start here before reading code at random.
---

# Symptom → cause

```text
Applies to
  Projects:  - all
  Packages:  - none
```

Work top-down; the first match is usually it.

## 403 / access denied on a route you just added

API: the route name is missing from the RBAC permissions in `authorization.global.php`. Route
names **are** authorization keys. Add it for every role that should reach it, and check the role
hierarchy comment at the top of the file — inheritance direction is not always what people assume.

Admin / Frontend: a *missing* guard entry does not cause a 403 — the guards use `POLICY_ALLOW`,
so an unlisted route is open to everyone. A 403 there means a guard rule exists in
`authorization-guards.global.php` and the caller's role lacks that permission in
`authorization.global.php`. The reverse symptom — a new page reachable while logged out — is
the missing entry.

## 404 on a route you just added

1. The module's `ConfigProvider` is not listed in `config/config.php`.
2. `RoutesDelegator` is not registered as a delegator on `Application::class` in that ConfigProvider.
3. Config cache is stale → run the repo's cache-clear script.
4. Confirm with the route-listing command. Absent → causes 1–3. Present → your URL or method
   differs from what you are calling (API updates are PATCH; templated projects submit POST).

## 404 on an existing route with a valid identifier

The resource-resolution attribute could not find the entity — identifier or placeholder mismatch,
or the record genuinely does not exist.

## "Service not found" / container exception

A missing `factories` entry, or you type-hinted an interface with no `aliases` entry mapping it to
the concrete class. Both live in the module `ConfigProvider`.

## Handler throws while building a response

The handler is missing its delegator registration. In the API that is the handler delegator that
injects the HAL response factory and resource generator — they are not constructor-injected.

## `#[Inject]` appears to be ignored

The class is registered with the wrong factory. It needs `AttributedServiceFactory::class`, not
`InvokableFactory` or a hand-written factory.

## Config change has no effect

Config cache. Also check load order: `*.local.php` overrides `*.global.php`, and the test-local
file overrides both under tests.

## 406 Not Acceptable

The `Accept` header does not match what content negotiation allows for that route.

## 415 Unsupported Media Type

Missing or wrong `Content-Type` on a write request.

## Empty or malformed body on a write

The malformed-body middleware rejected it, or you read the raw stream after the body-params
middleware consumed it. Use `getParsedBody()`.

## A form submit is silently rejected (templated projects)

Missing, stale or unvalidated CSRF token. Check the form has the CSRF element and the handler
validates it. A rotated session invalidates in-flight forms.

## CORS preflight fails

The CORS middleware must be piped **before** the routing middleware, and the origin must be listed
in the CORS local config — which does not exist until you copy it from the `.dist`.

## 403 with a token that "should" work

In stock Dotkernel API a token that fails validation does not produce 401: the authentication
middleware turns any request it cannot authenticate into a guest, so a route not granted to guest
answers 403. Causes: expired token, wrong client id or scope, or the OAuth keys were regenerated
after the token was issued. A 403 that persists with a freshly issued token is an authorization
problem instead — see "403 / access denied on a route you just added" above.

401 comes only from the token-issuing operations, or from a project that pipes Mezzio's own
`AuthenticationMiddleware` instead of the stock one — that middleware answers 401 when
authentication fails. Check which one `config/pipeline.php` or the route's middleware list uses.

## Class not found after adding a namespace

`composer dump-autoload`, then check the PSR-4 mapping. Case-sensitive, even where the local
filesystem is not.

## Tests fail in `setUp()`

- *"test mode is NOT enabled"* → the test-local config file is missing.
- *"non in-memory database"* → present but not configured for memory. Do not repoint tests at a
  real database.
- Column type errors only under test → an enum DBAL type with no SQLite branch.

## Schema-validation CI job is red

Entities and migrations have drifted. Generate a migration; do not edit the entity to match an old
migration, and do not hand-edit the migration.

## Passes locally, fails in CI (or the reverse)

A different PHP version in the matrix, or a stale local `.phpcs-cache` / `.phpunit.result.cache`.

## Diagnostic commands

All read-only except `composer clear-config-cache`, which deletes the cached merged config — safe,
and it touches no committed file, but it is a write.

```bash
php bin/cli.php route:list          # API / Admin; or the repo's equivalent
php bin/cli.php                     # console commands — API, Admin, Queue (no bin/cli.php in Frontend or Light)
composer clear-config-cache
php -l <file>
composer cs-check
composer static-analysis
php ./vendor/bin/doctrine-migrations status
php ./bin/doctrine fixtures:list
```

If nothing above matches, say so and ask. Do not start editing config files to see what happens.
