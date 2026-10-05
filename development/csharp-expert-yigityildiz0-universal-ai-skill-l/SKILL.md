---
name: csharp-expert
description: Deep C# expertise for enterprise application development. Use when writing C# code, implementing async/await patterns, designing with LINQ, working with.
---

# C# Expert

Specialized expertise in C# programming, providing deep guidance on async/await patterns, LINQ queries, generics and delegates, modern language features, dependency injection, error handling, and testing enterprise applications with xUnit.

## When to Use This Skill

Use this skill for:

- Implementing async/await and Task-based concurrency
- Writing efficient LINQ queries and custom extension methods
- Designing with generics, delegates, and event-driven patterns
- Leveraging modern C# features (pattern matching, records, file-scoped namespaces)
- Configuring dependency injection and applying SOLID principles
- Building robust error handling with structured logging
- Writing comprehensive tests with xUnit and mocking frameworks

**Trigger phrases**: "csharp", "c#", "dotnet", ".net", "asp.net", "async await", "linq", "entity framework", "xunit", "blazor"

## What This Skill Does

Provides C# expertise including:

- **Async/Await**: Task, ValueTask, async streams, cancellation, ConfigureAwait
- **LINQ**: Query and method syntax, deferred execution, Expression trees
- **Type System**: Generics, delegates, events, covariance/contravariance
- **Modern C#**: Pattern matching, records, switch expressions, list patterns
- **Architecture**: Dependency injection, SOLID principles, options pattern
- **Reliability**: Custom exceptions, Result pattern, structured logging
- **Testing**: xUnit, Moq/NSubstitute, FluentAssertions, integration tests

## Instructions

### Step 1: Master Async/Await and Task Patterns

**Task and ValueTask Basics**:

```csharp
// Async method returning Task<T> for I/O-bound work
public async Task<Customer> GetCustomerAsync(int id, CancellationToken ct = default)
{
    var customer = await _dbContext.Customers
        .FirstOrDefaultAsync(c => c.Id == id, ct);

    if (customer is null)
        throw new NotFoundException($"Customer {id} not found");

    return customer;
}

// Use ValueTask<T> when the result is often synchronous (cache hit)
private readonly ConcurrentDictionary<int, Product> _cache = new();

public ValueTask<Product> GetProductAsync(int id, CancellationToken ct = default)
{
    if (_cache.TryGetValue(id, out var cached))
        return ValueTask.FromResult(cached); // No allocation

    return new ValueTask<Product>(LoadAndCacheProductAsync(id, ct));
}

private async Task<Product> LoadAndCacheProductAsync(int id, CancellationToken ct)
{
    var product = await _repository.FindAsync(id, ct);
    _cache.TryAdd(id, product);
    return product;
}
```

**Async Streams with IAsyncEnumerable**:

```csharp
// Produce items lazily over an async stream
public async IAsyncEnumerable<LogEntry> StreamLogsAsync(
    DateTime since,
    [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var batch in _logSource.ReadBatchesAsync(since, ct))
    {
        foreach (var entry in batch.Entries)
        {
            ct.ThrowIfCancellationRequested();
            yield return entry;
        }
    }
}

// Consume the stream
await foreach (var log in service.StreamLogsAsync(DateTime.UtcNow.AddHours(-1), ct))
{
    Console.WriteLine($"{log.Timestamp}: {log.Message}");
}
```

**ConfigureAwait and SemaphoreSlim**:

