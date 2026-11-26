---
name: shirakaba-audit-queries
description: Find and fix N+1 queries and other excess statements in a Shirakaba application using StatementLog, the shirakaba/phpstan query-in-loop check and ORM eager loading. Use when asked about slow endpoints, query counts or N+1 problems in a project that uses shirakaba/database.
---

# Audit database queries in a Shirakaba application

Read the testing chapter (`vendor/shirakaba/docs/guide/09-testing.md`) and the entities section
of `vendor/shirakaba/docs/guide/06-database.md` first.

1. **Find loops statically.** Enable `reportQueriesInLoops: true` under `parameters.shirakaba`
   in `phpstan.neon` and run `vendor/bin/phpstan analyse`. Every database call inside a loop
   is reported.
2. **Measure per request.** In a test, add a `StatementLog` observer to the application
   (`$app->observe($log)`), call the endpoint with `TestClient`, and read `$log->last()` (the
   statements of the last request), `$log->repeated()` and `$log->describe()`.
3. **Fix the shape, not the symptom.**
   - Related rows: request them with `with('user', 'files', 'reply.user')` and read them
     through a projection with `into()`. Each relation level is one `IN` query, and leaf
     belongs-to and many-to-many relations share queries across paths.
   - Counts: `withCount('comments')` and an `int $commentsCount` parameter.
   - Values from other tables: a `#[Computed]` parameter filled by the `into()` callback,
     which receives every loaded entity at once (nested ones as a second list) so one query
     serves the page.
   - Filters across relations: `whereHas()` instead of loading and filtering in PHP.
4. **Pin the result.** Assert the statement count in the test, with the reason:
   `self::assertLessThanOrEqual(5, count($log->last()), $log->describe())`.

## Verify

- `vendor/bin/phpstan analyse` reports no query in a loop
- the test with the pinned statement count passes, and the rest of the suite still passes
