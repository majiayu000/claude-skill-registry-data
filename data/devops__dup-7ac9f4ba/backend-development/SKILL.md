---
name: backend-development
description: Provides development guidance for implementing backend features using Domain-Driven Design, hexagonal architecture, event-driven patterns, and HATEOAS conventions. Use when implementing new domain features, REST APIs, or integrating cross-domain functionality in the backend.
---

# Backend DDD Development Patterns Guide

## Architecture Overview

This project follows Domain-Driven Design (DDD) principles with hexagonal architecture:

```
Domain Layer
├── Aggregate Roots (@AggregateRoot)
├── Entities (@Entity)
├── Value Objects (Records)
├── Commands
└── Repository Interfaces (Secondary Ports)

Infrastructure Layer
├── REST API Controllers (@ApiController)
├── Application Services (@Service)
├── Repository Implementations (Secondary Adapters)
├── Event Listeners (@EventListener)
└── Jackson Converters (@JacksonComponent)
```

### Reference Implementation

The `club.klabis.calendar` package demonstrates these patterns:
- **Domain**: Calendar aggregate with CalendarItem entities
- **Commands**: CreateCalendarItemCommand for user intents
- **Events**: EventListeners for cross-domain integration
- **API**: CalendarApiController with HATEOAS support

## Key Design Patterns

### 1. DDD Annotations (jMolecules)

Mark architectural roles explicitly:

```java
@AggregateRoot      // Marks the aggregate root class
@Entity             // Marks entities within aggregates
@Identity           // Marks identity fields
@Service            // Marks application/domain services
@Repository         // Marks repository interfaces
```

**Usage**: Apply at class level to clarify domain semantics.

### 2. Aggregate Root Pattern

An aggregate is a cluster of domain objects treated as a single unit:

**Characteristics**:
- One aggregate root (public entry point)
- Contains entities and value objects
- Enforces business rules and invariants
- Has identity field marked with `@Identity`
- Manages its internal consistency

**Example structure**:
```java
@AggregateRoot
public class MyAggregate extends AbstractAggregateRoot<MyAggregate> {
    @Identity
    private AggregateId id;
    private Set<InternalEntity> children = new HashSet<>();

    // Business rule enforcement
    public void doSomething(Command cmd) {
        if (!isValidFor(cmd)) {
            throw new IllegalArgumentException("Cannot execute");
        }
        // Modify state
        this.children.add(new InternalEntity(...));
    }

    public Set<InternalEntity> getChildren() {
        return Collections.unmodifiableSet(children);
    }
}
```

### 3. Entity Design

Entities have identity and mutable state:

**Characteristics**:
- Identity field (typically nested record with value wrapper)
- Marked with `@Entity` within aggregate
- Can be modified through methods
- Equality based on identity, not state

**Example**:
```java
@Entity
public class ItemEntity {
    @Identity
    private Id id;
    private String status;
    private LocalDateTime createdAt;

    public record Id(long value) {
        static long MAX_VALUE = 0L;
        static synchronized Id newId() {
            return new Id(MAX_VALUE++);
        }
    }

    public static ItemEntity create() {
        return new ItemEntity(Id.newId(), "PENDING", LocalDateTime.now());
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) return true;
        if (obj == null || obj.getClass() != this.getClass()) return false;
        var that = (ItemEntity) obj;
        return this.id == that.id;  // Identity-based equality
    }
}
```

### 4. Value Objects as Records

Use immutable Java records for value objects:

```java
public record DateRange(LocalDate start, LocalDate end) {
    public DateRange {
        // Validation in compact constructor
        Assert.isTrue(!start.isAfter(end), "Start must not be after end");
    }

    public boolean includes(LocalDate date) {
        return !start.isAfter(date) && !end.isBefore(date);
    }
}
```

**Benefits**:
- Immutability enforced by compiler
- Auto-generated equals/hashCode/toString
- Compact syntax for simple objects

### 5. Command Pattern

Commands encapsulate user intents and data:

```java
public record CreateItemCommand(String name, String description, LocalDate dueDate) {
    public CreateItemCommand {
        // Validation in compact constructor
        Assert.hasText(name, "Name required");
    }

    // Factory methods for common cases
    public static CreateItemCommand quickTask(String name) {
        return new CreateItemCommand(name, "", LocalDate.now());
    }
}
```

