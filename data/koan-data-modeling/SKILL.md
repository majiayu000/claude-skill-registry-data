---
name: koan-data-modeling
description: Aggregate boundaries, relationships, lifecycle hooks, value objects
---

# Koan Data Modeling

## Core Principle

**Entities are aggregates that encapsulate business logic and define clear boundaries.** Use lifecycle hooks for invariants, value objects for cohesive data, and navigation helpers for relationships.

## Quick Reference

### Define Aggregate Boundary

```csharp
public class Order : Entity<Order>
{
    public string CustomerId { get; set; } = "";
    public Money Total { get; private set; } = new(0m, "USD");
    public OrderStatus Status { get; private set; } = OrderStatus.Draft;

    // Business methods
    public void MarkShipped() => Status = OrderStatus.Shipped;

    // Navigation helper
    public Task<Customer?> GetCustomer(CancellationToken ct = default) =>
        Customer.Get(CustomerId, ct);

    // Domain query
    public static Task<List<Order>> RecentOrders(int days = 7, CancellationToken ct = default) =>
        Query(o => o.Created > DateTimeOffset.UtcNow.AddDays(-days), ct);
}
```

### Value Objects

```csharp
public record Money(decimal Amount, string Currency);
public record Address(string Street, string City, string State, string Zip);

public class Invoice : Entity<Invoice>
{
    public Money Total { get; set; } = new(0m, "USD");
    public Address ShippingAddress { get; set; } = new("", "", "", "");
}
```

### Lifecycle Hooks

```csharp
public static class ProductLifecycle
{
    public static void Configure(EntityLifecycleBuilder<Product> pipeline)
    {
        pipeline.ProtectAll()
                .Allow(p => p.Price, p => p.Description)
                .BeforeUpsert(async (ctx, next) =>
                {
                    if (ctx.Entity.Price < 0)
                        throw new InvalidOperationException("Price cannot be negative");
                    await next();
                })
                .AfterLoad(ctx => ctx.Entity.FormattedPrice = $"${ctx.Entity.Price:F2}");
    }
}
```

### Relationships

```csharp
public class Todo : Entity<Todo>
{
    public string UserId { get; set; } = "";
    public string? CategoryId { get; set; }

    // Navigation helpers
    public Task<User?> GetUser(CancellationToken ct = default) =>
        User.Get(UserId, ct);

    public Task<Category?> GetCategory(CancellationToken ct = default) =>
        string.IsNullOrEmpty(CategoryId) ? Task.FromResult<Category?>(null)
            : Category.Get(CategoryId, ct);

    public Task<List<TodoItem>> GetItems(CancellationToken ct = default) =>
        TodoItem.Query(i => i.TodoId == Id, ct);
}
```

## When This Skill Applies

- ✅ Designing domain models
- ✅ Complex entity relationships
- ✅ Business logic encapsulation
- ✅ Data validation patterns
- ✅ Soft deletes and audit trails
- ✅ Entity lifecycle management

## Reference Documentation

- **Full Guide:** `docs/guides/data-modeling.md`
- **Entity Patterns:** `docs/examples/entity-pattern-recipes.md`
- **Sample:** `samples/S1.Web/` (Relationship patterns)
