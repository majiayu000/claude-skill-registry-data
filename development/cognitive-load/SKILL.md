---
name: Cognitive Load
description: This skill should be used when the user asks to "implement", "build", "create", "add feature", "develop", "design", "architect", "plan", "structure", "refactor", "improve", "optimize", "review", "fix", "solve", "handle", "debug", or discusses implementation strategies. Apply cognitive load principles to ALL development work as a cornerstone principle.
version: 1.0.0
---

# Cognitive Load: The Cornerstone Code Quality Philosophy

## Core Principle

**People can hold ~4 chunks in working memory at once.** Beyond this, mental burden increases exponentially. The goal is to minimize *extraneous* cognitive load - the load created by how information is presented, not the inherent task difficulty.

There are two types of cognitive load:
- **Intrinsic**: The inherent complexity of the task - cannot be reduced
- **Extraneous**: Created by code structure, naming, patterns - CAN and SHOULD be reduced

Great code is boring code. If newcomers take >40 minutes to understand a piece of code, it needs improvement.

## The 13 Principles

### 1. Extract Complex Conditionals

Multiple conditions in a single statement force simultaneous mental tracking.

```go
// High load - track all conditions at once
if val > someConstant && (condition2 || condition3) && (condition4 && !condition5) { }

// Low load - named, sequential concepts
isValid := val > someConstant
isAllowed := condition2 || condition3
isSecure := condition4 && !condition5
if isValid && isAllowed && isSecure { }
```

**Rule**: If a condition has more than 2-3 parts, extract to named variables.

### 2. Use Early Returns

Nested conditionals require tracking multiple preconditions simultaneously.

```go
// High load - nested context tracking
if isValid {
    if isSecure {
        if hasPermission {
            doStuff()
        }
    }
}

// Low load - linear thinking, guard clauses
if !isValid { return }
if !isSecure { return }
if !hasPermission { return }
doStuff()
```

**Rule**: Flatten nested conditionals with early returns. Focus on the happy path.

### 3. Prefer Composition Over Inheritance

Deep inheritance requires jumping between multiple files to understand behavior.

`AdminController → UserController → GuestController → BaseController` = exponential cognitive load.

**Rule**: Compose behaviors from small, focused components instead of inheriting from base classes.

### 4. Deep Modules Over Shallow Modules

- **Deep modules**: Simple interface, complex implementation (good)
- **Shallow modules**: Complex interface, small implementation (bad)

Unix I/O has 5 basic calls hiding hundreds of thousands of lines. That's a deep module.

**Anti-pattern**: 80 tiny classes with single methods each = impossible to understand. The cognitive load is in remembering ALL modules AND their interactions.

**Rule**: Don't fragment code into many small pieces. Interfaces more complex than implementations are a smell.

### 5. Single Responsibility (Correctly)

Wrong: "One method per responsibility" = shallow module explosion.

Correct: A module should be responsible to **one stakeholder**. If changes cause two different stakeholders to complain, the principle is violated.

**Rule**: SRP is about *who* might request changes, not counting methods.

### 6. Avoid Microservice Proliferation

5 developers × 17 microservices = distributed monolith disaster.

**Rule**: Start with a modular monolith. Only extract services when team scaling demands it. Apply deep/shallow thinking at architecture scale.

### 7. Limit Language Features

Every language feature creates a decision point. Readers must recreate *why* you chose this approach.

C++ developers must understand historical baggage, multiple initialization syntaxes, and competing paradigms.

**Rule**: Use orthogonal, minimal feature sets. Prefer boring, obvious patterns.

### 8. Self-Describing Status Codes

Numeric codes require mental mapping: `401` = expired JWT, `403` = insufficient access, `418` = banned user.

```json
// Instead of numeric codes in headers
{ "code": "jwt_has_expired" }
```

**Rule**: Return self-describing codes. Prefer "login" over "authentication", "permissions" over "authorization".

### 9. Avoid DRY Abuse

Over-eliminating repetition creates tight coupling between unrelated components.

"A little copying is better than a little dependency." — Rob Pike

**Rule**: Don't extract common functionality based on perceived similarity. Dependencies mean debugging 10+ stack trace levels.

### 10. Write Framework-Agnostic Code

"Magic" in frameworks forces learning framework internals before contributing business logic.

**Anti-pattern**: Business logic residing inside framework decorators/annotations.

**Rule**: Position frameworks outside core logic. New contributors should add value on day one without framework expertise.

### 11. Minimize Abstraction Layers

Layered architecture (hexagonal, onion) adds indirection without reducing cognitive load.

Real consequences:
- Doubled project complexity
- Glue code proliferation
- Changes requiring modifications across multiple layers
- Exponential debug traces

**Rule**: Add layers only when justified by practical extension needs, not architectural aesthetics.

### 12. DDD is Problem Space, Not Folder Structure

"We write code in DDD" = subjective interpretations per team = battleground for debate.

DDD addresses ubiquitous language and domain boundaries. It's not about repositories, aggregates, or folder naming.

**Rule**: Focus on understanding the problem domain, not enforcing structural patterns.

### 13. Familiarity ≠ Simplicity

Code can feel familiar (internalized mental models) without being simple.

Original authors add complexity incrementally (unnoticed). Newcomers encounter the entire mess at once.

**Detection**: If new developers experience sustained confusion (>40 minutes), the code needs improvement.

**Rule**: Measure code quality by newcomer onboarding time, not expert familiarity.

## Decision Framework

Before writing or reviewing code, ask:

1. **Can a newcomer understand this in <40 minutes?**
2. **How many things must I hold in memory simultaneously?**
3. **Am I adding extraneous load or reducing it?**

## When Reviewing/Generating Code

1. **Flag complex conditionals** - suggest extraction to named variables
2. **Identify deep nesting** - suggest early returns
3. **Spot shallow module proliferation** - suggest consolidation
4. **Check for framework coupling** - suggest separation of business logic
5. **Look for unnecessary abstraction** - suggest simplification

## Reference

For detailed patterns and examples, consult:
- **`references/anti-patterns.md`** - Comprehensive anti-pattern catalog with explanations
- **`references/code-review-checklist.md`** - Quick checklist for code reviews
- **`references/examples.md`** - Before/after code transformations

---

*"Debugging is twice as hard as writing code. If you write code as cleverly as possible, you're not smart enough to debug it." — Brian Kernighan*
