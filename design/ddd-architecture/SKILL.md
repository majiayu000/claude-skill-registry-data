---
name: ddd-architecture
description: Domain-Driven Design and Clean Architecture implementation guide
version: 1.0.0
author: DDD Boilerplate
tags: [ddd, clean-architecture, design-patterns, typescript]
---

# DDD Architecture Skill

This skill provides guidance for implementing Domain-Driven Design (DDD) patterns with Clean Architecture principles in TypeScript projects.

## When to Use This Skill

Use this skill when:
- Implementing domain models and aggregates
- Designing bounded contexts
- Creating repositories and domain services
- Applying tactical DDD patterns
- Reviewing code for architectural compliance
- Creating new entities, value objects, or domain events

## Domain Layer Patterns

### 1. Aggregate Root

**Purpose**: Transaction boundary and consistency enforcement

```typescript
import { AggregateRoot } from '@shared/domain/AggregateRoot';
import { DomainEvent } from '@shared/domain/DomainEvent';

export class Order extends AggregateRoot<OrderId> {
  private items: OrderItem[];
  private status: OrderStatus;

  private constructor(id: OrderId, items: OrderItem[], status: OrderStatus) {
    super(id);
    this.items = items;
    this.status = status;
  }

  // Factory method - only way to create instances
  static create(customerId: CustomerId, items: OrderItem[]): Order {
    if (items.length === 0) {
      throw new InvalidOrderError('Order must have at least one item');
    }
    
    const order = new Order(
      OrderId.generate(),
      items,
      OrderStatus.Pending
    );
    
    // Publish domain event
    order.addDomainEvent(new OrderCreatedEvent(order.id, customerId));
    
    return order;
  }

  // Business method with invariant protection
  confirm(): void {
    if (this.status !== OrderStatus.Pending) {
      throw new InvalidOrderError('Only pending orders can be confirmed');
    }
    
    this.status = OrderStatus.Confirmed;
    this.addDomainEvent(new OrderConfirmedEvent(this.id));
  }

  // Business method
  addItem(item: OrderItem): void {
    if (this.status !== OrderStatus.Pending) {
      throw new InvalidOrderError('Cannot modify non-pending order');
    }
    
    this.items.push(item);
  }

  // Query method
  get totalAmount(): Money {
    return this.items.reduce(
      (total, item) => total.add(item.subtotal),
      Money.zero(Currency.USD)
    );
  }
}
```

**Key Points**:
- Private constructor forces use of factory methods
- All state changes through business methods
- Invariants validated before state changes
- Domain events published for significant changes

### 2. Value Object

**Purpose**: Immutable, identity-less domain concepts

```typescript
import { ValueObject } from '@shared/domain/ValueObject';

export class Money extends ValueObject<{ amount: number; currency: Currency }> {
  private constructor(props: { amount: number; currency: Currency }) {
    super(props);
  }

  static create(amount: number, currency: Currency): Money {
    if (amount < 0) {
      throw new InvalidMoneyError('Amount cannot be negative');
    }
    return new Money({ amount, currency });
  }

  static zero(currency: Currency): Money {
    return new Money({ amount: 0, currency });
  }

  get amount(): number {
    return this.props.amount;
  }

  get currency(): Currency {
    return this.props.currency;
  }

  add(other: Money): Money {
    if (!this.props.currency.equals(other.currency)) {
      throw new InvalidMoneyError('Cannot add different currencies');
    }
    return Money.create(this.props.amount + other.amount, this.props.currency);
  }

  multiply(factor: number): Money {
    return Money.create(this.props.amount * factor, this.props.currency);
  }
}
```

**Key Points**:
- Extends ValueObject base class
- All properties readonly
- Factory method with validation
- Returns new instances for operations

### 3. Entity

**Purpose**: Objects with identity that can change over time

```typescript
import { Entity } from '@shared/domain/Entity';

export class OrderItem extends Entity<OrderItemId> {
  private quantity: Quantity;
  private unitPrice: Money;
  private readonly productId: ProductId;

  private constructor(
    id: OrderItemId,
    productId: ProductId,
    quantity: Quantity,
    unitPrice: Money
  ) {
    super(id);
    this.productId = productId;
    this.quantity = quantity;
    this.unitPrice = unitPrice;
  }

  static create(
    productId: ProductId,
    quantity: Quantity,
    unitPrice: Money
  ): OrderItem {
    return new OrderItem(
      OrderItemId.generate(),
      productId,
      quantity,
      unitPrice
    );
  }

  get subtotal(): Money {
    return this.unitPrice.multiply(this.quantity.value);
  }

  updateQuantity(newQuantity: Quantity): void {
    this.quantity = newQuantity;
  }
}
```

### 4. Domain Event

**Purpose**: Record of something significant that happened in the domain

```typescript
import { DomainEvent } from '@shared/domain/DomainEvent';

export class OrderConfirmedEvent implements DomainEvent {
  readonly occurredAt: Date;
  readonly eventType = 'OrderConfirmed';

  constructor(
    readonly orderId: OrderId,
    readonly customerId: CustomerId,
    readonly totalAmount: Money
  ) {
    this.occurredAt = new Date();
  }
}
```

