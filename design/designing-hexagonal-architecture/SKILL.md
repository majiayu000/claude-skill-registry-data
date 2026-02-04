---
name: designing-hexagonal-architecture
description: Guides the design and analysis of hexagonal architecture (Ports & Adapters) for backend systems. Use when structuring modular applications with clean separation between business logic and infrastructure.
---

# Designing Hexagonal Architecture

## Philosophy / Approach

Hexagonal Architecture, also known as Ports & Adapters pattern, is an architectural pattern proposed by Alistair Cockburn that aims to separate the core business logic of an application from external infrastructure. The philosophy centers on creating a flexible, testable, and maintainable system by inverting dependencies and isolating the domain from technical concerns.

The hexagonal shape represents the idea that the application has multiple "sides" where it interacts with the outside world, and each side is interchangeable. This approach enables:

- **Technology Independence**: Business logic doesn't depend on specific frameworks or databases
- **Testability**: Core domain can be tested without infrastructure
- **Flexibility**: External components can be replaced without affecting business rules
- **Maintainability**: Clear boundaries make reasoning about the system easier

## When to Use This Skill

- Designing new project architecture
- Refactoring inter-module dependencies

This skill is particularly valuable when building enterprise applications, microservices, or any system where long-term maintainability and testability are priorities.

## Core Concepts

Hexagonal Architecture is built on several fundamental principles that work together to create a robust, maintainable system.

### 1. Layer Separation

The application is organized into distinct layers, each with specific responsibilities:

- **Presentation Layer**: HTTP requests/responses, DTO transformation, user interface concerns
- **Application Layer**: Business logic orchestration, transaction management, use case implementation
- **Domain Layer**: Core business rules, domain models, business validations
- **Infrastructure Layer**: Database access, external APIs, file systems, third-party integrations

The dependency direction flows from outer layers toward the domain at the center.

### 2. Port - Interface Abstraction

Ports define the boundaries between the domain and the outside world. They are interfaces that express what the business logic needs without specifying how it's implemented.

**Characteristics of Ports:**
- Defined as interfaces or abstract contracts
- Located in or near the domain layer
- Express business needs in domain language
- Independent of implementation details

### 3. Adapter - Concrete Implementation

Adapters are concrete implementations of Port interfaces. They handle the actual communication with external systems and infrastructure.

**Types of Adapters:**
- **Primary/Driving Adapters**: Controllers, REST endpoints, GraphQL resolvers (drive the application)
- **Secondary/Driven Adapters**: Repositories, external service clients, messaging systems (driven by the application)

Adapters translate between the domain's language and the technical protocols of external systems.

### 4. Dependency Inversion

One of the most critical principles: dependencies point inward, toward the domain.

**Dependency Flow:**
```
External → Infrastructure → Application → Domain
```

**Key Rules:**
- Inner layers (domain) must never depend on outer layers
- Business logic remains independent of infrastructure
- Interfaces are defined by the domain, implemented by infrastructure

### 5. Applying SOLID Principles

Hexagonal Architecture naturally aligns with SOLID principles:

- **Single Responsibility**: Each module handles one specific concern
- **Open/Closed**: System is open for extension (new adapters) but closed for modification (domain remains stable)
- **Liskov Substitution**: Adapters implementing the same port are interchangeable
- **Interface Segregation**: Ports expose only the methods needed by the domain
- **Dependency Inversion**: Domain depends on abstractions (ports), not concrete implementations (adapters)

### 6. Module Independence

Each domain module operates independently with minimal coupling:

- Clear boundaries between modules
- Communication through well-defined interfaces
- Circular dependencies resolved through design patterns
- Modules can be deployed, tested, and scaled independently

## Implementation Workflow

### Step 1: Identify Domain Boundaries

Begin by understanding your business domains and their relationships. Map out:
- Core business entities and their responsibilities
- Natural boundaries between different business concerns
- Use cases and workflows within each domain

### Step 2: Define Ports

For each domain module, identify what it needs from the outside world and what it provides to others:
- **Inbound Ports**: Use cases the domain exposes (service interfaces)
- **Outbound Ports**: Dependencies the domain requires (repository interfaces, external service interfaces)

### Step 3: Implement Domain Logic

Build the core business logic without any infrastructure concerns:
- Create domain models and entities
- Implement business rules and validations
- Write services that orchestrate use cases
- Keep domain logic pure and testable

### Step 4: Create Adapters

