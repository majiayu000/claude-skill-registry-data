---
name: coding-standard
description: Expert in modern code design standards including SOLID principles, Clean Code patterns (KISS, YAGNI, DRY, TDA), design patterns, and pragmatic software design. **ALWAYS use when designing ANY classes/modules, implementing features, fixing bugs, refactoring code, or writing functions. ** Use proactively to ensure proper design, separation of concerns, simplicity, and maintainability. Triggers - "create class", "design module", "implement feature", "refactor code", "fix bug", "is this too complex", "apply SOLID", "keep it simple", "avoid over-engineering", writing any code.
---

# Coding Standard

Expert guidance for writing well-designed, simple, maintainable code following modern software engineering practices. All rules are **mandatory** when there is valid context for their application.

## Core Philosophy

1. **"Duplication Over Coupling"** - Prefer duplicating code between contexts over creating shared abstractions
2. **"Start Ugly, Refactor Later"** - Don't create abstractions until you have 2 or more real use cases
3. **KISS Over DRY** - Simplicity beats premature abstraction every time
4. **YAGNI Always** - Never add features or abstractions "just in case"

## When to Engage

Proactively assist when:
- Designing new classes or modules
- Implementing features without over-abstraction
- Refactoring to remove unnecessary complexity
- Fixing bugs
- Code reviews focusing on simplicity
- Detecting and preventing over-engineering
- Choosing duplication over coupling

## Rule Categories

### SOLID Principles (Object-Oriented Design)

1. **Single Responsibility Principle (SRP)** - One reason to change per class/module
   - When: Designing any class or module
   - See: [references/rules/solid-srp-rule.md](references/rules/solid-srp-rule.md)
   - Example: [references/pseudo-examples/solid-srp-example.md](references/pseudo-examples/solid-srp-example.md)

2. **Open/Closed Principle (OCP)** - Open for extension, closed for modification
   - When: Building extensible systems, adding new features
   - See: [references/rules/solid-ocp-rule.md](references/rules/solid-ocp-rule.md)
   - Example: [references/pseudo-examples/solid-ocp-example.md](references/pseudo-examples/solid-ocp-example.md)

3. **Liskov Substitution Principle (LSP)** - Subtypes must be substitutable for base types
   - When: Using inheritance or polymorphism
   - See: [references/rules/solid-lsp-rule.md](references/rules/solid-lsp-rule.md)
   - Example: [references/pseudo-examples/solid-lsp-example.md](references/pseudo-examples/solid-lsp-example.md)

4. **Interface Segregation Principle (ISP)** - Small, focused interfaces over large ones
   - When: Designing interfaces or abstract classes
   - See: [references/rules/solid-isp-rule.md](references/rules/solid-isp-rule.md)
   - Example: [references/pseudo-examples/solid-isp-example.md](references/pseudo-examples/solid-isp-example.md)

5. **Dependency Inversion Principle (DIP)** - Depend on abstractions, not concretions
   - When: Designing class dependencies, improving testability
   - See: [references/rules/solid-dip-rule.md](references/rules/solid-dip-rule.md)
   - Example: [references/pseudo-examples/solid-dip-example.md](references/pseudo-examples/solid-dip-example.md)

### Clean Code Principles (Simplicity & Pragmatism)

6. **KISS - Keep It Simple, Stupid** - Simplicity is the ultimate sophistication
   - When: Simple requirements, straightforward logic, avoiding over-engineering
   - See: [references/rules/kiss-rule.md](references/rules/kiss-rule.md)
   - Example: [references/pseudo-examples/kiss-example.md](references/pseudo-examples/kiss-example.md)

7. **YAGNI - You Aren't Gonna Need It** - Build only what you need right now
   - When: Feature not in current requirements, "we might need this later" scenarios
   - See: [references/rules/yagni-rule.md](references/rules/yagni-rule.md)
   - Example: [references/pseudo-examples/yagni-example.md](references/pseudo-examples/yagni-example.md)

8. **DRY - Don't Repeat Yourself** - Apply abstraction after Rule of Three
   - When: Same code appears 3+ times, logic is truly identical
   - See: [references/rules/dry-rule.md](references/rules/dry-rule.md)
   - Example: [references/pseudo-examples/dry-example.md](references/pseudo-examples/dry-example.md)

9. **TDA - Tell, Don't Ask** - Tell objects what to do, don't ask for data
   - When: Object has data and related business logic, encapsulation needed
   - See: [references/rules/tda-rule.md](references/rules/tda-rule.md)
   - Example: [references/pseudo-examples/tda-example.md](references/pseudo-examples/tda-example.md)

### Design Patterns

