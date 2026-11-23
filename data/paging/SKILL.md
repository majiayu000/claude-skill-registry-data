---
name: paging
description: Offset paging for every list (offset, limit, totalCount, Page of T), its defaults and limits, and stable ordering. Use when adding or changing anything that returns a list.
metadata:
  scope: shared
---

# Paging

## The rule

Every list is paged with an offset and a limit, and no endpoint returns an unbounded list. A repository is asked for a `PageRequest(Offset, Limit)` and returns a `Page<T>(Items, Offset, Limit, TotalCount)`, both from `src/Application/Common/Paging/`. Application owns that contract; Infrastructure turns it into `Skip` and `Take`, and each presentation maps it to and from its own wire shape. The default limit is `Paging.DefaultLimit` (10) and the maximum is `Paging.MaxLimit` (50). To get the next page, a caller adds the limit to the offset.

Lists return summaries (`MovieSummary`, `AuthorSummary`) worked out in SQL, not full entities with their children. A by-id query returns the full entity with all its children. That is a deliberate limit of the sample data model: when a parent can have many children, return its summary and page the children through their own list query instead.

When one response holds a page of parents and each one needs its children, ask for the children of the whole page in one trip with `GetReviewsForMoviesQuery` or `GetReviewsForAuthorsQuery`. They take at most `Paging.MaxLimit` ids, which is one page, and return an entry for every id. GraphQL uses them in its DataLoaders and MCP uses them for `includeReviews`. The REST templates don't call them, because their lists return summaries and a by-id query loads its children with the parent, but they stay in Application so the shared layers match in every template.

## Steps

1. Give the query `Offset` (default 0) and `Limit` (default `Paging.DefaultLimit`) properties, plus an optional `Query` search term if the list can be searched.
2. Validate them with `ValidOffset()`, `ValidLimit()` and `ValidSearchTerm()` (`validation`).
3. Give the repository method a `PageRequest page` parameter after any filters, and have it return `Page<T>`. Count before you skip and take.
4. Order by something that makes a stable order, ending with the id, so a row never shows up on two pages.
5. The handler passes the page through: `return await repository.GetMovies(request.Query, new PageRequest(request.Offset, request.Limit), cancellationToken);`

## Example

```csharp
// src/Infrastructure/Databases/MovieReviews/EntityFrameworkMovieReviewsRepository.cs
var totalCount = await movies.CountAsync(cancellationToken);

var result = await movies
    .OrderBy(m => m.Title)
    .ThenBy(m => m.Id)
    .Skip(page.Offset)
    .Take(page.Limit)
    .Select(m => new
    {
        m.Id,
        m.Title,
        ReviewCount = m.Reviews.Count,
        AverageStars = m.Reviews.Average(r => (double?)r.Stars)
    })
    .ToListAsync(cancellationToken);

return new([.. result.Select(m => new ApplicationMovieSummary(m.Id, m.Title, m.ReviewCount, RoundStars(m.AverageStars)))], page.Offset, page.Limit, totalCount);
```

## Don't

- Add an endpoint or query that returns every row.
- Use cursors or page numbers. Offset and limit everywhere; a presentation layer that needs cursors (GraphQL connections) wraps the offset.
- Return a tuple or a bare list and build the page in the handler.
- Order only by a column that can repeat, such as a title.
- `Include` child collections on a list just to count or average them. Project the numbers in SQL.

## Check

``` bash
dotnet test --filter "FullyQualifiedName~GetMovies|FullyQualifiedName~GetAuthors|FullyQualifiedName~GetReviews"
```