```csharp
// Library code should use ConfigureAwait(false) to avoid deadlocks
public async Task<byte[]> DownloadAsync(string url, CancellationToken ct = default)
{
    using var client = new HttpClient();
    var response = await client.GetAsync(url, ct).ConfigureAwait(false);
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadAsByteArrayAsync(ct).ConfigureAwait(false);
}

// Throttle concurrent access with SemaphoreSlim
private readonly SemaphoreSlim _semaphore = new(maxCount: 5);

public async Task<string> ThrottledRequestAsync(string url, CancellationToken ct = default)
{
    await _semaphore.WaitAsync(ct);
    try
    {
        return await _httpClient.GetStringAsync(url, ct);
    }
    finally
    {
        _semaphore.Release();
    }
}

// CancellationToken with timeout composition
public async Task ProcessWithTimeoutAsync(CancellationToken externalCt)
{
    using var cts = CancellationTokenSource.CreateLinkedTokenSource(externalCt);
    cts.CancelAfter(TimeSpan.FromSeconds(30));

    await DoWorkAsync(cts.Token); // Cancelled by either timeout or external signal
}
```

### Step 2: Achieve LINQ Mastery

**Query Syntax vs Method Syntax**:

```csharp
// Query syntax (reads like SQL, good for joins and grouping)
var expensiveOrders = from o in orders
                      where o.Total > 1000m
                      orderby o.CreatedAt descending
                      select new { o.Id, o.Total, o.Customer.Name };

// Equivalent method syntax (more flexible, composable)
var expensiveOrders = orders
    .Where(o => o.Total > 1000m)
    .OrderByDescending(o => o.CreatedAt)
    .Select(o => new { o.Id, o.Total, o.Customer.Name });

// Join with method syntax
var orderDetails = customers
    .Join(orders,
        c => c.Id,
        o => o.CustomerId,
        (c, o) => new { Customer = c.Name, o.Total, o.CreatedAt })
    .Where(x => x.Total > 500m)
    .ToList();

// GroupBy with aggregation
var salesByRegion = orders
    .GroupBy(o => o.Region)
    .Select(g => new
    {
        Region = g.Key,
        TotalSales = g.Sum(o => o.Total),
        OrderCount = g.Count(),
        AverageOrder = g.Average(o => o.Total)
    })
    .OrderByDescending(x => x.TotalSales);
```

**Deferred Execution and Custom Extension Methods**:

```csharp
// Deferred execution: the query is not evaluated until enumerated
IEnumerable<Order> query = orders.Where(o => o.Total > 100m);
// Nothing has executed yet; adding more items to orders will be reflected

var results = query.ToList(); // NOW it executes

// Custom extension method for reusable LINQ operators
public static class EnumerableExtensions
{
    public static IEnumerable<T> WhereNotNull<T>(this IEnumerable<T?> source) where T : class
    {
        return source.Where(item => item is not null)!;
    }

    public static IEnumerable<IEnumerable<T>> Batch<T>(this IEnumerable<T> source, int size)
    {
        var batch = new List<T>(size);
        foreach (var item in source)
        {
            batch.Add(item);
            if (batch.Count == size)
            {
                yield return batch;
                batch = new List<T>(size);
            }
        }
        if (batch.Count > 0)
            yield return batch;
    }
}

// Usage
var validNames = users.Select(u => u.Email).WhereNotNull().ToList();
var batches = records.Batch(100);
```

**Expression Trees**:

```csharp
// Build dynamic filters with Expression trees
public static class PredicateBuilder
{
    public static Expression<Func<T, bool>> And<T>(
        this Expression<Func<T, bool>> left,
        Expression<Func<T, bool>> right)
    {
        var parameter = Expression.Parameter(typeof(T));
        var body = Expression.AndAlso(
            Expression.Invoke(left, parameter),
            Expression.Invoke(right, parameter));
        return Expression.Lambda<Func<T, bool>>(body, parameter);
    }
}

// Dynamic query building for search filters
Expression<Func<Product, bool>> predicate = p => true;

if (!string.IsNullOrEmpty(filter.Name))
    predicate = predicate.And(p => p.Name.Contains(filter.Name));
if (filter.MinPrice.HasValue)
    predicate = predicate.And(p => p.Price >= filter.MinPrice.Value);

var results = await _dbContext.Products.Where(predicate).ToListAsync(ct);
```

