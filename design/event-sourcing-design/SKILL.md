---
name: event-sourcing-design
description: Event sourcing patterns and design decisions
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Event Sourcing Design Skill

Design event-sourced systems with proper event store, projection, and versioning patterns.

## MANDATORY: Documentation-First Approach

Before designing event sourcing:

1. **Invoke `docs-management` skill** for event sourcing patterns
2. **Verify patterns** via MCP servers (perplexity, context7)
3. **Base guidance on established event sourcing literature**

## Event Sourcing Fundamentals

```text
Traditional vs Event Sourcing:

TRADITIONAL (State-Based):
┌─────────────┐    ┌─────────────┐
│ Application │───►│  Database   │
│             │    │  (Current   │
│             │    │   State)    │
└─────────────┘    └─────────────┘

EVENT SOURCING:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Application │───►│ Event Store │───►│ Projections │
│             │    │ (All Events)│    │ (Read Views)│
└─────────────┘    └─────────────┘    └─────────────┘
                         │
                         ▼
                   [Complete History]
```

## When to Use Event Sourcing

### Good Fit Scenarios

```text
Event Sourcing Works Well For:

✓ AUDIT REQUIREMENTS
  - Complete history needed
  - Regulatory compliance
  - Legal evidence

✓ COMPLEX DOMAIN LOGIC
  - Business rules evolve
  - Temporal queries needed
  - "What if" analysis

✓ HIGH-VALUE AGGREGATES
  - Financial transactions
  - Medical records
  - Legal documents

✓ COLLABORATION SCENARIOS
  - Conflict resolution
  - Merge capabilities
  - Offline sync

✓ EVENT-DRIVEN ARCHITECTURE
  - Microservices integration
  - Async processing
  - Real-time updates
```

### Poor Fit Scenarios

```text
Event Sourcing May Not Fit:

✗ SIMPLE CRUD
  - Basic data entry
  - No audit needs
  - Simple queries

✗ FREQUENT UPDATES
  - High-velocity small changes
  - Real-time streaming data
  - IoT sensor data

✗ LARGE AGGREGATES
  - Many events per aggregate
  - Performance concerns
  - Memory constraints

✗ AD-HOC QUERIES
  - Complex reporting
  - Unknown query patterns
  - BI/analytics focus
```

## Event Store Design

### Event Structure

```csharp
// C# Event Structure Example
public record DomainEvent
{
    public required Guid EventId { get; init; }
    public required string EventType { get; init; }
    public required Guid AggregateId { get; init; }
    public required string AggregateType { get; init; }
    public required long Version { get; init; }
    public required DateTimeOffset Timestamp { get; init; }
    public required string Payload { get; init; }  // JSON
    public required string? Metadata { get; init; } // Correlation, causation
}
```

### Stream Organization

```text
Stream Strategies:

BY AGGREGATE (Most Common):
Stream: "Order-{orderId}"
Events: OrderCreated, ItemAdded, OrderPaid, ...

BY CATEGORY:
Stream: "$ce-Order" (category projection)
All events for all orders

BY CORRELATION:
Stream: "Saga-{correlationId}"
Events across aggregates for one workflow

GLOBAL STREAM:
Stream: "$all"
All events in order (for projections)
```

### Event Store Schema

```sql
-- PostgreSQL Event Store Schema
CREATE TABLE events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stream_id VARCHAR(255) NOT NULL,
    stream_position BIGINT NOT NULL,
    global_position BIGSERIAL NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    metadata JSONB,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(stream_id, stream_position)
);

CREATE INDEX idx_events_stream ON events(stream_id, stream_position);
CREATE INDEX idx_events_global ON events(global_position);
CREATE INDEX idx_events_type ON events(event_type);
```

## Aggregate Design

### Aggregate Structure

```csharp
// C# Aggregate Example
public abstract class Aggregate
{
    public Guid Id { get; protected set; }
    public long Version { get; protected set; } = -1;

    private readonly List<object> _uncommittedEvents = new();

    protected void Apply(object @event)
    {
        When(@event);
        _uncommittedEvents.Add(@event);
    }

    protected abstract void When(object @event);

    public void Load(IEnumerable<object> events)
    {
        foreach (var @event in events)
        {
            When(@event);
            Version++;
        }
    }

    public IReadOnlyList<object> GetUncommittedEvents()
        => _uncommittedEvents;

    public void ClearUncommittedEvents()
        => _uncommittedEvents.Clear();
}

public class Order : Aggregate
{
    private OrderStatus _status;
    private List<OrderItem> _items = new();

    public void Place(Guid customerId, List<OrderItem> items)
    {
        if (_status != OrderStatus.Draft)
            throw new InvalidOperationException("Order already placed");

        Apply(new OrderPlaced(Id, customerId, items, DateTimeOffset.UtcNow));
    }

    protected override void When(object @event)
    {
        switch (@event)
        {
            case OrderPlaced e:
                Id = e.OrderId;
                _status = OrderStatus.Placed;
                _items = e.Items.ToList();
                break;
            // Handle other events...
        }
    }
}
```

### Rehydration Pattern

```text
Aggregate Rehydration:

1. LOAD STREAM
   Read all events for aggregate from event store

2. CREATE AGGREGATE
   Instantiate empty aggregate

3. APPLY EVENTS
   Replay each event to rebuild state

4. EXECUTE COMMAND
   Validate against current state
   Generate new events

5. SAVE EVENTS
   Append new events to stream
   Use optimistic concurrency

┌──────────┐    ┌─────────────┐    ┌──────────┐
│ Load     │───►│ Replay      │───►│ Execute  │
│ Events   │    │ Events      │    │ Command  │
└──────────┘    └─────────────┘    └─────┬────┘
                                         │
                     ┌───────────────────┘
                     ▼
            ┌──────────────┐
            │ Append New   │
            │ Events       │
            └──────────────┘
```

