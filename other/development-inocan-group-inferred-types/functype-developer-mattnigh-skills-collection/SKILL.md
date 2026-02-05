---
name: functype-developer
description: Assist contributors working on the functype library codebase. Use this skill when creating new data structures, implementing functional interfaces (Functor, Monad, Foldable), adding tests, debugging library internals, or understanding functype's Scala-inspired architecture patterns including the Base pattern, HKT system, and Companion utilities.
---

# Functype Library Developer

## Overview

Guide for contributing to the functype TypeScript library. This skill provides architectural patterns, development workflows, and tooling for implementing new functional data structures following functype's Scala-inspired design.

## When to Use This Skill

Trigger this skill when:

- Creating new data structures or types
- Implementing functional interfaces (Functor, Monad, Foldable, etc.)
- Adding or fixing tests
- Understanding library architecture
- Debugging functional type implementations
- Following the Base pattern and type class system
- Working with the Feature Matrix

## Development Workflow

### Prerequisites

- **Node.js**: ≥ 18.0.0
- **pnpm**: 10.12.1
- **TypeScript**: Strict mode enabled

### Essential Commands

```bash
# Install dependencies
pnpm install

# Development (build with watch)
pnpm dev

# Before committing (MUST PASS)
pnpm validate

# Run tests
pnpm test

# Run specific test file
pnpm vitest run test/specific.spec.ts

# Check types without building
pnpm compile
```

### Pre-Commit Checklist

**Always run before committing:**

```bash
pnpm validate
```

This runs:

1. **Format**: Prettier formatting
2. **Lint**: ESLint checks
3. **Test**: All Vitest tests
4. **Build**: Production build

## Core Architecture

### Scala-Inspired Constructor Pattern

All types follow this pattern:

```typescript
// Constructor function returns object with methods
const option = Option(value) // Constructor
option.map((x) => x + 1) // Instance methods
Option.none() // Companion methods
```

**NOT class-based:**

```typescript
// ❌ Don't do this
class Option<T> {
  constructor(value: T) { ... }
}

// ✅ Do this
export function Option<T>(value: T | null | undefined): OptionType<T> {
  return value == null ? none() : some(value)
}
```

### Base Pattern

Use the `Base` function to add common functionality to all types:

```typescript
import { Base } from "@/core/base"

export function Option<T>(value: T | null | undefined): OptionType<T> {
  if (value == null) {
    return Base("None", {
      // methods here
      map: <B>(f: (val: T) => B) => Option.none<B>(),
      // ...
    })
  }

  return Base("Some", {
    // methods here
    map: <B>(f: (val: T) => B) => Option(f(value)),
    // ...
  })
}
```

**Base provides:**

- `Typeable` interface (type metadata)
- Standard `toString()` method
- Consistent object structure

### Type System Foundation

**Base constraint:**

```typescript
import type { Type } from "@/functor"

// Use Type instead of any
function process<T extends Type>(value: T): void {
  // ...
}
```

**Never use `any`**:

- Use `unknown` for uncertain types
- Use `Type` for generic constraints
- Use proper type definitions

### Functional Interfaces

Every container type should implement these when applicable:

**Core interfaces** (see `references/architecture.md` for details):

- `Functor` - map over values
- `Applicative` - apply wrapped functions
- `Monad` - flatMap for sequencing
- `Foldable` - extract via pattern matching
- `Traversable` - collection operations
- `Serializable` - JSON/YAML/binary serialization

**Reference the Feature Matrix:**
Check `docs/FUNCTYPE_FEATURE_MATRIX.md` to see which interfaces each type implements and what methods are required.

## Creating a New Data Structure

### Step-by-Step Guide

**1. Research existing patterns**

```bash
# Use the Explore agent to understand the codebase
# Look at Option, Either, or Try as reference implementations
```

**2. Create module structure**

```bash
mkdir -p src/mynewtype
touch src/mynewtype/index.ts
touch test/mynewtype.spec.ts
```

**3. Use the template script**

```bash
# Run the new-type-template script
./claude/skills/functype-developer/scripts/new-type-template.sh MyNewType
```

This generates:

- Basic type structure
- Required interface implementations
- Test file boilerplate

**4. Implement the type**

Follow the constructor pattern:

```typescript
// src/mynewtype/index.ts
import { Base } from "@/core/base"
import type { Functor } from "@/functor"

export type MyNewType<T> = Functor<T> & {
  // Your methods here
  getValue(): T
}

export function MyNew<T>(value: T): MyNewType<T> {
  return Base("MyNewType", {
    // Functor
    map: <B>(f: (val: T) => B): MyNewType<B> => {
      return MyNew(f(value))
    },

    // Your methods
    getValue: () => value,

    // Pipe for composition
    pipe: () => ({
      map: (f: (val: T) => any) => MyNew(value).map(f),
    }),
  })
}

// Companion methods
MyNew.empty = <T>() => MyNew<T>(null as any)
```

**5. Add exports**

Update `src/index.ts`:

```typescript
export { MyNew } from "./mynewtype"
export type { MyNewType } from "./mynewtype"
```

Update `package.json` exports:

```json
{
  "exports": {
    "./mynewtype": {
      "import": "./dist/esm/mynewtype/index.js",
      "require": "./dist/cjs/mynewtype/index.js",
      "types": "./dist/types/mynewtype/index.d.ts"
    }
  }
}
```

**6. Write comprehensive tests**

```typescript
// test/mynewtype.spec.ts
import { describe, expect, it } from "vitest"
import { MyNew } from "@/mynewtype"

describe("MyNewType", () => {
  describe("Construction", () => {
    it("should create from value", () => {
      const value = MyNew(5)
      expect(value.getValue()).toBe(5)
    })
  })

  describe("Functor", () => {
    it("should map over values", () => {
      const result = MyNew(5).map((x) => x * 2)
      expect(result.getValue()).toBe(10)
    })
  })

  // More tests...
})
```

