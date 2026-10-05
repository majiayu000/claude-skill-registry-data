---
name: spring-boot
description: Use when building Spring Boot services. Covers dependency injection, transaction boundaries, JPA performance, configuration, validation, and testing slices.
metadata:
  category: backend
  version: 1.0.0
  tags: [spring, java, jpa, transactions, testing]
---

# Spring Boot

## Purpose

Build Spring Boot services with correct transaction boundaries and a JPA layer that does not issue a hundred queries to render a list. Spring's defaults are safe; its abstractions hide the cost of getting them wrong.

## When to Use

- Building or reviewing a Spring Boot application.
- Diagnosing lazy-loading exceptions or N+1 query behavior.
- Getting transaction boundaries and propagation right.
- Structuring a test suite that is faster than a full context load per class.

## Capabilities

- Constructor injection and bean lifecycle.
- Declarative transactions: propagation, isolation, rollback rules.
- JPA/Hibernate: fetch strategies, entity graphs, projections.
- Configuration properties with validation and profiles.
- Test slices: `@WebMvcTest`, `@DataJpaTest`, Testcontainers.

## Inputs

- The service, its entities, and the slow endpoint if there is one.
- Database engine and connection pool configuration.

## Outputs

- Services with explicit transaction boundaries.
- Repositories that fetch exactly what the caller needs.
- Tests that load the narrowest context that proves the behavior.

## Workflow

1. **Use constructor injection** — Field injection with `@Autowired` hides dependencies and makes the class untestable without a container.
2. **Place `@Transactional` at the service layer** — Not on the repository (too narrow, one transaction per call) and not on the controller (too wide, the transaction spans view rendering).
3. **Fetch deliberately** — Every association is `LAZY`. Then use an entity graph or a fetch join for the specific query that needs it, and a DTO projection for read-only views.
4. **Validate configuration at startup** — `@ConfigurationProperties` with `@Validated`. A missing property should prevent boot, not surface as a null at runtime.
5. **Test in slices** — `@DataJpaTest` for repositories against Testcontainers, `@WebMvcTest` for controllers with mocked services, `@SpringBootTest` only for the handful of genuine end-to-end paths.

## Best Practices

- `@Transactional` on a private or self-invoked method does nothing. Spring proxies the bean; an internal call bypasses the proxy entirely. This is the most common silent transaction bug in Spring.
- `@Transactional` rolls back on unchecked exceptions only, by default. A checked exception commits. Set `rollbackFor` deliberately.
- `FetchType.EAGER` on an association is a decision made once and paid for on every query. Default to `LAZY` and fetch on demand.
- Never return entities from a controller. A DTO projection avoids lazy-loading surprises and stops you leaking every column.
- Keep the transaction short. Never make an HTTP call inside one — you are holding a database connection for the duration of someone else's outage.
- Set connection-pool size deliberately. The default is often larger than the database can serve.

## Examples

**Fetch join with a projection, avoiding both N+1 and over-fetching:**

```java
public interface OrderRepository extends JpaRepository<Order, UUID> {

    @Query("""
        select new com.example.orders.OrderSummary(
            o.id, c.name, size(o.lines), sum(l.priceCents * l.quantity))
        from Order o
          join o.customer c
          join o.lines l
        where o.status = :status
        group by o.id, c.name
        """)
    List<OrderSummary> findSummaries(@Param("status") OrderStatus status);
}
```

**Transaction boundary at the service, HTTP call outside it:**

```java
@Service
@RequiredArgsConstructor
public class RefundService {

    private final OrderRepository orders;
    private final PaymentGateway gateway;

    @Transactional(rollbackFor = Exception.class)
    public Refund record(UUID orderId, long amountCents, String gatewayRefundId) {
        Order order = orders.findById(orderId).orElseThrow(OrderNotFound::new);
        order.applyRefund(amountCents, gatewayRefundId);   // invariants live in the entity
        return order.latestRefund();
    }

    // The network call happens outside any transaction.
    public Refund refund(UUID orderId, long amountCents) {
        String gatewayRefundId = gateway.refund(orderId, amountCents);
        return record(orderId, amountCents, gatewayRefundId);
    }
}
```

## Notes

- `spring.jpa.open-in-view` defaults to `true` and keeps a database connection open for the entire request, including view rendering. Turn it off; the lazy-loading exceptions it then reveals are real bugs it was hiding.
- Hibernate's `@BatchSize` mitigates N+1 on collections without changing the query — a useful blunt instrument when a fetch join is impractical.
- `@SpringBootTest` loads the entire context. A suite of a hundred such tests is a suite that nobody runs locally.
