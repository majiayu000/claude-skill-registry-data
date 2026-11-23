---
name: json-serialization
description: How this Minimal API reads and writes JSON with System.Text.Json - the one set of options in UseApiDefaults, the source-generated AppJsonSerializerContext, which types it must list, and how tests use the same options. Use when adding a request or response type, changing how JSON looks, or when a value serialises differently than expected.
metadata:
  scope: presentation
---

# JSON serialization (Minimal API)

## The rule

Every request and response goes through System.Text.Json with one set of options, defined once in `UseApiDefaults()` (`src/Presentation/Serialization/JsonSerializerOptionsExtensions.cs`):

| Setting | Effect |
| --- | --- |
| `PropertyNamingPolicy = CamelCase` | `averageStars`, not `AverageStars` |
| `PropertyNameCaseInsensitive = true` | Request bodies are read whatever the case of their property names |
| `DefaultIgnoreCondition = WhenWritingNull` | Null properties are left out of responses |
| `NumberHandling = Strict` | Numbers must be JSON numbers. `"5"` for an `int` is refused, and OpenAPI shows `integer`, not `integer \| string` |
| `JsonStringEnumConverter(CamelCase)` | Enums are written and read as camelCase strings |

Startup applies those options to the Minimal API's `JsonOptions` and puts `AppJsonSerializerContext` (`src/Presentation/Serialization/AppJsonSerializerContext.cs`) first in the resolver chain, so listed types use generated code instead of reflection. The integration tests build their options with the same `UseApiDefaults()`, so they read responses exactly as a client would.

Responses are trees: lists return summaries, and an entity holds only the flat records it needs. There's no cycle handling, so a cycle fails loudly instead of being quietly cut.

## Steps

1. Add every new request and response type to `AppJsonSerializerContext` with `[JsonSerializable(typeof(...))]`, including the `Page<T>` and `List<T>` forms you return.
2. Change how JSON looks only in `UseApiDefaults()`. Keep the `[JsonSourceGenerationOptions]` on the context matching it.
3. Add a test in `tests/Presentation.Tests.Unit/Serialization/JsonSerializerOptionsExtensionsTests.cs` for any setting you change.
4. Never let a response type refer back to its parent. Return a flat record instead (`ReviewAuthor`, `ReviewedMovie`).

## Example

```csharp
// src/Presentation/Extensions/WebApplicationBuilderExtensions.cs
_ = builder.Services.Configure<JsonOptions>(options =>
    options.SerializerOptions.UseApiDefaults().TypeInfoResolverChain.Insert(0, AppJsonSerializerContext.Default));
```

```csharp
// tests/Presentation.Tests.Integration/Extensions/JsonSerializerExtensions.cs
private static readonly JsonSerializerOptions Options = new JsonSerializerOptions().UseApiDefaults();
```

## Don't

- Set serializer options anywhere but `UseApiDefaults()`, including in tests.
- Add `ReferenceHandler.IgnoreCycles` or `Preserve` to hide a cycle. Change the response shape.
- Use Newtonsoft.Json.
- Use `[JsonPropertyName]` to rename one property. The naming policy names them all.

## Check

``` bash
dotnet test tests/Presentation.Tests.Unit --filter "FullyQualifiedName~Serialization"
dotnet test tests/Presentation.Tests.Integration
```
