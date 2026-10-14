---
name: refactor
description: |
  Cross-language catalog of 62+ refactoring techniques based on Martin Fowler's "Refactoring" and
  Alexander Shvets' "Refactoring Guru". Detects the project's language automatically and provides
  idiomatic examples. Works with Java, Python, TypeScript, JavaScript, C#, Go, Kotlin, Ruby, PHP,
  Rust, Swift. Use this skill whenever the user asks to refactor code, improve code quality, eliminate
  code smells, simplify conditionals, restructure classes, improve API design, or apply any named
  refactoring technique. Also trigger when the user mentions code smells, legacy code improvement,
  clean code practices, SOLID principles, or asks "how can I improve this code". Even if the user
  just pastes code and asks for improvement suggestions, use this skill to identify applicable techniques.
  También se activa en castellano: "refactorizar", "refactorizar código",
  "mejorar este código", "malos olores del código", "olores de código",
  "código sucio", "limpiar código", "simplificar condicionales", "principios SOLID",
  "cómo mejorar este código", "código limpio", "reestructurar clase",
  "mejorar calidad del código", "técnica de refactorización", "extraer método",
  "renombrar variable", "mover método", "eliminar código duplicado",
  "reducir complejidad", "mejorar legibilidad", "reorganizar código".
  Includes general Java detection; Java examples should follow the project's Java version and idioms.
license: MIT
metadata:
  author: andresnator
  status: done
  version: "1.3.0"
---

# Refactoring Catalog (Multi-Language)

A comprehensive, technique-by-technique catalog of refactoring best practices for any language, sourced from Martin Fowler's *Refactoring: Improving the Design of Existing Code* (2nd Edition) and Alexander Shvets' *Refactoring in Java* (Refactoring Guru). Adapted for Python, TypeScript, Go, and Rust with idiomatic examples.

## Step 0: Detect Language

Before applying any technique, detect the project's stack:

| Project File | Language | Idiom Style |
|---|---|---|
| `pom.xml` / `build.gradle` | Java | OOP, Stream API |
| `pyproject.toml` / `requirements.txt` / `setup.py` | Python | Duck typing, comprehensions |
| `package.json` + `tsconfig.json` | TypeScript | Functional-OOP hybrid |
| `package.json` (no tsconfig) | JavaScript | Prototype-based, functional |
| `*.csproj` | C# | OOP, LINQ |
| `go.mod` | Go | Composition, implicit interfaces |
| `build.gradle.kts` | Kotlin | OOP + functional |
| `Gemfile` | Ruby | Duck typing, open classes |
| `composer.json` | PHP | OOP |
| `Cargo.toml` | Rust | Ownership, traits, no inheritance |
| `Package.swift` | Swift | Protocol-oriented |

If the language is **Java**, apply techniques with Java OOP, Stream API where appropriate, and the project's detected Java version constraints. Use `references/java-notes.md` for Java-specific constraints and the Java completion gate.

## Language Support Matrix

| Concept | Python | TypeScript | Go | Rust |
|---|---|---|---|---|
| Class / struct | `class` | `class` | `struct` + methods | `struct` + `impl` |
| Inheritance | `class Child(Parent)` | `extends` | Embedding (no inheritance) | Traits (no inheritance) |
| Interface / contract | `Protocol` / `ABC` | `interface` | `interface` (implicit) | `trait` |
| Encapsulation | `_private` convention | `private` keyword | Unexported (lowercase) | Private by default, `pub` |
| Polymorphism | Duck typing + ABC | Interfaces + classes | Implicit interfaces | Trait objects + generics |
| Generics | `typing.Generic[T]` | `<T>` | `[T any]` | `<T: Trait>` |
| Error handling | Exceptions | Exceptions | Error values (`error`) | `Result<T, E>` |
| Null safety | `None` / `Optional[T]` | `null` / `undefined` / `?` | `nil` (zero values) | `Option<T>` |
| Collections pipeline | Comprehensions / generators | Array methods (`.map`, `.filter`) | `for range` (no pipeline) | Iterator chain (`.filter().map()`) |
| Pattern matching | `match` (3.10+) | `switch` (no pattern matching) | `switch` (no pattern matching) | `match` (exhaustive) |
| Factory pattern | `@classmethod` / module function | Static method / function | `NewXxx()` function | `Type::new()` associated fn |
| Builder pattern | `__init__` + kwargs / dataclass | Fluent builder class | Functional options | Builder with consuming `self` |

