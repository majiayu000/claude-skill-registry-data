---
name: developing-with-dotnet
description: Write C#/.NET 9 — Clean Architecture, MediatR CQRS, EF Core, minimal APIs, DI.
when_to_use: Reach for this when writing C# / .NET application code (services, minimal APIs, EF Core data layers). For Blazor UI components use blazor; for Azure Functions serverless triggers use using-azure-functions; for Clerk auth in .NET use using-clerk; for generating/running .NET tests use xunit. This is the general C# language/architecture skill.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "**/*.cs"
  - "**/*.csproj"
  - "*.sln"
  - "global.json"
  - "Directory.Build.props"
---

# .NET Development Skill

.NET 9 development with Clean Architecture, CQRS via MediatR, Entity Framework Core,
minimal APIs, and modern dependency injection patterns.

**Progressive Disclosure**: Quick reference patterns here. See [REFERENCE.md](REFERENCE.md) for advanced topics.

---

## When to Use

Loaded by `backend-developer` or `frontend-developer` when:
- `*.csproj` or `*.sln` files present in project
- `Program.cs` detected
- `appsettings.json` present
- User mentions ".NET", "C#", "ASP.NET", or "Entity Framework"

---

## Clean Architecture Folder Structure

```
src/
  MyApp.Domain/              # Entities, ValueObjects, Enums, Events, Exceptions, Interfaces
  MyApp.Application/         # Features/ (Commands + Queries), Common/Behaviors, Interfaces
  MyApp.Infrastructure/      # Data/ (DbContext, Configs, Migrations), Services, DI extension
  MyApp.WebApi/              # Endpoints/, Filters/, Middleware/, Program.cs
tests/
  MyApp.Domain.Tests/
  MyApp.Application.Tests/
  MyApp.Infrastructure.Tests/
  MyApp.WebApi.Tests/
```

> **Full structure**: See [REFERENCE.md](REFERENCE.md) for the complete template walkthrough.

---

## CQRS with MediatR

### Command

```csharp
public sealed record CreateOrderCommand(
    string CustomerId,
    List<OrderItemDto> Items) : IRequest<Guid>;

public sealed class CreateOrderCommandHandler
    : IRequestHandler<CreateOrderCommand, Guid>
{
    private readonly IOrderRepository _orderRepository;
    private readonly IUnitOfWork _unitOfWork;

    public CreateOrderCommandHandler(
        IOrderRepository orderRepository, IUnitOfWork unitOfWork)
    {
        _orderRepository = orderRepository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Guid> Handle(
        CreateOrderCommand request, CancellationToken ct)
    {
        var order = Order.Create(request.CustomerId, request.Items);
        _orderRepository.Add(order);
        await _unitOfWork.SaveChangesAsync(ct);
        return order.Id;
    }
}
```

### Query

```csharp
public sealed record GetOrderByIdQuery(Guid Id) : IRequest<OrderDto?>;

public sealed class GetOrderByIdQueryHandler
    : IRequestHandler<GetOrderByIdQuery, OrderDto?>
{
    private readonly IApplicationDbContext _context;

    public GetOrderByIdQueryHandler(IApplicationDbContext context)
        => _context = context;

    public async Task<OrderDto?> Handle(
        GetOrderByIdQuery request, CancellationToken ct)
    {
        return await _context.Orders
            .Where(o => o.Id == request.Id)
            .Select(o => new OrderDto(o.Id, o.CustomerId, o.Total))
            .FirstOrDefaultAsync(ct);
    }
}
```

### Pipeline Behaviors

**CRITICAL**: MediatR 12+ changed the pipeline behavior constraint.
Use `where TRequest : notnull`, NOT `where TRequest : IRequest<TResponse>`.

```csharp
// Validation behavior
public sealed class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
        => _validators = validators;

    public async Task<TResponse> Handle(
        TRequest request, RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        if (!_validators.Any()) return await next();

        var context = new ValidationContext<TRequest>(request);
        var failures = (await Task.WhenAll(
                _validators.Select(v => v.ValidateAsync(context, ct))))
            .SelectMany(r => r.Errors)
            .Where(f => f is not null)
            .ToList();

        if (failures.Count != 0) throw new ValidationException(failures);
        return await next();
    }
}
```

