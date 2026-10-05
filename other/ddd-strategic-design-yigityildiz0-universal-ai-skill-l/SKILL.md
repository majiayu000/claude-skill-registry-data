---
name: ddd-strategic-design
description: Domain-Driven Design strategic and tactical patterns for complex business domains. Use when modeling domains, defining bounded contexts, or designing.
---

# DDD Strategic Design

Comprehensive guidance on Domain-Driven Design, covering both strategic patterns (bounded contexts, context mapping, ubiquitous language) and tactical patterns (aggregates, entities, value objects, domain events, repositories) with practical code examples and workshop techniques.

## When to Use This Skill

Use this skill for:

- Modeling a complex business domain with multiple stakeholder groups
- Identifying and defining bounded contexts for a new or existing system
- Drawing context maps to clarify integration relationships
- Designing aggregates with correct consistency boundaries
- Implementing domain events for cross-context communication
- Running event storming workshops to discover domain structure
- Establishing a ubiquitous language shared by developers and domain experts
- Refactoring an anemic domain model into a rich domain model

**Trigger phrases**: "domain-driven design", "DDD", "bounded context", "aggregate", "domain event", "event storming", "ubiquitous language", "context map", "value object", "anti-corruption layer", "shared kernel"

## What This Skill Does

Provides domain modeling patterns including:

- **Strategic Patterns**: Bounded contexts, context maps, shared kernel, anti-corruption layer, published language, customer-supplier, conformist, open host service
- **Tactical Patterns**: Aggregates, entities, value objects, domain events, domain services, repositories, factories
- **Discovery Techniques**: Event storming, domain storytelling, example mapping
- **Ubiquitous Language**: Glossary construction, language enforcement in code
- **Integration Patterns**: Context mapping relationships and their implementation
- **Code Organization**: Package structure aligned with bounded contexts

## Instructions

### Step 1: Discover the Domain with Event Storming

Event storming is a collaborative workshop for rapidly discovering domain structure.

**Workshop Setup**:

```
Materials:  Unlimited wall space, sticky notes (orange, blue, yellow,
            pink, purple, green, red), markers
Duration:   2-4 hours for Big Picture, 4-8 hours for Design Level
Attendees:  Domain experts, developers, product owners, UX designers

Sticky Note Color Code:
  Orange  = Domain Event       (past tense: "Order Placed")
  Blue    = Command            (imperative: "Place Order")
  Yellow  = Actor / User       (who triggers the command)
  Pink    = External System    (integration point)
  Purple  = Policy / Process   ("When X happens, then Y")
  Green   = Read Model / View  (data the actor needs to see)
  Red     = Hot Spot           (question, conflict, unknown)
```

**Big Picture Event Storming Steps**:

```
Phase 1: Chaotic Exploration (30 min)
  - Everyone writes domain events on orange stickies
  - Place them on the wall roughly left-to-right by time
  - No discussion, no filtering, just capture

Phase 2: Timeline Enforcement (20 min)
  - Arrange events in temporal order
  - Identify parallel streams (concurrent processes)
  - Mark hot spots (red stickies) for conflicts or unknowns

Phase 3: Reverse Narrative (30 min)
  - Walk backwards through the timeline
  - For each event, ask: "What caused this?"
  - Add commands (blue) and actors (yellow)

Phase 4: Bounded Context Discovery (30 min)
  - Look for clusters of related events
  - Draw boundaries around clusters with tape or markers
  - Name each boundary (these become bounded context candidates)

Phase 5: Context Relationships (20 min)
  - Draw arrows between contexts for events that cross boundaries
  - Identify upstream/downstream relationships
  - Mark integration hot spots
```

**Example Event Storm Output for E-Commerce**:

