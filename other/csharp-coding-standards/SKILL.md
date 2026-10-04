---
name: csharp-coding-standards
description: Defines the C# coding standards, patterns, and conventions to be applied consistently across all C# projects. Rules cover naming, structure, async patterns, null handling, dependency injection, logging, result patterns, and formatting. Apply these rules uniformly in all production code.
---

# C# Coding Standards

## Description

Defines the C# coding standards, patterns, and conventions to be applied consistently across all C# projects. Rules cover naming, structure, async patterns, null handling, dependency injection, logging, result patterns, and formatting. Apply these rules uniformly in all production code.

---

## 1. File & Namespace Structure

### 1.1 File-Scoped Namespaces

Always use **file-scoped namespaces**:

```csharp
// ✅ Correct
namespace MyApp.Core.Validators;

internal class OrderValidator { }

// ❌ Wrong
namespace MyApp.Core.Validators
{
    internal class OrderValidator { }
}
```

### 1.2 Using Directives

- Place `using` directives **outside** the namespace.
- Group: System namespaces first, then others ordered alphabetically – separated by a blank line.
- Use implicit usings where available; add explicit usings only when needed for disambiguation.

```csharp
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.Logging;
using MyApp.Core.Abstractions;
using MyApp.Domain;
```

### 1.3 One Type Per File

Each file contains exactly one top-level type. The file name must match the type name exactly.

---

## 2. Naming Conventions

### 2.1 Types

| Kind | Convention | Example |
|---|---|---|
| Classes | PascalCase | `OrderValidator`, `UserService` |
| Interfaces | `I` prefix + PascalCase | `IOrderRepository`, `IUserService` |
| Enums | PascalCase | `OrderStatus`, `PaymentMethod` |
| Structs | PascalCase | `Money`, `DateRange` |
| Records | PascalCase | `AppConfiguration`, `UserSettings` |

### 2.2 Members

| Kind | Convention | Example |
|---|---|---|
| Public properties | PascalCase | `CreatedAt`, `TotalAmount` |
| Public methods | PascalCase | `CreateOrder`, `ValidatePayment` |
| Private fields | `_camelCase` (underscore prefix) | `_repository`, `_logger` |
| Constants | PascalCase | `DefaultTimeout`, `MaxRetryCount` |
| Local variables | camelCase | `orderId`, `serializedData` |
| Method parameters | camelCase | `cancellationToken`, `userId` |
| Lambda parameters | Short camelCase | `x =>`, `e =>`, `o =>` |

### 2.3 Async Methods

> **All async methods MUST end with the `Async` suffix without exception.**

```csharp
// ✅ Correct
public async Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken);

// ❌ Wrong – missing Async suffix
public async Task<Order?> GetById(Guid id, CancellationToken cancellationToken);
```

This applies to:
- Interface declarations
- Public and internal implementation methods
- Private helper methods

---

## 3. Access Modifiers & Sealed Classes

### 3.1 Least Privilege

- Prefer `internal` for implementation types; use `public` only for types that are part of the public API surface.
- Implementation classes registered via DI should be `internal sealed`.
- Types that implement a public interface and form the public API are `public sealed`.

```csharp
// ✅ Correct: public sealed for types exposed via public interface
public sealed class OrderService : IOrderService { }

// ✅ Correct: internal sealed for infrastructure implementations
internal sealed class SqlOrderRepository : IOrderRepository { }
```

### 3.2 `sealed` Usage

Mark classes `sealed` by default unless inheritance is explicitly required. This prevents unintended derivation and enables JIT optimizations.

---

## 4. Null Handling & Defensive Programming

### 4.1 Nullable Reference Types

- Enable nullable context for all projects (`<Nullable>enable</Nullable>`).
- Annotate all nullable references explicitly with `?`.
- Avoid the null-forgiving operator (`!`) without an inline comment explaining why it is safe.
- Prefer early-return guards over deeply nested null checks.

```csharp
// ✅ Early return guard
if (id is null || id.Length == 0)
{
    return null;
}
```

### 4.2 Argument Validation

Use modern `ArgumentNullException` helpers for public/internal method boundaries:

```csharp
// ✅ Correct
ArgumentNullException.ThrowIfNull(order);
ArgumentNullException.ThrowIfNullOrEmpty(order.UserName);
```

### 4.3 Null Propagation & Coalescing

Prefer `?.` and `??` / `??=` over verbose null checks in expressions:

```csharp
// ✅ Correct
return items?.Select(x => x.ToDto()).ToArray();

var name = input?.Trim() ?? string.Empty;
```

---

## 5. Constructor Injection & Dependency Injection

### 5.1 Constructor Injection

Always inject dependencies via the constructor. Store them as `private readonly` fields prefixed with `_`.

```csharp
private readonly IOrderRepository _orderRepository;
private readonly ILogger<OrderService> _logger;

public OrderService(IOrderRepository orderRepository, ILogger<OrderService> logger)
{
    _orderRepository = orderRepository;
    _logger = logger;
}
```

### 5.2 Options Pattern

Access configuration via `IOptions<T>`. Extract `.Value` in the constructor and store as a field – do not access `.Value` repeatedly at call sites.

