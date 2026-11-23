---
name: add-a-use-case
description: How to add a command or query to the Application layer as a vertical slice (request, handler, validator, tests) using source-generated Mediator. Use when adding a new feature, a new query, or a new write operation.
metadata:
  scope: shared
---

# Add a use case

## The rule

Every use case is one folder holding three files: the request, its handler and its validator. Reads are queries, writes are commands. Mediator (the source-generated one, not MediatR) finds handlers at compile time, and `ValidationBehaviour` runs the validator before the handler (`mediator`).

```
src/Application/<Feature>/
├── Commands/<Verb><Thing>/   <Verb><Thing>Command.cs, ...Handler.cs, ...Validator.cs
├── Queries/Get<Thing>/       Get<Thing>Query.cs, ...Handler.cs, ...Validator.cs
├── Entities/                 records returned to callers
└── I<Feature>Repository.cs   what the handlers need from storage
```

## Steps

1. Create the folder under `Commands` or `Queries`, named for the use case (`UpdateReview`, `GetMovieById`).
2. Write the request: a class with `init` properties implementing `IRequest<TResponse>`, with an XML summary on the class and each property (`xml-docs-and-openapi`).
3. Write the validator (`validation`). Every request gets one, even if it only checks an id.
4. Write the handler with a primary constructor that takes repository interfaces. Return `ValueTask<TResponse>`. Pass the `CancellationToken` to every call (`cancellation`).
5. If the handler needs something new from storage, add it to the repository interface, then implement it in Infrastructure (`data-access-ef-core`).
6. Add tests: `tests/Application.Tests.Unit/<Feature>/<Commands|Queries>/<UseCase>/` with `<UseCase>HandlerTests.cs` and `<UseCase>ValidatorTests.cs`, covering every success and failure (`test-design`, `unit-tests`).
7. Expose it in Presentation (`expose-a-use-case`).

## Example

```csharp
// src/Application/Movies/Queries/GetMovies/GetMoviesQuery.cs
/// <summary>
/// Lists movies one page at a time, optionally only those whose title contains a search term.
/// </summary>
public class GetMoviesQuery : IRequest<Page<MovieSummary>>
{
    /// <summary>The words to look for in the title, ignoring case. Leave empty to list every movie.</summary>
    public string? Query { get; init; }

    /// <summary>The number of results to skip, 0 for the first page.</summary>
    public int Offset { get; init; }

    /// <summary>The largest number of results to return, from 1 to 50.</summary>
    public int Limit { get; init; } = Paging.DefaultLimit;
}
```

```csharp
// src/Application/Movies/Queries/GetMovies/GetMoviesHandler.cs
public class GetMoviesHandler(IMoviesRepository repository) : IRequestHandler<GetMoviesQuery, Page<MovieSummary>>
{
    public async ValueTask<Page<MovieSummary>> Handle(GetMoviesQuery request, CancellationToken cancellationToken)
    {
        var (items, totalCount) = await repository.GetMovies(request.Query, request.Offset, request.Limit, cancellationToken);

        return new Page<MovieSummary>(items, request.Offset, request.Limit, totalCount);
    }
}
```

A by-id query fetches and throws when nothing comes back:

```csharp
// src/Application/Reviews/Queries/GetReviewById/GetReviewByIdHandler.cs
var result = await repository.GetReviewById(request.Id, cancellationToken);

NotFoundException.ThrowIfNull(result, EntityType.Review);

return result;
```

## Don't

- Use MediatR. It's commercially licensed now; we use `Mediator.Abstractions` and `Mediator.SourceGenerator`.
- Put two use cases in one handler, or share a request between a read and a write.
- Return database models or `IQueryable` from a handler.
- Validate inside the handler. Rules go in the validator; the handler only checks things that need storage (does the author exist?).
- Forget the validator. A request with no rules still gets one that checks its ids.

## Check

``` bash
dotnet build
dotnet test tests/Application.Tests.Unit
```