```
┌─ Catalog Context ────────────────────────────┐
│  Product Created -> Product Priced ->         │
│  Product Published -> Product Discontinued    │
└──────────────────────────────────────────────┘
        │ Product Published
        ▼
┌─ Shopping Context ───────────────────────────┐
│  Item Added to Cart -> Cart Updated ->        │
│  Checkout Started -> Order Placed             │
└──────────────────────────────────────────────┘
        │ Order Placed
        ▼
┌─ Fulfillment Context ────────────────────────┐
│  Order Accepted -> Inventory Reserved ->      │
│  Shipment Created -> Shipment Dispatched ->   │
│  Delivery Confirmed                           │
└──────────────────────────────────────────────┘
        │ Order Placed
        ▼
┌─ Billing Context ────────────────────────────┐
│  Payment Initiated -> Payment Authorized ->   │
│  Payment Captured -> Refund Issued            │
└──────────────────────────────────────────────┘
```

### Step 2: Define Bounded Contexts and Ubiquitous Language

Each bounded context gets its own ubiquitous language. The same real-world concept may have different names and different shapes in different contexts.

**Example: "Product" Across Contexts**:

| Context | Term | Attributes | Behavior |
|---------|------|------------|----------|
| Catalog | Product | name, description, images, categories | publish, discontinue |
| Shopping | CartItem | productId, name, price, quantity | add, remove, updateQty |
| Fulfillment | ShipmentItem | sku, weight, dimensions, warehouseLocation | pick, pack |
| Billing | LineItem | productId, unitPrice, quantity, taxRate | calculateTotal |

**Ubiquitous Language Glossary Template**:

```markdown
## Bounded Context: [Name]

### Glossary

| Term | Definition | Examples | NOT the same as |
|------|-----------|----------|-----------------|
| Order | A confirmed intent to purchase one or more items | Order #12345 | Cart (not yet confirmed) |
| Fulfillment | The process of picking, packing, and shipping | Warehouse operations | Delivery (carrier-side) |
| Backorder | An order accepted but not yet fulfillable | Out-of-stock item ordered | Preorder (not yet released) |
```

**Enforcing Ubiquitous Language in Code**:

```java
// BAD: Generic, anemic, no domain language
public class Item {
    private String id;
    private double price;
    private int qty;
    private String type; // what does "type" mean in this domain?
}

// GOOD: Ubiquitous language embedded in types
public class OrderLineItem {
    private final ProductId productId;
    private final Money unitPrice;
    private final Quantity quantity;

    public Money lineTotal() {
        return unitPrice.multiply(quantity.value());
    }
}
```

### Step 3: Draw Context Maps

A context map shows how bounded contexts relate to each other.

**Context Map Relationship Types**:

```
Partnership (P)
  Two contexts evolve together; teams coordinate closely.

Shared Kernel (SK)
  A small, shared subset of the domain model maintained by both teams.

Customer-Supplier (C/S)
  Upstream (supplier) provides what downstream (customer) needs.
  Downstream can negotiate.

Conformist (CF)
  Downstream conforms to upstream's model with no negotiation power.

Anti-corruption Layer (ACL)
  Downstream translates upstream's model into its own language.

Open Host Service (OHS)
  Upstream provides a well-defined protocol (API) for many consumers.

Published Language (PL)
  A shared, documented exchange format (e.g., JSON schema, protobuf).
```

**Example Context Map**:

```
┌──────────┐    OHS/PL     ┌───────────┐
│ Catalog  │ ───────────>  │ Shopping  │
│ Context  │               │ Context   │
└──────────┘               └─────┬─────┘
                                 │
                          C/S    │
                                 ▼
                           ┌───────────┐    ACL     ┌───────────┐
                           │ Billing   │ <──────── │ Payment   │
                           │ Context   │            │ Gateway   │
                           └───────────┘            │ (Stripe)  │
                                                    └───────────┘
┌──────────┐    C/S
│ Shopping │ ───────────>  ┌─────────────┐
│ Context  │               │ Fulfillment │
└──────────┘               │ Context     │
                           └──────┬──────┘
                                  │  CF
                                  ▼
                           ┌─────────────┐
                           │ Shipping    │
                           │ Partner API │
                           └─────────────┘
```

### Step 4: Design Aggregates

Aggregates define transactional consistency boundaries. They are the most important tactical pattern.

**Aggregate Design Rules**:

```
Rule 1: Protect true invariants within a single aggregate.
Rule 2: Design small aggregates (prefer fewer entities inside).
Rule 3: Reference other aggregates by identity only (not object references).
Rule 4: Use eventual consistency across aggregate boundaries.
Rule 5: One transaction = one aggregate mutation.
```