### Step 3: Leverage Generics, Delegates, and Events

**Generic Constraints and Covariance/Contravariance**:

```csharp
// Multiple constraints on a generic type
public class Repository<T> where T : class, IEntity, new()
{
    public T Create()
    {
        var entity = new T(); // Possible because of new() constraint
        entity.CreatedAt = DateTime.UtcNow;
        return entity;
    }

    public async Task<T?> FindAsync(int id, CancellationToken ct = default)
    {
        return await _dbContext.Set<T>().FindAsync(new object[] { id }, ct);
    }
}

// Covariance (out): IEnumerable<Derived> can be used as IEnumerable<Base>
IEnumerable<string> strings = new List<string> { "a", "b" };
IEnumerable<object> objects = strings; // Covariant: out T

// Contravariance (in): Action<Base> can be used as Action<Derived>
Action<object> printObject = obj => Console.WriteLine(obj);
Action<string> printString = printObject; // Contravariant: in T

// Custom covariant interface
public interface IReadOnlyRepository<out T> where T : class
{
    Task<T?> FindAsync(int id);
    Task<IReadOnlyList<T>> GetAllAsync();
}

// Custom contravariant interface
public interface IComparer<in T>
{
    int Compare(T x, T y);
}
```

**Func, Action, and Custom Delegates**:

```csharp
// Func<T, TResult> for transformations
public async Task<TResult> ExecuteWithRetryAsync<TResult>(
    Func<CancellationToken, Task<TResult>> operation,
    int maxRetries = 3,
    CancellationToken ct = default)
{
    for (int attempt = 0; ; attempt++)
    {
        try
        {
            return await operation(ct);
        }
        catch (Exception ex) when (attempt < maxRetries - 1)
        {
            var delay = TimeSpan.FromSeconds(Math.Pow(2, attempt));
            await Task.Delay(delay, ct);
        }
    }
}

// Action<T> for side effects
public void ForEach<T>(IEnumerable<T> items, Action<T> action)
{
    foreach (var item in items)
        action(item);
}

// Predicate<T> for filtering
public List<T> Filter<T>(IEnumerable<T> source, Predicate<T> predicate)
{
    return source.Where(item => predicate(item)).ToList();
}
```

**Event Patterns**:

```csharp
// Standard .NET event pattern
public class OrderProcessor
{
    public event EventHandler<OrderEventArgs>? OrderCompleted;
    public event EventHandler<OrderEventArgs>? OrderFailed;

    protected virtual void OnOrderCompleted(OrderEventArgs e)
    {
        OrderCompleted?.Invoke(this, e);
    }

    public async Task ProcessAsync(Order order, CancellationToken ct = default)
    {
        try
        {
            await ValidateAsync(order, ct);
            await ChargePaymentAsync(order, ct);
            await FulfillAsync(order, ct);

            OnOrderCompleted(new OrderEventArgs(order, OrderStatus.Completed));
        }
        catch (Exception ex)
        {
            OrderFailed?.Invoke(this, new OrderEventArgs(order, OrderStatus.Failed, ex));
            throw;
        }
    }
}

public class OrderEventArgs : EventArgs
{
    public Order Order { get; }
    public OrderStatus Status { get; }
    public Exception? Error { get; }

    public OrderEventArgs(Order order, OrderStatus status, Exception? error = null)
    {
        Order = order;
        Status = status;
        Error = error;
    }
}
```

### Step 4: Embrace Pattern Matching and Modern C#

**Switch Expressions and Property Patterns**:

```csharp
// Switch expression with pattern matching
public decimal CalculateDiscount(Customer customer) => customer switch
{
    { Tier: CustomerTier.Gold, YearsActive: > 5 } => 0.25m,
    { Tier: CustomerTier.Gold } => 0.20m,
    { Tier: CustomerTier.Silver, YearsActive: > 3 } => 0.15m,
    { Tier: CustomerTier.Silver } => 0.10m,
    { IsNewCustomer: true } => 0.05m,
    _ => 0m
};

// Type patterns with when clauses
public string FormatError(Exception ex) => ex switch
{
    ArgumentNullException ane => $"Missing required argument: {ane.ParamName}",
    ValidationException ve when ve.Errors.Count > 1 => $"Multiple validation errors ({ve.Errors.Count})",
    ValidationException ve => $"Validation failed: {ve.Errors.First().ErrorMessage}",
    HttpRequestException { StatusCode: HttpStatusCode.NotFound } => "Resource not found",
    HttpRequestException hre => $"HTTP error: {hre.StatusCode}",
    _ => $"Unexpected error: {ex.Message}"
};
```

**List Patterns and Records**:

```csharp
// List patterns (C# 11+)
public string DescribeSequence(int[] numbers) => numbers switch
{
    [] => "empty",
    [var single] => $"single element: {single}",
    [var first, .., var last] => $"starts with {first}, ends with {last}",
};

// Records with value equality and immutability
public record Address(string Street, string City, string State, string Zip);

public record Customer(string Name, string Email, Address Address)
{
    // Computed property on a record
    public string DisplayName => $"{Name} ({Email})";
}

// Non-destructive mutation with 'with' expressions
var updated = customer with { Email = "new@example.com" };

// Record structs for value types
public readonly record struct Coordinate(double Latitude, double Longitude);

// Init-only setters for classes that are not records
public class AppConfig
{
    public string ConnectionString { get; init; } = string.Empty;
    public int MaxRetries { get; init; } = 3;
    public TimeSpan Timeout { get; init; } = TimeSpan.FromSeconds(30);
}

var config = new AppConfig
{
    ConnectionString = "Server=localhost;Database=app",
    MaxRetries = 5
};
// config.ConnectionString = "other"; // Compile error: init-only
```

**File-Scoped Namespaces and Global Usings**:

```csharp
// File-scoped namespace (C# 10+): saves one level of indentation
namespace MyApp.Services;

public class OrderService
{
    // Entire file is in this namespace
}

// GlobalUsings.cs: declare common imports once for the whole project
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading;
global using System.Threading.Tasks;
global using Microsoft.Extensions.Logging;
global using MyApp.Domain.Entities;
```

### Step 5: Apply Dependency Injection and SOLID Principles

**IServiceCollection Registration**:

```csharp
// Program.cs (minimal API style)
var builder = WebApplication.CreateBuilder(args);

// Register services with appropriate lifetimes
builder.Services.AddSingleton<ICacheService, RedisCacheService>();
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddScoped<IOrderRepository, SqlOrderRepository>();
builder.Services.AddTransient<IEmailSender, SmtpEmailSender>();

// Register all implementations of an interface via assembly scanning
builder.Services.Scan(scan => scan
    .FromAssemblyOf<ICommandHandler>()
    .AddClasses(classes => classes.AssignableTo(typeof(ICommandHandler<>)))
    .AsImplementedInterfaces()
    .WithScopedLifetime());

// Keyed services (C# 12 / .NET 8)
builder.Services.AddKeyedSingleton<INotifier, EmailNotifier>("email");
builder.Services.AddKeyedSingleton<INotifier, SmsNotifier>("sms");
```

**Options Pattern**:

```csharp
// Strongly typed configuration with validation
public class SmtpOptions
{
    public const string SectionName = "Smtp";

    [Required]
    public string Host { get; init; } = string.Empty;
    public int Port { get; init; } = 587;
    [Required]
    public string Username { get; init; } = string.Empty;
    [Required]
    public string Password { get; init; } = string.Empty;
}

// Registration with validation
builder.Services
    .AddOptions<SmtpOptions>()
    .BindConfiguration(SmtpOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart(); // Fail fast at startup if configuration is invalid

// Inject via IOptions<T>
public class EmailSender : IEmailSender
{
    private readonly SmtpOptions _options;

    public EmailSender(IOptions<SmtpOptions> options)
    {
        _options = options.Value;
    }
}
```

