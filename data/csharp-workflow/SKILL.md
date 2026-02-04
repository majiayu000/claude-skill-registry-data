---
name: csharp-workflow
description: C# and .NET project workflow guidelines. Activate when working with C# files (.cs), .csproj, .NET projects, or C#-specific tooling.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# C# Projects Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | Roslynator | `dotnet roslynator analyze` |
| Format | dotnet format | `dotnet format` |
| Build | dotnet | `dotnet build` |
| Test | dotnet | `dotnet test` |
| Publish | dotnet | `dotnet publish` |
| Watch | dotnet | `dotnet watch run` |
| NuGet restore | dotnet | `dotnet restore` |
| Add package | dotnet | `dotnet add package <name>` |

---

## C# 12+ Features

### Primary Constructors

SHOULD use primary constructors for dependency injection and simple initialization:

```csharp
public class UserService(IUserRepository repository, ILogger<UserService> logger)
{
    public async Task<User?> GetByIdAsync(int id) => await repository.FindAsync(id);
}
```

### Collection Expressions

SHOULD use collection expressions for collection initialization:

```csharp
// Preferred
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];

// Spread operator
int[] combined = [..firstArray, ..secondArray];
```

### Raw String Literals

SHOULD use raw string literals for multi-line strings and strings containing quotes:

```csharp
var json = """
    {
        "name": "Example",
        "value": 42
    }
    """;
```

### File-Scoped Namespaces

MUST use file-scoped namespaces to reduce nesting:

```csharp
namespace MyApp.Services;

public class MyService { }
```

---

## .NET 8+ Patterns

### Minimal APIs

SHOULD use minimal APIs for microservices and simple endpoints:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/api/users/{id}", async (int id, IUserService service) =>
    await service.GetByIdAsync(id) is User user
        ? Results.Ok(user)
        : Results.NotFound());

app.Run();
```

### AOT Compilation

SHOULD design for AOT compatibility when targeting native deployment:

- MUST NOT use reflection-heavy patterns
- SHOULD use source generators instead of runtime reflection
- MUST use `[JsonSerializable]` for System.Text.Json

```csharp
[JsonSerializable(typeof(User))]
[JsonSerializable(typeof(List<User>))]
internal partial class AppJsonContext : JsonSerializerContext { }
```

### Keyed Services

MAY use keyed services for named dependency resolution:

```csharp
builder.Services.AddKeyedSingleton<ICache, RedisCache>("redis");
builder.Services.AddKeyedSingleton<ICache, MemoryCache>("memory");
```

---

## Naming Conventions

### General Rules

| Element | Convention | Example |
|---------|------------|---------|
| Public members | PascalCase | `GetUserAsync()` |
| Private fields | _camelCase | `_userRepository` |
| Local variables | camelCase | `userName` |
| Constants | PascalCase | `MaxRetryCount` |
| Interfaces | IPascalCase | `IUserService` |
| Type parameters | TPascalCase | `TEntity` |
| Async methods | Async suffix | `GetUserAsync()` |

### MUST Follow

- MUST use `I` prefix for interfaces
- MUST use `Async` suffix for async methods
- MUST NOT use Hungarian notation
- MUST NOT use underscores in public identifiers

---

## Nullable Reference Types

### Configuration

MUST enable nullable reference types in all projects:

```xml
<PropertyGroup>
    <Nullable>enable</Nullable>
</PropertyGroup>
```

### Usage Rules

- MUST annotate all reference types explicitly
- MUST handle null appropriately with null-conditional operators
- SHOULD use `required` keyword for required properties
- MUST NOT use `!` (null-forgiving operator) except when absolutely necessary

```csharp
public class User
{
    public required string Name { get; init; }
    public string? Email { get; set; }
}
```

---

## Async/Await Best Practices

### Rules

- MUST use async all the way (no sync-over-async)
- MUST use `ConfigureAwait(false)` in library code
- MUST use `CancellationToken` for cancellable operations
- SHOULD prefer `ValueTask` for hot paths with frequent sync completion
- MUST NOT use `async void` except for event handlers

```csharp
public async Task<User?> GetUserAsync(int id, CancellationToken ct = default)
{
    return await _repository.FindAsync(id, ct).ConfigureAwait(false);
}
```

### Exception Handling

- MUST catch specific exceptions, not `Exception`
- SHOULD use `when` clause for conditional catches
- MUST NOT swallow exceptions silently

---

## Dependency Injection

### Rules

- MUST use constructor injection for required dependencies
- SHOULD use primary constructors for DI
- MUST NOT use service locator pattern
- MUST register services with appropriate lifetime

```csharp
// Registration
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddSingleton<ICacheService, CacheService>();
builder.Services.AddTransient<IEmailService, EmailService>();
```

### Lifetime Guidelines

| Lifetime | Use Case |
|----------|----------|
| Singleton | Stateless services, caches |
| Scoped | Per-request services, DbContext |
| Transient | Lightweight, stateless operations |

---

## Record Types

### DTOs and Value Objects

MUST use records for DTOs and immutable data:

```csharp
public record UserDto(int Id, string Name, string? Email);