**Command Handler**:
```java
public class MyAggregate extends AbstractAggregateRoot<MyAggregate> {
    public Item handle(CreateItemCommand command) {
        if (!canCreate(command)) {
            throw new IllegalArgumentException("Cannot create item");
        }
        Item item = Item.create(command.name(), command.description());
        this.items.add(item);
        return item;
    }
}
```

### 6. Repository Pattern

Repository interfaces define the contract for data access (Secondary Port):

```java
public interface MyRepository extends DataRepository<Item, Item.Id> {
    // Domain-specific queries
    Optional<Item> findByName(String name);
    List<Item> findAllActive();
    Optional<MyAggregate> readAggregate(AggregateId id);
}
```

**Design Principles**:
- Interface in domain package (secondary port)
- Implementation in infrastructure (secondary adapter)
- Use domain types, not DTOs
- Query methods return domain objects
- `readAggregate()` loads full aggregate with children

### 7. Application Service Layer

Services coordinate domain logic with infrastructure:

```java
@Service
@Component
public class MyApplicationService {
    private final MyRepository repository;
    private final EventPublisher eventPublisher;

    public MyApplicationService(MyRepository repository, EventPublisher eventPublisher) {
        this.repository = repository;
        this.eventPublisher = eventPublisher;
    }

    @Transactional
    public Item createItem(CreateItemCommand command) {
        MyAggregate agg = repository.readAggregate(command.aggregateId());
        Item item = agg.handle(command);
        repository.save(agg);
        return item;
    }
}
```

**Responsibilities**:
- Orchestrate domain operations
- Handle transactions with `@Transactional`
- Publish domain events
- Convert between domain and API layers

### 8. REST API Controller

Controllers expose domain functionality via HTTP:

```java
@ApiController(openApiTagName = "items", path = "/items")
@ExposesResourceFor(Item.class)
public class ItemApiController {

    private final MyApplicationService service;
    private final ModelAssembler<Item, ItemDto> assembler;

    @Relation(collectionRelation = "items")
    public record ItemDto(String name, String status, Link parentLink) {}

    @GetMapping
    public CollectionModel<EntityModel<ItemDto>> listItems() {
        List<Item> items = service.listAll();
        return assembler.toCollectionModel(items);
    }

    @PostMapping
    public ResponseEntity<Void> createItem(@RequestBody CreateItemCommand cmd) {
        Item item = service.createItem(cmd);
        return ResponseEntity.created(toSelfLink(item).toUri()).build();
    }
}
```

**Patterns**:
- DTOs for API contracts with `@Relation` annotation
- Convert domain objects to DTOs
- Use `ModelAssembler` for HATEOAS links
- `@ExposesResourceFor` declares exposed domain type
- Separate postprocessors for enriching responses

### 9. HATEOAS Representation Processors

Enrich API responses with hypermedia links:

```java
@Component
class ItemRepresentationProcessor
    implements RepresentationModelProcessor<EntityModel<ItemDto>> {

    @Override
    public EntityModel<ItemDto> process(EntityModel<ItemDto> model) {
        model.add(linkTo(methodOn(ItemApiController.class)
            .updateItem(null)).withRel("update"));
        return model;
    }
}

@Component
class ItemListRepresentationProcessor
    implements RepresentationModelProcessor<CollectionModel<EntityModel<ItemDto>>> {

    @Override
    public CollectionModel<EntityModel<ItemDto>> process(CollectionModel<...> model) {
        model.add(linkTo(methodOn(ItemApiController.class)
            .createItem(null)).withRel("create"));
        return model;
    }
}
```

### 10. Event-Driven Integration

React to domain events from other bounded contexts:

```java
@Component
class DomainEventListeners {
    private final MyRepository repository;

    @EventListener(OtherDomainEventOccurred.class)
    public void onExternalEvent(OtherDomainEventOccurred event) {
        // React to event from another bounded context
        Item item = repository.findById(itemId)
            .orElseGet(() -> Item.createFrom(event));

        // Update or create based on event data
        item.updateFrom(event);
        repository.save(item);
    }
}
```

**Patterns**:
- Use `@EventListener` with event class
- Extract aggregate from event: `event.getAggregate()`
- Find existing or create new: `findById().orElseGet()`
- React asynchronously to cross-domain changes

### 11. Jackson Custom Serialization

Handle special type serialization:

```java
@JacksonComponent
class ItemIdSerializer extends ValueSerializer<Item.Id>
    implements Converter<Item.Id, String> {

    @Override
    public void serialize(Item.Id value, JsonGenerator gen, SerializationContext ctxt) {
        ctxt.findValueSerializer(Long.class)
            .serialize(value?.value(), gen, ctxt);
    }

    @Override
    public String convert(Item.Id source) {
        return source != null ? Long.toString(source.value()) : null;
    }
}
```

**Used for**: Converting domain value objects to/from JSON in API layer.

## Development Workflow

### Implementing a New Feature

1. **Analyze the requirement**
   - Identify aggregate roots
   - Define entities and value objects
   - Determine invariants and business rules

2. **Design domain model**
   - Create aggregate root with `@AggregateRoot`
   - Add entities with `@Entity`
   - Use records for value objects
   - Implement business rules in aggregate

3. **Create commands**
   - Define command records
   - Add validation in compact constructors
   - Create factory methods for common cases

4. **Define repository contract**
   - Create interface extending `DataRepository<T, ID>`
   - Add domain-specific query methods
   - Include aggregate loading method

5. **Implement repository**
   - Create adapter class in infrastructure
   - Implement all interface methods
   - Handle queries with business-appropriate logic

6. **Create application service**
   - Inject repository interface
   - Create public methods for use cases
   - Implement command handling via `aggregate.handle()`
   - Add `@Transactional` for writes

7. **Build REST API**
   - Create DTOs with `@Relation`
   - Implement controller methods
   - Use `ModelAssembler` for HATEOAS
   - Create representation processors

8. **Add event listeners** (if needed)
   - Create listener component
   - React to external domain events
   - Update/create domain objects
   - Save to repository

### Using Factory Methods

Create consistent object construction:

```java
// In aggregate
public static MyAggregate create(Id id) {
    return new MyAggregate(id, new HashSet<>(), LocalDateTime.now());
}

// In entity
public static Item task(String name) {
    return new Item(Id.newId(), name, ItemStatus.TODO);
}

// In command
public static CreateItemCommand quickItem(String name) {
    return new CreateItemCommand(name, "", LocalDate.now());
}
```

### Immutable Collections

Always return unmodifiable collections from aggregates:

```java
public Set<Item> getItems() {
    return Collections.unmodifiableSet(items);
}

public List<Item> getOrderedItems() {
    return Collections.unmodifiableList(new ArrayList<>(items));
}
```

### Fluent/Builder API

Enable method chaining:

```java
public Item withStatus(ItemStatus status) {
    this.status = status;
    return this;
}

public Item withDescription(String description) {
    this.description = description;
    return this;
}

// Usage
Item item = Item.create()
    .withStatus(ACTIVE)
    .withDescription("Important task");
```

### DateTime Handling

**Convention**:
- **Domain**: Use `ZonedDateTime` for temporal data with timezone info
- **Value Objects**: Use `LocalDate` or `LocalDateTime` for timezone-agnostic data
- **API**: Convert to `LocalDate` in DTOs
- **Conversion**: Use shared utility functions

```java
// In domain
private ZonedDateTime createdAt = ZonedDateTime.now();

// In DTO (API)
public record ItemDto(LocalDate createdDate, ...) {}

// Conversion in controller
ItemDto toDto(Item item) {
    return new ItemDto(Globals.toLocalDate(item.getCreatedAt()), ...);
}
```

## Code Style Conventions

### Naming

```
Classes:        PascalCase (MyAggregate, ItemEntity)
Methods:        camelCase (createItem, readAggregate)
Constants:      UPPER_SNAKE_CASE (MAX_ITEMS, DEFAULT_STATUS)
Records:        PascalCase (ItemDto, CreateItemCommand)
Packages:       lowercase.reversed.domain (org.club.klabis.feature.domain)
```

### Method Organization

1. Annotations
2. Fields/Properties
3. Nested Classes/Records
4. Constructors
5. Factory/Builder methods (static)
6. Public behavior methods
7. Accessor methods (getters)
8. equals/hashCode/toString

### Validation Style

```java
// In compact record constructor - for value objects
public record DateRange(LocalDate start, LocalDate end) {
    public DateRange {
        Assert.isTrue(!start.isAfter(end), "Start must not be after end");
    }
}

// In methods - for business logic errors
public void schedule(LocalDateTime time) {
    if (time.isBefore(LocalDateTime.now())) {
        throw new IllegalArgumentException("Cannot schedule in past");
    }
}
```

### Import Organization

