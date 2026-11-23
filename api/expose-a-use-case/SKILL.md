---
name: expose-a-use-case
description: How to put an Application use case on a Minimal API endpoint - endpoint groups, static handler methods, TypedResults, Produces metadata, XML docs for Scalar, JSON source generation and tests. Use when adding or changing an endpoint in this Minimal API.
metadata:
  scope: presentation
---

# Expose a use case (Minimal API)

## The rule

Endpoints live in `src/Presentation/Endpoints/<Feature>Endpoints.cs`, one static class per resource. A `Map<Feature>Endpoints` extension maps a route group; each endpoint is a `public static async` method that builds the Application request, sends it through `ISender` and returns a `TypedResults` value. The method's XML comments become the operation's documentation in Scalar. Endpoints contain no logic: validation, not-found and everything else happen in Application, and `ApplicationExceptionHandler` turns exceptions into problem details.

## Steps

1. Add the use case first (`add-a-use-case`).
2. In the feature's endpoints class, map the route on the group and describe every response:

   ```csharp
   _ = root.MapGet("/{id:guid}", GetReviewById)
       .WithName(nameof(GetReviewById))
       .Produces<Entities.Review>()
       .ProducesValidationProblem()
       .ProducesProblem(StatusCodes.Status404NotFound)
       .ProducesProblem(StatusCodes.Status500InternalServerError);
   ```

3. Write the handler method: `[FromRoute]`, `[FromQuery]` and `[FromBody]` on every input, `[FromServices] ISender sender`, then `CancellationToken cancellationToken`. Optional query parameters with defaults go last.
4. Return the narrowest `TypedResults` type: `Ok<T>`, `CreatedAtRoute<T>` (with the by-id route name) for creates, `NoContent` for updates and deletes.
5. Bodies use a request class in `src/Presentation/Requests/` with XML docs and `<example>` values. Map it to the command in the endpoint.
6. Add every new request or response type to `AppJsonSerializerContext` (`src/Presentation/Serialization/`) with `[JsonSerializable(typeof(...))]`, including `Page<T>` and `List<T>` forms (`json-serialization`).
7. Document the method: `<summary>` (short, title case, shown as the operation name), `<remarks>` with a sentence or two and a sample request, `<param>` for each input except `sender` and the token, and a `<response code="...">` for each status.
8. A new endpoints class is mapped in `WebApplicationExtensions.ConfigureApplication` under `#region MinimalApi`.
9. Add a sample request for the endpoint to `src/Presentation/Presentation.http`.
10. Test it twice: a unit test calling the static method with a faked `ISender` (`tests/Presentation.Tests.Unit/Endpoints/`), and an integration test making the real request (`tests/Presentation.Tests.Integration/Endpoints/`, see `presentation-integration-tests`). Cover every documented status code (`test-design`).

## Example

```csharp
// src/Presentation/Endpoints/ReviewEndpoints.cs
public static async Task<CreatedAtRoute<Entities.Review>> CreateReview(
    [FromBody] CreateReviewRequest request,
    [FromServices] ISender sender,
    CancellationToken cancellationToken)
{
    var response = await sender.Send(new Commands.CreateReview.CreateReviewCommand
    {
        AuthorId = request.AuthorId,
        MovieId = request.MovieId,
        Stars = request.Stars
    }, cancellationToken);

    return TypedResults.CreatedAtRoute(response, nameof(GetReviewById), new { id = response.Id });
}
```

## Don't

- Use `Results.Ok(...)` or return `IResult`. `TypedResults` with a concrete return type gives OpenAPI the real response type.
- Catch exceptions or check `null` in an endpoint.
- Document the `sender` parameter (`xml-docs-and-openapi`).
- Forget `[JsonSerializable]` for a new type; serialization then falls back to reflection.
- Put a route's group-level settings (`RequireAuthorization`, `WithTags`) on single endpoints.

## Check

``` bash
dotnet test tests/Presentation.Tests.Unit
dotnet test tests/Presentation.Tests.Integration
dotnet run --project ./src/Presentation   # then read the endpoint at http://localhost:7310/scalar
```
