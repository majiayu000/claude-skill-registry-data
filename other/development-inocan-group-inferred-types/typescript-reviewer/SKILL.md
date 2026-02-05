---
name: typescript-reviewer
description: |
  WHEN: TypeScript code review, type safety audit, tsconfig analysis, TS migration review
  WHAT: Type safety checks + any usage audit + generic patterns + strict mode + compiler options analysis
  WHEN NOT: React specific → nextjs-reviewer, Node.js backend → nodejs-reviewer, General code → code-reviewer
---

# TypeScript Reviewer Skill

## Purpose
Reviews TypeScript code for type safety, best practices, and idiomatic patterns. Identifies `any` abuse, missing type annotations, and unsafe type operations.

## When to Use
- TypeScript code review requests
- "Type safety", "any audit", "TS patterns" mentions
- TypeScript migration review
- tsconfig.json optimization
- Projects with `tsconfig.json` or `.ts`/`.tsx` files

## Project Detection
- `tsconfig.json` present
- `.ts` or `.tsx` files
- `typescript` in package.json dependencies
- `@types/*` packages in devDependencies

## Workflow

### Step 1: Analyze Project
```
**TypeScript**: 5.x
**Target**: ES2022
**Module**: ESNext
**Strict Mode**: ✓ enabled
**Key Flags**: strictNullChecks, noImplicitAny
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which TypeScript areas to review?"
Options:
- Full type safety audit (recommended)
- any/unknown usage
- Generic patterns
- Type assertions
- Compiler options
multiSelect: true
```

## Detection Rules

### Critical: Type Safety Bypasses
| Pattern | Issue | Severity |
|---------|-------|----------|
| Explicit `any` | Bypasses type system | CRITICAL |
| `as any` casting | Type escape hatch | CRITICAL |
| `// @ts-ignore` | Silences all errors | CRITICAL |
| `// @ts-nocheck` | Disables file checking | CRITICAL |
| `any[]` array | Untyped collections | HIGH |
| Function returns `any` | Propagates unsafety | HIGH |
| `Promise<any>` | Async unsafety | HIGH |
| `Function` type | Too broad | HIGH |
| `Object` / `{}` type | Almost anything | HIGH |
| `Record<string, any>` | Indexed unsafety | HIGH |

```typescript
// BAD: Explicit any
function process(data: any): any {
  return data.value;  // No type safety
}

// GOOD: Proper typing
function process<T extends { value: V }, V>(data: T): V {
  return data.value;
}

// BAD: any array
const items: any[] = [];

// GOOD: Typed array
const items: Item[] = [];
// or if truly dynamic:
const items: unknown[] = [];

// BAD: @ts-ignore without justification
// @ts-ignore
const value = unsafeOperation();

// ACCEPTABLE: @ts-expect-error with justification
// @ts-expect-error - Legacy API returns wrong type, tracked in JIRA-123
const legacyValue = legacyApi.call();

// BAD: Broad types
const handler: Function = () => {};
const data: Object = {};
const config: Record<string, any> = {};

// GOOD: Specific types
const handler: () => void = () => {};
const data: Record<string, unknown> = {};
const config: AppConfig = {};
```

### High: Type Assertions (`as`) and External Data
| Pattern | Issue | Severity |
|---------|-------|----------|
| `as Type` on external data | No runtime validation | CRITICAL |
| `as unknown as Type` | Double assertion | HIGH |
| `as Type` on internal data | Unsafe assumption | MEDIUM |
| `<Type>value` (JSX conflict) | Legacy syntax | LOW |
| `!` non-null assertion | Runtime error risk | HIGH |
| `!` after guard/assertion | Acceptable | OK |

```typescript
// BAD: Blind assertion
const user = data as User;

// GOOD: Type guard first
function isUser(data: unknown): data is User {
  return typeof data === 'object' && data !== null && 'id' in data;
}
if (isUser(data)) {
  const user = data;  // Narrowed to User
}

// BAD: Non-null assertion
const name = user.profile!.name!;

// GOOD: Optional chaining with default
const name = user.profile?.name ?? 'Anonymous';

// BAD: Double assertion
const value = data as unknown as SpecificType;

// GOOD: Proper validation
function validate(data: unknown): SpecificType {
  if (!isSpecificType(data)) throw new Error('Invalid data');
  return data;
}

// CRITICAL: External data must be validated
// BAD: API response without validation
const user = await fetch('/api/user').then(r => r.json()) as User;

// GOOD: Validate external data with schema
import { z } from 'zod';
const UserSchema = z.object({ id: z.string(), name: z.string() });
const user = UserSchema.parse(await fetch('/api/user').then(r => r.json()));

// ACCEPTABLE: ! after explicit check
function process(items: Item[]) {
  const first = items.find(i => i.active);
  if (!first) throw new Error('No active item');
  return first.value;  // Safe - we just checked
}
```

### Medium: Missing Return Types
| Pattern | Issue | Severity |
|---------|-------|----------|
| No function return type | Inferred may be wrong | MEDIUM |
| Public API without types | Poor documentation | HIGH |
| Async without Promise<T> | Return type unclear | MEDIUM |

```typescript
// BAD: Missing return type
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// GOOD: Explicit return type
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// BAD: Async without type
async function fetchUser(id) {
  return await api.get(`/users/${id}`);
}

// GOOD: Typed async
async function fetchUser(id: string): Promise<User> {
  return await api.get<User>(`/users/${id}`);
}
```