10. **Singleton Pattern** - Ensure a class has only one instance
    - When: Database connections, configuration managers, global state
    - See: [references/rules/singleton-pattern-rule.md](references/rules/singleton-pattern-rule.md)
    - Example: [references/pseudo-examples/singleton-pattern-example.md](references/pseudo-examples/singleton-pattern-example.md)

11. **Factory Pattern** - Create objects without specifying exact classes
    - When: Creating objects based on runtime conditions
    - See: [references/rules/factory-pattern-rule.md](references/rules/factory-pattern-rule.md)
    - Example: [references/pseudo-examples/factory-pattern-example.md](references/pseudo-examples/factory-pattern-example.md)

12. **Observer Pattern** - Define one-to-many dependency for event notification
    - When: Event systems, pub/sub, reactive programming
    - See: [references/rules/observer-pattern-rule.md](references/rules/observer-pattern-rule.md)
    - Example: [references/pseudo-examples/observer-pattern-example.md](references/pseudo-examples/observer-pattern-example.md)

13. **Strategy Pattern** - Define family of algorithms, make them interchangeable
    - When: Algorithms can be swapped at runtime
    - See: [references/rules/strategy-pattern-rule.md](references/rules/strategy-pattern-rule.md)
    - Example: [references/pseudo-examples/strategy-pattern-example.md](references/pseudo-examples/strategy-pattern-example.md)

14. **Decorator Pattern** - Add responsibilities to objects dynamically
    - When: Adding features dynamically without inheritance
    - See: [references/rules/decorator-pattern-rule.md](references/rules/decorator-pattern-rule.md)
    - Example: [references/pseudo-examples/decorator-pattern-example.md](references/pseudo-examples/decorator-pattern-example.md)

15. **Repository Pattern** - Abstract data access logic
    - When: Separating data access from business logic
    - See: [references/rules/repository-pattern-rule.md](references/rules/repository-pattern-rule.md)
    - Example: [references/pseudo-examples/repository-pattern-example.md](references/pseudo-examples/repository-pattern-example.md)

16. **Dependency Injection** - Invert control by injecting dependencies
    - When: Improving testability, decoupling components
    - See: [references/rules/dependency-injection-rule.md](references/rules/dependency-injection-rule.md)
    - Example: [references/pseudo-examples/dependency-injection-example.md](references/pseudo-examples/dependency-injection-example.md)

### Function & Code Design Practices

17. **Pure Functions** - Prefer pure (stateless) functions
    - When: All languages, designing functions
    - See: [references/rules/pure-functions-rule.md](references/rules/pure-functions-rule.md)
    - Example: [references/pseudo-examples/pure-functions-example.md](references/pseudo-examples/pure-functions-example.md)

18. **Immutability** - Prefer immutable data structures
    - When: All languages, prevents unintended side effects
    - See: [references/rules/immutability-rule.md](references/rules/immutability-rule.md)
    - Example: [references/pseudo-examples/immutability-example.md](references/pseudo-examples/immutability-example.md)

19. **Single Responsibility Functions** - Keep functions short and focused
    - When: All languages, writing any function
    - See: [references/rules/single-responsibility-functions-rule.md](references/rules/single-responsibility-functions-rule.md)
    - Example: [references/pseudo-examples/single-responsibility-functions-example.md](references/pseudo-examples/single-responsibility-functions-example.md)

20. **Early Returns** - Use early returns to reduce nesting
    - When: All languages, handling multiple conditions
    - See: [references/rules/early-returns-rule.md](references/rules/early-returns-rule.md)
    - Example: [references/pseudo-examples/early-returns-example.md](references/pseudo-examples/early-returns-example.md)

21. **Composition Over Inheritance** - Prefer composition
    - When: All languages, designing class relationships
    - See: [references/rules/composition-over-inheritance-rule.md](references/rules/composition-over-inheritance-rule.md)
    - Example: [references/pseudo-examples/composition-over-inheritance-example.md](references/pseudo-examples/composition-over-inheritance-example.md)

22. **Loop Control Flow** - Use appropriate loops with break/continue
    - When: All languages, iterating collections
    - See: [references/rules/loop-control-flow-rule.md](references/rules/loop-control-flow-rule.md)
    - Example: [references/pseudo-examples/loop-control-flow-example.md](references/pseudo-examples/loop-control-flow-example.md)

23. **Avoid Global Variables** - Minimize global state
    - When: All languages, managing application state
    - See: [references/rules/avoid-global-variables-rule.md](references/rules/avoid-global-variables-rule.md)
    - Example: [references/pseudo-examples/avoid-global-variables-example.md](references/pseudo-examples/avoid-global-variables-example.md)

