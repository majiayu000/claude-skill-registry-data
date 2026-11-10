---
name: dotkernel-psr-standards
description: >
  Use when writing or reviewing any PHP in a Dotkernel project — which PSR applies, how to
  type handlers and middleware (PSR-7/PSR-15), how to obtain services (PSR-11, no service
  locator), logging (PSR-3), caching (PSR-6/PSR-16), building responses (PSR-17), autoloading
  (PSR-4), and coding style (PSR-1/PSR-12 via the Laminas Coding Standard). Also use when phpcs
  or phpstan complains, or when tempted to type-hint a concrete framework class instead of an
  interface.
---

# PSR compliance

```text
Applies to
  Projects:  - all
  Packages:  - all
```

Program against PSR interfaces. Type-hint the interface, inject the implementation. This applies
identically in every Dotkernel project.

## PSR-4 — autoloading

Namespace mirrors directory, case-sensitive, one class per file, file named after the class.

```text
<App>\User\Handler\User\GetUserResourceHandler → src/User/src/Handler/User/GetUserResourceHandler.php
Core\User\Entity\User                          → src/Core/src/User/src/Entity/User.php
```

Mappings live in `composer.json` under `autoload.psr-4` (and `autoload-dev` for tests). Adding a
mapping edits `composer.json` → needs user approval, then `composer dump-autoload`.

## PSR-7 — HTTP messages

Messages are **immutable**; `with*()` returns a new instance.

```php
$response = $response->withHeader('sunset', $date);   // correct
$response->withHeader('sunset', $date);               // silently does nothing
```

Type-hint `Psr\Http\Message\ServerRequestInterface` / `ResponseInterface`, never a concrete
Diactoros class. Read the body once via `(array) $request->getParsedBody()` — the body-params
middleware has already parsed it; re-reading the raw stream needs a `rewind()`.

## PSR-15 — handlers and middleware

```php
final class XMiddleware implements MiddlewareInterface
{
    public function process(
        ServerRequestInterface $request,
        RequestHandlerInterface $handler
    ): ResponseInterface {
        // before…
        $response = $handler->handle($request);
        // after…
        return $response;
    }
}
```

- Handlers implement `RequestHandlerInterface`; extend the project's abstract handler for its
  response helpers.
- One responsibility per middleware. Order is declared in `config/pipeline.php`, and changing it
  affects every request — justify any edit.
- Middleware that only enriches the request passes data via `$request->withAttribute(...)`.

## PSR-11 — container

Get services by constructor injection, resolved by the container:

```php
#[Inject(BookServiceInterface::class, CreateBookInputFilter::class)]
public function __construct(
    protected BookServiceInterface $bookService,
    protected CreateBookInputFilter $inputFilter,
) {
}
```

`dot-dependency-injection` reads `#[Inject]`; register the class with
`AttributedServiceFactory::class` in the module `ConfigProvider`. The stock Light does not install
`dot-dependency-injection` and uses hand-written factories instead; match that there. `#[Inject]` can also pull
config values by dotted key.

**Do not inject `ContainerInterface` and call `get()` inside a class** — that is the
service-locator anti-pattern. The only legitimate `$container->get()` sites are factories and
delegators, where you also declare `ContainerExceptionInterface` and
`NotFoundExceptionInterface`.

## PSR-3 — logging

Type-hint `Psr\Log\LoggerInterface`. Use levels deliberately: `error` for actionable failures,
`warning` for recoverable, `info` for lifecycle. Pass context as an array rather than
concatenating. **Never log credentials, tokens, password hashes, auth request bodies, or PII
beyond an identifier.**

## PSR-6 / PSR-16 — caching

Type-hint `Psr\Cache\CacheItemPoolInterface` (PSR-6) or `Psr\SimpleCache\CacheInterface`
(PSR-16). Always set an explicit TTL, never cache per-user-authorized data under a global key,
and provide an invalidation path when the underlying entity changes.

## PSR-17 — HTTP factories

Type-hint `ResponseFactoryInterface` / `StreamFactoryInterface` rather than instantiating a
concrete response — except inside the abstract handler, which already wraps the project's
response factory. Prefer its helpers over building responses yourself.

## PSR-1 / PSR-12 — style, enforced by the Laminas Coding Standard

`phpcs.xml` applies `LaminasCodingStandard`, a PSR-12 superset. It will fail you on:

- `declare(strict_types=1);` after `<?php` and one blank line.
- 4-space indent, LF endings, one trailing newline, no trailing whitespace, ~120-char lines.
- Sorted `use` statements: class imports first, blank line, then `use function` / `use const` —
  global functions **must** be imported, not called as `\count()`.
- Short array syntax; short closures where applicable.
- `! $foo`, not `!$foo`.
- Aligned `=>` in array literals and aligned `=` in consecutive assignments.
- One class per file; `final` where the class is not designed for extension.
- Type declarations on every parameter, property and return; nullable as `?Type`.

Run the repo's `cs-fix` for the mechanical parts. Never add sniff exclusions to `phpcs.xml` or
sprinkle `// phpcs:ignore` to get green.

## phpstan expectations

Dotkernel projects run a high level (commonly 8) with the Doctrine and PHPUnit extensions:

- No `mixed` leaking — cast or narrow at the boundary.
- Array shapes documented: `@param array<non-empty-string, mixed>`, `@return X[]`, and
  `@phpstan-type` / `@phpstan-import-type` for shapes reused across classes.
- Generics on collections: `@var Collection<int, UserRole>`.
- `instanceof` checks before using a nullable repository result — that is how the services here
  raise not-found errors.
- Do not silence with `@phpstan-ignore-*`. Fix the type.

## Framework-specific but non-negotiable

- Status codes via `Fig\Http\Message\StatusCodeInterface::STATUS_*`, not integer literals.
- Throw the project's typed exceptions with their static `::create(...)` constructors;
  messages from the shared message catalogue.
- Where the project provides a resource-resolution attribute on `handle()`, use it instead of
  fetching the entity manually.