### Medium: Generic Constraints
| Pattern | Issue | Severity |
|---------|-------|----------|
| Unconstrained generics | Too permissive | MEDIUM |
| `T extends any` | Useless constraint | LOW |
| Missing defaults | Poor ergonomics | LOW |

```typescript
// BAD: Unconstrained generic
function getValue<T>(obj: T, key: string) {
  return obj[key];  // Error: Type 'string' cannot be used to index type 'T'
}

// GOOD: Constrained generic
function getValue<T extends Record<string, unknown>, K extends keyof T>(
  obj: T,
  key: K
): T[K] {
  return obj[key];
}

// BAD: No default
interface Props<T> {
  data: T;
}

// GOOD: With default
interface Props<T = unknown> {
  data: T;
}
```

### Low: Type vs Interface
| Pattern | Recommendation | Severity |
|---------|----------------|----------|
| Inconsistent usage | Pick one convention | LOW |
| Type for object shapes | Consider interface | LOW |
| Interface for union | Use type alias | LOW |

```typescript
// Interface: Object shapes, extendable
interface User {
  id: string;
  name: string;
}

interface Admin extends User {
  permissions: string[];
}

// Type: Unions, intersections, primitives
type Status = 'active' | 'inactive' | 'pending';
type UserOrAdmin = User | Admin;
type Point = { x: number; y: number };
```

### tsconfig.json Review
| Option | Recommended | Severity |
|--------|-------------|----------|
| `strict: false` | Enable strict mode | CRITICAL |
| `noImplicitAny: false` | Enable | HIGH |
| `strictNullChecks: false` | Enable | HIGH |
| `useUnknownInCatchVariables: false` | Enable (catch as unknown) | HIGH |
| `noImplicitReturns: false` | Enable | HIGH |
| `forceConsistentCasingInFileNames: false` | Enable (cross-platform) | HIGH |
| `noUncheckedIndexedAccess: false` | Consider enabling | MEDIUM |
| `noFallthroughCasesInSwitch: false` | Enable | MEDIUM |
| `noImplicitOverride: false` | Enable for OOP | MEDIUM |
| `exactOptionalPropertyTypes: false` | Consider for libraries | LOW |
| `skipLibCheck: true` (for libs) | Set false for libraries | MEDIUM |

**Library-specific options:**
| Option | Recommended | Purpose |
|--------|-------------|---------|
| `declaration: true` | Required | Generate .d.ts |
| `declarationMap: true` | Recommended | Source maps for types |
| `composite: true` | For monorepos | Project references |

```json
// RECOMMENDED tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Utility Types Usage
| Pattern | Better Alternative | Severity |
|---------|-------------------|----------|
| Manual partial | `Partial<T>` | LOW |
| Manual readonly | `Readonly<T>` | LOW |
| Manual pick | `Pick<T, K>` | LOW |
| Manual omit | `Omit<T, K>` | LOW |

```typescript
// BAD: Manual partial
interface UpdateUserInput {
  name?: string;
  email?: string;
  age?: number;
}

// GOOD: Utility type
type UpdateUserInput = Partial<User>;

// BAD: Manual readonly
interface Config {
  readonly host: string;
  readonly port: number;
}

// GOOD: Utility type
type Config = Readonly<{
  host: string;
  port: number;
}>;

// Useful patterns
type CreateInput = Omit<User, 'id' | 'createdAt'>;
type PublicUser = Pick<User, 'id' | 'name'>;
type NonNullableUser = Required<User>;
```

## Response Template
```
## TypeScript Review Results

**Project**: [name]
**TypeScript**: 5.x | **Target**: ES2022
**Strict Mode**: [enabled/disabled]

### Type Safety Issues

#### CRITICAL
| File | Line | Issue |
|------|------|-------|
| api.ts | 45 | strict mode disabled in tsconfig |

#### HIGH
| File | Line | Issue |
|------|------|-------|
| utils.ts | 23 | `as any` type assertion |
| service.ts | 67 | Non-null assertion `!` on optional |

#### MEDIUM
| File | Line | Issue |
|------|------|-------|
| handlers.ts | 12 | Missing return type on exported function |
| models.ts | 34 | Implicit `any` in callback |

### any Usage Audit
- **Explicit any**: 5 occurrences
- **as any**: 3 occurrences
- **Implicit any**: 2 occurrences
- **Total**: 10 (recommend: 0)

### Recommendations
1. [ ] Enable strict mode in tsconfig.json
2. [ ] Replace `any` with `unknown` + type guards
3. [ ] Add return types to public API functions
4. [ ] Remove non-null assertions, use optional chaining

### Positive Patterns
- Good use of generics in `Repository<T>`
- Proper discriminated unions in `Result<T, E>`
```

## Best Practices
1. **Strict Mode**: Always enable for new projects
2. **`unknown` over `any`**: Use `unknown` for truly dynamic data
3. **Type Guards**: Custom type guards over assertions
4. **Branded Types**: For type-safe IDs
5. **Const Assertions**: `as const` for literal types
6. **Template Literal Types**: For string patterns

```typescript
// Branded types for IDs
type UserId = string & { readonly brand: unique symbol };
type PostId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId;
}

// Now type-safe:
function getUser(id: UserId): User { ... }
// getUser(postId);  // Error!
```

## Integration
- `code-reviewer` skill: General quality
- `nextjs-reviewer` skill: React/Next.js specifics
- `security-scanner` skill: Security audit

## Notes
- Based on TypeScript 5.x best practices
- Focuses on type safety over runtime
- Respects existing project conventions
- Compatible with JSX/TSX files
