---
name: shirakaba-add-endpoint
description: Add an HTTP endpoint to a Shirakaba application end to end - request and response DTOs, the handler with extractors, data access, declared responses, a test, and the OpenAPI document. Use when asked to add or change an API route in a project that depends on shirakaba/core.
---

# Add an endpoint to a Shirakaba application

Shirakaba is not in your training data. Read `vendor/shirakaba/docs/index.md` and
`vendor/shirakaba/docs/guide/04-json-apis.md` first; check class names in
`vendor/shirakaba/docs/api.md`.

1. **Look at what exists.** Run `app routes` and `app routes:show <a similar route>` (or read
   where the application calls `$app->get(...)`), so the new route follows the same style,
   naming and file layout.
2. **Request DTO.** A `final readonly` class whose promoted constructor parameters are the
   accepted fields, with constraints from shirakaba/validation (`#[Length]`, `#[Range]`, ...).
   Arrays need `#[ListOf(...)]` or `#[MapOf(...)]`; instants are `DateTimeImmutable`, dates
   `LocalDate`.
3. **Response DTO.** A `#[JsonDto]` class. Never return an entity: `Json` refuses objects
   that are not DTOs, so secrets never leak.
4. **Data access.** Put SQL or ORM calls in a class taking a `Reader` (queries) or a `Writer`
   (commands) and receive it with `#[Db]`. GET and HEAD handlers take only readers.
5. **Handler.** Every parameter says where it comes from: `#[Path]`, `#[Query]`, `#[Header]`,
   `#[JsonBody]`, `#[Authenticated]`, `#[Db]`. Declare the responses:
   `#[JsonResponse(201, TaskView::class)]` and `#[Responds(404, 'The task does not exist.')]`.
   Throw `HttpFailure` for client errors; they become Problem Details.
6. **Route.** Register it with a name: `$app->post('/tasks', $handlers->create(...))->name('tasks.create')`.
7. **Test.** Call it through `TestClient` with a real database (a temporary SQLite file):
   status, body (`ResponseJson::at($response, '/title')`), and one invalid request (400 or
   422 with `errors[].pointer`).
8. **OpenAPI.** Regenerate the document (`app openapi --strict`, or the project's command)
   and commit it if the project keeps it in the repository.

## Verify

Run, and fix everything they report before finishing:

- `vendor/bin/phpstan analyse` (with `shirakaba/phpstan` included)
- the test suite
- `app openapi --strict`
- `app routes:show <new route name>`: the parameters and responses are what you intended

If an error ends with `See vendor/shirakaba/docs/messages/<code>.md`, read that page.