**Example: Order Aggregate (Python)**:

```python
# domain/order/aggregate.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from domain.order.events import (
    OrderPlaced, OrderLineAdded, OrderConfirmed, OrderCancelled,
)
from domain.shared.value_objects import Money, Quantity

@dataclass(frozen=True)
class OrderLineItem:
    """Value object representing a line in an order."""
    product_id: UUID
    product_name: str
    unit_price: Money
    quantity: Quantity

    @property
    def line_total(self) -> Money:
        return self.unit_price * self.quantity.value

@dataclass
class Order:
    """Aggregate root for the Order bounded context."""
    id: UUID = field(default_factory=uuid4)
    customer_id: UUID = field(default=None)
    lines: List[OrderLineItem] = field(default_factory=list)
    status: str = field(default="draft")
    placed_at: datetime | None = field(default=None)
    _events: List = field(default_factory=list, repr=False)

    # --- Invariant-protecting methods ---

    def add_line(self, product_id: UUID, name: str,
                 price: Money, qty: Quantity) -> None:
        if self.status != "draft":
            raise InvalidOrderOperation(
                "Cannot add lines to a non-draft order"
            )
        if qty.value <= 0:
            raise ValueError("Quantity must be positive")
        line = OrderLineItem(product_id, name, price, qty)
        self.lines.append(line)
        self._events.append(OrderLineAdded(
            order_id=self.id, product_id=product_id, quantity=qty.value,
        ))

    def place(self) -> None:
        if self.status != "draft":
            raise InvalidOrderOperation("Order already placed")
        if not self.lines:
            raise InvalidOrderOperation("Cannot place an empty order")
        self.status = "placed"
        self.placed_at = datetime.utcnow()
        self._events.append(OrderPlaced(
            order_id=self.id,
            customer_id=self.customer_id,
            total=self.total.amount,
        ))

    def cancel(self, reason: str) -> None:
        if self.status not in ("draft", "placed"):
            raise InvalidOrderOperation(
                f"Cannot cancel order in status '{self.status}'"
            )
        self.status = "cancelled"
        self._events.append(OrderCancelled(
            order_id=self.id, reason=reason,
        ))

    @property
    def total(self) -> Money:
        return sum(
            (line.line_total for line in self.lines),
            Money(0, "USD"),
        )

    def collect_events(self) -> List:
        events = list(self._events)
        self._events.clear()
        return events

class InvalidOrderOperation(Exception):
    pass
```

**Example: Value Objects**:

```python
# domain/shared/value_objects.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: int      # Store in smallest unit (cents)
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be a 3-letter ISO code")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor: int) -> "Money":
        return Money(self.amount * factor, self.currency)

@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Quantity cannot be negative")

@dataclass(frozen=True)
class EmailAddress:
    address: str

    def __post_init__(self):
        if "@" not in self.address or "." not in self.address:
            raise ValueError(f"Invalid email: {self.address}")
        # Normalize to lowercase
        object.__setattr__(self, "address", self.address.lower().strip())
```