**Decorator Pattern with DI**:

```csharp
// Interface segregation: small, focused interfaces
public interface IOrderRepository
{
    Task<Order?> FindAsync(int id, CancellationToken ct = default);
    Task<IReadOnlyList<Order>> GetByCustomerAsync(int customerId, CancellationToken ct = default);
    Task SaveAsync(Order order, CancellationToken ct = default);
}

// Core implementation
public class SqlOrderRepository : IOrderRepository
{
    public async Task<Order?> FindAsync(int id, CancellationToken ct = default)
        => await _dbContext.Orders.FindAsync(new object[] { id }, ct);

    // Other methods...
}

// Decorator: adds caching without modifying the original class
public class CachedOrderRepository : IOrderRepository
{
    private readonly IOrderRepository _inner;
    private readonly ICacheService _cache;

    public CachedOrderRepository(IOrderRepository inner, ICacheService cache)
    {
        _inner = inner;
        _cache = cache;
    }

    public async Task<Order?> FindAsync(int id, CancellationToken ct = default)
    {
        var cacheKey = $"order:{id}";
        var cached = await _cache.GetAsync<Order>(cacheKey, ct);
        if (cached is not null) return cached;

        var order = await _inner.FindAsync(id, ct);
        if (order is not null)
            await _cache.SetAsync(cacheKey, order, TimeSpan.FromMinutes(10), ct);

        return order;
    }

    // Delegate other methods to _inner...
}

// Register the decorator chain
builder.Services.AddScoped<SqlOrderRepository>();
builder.Services.AddScoped<IOrderRepository>(sp =>
    new CachedOrderRepository(
        sp.GetRequiredService<SqlOrderRepository>(),
        sp.GetRequiredService<ICacheService>()));
```

### Step 6: Build Robust Error Handling and Logging

**Custom Exception Hierarchy**:

```csharp
// Base exception for the application domain
public abstract class AppException : Exception
{
    public string Code { get; }

    protected AppException(string code, string message, Exception? inner = null)
        : base(message, inner)
    {
        Code = code;
    }
}

public class NotFoundException : AppException
{
    public NotFoundException(string entity, object id)
        : base("NOT_FOUND", $"{entity} with id '{id}' was not found") { }
}

public class ConflictException : AppException
{
    public ConflictException(string message)
        : base("CONFLICT", message) { }
}

public class ValidationException : AppException
{
    public IReadOnlyList<ValidationError> Errors { get; }

    public ValidationException(IEnumerable<ValidationError> errors)
        : base("VALIDATION_FAILED", "One or more validation errors occurred")
    {
        Errors = errors.ToList().AsReadOnly();
    }
}
```

**Result Pattern (avoiding exceptions for expected failures)**:

```csharp
// Generic Result type
public class Result<T>
{
    public T? Value { get; }
    public string? Error { get; }
    public bool IsSuccess => Error is null;

    private Result(T value) { Value = value; }
    private Result(string error) { Error = error; }

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(string error) => new(error);

    public TOut Match<TOut>(Func<T, TOut> onSuccess, Func<string, TOut> onFailure)
        => IsSuccess ? onSuccess(Value!) : onFailure(Error!);
}

// Usage in a service
public async Task<Result<Order>> PlaceOrderAsync(CreateOrderRequest request, CancellationToken ct)
{
    if (request.Items.Count == 0)
        return Result<Order>.Failure("Order must contain at least one item");

    var customer = await _customerRepo.FindAsync(request.CustomerId, ct);
    if (customer is null)
        return Result<Order>.Failure($"Customer {request.CustomerId} not found");

    var order = new Order(customer, request.Items);
    await _orderRepo.SaveAsync(order, ct);

    return Result<Order>.Success(order);
}

// Consume the result
var result = await _orderService.PlaceOrderAsync(request, ct);
return result.Match(
    onSuccess: order => Ok(order),
    onFailure: error => BadRequest(new { error }));
```