For detailed concept-to-language mappings, see `references/language-idioms.md`.

## Core Philosophy

**Refactoring is the process of changing the internal structure of code without altering its observable behavior.** It is a disciplined technique, not a random cleanup. The golden rule is: Cover → Modify → Refactor (always have tests before you start).

## How to Use This Skill

1. **Detect** the language (Step 0 above)
2. **Diagnose first**: Identify the code smell (see `techniques/00-code-smells-diagnostic.md`)
3. **Check applicability**: See `references/language-applicability.md` for technique availability per language
4. **Select technique**: Each smell maps to one or more refactoring techniques; when several compete, use `references/selection-heuristics.md` for the ordered decision rules
5. **Read the technique file**: Each technique has multi-language examples (Python, TypeScript, Go, Rust)
6. **For Java**: Read `references/java-notes.md`, use Java OOP/Stream idioms, honor Java 8 versus Java 11+ API availability, and finish with the Java completion gate
7. **For language idiom mapping**: See `references/language-idioms.md`
8. **Apply incrementally**: Small steps, test after each change, commit frequently

## Technique Categories

The techniques are organized in 7 groups. Each technique has its own file in the `techniques/` directory.

### Group 1: Composing Methods (techniques/01-XX)
Techniques for building clean, well-structured methods. The foundation of all refactoring.
- `01-extract-method.md` — Extract a code fragment into a named function
- `02-inline-method.md` — Replace a function call with the function body
- `03-extract-variable.md` — Give a name to a complex expression
- `04-inline-variable.md` — Remove a variable that adds no clarity
- `05-replace-temp-with-query.md` — Replace temp variables with function calls
- `06-replace-method-with-method-object.md` — Turn a complex function into its own class/struct
- `07-substitute-algorithm.md` — Replace an algorithm with a clearer version

### Group 2: Moving Features (techniques/02-XX)
Techniques for placing code where it truly belongs.
- `08-move-method.md` — Move a function to where it has more cohesion
- `09-move-field.md` — Move a field to the type that uses it most
- `10-extract-class.md` — Split a type with multiple responsibilities
- `11-inline-class.md` — Merge a type that does too little
- `12-hide-delegate.md` — Encapsulate chain navigation behind a simpler interface
- `13-remove-middle-man.md` — Remove unnecessary delegation
- `14-move-statements.md` — Move statements into/out of functions, slide statements
- `15-split-loop.md` — Separate a loop that does multiple things
- `16-replace-loop-with-pipeline.md` — Use declarative pipelines instead of imperative loops
- `17-remove-dead-code.md` — Delete unused code

### Group 3: Organizing Data (techniques/03-XX)
Techniques for enriching data with behavior and protecting internal state.
- `18-encapsulate-variable.md` — Wrap data access with getters/functions
- `19-encapsulate-record.md` — Convert data structures into objects/structs
- `20-encapsulate-collection.md` — Protect collections from external mutation
- `21-replace-primitive-with-object.md` — Create domain types instead of using raw primitives
- `22-split-variable.md` — Give each purpose its own variable
- `23-rename-field.md` — Improve field names for clarity
- `24-replace-derived-variable-with-query.md` — Calculate values on demand
- `25-change-reference-to-value.md` — Make objects immutable (Value Objects)
- `26-change-value-to-reference.md` — Share a single instance across consumers
- `27-replace-type-code-with-subclasses.md` — Convert type codes to polymorphic hierarchy

### Group 4: Simplifying Conditionals (techniques/04-XX)
Techniques for taming conditional complexity.
- `28-decompose-conditional.md` — Name condition and branches
- `29-consolidate-conditional.md` — Merge related conditions
- `30-replace-nested-conditional-with-guard-clauses.md` — Early returns for special cases
- `31-replace-conditional-with-polymorphism.md` — Use polymorphism instead of switch/if-type
- `32-introduce-special-case.md` — Null Object pattern for default behavior
- `33-introduce-assertion.md` — Document invariants with executable assertions
- `34-replace-control-flag.md` — Replace boolean flags with break/return

