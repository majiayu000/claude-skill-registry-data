---
name: type-safety
description: Fixes TypeScript type safety issues including unsafe member access, assignments, returns, calls, and arguments. Use when encountering @typescript-eslint/no-unsafe-* errors or when working with unknown/any types.
---

# Type Safety Fixes

Fixes for TypeScript's strict type checking violations. These issues represent real runtime risks where the type system cannot guarantee correctness.

## Quick Start

1. Identify the unsafe operation type (member access, assignment, return, call, argument)
2. Trace the `any` or `unknown` type to its source
3. Apply the appropriate fix pattern from the workflows below
4. Verify with `npx tsc --noEmit`

## Priority

**P1 - Fix this week.** Unsafe type operations bypass TypeScript's guarantees and can cause runtime crashes.

## Workflows

### Unsafe Member Access (#2 - 316 occurrences)

**Detection**: `@typescript-eslint/no-unsafe-member-access`

**Pattern**: Accessing properties on `any` or `unknown` typed values.

```typescript
// PROBLEM
function processResponse(data: unknown) {
  const name = data.name; // Error: unsafe member access
}
```

**Fix Strategy**: Type guard with discriminated union.

```typescript
// SOLUTION
interface ApiResponse {
  name: string;
  id: number;
}

function isApiResponse(value: unknown): value is ApiResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'name' in value &&
    'id' in value &&
    typeof (value as ApiResponse).name === 'string' &&
    typeof (value as ApiResponse).id === 'number'
  );
}

function processResponse(data: unknown) {
  if (!isApiResponse(data)) {
    throw new Error('Invalid API response structure');
  }
  const name = data.name; // Now type-safe
}
```

**Why**: Type guards are reusable, self-documenting, and provide runtime validation. Better than `as` assertions because they verify shape at runtime.

---

### Unsafe Assignment (#3 - 251 occurrences)

**Detection**: `@typescript-eslint/no-unsafe-assignment`

**Pattern**: Assigning `any` typed value to a variable.

```typescript
// PROBLEM
const config = JSON.parse(fileContents); // any type
```

**Fix Strategy**: Parse with validation function.

```typescript
// SOLUTION
interface Config {
  port: number;
  host: string;
}

function parseConfig(raw: string): Config {
  const parsed: unknown = JSON.parse(raw);

  if (
    typeof parsed !== 'object' ||
    parsed === null ||
    typeof (parsed as Config).port !== 'number' ||
    typeof (parsed as Config).host !== 'string'
  ) {
    throw new Error('Invalid config structure');
  }

  return parsed as Config;
}

const config = parseConfig(fileContents); // Properly typed
```

**Why**: Explicit validation at parse boundaries catches errors early. Using `unknown` forces validation before use.

---

### Unsafe Return (#4 - 208 occurrences)

**Detection**: `@typescript-eslint/no-unsafe-return`

**Pattern**: Returning `any` typed value from a function.

```typescript
// PROBLEM
function getUser(id: string) {
  return database.query(`SELECT * FROM users WHERE id = ?`, [id]);
}
```

**Fix Strategy**: Add explicit return type annotation.

```typescript
// SOLUTION
interface User {
  id: string;
  name: string;
  email: string;
}

async function getUser(id: string): Promise<User | null> {
  const result = await database.query<User>(
    `SELECT * FROM users WHERE id = ?`,
    [id]
  );
  return result[0] ?? null;
}
```

**Why**: Return type annotations serve as documentation and catch type mismatches at function boundaries rather than call sites.

---

### Unsafe Call (#7 - 85 occurrences)

**Detection**: `@typescript-eslint/no-unsafe-call`

**Pattern**: Calling a function with `any` type.

```typescript
// PROBLEM
const handler = getHandler(eventType);
handler(event); // unsafe call
```

**Fix Strategy**: Type the function reference properly.

```typescript
// SOLUTION
type EventHandler = (event: Event) => void;

const handlerMap: Record<string, EventHandler> = {
  click: handleClick,
  submit: handleSubmit,
};

function getHandler(eventType: string): EventHandler | undefined {
  return handlerMap[eventType];
}

const handler = getHandler(eventType);
if (handler) {
  handler(event); // Now type-safe
}
```

**Why**: Function type aliases make callback signatures explicit and reusable.

---

### Unsafe Argument (#9 - 36 occurrences)

**Detection**: `@typescript-eslint/no-unsafe-argument`

