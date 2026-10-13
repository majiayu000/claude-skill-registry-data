---
name: golang-style-guide
description: "Conventions and best practices for writing readable, maintainable Go code based on the Google Go Style Guide. Use this skill when: Writing new Go packages, services, or command-line tools. Refactoring Go code to improve clarity and maintainability. Enforcing idiomatic Go naming, formatting, and structure. Designing APIs and libraries for long-term maintainability. Avoiding unnecessary abstraction or complexity in Go programs."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Skill: Go (Google Style Guide)

## Overview

This skill implements conventions from the [Google Go Style Guide](https://google.github.io/styleguide/go/guide).

The goal is to produce Go code that is:

- Clear and easy to read
- Simple and idiomatic
- Concise with a high signal-to-noise ratio
- Maintainable over time
- Consistent with the broader Go ecosystem

Readable code is prioritized over clever or complex solutions.

---

# Core Principles

## 1. Clarity

Code must be easy to understand. Prefer self-describing names. Comments should explain **why**, not **what**.

## 2. Simplicity

Use the simplest approach. Prefer core language features and the standard library. Avoid unnecessary abstraction.

## 3. Concision

High signal-to-noise ratio. Reduce repetition and boilerplate. Use common Go idioms.

## 4. Maintainability

Easy to modify correctly. Clear structure, low coupling, and meaningful tests.

---

# Formatting & Imports

## Always Use `gofmt`

All Go source code must be formatted with `gofmt`.

## Import Grouping

Imports should be organized into two groups:

1. Standard library packages
2. Third-party and project-specific packages

Separate these two groups with a blank line. Within each group, imports should be sorted alphabetically.

Example:

```go
import (
    "fmt"
    "os"

    "github.com/google/uuid"
    "myproject/internal/pkg"
)
```

---

# Naming

## MixedCaps & Initialisms

Go uses `MixedCaps` (camelCase or PascalCase).
**Initialisms** (acronyms) should have consistent casing. `URL` should be `URL` or `url`, never `Url`. `ID` should be `ID` or `id`, never `Id`.

| Correct          | Incorrect        |
| :--------------- | :--------------- |
| `XMLHTTPRequest` | `XmlHttpRequest` |
| `userID`         | `userId`         |
| `appID`          | `appId`          |
| `gRPC`           | `grpc`           |

## Package Names

- Short, all-lowercase, single word.
- No underscores or MixedCaps.
- Avoid names likely to be shadowed (e.g., use `usercount` instead of `count`).
- Rename imports if the original package name contains underscores.

## Receiver Names

- Short (1-2 letters), usually an abbreviation of the type.
- Be consistent within a type's method set.
- Avoid generic names like `me`, `this`, or `self`.

Example:

```go
func (tr *Tray) Activate() { ... }
func (ri *ResearchInfo) GetDetails() { ... }
```

---

# Receiver Types (Value vs. Pointer)

- Use a **pointer receiver** if the method needs to mutate the receiver.
- Use a **pointer receiver** if the receiver is a large struct or array.
- Use a **value receiver** for small, immutable types (like basic types or small structs with no pointers).
- **Consistency:** If any method of a type has a pointer receiver, all methods should probably have pointer receivers.

---

# Comments & Documentation

## Doc Comments

- Every exported symbol should have a doc comment.
- Comments must be complete sentences starting with the name of the symbol.
- Use the [Go doc comment style](https://go.dev/doc/comment).

Example:

```go
// A Server handles serving quotes from the works of Shakespeare.
type Server struct { ... }

// Encode writes the JSON encoding of req to w.
func Encode(w io.Writer, req *Request) { ... }
```

---

# Error Handling

## Error Strings

- Error strings should **not** be capitalized.
- Error strings should **not** end with punctuation.
- This ensures they flow well when wrapped or logged.

Example:

```go
// Good
return fmt.Errorf("something bad happened")

// Bad
return fmt.Errorf("Something bad happened.")
```

---

# Testing

Maintain a comprehensive test suite.

- Use **table-driven tests** for complex logic.
- Tests should be deterministic and provide clear failure messages.
- Focus on behavior over implementation details.

---

# Consistency

Consistency within a package is paramount. If the style guide is silent, follow the existing patterns in the codebase.

---

# Summary

1. **Clarity** over cleverness.
2. **Standard library** over dependencies.
3. **Idiomatic patterns** (errors, receivers, naming).
4. **Consistency** with the Google Go Style Guide.
