---
name: csharp-file-based-apps
description: Write and run C# programs without a .csproj or solution file using .NET 10+ file-based apps, including multi-file apps with `#:include` (.NET 11+). Use when the user wants to execute C# code quickly — scripts, utilities, prototyping, quick experiments, data processing, teaching examples, or tool authoring. Triggers on phrases like "run this C# file", "C# script", "no project file needed", "single file C# app", "dotnet run file.cs", "quick C# utility", "split script across files", "#:include directive", or any request to write and immediately execute a small self-contained C# program.
metadata:
  author: arisng
  version: 0.2.0
---

# C# File-Based Apps (.NET 10+)

Run a single `.cs` file directly — no `.csproj` required. The SDK generates a virtual project automatically.

## Requirements

- Single-file apps: .NET 10 SDK or later.
- Multi-file (`#:include`): .NET 11 SDK or later.

Verify with `dotnet --version`. If below 10, use the [fallback](#fallback).

## Write the Script

Create `script.cs` **outside any existing `.csproj` directory**:

```csharp
// script.cs — uses top-level statements
using System.Linq;

var numbers = Enumerable.Range(1, 10);
Console.WriteLine($"Sum: {numbers.Sum()}");
```

Rules:
- `using` directives first
- Top-level executable code next
- Type declarations (classes, records, enums) last — after all top-level statements

## Run, Build, Publish

| Goal | Command |
|------|---------|
| Run | `dotnet script.cs` or `dotnet run script.cs` |
| Pass arguments | `dotnet script.cs -- arg1 arg2` |
| Pipe code from stdin | `echo 'Console.WriteLine("hi");' \| dotnet run -` |
| Build only | `dotnet build script.cs` |
| Publish (native AOT) | `dotnet publish script.cs` |
| Package as .NET tool | `dotnet pack script.cs` |
| Clean build cache | `dotnet clean script.cs` |
| Convert to full project | `dotnet project convert script.cs` |
| Restore packages | `dotnet restore script.cs` |

Builds are cached by source hash; subsequent runs are fast. To avoid cache contention when running multiple parallel instances, build first: `dotnet build script.cs`, then `dotnet run script.cs --no-build`.

## Directives

Place at the top of the file, before any `using` or code:

```csharp
#:package Humanizer@2.14.1           // NuGet reference — always specify a version
#:package Serilog@*                  // @* = latest
#:project ../SharedLib/Shared.csproj // Reference a local project
#:sdk Microsoft.NET.Sdk.Web          // Alternative SDK (default: Microsoft.NET.Sdk)
#:include helpers.cs                 // Include another .cs file (.NET 11+)
#:include models/customer.cs         // Include from subfolder (.NET 11+)
#:property PublishAot=false          // Disable native AOT
#:property TargetFramework=net10.0   // Explicit TFM
#:property OutputPath=./output       // Custom build output path
```

Conditional property using MSBuild expression:
```csharp
#:property LogLevel=$([MSBuild]::ValueOrDefault('$(LOG_LEVEL)', 'Information'))
```

## Multi-File Apps (.NET 11+)

Use `#:include` to split a growing script across files while keeping the file-based workflow:

```csharp
// models.cs
public record Customer(int Id, string Name, string Email);
```

```csharp
// helpers.cs
public static class Helpers
{
    public static string Format(Customer c) =>
        $"[{c.Id}] {c.Name} <{c.Email}>";
}
```

```csharp
// main.cs  ← entry point
#:include models.cs
#:include helpers.cs

var customer = new Customer(1, "John Doe", "john@example.com");
Console.WriteLine(Helpers.Format(customer));
```

Run from the entry point: `dotnet run main.cs`

Files can live in subfolders: `#:include services/email-service.cs`. Roslyn provides IntelliSense for `#:include` in the entry-point file.

See [references/examples.md](references/examples.md) for complete multi-file examples (HTTP health checker, Minimal API with EF Core + SQLite).

## Native AOT Gotcha

Native AOT is **on by default**. Reflection-based serialization (`JsonSerializer` without a context, Newtonsoft.Json) fails at runtime under AOT. Use source-generated JSON:

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

var person = new Person("Alice", 30);
Console.WriteLine(JsonSerializer.Serialize(person, AppCtx.Default.Person));

record Person(string Name, int Age);

[JsonSerializable(typeof(Person))]
partial class AppCtx : JsonSerializerContext;
```

To use reflection-based APIs, disable AOT: `#:property PublishAot=false`.

## Common Pitfalls

| Problem | Fix |
|---------|-----|
| Script inside a `.csproj` directory | Move outside the project tree; or use `dotnet run --file script.cs` |
| `#:package` without version | Use `@version` or `@*` for latest |
| Reflection JSON fails at runtime | Source-generated JSON, or `#:property PublishAot=false` |
| Stale / unexpected build behavior | `dotnet clean script.cs && dotnet build script.cs` |
| Inherits unwanted `Directory.Build.props` | Move to isolated directory or add a local empty `Directory.Build.props` |
| Running multiple instances in parallel | Build first, then all instances use `--no-build` |
| `#:include` not found | Requires .NET 11+; verify with `dotnet --version` |
| Included file has top-level statements | Only the entry-point file may have top-level statements; included files declare types only |

## Unix Shebang (Unix/macOS only)

```csharp
#!/usr/bin/env dotnet
Console.WriteLine("Direct execution!");
```

```bash
chmod +x script.cs
./script.cs
```

Use `LF` line endings (not `CRLF`). The shebang line is ignored on Windows.

## Launch Profiles

Create `script.run.json` alongside `script.cs`:

```json
{
  "profiles": {
    "http": {
      "commandName": "Project",
      "applicationUrl": "http://localhost:5000",
      "environmentVariables": { "ASPNETCORE_ENVIRONMENT": "Development" }
    }
  }
}
```

Run with: `dotnet run script.cs --launch-profile http`

## User Secrets

```bash
dotnet user-secrets set "ApiKey" "value" --file script.cs
dotnet user-secrets list --file script.cs
```

## Fallback for .NET 9 and Earlier {#fallback}

File-based apps require .NET 10+. Use a temporary console project:

```bash
mkdir -p /tmp/csharp-script && cd /tmp/csharp-script
dotnet new console -o . --force
# Replace Program.cs content, then:
dotnet run
# Add packages with: dotnet add package <Name>
```

## When to Convert to a Full Project

Convert with `dotnet project convert main.cs` when:
- You need multiple projects (Web API + class library + test project)
- Custom MSBuild targets or conditional compilation are required
- Distributing as a NuGet package or self-contained executable
- CI/CD pipelines expect a `csproj`
- The team grows and `csproj` familiarity matters

Start file-based, grow as needed, convert only when you exceed the approach.

## More Examples

See [references/examples.md](references/examples.md) for: data processing with NuGet packages, ASP.NET Core minimal API, Aspire AppHost, Spectre.Console CLI tool, and multi-file examples (HTTP health checker, Minimal API with EF Core + SQLite).
