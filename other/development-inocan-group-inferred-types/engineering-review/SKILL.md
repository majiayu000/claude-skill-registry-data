---
name: engineering-review
description: Software engineering standards. Use when writing, generating, or reviewing code for SOLID principles, design patterns, and architecture.
allowed-tools: Read, Grep, Glob
---

# Code Review Skill

## When to Use
Invoke this skill when reviewing code for architectural soundness, design patterns, SOLID compliance, and software engineering best practices.

## Review Checklist

### SOLID Principles

| Principle | Check For | Red Flags |
|-----------|-----------|-----------|
| **SRP** - Single Responsibility | Each class/module has one reason to change | God classes, mixed concerns |
| **OCP** - Open/Closed | Extensible via abstraction, not modification | Switch statements on types, frequent edits to existing code |
| **LSP** - Liskov Substitution | Subtypes are substitutable for base types | Square/rectangle problems, violated contracts |
| **ISP** - Interface Segregation | Clients only implement what they need | Fat interfaces, empty method implementations |
| **DIP** - Dependency Inversion | Depend on abstractions, not concretions | Direct instantiation of dependencies, hard-coded types |

### Core Software Engineering Principles

| Principle | Definition | What to Check |
|-----------|------------|---------------|
| **Modularity** | System broken into discrete, self-contained units | Can modules be developed/tested independently? |
| **Cohesion** | How focused a module's responsibilities are | Does the module do one thing well? |
| **Separation of Concerns** | Different aspects isolated from each other | Is UI separate from business logic from data? |
| **Abstraction** | Expose essentials, hide complexity | Are implementation details leaked? |
| **Managed Coupling** | Minimize dependencies between modules | Can modules be changed without cascading effects? |

### Top 10 Code Smells

1. **Memory leaks** - Resources not released, will lead to crashes
2. **Improperly disposed objects** - Missing cleanup, resource exhaustion
3. **ORM misuse** - N+1 queries, lazy loading issues, missing indexes
4. **Security flaws** - Injection, auth bypass, data exposure
5. **Thread-safety issues** - Race conditions, deadlocks, shared mutable state
6. **Object lifetime problems** - Premature disposal, zombie objects
7. **SOLID violations** - See checklist above
8. **Poor exception handling** - Swallowed exceptions, missing context
9. **Scalability blockers** - Synchronous bottlenecks, unbounded resources
10. **Cache/session misuse** - Stale data, memory bloat, missing invalidation

---

## Architecture Styles

### Three-Tier Architecture
- **Presentation** - UI/API layer
- **Business** - Domain logic
- **Data** - Persistence layer
- All tiers are physically separate (unlike MVC which is logical separation)

### Monolith

**Characteristics:**
- Single codebase, unified deployment
- Tight coupling between components
- Centralized data management

**Advantages:**
- Simplicity for small/moderate complexity
- Performance (no inter-service communication)
- Easier deployment

**Disadvantages:**
- Maintenance challenges as it grows
- Scalability limitations (can't scale parts independently)
- Technology lock-in
- Bug in one subsystem can crash entire application

### Service-Oriented Architecture (SOA)

**Key Principles:**
- Well-defined, self-contained services
- Standardized communication protocols (XML, JSON)
- Loose coupling between services
- Service discoverability via registry
- Reusable, composable components

### Microservices

**Characteristics:**
- Small, independently deployable services
- Single responsibility per service
- Loosely coupled via APIs (HTTP, gRPC, message queues)
- Technology agnostic
- Decentralized data management
- Failure isolation

**Review Questions:**
- Is this service aligned with a bounded context?
- Can it be deployed independently?
- Does it communicate via messaging?
- Is it autonomously developed?

---

## Design Patterns

### Creational Patterns
*Focus: Object instantiation*

| Pattern | Purpose | Watch For |
|---------|---------|-----------|
| **Dependency Injection** | Decouple via interfaces, inject implementations | Improves testability/maintainability |
| **Factory Method** | Instantiate and return specific types | Centralizes object creation |
| **Singleton** | Ensure single instance | Can become anti-pattern, global state |
| **Lazy Initialization** | Defer resource allocation until needed | Reduces startup cost |

### Structural Patterns
*Focus: Composition, readability, maintainability*

| Pattern | Purpose | Watch For |
|---------|---------|-----------|
| **Repository** | Abstract data access (facade for data) | Clean separation from business logic |
| **Facade** | Simplify complex subsystems | Single entry point, hides complexity |

### Behavioral Patterns
*Focus: Object communication, modifiability*

| Pattern | Purpose | Watch For |
|---------|---------|-----------|
| **Strategy** | Select algorithm at runtime | Eliminates type-switching if/else |
| **Mediator** | Centralize object communication | Chat rooms, notification engines, pub/sub |

---

## Clean Architecture

**Goal:** Make the business layer immune from changes elsewhere in the application.

### Hexagonal Architecture (Ports & Adapters)
- Separation via ports (interfaces) and adapters (implementations)
- External dependencies easily mocked
- Business logic at the center

### Onion Architecture
- Organized in concentric circles
- Inner layers CAN depend on outer layers
- Outer layers CANNOT depend on inner layers
- Core domain at the center

---

## Domain-Driven Design Concepts

### Bounded Context
A logical boundary within which a specific domain model is defined and consistently used.

**Purpose:**
- Manage complexity by dividing into smaller pieces
- Ensure consistency within the boundary
- Isolate changes from other contexts

**Review Questions:**
- Are terms/entities used consistently within this context?
- Are integration points with other contexts well-defined?
- Does this context have a clear responsibility?

### Fit For Purpose

Software is "fit for purpose" when it meets:

| Quality | Description |
|---------|-------------|
| **Functional** | Includes necessary features for user needs |
| **Reliable** | Performs consistently without failures |
| **Efficient** | Optimal resource usage (CPU, memory, storage) |
| **Usable** | User-friendly, intuitive |
| **Secure** | Protects data from unauthorized access |
| **Maintainable** | Easy to update, modify, troubleshoot |

---

## Event-Driven Architecture Patterns

| Pattern | Description |
|---------|-------------|
| **Queue-Based Load Leveling** | Buffer requests to handle traffic spikes |
| **Claim Check** | Store large payloads separately, pass reference |
| **Competing Consumers** | Multiple consumers process from same queue |

---

## Anti-Patterns to Flag

### Cargo Cult Programming
Dogmatic, ritual, blind application of patterns without understanding purpose.

**Signs:**
- Pattern used but provides no benefit
- Complexity added without solving a problem
- "We always do it this way" reasoning

**Reminder:** Every pattern should serve a real purpose for the specific asset.

---

## Quick Reference

| Concern | Key Question |
|---------|--------------|
| **Responsibility** | Does this class/module have one reason to change? |
| **Coupling** | Can this be changed without cascading effects? |
| **Cohesion** | Are all parts of this module related? |
| **Abstraction** | Are implementation details hidden? |
| **Testability** | Can dependencies be mocked? |
| **Scalability** | Can this scale independently if needed? |
| **Security** | Are inputs validated? Data protected? |
| **Error Handling** | Are failures handled gracefully with context? |
