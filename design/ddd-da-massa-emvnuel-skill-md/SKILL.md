---
name: ddd-da-massa
description: Practical DDD patterns for Jakarta EE web applications with cognitive load distribution. Use when designing controllers, entities, services, or evaluating cohesion and load balance.
---

# DDD da Massa for Jakarta EE

Practical Domain-Driven Design patterns for web applications, applying Cognitive Load Theory to create maintainable code. Based on Alberto Souza's "DDD da Massa".

## Philosophy

> Enable web application development that does what's necessary, has sufficiently flexible design, and where understanding most of the project requires low effort.

## Key Principles

1. **Leverage frameworks** — Don't ignore them, maximize their value
2. **Contextual load limits** — Different components have different limits
3. **Logical responsibility division** — Based on cognitive load, not feelings
4. **100% cohesive components** — Every attribute used by every method

## Contextual Cognitive Load Limits

Different parts of a web application have different complexity budgets:

| Component               | Max Points | Rationale                                 |
| ----------------------- | ---------- | ----------------------------------------- |
| **Controller/Resource** | 7          | Handles information flow, must be clear   |
| **Domain Service**      | 7          | Business flow should be easily understood |
| **Form/Request DTO**    | 9          | Transient state with transformation logic |
| **Entity**              | 9          | Persistent state with behavior            |
| **Repository**          | 3          | Framework does the heavy lifting          |
| **Infrastructure**      | ∞          | Rarely touched, OK to be complex          |
| **Configuration**       | ∞          | Template, rarely modified                 |

## Core Patterns

### 1. 100% Cohesive Controllers

Every method in a controller must use ALL injected dependencies.

```java
@Path("/orders/{orderId}/payments")
@RequestScoped
public class OrderPaymentResource {

    @Inject
    private OrderRepository orders;      // Used by all methods

    @Inject
    private PaymentGateway gateway;      // Used by all methods

    @Inject
    private Event<PaymentEvent> events;  // Used by all methods

    @POST
    @Transactional
    public Response processPayment(
            @PathParam("orderId") Long orderId,
            @Valid PaymentRequest request) {

        Order order = orders.findById(orderId)
            .orElseThrow(NotFoundException::new);

        Payment payment = request.toPayment(order);
        PaymentResult result = gateway.process(payment);

        events.fire(new PaymentEvent(order, result));

        return Response.ok(PaymentResponse.from(result)).build();
    }
}
// All 3 dependencies used ✓
```

### 2. Form Value Objects (Smart DTOs)

DTOs that know how to convert themselves to domain objects.

```java
public record CreateOrderRequest(
    @NotBlank String customerId,
    @NotEmpty List<@Valid OrderItemRequest> items,
    String notes
) {
    // Conversion logic lives HERE, not in a separate Mapper
    public Order toEntity(Customer customer) {
        return new Order(
            customer,
            items.stream().map(OrderItemRequest::toEntity).toList(),
            notes
        );
    }
}
```

### 3. Rich Entities

Entities hold business logic, not just data.

```java
@Entity
public class Bolao {

    private Instant expiresAt;

    @ElementCollection
    private Set<String> invitedEmails;

    // ✓ Logic on state lives in the entity
    public Participation accept(User participant) {
        if (expiresAt.isBefore(Instant.now())) {
            throw new InvitationExpiredException();
        }

        if (!invitedEmails.contains(participant.getEmail())) {
            throw new NotInvitedException(participant);
        }

        return new Participation(this, participant);
    }
}
```

### 4. Domain Service Controllers

When controller + service roles merge (for simple flows):

```java
@Path("/payments/pagseguro/{orderId}")
@RequestScoped
public class PagseguroPaymentCallbackResource {

    @Inject
    private OrderRepository orders;

    @Inject
    private PaymentRepository payments;

    @Inject
    private Event<NewPaymentEvent> paymentEvents;

    @POST
    @Transactional
    public void processCallback(
            @PathParam("orderId") Long orderId,
            @Valid PagseguroCallbackRequest request) {

        Order order = orders.findById(orderId)
            .orElseThrow(NotFoundException::new);

        Payment payment = request.toPayment(order);
        payments.save(payment);

        paymentEvents.fire(new NewPaymentEvent(payment));
    }
}
// Acts as both controller AND domain service
```

## Load Distribution Check

If entity has LOW load but calling code has HIGH load → bad distribution:

```java
// ❌ Entity too thin, controller too fat
@POST
public Response accept(@Valid AcceptRequest request) {
    Bolao bolao = bolaoRepo.findById(request.bolaoId()).get();

    // All this logic should be IN the entity
    if (bolao.getExpiresAt().isBefore(Instant.now())) {
        return Response.status(422).entity("Expired").build();
    }
    if (!bolao.getEmails().contains(request.email())) {
        return Response.status(422).entity("Not invited").build();
    }
    // ... more external logic
}

// ✓ Move logic to entity
@POST
public Response accept(@Valid AcceptRequest request) {
    Bolao bolao = bolaoRepo.findById(request.bolaoId()).get();
    User user = userRepo.findByEmail(request.email()).orElseThrow();

    Participation participation = bolao.accept(user);  // Entity has the logic
    participationRepo.save(participation);

    return Response.ok().build();
}
```

## When to Create New Classes

Only create new files when:

1. **Cognitive load exceeded** — Must distribute
2. **New domain concept** — Entity, Value Object
3. **Language feature** — Enum, sealed type

Do NOT create classes just because it "feels cleaner".

## Cookbook Index

### Controller Patterns

- [cohesive-resources](cookbook/cohesive-resources.md) - 100% cohesive JAX-RS resources
- [domain-service-controller](cookbook/domain-service-controller.md) - Merged controller/service pattern

### DTO Patterns

- [form-value-objects](cookbook/form-value-objects.md) - Smart DTOs with conversion
- [request-validation](cookbook/request-validation.md) - Validation in DTOs

### Domain Patterns

- [rich-entities](cookbook/rich-entities.md) - Entities with behavior
- [load-distribution](cookbook/load-distribution.md) - Balancing load across layers

### Service Patterns

- [cohesive-services](cookbook/cohesive-services.md) - 100% cohesive CDI services
- [splitting-load](cookbook/splitting-load.md) - When and how to split services