```csharp
// Logging behavior
public sealed class LoggingBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
        => _logger = logger;

    public async Task<TResponse> Handle(
        TRequest request, RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        _logger.LogInformation("Handling {Request}", typeof(TRequest).Name);
        var response = await next();
        _logger.LogInformation("Handled {Request}", typeof(TRequest).Name);
        return response;
    }
}
```

**Licensing note**: MediatR requires a commercial license for organizations
with >$5M annual revenue since v13. See [REFERENCE.md](REFERENCE.md) for alternatives.

---

## Dependency Injection Patterns

### Registering Services

```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseNpgsql(
                configuration.GetConnectionString("DefaultConnection")));

        services.AddScoped<IApplicationDbContext>(sp =>
            sp.GetRequiredService<ApplicationDbContext>());

        return services;
    }
}
```

### IOptions Pattern

```csharp
public sealed class SmtpSettings
{
    public const string SectionName = "Smtp";
    public required string Host { get; init; }
    public required int Port { get; init; }
    public required string FromAddress { get; init; }
}

// Registration
services.Configure<SmtpSettings>(
    configuration.GetSection(SmtpSettings.SectionName));

// Injection (primary constructor syntax)
public class EmailService(IOptions<SmtpSettings> options)
{
    private readonly SmtpSettings _settings = options.Value;
}
```

### Keyed Services (.NET 8+)

```csharp
services.AddKeyedSingleton<ICache, RedisCache>("redis");
services.AddKeyedSingleton<ICache, MemoryCache>("memory");

// Injection via attribute
public class OrderService(
    [FromKeyedServices("redis")] ICache distributedCache,
    [FromKeyedServices("memory")] ICache localCache) { }
```

### Service Lifetime Guidance

| Lifetime | Use When | Example |
|----------|----------|---------|
| Singleton | Thread-safe, shared state | `IMemoryCache`, `HttpClient` factory |
| Scoped | Per-request state | `DbContext`, `IUnitOfWork` |
| Transient | Lightweight, stateless | Validators, mappers |

---

## Minimal API Patterns

**CRITICAL**: Use `TypedResults` (not `Results`) for proper OpenAPI integration.

```csharp
public static class OrderEndpoints
{
    public static RouteGroupBuilder MapOrderEndpoints(
        this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/orders")
            .WithTags("Orders")
            .RequireAuthorization();

        group.MapPost("/", CreateOrder).WithName("CreateOrder");
        group.MapGet("/{id:guid}", GetOrderById).WithName("GetOrderById");

        return group;
    }

    private static async Task<Results<Created<Guid>, ValidationProblem>>
        CreateOrder(CreateOrderRequest request, ISender sender,
            CancellationToken ct)
    {
        var command = new CreateOrderCommand(
            request.CustomerId, request.Items);
        var orderId = await sender.Send(command, ct);
        return TypedResults.Created($"/api/orders/{orderId}", orderId);
    }

    private static async Task<Results<Ok<OrderDto>, NotFound>>
        GetOrderById(Guid id, ISender sender, CancellationToken ct)
    {
        var order = await sender.Send(new GetOrderByIdQuery(id), ct);
        return order is not null
            ? TypedResults.Ok(order) : TypedResults.NotFound();
    }
}
```

### Endpoint Filters (.NET 9)

```csharp
public class RequestLoggingFilter : IEndpointFilter
{
    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        // Log before and after; add timing, correlation IDs, etc.
        return await next(context);
    }
}

// Usage
group.MapGet("/", GetAll).AddEndpointFilter<RequestLoggingFilter>();
```

---

## Entity Framework Core Patterns

### DbContext Configuration

```csharp
public class ApplicationDbContext : DbContext, IApplicationDbContext
{
    public ApplicationDbContext(
        DbContextOptions<ApplicationDbContext> options) : base(options) { }

    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(
            typeof(ApplicationDbContext).Assembly);
    }
}
```

### Entity Configuration (Fluent API)

```csharp
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.HasKey(o => o.Id);
        builder.Property(o => o.CustomerId).IsRequired().HasMaxLength(50);
        builder.Property(o => o.Total).HasPrecision(18, 2);
        builder.HasMany(o => o.Items).WithOne()
            .HasForeignKey(i => i.OrderId)
            .OnDelete(DeleteBehavior.Cascade);
        builder.HasQueryFilter(o => !o.IsDeleted);
    }
}
```

