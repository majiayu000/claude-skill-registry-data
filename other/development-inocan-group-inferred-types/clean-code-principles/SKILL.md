---
name: clean-code-principles
description: Detects violations of Clean Code principles and suggests refactorings. Use when reviewing code quality, improving readability, or refactoring methods, classes, and modules.
---

# Clean Code Refactoring Detection

Identify opportunities to apply Clean Code principles based on Robert C. Martin's guidelines.

---

## Naming

### Meaningful Names

**Detect**: Single-letter variables, abbreviations, `temp`/`data`/`info` suffixes  
**Refactor**: Intention-revealing names that explain purpose  
**Cookbook**: [meaningful-names.md](./cookbook/meaningful-names.md)

### Pronounceable Names

**Detect**: Unpronounceable abbreviations (`genymdhms`, `modymdhms`)  
**Refactor**: Names that can be discussed verbally  
**Cookbook**: [meaningful-names.md](./cookbook/meaningful-names.md)

### Searchable Names

**Detect**: Magic numbers, single-letter constants  
**Refactor**: Named constants with clear purpose  
**Cookbook**: [meaningful-names.md](./cookbook/meaningful-names.md)

---

## Functions

### Small Functions

**Detect**: Methods longer than 20 lines, multiple levels of abstraction  
**Refactor**: Extract smaller, single-purpose functions  
**Cookbook**: [small-functions.md](./cookbook/small-functions.md)

### Single Responsibility

**Detect**: Functions doing multiple unrelated tasks  
**Refactor**: One function, one responsibility, one level of abstraction  
**Cookbook**: [small-functions.md](./cookbook/small-functions.md)

### Few Arguments

**Detect**: Functions with more than 3 arguments  
**Refactor**: Parameter objects, builder pattern, method extraction  
**Cookbook**: [function-arguments.md](./cookbook/function-arguments.md)

### No Side Effects

**Detect**: Functions that modify global state or input parameters  
**Refactor**: Pure functions, explicit state changes  
**Cookbook**: [side-effects.md](./cookbook/side-effects.md)

### Command Query Separation

**Detect**: Functions that both change state AND return values  
**Refactor**: Separate commands (void) from queries (return value)  
**Cookbook**: [command-query-separation.md](./cookbook/command-query-separation.md)

---

## Comments

### Self-Documenting Code

**Detect**: Comments explaining "what" instead of code explaining itself  
**Refactor**: Rename variables and extract methods to make intent clear  
**Cookbook**: [comments.md](./cookbook/comments.md)

### Useful Comments

**Detect**: Commented-out code, redundant comments, changelog in code  
**Refactor**: Legal/license comments, intent explanation, TODO with tickets  
**Cookbook**: [comments.md](./cookbook/comments.md)

---

## Error Handling

### Exceptions Over Error Codes

**Detect**: Methods returning error codes or status flags  
**Refactor**: Throw specific, descriptive exceptions  
**Cookbook**: [error-handling.md](./cookbook/error-handling.md)

### Unchecked Exceptions

**Detect**: Checked exceptions creating coupling  
**Refactor**: Runtime exceptions with meaningful messages  
**Cookbook**: [error-handling.md](./cookbook/error-handling.md)

### Don't Return Null

**Detect**: Methods returning `null` for error/empty cases  
**Refactor**: `Optional<T>`, empty collections, Null Object pattern  
**Cookbook**: [null-handling.md](./cookbook/null-handling.md)

### Don't Pass Null

**Detect**: `null` passed as method argument  
**Refactor**: Overloaded methods, default values, Optional parameters  
**Cookbook**: [null-handling.md](./cookbook/null-handling.md)

---

## Classes

### Single Responsibility (SRP)

**Detect**: Classes with multiple reasons to change, mixed concerns  
**Refactor**: Separate classes for distinct responsibilities  
**Cookbook**: [single-responsibility.md](./cookbook/single-responsibility.md)

### Cohesion

**Detect**: Methods not using instance variables, unrelated fields  
**Refactor**: Extract related fields/methods into new classes  
**Cookbook**: [cohesion.md](./cookbook/cohesion.md)

