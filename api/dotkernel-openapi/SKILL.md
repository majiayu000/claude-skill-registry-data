---
name: dotkernel-openapi
description: >
  Use when documenting an endpoint in a Dotkernel project that publishes OpenAPI (typically
  the API) — adding or editing a module's OpenAPI.php, describing request bodies, responses,
  parameters, security schemes or schemas, marking an operation deprecated, or regenerating the
  interactive documentation. Also use when an endpoint exists but is missing from the docs, or
  when checking whether this project publishes OpenAPI at all.
---

# OpenAPI documentation

```text
Applies to
  Projects:  - Dotkernel API
  Packages:  - none
```

**Applies only to projects that publish OpenAPI.** Confirm first: `zircote/swagger-php` in
`composer.json` and per-module `src/<Module>/src/OpenAPI.php` files. Of the stock projects only the
API publishes OpenAPI; Admin, Frontend, Light and Queue have no OpenAPI surface. Whether a
project has a `documentation/` directory varies in derived projects — check, do not infer it.

Why it matters: it lets front-end and back-end developers work in parallel against mock servers,
it makes documentation auto-generated rather than hand-maintained, and tooling like Postman and
codegen consumes it.

## Where the attributes live

Not on the handler. Each module has one dedicated file containing no classes — only a sequence of
`#[OA\…]` attributes, each preceded by a docblock pointing at the handler it documents:

```php
/**
 * @see GetBookCollectionHandler::handle()
 */
#[OA\Get(
    path: '/book',
    description: 'Authenticated admin fetches a list of books',
    summary: 'Admin lists books',
    security: [['AuthToken' => []]],
    tags: ['Book'],
    parameters: [
        new OA\Parameter(
            name: 'page',
            description: 'Page number',
            in: 'query',
            required: false,
            schema: new OA\Schema(type: 'integer'),
            example: 1,
        ),
    ],
    responses: [
        new OA\Response(
            response: StatusCodeInterface::STATUS_OK,
            description: 'Returns a paginated list of books',
        ),
    ],
)]
```

## Rules

- Keep operations in the same order as the routes in `RoutesDelegator`, so the two files diff by
  eye.
- One `tags` entry per resource, matching the module.
- The security scheme on **every** authenticated endpoint. Omitting it tells clients the endpoint
  is public — a documentation bug with security consequences.
- Status codes via `StatusCodeInterface::STATUS_*`, not literals.
- Document failure responses too: 400, 403, 404 and 409 where they apply. A missing or invalid
  token runs as guest, so a protected operation answers 403, not 401. Only the token-issuing
  operations can answer 401 — verify which errors do in the repo before documenting it.
- Deprecated operations get `deprecated: true` plus a description naming the replacement, paired
  with the deprecation attribute on the handler (see `dotkernel-evolution-pattern`).
- Reuse `OA\Schema` definitions rather than repeating inline shapes.

## Security constraints

- **Never** put a real credential, token, internal hostname, customer email or production
  identifier in an `example`. Use obvious placeholders.
- Interactive documentation should not be enabled in production.

## Definition of done

An endpoint is not finished until its operation exists. The route, the authorization entry and the
documentation are three separate registrations, and it is easy to do two of the three — verify all
of them.