### Group 5: Simplifying Method Calls / API Design (techniques/05-XX)
Techniques for building self-documenting interfaces.
- `35-change-function-declaration.md` — Rename functions and change parameters
- `36-introduce-parameter-object.md` — Group related parameters into an object
- `37-parameterize-function.md` — Unify similar functions with a parameter
- `38-remove-flag-argument.md` — Replace boolean params with named functions
- `39-preserve-whole-object.md` — Pass the object instead of extracted values
- `40-replace-parameter-with-query.md` — Let the function calculate what it needs
- `41-replace-query-with-parameter.md` — Pass value as param for purity/testability
- `42-remove-setting-method.md` — Make properties read-only
- `43-replace-constructor-with-factory.md` — Use factory functions for flexible creation
- `44-replace-function-with-command.md` — Encapsulate function as object
- `45-separate-query-from-modifier.md` — CQS: separate reads from writes

### Group 6: Dealing with Generalization (techniques/06-XX)
Techniques for refactoring type hierarchies and shared behavior.
- `46-pull-up-method.md` — Move duplicated functions to shared parent/trait/interface
- `47-push-down-method.md` — Move specialized functions to specific types
- `48-pull-up-constructor-body.md` — Unify constructor/initialization logic
- `49-extract-superclass.md` — Create common parent for shared behavior
- `50-extract-interface.md` — Define a contract without implementation
- `51-collapse-hierarchy.md` — Merge unnecessary hierarchy levels
- `52-form-template-method.md` — Template Method pattern
- `53-replace-subclass-with-delegate.md` — Composition over inheritance
- `54-replace-superclass-with-delegate.md` — Replace extends with has-a
- `55-replace-inheritance-with-delegation.md` — General inheritance to delegation

### Group 7: Additional Techniques (techniques/07-XX)
Cross-cutting techniques from both sources.
- `56-combine-functions-into-class.md` — Group functions that share data
- `57-combine-functions-into-transform.md` — Enrich read-only data
- `58-split-phase.md` — Separate code into processing phases
- `59-introduce-foreign-method.md` — Extend third-party types you can't modify
- `60-introduce-local-extension.md` — Wrapper or subclass for library extension
- `61-replace-error-code-with-exception.md` — Modernize error handling
- `62-replace-exception-with-test.md` — Don't use exceptions for control flow

## Diagnostic Guide

Start with `techniques/00-code-smells-diagnostic.md` to identify which techniques apply to your code. The diagnostic maps 24 code smells to their recommended refactoring techniques.

## Applying the Skill

When given code to refactor:

1. Detect the language (Step 0)
2. Read `techniques/00-code-smells-diagnostic.md` to identify the smells present
3. For each identified smell, read the corresponding technique file(s)
4. Check `references/language-applicability.md` — if the technique doesn't apply to the target language, the table shows the alternative
5. Apply techniques in small steps, always testing between changes
6. Provide idiomatic examples for the detected language
7. Explain WHY each refactoring improves the code, not just HOW to do it
8. For Java, report the `references/java-notes.md` Java completion gate verdict
9. For language-specific idiom translations, consult `references/language-idioms.md`

## Key Principles

These principles underpin every technique in the catalog:

1. **Names matter more than length** — a well-named 1-line function is better than an inline expression
2. **Small steps** — extract small fragments, test, commit. Never batch multiple changes
3. **Intention over implementation** — code should communicate WHAT, not HOW
4. **Data and logic that change together should live together** — cohesion is king
5. **Prefer composition over inheritance** — delegation is more flexible than extends
6. **Immutability is a powerful preservative** — immutable data is easier to reason about
7. **CQS (Command-Query Separation)** — a function either returns a value or modifies state, never both

## Reference Files

| File | Content |
|---|---|
| `references/language-idioms.md` | Refactoring concept → {Python, TypeScript, Go, Rust} equivalents |
| `references/language-applicability.md` | 62-technique × language applicability matrix with alternatives |
| `references/java-notes.md` | Java-specific constraints, Java 8 vs 11+ notes, and the Java completion gate |
| `references/selection-heuristics.md` | Ordered decision rules when several techniques compete: conditionals tree, smell directionality, falsifiable micro-tests, inheritance→delegation triggers |
| `references/technique-to-pattern.md` | Which refactoring techniques land on which GoF pattern (Kerievsky bridge) |
