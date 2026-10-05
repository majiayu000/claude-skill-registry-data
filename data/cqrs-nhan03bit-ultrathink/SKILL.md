---
name: cqrs
description: Command Query Responsibility Segregation — separate read/write models, event buses, and projections.
layer: utility
category: architecture
triggers:
  - "cqrs"
  - "command query"
  - "read model"
  - "write model"
  - "projection"
inputs:
  - "CQRS architecture decisions"
  - "Read/write model separation design"
  - "Event bus and projection setup"
  - "Eventual consistency strategies"
outputs:
  - "CQRS architecture with separate models"
  - "Command and query handlers"
  - "Event bus configurations"
  - "Projection and read model patterns"
linksTo:
  - event-sourcing
  - message-queues
  - microservices
  - database-optimization
linkedFrom: []
preferredNextSkills:
  - event-sourcing
  - message-queues
  - microservices
fallbackSkills: []
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# CQRS Patterns

## Purpose

Provide expert guidance on Command Query Responsibility Segregation (CQRS) — separating read and write models, implementing command/query buses, building projections, handling eventual consistency, and knowing when CQRS is (and is not) appropriate. Covers both simple CQRS (separate read/write repos) and full CQRS with event sourcing.

## When to Use CQRS

**Good fit:**
- Read and write workloads have vastly different scaling needs
- Complex domain logic on writes, simple reads
- Multiple read representations of the same data (list view, dashboard, search)
- Event sourcing is already in use
- Microservice with distinct read/write patterns

**Bad fit:**
- Simple CRUD with no complex business logic
- Small-scale app with uniform read/write patterns
- Team unfamiliar with eventual consistency tradeoffs

## Architecture Overview

```
┌──────────┐     Command     ┌─────────────┐     Events     ┌─────────────┐
│  Client   │ ─────────────→ │  Write Side  │ ─────────────→ │  Event Bus  │
│           │                │  (Commands)  │                │             │
│           │     Query      ├─────────────┤                ├─────────────┤
│           │ ←───────────── │  Read Side   │ ←───────────── │ Projections │
│           │                │  (Queries)   │                │             │
└──────────┘                └─────────────┘                └─────────────┘
                              Write DB                        Read DB(s)
```

## Command Side (Write Model)

**Command definition:**

```typescript
// commands/create-order.command.ts
interface Command {
  readonly type: string;
  readonly timestamp: Date;
  readonly metadata: { userId: string; correlationId: string };
}

interface CreateOrderCommand extends Command {
  type: 'CreateOrder';
  payload: {
    customerId: string;
    items: Array<{ productId: string; quantity: number; price: number }>;
    shippingAddress: Address;
  };
}

interface CancelOrderCommand extends Command {
  type: 'CancelOrder';
  payload: { orderId: string; reason: string };
}
```

**Command handler:**

```typescript
// handlers/create-order.handler.ts
class CreateOrderHandler implements CommandHandler<CreateOrderCommand> {
  constructor(
    private readonly orderRepo: OrderWriteRepository,
    private readonly eventBus: EventBus,
    private readonly inventoryService: InventoryService,
  ) {}

  async execute(command: CreateOrderCommand): Promise<string> {
    // Validate business rules against the write model
    const { customerId, items, shippingAddress } = command.payload;

    // Check inventory (synchronous consistency boundary)
    for (const item of items) {
      const available = await this.inventoryService.checkAvailability(
        item.productId,
        item.quantity,
      );
      if (!available) {
        throw new InsufficientInventoryError(item.productId);
      }
    }

    // Create aggregate
    const order = Order.create({
      customerId,
      items,
      shippingAddress,
    });

    // Persist write model
    await this.orderRepo.save(order);

    // Publish domain events (async projection update)
    await this.eventBus.publish(
      new OrderCreatedEvent({
        orderId: order.id,
        customerId,
        items,
        total: order.total,
        createdAt: order.createdAt,
      }),
    );

    return order.id;
  }
}
```

**Command bus:**

```typescript
// bus/command-bus.ts
type CommandHandler<T extends Command> = {
  execute(command: T): Promise<any>;
};

class CommandBus {
  private handlers = new Map<string, CommandHandler<any>>();

  register<T extends Command>(type: string, handler: CommandHandler<T>) {
    if (this.handlers.has(type)) {
      throw new Error(`Handler already registered for command: ${type}`);
    }
    this.handlers.set(type, handler);
  }

  async dispatch<T extends Command>(command: T): Promise<any> {
    const handler = this.handlers.get(command.type);
    if (!handler) {
      throw new Error(`No handler for command: ${command.type}`);
    }
    return handler.execute(command);
  }
}
```

## Query Side (Read Model)

**Query definition and handler:**

```typescript
// queries/get-order-summary.query.ts
interface GetOrderSummaryQuery {
  type: 'GetOrderSummary';
  orderId: string;
}

interface OrderSummaryDto {
  orderId: string;
  customerName: string;
  itemCount: number;
  total: number;
  status: string;
  createdAt: Date;
}

class GetOrderSummaryHandler implements QueryHandler<GetOrderSummaryQuery, OrderSummaryDto> {
  constructor(private readonly readDb: ReadDatabase) {}

  async execute(query: GetOrderSummaryQuery): Promise<OrderSummaryDto> {
    // Read from the denormalized read model — optimized for this query
    const row = await this.readDb.query(
      `SELECT order_id, customer_name, item_count, total, status, created_at
       FROM order_summaries
       WHERE order_id = $1`,
      [query.orderId],
    );

    if (!row) throw new NotFoundException(`Order ${query.orderId} not found`);
    return row;
  }
}
```

