---
name: Go File Splitting
description: This skill should be used when the user asks about "file size", "large file", "split file", "file too long", "LOC limit", "organize Go files", or needs guidance on when and how to split large Go source files.
---

# Go File Splitting

Strategies for managing large Go source files and planning strategic splits.

## Overview

Large files are harder to navigate, understand, and maintain. However, not all large files should be split - cohesive code should stay together.

## Size Guidelines

| Lines | Tier | Recommendation |
|-------|------|----------------|
| <500 | 🟢 Green | No action needed |
| 500-999 | 🟡 Yellow | Monitor, consider if growing |
| ≥1000 | 🔴 Red | Evaluate for split |

## When to Split

### Good Reasons to Split

1. **Multiple Responsibilities**
   - File handles unrelated functionality
   - Clear "sections" with distinct purposes

2. **Multiple Entity Types**
   - CRUD for different domain entities
   - Handlers for different resources

3. **Mixed Abstraction Levels**
   - High-level orchestration + low-level implementation
   - Public API + internal helpers

4. **Navigation Difficulty**
   - Hard to find specific code
   - IDE outline too long to scan

### Bad Reasons to Split

1. **Just to meet line limit**
   - Cohesive code should stay together

2. **Arbitrary groupings**
   - "Functions A-M" vs "Functions N-Z"

3. **Small splits**
   - Creating files <50 lines

4. **Breaking cohesion**
   - Separating tightly coupled code

## Split Strategies

### Strategy 1: By Responsibility

Split file along clear responsibility boundaries.

**Before:** `handler.go` (1500 lines)
```
- 400 lines: HTTP handlers
- 350 lines: Validation logic
- 300 lines: Response formatting
- 250 lines: Middleware
- 200 lines: Helpers
```

**After:**
```
handler.go      (400 lines) - HTTP handlers
validation.go   (350 lines) - Validation
response.go     (300 lines) - Response formatting
middleware.go   (250 lines) - Middleware
helpers.go      (200 lines) - Shared helpers
```

### Strategy 2: By Entity

Split when one file handles multiple domain entities.

**Before:** `store.go` (2000 lines)
```
- User CRUD operations
- Order CRUD operations
- Product CRUD operations
- Shared database helpers
```

**After:**
```
store.go         (200 lines) - Shared helpers, interface
store_user.go    (600 lines) - User operations
store_order.go   (700 lines) - Order operations
store_product.go (500 lines) - Product operations
```

### Strategy 3: By Visibility

Split public API from implementation details.

**Before:** `parser.go` (1200 lines)
```
- Parse() - main entry point
- Internal parsing functions
- Helper functions
```

**After:**
```
parser.go      (200 lines) - Public API (Parse, Config)
parser_impl.go (800 lines) - Core parsing implementation
parser_util.go (200 lines) - Utility functions
```

### Strategy 4: By Complexity

Extract complex algorithms into dedicated files.

**Before:** `process.go` (1500 lines)
```
- Simple orchestration
- Complex algorithm A (500 lines)
- Complex algorithm B (600 lines)
```

**After:**
```
process.go        (400 lines) - Orchestration
process_algo_a.go (500 lines) - Algorithm A
process_algo_b.go (600 lines) - Algorithm B
```

## Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| `{name}.go` | `handler.go` | Core/primary file |
| `{name}_{aspect}.go` | `store_user.go` | Entity/aspect variant |
| `{aspect}.go` | `validation.go` | Standalone aspect |

## Justified Large Files

Some files are appropriately large:

1. **Single complex algorithm**
   - Parser implementations
   - State machines
   - Mathematical computations

2. **Generated code**
   - Protocol buffers
   - API clients
   - Schema types

3. **Type definitions with methods**
   - Large struct with many methods
   - All methods closely related

Document these decisions:

```go
// Package expr implements expression parsing.
//
// This file is intentionally large (~1200 LOC) because the
// recursive descent parser is highly interconnected and
// splitting would obscure the algorithm flow.
// See ADR-015 for the decision rationale.
package expr
```

## File Organization Checklist

Before splitting, verify:
- [ ] Clear responsibility boundaries exist
- [ ] New files will be >50 lines each
- [ ] Names describe contents clearly
- [ ] No circular dependencies created
- [ ] Tests still run correctly
- [ ] IDE navigation improves

After splitting, verify:
- [ ] `go build ./...` passes
- [ ] `go test ./...` passes
- [ ] `golangci-lint run ./...` passes
- [ ] File sizes are in green/yellow range
- [ ] Each file has clear purpose

## Test File Handling

Generally keep test files together unless:
- Tests are >2000 lines
- Clear test groupings exist
- Each test file maps to a source file

When splitting tests:
```
store_test.go        → Common test helpers
store_user_test.go   → User tests
store_order_test.go  → Order tests
```
