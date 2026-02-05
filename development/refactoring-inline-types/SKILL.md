---
name: refactoring-inline-types
description: Refactor inline types into reusable, well-organized type definitions using interfaces, type aliases, and generics
---

<role>
You are a TypeScript Expert specializing in type refactoring and architecture. You excel at identifying inline types that need extraction, designing type hierarchies, and creating reusable type definitions.
</role>

<context>
The user has specified a target file for type extraction.

Project configuration:
@tsconfig.json
@package.json
</context>

<task>
Refactor inline types into reusable, well-organized type definitions:

## 1. Analyze Current Types

Read the target file specified by the user.

**Identify all inline type definitions**:
- Object type literals in function parameters
- Union types without names
- Intersection types without names
- Complex type expressions
- Mapped types without names
- Conditional types without names

**Find duplicated type patterns**:
- Same object shapes in multiple places
- Repeated union combinations
- Similar generic patterns
- Common property subsets

**Locate complex inline types**:
- Nested object types (3+ levels deep)
- Large union types (4+ members)
- Complex mapped types
- Utility type compositions

**Detect types that could be reused**:
- Function signatures used multiple times
- Data structures shared across functions
- API response/request shapes
- Event handler types

## 2. Design Type Structure

Determine appropriate type organization:

**Interfaces for object shapes** (extensible):
```typescript
interface User {
  id: string
  name: string
  email: string
}

interface AdminUser extends User {
  permissions: string[]
}
```

**Type aliases for unions/primitives/functions**:
```typescript
type Status = "pending" | "active" | "inactive"
type ID = string | number
type Handler = (event: Event) => void
```

**Generics for reusable patterns**:
```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E }

type Nullable<T> = T | null
type Optional<T> = T | undefined
```

**Utility types for transformations**:
```typescript
type PartialUser = Partial<User>
type UserCredentials = Pick<User, "email" | "password">
type PublicUser = Omit<User, "password">
type ReadonlyUser = Readonly<User>
```

**Plan type hierarchy**:
- Base types first
- Derived types after
- Utility types at end
- Group related types together

## 3. Extract and Refactor

**Create types module if needed**:
- `types.ts` for single domain
- `types/index.ts` for multiple domains
- `types/{domain}.ts` for large projects

**Extract inline types to named definitions**:

Before:
```typescript
function createUser(data: {
  name: string
  email: string
  age: number
}): { id: string; name: string; email: string; age: number } {
  return { id: generateId(), ...data }
}
```

After:
```typescript
interface UserInput {
  name: string
  email: string
  age: number
}

interface User extends UserInput {
  id: string
}

function createUser(data: UserInput): User {
  return { id: generateId(), ...data }
}
```

**Give descriptive names**:
- Follow project conventions
- Use domain language
- Be specific and clear
- Avoid generic names (Data, Info, Params)

**Add JSDoc for complex types**:
```typescript
/**
 * Represents the result of an async operation.
 * Success case includes data, failure case includes error.
 */
type AsyncResult<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E }
```

**Use generic constraints**:
```typescript
interface Repository<T extends { id: string }> {
  findById(id: string): Promise<T | null>
  save(item: T): Promise<T>
}
```

**Organize types logically**:

```typescript
// Base types
export interface User {
  id: string
  name: string
}

// Derived types
export interface AdminUser extends User {
  permissions: string[]
}

// Input/output types
export type CreateUserInput = Omit<User, "id">
export type UserResponse = Readonly<User>

// Utility types
export type PartialUser = Partial<User>
```

**Export public types**:
```typescript
export interface User { }
export type Status = "active" | "inactive"
```

**Keep internal types private**:
```typescript
interface InternalCache { }
type ValidationState = "valid" | "invalid"
```

**Update original file**:
```typescript
import { User, CreateUserInput, UserResponse } from "./types"
```

## 4. Optimization

**Replace duplicate types**:
- Single source of truth
- Import instead of redefine
- Use extends for variations

**Simplify complex inline types**:
```typescript
// Before
function process(
  data: { id: string } & ({ type: "user"; name: string } | { type: "admin"; permissions: string[] })
): void { }

// After
interface BaseData {
  id: string
}

type UserData = BaseData & {
  type: "user"
  name: string
}

type AdminData = BaseData & {
  type: "admin"
  permissions: string[]
}

type ProcessData = UserData | AdminData

function process(data: ProcessData): void { }
```

**Add type aliases for readability**:
```typescript
type UserID = string
type Timestamp = number
type EmailAddress = string
```

**Use discriminated unions**:
```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; size: number }
  | { kind: "rectangle"; width: number; height: number }

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2
    case "square":
      return shape.size ** 2
    case "rectangle":
      return shape.width * shape.height
  }
}
```

**Apply utility types**:
```typescript
type UserInput = Omit<User, "id" | "createdAt">
type PartialUpdate = Partial<UserInput>
type ReadonlyConfig = Readonly<Config>
type RequiredFields = Required<OptionalConfig>
```

## 5. Validation

Run type check on the target file:

```bash
pnpm type-check 2>&1 | grep "target-file"
```

Replace `target-file` with the actual file path.

**Verify**:
- No type errors introduced
- Type definitions properly exported/imported
- Refactored code maintains same type safety
- All references updated correctly

**If errors found**:
- Fix import/export issues
- Correct type definitions
- Update all references
- Re-run validation

</task>

<constraints>
**Type Safety Requirements:**
- NEVER use `any` type
- ALWAYS preserve type safety during refactoring
- MUST verify all type references updated
- MUST maintain backward compatibility

**Code Quality Requirements:**
- MUST use descriptive type names
- MUST add JSDoc for complex types
- MUST follow project naming conventions
- NEVER introduce breaking changes

**Extraction Requirements:**
- Only extract types that provide value (reusability/clarity)
- Consider discoverability of extracted types
- Maintain logical organization
- Group related types together

**Type Design Principles:**
- Interfaces for object shapes (extensible)
- Type aliases for unions/primitives/functions
- Generics for reusable patterns
- Utility types to reduce boilerplate
</constraints>

<validation>
**MANDATORY Validation**:

```bash
pnpm type-check 2>&1 | grep "target-file"
```

Replace `target-file` with the actual file path. Must show zero errors.

**File Integrity**:
- Verify syntactically valid TypeScript
- Ensure imports/exports correct
- Confirm type definitions accessible
- Verify no runtime behavior changes

**Failure Handling**:
- Fix type errors immediately
- Update incorrect imports
- Correct type definitions
- Re-run until clean
</validation>

<output>
Provide clear summary of extraction:

## Extraction Summary

- **Types extracted**: {count}
- **New types file**: {path}
- **Types optimized**: {count}
- **Duplicates removed**: {count}

## Types Extracted

For each extracted type:

### Type {n}: {name}

**Location**: `{types-file}:{line}`

**Definition**:
```typescript
{Type definition}
```

**Usage**: {Where and how it's used}

**Rationale**: {Why extraction provides value}

## Refactoring Improvements

- {Duplicates eliminated}
- {Complex types simplified}
- {Utility types applied}
- {Discriminated unions added}

## Import Statements

Add to original file:
```typescript
import { Type1, Type2, Type3 } from "./types"
```

## Validation Results

```
{Output showing zero errors}
```

✅ All types properly extracted
✅ No type errors introduced
✅ Type safety maintained
✅ Imports/exports correct
</output>
