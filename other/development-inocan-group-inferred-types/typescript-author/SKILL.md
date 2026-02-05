---
name: typescript-author
description: Write TypeScript for Web Components and Node.js with strict typing. Use when adding types to JavaScript projects, building type-safe APIs, or creating generic utilities.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# TypeScript Authoring Skill

Write strictly-typed TypeScript extending javascript-author patterns.

## Core Principles

| Principle | Description |
|-----------|-------------|
| Strict Mode | Always use strict TypeScript configuration |
| Explicit Types | Prefer explicit over inferred types at boundaries |
| Narrow Types | Use unions, discriminated unions, and type guards |
| Functional Core | Same as JavaScript: pure functions, no side effects |
| Named Exports | Same as JavaScript: no default exports |

## Configuration

### Strict tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,

    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    "outDir": "dist",
    "rootDir": "src",

    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Key Strict Options

| Option | Purpose |
|--------|---------|
| `strict` | Enables all strict checks |
| `noUncheckedIndexedAccess` | Array/object access returns `T \| undefined` |
| `noImplicitOverride` | Requires `override` keyword |
| `exactOptionalPropertyTypes` | `?:` means missing, not undefined |

## Type Patterns

### Interface vs Type

```typescript
// Use interface for object shapes (extendable)
interface User {
  id: string;
  name: string;
  email: string;
}

// Use type for unions, primitives, computed types
type UserId = string;
type Status = 'pending' | 'active' | 'inactive';
type UserWithStatus = User & { status: Status };
```

### Discriminated Unions

```typescript
// Pattern: Use 'type' or 'kind' discriminator
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };

type ApiResponse =
  | { type: 'loading' }
  | { type: 'success'; data: unknown }
  | { type: 'error'; message: string };

function handleResponse(response: ApiResponse): void {
  switch (response.type) {
    case 'loading':
      showSpinner();
      break;
    case 'success':
      render(response.data); // TypeScript knows data exists
      break;
    case 'error':
      showError(response.message); // TypeScript knows message exists
      break;
  }
}
```

### Type Guards

```typescript
// User-defined type guard
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    'email' in value
  );
}

// Assertion function
function assertUser(value: unknown): asserts value is User {
  if (!isUser(value)) {
    throw new TypeError('Expected User object');
  }
}

// Usage
function processInput(input: unknown): User {
  assertUser(input);
  return input; // Type narrowed to User
}
```

### Generics

```typescript
// Basic generic function
function first<T>(array: T[]): T | undefined {
  return array[0];
}

// Constrained generic
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic with default
function createStore<T = Record<string, unknown>>(
  initial: T
): { get(): T; set(value: T): void } {
  let state = initial;
  return {
    get: () => state,
    set: (value) => { state = value; }
  };
}
```

## Web Component Types

### Typed Custom Element

```typescript
// types.ts
interface MyComponentProps {
  value: string;
  disabled?: boolean;
}

interface MyComponentEvents {
  'value-change': CustomEvent<{ oldValue: string; newValue: string }>;
  'submit': CustomEvent<void>;
}

// my-component.ts
class MyComponent extends HTMLElement {
  static observedAttributes = ['value', 'disabled'] as const;

  // Private state
  #value = '';

  // Typed getter/setter
  get value(): string {
    return this.#value;
  }

  set value(newValue: string) {
    const oldValue = this.#value;
    this.#value = newValue;
    this.dispatchEvent(
      new CustomEvent('value-change', {
        detail: { oldValue, newValue },
        bubbles: true
      })
    );
  }

  get disabled(): boolean {
    return this.hasAttribute('disabled');
  }

  set disabled(value: boolean) {
    this.toggleAttribute('disabled', value);
  }

  // Typed attribute callback
  attributeChangedCallback(
    name: typeof MyComponent.observedAttributes[number],
    oldValue: string | null,
    newValue: string | null
  ): void {
    if (oldValue === newValue) return;

    switch (name) {
      case 'value':
        this.#value = newValue ?? '';
        break;
      case 'disabled':
        // Handle disabled state
        break;
    }
  }

  // Typed event emission
  #emit<K extends keyof MyComponentEvents>(
    type: K,
    detail: MyComponentEvents[K]['detail']
  ): void {
    this.dispatchEvent(new CustomEvent(type, { detail, bubbles: true }));
  }
}

customElements.define('my-component', MyComponent);

export { MyComponent };
export type { MyComponentProps, MyComponentEvents };
```

