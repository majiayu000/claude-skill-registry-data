---
name: ddd-clean-architecture
description: Implement domain-driven design (DDD) and clean architecture patterns in ASP.NET Core Web APIs. Use this skill when building or refactoring backend services that need strategic domain modeling, tactical DDD patterns (entities, value objects, aggregates, domain events, repositories), and clean architecture layers (domain, application, infrastructure, presentation). Follows principles from Eric Evans' "Domain-Driven Design" and Robert C. Martin's "Clean Architecture".
license: Complete terms in LICENSE.txt
---

This skill guides implementation of domain-driven design and clean architecture patterns in ASP.NET Core Web APIs, following the strategic and tactical patterns from Eric Evans' "Domain-Driven Design" and the architectural principles from Robert C. Martin's "Clean Architecture".

The user provides backend requirements: a feature, bounded context, aggregate, or architectural refactoring to implement. They may include domain context, business rules, or technical constraints.

## Strategic Design Principles

Before coding, understand the domain and establish clear boundaries:

- **Ubiquitous Language**: Identify key domain terms and use them consistently in code, comments, and conversations
- **Bounded Contexts**: Define clear boundaries where a domain model applies. Each bounded context has its own model and language
- **Context Mapping**: Understand relationships between bounded contexts (Shared Kernel, Customer-Supplier, Anti-Corruption Layer, etc.)
- **Core Domain**: Identify what makes the business unique and valuable. Invest the most effort here
- **Subdomains**: Distinguish between Core, Supporting, and Generic subdomains to allocate appropriate design effort

## Clean Architecture Layers

Organize code into layers with clear dependency rules (dependencies point inward):

### 1. Domain Layer (Innermost - No Dependencies)

- **Entities**: Objects with identity that persist through time and state changes
- **Value Objects**: Immutable objects defined by their attributes, not identity
- **Aggregates**: Cluster of entities and value objects with a root entity enforcing invariants
- **Domain Events**: Events that domain experts care about
- **Domain Services**: Operations that don't belong to a single entity
- **Specifications**: Business rule predicates that can be combined and reused
- **Enumerations**: Domain-specific enumeration types (use strongly-typed enums)

### 2. Application Layer (Orchestration - Depends on Domain)

- **Use Cases/Commands**: Application-specific business operations (CQRS commands)
- **Queries**: Read operations returning DTOs (CQRS queries)
- **Application Services**: Coordinate use cases, manage transactions
- **DTOs**: Data transfer objects for crossing boundaries
- **Interfaces**: Repository interfaces, external service interfaces (defined here, implemented in Infrastructure)
- **Validators**: Input validation using FluentValidation

### 3. Infrastructure Layer (External - Depends on Application & Domain)

- **Persistence**: EF Core DbContext, repository implementations
- **External Services**: API clients, message queues, email services
- **Identity & Security**: Authentication, authorization implementations
- **Caching**: Redis, in-memory cache implementations
- **File Storage**: Blob storage, file system operations
- **Configuration**: Options pattern implementations

### 4. Presentation Layer (API - Depends on Application)

- **Controllers**: Thin controllers that delegate to application layer
- **Minimal APIs**: Endpoint definitions (if using minimal API pattern)
- **Middleware**: Cross-cutting concerns (logging, exception handling)
- **Filters**: Action filters, exception filters
- **Models**: API request/response models (different from DTOs)

## Tactical DDD Patterns Implementation

### Entities

- Entities have identity that persists through time and state changes
- Follow the entity base class pattern established in the project
- Implement equality based on identity (Id property)
- Encapsulate business rules and invariants within entities

### Value Objects

- Use C# records for immutable value objects
- Define value objects by their attributes, not identity
- Records provide structural equality by default
- Keep value objects simple and focused on domain concepts

### Aggregates

- Identify aggregate boundaries based on transactional consistency needs
- Ensure one root entity per aggregate
- Enforce invariants in the aggregate root
- Reference other aggregates by identity only
- Keep aggregates small and focused

### Domain Events

- Define domain events for important business occurrences
- Raise events within entities/aggregates when state changes occur
- Handle events at the application layer for cross-aggregate coordination

### Repository Pattern

- Define specific repository interfaces for each aggregate root
- Place interfaces in the Application or Domain layer
- Implement repositories in the Infrastructure layer using EF Core
- Avoid generic repositories - create focused, aggregate-specific repositories
- Repository methods should reflect domain operations, not just CRUD

### Result Pattern

- Use ErrorOr library for operation outcomes
- Return `ErrorOr<T>` from application services and use cases
- Avoid exceptions for flow control
- Provide meaningful error types for different failure scenarios

## Essential NuGet Packages

- **ErrorOr**: For error handling and result pattern
- **FluentValidation**: For input validation
- **Entity Framework Core**: For persistence

## Implementation Guidelines

1. **Start with the Domain**: Model the core domain first, independent of infrastructure
2. **Protect Invariants**: Encapsulate business rules within entities and aggregates
3. **Explicit is Better**: Make implicit concepts explicit (value objects, domain events)
4. **Persistence Ignorance**: Domain layer should not depend on ORM or database concerns
5. **Dependency Inversion**: High-level modules should not depend on low-level modules
6. **Unit of Work**: Manage transactions at the application layer
7. **Thin Controllers**: Controllers should only validate, delegate, and return results
8. **Avoid Anemic Models**: Put behavior in the domain, not just in services
9. **Test Domain Logic**: Focus testing efforts on domain and application layers
10. **Evolution**: Design should evolve with understanding; refactor as knowledge grows

## Anti-Patterns to Avoid

- **Anemic Domain Model**: Entities with only getters/setters and no behavior
- **Transaction Script**: Business logic scattered in service classes
- **God Aggregate**: Aggregates that are too large and do too much
- **Repository Overload**: Repositories with dozens of query methods
- **Infrastructure Leakage**: Domain layer depending on infrastructure concerns
- **CRUD Thinking**: Modeling operations as simple create/read/update/delete
- **Generic Repositories**: Abstraction that doesn't add value and hinders querying
- **MediatR Overuse**: Don't use MediatR unless explicitly requested - keep it simple

```console
src/
├── Domain/
│   ├── Common/
│   │   ├── Entity.cs
│   │   ├── ValueObject.cs
│   │   └── DomainEvent.cs
│   ├── Orders/
│   │   ├── Order.cs (Aggregate Root)
│   │   ├── OrderItem.cs (Entity)
│   │   ├── Money.cs (Value Object)
│   │   └── Events/
│   │       └── OrderPlacedEvent.cs
│   └── Customers/
├── Application/
│   ├── Common/
│   │   ├── Behaviors/
│   │   └── Interfaces/
│   ├── Orders/
│   │   ├── Commands/
│   │   ├── Queries/
│   │   └── DTOs/
│   └── DependencyInjection.cs
├── Infrastructure/
│   ├── Persistence/
│   │   ├── ApplicationDbContext.cs
│   │   ├── Configurations/
│   │   └── Repositories/
│   ├── Services/
│   └── DependencyInjection.cs
└── WebApi/
    ├── Controllers/
    ├── Middleware/
    └── Program.cs
```

Remember: DDD is about modeling complex domains. If the domain is simple (CRUD), don't over-engineer. Apply DDD patterns where complexity justifies the investment. Clean architecture provides structure; DDD provides rich domain modeling within that structure.