24. **Class Design** - Separate data and methods appropriately
    - When: All languages, designing classes
    - See: [references/rules/class-design-rule.md](references/rules/class-design-rule.md)
    - Example: [references/pseudo-examples/class-design-example.md](references/pseudo-examples/class-design-example.md)

25. **Avoid Side Effects** - Minimize side effects in functions
    - When: All languages, writing functions
    - See: [references/rules/avoid-side-effects-rule.md](references/rules/avoid-side-effects-rule.md)
    - Example: [references/pseudo-examples/avoid-side-effects-example.md](references/pseudo-examples/avoid-side-effects-example.md)

26. **Avoid Getters/Setters** - Prefer direct access or immutability
    - When: All languages, can lead to unexpected side effects
    - See: [references/rules/avoid-getters-setters-rule.md](references/rules/avoid-getters-setters-rule.md)
    - Example: [references/pseudo-examples/avoid-getters-setters-example.md](references/pseudo-examples/avoid-getters-setters-example.md)

27. **Avoid Module-Level Side Effects** - Wrap in lazy initialization
    - When: All languages, module initialization
    - See: [references/rules/avoid-module-level-side-effects-rule.md](references/rules/avoid-module-level-side-effects-rule.md)
    - Example: [references/pseudo-examples/avoid-module-side-effects-example.md](references/pseudo-examples/avoid-module-side-effects-example.md)

28. **Keep Functions Small** - Target < 20 lines per function
    - When: All languages, writing any function
    - See: [references/rules/keep-functions-small-rule.md](references/rules/keep-functions-small-rule.md)
    - Example: [references/pseudo-examples/keep-functions-small-example.md](references/pseudo-examples/keep-functions-small-example.md)

29. **Meaningful Names** - Use self-documenting names over comments
    - When: All languages, naming variables, functions, classes
    - See: [references/rules/meaningful-names-rule.md](references/rules/meaningful-names-rule.md)
    - Example: [references/pseudo-examples/meaningful-names-example.md](references/pseudo-examples/meaningful-names-example.md)

30. **Single Level of Abstraction** - Keep functions at one abstraction level
    - When: All languages, writing functions
    - See: [references/rules/single-level-abstraction-rule.md](references/rules/single-level-abstraction-rule.md)
    - Example: [references/pseudo-examples/single-level-abstraction-example.md](references/pseudo-examples/single-level-abstraction-example.md)

## Quick Reference

**When principles conflict:**
- KISS vs DRY: Prefer KISS, apply DRY only after Rule of Three
- YAGNI vs Future-Proofing: Start with YAGNI, refactor when needed
- SOLID vs KISS: Apply SOLID when complexity is justified
- TDA vs Simple Data: Use TDA for business logic, simple structs for DTOs

**Apply principles when:**
- Complex business logic that will evolve
- Multiple implementations needed
- Team projects requiring clear boundaries
- Testability is critical
- Long-term maintainability is a priority

**Don't over-apply when:**
- Simple CRUD operations with stable requirements
- Small utilities (< 100 lines)
- Prototypes or POCs
- Performance-critical code where abstraction adds overhead
- When it adds complexity without clear benefit

## Usage Instructions for Agentic Tools

**IMPORTANT - Context and Token Management:**

This SKILL.md file contains **summary information** for all 30 coding standards. Use this summary to:
- Understand which rules apply to your current task
- Know when to apply each rule
- Get quick guidance without reading detailed references

**Do NOT preemptively load references.** Only read detailed rule files and examples when:
1. **Actively implementing** a specific pattern or rule
2. **Need clarification** on how to apply a rule
3. **Reviewing/debugging** code that uses a specific pattern

**Example workflow:**
- ✅ GOOD: "I'm implementing a notification system" → Check SKILL.md → See Observer Pattern applies → Read observer-pattern-rule.md → Implement
- ❌ BAD: "I'm implementing a notification system" → Load all 7 design pattern rules "just in case"

**When to read what:**
- **SKILL.md only**: General guidance, rule selection, understanding when to apply
- **references/rules/{rule}.md**: Detailed implementation guidance for a specific rule you're applying
- **references/pseudo-examples/{rule}-example.md**: Pseudo-code examples when you need to see concrete implementation

**Token efficiency**: The summary in SKILL.md is designed to be sufficient for most decisions. Only load references when you actually need implementation details.

---

## Quick Usage Steps

When implementing any code:
1. Review relevant rule categories in SKILL.md based on the task
2. Identify which specific rules apply to your current implementation
3. **Only then** read specific rule files from references/rules/ for those rules
4. **Only if needed** consult examples from references/examples/ for clarification
5. Apply rules as mandatory requirements with valid context
6. Balance principles - don't over-engineer simple solutions
