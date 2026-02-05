---
name: saga-patterns
description: Distributed transaction patterns using orchestration and choreography
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Saga Patterns Skill

## When to Use This Skill

Use this skill when:

- **Saga Patterns tasks** - Working on distributed transaction patterns using orchestration and choreography
- **Planning or design** - Need guidance on Saga Patterns approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design distributed transaction patterns using orchestration and choreography for microservices.

## MANDATORY: Documentation-First Approach

Before designing sagas:

1. **Invoke `docs-management` skill** for saga patterns
2. **Verify patterns** via MCP servers (perplexity, context7)
3. **Base guidance on established microservices patterns**

## Saga Fundamentals

```text
Why Sagas?

PROBLEM:
Distributed transactions across services are complex.
Traditional 2PC (Two-Phase Commit) doesn't scale.

SOLUTION:
Saga = Sequence of local transactions
Each step has a compensating action
Eventual consistency instead of ACID

┌─────────┐    ┌─────────┐    ┌─────────┐
│ Step 1  │───►│ Step 2  │───►│ Step 3  │
│ Tx + Cx │    │ Tx + Cx │    │ Tx + Cx │
└─────────┘    └─────────┘    └─────────┘
     │              │              │
     ▼              ▼              ▼
   Local         Local          Local
 Transaction  Transaction    Transaction

Tx = Forward Transaction
Cx = Compensating Transaction
```

## Saga Coordination Styles

### Choreography (Event-Driven)

```text
Choreography Pattern:

Services communicate through events.
No central coordinator.
Each service knows what to do next.

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Order     │    │  Payment    │    │  Inventory  │
│   Service   │    │  Service    │    │  Service    │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ OrderCreated     │                  │
       │─────────────────►│                  │
       │                  │ PaymentProcessed │
       │                  │─────────────────►│
       │                  │                  │ InventoryReserved
       │◄─────────────────┼──────────────────│
       │ OrderConfirmed   │                  │

Characteristics:
✓ Loose coupling
✓ Simple services
✗ Hard to track
✗ Cyclic dependencies risk
```

### Orchestration (Coordinator-Driven)

```text
Orchestration Pattern:

Central orchestrator coordinates the saga.
Services expose commands.
Orchestrator manages state.

                ┌─────────────────┐
                │   Orchestrator  │
                │  (Saga Manager) │
                └────────┬────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Order     │  │  Payment    │  │  Inventory  │
│   Service   │  │  Service    │  │  Service    │
└─────────────┘  └─────────────┘  └─────────────┘

Characteristics:
✓ Clear flow visibility
✓ Easier debugging
✗ Single point of failure
✗ Coupling to orchestrator
```

## Choreography Implementation

### Event-Driven Flow

```csharp
// Order Service - Starts Saga
public class OrderService
{
    private readonly IEventPublisher _events;

    public async Task CreateOrderAsync(CreateOrderCommand cmd)
    {
        var order = new Order(cmd.CustomerId, cmd.Items);
        await _repository.SaveAsync(order);

        // Publish event to start saga
        await _events.PublishAsync(new OrderCreated
        {
            OrderId = order.Id,
            CustomerId = cmd.CustomerId,
            TotalAmount = order.TotalAmount
        });
    }

    // Handle compensation
    public async Task HandleAsync(PaymentFailed @event)
    {
        var order = await _repository.GetAsync(@event.OrderId);
        order.Cancel("Payment failed");
        await _repository.SaveAsync(order);

        await _events.PublishAsync(new OrderCancelled
        {
            OrderId = @event.OrderId,
            Reason = "Payment failed"
        });
    }
}

// Payment Service - Reacts to OrderCreated
public class PaymentService
{
    public async Task HandleAsync(OrderCreated @event)
    {
        try
        {
            var payment = await ProcessPaymentAsync(@event.OrderId, @event.TotalAmount);

            await _events.PublishAsync(new PaymentProcessed
            {
                OrderId = @event.OrderId,
                PaymentId = payment.Id
            });
        }
        catch (PaymentException ex)
        {
            await _events.PublishAsync(new PaymentFailed
            {
                OrderId = @event.OrderId,
                Reason = ex.Message
            });
        }
    }
}

// Inventory Service - Reacts to PaymentProcessed
public class InventoryService
{
    public async Task HandleAsync(PaymentProcessed @event)
    {
        try
        {
            await ReserveInventoryAsync(@event.OrderId);

            await _events.PublishAsync(new InventoryReserved
            {
                OrderId = @event.OrderId
            });
        }
        catch (InsufficientInventoryException)
        {
            // Trigger compensation
            await _events.PublishAsync(new InventoryReservationFailed
            {
                OrderId = @event.OrderId
            });
        }
    }

    // Compensating action
    public async Task HandleAsync(OrderCancelled @event)
    {
        await ReleaseInventoryAsync(@event.OrderId);
    }
}
```