```csharp
private readonly AppConfiguration _configuration;

public OrderService(IOptions<AppConfiguration> options)
{
    _configuration = options.Value;
}
```

### 5.3 DI Registration

Centralize all service registrations in a dedicated `DependencyInjection.cs` static class with `IServiceCollection` extension methods.

```csharp
public static class DependencyInjection
{
    public static void AddMyFeature(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddTransient<IOrderService, OrderService>();
        services.AddKeyedTransient<IPaymentStrategy, CreditCardStrategy>("creditcard");
    }
}
```

Lifetime guidance:
- `AddTransient` – stateless, short-lived services.
- `AddSingleton` – thread-safe, shared-state services (e.g., `TimeProvider`, static caches).
- `AddKeyedTransient` / `AddKeyedSingleton` – strategy-pattern registrations keyed by a discriminator.

---

## 6. Async / Await

### 6.1 Always Propagate CancellationToken

Every public and internal async method should accept a `CancellationToken` as its **last parameter**:

```csharp
// ✅ Correct
Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
Task SaveAsync(Order order, CancellationToken cancellationToken);
```

### 6.2 No `ConfigureAwait(false)` in Application Code

Do not use `.ConfigureAwait(false)` in application-layer and library code targeting ASP.NET Core. Reserve it only for low-level infrastructure libraries where synchronization context must be avoided explicitly.

### 6.3 Never Use `async void`

Never use `async void` except for event handlers. Always return `Task` or `Task<T>`.

### 6.4 Async Locks via SemaphoreSlim

Use `SemaphoreSlim` for async-compatible critical sections. Always release in a `finally` block:

```csharp
private static readonly SemaphoreSlim Lock = new(1, 1);

await Lock.WaitAsync(cancellationToken);
try
{
    // Critical section
}
finally
{
    Lock.Release();
}
```

### 6.5 Return Task Directly for Pass-Through Methods

When a method only delegates to a single async call with no surrounding logic, return the `Task` directly to avoid an unnecessary state machine:

```csharp
// ✅ Correct – no state machine overhead
private Task<string?> GetCachedValueAsync(string key, CancellationToken cancellationToken)
{
    return _cache.GetStringAsync(key, cancellationToken);
}
```

---

## 7. Result Pattern

### 7.1 Internal Results

Do not throw exceptions for expected, recoverable validation failures. Use typed result objects that carry success/failure state and an optional message:

```csharp
// Validator result (IsValid + Message)
public static ValidationResult Valid() => new(true);
public static ValidationResult Invalid(string message) => new(false, message);

// Handler/operation result (Value + HasError + Message)
public Result<T> Execute(...)
{
    if (inputIsInvalid)
        return new Result<T>("Validation failed: input cannot be null");

    return new Result<T>(computedValue);
}
```

### 7.2 Public Results

Public-facing operation results use static factory methods for readability:

```csharp
// ✅ Correct
return OperationResult.Success();
return OperationResult.Failure("The record was not found");
```

### 7.3 Fail Fast, Return Early

Validate all inputs at the top of the method. Return early on error. Do not let invalid state propagate deep into a method body.

```csharp
var validation = _validator.Validate(request);
if (!validation.IsValid)
{
    return OperationResult.Failure(validation.Message!);
}

// proceed with valid data only
```

---

## 8. Logging

### 8.1 Structured Logging

Always use **named placeholder syntax** – never string interpolation in log messages:

```csharp
// ✅ Correct
_logger.LogWarning("Order '{OrderId}' was not found for user '{UserId}'", orderId, userId);

// ❌ Wrong
_logger.LogWarning($"Order '{orderId}' was not found for user '{userId}'");
```

### 8.2 Log Level Selection

| Situation | Level |
|---|---|
| Normal successful operation | `LogDebug` |
| Handled failure or unexpected but recoverable condition | `LogWarning` |
| Unrecoverable exception or system error | `LogError` |
| Sensitive / PII data | Do not log – redact |

### 8.3 Logger Injection

Always inject `ILogger<T>` where `T` is the exact enclosing class. Do not share logger instances across types.

---

## 9. Collections & LINQ

### 9.1 Collection Expressions

Use C# 12+ collection expressions (`[]`) for empty collections and simple inline initialization:

```csharp
// ✅ Correct
string[] tags = [];
Items = existingItems ?? [],
return [];
```

### 9.2 LINQ Style

- Prefer **method syntax** over query syntax.
- Chain transformations fluently (`.Where()`, `.Select()`, `.OrderBy()`) and materialize at the end with `.ToList()` or `.ToArray()`.
- Avoid intermediate `.ToList()` calls mid-chain; defer materialization.

```csharp
// ✅ Correct
return orders
    .Where(o => o.IsActive)
    .Select(o => o.ToSummaryDto())
    .ToArray();
```

### 9.3 Empty Collection Checks

Prefer `.Length == 0` or `.Count == 0` over `!collection.Any()` in performance-sensitive paths.

---

## 10. Pattern Matching & Switch Expressions

