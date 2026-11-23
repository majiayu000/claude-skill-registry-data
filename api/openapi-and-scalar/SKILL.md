---
name: openapi-and-scalar
description: How this Minimal API builds its OpenAPI document and serves the Scalar API reference - AddOpenApi, the document and operation transformers, the bearer scheme when authentication is on, the Scalar options, and the tests that read the generated document. Use when changing the API description, tags, security scheme, Scalar settings, or when the API reference looks wrong.
metadata:
  scope: presentation
---

# OpenAPI and Scalar (Minimal API)

## The rule

The OpenAPI document is generated at runtime by `Microsoft.AspNetCore.OpenApi` and served at `/openapi/v1.json`. Scalar (`Scalar.AspNetCore`) renders it at `/scalar`. Operation and schema text comes from XML comments (`xml-docs-and-openapi`); everything else is set by transformers in `src/Presentation/OpenApi/`.

| Transformer | Adds |
| --- | --- |
| `DocumentInfoTransformer` | Title (with the environment name), description, contact, licence, external docs and the tag descriptions |
| `BearerSecurityTransformer` | Only in a solution with authentication, and only when `Authentication:Authority` is set: the `Bearer` security scheme, a security requirement and a `401` response on every operation that needs a token |

Scalar is set up in `WebApplicationExtensions.ConfigureApplication` with the title, C# `HttpClient` as the default code sample, and its developer tools, agent, MCP and telemetry features turned off.

`tests/Presentation.Tests.Integration/OpenApi/OpenApiDocumentTests.cs` reads the generated document and fails if an operation has no summary, description, sample request or parameter descriptions, or a schema property has no description.

## Steps

1. A new tag needs a `CreateTag(...)` line in `DocumentInfoTransformer` with a one-sentence description, and `WithTags` on the endpoint group.
2. Something every operation needs goes in an operation transformer; something about the whole API goes in a document transformer. Register it in `AddOpenApi` in `WebApplicationBuilderExtensions`.
3. Transformers are classes implementing `IOpenApiDocumentTransformer` or `IOpenApiOperationTransformer`, `sealed`, with XML docs. Unit test them in `tests/Presentation.Tests.Unit/OpenApi/`.
4. When you add an endpoint, update the operation count in `GetOpenApiDocument_ShouldDescribe_EveryOperation`.
5. Run the app and read the result at <http://localhost:7310/scalar>.

## Example

```csharp
// src/Presentation/Extensions/WebApplicationBuilderExtensions.cs
_ = builder.Services.AddOpenApi(options =>
{
    _ = options.AddDocumentTransformer<DocumentInfoTransformer>();

    // Only with --include-auth.
    if (authentication.Enabled)
    {
        _ = options.AddDocumentTransformer<BearerSecurityTransformer>();
        _ = options.AddOperationTransformer<BearerSecurityTransformer>();
    }
});
```

```csharp
// src/Presentation/Extensions/WebApplicationExtensions.cs
_ = app.MapOpenApi();
_ = app.MapScalarApiReference(options => options
    .WithTitle("CleanMinimalApi API")
    .WithDefaultHttpClient(ScalarTarget.CSharp, ScalarClient.HttpClient)
    .HideDeveloperTools()
    .DisableAgent()
    .DisableMcp()
    .DisableTelemetry());
```

## Don't

- Add Swashbuckle or NSwag. The built-in generator and Scalar replace them.
- Describe operations with `WithSummary` or `WithDescription`. The XML comments are the one source.
- Turn Scalar telemetry back on.
- Add the security scheme when authentication is off. The reference would ask for a token nobody needs.

## Check

``` bash
dotnet test --filter "FullyQualifiedName~OpenApi"
dotnet run --project ./src/Presentation   # then open http://localhost:7310/scalar
```
