---
name: engineering-standards
description: Core software engineering principles (SOLID, DRY, YAGNI, KISS) with detection patterns and refactoring guidance. Load when reviewing code quality, planning architecture, or identifying technical debt.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Engineering Standards

Foundational principles for high-quality software. Use this skill when:
- Reviewing code for quality issues
- Planning architectural changes
- Identifying refactoring opportunities
- Evaluating technical debt

## SOLID Principles

### Single Responsibility (SRP)
A class/module should have one reason to change.

**Detection patterns:**
- Class with 5+ public methods doing unrelated things
- Method longer than 50 lines
- Class name contains "And" or "Manager" with mixed concerns
- File imports from 10+ unrelated modules

**Refactoring:**
- Extract class for each responsibility
- Split into focused modules
- Use composition over inheritance

### Open/Closed (OCP)
Open for extension, closed for modification.

**Detection patterns:**
- Switch/case on type with frequent additions
- if/else chains checking instance types
- Modifying existing code to add new features

**Refactoring:**
- Strategy pattern for varying behaviors
- Plugin architecture for extensions
- Dependency injection for configurability

### Liskov Substitution (LSP)
Subtypes must be substitutable for their base types.

**Detection patterns:**
- Override that throws "not implemented"
- Subclass that ignores parent behavior
- Type checks before calling inherited methods

**Refactoring:**
- Favor composition over inheritance
- Extract interface for true polymorphism
- Use abstract base with required overrides

### Interface Segregation (ISP)
Clients shouldn't depend on methods they don't use.

**Detection patterns:**
- Interface with 10+ methods
- Implementing classes that stub methods as no-ops
- "Fat" interfaces with unrelated method groups

**Refactoring:**
- Split into role-specific interfaces
- Use mixins/traits for optional behaviors
- Compose multiple focused interfaces

### Dependency Inversion (DIP)
Depend on abstractions, not concretions.

**Detection patterns:**
- Direct instantiation of dependencies (`new ConcreteClass()`)
- Hard-coded database/API connections
- Test files creating production instances

**Refactoring:**
- Constructor injection
- Factory pattern for complex creation
- Interface-based dependencies

---

## DRY (Don't Repeat Yourself)

**Detection patterns:**
- Copy-pasted code blocks (3+ occurrences)
- Similar functions with minor variations
- Duplicated validation logic
- Repeated configuration values

**Refactoring:**
- Extract shared function/class
- Parameterize variations
- Create configuration constants
- Use template method pattern

**Exceptions (acceptable duplication):**
- Test code clarity (explicit over DRY)
- Cross-boundary isolation (microservices)
- Performance-critical paths

---

## YAGNI (You Aren't Gonna Need It)

**Detection patterns:**
- Unused parameters "for future use"
- Abstract classes with single implementation
- Configuration options never used
- Speculative generalization

**Guidance:**
- Build for current requirements
- Refactor when needs emerge
- Delete dead code immediately
- Prefer simple over flexible

---

## KISS (Keep It Simple, Stupid)

**Detection patterns:**
- Cyclomatic complexity > 10
- Nested callbacks/promises 4+ deep
- Generic solutions for specific problems
- Framework overkill for simple tasks

**Refactoring:**
- Flatten control flow
- Extract named functions
- Use early returns
- Choose boring technology

---

## Code Smells Quick Reference

| Smell | Symptom | Fix |
|-------|---------|-----|
| Long Method | >50 lines, multiple concerns | Extract method |
| Large Class | >500 lines, many responsibilities | Extract class |
| Feature Envy | Method uses other class more than own | Move method |
| Data Clumps | Same fields appear together | Extract object |
| Primitive Obsession | Strings/ints for domain concepts | Value objects |
| Switch Statements | Type-based switching | Polymorphism |
| Parallel Inheritance | Every subclass needs partner subclass | Merge hierarchies |
| Lazy Class | Class doing too little | Inline class |
| Speculative Generality | Unused abstraction | Remove it |
| Temporary Field | Field only set sometimes | Extract class |

---

## When to Apply

**Always apply:**
- SRP, DRY for production code
- KISS for all code

**Apply with judgment:**
- OCP when extension points are clear
- ISP when interfaces grow beyond 5 methods
- DIP at module boundaries

**Defer:**
- YAGNI violations until pattern emerges 3+ times

See [references/refactoring-catalog.md](references/refactoring-catalog.md) for detailed refactoring techniques.
