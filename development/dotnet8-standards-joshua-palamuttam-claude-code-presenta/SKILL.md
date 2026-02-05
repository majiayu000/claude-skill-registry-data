---
name: dotnet8-standards
description: C# 12 and .NET 8 coding standards including primary constructors, collection expressions, async patterns, null handling, and naming conventions. Use when writing or reviewing .NET 8 code.
---

# .NET 8 Coding Standards

## Overview
These standards ensure consistent, modern C# code across the codebase. Follow these patterns for all .NET 8 development.

## C# 12 Syntax

### Primary Constructors
Use primary constructors for dependency injection:

```csharp
// Good - primary constructor
public class TaskService(ITaskRepository repository, ILogger<TaskService> logger)
{
    public async Task<TaskItem> GetByIdAsync(Guid id) => await repository.GetByIdAsync(id);
}

// Avoid - traditional constructor
public class TaskService
{
    private readonly ITaskRepository _repository;
    public TaskService(ITaskRepository repository) => _repository = repository;
}
```

### Collection Expressions
Use collection expressions for initialization:

```csharp
// Good
List<string> items = ["one", "two", "three"];
int[] numbers = [1, 2, 3];

// Avoid
var items = new List<string> { "one", "two", "three" };
```

## Naming Conventions

### Classes and Methods
- PascalCase for classes, methods, properties: `TaskService`, `GetAllAsync`, `IsCompleted`
- Async methods suffix with `Async`: `GetByIdAsync`, `CreateAsync`

### Variables and Parameters
- camelCase for local variables and parameters: `taskId`, `pageSize`
- No Hungarian notation or prefixes
- Descriptive names over abbreviations: `cancellationToken` not `ct`

### Interfaces
- Prefix with `I`: `ITaskService`, `ITaskRepository`

## Async/Await Patterns

### Always Use CancellationToken
```csharp
// Good - accepts and passes CancellationToken
public async Task<List<TaskItem>> GetAllAsync(CancellationToken cancellationToken = default)
{
    return await repository.GetAllAsync(cancellationToken);
}

// Avoid - no cancellation support
public async Task<List<TaskItem>> GetAllAsync()
{
    return await repository.GetAllAsync();
}
```

### ConfigureAwait
In library code, use `ConfigureAwait(false)`:
```csharp
await repository.GetAllAsync(cancellationToken).ConfigureAwait(false);
```

In ASP.NET Core controllers/services, it's optional (HttpContext flows automatically).

## Null Handling

### Nullable Reference Types
Enable nullable reference types (already in csproj):
```csharp
// Explicit nullability
public string? Description { get; set; }  // Can be null
public string Title { get; set; } = string.Empty;  // Cannot be null
```

### Null Checks
Use pattern matching for null checks:
```csharp
// Good
if (task is null) return NotFound();
if (task is not null) Process(task);

// Avoid
if (task == null) return NotFound();
```

## Property Initialization

### Required Properties
Use `required` modifier for mandatory properties:
```csharp
public class CreateTaskRequest
{
    public required string Title { get; init; }
    public string? Description { get; init; }
}
```

### Init-Only Properties
Use `init` for immutable properties:
```csharp
public class TaskItem
{
    public Guid Id { get; init; }
    public required string Title { get; init; }
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;
}
```

## Records for DTOs

Use records for request/response DTOs:
```csharp
public record CreateTaskRequest(string Title, string? Description);
public record TaskResponse(Guid Id, string Title, string? Description, bool IsCompleted);
```

## File-Scoped Namespaces

Always use file-scoped namespaces:
```csharp
// Good
namespace TaskApi.Services;

public class TaskService { }

// Avoid
namespace TaskApi.Services
{
    public class TaskService { }
}
```

## Expression-Bodied Members

Use for single-line implementations:
```csharp
// Good
public string FullName => $"{FirstName} {LastName}";
public override string ToString() => Title;

// Use block body for multi-line
public async Task<TaskItem?> GetByIdAsync(Guid id)
{
    var task = await repository.GetByIdAsync(id);
    logger.LogInformation("Retrieved task {Id}", id);
    return task;
}
```
