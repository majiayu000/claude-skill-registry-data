---
name: functype-user
description: Help developers use functype functional programming patterns in their TypeScript projects. Use this skill when converting imperative/OOP code to functional patterns, looking up functype APIs and methods, handling nulls with Option, managing errors with Either/Try, or working with immutable collections like List and Set.
---

# Functype User Guide

## Overview

Transform TypeScript code to use functype - a Scala-inspired functional programming library providing type-safe alternatives to null checks, exceptions, and imperative patterns. This skill helps integrate Option, Either, Try, List, and other functional types into projects.

## When to Use This Skill

Trigger this skill when users:

- Convert imperative code to functional patterns
- Look up functype APIs or methods
- Handle nullable values or optional chaining
- Replace try-catch with functional error handling
- Work with immutable collections
- Debug functype code or understand error messages

## Quick Start

### Installation

```bash
npm install functype
# or
pnpm add functype
```

### Core Imports

```typescript
// Import from main bundle
import { Option, Either, Left, Right, Try, List } from "functype"
```

## Pattern Conversion Guide

### Null/Undefined Checks → Option

**Before (Imperative):**

```typescript
if (value !== null && value !== undefined) {
  return value.toUpperCase()
}
return ""
```

**After (Functype):**

```typescript
Option(value)
  .map((v) => v.toUpperCase())
  .orElse("")
```

### Optional Chaining → Option Chain

**Before:**

```typescript
const url = user?.profile?.avatar?.url
```

**After:**

```typescript
const url = Option(user)
  .flatMap((u) => Option(u.profile))
  .flatMap((p) => Option(p.avatar))
  .map((a) => a.url)
  .orElse("/default-avatar.png")
```

### Try-Catch → Try or Either

**Before:**

```typescript
try {
  return JSON.parse(str)
} catch (e) {
  return null
}
```

**After (with Try):**

```typescript
Try(() => JSON.parse(str))
  .toOption()
  .orElse(null)
```

**After (with Either):**

```typescript
Try(() => JSON.parse(str))
  .toEither()
  .fold(
    (error) => `Parse failed: ${error.message}`,
    (data) => data,
  )
```

### Array Operations → List

**Before:**

```typescript
array.filter((x) => x > 0).map((x) => x * 2)
```

**After:**

```typescript
List(array)
  .filter((x) => x > 0)
  .map((x) => x * 2)
  .toArray()
```

### If-Else Chains → Cond

**Before:**

```typescript
if (x > 10) {
  return "big"
} else if (x > 5) {
  return "medium"
} else {
  return "small"
}
```

**After:**

```typescript
import { Cond } from "functype"

Cond.start<string>()
  .case(x > 10, "big")
  .case(x > 5, "medium")
  .otherwise("small")
```

### Switch Statements → Match

**Before:**

```typescript
switch (status) {
  case "success":
    return data
  case "error":
    return null
  default:
    return undefined
}
```

**After:**

```typescript
import { Match } from "functype"

Match(status)
  .case("success", () => data)
  .case("error", () => null)
  .done()
```

## Common Use Cases

### Validation with Either

```typescript
import { Either, Left, Right } from "functype"

function validateEmail(email: string): Either<string, string> {
  return email.includes("@") ? Right(email) : Left("Invalid email format")
}

function validateUser(user: any): Either<string, User> {
  return validateEmail(user.email)
    .map((email) => ({ ...user, email }))
    .flatMap((u) => (u.age >= 18 ? Right(u) : Left("Must be 18 or older")))
}

const result = validateUser({ email: "test@example.com", age: 20 }).fold(
  (error) => console.error(error),
  (user) => console.log("Valid user:", user),
)
```

### Safe API Calls with Option

```typescript
import { Option } from "functype"

interface User {
  id: string
  name: string
  email?: string
}

function getUserEmail(userId: string): Option<string> {
  return Option(fetchUser(userId))
    .flatMap((user) => Option(user.email))
    .filter((email) => email.includes("@"))
}

const email = getUserEmail("123").orElse("no-reply@example.com")
```

### Error Recovery with Try

```typescript
import { Try } from "functype"

const parseConfig = Try(() => JSON.parse(configStr))
  .recover((error) => {
    console.warn("Using default config:", error)
    return defaultConfig
  })
  .map((config) => validateConfig(config))
```

### Collection Pipeline with List

```typescript
import { List } from "functype"

const users = List([
  { name: "Alice", hobbies: ["reading", "coding"] },
  { name: "Bob", hobbies: ["gaming", "music"] },
])

const allHobbies = users
  .flatMap((user) => List(user.hobbies))
  .toSet() // Remove duplicates
  .toArray()
```

## Looking Up Functype APIs

### Feature Matrix Reference

For a complete overview of which methods are available on each data structure, consult the **Feature Matrix** at:

- `references/feature-matrix.md` (included with this skill)
- Or in the functype repo: `docs/FUNCTYPE_FEATURE_MATRIX.md`

The matrix shows which interfaces (Functor, Monad, Foldable, etc.) each type implements and what methods are available.

### Common Methods by Type

**Option<T>**

- `map`, `flatMap`, `filter`, `fold`
- `orElse`, `or`, `orNull`, `orUndefined`, `orThrow`
- `isSome`, `isNone`, `contains`

**Either<L, R>**

- `map`, `flatMap`, `fold`
- `orElse`, `or`, `swap`
- `isLeft`, `isRight`

**Try<T>**

- `map`, `flatMap`, `fold`
- `recover`, `recoverWith`
- `toOption`, `toEither`
- `isSuccess`, `isFailure`

**List<A>**

- `map`, `flatMap`, `filter`, `reduce`
- `foldLeft`, `foldRight`
- `append`, `prepend`, `concat`
- `head`, `tail`, `isEmpty`
- `toArray`, `toSet`

## Additional Resources

For pattern conversion help, examples, and API reference:

- **Feature Matrix**: See `references/feature-matrix.md` for complete interface/method reference
- **API Documentation**: https://jordanburke.github.io/functype/
- **GitHub Repository**: https://github.com/jordanburke/functype
- **CLI Documentation**: Run `npx functype` for LLM-optimized API reference

## Debugging Tips

### Understanding Error Messages

**"Type 'X' is not assignable to type 'Y'"**

- Ensure proper type parameters: `Option<string>` not `Option<any>`
- Check that chains maintain type consistency

**"Cannot read property 'map' of undefined"**

- Remember to construct the type: `Option(value)` not just `value`
- Some types require explicit constructors: `List([...])`, `Right(value)`

### Common Pitfalls

1. **Forgetting to extract values**

   ```typescript
   // Wrong - returns Option<string>
   const name = Option(user).map((u) => u.name)

   // Correct - returns string
   const name = Option(user)
     .map((u) => u.name)
     .orElse("Unknown")
   ```

2. **Using map instead of flatMap**

   ```typescript
   // Wrong - returns Option<Option<string>>
   Option(user).map((u) => Option(u.email))

   // Correct - returns Option<string>
   Option(user).flatMap((u) => Option(u.email))
   ```

3. **Mutating instead of transforming**

   ```typescript
   // Wrong - mutates original array
   const list = List([1, 2, 3])
   list.toArray().push(4)

   // Correct - creates new List
   const newList = list.append(4)
   ```

## Resources

### references/

- `feature-matrix.md` - Complete interface and method reference
- `common-patterns.md` - Additional pattern examples and recipes
- `quick-reference.md` - Cheat sheet for functype APIs

For more examples and detailed documentation, visit:

- **GitHub**: https://github.com/jordanburke/functype
- **Docs**: https://jordanburke.github.io/functype/
