---
name: cqrs-architecture
description: CQRS pattern implementation and query optimization
allowed-tools: Read, Glob, Grep, Write, Edit
---

# CQRS Architecture Skill

Design and implement Command Query Responsibility Segregation patterns for scalable systems.

## MANDATORY: Documentation-First Approach

Before implementing CQRS:

1. **Invoke `docs-management` skill** for CQRS patterns
2. **Verify patterns** via MCP servers (perplexity, context7)
3. **Base guidance on established CQRS literature**

## CQRS Fundamentals

```text
Traditional vs CQRS:

TRADITIONAL (Single Model):
┌─────────────────────────────────┐
│         Application            │
├─────────────────────────────────┤
│      Domain Model              │
│  (Reads + Writes)              │
├─────────────────────────────────┤
│         Database               │
└─────────────────────────────────┘

CQRS (Separated Models):
┌───────────────┐    ┌───────────────┐
│ Command Side  │    │  Query Side   │
│ (Write Model) │    │ (Read Model)  │
├───────────────┤    ├───────────────┤
│ Domain Logic  │    │ DTO/Views     │
│ Aggregates    │    │ Projections   │
├───────────────┤    ├───────────────┤
│ Write DB      │───►│ Read DB       │
└───────────────┘    └───────────────┘
```

## CQRS Levels

### Level 1: Logical Separation

```text
Same database, separate code paths:

┌─────────────────────────────────────┐
│           Application               │
├──────────────────┬──────────────────┤
│ Command Handlers │ Query Handlers   │
│ - Validation     │ - Direct SQL     │
│ - Domain Logic   │ - Projections    │
│ - Events         │ - DTOs           │
├──────────────────┴──────────────────┤
│           Single Database           │
└─────────────────────────────────────┘

Benefits:
✓ Clean separation in code
✓ Simple deployment
✓ Single source of truth
✓ Good starting point
```

### Level 2: Separate Read Models

```text
Same write DB, separate read DB:

┌─────────────────┐    ┌─────────────────┐
│ Command Side    │    │  Query Side     │
├─────────────────┤    ├─────────────────┤
│ Command Handler │    │ Query Handler   │
│ Domain Model    │    │ DTOs            │
├─────────────────┤    ├─────────────────┤
│ Write Database  │───►│ Read Database   │
│ (Normalized)    │sync│ (Denormalized)  │
└─────────────────┘    └─────────────────┘

Benefits:
✓ Optimized read performance
✓ Scale reads independently
✓ Different storage technologies
✓ Eventually consistent reads
```

### Level 3: Event-Sourced CQRS

```text
Event store as write model, projections as read:

┌─────────────────┐    ┌─────────────────┐
│ Command Side    │    │  Query Side     │
├─────────────────┤    ├─────────────────┤
│ Command Handler │    │ Query Handler   │
│ Aggregate       │    │ Read Models     │
├─────────────────┤    ├─────────────────┤
│ Event Store     │───►│ Multiple Read   │
│ (Append-only)   │    │ Databases       │
└─────────────────┘    └─────────────────┘

Benefits:
✓ Complete audit trail
✓ Temporal queries
✓ Multiple projections
✓ Rebuild read models
```

## Command Side Design

### Command Structure

```csharp
// Command Definition
public record PlaceOrderCommand(
    Guid CustomerId,
    List<OrderItemDto> Items,
    string ShippingAddress
) : ICommand<OrderId>;

// Command Handler
public class PlaceOrderHandler : ICommandHandler<PlaceOrderCommand, OrderId>
{
    private readonly IOrderRepository _repository;
    private readonly IEventPublisher _events;

    public async Task<OrderId> HandleAsync(
        PlaceOrderCommand command,
        CancellationToken ct)
    {
        // Validation
        if (!command.Items.Any())
            throw new ValidationException("Order must have items");

        // Domain logic
        var order = Order.Create(
            command.CustomerId,
            command.Items.Select(i => new OrderItem(i.ProductId, i.Quantity)));

        // Persistence
        await _repository.SaveAsync(order, ct);

        // Publish events
        await _events.PublishAsync(order.GetDomainEvents(), ct);

        return order.Id;
    }
}
```

### Command Patterns

```text
Command Best Practices:

NAMING:
- Imperative: PlaceOrder, CancelOrder, UpdateAddress
- Include context: not just "Create" but "CreateOrder"

STRUCTURE:
- Immutable (records)
- Only data needed for operation
- No business logic in command

VALIDATION:
- Input validation in handler
- Business validation in domain
- Return meaningful errors

IDEMPOTENCY:
- Include idempotency key
- Handle duplicate submissions
- Return same result for retries
```

## Query Side Design

### Query Structure

```csharp
// Query Definition
public record GetOrderByIdQuery(Guid OrderId) : IQuery<OrderDetailsDto>;

// Query Handler
public class GetOrderByIdHandler : IQueryHandler<GetOrderByIdQuery, OrderDetailsDto>
{
    private readonly IReadDbContext _db;

    public async Task<OrderDetailsDto> HandleAsync(
        GetOrderByIdQuery query,
        CancellationToken ct)
    {
        var order = await _db.OrderDetails
            .Where(o => o.OrderId == query.OrderId)
            .Select(o => new OrderDetailsDto
            {
                OrderId = o.OrderId,
                CustomerName = o.Customer.Name,
                Items = o.Items.Select(i => new OrderItemDto
                {
                    ProductName = i.ProductName,
                    Quantity = i.Quantity,
                    Price = i.Price
                }).ToList(),
                Status = o.Status,
                TotalAmount = o.TotalAmount
            })
            .FirstOrDefaultAsync(ct);

        return order ?? throw new NotFoundException("Order not found");
    }
}
```