## Projection Patterns

### Projection Types

```text
Projection Categories:

1. LIVE PROJECTIONS
   - Built in real-time
   - Subscribe to event stream
   - Eventually consistent
   - Good for read models

2. CATCH-UP PROJECTIONS
   - Rebuild from history
   - Can run any time
   - Used for new read models
   - Batch processing

3. SNAPSHOT PROJECTIONS
   - Periodic state capture
   - Optimization for rehydration
   - Combined with events

4. INLINE PROJECTIONS
   - Same transaction as write
   - Strongly consistent
   - Limited scalability
```

### Projection Implementation

```csharp
// C# Projection Example
public class OrderSummaryProjection : IProjection
{
    private readonly IOrderSummaryRepository _repository;

    public async Task HandleAsync(OrderPlaced @event)
    {
        var summary = new OrderSummary
        {
            OrderId = @event.OrderId,
            CustomerId = @event.CustomerId,
            Status = "Placed",
            ItemCount = @event.Items.Count,
            TotalAmount = @event.Items.Sum(i => i.Price * i.Quantity),
            PlacedAt = @event.Timestamp
        };

        await _repository.InsertAsync(summary);
    }

    public async Task HandleAsync(OrderPaid @event)
    {
        await _repository.UpdateAsync(
            @event.OrderId,
            summary => summary.Status = "Paid");
    }
}
```

## Snapshotting

### When to Snapshot

```text
Snapshotting Decisions:

SNAPSHOT WHEN:
- Aggregate has many events (100+)
- Rehydration time is slow
- Read performance matters
- Events are append-heavy

SNAPSHOT FREQUENCY:
- Every N events (e.g., 100)
- At time intervals
- At significant state changes
- On-demand (lazy)

DON'T SNAPSHOT WHEN:
- Aggregates are short-lived
- Few events per aggregate
- Full history replay is rare
```

### Snapshot Structure

```csharp
// Snapshot Record
public record Snapshot
{
    public required Guid AggregateId { get; init; }
    public required string AggregateType { get; init; }
    public required long Version { get; init; }
    public required string State { get; init; }  // Serialized
    public required DateTimeOffset CreatedAt { get; init; }
}

// Loading with Snapshot
public async Task<Order> LoadAsync(Guid orderId)
{
    // 1. Try to load snapshot
    var snapshot = await _snapshotStore.GetLatestAsync(orderId);

    // 2. Create aggregate from snapshot or empty
    var order = snapshot != null
        ? Order.FromSnapshot(snapshot)
        : new Order();

    // 3. Load events after snapshot version
    var events = await _eventStore.ReadAsync(
        $"Order-{orderId}",
        fromVersion: snapshot?.Version + 1 ?? 0);

    // 4. Apply remaining events
    order.Load(events);

    return order;
}
```

## Event Versioning

### Versioning Strategies

```text
Event Schema Evolution:

1. WEAK SCHEMA (Recommended)
   - Add new optional fields
   - Old events deserialize with defaults
   - Forward/backward compatible

2. UPCASTING
   - Transform old events to new format
   - On read, not on store
   - Keep original event intact

3. EVENT TYPE VERSIONING
   - OrderPlacedV1, OrderPlacedV2
   - Route to appropriate handler
   - More explicit, more verbose

4. COPY AND TRANSFORM
   - Migrate entire stream
   - Create new events from old
   - One-time operation (risky)
```

### Upcasting Example

```csharp
// Upcaster Pattern
public interface IEventUpcaster
{
    bool CanUpcast(string eventType, JsonDocument payload);
    object Upcast(string eventType, JsonDocument payload);
}

public class OrderPlacedV1ToV2Upcaster : IEventUpcaster
{
    public bool CanUpcast(string eventType, JsonDocument payload)
    {
        return eventType == "OrderPlaced"
            && !payload.RootElement.TryGetProperty("Currency", out _);
    }

    public object Upcast(string eventType, JsonDocument payload)
    {
        // Transform V1 (no currency) to V2 (with currency)
        return new OrderPlacedV2
        {
            OrderId = payload.GetProperty("OrderId").GetGuid(),
            CustomerId = payload.GetProperty("CustomerId").GetGuid(),
            Items = DeserializeItems(payload.GetProperty("Items")),
            Currency = "USD",  // Default for V1 events
            Timestamp = payload.GetProperty("Timestamp").GetDateTimeOffset()
        };
    }
}
```

## Design Decision Matrix

| Factor | Event Sourcing | State-Based |
|--------|----------------|-------------|
| **Audit Trail** | Built-in, complete | Requires separate logging |
| **Complexity** | Higher initial | Lower initial |
| **Query Flexibility** | Requires projections | Direct queries |
| **Temporal Queries** | Native support | Difficult to retrofit |
| **Storage** | Grows with events | Fixed (current state) |
| **Debugging** | Event replay | State inspection |
| **Team Experience** | Requires training | Familiar patterns |

## Workflow

When designing event-sourced systems:

1. **Evaluate Fit**: Is event sourcing appropriate?
2. **Identify Aggregates**: Define consistency boundaries
3. **Design Events**: Name, structure, versioning strategy
4. **Choose Event Store**: EventStoreDB, Marten, custom
5. **Plan Projections**: Read models needed
6. **Consider Snapshots**: Performance optimization
7. **Version Strategy**: How will events evolve?
8. **Test Strategy**: Event-based testing

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