**Structured Logging with ILogger and Serilog**:

```csharp
// ILogger with structured logging (semantic parameters, not string interpolation)
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public OrderService(ILogger<OrderService> logger)
    {
        _logger = logger;
    }

    public async Task ProcessAsync(Order order, CancellationToken ct)
    {
        _logger.LogInformation("Processing order {OrderId} for customer {CustomerId}",
            order.Id, order.CustomerId);

        try
        {
            await ExecuteAsync(order, ct);
            _logger.LogInformation("Order {OrderId} processed successfully in {ElapsedMs}ms",
                order.Id, stopwatch.ElapsedMilliseconds);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to process order {OrderId}", order.Id);
            throw;
        }
    }
}

// Serilog configuration in Program.cs
builder.Host.UseSerilog((context, config) => config
    .ReadFrom.Configuration(context.Configuration)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .WriteTo.Console(outputTemplate:
        "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}")
    .WriteTo.Seq("http://localhost:5341"));

// Global exception handling middleware
public class GlobalExceptionMiddleware : IMiddleware
{
    private readonly ILogger<GlobalExceptionMiddleware> _logger;

    public GlobalExceptionMiddleware(ILogger<GlobalExceptionMiddleware> logger)
    {
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context, RequestDelegate next)
    {
        try
        {
            await next(context);
        }
        catch (AppException ex)
        {
            _logger.LogWarning(ex, "Application error: {ErrorCode}", ex.Code);
            context.Response.StatusCode = ex switch
            {
                NotFoundException => StatusCodes.Status404NotFound,
                ConflictException => StatusCodes.Status409Conflict,
                ValidationException => StatusCodes.Status422UnprocessableEntity,
                _ => StatusCodes.Status400BadRequest
            };
            await context.Response.WriteAsJsonAsync(new { error = ex.Code, message = ex.Message });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception");
            context.Response.StatusCode = StatusCodes.Status500InternalServerError;
            await context.Response.WriteAsJsonAsync(new { error = "INTERNAL_ERROR" });
        }
    }
}
```

### Step 7: Write Comprehensive Tests with xUnit

**Fact and Theory Tests**:

```csharp
public class OrderCalculatorTests
{
    // Single test case
    [Fact]
    public void CalculateTotal_WithEmptyItems_ReturnsZero()
    {
        var calculator = new OrderCalculator();
        var result = calculator.CalculateTotal(Array.Empty<OrderItem>());
        Assert.Equal(0m, result);
    }

    // Parameterized tests with InlineData
    [Theory]
    [InlineData(100, 0.10, 90)]
    [InlineData(200, 0.25, 150)]
    [InlineData(50, 0, 50)]
    public void ApplyDiscount_WithVariousInputs_ReturnsExpected(
        decimal price, decimal discount, decimal expected)
    {
        var calculator = new OrderCalculator();
        var result = calculator.ApplyDiscount(price, discount);
        Assert.Equal(expected, result);
    }

    // Complex test data with ClassData
    [Theory]
    [ClassData(typeof(BulkOrderTestData))]
    public void CalculateTotal_WithBulkOrders_AppliesTierPricing(
        List<OrderItem> items, decimal expected)
    {
        var calculator = new OrderCalculator();
        var result = calculator.CalculateTotal(items);
        Assert.Equal(expected, result);
    }
}

public class BulkOrderTestData : IEnumerable<object[]>
{
    public IEnumerator<object[]> GetEnumerator()
    {
        yield return new object[]
        {
            new List<OrderItem> { new("Widget", 10, 5.00m) },
            50.00m
        };
        yield return new object[]
        {
            new List<OrderItem> { new("Widget", 100, 5.00m) },
            450.00m // 10% bulk discount
        };
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
```

