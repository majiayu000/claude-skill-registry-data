---
name: csharp-dotnet
description: |
  Principal .NET 10 Architect providing high-performance, idiomatic C# 14 solutions.
  
  Use when user asks about:
  - .NET design patterns (Singleton, Factory, CQRS, Repository, Options Pattern)
  - C# coding style and best practices
  - Architecture decisions (Minimal APIs, Modular Monoliths)
  - Modern C# implementations with primary constructors, records, field keyword
  
  Triggers: ".NET", "C#", "design pattern", "architecture", "Minimal API", 
  "primary constructor", "record type", "Options Pattern", "Singleton", "Factory",
  "CQRS", "Repository pattern", "dependency injection"
---

# .NET 10 / C# 14 Design Patterns & Style Guide

Provide high-performance, concise, and idiomatic C# 14 solutions. Target CLI-focused development (Zed/VS Code, `dotnet` CLI).

## Core Principles

| Principle | Approach |
|-----------|----------|
| Conciseness | Primary constructors, records, `field` keyword |
| Thread Safety | `Lazy<T>`, `ConcurrentDictionary`, immutable types |
| No Bloat | Avoid unnecessary abstract factories |
| Minimal APIs | Prefer over traditional MVC controllers |
| Modular Monolith | Prefer over complex microservices |

## Output Format

1. **Context** - Brief explanation of *why* the pattern fits
2. **Code** - Modern C# 14 implementation
3. **Key Features** - Highlight C# 14 features used

## Pattern Quick Reference

### Singleton (Thread-Safe)

```csharp
public sealed class ConfigService(IOptions<AppSettings> options)
{
    private static readonly Lazy<ConfigService> _instance = new(() => 
        new ConfigService(/* resolve from DI */));
    
    public static ConfigService Instance => _instance.Value;
    public AppSettings Settings => options.Value;
}
```

### Options Pattern (Preferred for Config)

```csharp
// appsettings.json binding
public record DatabaseOptions
{
    public const string Section = "Database";
    public required string ConnectionString { get; init; }
    public int MaxRetries { get; init; } = 3;
}

// Registration
builder.Services.Configure<DatabaseOptions>(
    builder.Configuration.GetSection(DatabaseOptions.Section));

// Usage with primary constructor
public class UserRepository(IOptions<DatabaseOptions> options)
{
    private readonly string _connectionString = options.Value.ConnectionString;
}
```

### Factory Pattern (Modern)

```csharp
public interface IPaymentProcessor { Task ProcessAsync(decimal amount); }

public class PaymentProcessorFactory(IServiceProvider sp)
{
    public IPaymentProcessor Create(string type) => type switch
    {
        "stripe" => sp.GetRequiredService<StripeProcessor>(),
        "paypal" => sp.GetRequiredService<PayPalProcessor>(),
        _ => throw new ArgumentException($"Unknown processor: {type}")
    };
}
```

### Repository Pattern (Generic)

```csharp
public interface IRepository<T> where T : class
{
    ValueTask<T?> GetByIdAsync(int id, CancellationToken ct = default);
    IAsyncEnumerable<T> GetAllAsync(CancellationToken ct = default);
    Task AddAsync(T entity, CancellationToken ct = default);
    Task UpdateAsync(T entity, CancellationToken ct = default);
    Task DeleteAsync(int id, CancellationToken ct = default);
}

public class EfRepository<T>(AppDbContext db) : IRepository<T> where T : class
{
    public ValueTask<T?> GetByIdAsync(int id, CancellationToken ct = default) 
        => db.Set<T>().FindAsync([id], ct);
    
    public IAsyncEnumerable<T> GetAllAsync(CancellationToken ct = default) 
        => db.Set<T>().AsAsyncEnumerable();
    
    public async Task AddAsync(T entity, CancellationToken ct = default)
    {
        db.Set<T>().Add(entity);
        await db.SaveChangesAsync(ct);
    }
    
    public async Task UpdateAsync(T entity, CancellationToken ct = default)
    {
        db.Set<T>().Update(entity);
        await db.SaveChangesAsync(ct);
    }
    
    public async Task DeleteAsync(int id, CancellationToken ct = default)
    {
        var entity = await GetByIdAsync(id, ct);
        if (entity is not null)
        {
            db.Set<T>().Remove(entity);
            await db.SaveChangesAsync(ct);
        }
    }
}
```

### CQRS (Simplified)

```csharp
// Commands
public record CreateOrderCommand(string CustomerId, List<OrderItem> Items);
public interface ICommandHandler<TCommand> 
{
    Task<Result> HandleAsync(TCommand command, CancellationToken ct = default);
}

// Queries
public record GetOrderQuery(int OrderId);
public interface IQueryHandler<TQuery, TResult>
{
    Task<TResult> HandleAsync(TQuery query, CancellationToken ct = default);
}

// Minimal API integration
app.MapPost("/orders", async (
    CreateOrderCommand cmd,
    ICommandHandler<CreateOrderCommand> handler,
    CancellationToken ct) =>
{
    var result = await handler.HandleAsync(cmd, ct);
    return result.IsSuccess ? Results.Created() : Results.BadRequest(result.Error);
});
```

## Minimal API Patterns

```csharp
var builder = WebApplication.CreateBuilder(args);

// Service registration
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.Configure<DatabaseOptions>(
    builder.Configuration.GetSection(DatabaseOptions.Section));

var app = builder.Build();

// Route groups
var api = app.MapGroup("/api/v1");
var users = api.MapGroup("/users").RequireAuthorization();

users.MapGet("/", async (IUserService svc, CancellationToken ct) => 
    await svc.GetAllAsync(ct));

users.MapGet("/{id:int}", async (int id, IUserService svc, CancellationToken ct) => 
    await svc.GetByIdAsync(id, ct) is { } user 
        ? Results.Ok(user) 
        : Results.NotFound());

users.MapPost("/", async (CreateUserRequest req, IUserService svc, CancellationToken ct) =>
{
    var user = await svc.CreateAsync(req, ct);
    return Results.Created($"/api/v1/users/{user.Id}", user);
});

app.Run();
```

## C# 14 Features to Use

| Feature | Usage |
|---------|-------|
| Primary constructors | DI injection: `class Service(IRepo repo)` |
| `field` keyword | Backing field access in properties |
| Records | DTOs, Commands, Queries, Value Objects |
| Required members | `required string Name { get; init; }` |
| Collection expressions | `[1, 2, 3]` instead of `new[] {1, 2, 3}` |
| Pattern matching | Switch expressions for complex conditionals |

## Resources

- **Design patterns details**: See `references/patterns.md`
- **Minimal API patterns**: See `references/minimal-api.md`
