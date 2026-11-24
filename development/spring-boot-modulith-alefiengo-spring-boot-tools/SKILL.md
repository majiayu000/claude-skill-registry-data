---
name: spring-boot-modulith
description: >
  Modular architecture with Spring Modulith (Spring's official modular
  monolith). Feature-based module structure, encapsulation with internal/,
  automatic boundary verification, communication via domain events, isolated
  testing (@ApplicationModuleTest), and migration from traditional monoliths.
  Use when Spring Modulith adoption, module boundary verification or modular
  monolith design is requested; new projects alone do not require Modulith.
---

# Spring Modulith (modular monolith)

## Scope

Use this skill when module boundaries, event publication or Modulith adoption are relevant. Preserve existing boundaries and verify them with `ApplicationModules.verify()`; do not introduce Modulith to solve an unrelated controller change. Route operational diagnosis to observability and test design to testing.


## Concept

Spring Modulith is a Spring project (referenced from the Spring Boot code-structure guidance) for structuring a monolith **with boundaries**. It is not hexagonal; it is **package-by-feature with enforcement**.

```
com.example.myapp/
├── order/
│   ├── internal/              ← internal: verification rejects access from outside
│   │   ├── OrderEntity.java
│   │   ├── OrderRepository.java
│   │   └── OrderInternalService.java
│   ├── OrderController.java   ← public API of the module
│   ├── OrderService.java      ← public interface
│   └── OrderCreatedEvent.java ← domain event (public)
├── user/
│   ├── internal/
│   │   ├── UserEntity.java
│   │   └── UserRepository.java
│   ├── UserController.java
│   ├── UserService.java
│   └── UserRegisteredEvent.java
└── shared/                    ← shared: config, exceptions, global DTOs
```

## Dependency

Use the Spring Modulith BOM compatible with the project's Boot line; do not assume the Boot BOM manages Modulith versions. Verify the selected Modulith release against the project Boot version before choosing `spring-modulith.version`:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.modulith</groupId>
            <artifactId>spring-modulith-bom</artifactId>
            <version>${spring-modulith.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Add `org.springframework.modulith:spring-modulith-starter-core` and test-scoped `spring-modulith-starter-test`. For persistent event publications choose `spring-modulith-starter-jdbc` or `spring-modulith-starter-jpa` and configure its storage.

## Define a module explicitly

Use `package-info.java` at the module root:

```java
@org.springframework.modulith.ApplicationModule(allowedDependencies = {"user", "shared"})
package com.example.myapp.order;
```

## Encapsulation

Top-level feature packages are modules. Their base packages expose APIs; nested packages are internal unless explicitly exposed with `@NamedInterface`. Java can still compile an import of a public class from an internal package; Modulith verification detects that boundary violation.

## Automatic verification

```java
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;

class ArchitectureTest {
    @Test
    void shouldRespectModuleBoundaries() {
        ApplicationModules.of(MyApp.class).verify();
    }
}
```

`MyApp` is the project's `@SpringBootApplication` class. Run this JUnit test in the build. `@ApplicationModuleTest` tests module behavior; it does not provide an autowired `ApplicationModules` bean by default.

## Inter-module communication

**Never** import classes from another module that are not part of its public API (Controller, Service interface, Event). For asynchronous communication: **domain events**.

```java
// order/OrderCreatedEvent.java
public record OrderCreatedEvent(
    Long orderId,
    Long customerId,
    BigDecimal total
) {}

// user/ — listens to the event
@ApplicationModuleListener
void onOrderCreated(OrderCreatedEvent event) {
    log.info("User {} created order {}", event.customerId(), event.orderId());
}
```

### Event externalization

For Kafka choose `spring-modulith-events-kafka`, configure the Kafka producer, and annotate exported event types with `@Externalized("orders")` (from `org.springframework.modulith.events`). AMQP/JMS need their corresponding adapters. Persistent event publication and retry handling need a configured JDBC/JPA event registry; configure outbox mode using the selected release's documented adapter options when required.

Review event serialization, transaction boundaries, delivery guarantees and broker failure recovery; test them with the selected adapter.

## Isolated per-module testing

```java
@ApplicationModuleTest
@Transactional
class OrderModuleTest {

    @Test
    void shouldPlaceOrder() {
        // loads the selected module according to its bootstrap mode
        // explicitly provide @MockitoBean collaborators for external dependencies
    }
}
```

## Migrating an existing monolith

1. **Confirm adoption scope** and compatibility before adding Modulith and verification tests. Existing package boundaries may already meet the requirement.
2. **Move classes by feature** to top-level packages and fix imports as each step compiles.
3. **Create `internal/`** inside each module and move implementations there.
4. **Extract events** where one module needs another's data.
5. **Run `verify()`** — the errors tell you exactly where the coupling is.
6. **Repeat** until `verify()` passes.

## Monolith vs microservices

| Stage                     | When                                                                 |
|---------------------------|----------------------------------------------------------------------|
| Modulith                  | when verifiable in-process module boundaries justify adoption                                                     |
| Modulith + events         | when asynchronous in-process collaboration and delivery semantics are required                                   |
| Extract module to service | when you need independent deployment, a dedicated team, or a different resource scale |

Compare operational cost, team ownership, consistency and deployment constraints.
Independent scaling or deployment can justify a service; an ordinary layered
monolith can also be sufficient. Modulith and events are optional design choices.

## References

- [Modulith starters and compatibility](https://docs.spring.io/spring-modulith/reference/appendix.html)
- [Module definitions and boundaries](https://docs.spring.io/spring-modulith/reference/fundamentals.html)
- [Event externalization](https://docs.spring.io/spring-modulith/reference/events.html)
