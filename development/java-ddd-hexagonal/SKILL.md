---
name: java-ddd-hexagonal
description: |
  Guide Claude to create domain modules following DDD principles and hexagonal architecture for Java + Spring Boot projects.
  Use when user requests:
  (1) "Create a new module" / "새 모듈 만들어줘" / "도메인 모듈 생성"
  (2) "Add {feature} module" (e.g., "Add order module", "Add product module")
  (3) "Build {domain} bounded context" / "{domain} 바운디드 컨텍스트 구현"
  (4) Any request to create a new domain module for Java + Spring Boot projects with DDD and hexagonal architecture.
  Applies Kent Beck's TDD workflow (Red → Green → Refactor).
  Adapts to any Java/Spring Boot project by reading CLAUDE.md at project root.
  Uses Java 17+ features including records, sealed classes, and pattern matching.
---

# Java DDD Hexagonal Architecture

Guide Claude to create domain modules following Domain-Driven Design principles and hexagonal architecture (Ports & Adapters) for Java + Spring Boot projects.

## Overview

**Architecture**: Hexagonal (Ports & Adapters) with three layers
**Testing**: Kent Beck's TDD workflow - Red → Green → Refactor
**Adaptable**: Reads CLAUDE.md to understand project structure
**Java Version**: Java 17+ with records, sealed classes, pattern matching

## Quick Start Workflow

When user requests a new module, follow these steps in order:

### Step 0: Read Project Configuration

**Read CLAUDE.md at project root** to extract:

1. **Base package name**: Look for package patterns
   - Example: `com.shop.ecommerce.order.domain` → base is `com.shop.ecommerce`
   - Example: `io.example.app.member.application` → base is `io.example.app`

2. **Module structure**: Check directory layout
   - Look for: `modules/{module}/`, `libs/`, `buildSrc/`

3. **Build system**: Identify build configuration
   - Convention plugins: `plugins { id("conventions") }`
   - Version catalog: `libs.versions.toml`

4. **Common modules**: Find shared libraries
   - Domain common: `:libs:common`
   - Adapter libs: `:libs:adapter:*`

5. **Tech stack**: Extract versions
   - Java, Spring Boot versions
   - Testing libraries (JUnit 5, Mockito)

**If CLAUDE.md not found**:
- Ask user for base package
- Use defaults: `com.example.project`
- Proceed with standard patterns

### Step 1: Understand Requirements

Ask clarifying questions:
- Module's purpose? (e.g., "Manage customer orders")
- Main entities? (e.g., "Order, OrderItem, Customer")
- Operations needed? (e.g., "Place order, cancel order, track status")
- Special infrastructure? (Caching, messaging, etc.)

### Step 2: Create Module Structure

**Use Write and Bash tools directly - NO external scripts needed.**

Create directory structure following hexagonal architecture:

```
modules/{module}/
├── domain/
│   └── src/
│       ├── main/java/{basePackage}/{module}/domain/
│       │   ├── model/           # Aggregates, entities
│       │   ├── vo/              # Value objects (records)
│       │   ├── event/           # Domain events (records)
│       │   └── exception/       # Domain exceptions
│       └── test/java/{basePackage}/{module}/domain/
│
├── application/
│   └── src/
│       ├── main/java/{basePackage}/{module}/application/
│       │   ├── port/
│       │   │   ├── in/          # Use cases (inbound ports)
│       │   │   └── out/         # Repositories (outbound ports)
│       │   └── service/         # Use case implementations
│       └── test/java/{basePackage}/{module}/application/
│
└── adapter/
    ├── in/web/
    │   └── src/main/java/{basePackage}/{module}/adapter/in/web/
    └── out/persistence/
        └── src/main/java/{basePackage}/{module}/adapter/out/persistence/
```

**Example commands**:
```bash
mkdir -p modules/order/domain/src/main/java/com/example/project/order/domain/model
mkdir -p modules/order/domain/src/main/java/com/example/project/order/domain/vo
mkdir -p modules/order/application/src/main/java/com/example/project/order/application/port/in
# ... continue for all directories
```

