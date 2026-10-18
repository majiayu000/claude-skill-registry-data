---
name: ddd-modeling
description: "Apply DDD principles to model complex business domains. Covers bounded contexts, aggregates, domain events, repositories, and ubiquitous language."
category: architecture
tags: [ddd, domain-driven-design, bounded-context, aggregates, events]
complexity: expert
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Domain-Driven Design (DDD) Modeler

## Purpose
Model complex business domains using DDD tactical and strategic patterns to create software that reflects real business logic.

## Strategic DDD

### 1️⃣ Domain Discovery (Event Storming)
Run a collaborative session:
1. **Domain Events** (orange): What happened? (OrderPlaced, PaymentFailed, ItemShipped)
2. **Commands** (blue): What triggers events? (PlaceOrder, ProcessPayment)
3. **Actors** (yellow): Who sends commands? (Customer, System, Admin)
4. **Aggregates** (yellow): What handles commands? (Order, Payment)
5. **Policies** (purple): When X happens, do Y
6. **External Systems** (pink): Third-party integrations

### 2️⃣ Bounded Contexts
Identify distinct business areas with their own ubiquitous language:
```
Order Management Context: Order, OrderItem, Fulfillment, Shipment
Payment Context: Payment, Transaction, Refund, Invoice
Inventory Context: Product, Stock, Warehouse, Reservation
Customer Context: Customer, Account, Address, Preferences
```

### 3️⃣ Aggregate Design
```python
# Aggregate root enforces business invariants
class Order(AggregateRoot):
    _MAX_ITEMS = 50
    
    def __init__(self, order_id: OrderId, customer_id: CustomerId):
        self._id = order_id
        self._customer_id = customer_id
        self._items: list[OrderItem] = []
        self._status = OrderStatus.DRAFT
        self._events: list[DomainEvent] = []
    
    def add_item(self, product_id: ProductId, quantity: int, price: Money) -> None:
        # Enforce business rules (invariants)
        if self._status != OrderStatus.DRAFT:
            raise OrderNotModifiableError("Cannot add items to a placed order")
        if len(self._items) >= self._MAX_ITEMS:
            raise OrderLimitExceededError(f"Maximum {self._MAX_ITEMS} items allowed")
        
        # Update state
        existing = self._find_item(product_id)
        if existing:
            existing.increase_quantity(quantity)
        else:
            self._items.append(OrderItem(product_id, quantity, price))
        
        # Raise domain event
        self._raise(ItemAddedToOrder(self._id, product_id, quantity))
    
    def place(self) -> None:
        if not self._items:
            raise EmptyOrderError("Cannot place an empty order")
        
        self._status = OrderStatus.PLACED
        self._raise(OrderPlaced(
            order_id=self._id,
            customer_id=self._customer_id,
            total=self._calculate_total(),
            placed_at=datetime.utcnow(),
        ))
    
    def _raise(self, event: DomainEvent) -> None:
        self._events.append(event)
```

### 4️⃣ Domain Events
```python
@dataclass(frozen=True)
class OrderPlaced:
    order_id: OrderId
    customer_id: CustomerId
    total: Money
    placed_at: datetime
    
    # Used for routing to correct handler
    @property
    def event_type(self) -> str:
        return "order.placed"

# Event handlers in other contexts
class PaymentContext:
    def handle_order_placed(self, event: OrderPlaced) -> None:
        # Create a pending payment in payment context
        payment = Payment.create_for_order(event.order_id, event.total)
        self.payments.save(payment)
```

### 5️⃣ Repository Pattern
```python
class OrderRepository(Protocol):
    def find_by_id(self, order_id: OrderId) -> Order | None: ...
    def save(self, order: Order) -> None: ...  # Also dispatches domain events
    def find_by_customer(self, customer_id: CustomerId) -> list[Order]: ...

class PostgresOrderRepository:
    def save(self, order: Order) -> None:
        # Persist the aggregate
        with self.db.transaction():
            self.db.execute(...)
            # Dispatch domain events after successful save
            for event in order.collect_events():
                self.event_bus.publish(event)
```

## Outputs
1. Bounded context map
2. Ubiquitous language glossary
3. Aggregate design with invariants
4. Domain event catalog
5. Context integration patterns (ACL, Published Language)