**Pattern**: Passing `any` typed value as function argument.

```typescript
// PROBLEM
const data = JSON.parse(input);
processData(data); // unsafe argument
```

**Fix Strategy**: Validate at parse boundary.

```typescript
// SOLUTION
interface InputData {
  items: string[];
  count: number;
}

function parseInputData(raw: string): InputData {
  const parsed: unknown = JSON.parse(raw);
  // validation logic here
  return parsed as InputData;
}

const data = parseInputData(input);
processData(data); // Now safe
```

**Why**: Fix type at its source rather than at every call site. Centralizes validation.

---

### Any Type Usage (#14 - 25 occurrences)

**Detection**: Manual search for `: any` in source files.

**Fix Matrix**:

| Current Usage | Replacement |
|---------------|-------------|
| `any` for unknown data | `unknown` with type guards |
| `any` for flexible functions | Generic type parameter `<T>` |
| `any` for complex types | Proper interface definition |
| `any` to silence errors | Fix underlying type issue |

```typescript
// PROBLEM - any for flexibility
function clone(obj: any): any {
  return JSON.parse(JSON.stringify(obj));
}

// SOLUTION - generic
function clone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj)) as T;
}
```

```typescript
// PROBLEM - any for unknown API response
const response: any = await fetch(url);

// SOLUTION - unknown with validation
const response: unknown = await fetch(url).then(r => r.json());
if (!isValidResponse(response)) {
  throw new Error('Invalid response');
}
```

**Why**: `any` disables type checking entirely. `unknown` is the type-safe alternative.

---

### Unsafe Template Expressions (#17 - 6 occurrences)

**Detection**: `@typescript-eslint/restrict-template-expressions`

**Pattern**: Using non-string types in template literals.

```typescript
// PROBLEM
const message = `User: ${user}`;  // user might be object
```

**Fix Options**:

```typescript
// Explicit string conversion
const message = `User: ${String(user.name)}`;

// With type guard
const message = `User: ${user?.name ?? 'Unknown'}`;

// JSON for objects
const debugMessage = `Data: ${JSON.stringify(data, null, 2)}`;
```

**Why**: Template literals call `toString()` implicitly, producing `[object Object]` for objects.

---

## Scripts

### Detect Type Safety Issues

Run the detection script to find all type safety issues in your codebase:

```bash
# From skill directory
node scripts/detect-type-issues.js /path/to/src
```

Output: JSON report of all unsafe operations with file locations and fix suggestions.

### Generate Type Guard

Generate a type guard function for a given interface:

```bash
node scripts/generate-type-guard.js --interface "User" --file /path/to/types.ts
```

---

## Type Guard Templates

### Simple Object Guard

```typescript
function isTypeName(value: unknown): value is TypeName {
  return (
    typeof value === 'object' &&
    value !== null &&
    'requiredProp' in value &&
    typeof (value as TypeName).requiredProp === 'expected-type'
  );
}
```

### Array Guard

```typescript
function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every(item => typeof item === 'string');
}
```

### Union Guard

```typescript
type Status = 'pending' | 'active' | 'completed';

function isStatus(value: unknown): value is Status {
  return value === 'pending' || value === 'active' || value === 'completed';
}
```

### Nested Object Guard

```typescript
interface Order {
  id: string;
  items: OrderItem[];
  customer: Customer;
}

function isOrder(value: unknown): value is Order {
  if (typeof value !== 'object' || value === null) return false;
  const obj = value as Record<string, unknown>;
  return (
    typeof obj.id === 'string' &&
    Array.isArray(obj.items) &&
    obj.items.every(isOrderItem) &&
    isCustomer(obj.customer)
  );
}
```

---

## Validation Library Integration

For complex validation, consider using Zod:

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

type User = z.infer<typeof UserSchema>;

function parseUser(data: unknown): User {
  return UserSchema.parse(data);
}
```

**When to use Zod vs manual type guards**:
- Manual: Simple shapes, no dependencies needed
- Zod: Complex validation rules, multiple schemas, runtime validation requirements

---

## Common Sources of `any`

1. **JSON.parse()** - Always returns `any`
2. **External library types** - Some libraries have poor typing
3. **Event handlers** - DOM events often have `any` targets
4. **Dynamic property access** - `obj[key]` can produce `any`
5. **Type assertion failures** - When `as unknown as T` is used

Fix these at the source to prevent propagation through the codebase.
