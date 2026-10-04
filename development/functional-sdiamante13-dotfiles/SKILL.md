---
name: functional
description: Refactor Swift code toward declarative functional programming with immutability, value types, pure functions, transformations, and closure-based APIs. Use when asked for functional refactoring or `/refactor:functional`.
metadata:
  legacy-name: refactor:functional
---

Refactor this Swift codebase to follow functional programming principles:

Replace Mutability with Immutability

Convert var to let wherever possible
Replace mutable collections with immutable transformations
Use value types (structs/enums) instead of reference types (classes) where appropriate
Eliminate property mutations in favor of creating new instances


Extract Pure Functions

Identify functions with side effects and refactor them to be pure
Move I/O operations (network calls, file access, database queries) to the edges of the system
Replace stateful methods with functions that take input and return output
Ensure functions don't modify external state or rely on mutable global variables


Use Higher-Order Functions

Replace for-loops with map, filter, reduce, compactMap, flatMap
Convert imperative conditional logic to functional chains
Use function composition to build complex operations from simple ones
Leverage lazy sequences for performance where appropriate


Functional Error Handling

Replace try-catch blocks with Result types where suitable
Use Optional chaining and nil-coalescing operators
Implement functional error propagation with map and flatMap on Result
Avoid force unwrapping (!); use guard let, if let, or functional alternatives


Eliminate Shared Mutable State

Replace singletons with dependency injection of immutable services
Convert stateful classes to stateless functions or immutable structs
Use actors or other concurrency-safe patterns when mutation is necessary
Pass data explicitly rather than relying on shared state


Apply Functional Patterns

Implement custom operators for common transformations
Use currying for partial function application
Create small, composable functions following the single responsibility principle
Model domain concepts as algebraic data types (enums with associated values)


Specific Transformations

Convert delegate patterns to closure-based APIs
Replace inheritance hierarchies with protocol composition
Transform imperative algorithms to recursive or fold-based implementations
Use KeyPaths for type-safe property access



Example transformation patterns to look for:

Loops that build arrays → map/filter/reduce
Nested if-else → pattern matching with switch
Mutable accumulator patterns → fold/reduce
Callback hell → flatMap chains or async/await
Stateful iteration → sequence/generator patterns

Maintain Swift idioms while applying functional principles. The goal is readable, maintainable code that leverages Swift's functional capabilities without sacrificing clarity.
