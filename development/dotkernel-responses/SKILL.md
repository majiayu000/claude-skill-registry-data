---
name: dotkernel-responses
description: >
  Use when shaping what a Dotkernel handler returns — HAL resources and collections and the
  MetadataMap for API-style projects, or templates, redirects and flash messages for templated
  projects — plus pagination, content negotiation, and the error body. Also use when a response
  is missing links, a list is not paginated, a resource exposes the wrong fields, or an error
  leaks internal detail.
---

# Responses

```text
Applies to
  Projects:  - Dotkernel API
             - Dotkernel Admin
             - Dotkernel Frontend
             - Dotkernel Light
  Packages:  - none
```

Identify the variant first (`dotkernel-project-variants`). Both dialects share one rule:
**handlers do not hand-build response payloads.** They hand an object to the presentation layer.

## API-style: HAL

### Single resource

1. The entity extends the `Core` abstract entity, which implements `ArraySerializableInterface`.
   **`getArrayCopy()` is your serialisation boundary** — it decides what a client receives.
   Never expose password hashes, internal numeric ids, tokens, or relations you did not intend.
2. Register it in the module `ConfigProvider`'s HAL config:

   ```php
   AppConfigProvider::getResource(Book::class, 'book::view-book')
   ```

   That maps to route-based resource metadata with an array-serialisable hydrator and generates
   the `self` link from the named route. Optional arguments override the identifier property and
   the route placeholder.

3. The handler returns the repo's `createResponse(...)`, or its created-response helper for 201.

### Collections

1. `<App>\<Module>\Collection\BookCollection` extends the project's resource collection
   class (itself a Doctrine `Paginator`) — usually an empty class body.
2. Register it, naming the embedded relation (plural, lowercase):

   ```php
   AppConfigProvider::getCollection(BookCollection::class, 'book::list-book', 'books')
   ```

3. The service returns a `QueryBuilder`; the handler wraps it:

   ```php
   return $this->createResponse(
       $request,
       new BookCollection($this->bookService->getBooks($request->getQueryParams()))
   );
   ```

Pagination links (`first`, `prev`, `self`, `next`, `last`) are generated from the route. Do not
build them.

### Content negotiation

The content-negotiation middleware picks the representation from `Accept` — typically
`application/json` and `application/hal+json`. Never hardcode a `Content-Type` in a handler.

## Templated: views, redirects, flash

- The handler — or, in Frontend, the controller action — renders a named template through the
  renderer and returns an HTML response.
  Template paths are registered under `templates` in the module `ConfigProvider`.
- Pass view models or plain arrays; **escaping happens in the view**. Never assemble HTML in a
  handler or service.
- After a successful write, redirect to a `GET` route rather than rendering — the post/redirect/get
  pattern — and carry the outcome in a flash message.
- After a failed write, re-render the same template with the bound form so input and messages
  survive (see `dotkernel-input-validation`).
- Build URLs with the URL helper and the route name, never string concatenation.

## Pagination (both dialects)

The shared paginator helper normalises the query string:

| Param | Behaviour |
| --- | --- |
| `page` | 1-based; derives `offset` |
| `offset` | alternative to `page` |
| `limit` | has a default; clamp the maximum |
| `sort` | **must be whitelisted** against an explicit column list |
| `dir` | `asc` \| `desc` |

The whitelist lives in the service. Skipping it is a security issue, not a style choice.

## Errors

Throw; do not construct error responses. The error-handling middleware renders them
consistently — RFC 7807 problem details in the API, an error page or flash in a templated project.

```php
throw BadRequestException::create(
    detail: Message::VALIDATOR_INVALID_DATA,
    additional: ['errors' => $this->inputFilter->getMessages()]
);
```

The project's exception namespace maps to status codes — bad request 400, unauthorized 401,
forbidden 403, not found 404, not acceptable 406, conflict 409, unsupported media type 415, plus
project-specific ones. Messages come from the shared catalogue. **Never leak SQL, stack traces, file
paths or internal class names** into a user-visible message.

One known exception in the stock API: `AuthorizationMiddleware` answers a refusal with
`{"error": {"messages": [...]}}` and status 403 instead of problem details. Do not copy that
pattern — new code throws.

Non-resource successes have helpers too — empty/no-content, an info-message envelope, plain
JSON. Prefer the existing helper over an ad-hoc shape so clients see one consistent envelope.

## Checklist

- [ ] `getArrayCopy()` (or the view model) exposes exactly the intended fields.
- [ ] Resource/collection registered in HAL config, or template path registered.
- [ ] Collection class created and its embedded relation named (API).
- [ ] Redirect-after-write and flash message wired (templated).
- [ ] Sort whitelist and limit clamp present in the service.
- [ ] Errors thrown as typed exceptions with catalogue messages.
- [ ] Test asserts the body or rendered output, not only the status code.