Use switch expressions for exhaustive value dispatch instead of chains of `if`/`else if`:

```csharp
// ✅ Correct
var label = status switch
{
    OrderStatus.Pending   => "Awaiting confirmation",
    OrderStatus.Confirmed => "Confirmed",
    OrderStatus.Shipped   => "On the way",
    _                     => "Unknown",
};
```

Prefer `is null` / `is not null` over `== null` / `!= null` for reference type null checks:

```csharp
if (order is null) { ... }
if (result is not null) { ... }
```

---

## 11. Domain Model Design

### 11.1 Required Properties

Use the `required` keyword for mandatory properties to enforce initialization at the call site:

```csharp
public sealed class Order
{
    public required Guid Id { get; set; }
    public required string CustomerName { get; set; }
    public required decimal TotalAmount { get; set; }
}
```

### 11.2 Sealed Domain Models

Seal domain and result classes that are not designed for inheritance:

```csharp
public sealed class Order { }
public sealed class OperationResult { }
```

---

## 12. XML Documentation

### 12.1 Public API

All `public` interfaces, classes, and their members must carry full XML doc comments:

```csharp
/// <summary>
/// Retrieves an order by its unique identifier.
/// </summary>
/// <param name="id">The unique identifier of the order.</param>
/// <param name="cancellationToken">A cancellation token.</param>
/// <returns>The order if found; otherwise, <c>null</c>.</returns>
Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
```

### 12.2 Internal Types

XML doc comments are optional on `internal` types but strongly encouraged for any non-trivial logic.

---

## 13. Constants & Magic Values

### 13.1 Named Constants

Never use magic numbers or strings inline. Declare them as `private const` or `private static readonly`:

```csharp
private const int MaxRetryCount = 3;
private const string DefaultCacheKeyPrefix = "order";
private const int DefaultTimeoutSeconds = 60;
```

### 13.2 Constants Organization

Group related constants into dedicated static classes inside a `Constants/` folder. One class per logical domain (e.g., `CacheKeys`, `HeaderNames`, `ErrorMessages`).

---

## 14. Formatting

### 14.1 Indentation & Whitespace

- **Indent size**: 4 spaces – no tabs.
- **Line endings**: CRLF.
- One blank line between method bodies.
- One blank line between property groups.

### 14.2 Braces

Always use braces, even for single-line `if` / `else` / `for` / `foreach` bodies:

```csharp
// ✅ Correct
if (order is null)
{
    return OperationResult.Failure("Order not found");
}

// ❌ Wrong
if (order is null)
    return OperationResult.Failure("Order not found");
```

### 14.3 Expression-Bodied Members

| Member Type | Preferred Style |
|---|---|
| Properties | Expression-bodied (`=>`) allowed |
| Short indexers | Expression-bodied allowed |
| Methods | **Block body** preferred |
| Constructors | **Block body** required |
| Lambdas | Expression-bodied preferred |
| Local functions | Block body preferred |

### 14.4 Long Parameter Lists

Break constructor or method parameters onto separate lines when there are 3 or more:

```csharp
public OrderService(
    IOrderRepository orderRepository,
    IPaymentService paymentService,
    IOptions<AppConfiguration> options,
    ILogger<OrderService> logger)
```

### 14.5 Object & Collection Initializers

Always use object initializer syntax for domain objects and DTOs. Include a trailing comma after the last member:

```csharp
var order = new Order
{
    Id = Guid.NewGuid(),
    CustomerName = request.CustomerName.Trim(),
    TotalAmount = request.Amount,
    Tags = [],
};
```

---

## 15. Extension Methods

- Place extension methods in a dedicated `Extensions/` folder.
- One static class per extended type or logical concept: `StringExtensions`, `EnumExtensions`, `DateTimeExtensions`.
- All extension classes are `public static`.
- Generic constraints should be as tight as the use case requires.

```csharp
public static class EnumExtensions
{
    public static string GetSerializedValue<T>(this T value) where T : Enum { ... }
    public static T ToEnum<T>(this string value) where T : struct, Enum { ... }
    public static T? ToNullableEnum<T>(this string? value) where T : struct, Enum { ... }
}
```

---

## 16. Security-Sensitive Code

- Never log raw sensitive bytes, private key material, passwords, tokens, or PII.
- Use constant-time or span-based byte array comparison helpers to prevent timing attacks – never use `==` or `SequenceEqual` for security-critical comparisons.
- Always sanitize user input (`.Trim()`) before storing, comparing, or forwarding.
- Validate all untrusted input at the boundary layer – do not rely on inner layers to catch invalid data.

---

## Quick Reference Checklist

Before submitting any C# file, verify:

- [ ] File-scoped namespace used
- [ ] All async methods end with the `Async` suffix
- [ ] `CancellationToken` is the last parameter of every async method
- [ ] Nullable reference types annotated correctly – no unexplained `!`
- [ ] Braces on every `if` / `else` / `for` / `foreach`
- [ ] No magic numbers or strings – all constants named
- [ ] Structured logging – no string interpolation in log calls
- [ ] Public API members have XML documentation
- [ ] Result pattern used instead of exceptions for expected failures