**Key Points**:
- All properties readonly (immutable)
- Past tense naming
- Contains all relevant data
- Includes timestamp

### 5. Repository Interface

**Purpose**: Abstraction for aggregate persistence

```typescript
// Domain layer - interface only
export interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order | null>;
  findByCustomerId(customerId: CustomerId): Promise<Order[]>;
  delete(order: Order): Promise<void>;
}

// Infrastructure layer - implementation
export class SqlOrderRepository implements OrderRepository {
  constructor(private readonly db: Database) {}

  async save(order: Order): Promise<void> {
    const model = OrderMapper.toModel(order);
    await this.db.orders.upsert(model);
  }

  async findById(id: OrderId): Promise<Order | null> {
    const model = await this.db.orders.findUnique({
      where: { id: id.value }
    });
    return model ? OrderMapper.toDomain(model) : null;
  }
}
```

## Application Layer Patterns

### Use Case / Command Handler

```typescript
export class CreateOrderUseCase {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly productRepository: ProductRepository,
    private readonly eventPublisher: EventPublisher
  ) {}

  async execute(command: CreateOrderCommand): Promise<CreateOrderResult> {
    // 1. Validate and create value objects
    const customerId = CustomerId.create(command.customerId);
    
    // 2. Load necessary aggregates
    const items = await Promise.all(
      command.items.map(async (item) => {
        const product = await this.productRepository.findById(
          ProductId.create(item.productId)
        );
        if (!product) {
          throw new ProductNotFoundError(item.productId);
        }
        return OrderItem.create(
          product.id,
          Quantity.create(item.quantity),
          product.price
        );
      })
    );

    // 3. Execute domain logic
    const order = Order.create(customerId, items);

    // 4. Persist
    await this.orderRepository.save(order);

    // 5. Publish events
    for (const event of order.domainEvents) {
      await this.eventPublisher.publish(event);
    }

    // 6. Return result
    return new CreateOrderResult(order.id.value);
  }
}
```

## DO's and DON'Ts

### DO

- ✅ Start with domain modeling before technical concerns
- ✅ Use ubiquitous language consistently
- ✅ Keep aggregates small and focused
- ✅ Validate invariants in domain objects
- ✅ Use factory methods for object creation
- ✅ Publish domain events for state changes
- ✅ Write unit tests for domain logic without mocks
- ✅ Use dependency injection for infrastructure

### DON'T

- ❌ Create anemic domain models (data without behavior)
- ❌ Let ORM/database concerns leak into domain
- ❌ Modify multiple aggregates in one transaction
- ❌ Import infrastructure in domain layer
- ❌ Use primitive types for domain concepts
- ❌ Skip validation in value objects
- ❌ Return database models from repositories

## File Structure Template

When creating a new bounded context:

```
src/[context]/
├── domain/
│   ├── [Aggregate].ts          # Aggregate root
│   ├── [Entity].ts             # Entities
│   ├── [ValueObject].ts        # Value objects  
│   ├── [Repository].ts         # Repository interface
│   ├── [DomainService].ts      # Domain services
│   └── events/
│       └── [Event]Event.ts     # Domain events
├── application/
│   ├── commands/
│   │   └── [Action][Entity]Command.ts
│   ├── queries/
│   │   └── Get[Entity]Query.ts
│   ├── handlers/
│   │   ├── [Action][Entity]Handler.ts
│   │   └── Get[Entity]Handler.ts
│   └── dtos/
│       └── [Entity]Dto.ts
├── infrastructure/
│   ├── [Repository]Impl.ts     # Repository implementation
│   ├── mappers/
│   │   └── [Entity]Mapper.ts   # Domain <-> Model mapping
│   └── models/
│       └── [Entity]Model.ts    # Database model
└── interface/
    └── [Entity]Controller.ts   # API endpoints
```

## Common Patterns Reference

### Specification Pattern

```typescript
interface Specification<T> {
  isSatisfiedBy(entity: T): boolean;
}

class OrderEligibleForDiscount implements Specification<Order> {
  isSatisfiedBy(order: Order): boolean {
    return order.totalAmount.amount > 100;
  }
}
```

### Domain Service

```typescript
class PricingService {
  calculateDiscount(order: Order, customer: Customer): Money {
    // Complex logic that doesn't belong to a single aggregate
    if (customer.isVip && order.totalAmount.amount > 500) {
      return order.totalAmount.multiply(0.1);
    }
    return Money.zero(order.totalAmount.currency);
  }
}
```

### Factory Pattern

```typescript
class OrderFactory {
  constructor(private readonly productRepository: ProductRepository) {}

  async createFromCart(cart: Cart): Promise<Order> {
    const items = await Promise.all(
      cart.items.map(async (cartItem) => {
        const product = await this.productRepository.findById(cartItem.productId);
        return OrderItem.create(product.id, cartItem.quantity, product.price);
      })
    );
    return Order.create(cart.customerId, items);
  }
}
```
