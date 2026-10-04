---
name: java-oop-solid-design
category: architecture
description: Use when modelling a rich domain in Java - SOLID principles, encapsulated entities that enforce their own invariants, and value objects over primitives
tech_stack: Java
---
# Java OOP & SOLID Design

## Overview

Java is chosen precisely when the domain is rich (see java-vs-go-decision). That value is only realized if you model it with real objects that protect their invariants — not anemic data bags with a pile of setters and logic scattered in services.

**Core principle:** Objects own their invariants. If a rule about an entity can be violated from outside the entity, the model is broken.

## SOLID, concretely

- **S — Single Responsibility:** one reason to change per class. A class that parses HTTP, applies business rules, and writes SQL is three classes.
- **O — Open/Closed:** extend behavior via new types/strategies, not by editing a growing `switch`. New payment method → new `PaymentMethod` implementation, not another `case`.
- **L — Liskov:** a subtype must honor the supertype's contract. If `Square extends Rectangle` breaks `setWidth`, the hierarchy is wrong — prefer composition.
- **I — Interface Segregation:** many small role interfaces over one fat one. A caller that needs `read` shouldn't depend on `write`.
- **D — Dependency Inversion:** services depend on interfaces (ports), not concrete adapters. Inject the interface via the constructor.

## Encapsulation over anemic models

```java
// ❌ anemic: invariant lives nowhere, anyone can break it
class Task {
    public String title;      // no bound enforced
    public Status status;
}
task.title = "x".repeat(500); // invalid state, no guard

// ✅ rich: the entity enforces its own rules
public final class Task {
    private final TaskId id;
    private String title;
    private Status status;

    private Task(TaskId id, String title) { this.id = id; this.title = title; }

    public static Task create(String title) {
        if (title == null || title.isBlank() || title.length() > 200)
            throw new InvalidTaskTitle(title);
        return new Task(TaskId.newId(), title);
    }

    public void rename(String title) { /* same guard, reused */ }
    public void complete() {
        if (status == Status.DONE) throw new IllegalTransition("already done");
        this.status = Status.DONE;
    }
    // getters, no public setters
}
```

## Value objects over primitives

Wrap meaningful primitives: `TaskId`, `Email`, `Money` — not raw `String`/`long`/`BigDecimal`. A `TaskId` can't be accidentally passed where a `UserId` is expected, and validation lives in one place. Java `record` makes these cheap.

## Prefer

- `record` for immutable value objects and DTOs.
- `sealed` interfaces + pattern matching for closed hierarchies (states, commands).
- Immutability by default; expose behavior methods, not setters.
- Throw domain exceptions (`InvalidTaskTitle`) mapped to HTTP status at the boundary — not raw `IllegalArgumentException` leaking out.

Prefer a `sealed` interface + exhaustive `switch` pattern matching (final since Java 21) for a closed set of states or commands over a type enum plus `if`/`instanceof` chains — the compiler then refuses to let a new case go unhandled.

## Common Mistakes

- Public setters that let callers build invalid state.
- Business rules in the service that should be on the entity.
- `String`/`long` everywhere instead of value objects.
- A god-service with dozens of methods and no domain objects.
- Lombok `@Data`/`@EqualsAndHashCode` on a JPA entity — it pulls in lazy associations (forcing a load, or crashing outside the session) and generates a mutable, settable id that breaks `equals`/`hashCode` once the entity is persisted. Write `equals`/`hashCode` on the id only, or skip Lombok on entities.

## Red Flags

- An entity with only getters/setters and no behavior.
- The same validation copy-pasted in two services → it belongs on the entity/value object.
- A `switch` over a type enum that grows every feature → missing polymorphism.
