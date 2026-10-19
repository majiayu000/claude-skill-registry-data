---
name: typescript-development
description: >
  Architect, implement, and review type-safe TypeScript applications under strict
  mode. Use when defining discriminated unions, writing reusable generics and
  type guards, configuring tsconfig.json, modeling domain types without any/unknown
  leaks, or validating external schemas with Zod or Typebox.
compatibility: >
  Agent Skills-compatible coding agents operating on TypeScript 5.0+ codebases.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "typescript, types, generics, discriminated-unions, tsconfig, strict"
  topics: "programming-languages, software-development"
---

# Strict TypeScript Development

TypeScript provides static typing over JavaScript, catching type errors before code runs. Writing production-grade TypeScript requires strict compiler settings, rigorous domain modeling with discriminated unions, avoiding `any`, and leveraging type narrowing and user-defined type guards.

## Core Rules

1. **Always enable `strict: true`**: Never disable strict mode. Key flags (`noImplicitAny`, `strictNullChecks`, `noImplicitReturns`) must remain active.
2. **Never use `any`**: Use `unknown` for unvalidated external input and narrow with type guards or schema validators (Zod/TypeBox).
3. **Make illegal states unrepresentable**: Use **Discriminated Unions** instead of optional properties to model distinct entity states.
4. **Prefer `type` for unions/aliases and `interface` for object models**: Be consistent with team standards.
5. **Enforce `const` assertions where appropriate**: Use `as const` for literals, configurations, and tuple definitions.
6. **Avoid type assertions (`as Type`)**: Type assertions bypass compiler checks. Prefer type narrowing via `isinstance`, `typeof`, or user-defined type guards (`is`).

---

## 1. Domain Modeling: Discriminated Unions

Avoid bag-of-optionals objects where invalid combinations are possible:

```typescript
// ANTI-PATTERN: Can have error and data simultaneously, or status='success' with no data:
interface BadApiResponse {
  status: 'loading' | 'success' | 'error';
  data?: User;
  error?: string;
}

// CORRECT: Discriminated Union
export type ApiResponse<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T; timestamp: number }
  | { status: 'error'; error: Error; retryCount: number };

export function renderResponse<T>(res: ApiResponse<T>): string {
  switch (res.status) {
    case 'idle':
      return 'Waiting to start...';
    case 'loading':
      return 'Loading...';
    case 'success':
      // TypeScript automatically narrows res to the success variant!
      return `Loaded data at ${res.timestamp}`;
    case 'error':
      return `Failed: ${res.error.message} (retries: ${res.retryCount})`;
  }
}
```

---

## 2. Type Narrowing and User-Defined Type Guards

When dealing with `unknown` inputs from network requests or user events:

```typescript
export interface UserAccount {
  id: string;
  email: string;
  roles: readonly string[];
}

// User-defined type guard: arg is UserAccount
export function isUserAccount(value: unknown): value is UserAccount {
  if (typeof value !== 'object' || value === null) {
    return false;
  }

  const candidate = value as Record<string, unknown>;
  return (
    typeof candidate.id === 'string' &&
    typeof candidate.email === 'string' &&
    Array.isArray(candidate.roles) &&
    candidate.roles.every(r => typeof r === 'string')
  );
}

// In application code:
export function processPayload(raw: unknown): string {
  if (isUserAccount(raw)) {
    // Safely access raw.email and raw.roles with full type-safety
    return raw.email.toLowerCase();
  }
  throw new TypeError('Invalid user payload structure');
}
```

---

## 3. Reusable Generics and Utility Types

```typescript
// Generic Repository pattern
export interface Entity {
  readonly id: string;
}

export interface CrudRepository<T extends Entity> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<void>;
  update(id: string, updates: Partial<Omit<T, 'id'>>): Promise<T>;
}

// Immutability utility: DeepReadonly
export type DeepReadonly<T> = T extends Function | boolean | number | string | null | undefined
  ? T
  : T extends Array<infer U>
  ? ReadonlyArray<DeepReadonly<U>>
  : { readonly [K in keyof T]: DeepReadonly<T[K]> };
```

---

## 4. Recommended `tsconfig.json` Configuration

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| `as unknown as TargetType` | Masks type mismatches; leads to runtime crashes | Use validation library (Zod) or explicit type guard |
| Optional properties for mutually exclusive states | Leaves room for invalid combinations | Use Discriminated Unions |
| Blindly ignoring `null` with non-null assertion (`!`) | Crashes at runtime with `Cannot read properties of null` | Handle null with `if (val != null)` or optional chaining `?.` |
| Using `Function` or `{}` as types | Loses argument checking or accepts anything except null/undefined | Use explicit signatures `() => void` or `Record<string, unknown>` |

---

## 6. Verification Checklist

- [ ] `tsc --noEmit` succeeds with 0 errors under `strict: true`.
- [ ] No `any` types in newly authored code (`unknown` used for unverified data).
- [ ] Non-null assertions (`!`) are eliminated or justified by provable invariants.
- [ ] Discriminated unions used for multi-state domain logic.
- [ ] ESLint TypeScript rules (`@typescript-eslint/recommended-type-checked`) pass.
