---
name: scala-conventions-enforcer
description: This skill should be used proactively before writing any Scala code for the first time in a session. It ensures all Scala code adheres to project-specific coding standards, formatting rules, naming conventions, and architectural patterns defined in the comprehensive style guide. Trigger this skill when about to write Scala classes, traits, objects, or modify existing Scala files.
---

# Scala Conventions Enforcer

## Overview

This skill enforces consistent Scala coding standards across the test-probe project. It provides comprehensive guidelines for formatting, naming, package structure, visibility patterns, actor design, and testing practices specific to this Scala 3.3.6 LTS project built on Apache Pekko Typed Actors.

**When to activate**: Proactively load this skill before writing, or peer reviewing / quality checks, Scala code for the first time in any session to ensure all code follows established conventions from the start.

---

## ⚠️ MANDATORY ACTIVATION - READ THIS FIRST ⚠️

**CRITICAL**: This skill MUST be loaded before any Scala code work in EVERY session.

### Activation Triggers (Load Immediately When You See These)

**MUST LOAD BEFORE**:
- ✋ Reviewing Scala code (peer reviews, quality checks, code analysis)
- ✋ Writing ANY Scala code (new files, modifications, refactoring)
- ✋ Discussing Scala implementation approaches
- ✋ Answering questions about Scala patterns

**TRIGGER PHRASES** that should activate this skill:
- "review this Scala code"
- "peer review"
- "check the code"
- "let me write..."
- "I'll implement..."
- "add a new class/object/trait"

### Failure Mode (What Happens If You Don't Load This)

❌ **Incomplete Reviews**: Miss project-specific patterns (Try/Either, visibility, Scala 3 syntax)
❌ **Wrong Severity**: Call STANDARD violations "minor style issues"
❌ **Generic Feedback**: Give general Scala advice instead of project-specific guidance
❌ **Java-Looking Code**: Produce barely-compiles code instead of beautiful, expressive Scala
❌ **Wasted Time**: User has to correct you on conventions you should already know

### Loading Process (Do This NOW)

1. **Load this skill** (you're doing it right now ✅)
2. **Read the authoritative style guide**: `.claude/styles/scala-conventions.md` (single source of truth - 361 lines)
3. **Keep it in mind** throughout the session
4. **Apply standards** to all Scala work

---

## Core Principle

**All Scala code must strictly adhere to the conventions in `.claude/styles/scala-conventions.md` (SINGLE SOURCE OF TRUTH)**. These are not suggestions—they are mandatory standards that ensure:

- Consistent code quality across the codebase
- High testability (70%+ coverage minimum, 85%+ for actors)
- Proper actor patterns and supervision strategies
- Type safety and explicit typing
- Maintainable and readable code

## Quick Reference Checklist

Before writing any Scala code, verify adherence to these critical standards:

### Formatting & Structure
- [ ] 2-space indentation (no tabs)
- [ ] Maximum 120 character line length
- [ ] Package structured as chained declarations (not single-line)
- [ ] Explicit return types on all public methods
- [ ] All variables explicitly typed

### Naming
- [ ] PascalCase for classes/objects/traits
- [ ] camelCase for methods/variables
- [ ] UPPER_SNAKE_CASE for constants
- [ ] No `*Impl` suffixes on classes

### Visibility Pattern (CRITICAL for testability)
- [ ] Methods are PUBLIC (not `private`)
- [ ] Visibility restriction at object/class level using `private[module]`
- [ ] Companion objects for actor behaviors
- [ ] This pattern enables 85%+ test coverage

### Actor-Specific Conventions
- [ ] Typed actors using Pekko Typed APIs
- [ ] Sealed trait for message protocols
- [ ] Companion object with `apply()` behavior factory
- [ ] Supervision strategy defined
- [ ] Error kernel pattern for critical actors

### Testing Requirements
- [ ] Unit tests for all public methods
- [ ] Component tests (BDD) for integration scenarios
- [ ] Minimum 70% coverage (85% for actors, 80% for business logic)
- [ ] ScalaTest with FlatSpec or FunSpec style

## How to Use This Skill

### 1. Load the Complete Style Guide

Before writing OR reviewing Scala code, read the authoritative style guide (single source of truth):

**MUST READ**: `.claude/styles/scala-conventions.md`

**NOTE**: This skill does NOT duplicate the style guide. Always read the authoritative file above.

This file contains detailed guidance on:
- Formatting and code structure
- Naming conventions
- Import organization and package structuring
- Method definitions and explicit typing
- Pattern matching best practices
- Actor patterns and Pekko conventions
- Future and async patterns
- Error handling strategies
- Testing standards
- Visibility pattern for testability
- And more...

### 2. Apply Conventions During Development

**Before writing code:**
- Review the relevant section of scala-conventions.md
- Plan class structure following the patterns
- Apply visibility pattern for testability

**While writing code:**
- Follow formatting rules (indentation, line length, braces)
- Use explicit types on all variables and public methods
- Structure packages as chained declarations
- Apply proper naming conventions

**After writing code:**
- Verify visibility pattern is applied (public methods, `private[module]` objects)
- Ensure all conventions are followed
- Write corresponding tests following testing standards

### 3. Common Violations to Avoid

The skill helps prevent these frequent violations:

❌ **Using `private` methods** → Reduces coverage by 20-40%
```scala
object MyActor {
  private def handleMessage(...) = { ... }  // ❌ CANNOT UNIT TEST
}
```

✅ **Correct visibility pattern**
```scala
private[core] object MyActor {
  def handleMessage(...) = { ... }  // ✅ CAN UNIT TEST
}
```

❌ **Implicit typing**
```scala
val timeout = 5.seconds  // ❌ Type not explicit
```

✅ **Explicit typing**
```scala
val timeout: FiniteDuration = 5.seconds  // ✅ Type explicit
```

❌ **Single-line package declaration**
```scala
package io.distia.probe.actors.routers  // ❌
```

✅ **Chained package declaration**
```scala
package io.distia.probe
package actors
package routers  // ✅ Enables relative imports
```

## Integration with Project Standards

This skill works in conjunction with other project enforcement mechanisms:

- **visibility-pattern-guardian** skill: Actively blocks `private` method violations
- **test-quality-enforcer** skill: Enforces coverage thresholds
- **scala-ninja** agent: Expert code review for advanced patterns
- **akka-expert** agent: Actor system and supervision guidance

## Resources

### 📖 Authoritative Style Guide (Single Source of Truth)

**`.claude/styles/scala-conventions.md`**

This is the ONLY authoritative style guide. Do not reference or maintain duplicates.

The complete Scala coding standards document covering:
- Comprehensive formatting rules (Scala 3 `then` keyword, indentation, line length)
- Detailed naming conventions (PascalCase, camelCase, UPPER_SNAKE_CASE)
- Package and import organization (chained declarations, import grouping)
- Visibility patterns for testability (public methods, `private[module]` objects)
- Actor-specific conventions (Pekko Typed APIs, message protocols, supervision)
- Future/async patterns (non-blocking bias, `.map` over `.onSuccess`)
- Error handling best practices (Try/Either, `.toEither`, `.left.map`)
- Functional styling (if/then, Option matching, expressive code)
- Testing standards and requirements (70%+ coverage, unit + component + BDD)
- Code examples and anti-patterns (what to do, what NOT to do)

**Usage**: Read this file BEFORE writing or reviewing ANY Scala code to ensure full compliance with project standards.