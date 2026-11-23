---
name: data-access-ef-core
description: How the repository reads and writes the SQLite database with EF Core - scoped DbContext, no tracking by default, SQL projections for lists, set-based updates and deletes, and safe LIKE searches. Use when adding or changing a repository method or a query.
metadata:
  scope: shared
---

# Data access with EF Core

## The rule

One repository, `EntityFrameworkMovieReviewsRepository` in `src/Infrastructure/Databases/MovieReviews/`, implements every repository interface from Application. It and `MovieReviewsDbContext` are scoped: one per request, never shared between threads. The context doesn't track queries (`QueryTrackingBehavior.NoTracking` in `AddInfrastructure`), because nothing loads an entity to change it. Lists are projected in SQL. Updates and deletes are set-based and are their own existence check. The repository returns Application entities, never database models.

## Steps

1. Add the method to the Application interface first (`IMoviesRepository` and friends), taking a `CancellationToken` last.
2. Implement it in the matching `#region` of the repository, as `public async Task<...>` like every other method.
3. Reads: start from `this.context.<Set>`, filter, then either
   - **a list**: take a `PageRequest page`, count, order (ending with the id), `Skip(page.Offset)`, `Take(page.Limit)`, `Select` the summary fields so SQL does the counting and averaging, and return `new Page<T>(items, page.Offset, page.Limit, totalCount)` (`paging`), or
   - **one entity**: `Include` what the entity needs, `FirstOrDefaultAsync`, then map with `this.mapper.ToDomain(...)` (`mapping-with-mapperly`).
4. Writes:
   - **create**: build the model, set `DateCreated` and `DateModified` from `this.timeProvider.GetUtcNow().UtcDateTime`, `Add`, `SaveChangesAsync`, then read it back with its includes.
   - **update**: `Where(...).ExecuteUpdateAsync(setters => ...)`, always setting `DateModified`. No rows changed means not found, so return `null`; otherwise read the entity back and return it.
   - **delete**: `Where(...).ExecuteDeleteAsync(...)`, returning whether a row was deleted.
   - Don't check first. The handler turns `null` or `false` into `NotFoundException` (`errors-and-exceptions`).
   - New rows get a version 7 GUID from `Version7GuidValueGenerator`, set up for every model in `EntityConfiguration<T>`. Each model needs its own configuration class, even an empty one, or it gets random GUIDs.
5. Text search uses `EF.Functions.Like` with the `ContainsPattern` helper, which escapes `%`, `_` and `\`.
6. Add repository tests (`integration-tests`).

## Example

```csharp
// src/Infrastructure/Databases/MovieReviews/EntityFrameworkMovieReviewsRepository.cs
public async Task<ApplicationReview?> UpdateReview(Guid id, int stars, CancellationToken cancellationToken)
{
    var now = this.timeProvider.GetUtcNow().UtcDateTime;

    // The update is the existence check: no rows changed means there's no such review.
    var updated = await this.context.Reviews
        .Where(r => r.Id == id)
        .ExecuteUpdateAsync(
            setters => setters
                .SetProperty(r => r.Stars, stars)
                .SetProperty(r => r.DateModified, now),
            cancellationToken);

    return updated == 0 ? null : await this.GetReviewById(id, cancellationToken);
}
```

```csharp
if (!string.IsNullOrWhiteSpace(query))
{
    var pattern = ContainsPattern(query);

    movies = movies.Where(m => EF.Functions.Like(m.Title, pattern, EscapeCharacter));
}
```

## Don't

- Register the `DbContext` or repository as a singleton. A shared context fails under concurrent requests.
- Use `string.Contains(value, StringComparison.OrdinalIgnoreCase)` in a query. EF Core can't translate it; use the `LIKE` helper.
- Use `DateTime.UtcNow`. Use the injected `TimeProvider` so tests can fix the clock.
- `Include` children on a list query to count them.
- Load an entity, change it and `SaveChanges` to update one column. Use `ExecuteUpdateAsync`.
- Add `AsNoTracking()` to a query. It's already the default.
- Call an `Exists` method before an update or delete.
- Return a database model or `IQueryable` from the repository.

## Check

``` bash
dotnet test tests/Infrastructure.Tests.Integration
```
