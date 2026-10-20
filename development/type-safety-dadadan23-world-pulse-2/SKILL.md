---
name: "type-safety"
description: 'Apply type safety patterns including nullable types, validation, static analysis, and strong typing. Use when adding type annotations, implementing nullable reference types, validating inputs with value objects, configuring static analysis tools, or designing type-safe APIs.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Type Safety

> **Purpose**: Use type systems to catch errors at compile/analysis time rather than runtime. 
> **Goal**: Prevent null errors, type mismatches, and invalid states. 
> **Note**: For implementation, see [C# Development](../csharp/SKILL.md) or [Python Development](../python/SKILL.md).

---

## When to Use This Skill

- Adding type annotations to existing code
- Implementing nullable reference types
- Building type-safe APIs with value objects
- Configuring static analysis tools
- Designing strongly-typed data transfer objects

## Prerequisites

- Language with type system support

## Why Type Safety Matters

```
Runtime Error (Bad):
 function getUser(id):
 return database.find(id) # What type? Nullable?
 
 user = getUser(123)
 print(user.email) # NullReferenceException at runtime

Type-Safe (Good):
 function getUser(id: int) -> User | null:
 return database.find(id)
 
 user = getUser(123)
 if user != null:
 print(user.email) # [PASS] Compiler ensures null check
```

---

## Nullable Types

### Concept

Explicitly declare whether a value can be null/None.

```
Type Declarations:
 
 User - Never null (must have value)
 User? - Nullable (might be null)
 
Benefits:
 - Compiler/analyzer warns about potential null access
 - Forces explicit null handling
 - Self-documenting code
```

### Null Handling Patterns

```
Pattern 1: Null Check
 user = findUser(id)
 if user != null:
 return user.email
 else:
 throw NotFoundException()

Pattern 2: Default Value
 user = findUser(id)
 return user?.email ?? "unknown@example.com"

Pattern 3: Early Return
 user = findUser(id)
 if user == null:
 return NotFound()
 
 # user is non-null from here
 return Ok(user)

Pattern 4: Required (Fail Fast)
 user = findUser(id) ?? throw NotFoundException(id)
 return user.email # Guaranteed non-null
```

---

## Type Annotations

### Function Signatures

```
Fully Typed Function:

 function calculateTotal(
 items: List<OrderItem>, # Input type
 discountPercent: decimal, # Primitive type
 taxRate: decimal? # Nullable parameter
 ) -> decimal: # Return type
 ...

Benefits:
 - Clear contract
 - IDE autocomplete
 - Compile-time validation
 - Documentation
```

### Data Types

```
Primitive Types:
 int, float, decimal, string, bool, datetime

Collection Types:
 List<T> # Ordered, duplicates allowed
 Set<T> # Unique values
 Map<K, V> # Key-value pairs
 Array<T> # Fixed size

Custom Types:
 User # Class/struct
 OrderStatus # Enum
 Result<T, E> # Union/discriminated type
```

---

## Best Practices

| Practice | Description |
|----------|-------------|
| **Annotate everything** | Types on all function parameters and returns |
| **Enable strict mode** | Turn on all null safety and type checks |
| **Avoid `any`/`object`** | Use specific types instead of escape hatches |
| **Validate at boundaries** | Check external input, trust internal data |
| **Use enums** | Replace magic strings/numbers with enums |
| **Prefer immutability** | Use readonly/final where possible |
| **Run analyzers in CI** | Fail builds on type errors |
| **Document nullable intent** | Explicit `?` for nullable, no `?` for required |

---

## Type Safety Tools

| Language | Tools |
|----------|-------|
| **C#** | Roslyn analyzers, nullable reference types, StyleCop |
| **Python** | mypy, pyright, pydantic |
| **TypeScript** | tsc strict mode, ESLint |
| **Java** | SpotBugs, Error Prone, NullAway |
| **Go** | go vet, staticcheck |

---

**See Also**: [Testing](../testing/SKILL.md) - [C# Development](../csharp/SKILL.md) - [Python Development](../python/SKILL.md)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Too many any/Object types | Replace with specific types or generics, enable strict mode incrementally |
| Generic type inference fails | Add explicit type parameters at call site, check constraint compatibility |
| Static analysis too noisy | Configure severity levels, suppress false positives with inline comments, fix incrementally |

## References

- [Value Objects Enums Validation](references/value-objects-enums-validation.md)
- [Static Analysis Generics](references/static-analysis-generics.md)