### Read Model Optimization

```text
Query Optimization Strategies:

1. DENORMALIZATION
   - Pre-join data
   - Store calculated values
   - Flatten hierarchies

2. MATERIALIZED VIEWS
   - Database-managed
   - Automatically updated
   - Query-optimized

3. CACHING
   - In-memory for hot data
   - Distributed for shared
   - Invalidate on events

4. SPECIALIZED STORES
   - ElasticSearch for search
   - Redis for real-time
   - ClickHouse for analytics
```

## Synchronization Patterns

### Projection from Events

```csharp
// Event-Driven Projection
public class OrderProjection : IEventHandler<OrderPlaced>, IEventHandler<OrderShipped>
{
    private readonly IOrderViewRepository _views;

    public async Task HandleAsync(OrderPlaced @event, CancellationToken ct)
    {
        var view = new OrderView
        {
            OrderId = @event.OrderId,
            CustomerId = @event.CustomerId,
            Status = "Placed",
            PlacedAt = @event.Timestamp,
            ItemCount = @event.Items.Count,
            TotalAmount = @event.TotalAmount
        };

        await _views.InsertAsync(view, ct);
    }

    public async Task HandleAsync(OrderShipped @event, CancellationToken ct)
    {
        await _views.UpdateAsync(@event.OrderId, view =>
        {
            view.Status = "Shipped";
            view.ShippedAt = @event.Timestamp;
            view.TrackingNumber = @event.TrackingNumber;
        }, ct);
    }
}
```

### Consistency Patterns

```text
Consistency Options:

STRONG CONSISTENCY (Same Transaction):
┌──────────┐    ┌──────────┐
│ Command  │───►│ Read     │
│ DB       │    │ Model    │
│          │    │ Update   │
└──────────┴────┴──────────┘
     Same Transaction

EVENTUAL CONSISTENCY (Async):
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Command  │───►│ Message  │───►│ Read     │
│ DB       │    │ Queue    │    │ Model    │
└──────────┘    └──────────┘    └──────────┘
     Async, Eventually Consistent

HYBRID (Read-Your-Writes):
- Immediate read from command side
- Eventually consistent for others
- Version checking in queries
```

## MediatR Implementation

### Setup with MediatR

```csharp
// Registration
services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly);
});

// Command/Query Interfaces
public interface ICommand<TResult> : IRequest<TResult> { }
public interface IQuery<TResult> : IRequest<TResult> { }

// Handler Interfaces
public interface ICommandHandler<TCommand, TResult>
    : IRequestHandler<TCommand, TResult>
    where TCommand : ICommand<TResult> { }

public interface IQueryHandler<TQuery, TResult>
    : IRequestHandler<TQuery, TResult>
    where TQuery : IQuery<TResult> { }
```

### Pipeline Behaviors

```csharp
// Validation Behavior
public class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        var failures = _validators
            .Select(v => v.Validate(request))
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();

        if (failures.Any())
            throw new ValidationException(failures);

        return await next();
    }
}

// Logging Behavior
public class LoggingBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        _logger.LogInformation("Handling {RequestType}", typeof(TRequest).Name);
        var response = await next();
        _logger.LogInformation("Handled {RequestType}", typeof(TRequest).Name);
        return response;
    }
}
```

## API Design with CQRS

### REST API Pattern

```csharp
[ApiController]
[Route("api/orders")]
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;

    // Commands use POST/PUT/DELETE
    [HttpPost]
    public async Task<ActionResult<OrderId>> PlaceOrder(
        [FromBody] PlaceOrderCommand command,
        CancellationToken ct)
    {
        var orderId = await _mediator.Send(command, ct);
        return CreatedAtAction(nameof(GetOrder), new { id = orderId }, orderId);
    }

    // Queries use GET
    [HttpGet("{id}")]
    public async Task<ActionResult<OrderDetailsDto>> GetOrder(
        Guid id,
        CancellationToken ct)
    {
        var order = await _mediator.Send(new GetOrderByIdQuery(id), ct);
        return Ok(order);
    }

    [HttpGet]
    public async Task<ActionResult<PagedResult<OrderSummaryDto>>> ListOrders(
        [FromQuery] ListOrdersQuery query,
        CancellationToken ct)
    {
        var orders = await _mediator.Send(query, ct);
        return Ok(orders);
    }
}
```

## When to Use CQRS

### Good Fit

```text
CQRS Works Well For:

✓ Complex reads AND writes
  - Different optimization needs
  - Read/write ratio imbalance

✓ Multiple views of data
  - Different query patterns
  - Multiple UI requirements

✓ Collaborative domains
  - Many concurrent users
  - Complex validation

✓ Event-driven systems
  - Microservices
  - Async processing

✓ Scalability requirements
  - Independent read/write scaling
  - Performance optimization
```

### Poor Fit

```text
CQRS May Not Fit:

✗ Simple CRUD applications
  - Overhead not justified
  - Same model works fine

✗ Small team/project
  - Added complexity
  - Maintenance burden

✗ Strong consistency required
  - Real-time requirements
  - Financial transactions

✗ Unknown query patterns
  - Ad-hoc reporting
  - BI requirements
```

## Workflow

When implementing CQRS:

1. **Evaluate Fit**: Is CQRS appropriate for this context?
2. **Choose Level**: Logical, physical, or event-sourced?
3. **Design Commands**: Identify write operations
4. **Design Queries**: Identify read patterns
5. **Plan Sync**: How will read models be updated?
6. **Implement Pipeline**: Validation, logging, etc.
7. **Consider Consistency**: What guarantees are needed?
8. **Test Both Sides**: Command and query testing

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