Create `build.gradle.kts` files using Write tool:

**Domain**:
```kotlin
plugins {
    id("conventions")  // Pure Java, NO Spring
}

dependencies {
    api(project(":libs:common"))
    testImplementation(libs.bundles.java.test)
}
```

**Application**:
```kotlin
plugins {
    id("springBootConventions")
}

dependencies {
    api(project(":modules:order:domain"))
    implementation(project(":libs:common"))
    implementation(libs.spring.boot.starter.core)
    testImplementation(libs.bundles.java.test)
}
```

**Adapter**:
```kotlin
plugins {
    id("springBootConventions")
}

dependencies {
    implementation(project(":modules:order:domain"))
    implementation(project(":modules:order:application"))
    // Add infrastructure dependencies based on needs
    // e.g., libs.spring.boot.starter.data.jpa
}
```

**Update `settings.gradle.kts`**:
```kotlin
include(":modules:order:domain")
include(":modules:order:application")
include(":modules:order:adapter:in:web")
include(":modules:order:adapter:out:persistence")
```

### Step 3: Follow TDD Workflow

**CRITICAL**: Always write tests BEFORE implementation.

**See**: [references/tdd-workflow.md](references/tdd-workflow.md) for complete guide

**Kent Beck's cycle**:
1. **RED**: Write failing test
2. **GREEN**: Minimal code to pass
3. **REFACTOR**: Improve structure
4. **REPEAT**: Next test

**Development order**:
1. **Domain layer** (pure Java, NO Spring)
   - Write domain tests first
   - Implement value objects (records), entities, aggregates
   - Add domain events
2. **Application layer** (Spring allowed)
   - Write use case tests with mocked repositories
   - Implement services
3. **Adapter layer** (infrastructure)
   - Write integration tests
   - Implement controllers, repositories

**Example TDD session**:

```java
// 1. RED: Write failing test
class OrderTest {
    @Test
    void shouldPlaceOrderWithItems() {
        var order = Order.place(customerId, items);

        assertThat(order.getEntityId()).isNotNull();
        assertThat(order.getStatus()).isEqualTo(OrderStatus.PENDING);
    }
}
// Run → FAILS ✗

// 2. GREEN: Minimal implementation
public class Order extends AggregateRoot<OrderId> {
    public static Order place(CustomerId customerId, List<OrderItem> items) {
        if (items.isEmpty()) {
            throw new IllegalArgumentException("Order must contain items");
        }
        var order = new Order(OrderId.generate(), customerId, items, OrderStatus.PENDING);
        order.registerEvent(new OrderPlacedEvent(order.getEntityId()));
        return order;
    }
}
// Run → PASSES ✓

// 3. REFACTOR: Improve (keep tests green)
// 4. REPEAT: Write next test
```

### Step 4: Verify Implementation

Run checks after each refactoring:

```bash
./gradlew :modules:order:test
./gradlew check  # tests + linting + coverage
```

## Architecture Principles

### Hexagonal Architecture (Ports & Adapters)

**See**: [references/hexagonal-architecture.md](references/hexagonal-architecture.md) for complete guide

**Three layers**:
```
Domain (pure) ← Application (orchestration) ← Adapter (infrastructure)
```

**Dependency Rule**: Always point INWARD

**Ports**: Interfaces defining contracts
- Inbound ports: Use cases (what app offers)
- Outbound ports: Repositories (what app needs)

**Adapters**: Concrete implementations
- Inbound adapters: REST, GraphQL, CLI
- Outbound adapters: Databases, APIs, files

### Layer Responsibilities

**See**: [references/layer-responsibilities.md](references/layer-responsibilities.md) for details

**Domain**:
- Pure business logic
- NO framework dependencies
- NO Spring, NO JPA annotations

**Application**:
- Use case orchestration
- Port interfaces
- Spring annotations allowed
- Transaction boundaries

**Adapter**:
- Infrastructure code
- Implement ports
- Any framework/library
- REST, persistence, messaging

### DDD Building Blocks

