---
name: using-generics
description: Teaches generic constraints, avoiding any in generic defaults, and mapped types in TypeScript. Use when creating reusable functions, components, or types that work with multiple types while maintaining type safety.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
version: 1.0.0
---

<role>
This skill teaches how to use TypeScript generics effectively with proper constraints, avoiding `any` defaults, and leveraging mapped types for type transformations.
</role>

<when-to-activate>
This skill activates when:

- Creating reusable functions or classes
- Designing generic APIs or libraries
- Working with generic defaults (`<T = ...>`)
- Implementing mapped types or conditional types
- User mentions generics, type parameters, constraints, or reusable types
</when-to-activate>

<overview>
Generics enable writing reusable code that works with multiple types while preserving type safety. Proper use of constraints prevents `any` abuse and provides better IDE support.

**Key Concepts**:

1. **Generic Parameters**: `<T>` - Type variables that get filled in at call site
2. **Constraints**: `<T extends Shape>` - Limits what types T can be
3. **Defaults**: `<T = string>` - Fallback when type not provided
4. **Mapped Types**: Transform existing types systematically

**Impact**: Write flexible, reusable code without sacrificing type safety.
</overview>

<workflow>
## Generic Design Flow

**Step 1: Identify the Varying Type**

What changes between uses?
- Data type in container (Array<T>, Promise<T>)
- Object shape variations
- Return type based on input
- Multiple related types

**Step 2: Choose Constraint Strategy**

**No Constraint** - Accepts any type
```typescript
function identity<T>(value: T): T {
  return value;
}
```

**Extends Constraint** - Requires specific shape
```typescript
function logId<T extends { id: string }>(item: T): void {
  console.log(item.id);
}
```

**Union Constraint** - Limited set of types
```typescript
function process<T extends string | number>(value: T): T {
  return value;
}
```

**Multiple Constraints** - Multiple type parameters with relationships
```typescript
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

**Step 3: Set Default (If Needed)**

Prefer no default over `any` default:
```typescript
interface ApiResponse<T = unknown> { data: T; }
```

Or require explicit type parameter:
```typescript
interface ApiResponse<T> { data: T; }
```
</workflow>

<examples>
## Example 1: Generic Function Constraints

**❌ No constraint (too permissive)**

```typescript
function getProperty<T>(obj: T, key: string): any {
  return obj[key];
}
```

**Problems**:
- `obj[key]` not type-safe (T might not have string keys)
- Returns `any` (loses type information)
- No IDE autocomplete for key

**✅ Proper constraints**

```typescript
function getProperty<T extends object, K extends keyof T>(
  obj: T,
  key: K
): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name");
const invalid = getProperty(user, "invalid");
```

**Benefits**:
- Type-safe key access
- Return type is `T[K]` (actual property type)
- IDE autocompletes valid keys
- Compile error for invalid keys

---

## Example 2: Generic Defaults

**❌ Using `any` default (unsafe)**

```typescript
interface Result<T = any> {
  data: T;
  error?: string;
}

const result: Result = { data: "anything" };
result.data.nonExistentProperty;
```

**✅ Using `unknown` default (safe)**

```typescript
interface Result<T = unknown> {
  data: T;
  error?: string;
}

const result: Result = { data: "anything" };

if (typeof result.data === "string") {
  console.log(result.data.toUpperCase());
}
```

**✅ No default (best)**

```typescript
interface Result<T> {
  data: T;
  error?: string;
}

const result: Result<string> = { data: "specific type" };
console.log(result.data.toUpperCase());
```

---

## Example 3: Constraining Generic Parameters

**Example: Ensuring object has id**

```typescript
interface HasId {
  id: string;
}

function findById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

const users = [
  { id: "1", name: "Alice" },
  { id: "2", name: "Bob" }
];

const user = findById(users, "1");
```

**Example: Ensuring constructable type**

```typescript
interface Constructable<T> {
  new (...args: any[]): T;
}

function create<T>(Constructor: Constructable<T>): T {
  return new Constructor();
}

class User {
  name = "Anonymous";
}

const user = create(User);
```

**Example: Ensuring array element type**

```typescript
function firstElement<T>(arr: T[]): T | undefined {
  return arr[0];
}

const first = firstElement([1, 2, 3]);
const second = firstElement(["a", "b"]);
```

---

## Example 4: Multiple Type Parameters

**Example: Key-value mapping**

```typescript
function mapObject<T extends object, U>(
  obj: T,
  fn: (value: T[keyof T]) => U
): Record<keyof T, U> {
  const result = {} as Record<keyof T, U>;

  for (const key in obj) {
    result[key] = fn(obj[key]);
  }

  return result;
}