## Orchestration Implementation

### Saga Orchestrator

```csharp
// Saga State Machine
public class OrderSaga : Saga<OrderSagaData>,
    IAmStartedBy<OrderCreated>,
    IHandle<PaymentProcessed>,
    IHandle<PaymentFailed>,
    IHandle<InventoryReserved>,
    IHandle<InventoryReservationFailed>
{
    protected override void ConfigureHowToFindSaga(SagaPropertyMapper<OrderSagaData> mapper)
    {
        mapper.MapSaga(s => s.OrderId)
            .ToMessage<OrderCreated>(m => m.OrderId)
            .ToMessage<PaymentProcessed>(m => m.OrderId)
            .ToMessage<PaymentFailed>(m => m.OrderId)
            .ToMessage<InventoryReserved>(m => m.OrderId)
            .ToMessage<InventoryReservationFailed>(m => m.OrderId);
    }

    public async Task Handle(OrderCreated message, IMessageHandlerContext context)
    {
        Data.OrderId = message.OrderId;
        Data.CustomerId = message.CustomerId;
        Data.TotalAmount = message.TotalAmount;
        Data.Status = SagaStatus.Started;

        // Request payment
        await context.Send(new ProcessPaymentCommand
        {
            OrderId = message.OrderId,
            Amount = message.TotalAmount
        });
    }

    public async Task Handle(PaymentProcessed message, IMessageHandlerContext context)
    {
        Data.PaymentId = message.PaymentId;
        Data.Status = SagaStatus.PaymentCompleted;

        // Request inventory reservation
        await context.Send(new ReserveInventoryCommand
        {
            OrderId = message.OrderId
        });
    }

    public async Task Handle(PaymentFailed message, IMessageHandlerContext context)
    {
        Data.Status = SagaStatus.Failed;

        // Compensate: Cancel order
        await context.Send(new CancelOrderCommand
        {
            OrderId = message.OrderId,
            Reason = "Payment failed"
        });

        MarkAsComplete();
    }

    public async Task Handle(InventoryReserved message, IMessageHandlerContext context)
    {
        Data.Status = SagaStatus.Completed;

        // Complete the saga
        await context.Publish(new OrderCompleted
        {
            OrderId = Data.OrderId
        });

        MarkAsComplete();
    }

    public async Task Handle(InventoryReservationFailed message, IMessageHandlerContext context)
    {
        Data.Status = SagaStatus.Failed;

        // Compensate: Refund payment
        await context.Send(new RefundPaymentCommand
        {
            OrderId = Data.OrderId,
            PaymentId = Data.PaymentId
        });

        // Compensate: Cancel order
        await context.Send(new CancelOrderCommand
        {
            OrderId = Data.OrderId,
            Reason = "Inventory unavailable"
        });

        MarkAsComplete();
    }
}

public class OrderSagaData : ContainSagaData
{
    public Guid OrderId { get; set; }
    public Guid CustomerId { get; set; }
    public decimal TotalAmount { get; set; }
    public Guid? PaymentId { get; set; }
    public SagaStatus Status { get; set; }
}
```

## Compensating Transactions

### Compensation Design

```text
Compensation Principles:

1. SEMANTIC UNDO
   Not always exact reverse
   Example: Cancel order vs. un-create order

2. IDEMPOTENT
   Can be called multiple times safely
   Same result regardless of retries

3. NEVER FAIL
   Compensation must succeed eventually
   Use retries with backoff

4. ORDERED
   Compensate in reverse order
   Last step first, first step last

Compensation Flow:
Step 1 ─► Step 2 ─► Step 3 ─► FAILURE
   │         │         │         │
   │         │         │         ▼
   │         │         └───► Compensate 3
   │         │                   │
   │         └───────────────► Compensate 2
   │                             │
   └─────────────────────────► Compensate 1
```

