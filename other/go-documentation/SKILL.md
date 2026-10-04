---
name: go-documentation
description: "Writing idiomatic Golang documentation. Covers godoc comments, README structure, and Example tests."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:55:00 GMT
---

## Core Documentation Layers

1. **Godoc Comments** — Comments on exported types, functions, and variables that render on pkg.go.dev.
2. **README.md** — The front page of the project (Installation, Usage, Examples).
3. **Example Tests** — Runnable code examples in `_test.go` files that appear in Godoc.
4. **CONTRIBUTING.md** — Guide for new developers to set up and contribute.
5. **llms.txt** — Structured overview for AI agents and LLMs.

## Godoc Best Practices

### 1. Formatting
Comments must start with the name of the identifier being documented and be a complete sentence.
```go
// User represents a system user account.
type User struct { ... }

// FindByID retrieves a user by their unique identifier.
// It returns ErrNotFound if no user exists with the given ID.
func FindByID(ctx context.Context, id string) (*User, error) { ... }
```

### 2. Package Comments
Every package should have a package comment in `doc.go` or the main file of the package.
```go
// Package auth provides primitives for user authentication and 
// session management.
package auth
```

### 3. Example Functions
Place these in `_test.go`. They are verified by `go test`.
```go
func ExampleFindByID() {
    user, err := FindByID(ctx, "123")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(user.Name)
    // Output: John Doe
}
```

## README Structure (Recommended)

1. **Title and Badges** (Go version, License, CI status).
2. **One-sentence Summary**.
3. **Demo / Quick Start** (minimal code example).
4. **Installation Instructions**.
5. **Features / Roadmap**.
6. **License**.

## API Documentation

- **REST/HTTP**: Use `swaggo/swag` to generate OpenAPI specs from code comments.
- **gRPC**: Use Protobuf definitions as the source of truth.

## AI-Friendly Documentation

Include a `llms.txt` at the root of the repository to provide a concise summary of the project architecture and key entry points for AI coding assistants.

## Anti-patterns

- ❌ **Exported identifiers without comments** — Triggers a lint warning and makes the API hard to use.
- ❌ **Restating the name** — `// FindByID finds by ID.` (Low value). Explain the *why* and the *errors*.
- ❌ **Outdated examples** — Code examples in READMEs that don't compile. Use `Example` tests instead.
- ❌ **Huge monolithic README** — For large projects, move deep-dives into a `docs/` folder.
- ❌ **Missing package comment** — Makes the library overview page on pkg.go.dev empty.