const user = { name: "Alice", age: 30 };
const lengths = mapObject(user, val => String(val).length);
```

**Example: Conditional return types**

```typescript
function parse<T extends "json" | "text">(
  response: Response,
  type: T
): T extends "json" ? Promise<unknown> : Promise<string> {
  if (type === "json") {
    return response.json() as any;
  }
  return response.text() as any;
}

const json = await parse(response, "json");
const text = await parse(response, "text");
```

---

## Example 5: Mapped Types

**Making properties optional:**

```typescript
type Partial<T> = {
  [P in keyof T]?: T[P];
};

const partialUser: Partial<User> = { name: "Alice" };
```

**Making properties readonly:**

```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
```

**Picking specific properties:**

```typescript
type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};

type UserPreview = Pick<User, "id" | "name">;
```

See `references/detailed-examples.md` for DeepPartial, FilterByType, and other complex mapped type patterns.

---

## Example 6: Conditional Types

**Unwrap promise type:**

```typescript
type Awaited<T> = T extends Promise<infer U> ? U : T;
```

**Extract function parameters:**

```typescript
type Parameters<T> = T extends (...args: infer P) => any ? P : never;
```

See `references/detailed-examples.md` for more conditional type patterns including FilterByType, nested promise unwrapping, and parameter extraction.
</examples>

<progressive-disclosure>
## Reference Files

**In this skill:**

- `references/detailed-examples.md` - DeepPartial, FilterByType, conditional types, constructables
- `references/common-patterns.md` - Array ops, object utils, Promise utils, builders
- `references/advanced-patterns.md` - Recursive generics, variadic tuples, branded types, HKTs

**Related skills:**

- Use the using-type-guards skill for narrowing generic types
- Use the avoiding-any-types skill for generic defaults
- Use the using-runtime-checks skill for validating generic data
</progressive-disclosure>

<constraints>
**MUST:**

- Use `extends` to constrain generic parameters when accessing properties
- Use `keyof T` for type-safe property access
- Use `unknown` for generic defaults if truly dynamic
- Specify return type based on generic parameters

**SHOULD:**

- Prefer no default over `any` default
- Use descriptive type parameter names for complex generics
- Infer type parameters from usage when possible
- Use helper types (Pick, Omit, Partial) over manual mapping

**NEVER:**

- Use `any` as generic default
- Access properties on unconstrained generics
- Use `as any` to bypass generic constraints
- Create overly complex nested generics (split into smaller types)
</constraints>

<patterns>
## Common Generic Patterns

### Array Operations

```typescript
function last<T>(arr: T[]): T | undefined {
  return arr[arr.length - 1];
}

function chunk<T>(arr: T[], size: number): T[][] {
  const chunks: T[][] = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
}
```

### Object Utilities

```typescript
function pick<T extends object, K extends keyof T>(
  obj: T,
  ...keys: K[]
): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}
```

### Class Generics

```typescript
class Container<T> {
  constructor(private value: T) {}

  map<U>(fn: (value: T) => U): Container<U> {
    return new Container(fn(this.value));
  }
}
```

See `references/common-patterns.md` for complete implementations including Promise utilities, builders, event emitters, and more.
</patterns>

<validation>
## Generic Type Safety Checklist

1. **Constraints**:
   - [ ] Generic parameters constrained when accessing properties
   - [ ] `keyof` used for property key types
   - [ ] `extends` used appropriately

2. **Defaults**:
   - [ ] No `any` defaults
   - [ ] `unknown` used for truly dynamic defaults
   - [ ] Or no default (require explicit type)

3. **Type Inference**:
   - [ ] Type parameters inferred from usage
   - [ ] Explicit types only when inference fails
   - [ ] Return types correctly derived from generics

4. **Complexity**:
   - [ ] Generic types are understandable
   - [ ] Complex types split into smaller pieces
   - [ ] Helper types used appropriately
</validation>

<advanced-patterns>
## Advanced Generic Patterns

For advanced patterns including:

- **Recursive Generics** (DeepReadonly, DeepPartial)
- **Variadic Tuple Types** (type-safe array concatenation)
- **Template Literal Types** (string manipulation at type level)
- **Branded Types** (nominal typing in structural system)
- **Distributive Conditional Types**
- **Higher-Kinded Types** (simulation)

See `references/advanced-patterns.md` for detailed implementations and examples.
</advanced-patterns>