**7. Update Feature Matrix**

Add your type to `docs/FUNCTYPE_FEATURE_MATRIX.md` showing which interfaces it implements.

**8. Validate**

```bash
pnpm validate
```

### Interface Implementation Checklist

When implementing interfaces, refer to this checklist:

**Functor:**

- [ ] `map<B>(f: (value: A) => B): Functor<B>`

**Applicative (extends Functor):**

- [ ] `ap<B>(ff: Applicative<(value: A) => B>): Applicative<B>`

**Monad (extends Applicative):**

- [ ] `flatMap<B>(f: (value: A) => Monad<B>): Monad<B>`

**Foldable:**

- [ ] `fold<B>(onEmpty: () => B, onValue: (value: A) => B): B`
- [ ] `foldLeft<B>(z: B): (op: (b: B, a: A) => B) => B`
- [ ] `foldRight<B>(z: B): (op: (a: A, b: B) => B) => B`

See `references/architecture.md` for complete interface definitions.

## Testing Patterns

### Test Structure

Use Vitest with describe/it pattern:

```typescript
describe("TypeName", () => {
  describe("Feature Group", () => {
    it("should do specific thing", () => {
      // Arrange
      const input = createInput()

      // Act
      const result = performOperation(input)

      // Assert
      expect(result).toBe(expected)
    })
  })
})
```

### Property-Based Testing

Use fast-check for property tests:

```typescript
import { fc, test } from "@fast-check/vitest"

test.prop([fc.integer()])("should always return positive", (n) => {
  const result = Math.abs(n)
  expect(result).toBeGreaterThanOrEqual(0)
})
```

### Edge Cases to Test

Always test:

- Empty/null/undefined inputs
- Type inference correctness
- Method chaining
- Error cases
- Immutability (original unchanged)

## Code Style Guidelines

### Imports

```typescript
// Type-only imports when possible
import type { Type } from "@/functor"
import { Option } from "@/option"

// Organized with simple-import-sort (automatic)
```

### Types

```typescript
// ✅ Use Type for constraints
function process<T extends Type>(value: T): void

// ✅ Prefer types over interfaces
export type MyType<T> = {
  value: T
}

// ✅ Explicit type annotations
function transform<T>(input: T): MyType<T> {
  return { value: input }
}
```

### Naming

```typescript
// PascalCase for types
type OptionType<T> = { ... }

// camelCase for functions/variables
const someValue = Option(5)
function mapOption<T>(opt: OptionType<T>) { ... }

// Constructor functions are PascalCase
Option(value)
Either(value)
```

### Functional Style

```typescript
// ✅ Immutability
const newList = list.append(item)

// ❌ Mutation
list.push(item)

// ✅ Pure functions
function double(x: number): number {
  return x * 2
}

// ❌ Side effects
function double(x: number): number {
  console.log(x) // side effect
  return x * 2
}
```

### Pattern Matching

```typescript
// ✅ Use Cond for conditionals
import { Cond } from "@/cond"

Cond.start<string>()
  .case(x > 10, "big")
  .case(x > 5, "medium")
  .otherwise("small")

// ✅ Use Match for switches
import { Match } from "@/match"

Match(status)
  .case("success", () => handleSuccess())
  .case("error", () => handleError())
  .done()

// ❌ Avoid early returns
// Use Cond or Option instead
```

## Common Development Tasks

### Adding a Helper Method

```typescript
// Add to type definition
export type MyType<T> = {
  // existing methods...

  // New helper
  isEmpty(): boolean
}

// Implement in constructor
export function MyType<T>(value: T): MyType<T> {
  return Base("MyType", {
    // existing methods...

    isEmpty: () => value == null,
  })
}
```

### Implementing Serialization

```typescript
import { createSerializable } from "@/core/serializable"

export function MyType<T>(value: T): MyType<T> {
  return Base("MyType", {
    // other methods...

    serialize: () =>
      createSerializable({
        type: "MyType",
        value: value,
      }),
  })
}
```

### Adding Do-Notation Support

```typescript
export const MyTypeCompanion = {
  Do: <T>(gen: () => Generator<MyType<any>, T, any>): MyType<T> => {
    // Implementation here
    // See Option or Either for reference
  },
}

export const MyType = Object.assign(MyTypeConstructor, MyTypeCompanion)
```

## Debugging Tips

### TypeScript Errors

**"Type instantiation is excessively deep"**

- Check for circular type references
- Simplify nested generic types
- Use type aliases to break up complex types

**"Property 'X' does not exist on type 'Y'"**

- Ensure all interfaces are properly implemented
- Check that types are correctly exported
- Verify Base pattern includes all required methods

### Test Failures

```bash
# Run specific test with verbose output
pnpm vitest run test/mytype.spec.ts --reporter=verbose

# Run tests in watch mode
pnpm test:watch

# Check test coverage
pnpm test:coverage
```

### Build Issues

```bash
# Clean and rebuild
pnpm clean && pnpm build

# Check TypeScript compilation only
pnpm compile

# Analyze bundle size
pnpm analyze:size
```

## Resources

### scripts/

- `new-type-template.sh` - Generate boilerplate for new types
- `validate.sh` - Run the full validation workflow

### references/

- `architecture.md` - Detailed architecture and patterns
- `adding-types.md` - Complete guide for adding new data structures
- `testing-patterns.md` - Testing strategies and examples

### External Links

- **GitHub**: https://github.com/jordanburke/functype
- **Docs**: https://jordanburke.github.io/functype/
- **Feature Matrix**: `docs/FUNCTYPE_FEATURE_MATRIX.md`
