---
name: "typescript-patterns"
description: "TypeScript utility types and type-safe API design patterns. Use when designing type systems, creating utility types, or implementing type-safe patterns."
---

# TypeScript Type Design Patterns

## Utility Type Patterns

### Built-in Utilities (Quick Reference)

```typescript
// Selection
Pick<User, 'id' | 'name'>      // Select specific fields
Omit<User, 'password'>          // Exclude specific fields

// Modification
Partial<User>                   // All optional
Required<User>                  // All required
Readonly<User>                  // All readonly

// Mapping
Record<string, User>            // Object with User values

// Union manipulation
Exclude<'a' | 'b' | 'c', 'a'>  // 'b' | 'c'
Extract<'a' | 'b', 'a' | 'c'>  // 'a'
NonNullable<T | null>           // T

// Function utilities
ReturnType<typeof fn>           // Extract return type
Parameters<typeof fn>           // Extract parameter types
```

### Custom Utility Types

**Make specific fields optional:**
```typescript
type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

type UserUpdate = Optional<User, 'email' | 'avatar'>;
```

**Deep Partial:**
```typescript
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

**Nullable:**
```typescript
type Nullable<T> = T | null;
```

## Discriminated Unions

### Pattern

```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function handle<T>(result: Result<T>) {
  if (result.success) {
    // TypeScript knows result.data exists
    console.log(result.data);
  } else {
    // TypeScript knows result.error exists
    console.log(result.error);
  }
}
```

**Critical**: Discriminant must be a literal type (`true`, `'loading'`, etc.).

### API Response Pattern

```typescript
type ApiResponse<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };
```

## Generic Type Design

### Constraints

```typescript
// Constrain to objects with specific properties
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Constrain to specific shape
function processEntity<T extends { id: string }>(entity: T) {
  return entity.id;
}

// Multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

### Default Type Parameters

```typescript
interface ApiResponse<T = unknown> {
  data: T;
  status: number;
}

// Can omit type parameter
const response: ApiResponse = { data: "anything", status: 200 };

// Or provide specific type
const typed: ApiResponse<User> = { data: user, status: 200 };
```

## Type Guards

### Custom Type Guards

```typescript
interface User {
  type: 'user';
  name: string;
}

interface Admin {
  type: 'admin';
  name: string;
  permissions: string[];
}

// Type predicate
function isAdmin(user: User | Admin): user is Admin {
  return user.type === 'admin';
}

// Usage
if (isAdmin(user)) {
  // TypeScript knows user is Admin
  console.log(user.permissions);
}
```

### Assertion Functions

```typescript
function assertIsDefined<T>(value: T): asserts value is NonNullable<T> {
  if (value === null || value === undefined) {
    throw new Error('Value is null or undefined');
  }
}

function process(value: string | null) {
  assertIsDefined(value);
  // TypeScript knows value is string here
  return value.toUpperCase();
}
```

## Conditional Types

### Basic Pattern

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false
```

### Extract Return Type

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() {
  return { id: '1', name: 'Alice' };
}

type User = ReturnType<typeof getUser>;  // { id: string; name: string }
```

### Unwrap Promise

```typescript
type Unwrap<T> = T extends Promise<infer U> ? U : T;

type Result = Unwrap<Promise<string>>;  // string
type Direct = Unwrap<number>;           // number
```

## Mapped Types

### Transform Properties

```typescript
// Make all properties optional
type Optional<T> = {
  [P in keyof T]?: T[P];
};

// Make all properties readonly
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

// Transform all to string
type Stringify<T> = {
  [P in keyof T]: string;
};
```

### Conditional Property Types

```typescript
// Make all properties nullable
type Nullable<T> = {
  [P in keyof T]: T[P] | null;
};
```

## Template Literal Types

### String Manipulation

```typescript
// Capitalize
type Greeting = `Hello ${string}`;

// Event names
type EventName = 'click' | 'hover' | 'focus';
type Handler = `on${Capitalize<EventName>}`;
// 'onClick' | 'onHover' | 'onFocus'

// Combine literals
type Color = 'red' | 'blue';
type Size = 'sm' | 'lg';
type Variant = `${Color}-${Size}`;
// 'red-sm' | 'red-lg' | 'blue-sm' | 'blue-lg'
```

## Type-Safe Event Emitters