public record CreateUserRequest(string Name, string Email);

public record ApiResponse<T>(T Data, bool Success, string? Error = null);
```

### Rules

- MUST use positional records for simple DTOs
- MAY use record classes with properties for complex objects
- SHOULD use `with` expressions for immutable updates

---

## LINQ Best Practices

### Method Syntax

SHOULD prefer method syntax over query syntax:

```csharp
// Preferred
var adults = users
    .Where(u => u.Age >= 18)
    .OrderBy(u => u.Name)
    .Select(u => new UserDto(u.Id, u.Name, u.Email));

// Avoid query syntax for simple queries
var adults = from u in users
             where u.Age >= 18
             select u;
```

### Performance

- MUST materialize queries when iterating multiple times
- SHOULD use `Any()` instead of `Count() > 0`
- SHOULD use `FirstOrDefault()` with predicate
- MUST NOT use LINQ in hot paths without benchmarking

---

## Testing

### Framework Options

| Framework | Command |
|-----------|---------|
| xUnit | `dotnet test` |
| NUnit | `dotnet test` |
| MSTest | `dotnet test` |

### xUnit Patterns (RECOMMENDED)

```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _mockRepo = new();
    private readonly UserService _sut;

    public UserServiceTests()
    {
        _sut = new UserService(_mockRepo.Object);
    }

    [Fact]
    public async Task GetByIdAsync_WhenUserExists_ReturnsUser()
    {
        // Arrange
        var expected = new User { Id = 1, Name = "Test" };
        _mockRepo.Setup(r => r.FindAsync(1, default))
            .ReturnsAsync(expected);

        // Act
        var result = await _sut.GetByIdAsync(1);

        // Assert
        Assert.Equal(expected, result);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task GetByIdAsync_WhenIdInvalid_ThrowsArgumentException(int id)
    {
        await Assert.ThrowsAsync<ArgumentException>(() => _sut.GetByIdAsync(id));
    }
}
```

### Rules

- MUST follow Arrange-Act-Assert pattern
- MUST use meaningful test names
- SHOULD use `[Theory]` for parameterized tests
- MUST mock external dependencies

---

## Project Structure

### RECOMMENDED Layout

```
MySolution/
├── src/
│   ├── MyApp.Api/
│   │   ├── Controllers/
│   │   ├── Endpoints/
│   │   └── Program.cs
│   ├── MyApp.Application/
│   │   ├── Services/
│   │   └── DTOs/
│   ├── MyApp.Domain/
│   │   ├── Entities/
│   │   └── Interfaces/
│   └── MyApp.Infrastructure/
│       ├── Data/
│       └── Services/
├── tests/
│   ├── MyApp.UnitTests/
│   └── MyApp.IntegrationTests/
├── Directory.Build.props
├── Directory.Packages.props
└── MySolution.sln
```

### Directory.Build.props

SHOULD use centralized build configuration:

```xml
<Project>
    <PropertyGroup>
        <TargetFramework>net8.0</TargetFramework>
        <ImplicitUsings>enable</ImplicitUsings>
        <Nullable>enable</Nullable>
        <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    </PropertyGroup>
</Project>
```

---

## Error Handling

### Result Pattern

SHOULD use Result pattern for expected failures:

```csharp
public record Result<T>(T? Value, bool IsSuccess, string? Error = null)
{
    public static Result<T> Success(T value) => new(value, true);
    public static Result<T> Failure(string error) => new(default, false, error);
}
```

### Exceptions

- MUST use exceptions for exceptional conditions only
- SHOULD create custom exceptions for domain errors
- MUST include relevant context in exception messages

---

## Configuration

### Options Pattern

MUST use Options pattern for configuration:

```csharp
public class DatabaseOptions
{
    public const string SectionName = "Database";
    public required string ConnectionString { get; init; }
    public int MaxRetryCount { get; init; } = 3;
}

// Registration
builder.Services.Configure<DatabaseOptions>(
    builder.Configuration.GetSection(DatabaseOptions.SectionName));
```

---

## Code Quality

### Analyzers

SHOULD enable code analysis:

```xml
<PropertyGroup>
    <EnableNETAnalyzers>true</EnableNETAnalyzers>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
</PropertyGroup>
```

### EditorConfig

MUST include `.editorconfig` for consistent style across team.
