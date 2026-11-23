---
name: csharp-house-style
description: The house C# style enforced by .editorconfig and the build - this. qualification, usings inside file-scoped namespaces, discards, regions, primary constructors, nullable and naming. Use whenever writing or reviewing C# in this solution.
metadata:
  scope: shared
---

# C# house style

## The rule

`.editorconfig` holds the style and the build enforces it (`EnforceCodeStyleInBuild`, `AnalysisLevel` `latest-recommended`, `TreatWarningsAsErrors`, all in `Directory.Build.props`). If the build is clean and `dotnet format --verify-no-changes` passes, the style is right. These are the parts that differ from most .NET code, so they're the ones people trip on.

| Rule | Looks like |
| --- | --- |
| File-scoped namespace first, then `using` directives inside it | `namespace X.Y;` then `using Mediator;` |
| Qualify members with `this.` | `this.context.Reviews`, `this.RuleFor(...)` |
| Discard unused results with `_ =` | `_ = services.AddScoped<...>();` |
| `var` everywhere | `var result = ...` |
| Braces on every `if`, Allman style | opening brace on its own line |
| Block bodies for methods and constructors | no `=> expression` methods |
| Primary constructors for injected services | `public class XHandler(IRepo repository)` |
| `#region` to group long classes | `#region Authors` ... `#endregion Authors` |
| Nullable reference types on | `string?` when null is a real value |
| Collection expressions | `[.. result.Select(...)]`, `List<T> x = [];` |
| Async methods return `ValueTask` in handlers, `Task` in repositories | as the interfaces declare |

Naming: PascalCase types and members, camelCase locals and parameters, no underscores on fields (`this.` tells you it's a field). Interfaces start with `I`.

## Steps

1. Write the code to match a neighbouring file.
2. Run `dotnet format` to fix whitespace and using order.
3. Run `dotnet build` and fix every warning. Nullable warnings are fixed with real null handling, not `!`, except for EF navigation properties (`= null!`).

## Don't

- Move usings above the namespace or drop `this.` to match another codebase.
- Add `#pragma warning disable` or `<NoWarn>` to quiet an analyser.
- Use `_camelCase` fields.
- Leave unused usings; IDE0005 fails the build.

## Check

``` bash
dotnet format --verify-no-changes
dotnet build
```