**Example: Order Aggregate (C#)**:

```csharp
// Domain/Orders/Order.cs
public class Order : AggregateRoot
{
    private readonly List<OrderLine> _lines = new();
    public IReadOnlyList<OrderLine> Lines => _lines.AsReadOnly();
    public CustomerId CustomerId { get; private set; }
    public OrderStatus Status { get; private set; } = OrderStatus.Draft;
    public Money Total => _lines.Aggregate(
        Money.Zero("USD"),
        (sum, line) => sum + line.LineTotal);

    public void AddLine(ProductId productId, string name,
                        Money unitPrice, Quantity qty)
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOrderOperationException(
                "Cannot modify a placed order.");

        _lines.Add(new OrderLine(productId, name, unitPrice, qty));
        AddDomainEvent(new OrderLineAddedEvent(Id, productId, qty.Value));
    }

    public void Place()
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOrderOperationException("Already placed.");
        if (!_lines.Any())
            throw new InvalidOrderOperationException("Order is empty.");

        Status = OrderStatus.Placed;
        AddDomainEvent(new OrderPlacedEvent(
            Id, CustomerId, Total.Amount));
    }
}
```

### Step 5: Implement Domain Events

Domain events represent something important that happened in the domain.

**Domain Event Definition**:

```python
# domain/order/events.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class OrderPlaced(DomainEvent):
    order_id: UUID = None
    customer_id: UUID = None
    total: int = 0

@dataclass(frozen=True)
class OrderLineAdded(DomainEvent):
    order_id: UUID = None
    product_id: UUID = None
    quantity: int = 0

@dataclass(frozen=True)
class OrderCancelled(DomainEvent):
    order_id: UUID = None
    reason: str = ""
```

**Event Dispatcher (in-process)**:

```python
# infrastructure/event_dispatcher.py
from collections import defaultdict
from typing import Callable, Type

class EventDispatcher:
    def __init__(self):
        self._handlers: dict[Type, list[Callable]] = defaultdict(list)

    def register(self, event_type: Type, handler: Callable) -> None:
        self._handlers[event_type].append(handler)

    def dispatch(self, event) -> None:
        for handler in self._handlers[type(event)]:
            handler(event)

# Usage in application service
class PlaceOrderUseCase:
    def __init__(self, repo: OrderRepository,
                 dispatcher: EventDispatcher):
        self._repo = repo
        self._dispatcher = dispatcher

    def execute(self, command: PlaceOrderCommand) -> UUID:
        order = self._repo.find_by_id(command.order_id)
        order.place()
        self._repo.save(order)
        for event in order.collect_events():
            self._dispatcher.dispatch(event)
        return order.id
```

### Step 6: Structure Code by Bounded Context

```
src/
├── catalog/                    # Bounded Context: Catalog
│   ├── domain/
│   │   ├── product.py          # Aggregate root
│   │   ├── events.py           # Domain events
│   │   └── value_objects.py    # Price, SKU, etc.
│   ├── application/
│   │   ├── commands.py         # CreateProduct, PublishProduct
│   │   └── handlers.py         # Command handlers
│   └── infrastructure/
│       ├── postgres_repo.py    # Repository implementation
│       └── search_index.py     # Elasticsearch adapter
│
├── ordering/                   # Bounded Context: Ordering
│   ├── domain/
│   │   ├── order.py            # Aggregate root
│   │   ├── events.py
│   │   └── value_objects.py    # Money, Quantity, etc.
│   ├── application/
│   │   ├── commands.py
│   │   └── handlers.py
│   └── infrastructure/
│       ├── postgres_repo.py
│       └── payment_client.py   # ACL to payment gateway
│
├── fulfillment/                # Bounded Context: Fulfillment
│   ├── domain/
│   ├── application/
│   └── infrastructure/
│
└── shared_kernel/              # Shared Kernel (minimal!)
    ├── domain_event.py         # Base event class
    ├── aggregate_root.py       # Base aggregate
    └── entity.py               # Base entity with identity
```

## Best Practices

- **Start with strategic design before tactical** - Bounded contexts matter more than aggregate internals
- **One ubiquitous language per bounded context** - Do not force a single model across the entire system
- **Keep aggregates small** - Large aggregates cause contention and performance issues
- **Reference aggregates by ID, not object** - Prevents coupling and enables distribution
- **Use eventual consistency across aggregates** - Immediate consistency is only needed within one aggregate
- **Domain events are facts, not commands** - Name them in past tense ("OrderPlaced", not "PlaceOrder")
- **Protect invariants in the aggregate** - Never let external code reach into an aggregate to set state
- **Avoid "god aggregates"** - If an aggregate has 15+ fields, it probably needs splitting
- **Value objects should be immutable** - Use `frozen=True` in Python, `record` in C#/Java
- **Run event storming before writing code** - Discovery is faster with sticky notes than refactoring

## Common Patterns

### Pattern 1: Anti-corruption Layer Between Contexts

When integrating with a context you do not control (legacy system, third-party API), translate at the boundary:

```python
# ordering/infrastructure/catalog_acl.py
from ordering.domain.value_objects import ProductInfo, Money
from catalog_client import CatalogAPIClient

class CatalogAntiCorruptionLayer:
    """Translates Catalog context models into Ordering context models."""

    def __init__(self, client: CatalogAPIClient):
        self._client = client

    def get_product_info(self, product_id: str) -> ProductInfo:
        raw = self._client.get_product(product_id)
        return ProductInfo(
            product_id=raw["id"],
            name=raw["title"],              # "title" in catalog, "name" in ordering
            price=Money(
                amount=int(raw["price_cents"]),
                currency=raw["currency"],
            ),
        )
```

### Pattern 2: Saga for Cross-Aggregate Coordination

When a business process spans multiple aggregates, use a saga (process manager):

```python
# ordering/application/sagas/order_fulfillment_saga.py
class OrderFulfillmentSaga:
    """Coordinates Order, Payment, and Inventory across contexts."""

    def __init__(self, orders, payments, inventory, events):
        self._orders = orders
        self._payments = payments
        self._inventory = inventory
        self._events = events

    def handle_order_placed(self, event: OrderPlaced) -> None:
        # Step 1: Reserve inventory
        try:
            self._inventory.reserve(event.order_id, event.line_items)
        except InsufficientStock:
            self._orders.reject(event.order_id, "Insufficient stock")
            return

        # Step 2: Authorize payment
        try:
            self._payments.authorize(event.order_id, event.total)
        except PaymentDeclined:
            self._inventory.release(event.order_id)  # Compensate
            self._orders.reject(event.order_id, "Payment declined")
            return

        # Step 3: Confirm order
        self._orders.confirm(event.order_id)

    def handle_order_cancelled(self, event: OrderCancelled) -> None:
        # Compensating actions
        self._payments.void(event.order_id)
        self._inventory.release(event.order_id)
```

### Pattern 3: Specification Pattern for Complex Queries

Encapsulate business rules as composable specifications:

```python
# domain/shared/specification.py
from abc import ABC, abstractmethod

class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool: ...

    def and_(self, other: "Specification") -> "Specification":
        return AndSpecification(self, other)

    def or_(self, other: "Specification") -> "Specification":
        return OrSpecification(self, other)

    def not_(self) -> "Specification":
        return NotSpecification(self)

class AndSpecification(Specification):
    def __init__(self, left, right):
        self._left, self._right = left, right
    def is_satisfied_by(self, candidate) -> bool:
        return (self._left.is_satisfied_by(candidate)
                and self._right.is_satisfied_by(candidate))

# Usage
class HighValueOrder(Specification):
    def is_satisfied_by(self, order) -> bool:
        return order.total.amount >= 10000

class RecentOrder(Specification):
    def __init__(self, days: int = 30):
        self._days = days
    def is_satisfied_by(self, order) -> bool:
        cutoff = datetime.utcnow() - timedelta(days=self._days)
        return order.placed_at >= cutoff

# Compose specifications
vip_candidates = HighValueOrder().and_(RecentOrder(days=90))
```

## Quality Checklist

- [ ] Bounded contexts identified and named using ubiquitous language
- [ ] Context map drawn showing all relationships (ACL, OHS, C/S, etc.)
- [ ] Ubiquitous language glossary maintained per bounded context
- [ ] Aggregates designed small (ideally 1-3 entities per aggregate)
- [ ] Aggregates reference each other by ID only, not by object
- [ ] All invariants protected within aggregate methods (no public setters)
- [ ] Domain events defined for all state transitions that cross contexts
- [ ] Value objects used for descriptive attributes (Money, Email, Quantity)
- [ ] Repository interface defined in the domain layer, implemented in infrastructure
- [ ] No framework dependencies in the domain layer
- [ ] Event storming conducted with domain experts before implementation
- [ ] Sagas or process managers handle cross-aggregate workflows

## Related Skills

- `architecture-design` - System-level decomposition and trade-off analysis
- `api-design` - Designing published language and open host services
- `microservices-patterns` - Implementing bounded contexts as services
- `event-driven-architecture` - Event infrastructure and messaging patterns
- `refactoring-expert` - Refactoring toward a rich domain model

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