**Query bus:**

```typescript
class QueryBus {
  private handlers = new Map<string, QueryHandler<any, any>>();

  register<Q, R>(type: string, handler: QueryHandler<Q, R>) {
    this.handlers.set(type, handler);
  }

  async execute<Q extends { type: string }, R>(query: Q): Promise<R> {
    const handler = this.handlers.get(query.type);
    if (!handler) throw new Error(`No handler for query: ${query.type}`);
    return handler.execute(query);
  }
}
```

## Projections

Projections transform domain events into read-optimized views:

```typescript
// projections/order-summary.projection.ts
class OrderSummaryProjection implements EventHandler {
  constructor(private readonly readDb: ReadDatabase) {}

  // Each method handles one event type
  async onOrderCreated(event: OrderCreatedEvent) {
    await this.readDb.query(
      `INSERT INTO order_summaries (order_id, customer_name, item_count, total, status, created_at)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [
        event.orderId,
        event.customerName,
        event.items.length,
        event.total,
        'pending',
        event.createdAt,
      ],
    );
  }

  async onOrderShipped(event: OrderShippedEvent) {
    await this.readDb.query(
      `UPDATE order_summaries SET status = 'shipped', shipped_at = $2 WHERE order_id = $1`,
      [event.orderId, event.shippedAt],
    );
  }

  async onOrderCancelled(event: OrderCancelledEvent) {
    await this.readDb.query(
      `UPDATE order_summaries SET status = 'cancelled', cancel_reason = $2 WHERE order_id = $1`,
      [event.orderId, event.reason],
    );
  }
}

// Multiple projections from the same events
class CustomerDashboardProjection implements EventHandler {
  async onOrderCreated(event: OrderCreatedEvent) {
    await this.readDb.query(
      `UPDATE customer_dashboards
       SET total_orders = total_orders + 1,
           total_spent = total_spent + $2,
           last_order_at = $3
       WHERE customer_id = $1`,
      [event.customerId, event.total, event.createdAt],
    );
  }
}
```

## Event Bus Implementation

```typescript
// bus/event-bus.ts
type EventSubscriber = (event: DomainEvent) => Promise<void>;

class InMemoryEventBus implements EventBus {
  private subscribers = new Map<string, EventSubscriber[]>();

  subscribe(eventType: string, handler: EventSubscriber) {
    const handlers = this.subscribers.get(eventType) ?? [];
    handlers.push(handler);
    this.subscribers.set(eventType, handlers);
  }

  async publish(event: DomainEvent) {
    const handlers = this.subscribers.get(event.type) ?? [];
    // Run projections in parallel — each is independent
    await Promise.allSettled(handlers.map((h) => h(event)));
  }
}

// For production: use a persistent message broker
class RabbitMQEventBus implements EventBus {
  async publish(event: DomainEvent) {
    await this.channel.publish(
      'domain-events',
      event.type,
      Buffer.from(JSON.stringify(event)),
      { persistent: true, messageId: event.id },
    );
  }
}
```

## Eventual Consistency Handling

**Client-side strategies:**

```typescript
// 1. Optimistic UI — update immediately, reconcile later
async function createOrder(data: CreateOrderInput) {
  // Optimistically add to local state
  addOptimisticOrder(data);

  // Send command
  const orderId = await commandBus.dispatch({
    type: 'CreateOrder',
    payload: data,
  });

  // Poll or use WebSocket for projection to catch up
  await waitForProjection('order_summaries', orderId);
}

// 2. Return write model result for the creating user
async function createOrderEndpoint(req, res) {
  const order = await commandBus.dispatch(createOrderCommand);
  // Return the write model result directly — no eventual consistency for creator
  res.status(201).json({
    orderId: order.id,
    status: order.status,
    total: order.total,
  });
}

// 3. Versioned reads — client sends last-known version
async function getOrder(req, res) {
  const minVersion = parseInt(req.headers['if-none-match'] ?? '0');
  const order = await queryBus.execute({
    type: 'GetOrderSummary',
    orderId: req.params.id,
  });

  if (order.version <= minVersion) {
    // Projection hasn't caught up yet — retry or return 304
    return res.status(304).end();
  }

  res.set('ETag', String(order.version));
  res.json(order);
}
```

## Best Practices

1. **Start simple** — Separate read/write repos before adding event buses and projections.
2. **One command, one handler** — Each command has exactly one handler.
3. **Queries are side-effect free** — Read operations never modify state.
4. **Commands return minimal data** — Typically just the ID; clients query for details.
5. **Projections must be idempotent** — Events may be replayed during rebuilds.
6. **Use persistent event storage** — Required for projection rebuilds and auditing.
7. **Handle projection lag** — Clients must tolerate eventual consistency.
8. **Separate read databases** — Denormalized, optimized per query pattern.
9. **Version projections** — Allow rebuilding from events without downtime.
10. **Monitor projection lag** — Alert when read models fall behind the write model.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| CQRS for simple CRUD | Unnecessary complexity | Use CQRS only when read/write patterns diverge significantly |
| Querying the write model | Defeats the purpose of separation | Read side should have its own optimized store |
| Non-idempotent projections | Replaying events corrupts read model | Use upserts or track processed event IDs |
| Synchronous projections | Command latency includes projection time | Project asynchronously via event bus |
| Ignoring eventual consistency | UI shows stale data | Use optimistic UI, polling, or WebSocket notifications |
| Missing correlation IDs | Cannot trace command through projections | Include correlationId in all commands and events |
