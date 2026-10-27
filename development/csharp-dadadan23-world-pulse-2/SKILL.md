---
name: "csharp"
description: 'Write production-ready C# and .NET code following modern best practices. Use when building .NET applications, writing async/await code, using Entity Framework Core, implementing dependency injection, configuring nullable reference types, or optimizing C# performance.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 languages: ["csharp"]
 frameworks: ["dotnet", "aspnet-core"]
 platforms: ["windows", "linux", "macos"]
---

# C# / .NET Development

> **Purpose**: Production-ready C# and .NET development standards for building secure, performant, maintainable applications. 
> **Audience**: Engineers building .NET applications with C#, ASP.NET Core, Entity Framework Core. 
> **Standard**: Follows [github/awesome-copilot](https://github.com/github/awesome-copilot) .NET development patterns.

---

## When to Use This Skill

- Building .NET applications with C#
- Writing async/await code patterns
- Using Entity Framework Core for data access
- Implementing dependency injection
- Configuring nullable reference types

## Prerequisites

- .NET 8+ SDK installed
- C# 12+ language features
- IDE with C# support

## Quick Reference

| Need | Solution | Pattern |
|------|----------|---------|
| **Async code** | Use `async`/`await` everywhere | `async Task<T> GetDataAsync()` |
| **Null safety** | Enable nullable reference types | `<Nullable>enable</Nullable>` |
| **Error handling** | Use Result types or exceptions | `try-catch` with specific types |
| **DI** | Constructor injection with interfaces | `IServiceCollection` |
| **Testing** | xUnit, NUnit, or TUnit | `[Fact]`, `[Test]` |
| **Logging** | `ILogger<T>` with structured logging | `_logger.LogInformation("User {UserId}", id)` |

---

## C# Language Version

**Current**: C# 14 (.NET 10+) 
**Minimum**: C# 8 (.NET Core 3.1+)

### Modern C# Features (Use These)

```csharp
// File-scoped namespaces (C# 10+)
namespace MyApp.Services;

// Primary constructors (C# 12+)
public class UserService(ILogger<UserService> logger, IUserRepository repo)
{
 public async Task<User> GetUserAsync(int id) => 
 await repo.GetByIdAsync(id);
}

// Required properties (C# 11+)
public class User
{
 public required int Id { get; init; }
 public required string Name { get; init; }
}

// Raw string literals (C# 11+)
string json = """
 {
 "name": "John",
 "age": 30
 }
 """;

// Pattern matching
string GetStatus(Order order) => order switch
{
 { Status: "pending", TotalAmount: > 1000 } => "High value pending",
 { Status: "shipped" } => "In transit",
 { Status: "delivered" } => "Completed",
 _ => "Unknown"
};
```

---

## Common Pitfalls

| Issue | Problem | Solution |
|-------|---------|----------|
| **Sync over async** | Using `.Result` or `.Wait()` | Always use `await` |
| **No cancellation** | Long operations can't be cancelled | Pass `CancellationToken` |
| **N+1 queries** | Loading related data in loop | Use `.Include()` for eager loading |
| **Magic strings** | Hardcoded strings everywhere | Use `nameof()` or constants |
| **No null checks** | NullReferenceException | Enable nullable reference types |
| **Poor logging** | Unstructured log messages | Use structured logging with parameters |

---

## Resources

- **Official Docs**: [learn.microsoft.com/dotnet](https://learn.microsoft.com/dotnet)
- **C# Guide**: [learn.microsoft.com/csharp](https://learn.microsoft.com/csharp)
- **ASP.NET Core**: [learn.microsoft.com/aspnet/core](https://learn.microsoft.com/aspnet/core)
- **EF Core**: [learn.microsoft.com/ef/core](https://learn.microsoft.com/ef/core)
- **Testing**: [xunit.net](https://xunit.net), [nunit.org](https://nunit.org)
- **Awesome Copilot**: [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot)

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md)

**Last Updated**: January 27, 2026

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`scaffold-solution.ps1`](scripts/scaffold-solution.ps1) | Create .NET solution with API/Core/Infrastructure + xUnit tests | `./scripts/scaffold-solution.ps1 -Name MyApp [-Framework net9.0]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Deadlock with async code | Use async/await all the way up, never call .Result or .Wait() on async methods |
| EF Core migration errors | Run dotnet ef migrations list to check state, recreate if corrupted |
| Nullable warnings everywhere | Enable Nullable in .csproj, fix warnings incrementally |

## References

- [Async Nullable Di](references/async-nullable-di.md)
- [Efcore Errors Testing](references/efcore-errors-testing.md)
- [Logging Perf Security](references/logging-perf-security.md)