**Fixtures and Mocking with Moq**:

```csharp
// Shared test fixture for expensive setup (database, config)
public class DatabaseFixture : IAsyncLifetime
{
    public AppDbContext DbContext { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;
        DbContext = new AppDbContext(options);
        await DbContext.Database.EnsureCreatedAsync();
    }

    public async Task DisposeAsync()
    {
        await DbContext.DisposeAsync();
    }
}

// Use the fixture via IClassFixture<T>
public class OrderServiceTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public OrderServiceTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task PlaceOrder_WithValidData_ReturnsSuccess()
    {
        // Arrange
        var mockEmailSender = new Mock<IEmailSender>();
        mockEmailSender
            .Setup(x => x.SendAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<CancellationToken>()))
            .Returns(Task.CompletedTask);

        var mockLogger = new Mock<ILogger<OrderService>>();

        var service = new OrderService(
            new SqlOrderRepository(_fixture.DbContext),
            mockEmailSender.Object,
            mockLogger.Object);

        var request = new CreateOrderRequest(CustomerId: 1, Items: new[] { new OrderItemDto("Widget", 5) });

        // Act
        var result = await service.PlaceOrderAsync(request, CancellationToken.None);

        // Assert
        Assert.True(result.IsSuccess);
        mockEmailSender.Verify(
            x => x.SendAsync("order-confirmation", It.IsAny<string>(), It.IsAny<CancellationToken>()),
            Times.Once);
    }
}
```

**FluentAssertions and Integration Testing**:

```csharp
// FluentAssertions for readable assertions
using FluentAssertions;

[Fact]
public void Customer_WithGoldTier_ShouldHaveCorrectDiscount()
{
    var customer = new Customer("Alice", CustomerTier.Gold, yearsActive: 6);
    var discount = _calculator.CalculateDiscount(customer);

    discount.Should().Be(0.25m);
    customer.DisplayName.Should().StartWith("Alice");
    customer.Tier.Should().Be(CustomerTier.Gold);
}

[Fact]
public async Task GetOrders_ShouldReturnPagedResults()
{
    var orders = await _service.GetOrdersAsync(page: 1, pageSize: 10);

    orders.Should().NotBeNull();
    orders.Items.Should().HaveCountLessOrEqualTo(10);
    orders.Items.Should().BeInDescendingOrder(o => o.CreatedAt);
    orders.TotalCount.Should().BeGreaterThan(0);
}

// Integration testing with WebApplicationFactory
public class OrdersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public OrdersApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace real database with in-memory for tests
                services.RemoveAll<DbContextOptions<AppDbContext>>();
                services.AddDbContext<AppDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        }).CreateClient();
    }

    [Fact]
    public async Task GetOrders_ReturnsOkWithOrders()
    {
        var response = await _client.GetAsync("/api/orders");

        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var content = await response.Content.ReadFromJsonAsync<PagedResult<OrderDto>>();
        content.Should().NotBeNull();
        content!.Items.Should().NotBeEmpty();
    }

    [Fact]
    public async Task CreateOrder_WithInvalidData_ReturnsBadRequest()
    {
        var request = new CreateOrderRequest(CustomerId: 0, Items: Array.Empty<OrderItemDto>());
        var response = await _client.PostAsJsonAsync("/api/orders", request);

        response.StatusCode.Should().Be(HttpStatusCode.UnprocessableEntity);
    }
}
```

## Best Practices

- **Prefer async all the way** - Avoid mixing sync and async code; do not call `.Result` or `.Wait()` on tasks
- **Use CancellationToken everywhere** - Pass it through every async method signature and honor it
- **Small interfaces** - Follow Interface Segregation; clients should not depend on methods they do not use
- **Immutable data** - Use records and init-only setters for DTOs and value objects
- **Validate at boundaries** - Use FluentValidation or DataAnnotations at API entry points, not deep in domain logic
- **Log structurally** - Use semantic message templates with named parameters, never string interpolation in log calls
- **Fail fast** - Validate configuration at startup with `ValidateOnStart()`; do not let misconfiguration surface at runtime
- **Dispose properly** - Implement `IAsyncDisposable` for types that hold unmanaged or pooled resources