**See**: [references/ddd-principles.md](references/ddd-principles.md) for complete reference

**Core concepts**:
- **Aggregate Root**: Transaction boundary, publishes events
- **Entity**: Identity-based objects
- **Value Object**: Immutable, validated (use records)
- **Domain Event**: Something that happened (use records)
- **Repository**: Persistence abstraction

## Common Patterns

### Pattern 1: Aggregate Root

```java
public class Order extends AggregateRoot<OrderId> {
    private final CustomerId customerId;
    private final List<OrderItem> items;
    private final OrderStatus status;

    private Order(OrderId entityId, CustomerId customerId,
                  List<OrderItem> items, OrderStatus status) {
        super(entityId);
        this.customerId = customerId;
        this.items = List.copyOf(items);  // Defensive copy
        this.status = status;
    }

    // Factory for new entities (publishes events)
    public static Order place(CustomerId customerId, List<OrderItem> items) {
        if (items.isEmpty()) {
            throw new IllegalArgumentException("Order must contain items");
        }

        var order = new Order(
            OrderId.generate(),
            customerId,
            items,
            OrderStatus.PENDING
        );
        order.registerEvent(new OrderPlacedEvent(order.getEntityId()));
        return order;
    }

    // Factory for reconstitution (no events)
    public static Order from(OrderId entityId, CustomerId customerId,
                            List<OrderItem> items, OrderStatus status,
                            LocalDateTime createdAt, LocalDateTime updatedAt) {
        var order = new Order(entityId, customerId, items, status);
        order.setCreatedAt(createdAt);
        order.setUpdatedAt(updatedAt);
        return order;
    }

    // Business methods (immutable updates)
    public Order cancel() {
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("Only pending orders can be cancelled");
        }

        var cancelled = new Order(getEntityId(), customerId, items, OrderStatus.CANCELLED);
        cancelled.setCreatedAt(getCreatedAt());
        cancelled.setUpdatedAt(getUpdatedAt());
        cancelled.registerEvent(new OrderCancelledEvent(getEntityId()));
        return cancelled;
    }

    // Getters
    public CustomerId getCustomerId() { return customerId; }
    public List<OrderItem> getItems() { return items; }
    public OrderStatus getStatus() { return status; }
}
```

### Pattern 2: Value Object (Record)

```java
// ID value object
public record OrderId(UUID value) implements ValueObject, Serializable {
    public static OrderId generate() {
        return new OrderId(UUID.randomUUID());
    }

    public static OrderId from(String value) {
        return new OrderId(UUID.fromString(value));
    }

    @Override
    public String toString() {
        return value.toString();
    }
}

// Validated value object
public record Email(String value) implements ValueObject {
    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");

    public Email {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Email cannot be blank");
        }
        if (!EMAIL_PATTERN.matcher(value).matches()) {
            throw new IllegalArgumentException("Invalid email format: " + value);
        }
        if (value.length() > 255) {
            throw new IllegalArgumentException("Email must not exceed 255 characters");
        }
    }
}

// Composite value object
public record OAuthInfo(OAuthProvider provider, String providerId)
    implements ValueObject {

    public OAuthInfo {
        if (providerId == null || providerId.isBlank()) {
            throw new IllegalArgumentException("Provider ID cannot be blank");
        }
    }
}
```

### Pattern 3: Use Case (Port)

```java
public interface PlaceOrderUseCase {
    Response execute(Command command);

    record Command(
        String customerId,
        List<OrderItemDto> items
    ) {}

    record Response(String orderId) {}
}

public record OrderItemDto(
    String productId,
    int quantity,
    BigDecimal price
) {}
```

### Pattern 4: Service (Implementation)

```java
@Service
public class PlaceOrderService implements PlaceOrderUseCase {
    private final OrderRepository orderRepository;

    public PlaceOrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @Override
    @Transactional
    public Response execute(Command command) {
        var customerId = CustomerId.from(command.customerId());
        var items = command.items().stream()
            .map(dto -> new OrderItem(
                ProductId.from(dto.productId()),
                new Quantity(dto.quantity()),
                new Money(dto.price())
            ))
            .toList();

        var order = Order.place(customerId, items);
        var saved = orderRepository.save(order);

        return new Response(saved.getEntityId().toString());
    }
}
```