### Compensation Examples

```csharp
// Forward Transaction and Compensation Pairs
public class ReservationService
{
    // Forward: Reserve inventory
    public async Task<ReservationId> ReserveAsync(OrderId orderId, List<Item> items)
    {
        var reservation = new Reservation(orderId, items);
        foreach (var item in items)
        {
            await _inventory.DecrementAsync(item.ProductId, item.Quantity);
        }
        await _repository.SaveAsync(reservation);
        return reservation.Id;
    }

    // Compensating: Release reservation
    public async Task ReleaseAsync(ReservationId reservationId)
    {
        var reservation = await _repository.GetAsync(reservationId);
        if (reservation.Status == ReservationStatus.Released)
            return; // Idempotent

        foreach (var item in reservation.Items)
        {
            await _inventory.IncrementAsync(item.ProductId, item.Quantity);
        }

        reservation.Release();
        await _repository.SaveAsync(reservation);
    }
}
```

## Error Handling

### Retry Strategies

```text
Retry Patterns:

1. IMMEDIATE RETRY
   For transient failures
   Network glitches, timeouts

2. EXPONENTIAL BACKOFF
   Increasing delays
   1s → 2s → 4s → 8s

3. CIRCUIT BREAKER
   Stop retrying after threshold
   Allow recovery time

4. DEAD LETTER QUEUE
   Capture failed messages
   Manual intervention
```

### Timeout Handling

```csharp
// Saga with Timeout
public class OrderSaga : Saga<OrderSagaData>
{
    public async Task Handle(OrderCreated message, IMessageHandlerContext context)
    {
        // Set timeout for payment
        await RequestTimeout<PaymentTimeout>(
            context,
            TimeSpan.FromMinutes(30));

        await context.Send(new ProcessPaymentCommand { ... });
    }

    public async Task Timeout(PaymentTimeout timeout, IMessageHandlerContext context)
    {
        if (Data.Status == SagaStatus.AwaitingPayment)
        {
            // Payment didn't complete in time
            await context.Send(new CancelOrderCommand
            {
                OrderId = Data.OrderId,
                Reason = "Payment timeout"
            });

            Data.Status = SagaStatus.TimedOut;
            MarkAsComplete();
        }
    }
}
```

## Saga Design Template

```markdown
# Saga Design: [Process Name]

## Overview
[What this saga accomplishes]

## Trigger
[What event starts this saga]

## Steps

| Step | Service | Action | Compensating Action |
|------|---------|--------|---------------------|
| 1 | [Service] | [Forward action] | [Compensation] |
| 2 | [Service] | [Forward action] | [Compensation] |
| 3 | [Service] | [Forward action] | [Compensation] |

## Flow Diagram

```text
[ASCII saga flow diagram]
```

## Failure Scenarios

| Failure Point | What Failed | Compensation Chain |
|---------------|-------------|-------------------|
| After Step 1 | [Description] | Compensate 1 |
| After Step 2 | [Description] | Compensate 2 → 1 |

## Timeout Handling

- Step 1 timeout: [What happens]
- Step 2 timeout: [What happens]

## Idempotency

- [How duplicates are handled]

## Monitoring

- [What to monitor]
- [Alerting thresholds]

```text

```

## Choosing Choreography vs Orchestration

| Factor | Choreography | Orchestration |
|--------|--------------|---------------|
| **Coupling** | Loose | Tighter |
| **Visibility** | Distributed | Centralized |
| **Complexity** | In events | In orchestrator |
| **Debugging** | Harder | Easier |
| **Team structure** | Independent teams | Central team |
| **Failure handling** | Distributed | Centralized |
| **Best for** | Simple flows | Complex flows |

## Workflow

When designing sagas:

1. **Identify Boundaries**: Which services participate?
2. **Define Steps**: Forward actions in order
3. **Design Compensations**: Reverse actions for each step
4. **Choose Style**: Choreography or orchestration?
5. **Handle Failures**: Timeouts, retries, dead letters
6. **Ensure Idempotency**: All actions repeatable safely
7. **Plan Monitoring**: Track saga state and failures
8. **Test Failure Paths**: Verify compensations work

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