## Common Patterns

### Pattern 1: Mediator with CQRS

```csharp
// Command and handler using MediatR
public record CreateOrderCommand(int CustomerId, List<OrderItemDto> Items) : IRequest<Result<int>>;

public class CreateOrderHandler : IRequestHandler<CreateOrderCommand, Result<int>>
{
    private readonly IOrderRepository _orders;
    private readonly ILogger<CreateOrderHandler> _logger;

    public CreateOrderHandler(IOrderRepository orders, ILogger<CreateOrderHandler> logger)
    {
        _orders = orders;
        _logger = logger;
    }

    public async Task<Result<int>> Handle(CreateOrderCommand command, CancellationToken ct)
    {
        var order = Order.Create(command.CustomerId, command.Items);
        await _orders.SaveAsync(order, ct);

        _logger.LogInformation("Order {OrderId} created for customer {CustomerId}",
            order.Id, command.CustomerId);

        return Result<int>.Success(order.Id);
    }
}

// Query and handler (read side)
public record GetOrderQuery(int OrderId) : IRequest<OrderDto?>;

public class GetOrderHandler : IRequestHandler<GetOrderQuery, OrderDto?>
{
    private readonly IReadOnlyRepository<Order> _orders;

    public GetOrderHandler(IReadOnlyRepository<Order> orders) => _orders = orders;

    public async Task<OrderDto?> Handle(GetOrderQuery query, CancellationToken ct)
    {
        var order = await _orders.FindAsync(query.OrderId, ct);
        return order is null ? null : OrderDto.FromDomain(order);
    }
}

// Minimal API endpoint using MediatR
app.MapPost("/api/orders", async (CreateOrderCommand command, IMediator mediator, CancellationToken ct) =>
{
    var result = await mediator.Send(command, ct);
    return result.Match(
        onSuccess: id => Results.Created($"/api/orders/{id}", new { id }),
        onFailure: error => Results.BadRequest(new { error }));
});
```

### Pattern 2: Pipeline Behavior (cross-cutting concerns)

```csharp
// Validation pipeline behavior that runs before every handler
public class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        var context = new ValidationContext<TRequest>(request);
        var failures = (await Task.WhenAll(
                _validators.Select(v => v.ValidateAsync(context, ct))))
            .SelectMany(r => r.Errors)
            .Where(f => f is not null)
            .ToList();

        if (failures.Count > 0)
            throw new ValidationException(failures.Select(f =>
                new ValidationError(f.PropertyName, f.ErrorMessage)));

        return await next();
    }
}

// Register the pipeline
builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
```

## Quality Checklist

- [ ] All async methods accept and forward CancellationToken
- [ ] No `.Result` or `.Wait()` calls on tasks (async all the way)
- [ ] LINQ queries use deferred execution correctly (materialized only when needed)
- [ ] Generic constraints are as tight as necessary
- [ ] Dependency injection lifetimes are correct (no captive dependency problems)
- [ ] Structured logging uses message templates, not string interpolation
- [ ] Custom exceptions inherit from a common base
- [ ] Tests use Arrange-Act-Assert and meaningful assertion messages
- [ ] Integration tests replace external dependencies with test doubles

## Related Skills

- `typescript-expert` - Frontend/fullstack with Blazor WASM interop
- `sql-expert` - Entity Framework Core and raw SQL optimization
- `cicd-architect` - .NET CI/CD pipelines with GitHub Actions
- `code-quality` - Static analysis with Roslyn analyzers
- `kubernetes-expert` - Containerized .NET microservices on K8s

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Microsoft C# documentation, .NET design guidelines, enterprise patterns


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
