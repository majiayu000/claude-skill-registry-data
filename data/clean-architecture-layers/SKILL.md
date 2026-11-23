---
name: clean-architecture-layers
description: The dependency rule and what belongs in each layer (Application, Infrastructure, Presentation) of this Clean Architecture solution. Use when deciding where new code goes, adding a project reference, or reviewing a change that crosses layers.
metadata:
  scope: shared
---

# Clean architecture layers

## The rule

Three projects, and dependencies only point inwards. Application knows nothing about the database, HTTP or any framework. Infrastructure implements the interfaces Application declares. Presentation wires everything together and turns use cases into endpoints.

```
Presentation ──► Application ◄── Infrastructure
      └───────────────────────────────►┘  (startup wiring only)
```

| Layer | Holds | Never holds |
| --- | --- | --- |
| `src/Application` | Commands, queries, handlers, validators, entities (records), repository interfaces, paging, exceptions, pipeline behaviours | EF Core, ASP.NET Core, Serilog, anything about HTTP or SQL |
| `src/Infrastructure` | `DbContext`, database models, EF configuration, migrations, the repository, Mapperly mappers, sample data, `AddInfrastructure()` | Business rules, validation, HTTP types |
| `src/Presentation` | Endpoints, tools, resolvers or function handlers, request and response models, exception-to-response mapping, API documentation, authentication, health check endpoints, startup | Database access, business rules |

Infrastructure keeps its types `internal`. The only public surface is `AddInfrastructure()`, `AddInfrastructureHealthChecks()` and `InitialiseInfrastructure()` in `src/Infrastructure/DependencyInjection.cs`.

## Steps

1. Is it a rule about the domain (what's valid, what exists, what a use case does)? It goes in Application.
2. Is it about how data is stored or fetched? Infrastructure, behind an interface in Application (`IMoviesRepository`, `IAuthorsRepository`, `IReviewsRepository`).
3. Is it about how a caller talks to us (routes, status codes, JSON, tokens)? Presentation.
4. Need a new dependency between projects? Only Presentation → Application, Presentation → Infrastructure and Infrastructure → Application are allowed. Tests reference the layer they test.

## Example

The handler depends on an interface, not on EF Core:

```csharp
// src/Application/Movies/Queries/GetMovies/GetMoviesHandler.cs
public class GetMoviesHandler(IMoviesRepository repository) : IRequestHandler<GetMoviesQuery, Page<MovieSummary>>
```

`EntityFrameworkMovieReviewsRepository` in Infrastructure implements all three repository interfaces, and `AddInfrastructure()` registers it for each.

## Don't

- Reference `Microsoft.EntityFrameworkCore` or `Microsoft.AspNetCore.*` from Application.
- Return database models (`Infrastructure/.../Models`) from the repository. Map them to Application entities first (`mapping-with-mapperly`).
- Put validation in an endpoint. It belongs in an Application validator (`validation`).
- Make an Infrastructure type `public` so Presentation can use it. Add what's needed to `DependencyInjection.cs` instead.

## Check

``` bash
dotnet build
grep -rn "EntityFrameworkCore\|AspNetCore" src/Application --include=*.cs --include=*.csproj   # expect nothing
```