Implement concrete adapters for each port:
- Primary adapters to expose domain functionality (controllers, event handlers)
- Secondary adapters to fulfill domain dependencies (database repositories, API clients)

### Step 5: Configure Dependency Injection

Wire everything together using a DI container:
- Bind port interfaces to adapter implementations
- Configure module relationships
- Resolve circular dependencies if needed

## Patterns / Examples

Hexagonal Architecture can be implemented in various programming languages and frameworks. We provide detailed examples for:

- **[TypeScript/NestJS](./examples/TYPESCRIPT.md)**: Full implementation with NestJS dependency injection, decorators, and Prisma ORM
- **[Ruby on Rails](./examples/RUBY_ON_RAILS.md)**: Rails-friendly approach with service objects, repositories, and Active Record integration
- **[Java Spring](./examples/JAVA_SPRING.md)**: Spring Boot implementation with Spring Data JPA, component scanning, and annotations
- **[Kotlin Spring](./examples/KOTLIN_SPRING.md)**: Kotlin Spring Boot implementation with coroutines support, null safety, and idiomatic Kotlin patterns

Each example demonstrates:
1. Port Interface Definition
2. Adapter Implementation
3. Module Configuration with Dependency Injection
4. Repository Pattern (Infrastructure Layer)
5. Complete Layered Architecture
6. Using Ports in Other Modules
7. Testing with Mocks

Choose the example that matches your technology stack to see concrete implementations of the concepts discussed in this skill.

## Best Practices

### Clear Layer Separation

Maintain strict separation between layers with consistent dependency direction. Each layer should have a single, well-defined responsibility. Never allow business logic to leak into presentation or infrastructure layers.

**Guidelines:**
- Controllers should only handle HTTP concerns (validation, serialization)
- Services contain business logic and orchestration
- Repositories handle data persistence
- Keep domain models independent of ORM annotations

### Minimize Port Interfaces

Design ports to expose only the methods needed by the domain. Follow the Interface Segregation Principle by creating focused, role-specific interfaces rather than large, monolithic ones.

**Guidelines:**
- Create separate ports for different client needs
- Avoid "god interfaces" with many unrelated methods
- Name ports based on their business purpose
- Keep port methods at the right level of abstraction

### Domain-Based Module Separation

Organize code by business domain rather than technical layers. Each domain module should be cohesive and loosely coupled from other domains.

**Guidelines:**
- Use forwardRef to resolve circular dependencies when necessary
- Communicate between modules through ports/adapters
- Keep each module independently testable
- Consider domain boundaries when splitting modules

## Common Pitfalls

### Managing Circular Dependencies

Circular dependencies between modules indicate design issues. While forwardRef provides a technical solution, it's important to analyze the root cause.

**Warning Signs:**
- Multiple modules depending on each other
- Deep dependency chains that loop back
- Difficulty in testing modules in isolation

**Solutions:**
- Introduce a shared kernel for common concepts
- Use events for decoupled communication
- Extract a new module if responsibilities are mixed
- Apply dependency inversion through ports

### Consider Testability

Architecture should facilitate testing, not hinder it. Ports enable easy mocking, but only if designed properly.

**Common Issues:**
- Ports that expose implementation details
- Tight coupling between layers despite using interfaces
- Difficulty in creating test doubles

**Solutions:**
- Design ports from the domain's perspective
- Use constructor injection for all dependencies
- Create in-memory adapters for testing
- Write tests that don't require infrastructure

### Avoid Over-Abstraction

Not every interaction needs a port-adapter pair. Over-engineering leads to unnecessary complexity.

**When to Avoid:**
- Simple CRUD operations with no business logic
- One-to-one mapping between port and adapter with no variation
- Internal utilities that won't change

**Balance:**
- Start simple, add abstraction when needed
- Apply ports where flexibility matters
- Consider the likelihood of implementation changes

### Performance Impact Analysis

Layer separation and indirection can introduce overhead. Monitor and optimize where necessary.

**Considerations:**
- Extra method calls through ports/adapters
- Object mapping between layers
- Transaction boundaries across layers

**Optimization Strategies:**
- Use profiling to identify actual bottlenecks
- Apply caching at appropriate layers
- Consider batch operations for high-volume scenarios
- Don't optimize prematurely - measure first

## Additional Resources

- Clean Architecture by Robert C. Martin
- Domain-Driven Design by Eric Evans
- Hexagonal Architecture by Alistair Cockburn (original article)
- Ports and Adapters Pattern documentation
