---
name: cdd-design-pillars
description: Measures and limits cognitive load in Jakarta EE/MicroProfile code. Use when reviewing code complexity, designing services/entities, or identifying when to extract abstractions.
---

# CDD Design Pillars for Jakarta EE

Design principles based on Cognitive Driven Development (CDD) and Alberto Souza's "Pilares Design Código", adapted for Jakarta EE/MicroProfile applications.

## Core Philosophy

> The best code is code that doesn't need to be written. When we must write code, it should function correctly through the simplest possible implementation that requires minimal mental effort to understand, maintain, and evolve.

## Cognitive Load Theory

Code complexity is measured by **intrinsic cognitive load** — the mental effort required to understand code. Research suggests working memory holds ~7 items simultaneously.

### Cognitive Load Points

| Element                        | Points        |
| ------------------------------ | ------------- |
| Custom class dependency        | +1            |
| Branch (if, else, switch case) | +1            |
| Loop (for, while, forEach)     | +1            |
| Try-catch block                | +1 per catch  |
| Lambda/function transformation | +1            |
| Nested branch                  | +1 additional |

### Load Limits by Component Type

| Component                            | Max Points | Rationale                             |
| ------------------------------------ | ---------- | ------------------------------------- |
| Domain Service / Application Service | 7          | Business flow must be crystal clear   |
| Entity / Value Object                | 9          | Can hold more complex state logic     |
| Controller / Resource                | 7          | Entry points should be simple         |
| Repository implementation            | 5          | Should be straightforward data access |

## Core Pillars

### 1. Quality is Non-Negotiable

Design proportional to complexity with current knowledge. Execute your code as fast as possible — implement outside-in.

### 2. Protect System Boundaries

- External boundaries get maximum protection
- Never bind external request parameters directly to domain objects
- Never serialize domain objects directly to API responses
- Use DTOs for input/output

### 3. Create Only Valid References

Every object must be in a valid state from creation. Use constructors and factory methods to enforce invariants.

### 4. Keep Operations in the Owning Class

Operations on data whose type is a language primitive should live inside the class that owns the data.

### 5. Every Indirection Must Earn Its Place

Each new class/file increases system complexity. Only create abstractions when cognitive load exceeds limits.

### 6. Explicit Business Rules

Business rules must be declared explicitly in code, not hidden in conditionals or scattered across layers.

### 7. Favor Encapsulation for Cohesion

Don't modify references you didn't create. Keep state manipulation inside the owning class.

## Jakarta EE Quick Reference

### JAX-RS Resource (≤7 points)

```java
@Path("/orders")
@RequestScoped
public class OrderResource {

    @Inject
    private OrderService orderService;  // +1

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    public Response create(@Valid CreateOrderRequest request) {  // +1
        Order order = orderService.create(request);  // +1
        return Response.created(/*uri*/).entity(OrderResponse.from(order)).build();
    }
    // Total: 3 points ✓
}
```

### CDI Service (≤7 points)

```java
@ApplicationScoped
public class PaymentService {

    @Inject
    private PaymentGateway gateway;  // +1

    @Inject
    private TransactionRepository transactions;  // +1

    public Transaction process(PaymentRequest request) {
        if (!request.isValid()) {  // +1 branch
            throw new InvalidPaymentException();
        }

        Payment payment = gateway.charge(request);  // +1
        Transaction tx = Transaction.from(payment);  // +1
        return transactions.save(tx);
    }
    // Total: 5 points ✓
}
```

### JPA Entity with Encapsulated Logic (≤9 points)

```java
@Entity
public class Order {

    @Id @GeneratedValue
    private Long id;

    private Instant expiresAt;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    // ✓ Operation on owned data stays in the class
    public boolean acceptsModification() {
        return this.expiresAt.isAfter(Instant.now())
            && this.status == OrderStatus.PENDING;
    }

    // ✓ State change is encapsulated
    public void cancel() {
        if (!acceptsModification()) {
            throw new OrderCannotBeCancelledException();
        }
        this.status = OrderStatus.CANCELLED;
    }
}
```

### Boundary Separation with DTOs

```java
// Request DTO - external boundary
public record CreateOrderRequest(
    @NotBlank String customerId,
    @NotEmpty List<OrderItemRequest> items
) {
    public Order toEntity(Customer customer) {
        return new Order(customer, items.stream()
            .map(OrderItemRequest::toEntity)
            .toList());
    }
}

// Response DTO - external boundary
public record OrderResponse(
    String orderId,
    String status,
    BigDecimal total
) {
    public static OrderResponse from(Order order) {
        return new OrderResponse(
            order.getId().toString(),
            order.getStatus().name(),
            order.getTotal()
        );
    }
}
```

## Anti-Patterns

### ❌ Logic Outside Owning Class

```java
// BAD: Logic on Order's data lives outside Order
if (order.getExpiresAt().isBefore(Instant.now())) {
    return "Expired";
}

// GOOD: Ask the object
if (order.isExpired()) {
    return "Expired";
}
```

### ❌ Exceeding Cognitive Load

```java
// BAD: Too many points for a service (~11 points)
public Result process(Request req) {
    List<Handler> handlers = this.handlers.stream()  // +1
        .map(h -> h.accepts(req))  // +1
        .filter(Optional::isPresent)  // +2 (filter + branch)
        .map(Optional::get)  // +1
        .collect(toList());  // +1

    for (Handler h : handlers) {  // +1
        try {  // +1
            return h.handle();
        } catch (NetworkException e) {  // +1
            log.error(...);
        } catch (Exception e) {  // +1
            log.error(...);
        }
    }
    return Result.failure();
}

// GOOD: Extract to reduce points
@Inject
private HandlerSelector handlerSelector;  // Extracted abstraction

public Result process(Request req) {
    List<Handler> handlers = handlerSelector.selectFor(req);  // +1
    return executeWithFallback(handlers, req);  // Extracted
}
```

## Cookbook Index

### Core Pillars

- [protect-boundaries](cookbook/protect-boundaries.md) - Protecting system boundaries
- [valid-state-only](cookbook/valid-state-only.md) - Creating only valid references
- [explicit-business-rules](cookbook/explicit-business-rules.md) - Making business rules explicit
- [favor-encapsulation](cookbook/favor-encapsulation.md) - Encapsulation for cohesion

### Cognitive Load Patterns

- [cognitive-load-limits](cookbook/cognitive-load-limits.md) - Measuring and limiting load
- [concentrate-operations](cookbook/concentrate-operations.md) - Keep operations in owning class
- [extract-abstractions](cookbook/extract-abstractions.md) - When to create new abstractions

### Jakarta EE Application

- [boundary-separation](cookbook/boundary-separation.md) - DTOs and boundary protection
- [rest-resource-design](cookbook/rest-resource-design.md) - JAX-RS with CDD
- [cdi-bean-design](cookbook/cdi-bean-design.md) - CDI beans with cognitive limits
- [jpa-entity-design](cookbook/jpa-entity-design.md) - Entities with encapsulated logic
- [validation-patterns](cookbook/validation-patterns.md) - Bean Validation patterns