### Migrations

```bash
dotnet ef migrations add InitialCreate \
    --project src/MyApp.Infrastructure \
    --startup-project src/MyApp.WebApi

dotnet ef database update \
    --project src/MyApp.Infrastructure \
    --startup-project src/MyApp.WebApi

# Idempotent SQL script for production
dotnet ef migrations script --idempotent --output migrate.sql \
    --project src/MyApp.Infrastructure \
    --startup-project src/MyApp.WebApi
```

### Value Converters

```csharp
// Enum as string
builder.Property(o => o.Status).HasConversion<string>().HasMaxLength(20);

// Strongly-typed ID
builder.Property(o => o.Id)
    .HasConversion(id => id.Value, value => new OrderId(value));
```

---

## Configuration Binding (.NET 9)

**CRITICAL**: `[OptionsValidator]` is a source-generated validator.
It generates `IValidateOptions<T>` at compile time -- not data annotation
validation on options classes.

```csharp
public sealed class DatabaseSettings
{
    public const string SectionName = "Database";

    [Required]
    public required string ConnectionString { get; init; }

    [Range(1, 100)]
    public int MaxRetryCount { get; init; } = 3;
}

// Source-generated validator
[OptionsValidator]
public partial class DatabaseSettingsValidator
    : IValidateOptions<DatabaseSettings> { }

// Registration
services.AddOptionsWithValidateOnStart<DatabaseSettings>()
    .BindConfiguration(DatabaseSettings.SectionName)
    .ValidateOnStart();
services.AddSingleton<IValidateOptions<DatabaseSettings>,
    DatabaseSettingsValidator>();
```

---

## Error Handling

### Result Pattern

```csharp
public sealed class Result<T>
{
    private Result(T? value, Error? error, bool isSuccess)
    { Value = value; Error = error; IsSuccess = isSuccess; }

    public T? Value { get; }
    public Error? Error { get; }
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;

    public static Result<T> Success(T value) => new(value, null, true);
    public static Result<T> Failure(Error error) => new(default, error, false);
}

public sealed record Error(string Code, string Message)
{
    public static readonly Error None = new(string.Empty, string.Empty);
    public static readonly Error NotFound = new("NotFound", "Resource not found");
}
```

### ProblemDetails Middleware

```csharp
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = ctx =>
    {
        ctx.ProblemDetails.Extensions["traceId"] =
            ctx.HttpContext.TraceIdentifier;
    };
});
app.UseExceptionHandler();
app.UseStatusCodePages();
```

> **More patterns**: See [REFERENCE.md](REFERENCE.md) for custom exception handler
> mapping (ValidationException, NotFoundException, etc.).

---

## Quick Reference Card

### CLI Commands

```bash
dotnet new sln -n MyApp                    # Create solution
dotnet new webapi -n MyApp.WebApi          # Create Web API project
dotnet new classlib -n MyApp.Domain        # Create class library
dotnet sln add src/MyApp.WebApi            # Add project to solution
dotnet add package MediatR                 # Add NuGet package
dotnet build                               # Build
dotnet run --project src/MyApp.WebApi      # Run
dotnet watch --project src/MyApp.WebApi    # Run with hot reload
dotnet test                                # Run all tests
dotnet test --filter "FullyQualifiedName~OrderTests"  # Filter tests
dotnet test --collect:"XPlat Code Coverage"            # With coverage
```

### Essential NuGet Packages

| Package | Purpose |
|---------|---------|
| `MediatR` | CQRS mediator pattern |
| `FluentValidation` | Request validation |
| `Mapster` | High-performance object mapping |
| `Serilog.AspNetCore` | Structured logging |
| `Microsoft.EntityFrameworkCore` | ORM |
| `Npgsql.EntityFrameworkCore.PostgreSQL` | PostgreSQL provider |
| `xunit` + `FluentAssertions` + `NSubstitute` | Testing stack |
| `Microsoft.AspNetCore.Mvc.Testing` | Integration testing |
| `Testcontainers` | Docker-based test infrastructure |

---

## See Also

- [REFERENCE.md](REFERENCE.md) - Advanced patterns, DDD, AOT, testing deep-dive
- [Microsoft .NET Documentation](https://learn.microsoft.com/dotnet/)
- [Clean Architecture Template](https://github.com/jasontaylordev/CleanArchitecture)