```java
import java.*;          // Java standard library
import java.time.*;     // Java time APIs
import org.springframework.*;  // Framework
import org.jmolecules.*; // DDD annotations
import club.klabis.*;    // Local packages
```

## Common Patterns Reference

### Find or Create Pattern

```java
Item item = repository.findById(id)
    .map(existing -> {
        existing.updateFrom(event);
        return existing;
    })
    .orElseGet(() -> Item.createFrom(event));

repository.save(item);
```

### Optional Chaining

```java
Optional<Item> result = repository.findById(id)
    .filter(item -> item.isActive())
    .map(item -> item.withStatus(UPDATED));
```

### Validation in Constructor

```java
protected MyAggregate(Id id, Set<Item> items) {
    Assert.notNull(id, "ID required");
    Assert.notEmpty(items, "At least one item required");
    this.id = id;
    this.items.addAll(items);
}
```

### Transaction Boundary

```java
@Transactional
public Item processCommand(Command cmd) {
    MyAggregate agg = repository.readAggregate(cmd.aggregateId());
    Item result = agg.handle(cmd);
    return repository.save(agg);
}
```

### HATEOAS Link Building

```java
Link selfLink = linkTo(methodOn(ItemController.class)
    .getItem(item.getId())).withSelfRel();

model.add(selfLink);
model.add(linkTo(methodOn(ItemController.class)
    .deleteItem(item.getId())).withRel("delete"));
```

## Testing Patterns

### Unit Test - Domain Logic

```java
@Test
void aggregateEnforcesBusinessRule() {
    var agg = MyAggregate.create(id);

    assertThrows(IllegalArgumentException.class, () -> {
        agg.doInvalidOperation();
    });
}
```

### Unit Test - Repository Mock

```java
@Test
void serviceUsesRepository() {
    var repo = mock(MyRepository.class);
    var service = new MyApplicationService(repo);

    when(repo.findById(id)).thenReturn(Optional.of(item));
    var result = service.getItem(id);

    verify(repo).findById(id);
    assertNotNull(result);
}
```

### Integration Test - End-to-End

```java
@Test
void endToEndFeatureWorks() {
    var cmd = CreateItemCommand.quickItem("Test");
    var result = service.createItem(cmd);

    var found = repository.findById(result.getId());
    assertTrue(found.isPresent());
    assertEquals("Test", found.get().getName());
}
```

## FAQ

**Q: Should I put business logic in the service or the aggregate?**
A: Business logic belongs in the aggregate. The service orchestrates and handles transactions.

**Q: How do I handle validation errors?**
A: Use exceptions for user input errors. Use `Assert` for internal invariants. Catch and convert to HTTP errors in controller.

**Q: When should I use an event listener vs a direct service call?**
A: Use event listeners for cross-domain/bounded context integration. Use direct calls within the same domain.

**Q: What's the difference between a Command and a DTO?**
A: Commands represent user intent with business semantics. DTOs are data transfer objects for serialization.

**Q: How do I model optional fields?**
A: Use `@Nullable` annotation. Handle nulls in value object methods. Use `Optional` in query methods.

**Q: Should repository queries return Optional or List?**
A: Single item by identity: `Optional<T>`. Multiple items or searches: `List<T>`.

## Common Gotchas

1. **Modifying collections from outside**: Always return unmodifiable collections
2. **Equality checks**: Base entity equality on identity, not state
3. **Lazy loading**: Eager load children when reading aggregate
4. **Transaction scope**: Ensure related operations are in same transaction
5. **DTO pollution**: Don't use DTOs in domain layer
6. **Event ordering**: Event listeners may execute in any order - design for this
7. **Null handling**: Use `@Nullable` annotations and check before dereferencing

## References

**Package Locations**:
- Domain layer: `src/main/java/club/klabis/{feature}/`
- Infrastructure: `src/main/java/club/klabis/{feature}/infrastructure/`
- Tests: `src/test/java/club/klabis/{feature}/`

**Key Classes** (Examples from reference implementation):
- Aggregate: `club.klabis.calendar.Calendar`
- Entity: `club.klabis.calendar.CalendarItem`
- Command: `club.klabis.calendar.CreateCalendarItemCommand`
- Repository: `club.klabis.calendar.CalendarRepository`
- Service: `club.klabis.calendar.infrastructure.CalendarService`
- Controller: `club.klabis.calendar.infrastructure.CalendarApiController`
- Listener: `club.klabis.calendar.infrastructure.EventListeners`