### Augmenting HTMLElementTagNameMap

```typescript
// global.d.ts
declare global {
  interface HTMLElementTagNameMap {
    'my-component': MyComponent;
    'user-card': UserCard;
  }
}

export {};

// Usage - now type-safe
const element = document.querySelector('my-component');
// element is MyComponent | null, not Element | null
```

## API Types

### Request/Response Types

```typescript
// api-types.ts
interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}

type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: ApiError };

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

// Typed fetch wrapper
async function apiFetch<T>(
  url: string,
  options?: RequestInit
): Promise<ApiResult<T>> {
  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      const error = await response.json() as ApiError;
      return { ok: false, error };
    }

    const data = await response.json() as T;
    return { ok: true, data };
  } catch (cause) {
    return {
      ok: false,
      error: {
        code: 'NETWORK_ERROR',
        message: cause instanceof Error ? cause.message : 'Unknown error'
      }
    };
  }
}
```

### Zod for Runtime Validation

```typescript
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.coerce.date()
});

// Infer type from schema
type User = z.infer<typeof UserSchema>;

// Parse with runtime validation
function parseUser(input: unknown): User {
  return UserSchema.parse(input);
}

// Safe parse (returns result object)
function safeParseUser(input: unknown): z.SafeParseReturnType<unknown, User> {
  return UserSchema.safeParse(input);
}
```

## Utility Types

### Common Built-in Types

```typescript
// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Pick - select properties
type UserName = Pick<User, 'id' | 'name'>;

// Omit - exclude properties
type UserWithoutEmail = Omit<User, 'email'>;

// Record - object type
type UserMap = Record<string, User>;

// ReturnType - function return type
type FetchResult = ReturnType<typeof fetch>;

// Parameters - function parameters
type FetchParams = Parameters<typeof fetch>;

// Awaited - unwrap Promise
type ResolvedData = Awaited<Promise<User>>;
```

### Custom Utility Types

```typescript
// Make specific properties optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Make specific properties required
type RequiredBy<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Deep partial
type DeepPartial<T> = T extends object
  ? { [P in keyof T]?: DeepPartial<T[P]> }
  : T;

// Non-nullable
type NonNullableProps<T> = {
  [P in keyof T]: NonNullable<T[P]>;
};

// Extract keys by value type
type KeysOfType<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never;
}[keyof T];
```

## File Organization

```
src/
├── types/
│   ├── index.ts          # Re-exports all types
│   ├── api.ts            # API request/response types
│   ├── domain.ts         # Business domain types
│   └── components.ts     # Component prop/event types
├── components/
│   └── my-component/
│       ├── my-component.ts
│       ├── my-component.types.ts  # Component-specific types
│       └── my-component.test.ts
├── utils/
│   ├── type-guards.ts    # isX and assertX functions
│   └── validators.ts     # Zod schemas
└── index.ts
```

## Best Practices

### Do

```typescript
// Explicit return types on public functions
function calculateTotal(items: LineItem[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Use const assertions for literals
const STATUSES = ['pending', 'active', 'closed'] as const;
type Status = typeof STATUSES[number];

// Prefer unknown over any
function parseJSON(text: string): unknown {
  return JSON.parse(text);
}

// Use satisfies for type checking without widening
const config = {
  port: 3000,
  host: 'localhost'
} satisfies Record<string, string | number>;
```

### Don't

```typescript
// Don't use any
function bad(data: any) { } // Avoid

// Don't use non-null assertion without cause
const element = document.querySelector('#app')!; // Dangerous

// Don't use type assertions carelessly
const user = response as User; // Prefer type guards

// Don't ignore errors in catch
try {
  // ...
} catch (e) { } // Always handle or log
```

## Checklist

When writing TypeScript:

- [ ] tsconfig.json has strict mode enabled
- [ ] All exports are named (no default exports)
- [ ] Public function boundaries have explicit types
- [ ] Unknown data is validated before use
- [ ] Type guards used instead of type assertions
- [ ] Discriminated unions for state management
- [ ] No `any` types (use `unknown` instead)

## Related Skills

- **javascript-author** - Base patterns for functional core
- **unit-testing** - Testing typed code
- **api-client** - Typed API interactions
- **custom-elements** - Web Component patterns
