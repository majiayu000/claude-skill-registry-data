---
name: solid-principles
description: Enforce SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion) in object-oriented design. Use when writing or reviewing classes and modules.
---

# SOLID Principles Skill

You are assisting with code that must follow SOLID principles strictly.

## Principles to Enforce

### 1. Single Responsibility Principle (SRP)
- Each class should have ONE reason to change
- Each function should do ONE thing well
- Separate concerns: business logic, data access, presentation, validation
- If a class name contains "and" or "or", it likely violates SRP

**Red flags:**
- Classes with multiple unrelated methods
- Functions doing multiple operations
- Mixed concerns (e.g., validation + persistence in same method)

### 2. Open/Closed Principle (OCP)
- Open for extension, closed for modification
- Use abstract base classes and protocols for extensibility
- Prefer composition over inheritance
- New features should be added by extending, not modifying existing code

**Patterns to use:**
- Strategy pattern for varying algorithms
- Template method for varying steps
- Dependency injection for varying implementations

### 3. Liskov Substitution Principle (LSP)
- Subtypes must be substitutable for their base types
- Derived classes must not strengthen preconditions
- Derived classes must not weaken postconditions
- Avoid empty implementations or NotImplementedError in production code

**Guidelines:**
- Don't override methods to do nothing
- Maintain expected behavior contracts
- Use composition when inheritance doesn't fit naturally

### 4. Interface Segregation Principle (ISP)
- Clients should not depend on interfaces they don't use
- Create focused, cohesive protocols/abstract classes
- Many small interfaces > one large interface
- Use Python Protocols for implicit interfaces

**Implementation:**
- Split large interfaces into role-specific ones
- Use Protocol from typing module
- Avoid "fat" base classes with many optional methods

### 5. Dependency Inversion Principle (DIP)
- High-level modules should not depend on low-level modules
- Both should depend on abstractions (protocols, abstract classes)
- Abstractions should not depend on details
- Details should depend on abstractions

**Patterns:**
- Constructor injection for required dependencies
- Use abstract base classes or Protocols
- Depend on interfaces, not concrete implementations

## Code Review Checklist

When reviewing or writing code, check:
- [ ] Does each class have a single, clear responsibility?
- [ ] Can new behavior be added without modifying existing code?
- [ ] Can subclasses replace their parents without breaking functionality?
- [ ] Are interfaces focused and cohesive?
- [ ] Do modules depend on abstractions rather than concrete implementations?

## Practical Application for Admission Rules System

For the Norwegian admission rules system:
- **SRP**: Separate rule evaluation, grade calculation, quota management
- **OCP**: Make rules extensible (new admission rules without changing core engine)
- **LSP**: All rule types should be substitutable
- **ISP**: Separate interfaces for validators, calculators, reporters
- **DIP**: Depend on abstract rule interfaces, not concrete rule implementations

## Response Format

When applying SOLID principles:
1. Identify which principle(s) are relevant
2. Explain the violation if any exists
3. Provide refactored code following the principle(s)
4. Explain the benefit of the refactoring
