---
name: composable-architecture
description: Apply functional and compositional architecture patterns when designing systems, modules, and components. Use when creating architecture definitions, designing system boundaries, defining interfaces, or building modular systems.
---

# Composable Architecture Patterns

## Core Principles

**Functional Core, Imperative Shell**
- Pure core: Business logic as pure functions (no side effects)
- Imperative shell: I/O pushed to system edges
- Unit test core, integration test shell

**Composition Over Inheritance**
- Build from small, composable functions
- Prefer data transformation over stateful mutation
- Use pipelines and modifier chaining

## Hexagonal Architecture (Ports & Adapters)

```
[External] → [Adapter] → [Port] → [Core] → [Port] → [Adapter] → [External]
```

- **Core**: Pure business logic, no external dependencies
- **Ports**: Interfaces defining capabilities
- **Adapters**: Implementations connecting to external systems

## C4 Model Hierarchy

1. **System Context**: Boundaries and external actors
2. **Module**: Major architectural components (map 1:1 to directories)
3. **Component**: Internal module structure
4. **Code**: Implementation details

## Design Process

**New system:**
1. Define boundaries (inside vs outside)
2. Identify ports (capabilities needed/provided)
3. Design pure core (business rules as functions)
4. Create adapters (connect to external world)

**Refactoring:**
1. Extract pure functions from mixed logic
2. Define interfaces for dependencies
3. Move I/O to edges
4. Replace inheritance with composition

## Anti-patterns

- Mixing business logic with I/O
- Circular dependencies between modules
- Using inheritance for code reuse
- Coupling core logic to specific technologies
- "God" modules with multiple responsibilities

**Remember**: Build from simple, pure, testable pieces. Keep complex logic in pure core, push messy reality to edges.