### Pattern 5: Repository Port

```java
// Port (Application layer)
public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(OrderId id);
    void deleteById(OrderId id);
}

// Adapter (Infrastructure layer)
@Repository
public class OrderRepositoryAdapter implements OrderRepository {
    private final OrderJpaRepository persistenceRepo;
    private final DomainEventPublisher eventPublisher;

    public OrderRepositoryAdapter(OrderJpaRepository persistenceRepo,
                                  DomainEventPublisher eventPublisher) {
        this.persistenceRepo = persistenceRepo;
        this.eventPublisher = eventPublisher;
    }

    @Override
    public Order save(Order order) {
        var entity = OrderMapper.toEntity(order);
        var saved = persistenceRepo.save(entity);

        // Publish events
        order.getEvents().forEach(eventPublisher::publish);

        return OrderMapper.toDomain(saved);
    }
}
```

### Pattern 6: Controller (Adapter)

```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final PlaceOrderUseCase placeOrderUseCase;

    public OrderController(PlaceOrderUseCase placeOrderUseCase) {
        this.placeOrderUseCase = placeOrderUseCase;
    }

    @PostMapping
    public ResponseEntity<OrderResponse> placeOrder(@RequestBody PlaceOrderRequest request) {
        var response = placeOrderUseCase.execute(
            new PlaceOrderUseCase.Command(
                request.customerId(),
                request.items()
            )
        );
        return ResponseEntity.ok(new OrderResponse(response.orderId()));
    }
}
```

## Naming Conventions

**Packages**: `{basePackage}.{module}.{layer}.{sublayer}`

**Classes**:
- Aggregate: `Order`, `Customer`
- Value Object: `OrderId`, `Email` (records)
- Event: `OrderPlacedEvent` (records)
- Use Case: `PlaceOrderUseCase`
- Service: `PlaceOrderService`
- Controller: `OrderController`
- Repository Port: `OrderRepository`
- Repository Adapter: `OrderRepositoryAdapter`

## Best Practices

1. **Test first**: Always write failing test before implementation
2. **One test at a time**: Focus on simplest next behavior
3. **Keep domain pure**: NO framework dependencies in domain
4. **Ports before adapters**: Define interfaces before implementations
5. **Immutable domain**: Domain entities return new instances on updates
6. **Events for side effects**: Use domain events for cross-module communication
7. **Run tests frequently**: After every small change
8. **Commit when green**: Never commit failing tests
9. **Use records for value objects**: Immutable by default
10. **Use sealed classes for enums**: Type-safe with pattern matching

## Common Issues

### Issue: Domain using Spring annotations
**Solution**: Remove all Spring dependencies from domain/build.gradle.kts

### Issue: Circular dependencies
**Solution**: Use domain events, not direct module dependencies

### Issue: Tests failing with Spring context errors
**Solution**: Domain tests should NOT load Spring context

### Issue: Records not validating
**Solution**: Use compact constructor with validation

## Project-Specific Adaptation

This skill adapts to your project:
- Read CLAUDE.md for configuration
- Follow project's build system
- Use project's base package
- Adapt to project's conventions

Core principles remain the same:
- Hexagonal architecture
- DDD building blocks
- TDD workflow

## Reference Documentation

- **[Hexagonal Architecture](references/hexagonal-architecture.md)**: Ports & Adapters pattern
- **[Layer Responsibilities](references/layer-responsibilities.md)**: What each layer should/shouldn't do
- **[DDD Principles](references/ddd-principles.md)**: Building blocks and patterns
- **[TDD Workflow](references/tdd-workflow.md)**: Red-Green-Refactor with JUnit 5

## Tools

Claude uses these tools directly (no external scripts):
- **Write**: Create files
- **Bash(mkdir)**: Create directories
- **Edit**: Modify files
- **./gradlew test**: Run tests
- **./gradlew check**: Full quality checks
