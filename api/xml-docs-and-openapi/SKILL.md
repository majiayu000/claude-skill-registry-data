---
name: xml-docs-and-openapi
description: How XML documentation comments on requests, entities and presentation members become the API documentation (OpenAPI and Scalar, GraphQL descriptions, MCP tool descriptions), and the generator gotchas. Use when adding or changing a public type, property, endpoint or request model.
metadata:
  scope: shared
---

# XML docs and API documentation

## The rule

The API documentation is generated from XML comments, so the comments are the documentation. `GenerateDocumentationFile` is on for every project. Missing comments (CS1591) aren't build errors, but every request, entity and public presentation member has them anyway.

Where the comments end up:

| Comment on | Shows up as |
| --- | --- |
| Application request properties and entity record `<param>` tags | Schema and field descriptions (OpenAPI, GraphQL) |
| Endpoint or tool `<summary>`, `<remarks>`, `<param>`, `<response>` | Operation summary, description, parameter text and response codes |
| Request model `<example>` | The example value in the API reference |

## Steps

1. Requests: a `<summary>` on the class saying what the use case does, and one on each property saying what it means and its allowed values.
2. Entity records: a `<summary>` on the record and a `<param>` for each positional parameter.
3. Write for the person calling the API: plain sentences, units and ranges, what an empty value means.
4. Endpoint and tool comments are covered by `expose-a-use-case` for this template.
5. Run the app and read the result in the API reference before you call it done.

## Example

```csharp
// src/Application/Movies/Entities/MovieSummary.cs
/// <summary>
/// A movie in a list, with how many reviews it has and their average star rating instead of the reviews themselves.
/// </summary>
/// <param name="Id">The unique identifier of the movie.</param>
/// <param name="Title">The title of the movie.</param>
/// <param name="ReviewCount">The number of reviews written about the movie.</param>
/// <param name="AverageStars">The average star rating to one decimal place, or null when the movie has no reviews.</param>
public record MovieSummary(Guid Id, string Title, int ReviewCount, double? AverageStars);
```

## Don't

- Document an injected `[FromServices] ISender sender` parameter. The .NET 10 OpenAPI generator puts that text on the request body instead. Leave it undocumented; `NoWarn 1573` in the Presentation project allows that.
- Copy the member name as the summary ("Gets the title").
- Leave `TODO` or placeholder comments.

## Check

``` bash
dotnet build
dotnet test --filter "FullyQualifiedName~OpenApi"
```