```typescript
type EventMap = {
  'user:login': { userId: string; timestamp: Date };
  'user:logout': { userId: string };
  'data:update': { id: string; data: unknown };
};

class TypedEmitter {
  on<K extends keyof EventMap>(
    event: K,
    handler: (data: EventMap[K]) => void
  ): void {
    // Implementation
  }

  emit<K extends keyof EventMap>(
    event: K,
    data: EventMap[K]
  ): void {
    // Implementation
  }
}

// Usage is fully type-safe
const emitter = new TypedEmitter();
emitter.on('user:login', (data) => {
  // data is typed as { userId: string; timestamp: Date }
  console.log(data.userId);
});
```

## Branded Types

Create distinct types from same primitive:

```typescript
type UserId = string & { readonly __brand: 'UserId' };
type ProductId = string & { readonly __brand: 'ProductId' };

function createUserId(id: string): UserId {
  return id as UserId;
}

function getUser(id: UserId) { /* ... */ }

const userId = createUserId('user-123');
const productId = 'product-456' as ProductId;

// This is a type error:
// getUser(productId);  // ProductId is not assignable to UserId
```

**Use when**: Need to distinguish same-typed values (IDs, tokens, etc.).

## Interface vs Type

**Use Interface for:**
- Object shapes
- When extension is expected
- Class contracts

**Use Type for:**
- Unions
- Tuples
- Complex computed types
- When using utility types

```typescript
// Interface - extensible
interface User {
  id: string;
  name: string;
}

interface Admin extends User {
  role: 'admin';
}

// Type - unions
type Status = 'idle' | 'loading' | 'success' | 'error';

type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };
```

## tsconfig.json Essential Settings

```json
{
  "compilerOptions": {
    // Strict type checking
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,

    // Module resolution
    "moduleResolution": "bundler",
    "module": "ESNext",
    "target": "ES2022",

    // Emit
    "declaration": true,
    "sourceMap": true,

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,

    // Performance
    "skipLibCheck": true,

    // Path mapping
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

**Always enable**: `strict`, `noUncheckedIndexedAccess`, `forceConsistentCasingInFileNames`

## Best Practices

### 1. Avoid `any`

```typescript
// Bad
function process(data: any) {
  return data.value;
}

// Good - use proper types
function process(data: { value: string }) {
  return data.value;
}

// Good - use unknown for truly unknown
function parse(json: string): unknown {
  return JSON.parse(json);
}
```

### 2. Use `const` Assertions

```typescript
// Instead of
const colors = ['red', 'blue']; // string[]

// Use const assertion
const colors = ['red', 'blue'] as const; // readonly ['red', 'blue']

// For objects
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
```

### 3. Prefer Union Types Over Enums

```typescript
// Instead of enum
enum Status {
  Idle = 'idle',
  Loading = 'loading',
}

// Prefer union type
type Status = 'idle' | 'loading' | 'success' | 'error';
```

**Why**: Simpler, more flexible, better tree-shaking.

### 4. Use `readonly` for Immutability

```typescript
interface User {
  readonly id: string;
  name: string;
}

function processItems(items: readonly string[]) {
  // Cannot mutate items
  return items.join(',');
}
```

### 5. Type Narrowing

```typescript
function process(value: string | number | null) {
  // Null check
  if (value === null) return 'null';

  // typeof check
  if (typeof value === 'string') {
    return value.toUpperCase();
  }

  // TypeScript knows value is number here
  return value.toFixed(2);
}
```

## Common Pitfalls

**Type assertions (`as`)** - Use sparingly:
```typescript
// Avoid when possible
const user = data as User;

// Better: Validate at runtime
if (isUser(data)) {
  // data is User here
}
```

**Non-null assertion (`!`)** - Dangerous:
```typescript
// Avoid
const user = getUser()!;

// Better: Handle null
const user = getUser();
if (user) {
  // Use user safely
}
```

**Empty object type `{}`** - Too permissive:
```typescript
// Bad
const config: {} = 'anything';

// Good
const config: object = { key: 'value' };
const settings: Record<string, unknown> = { key: 'value' };
```

## Type Design Checklist

When designing types:
- [ ] Use strict mode
- [ ] Avoid `any` - use `unknown` or proper types
- [ ] Use discriminated unions for state
- [ ] Use const assertions for literal types
- [ ] Prefer interfaces for objects, types for unions
- [ ] Use readonly where appropriate
- [ ] Provide good error messages (use descriptive types)
- [ ] Consider future extension needs