### Small Classes

**Detect**: Classes with 200+ lines or 10+ methods  
**Refactor**: Identify hidden responsibilities, extract collaborators  
**Cookbook**: [small-classes.md](./cookbook/small-classes.md)

---

## Code Smells

### Long Method

**Detect**: Methods exceeding 20 lines  
**Refactor**: Extract Method until each does one thing  
**Cookbook**: [long-method.md](./cookbook/long-method.md)

### Primitive Obsession

**Detect**: Strings for emails/phone/money, parallel arrays  
**Refactor**: Value objects, domain-specific types  
**Cookbook**: [primitive-obsession.md](./cookbook/primitive-obsession.md)

### Feature Envy

**Detect**: Method uses more data from other class than its own  
**Refactor**: Move method to the class it envies  
**Cookbook**: [feature-envy.md](./cookbook/feature-envy.md)

### Data Clumps

**Detect**: Same group of parameters passed together repeatedly  
**Refactor**: Parameter object or extract class  
**Cookbook**: [data-clumps.md](./cookbook/data-clumps.md)

### Divergent Change

**Detect**: Class changes for unrelated reasons  
**Refactor**: Split class by responsibility  
**Cookbook**: [divergent-change.md](./cookbook/divergent-change.md)

### Shotgun Surgery

**Detect**: One change requires many small edits across classes  
**Refactor**: Consolidate related logic into single class  
**Cookbook**: [shotgun-surgery.md](./cookbook/shotgun-surgery.md)

---

## Quick Reference Table

| Principle             | Detection Signal                   | Clean Code Solution               |
| --------------------- | ---------------------------------- | --------------------------------- |
| Meaningful Names      | Single-letter vars, abbreviations  | Intention-revealing names         |
| Small Functions       | Methods > 20 lines                 | Extract, one level of abstraction |
| Few Arguments         | > 3 parameters                     | Parameter objects, builder        |
| No Side Effects       | Modifies global/input state        | Pure functions                    |
| Command Query Sep.    | Function changes state AND returns | Separate commands from queries    |
| Self-Documenting      | Comments explain "what"            | Rename, extract methods           |
| Exceptions            | Error codes, status flags          | Specific exceptions               |
| Don't Return Null     | Null for errors/empty              | Optional, empty collections       |
| Single Responsibility | Multiple reasons to change         | Separate classes                  |
| Cohesion              | Methods don't use instance vars    | Extract new classes               |
| Long Method           | > 20 lines                         | Extract Method                    |
| Primitive Obsession   | Strings for domain types           | Value objects                     |
| Feature Envy          | Uses external class data           | Move method                       |
| Data Clumps           | Repeated parameter groups          | Parameter object                  |

---

## Boy Scout Rule

> Leave the code cleaner than you found it.

Apply opportunistic refactoring:

1. Fix one naming issue
2. Extract one long method
3. Remove one piece of dead code
4. Add one missing null check

---

## Cookbook Index

Clean Code recipes with practical examples:

**Naming**: [Meaningful Names](./cookbook/meaningful-names.md)

**Functions**: [Small Functions](./cookbook/small-functions.md) · [Function Arguments](./cookbook/function-arguments.md) · [Side Effects](./cookbook/side-effects.md) · [Command Query Separation](./cookbook/command-query-separation.md)

**Comments**: [Comments](./cookbook/comments.md)

**Error Handling**: [Error Handling](./cookbook/error-handling.md) · [Null Handling](./cookbook/null-handling.md)

**Classes**: [Single Responsibility](./cookbook/single-responsibility.md) · [Cohesion](./cookbook/cohesion.md) · [Small Classes](./cookbook/small-classes.md)

**Code Smells**: [Long Method](./cookbook/long-method.md) · [Primitive Obsession](./cookbook/primitive-obsession.md) · [Feature Envy](./cookbook/feature-envy.md) · [Data Clumps](./cookbook/data-clumps.md) · [Divergent Change](./cookbook/divergent-change.md) · [Shotgun Surgery](./cookbook/shotgun-surgery.md)
