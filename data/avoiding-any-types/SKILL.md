---
name: avoiding-any-types
description: Teaches when and how to use unknown instead of any type in TypeScript. Use when working with TypeScript code that has any types, needs type safety, handling external data, or when designing APIs. Critical for preventing type safety violations.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
version: 1.0.0
---

<role>
This skill teaches how to eliminate `any` type abuse in TypeScript by using `unknown` with proper type guards. Based on stress test findings where 83% of AI agents overused `any`, defeating TypeScript's purpose.
</role>

<when-to-activate>
This skill activates when:

- Code contains `any` type annotations
- Working with external data (APIs, JSON, user input)
- Designing generic functions or types
- User mentions type safety, type checking, or avoiding `any`
- Files contain patterns like `: any`, `<any>`, `as any`
</when-to-activate>

<overview>
The `any` type is TypeScript's escape hatch that disables all type checking. While sometimes necessary, overusing `any` defeats TypeScript's purpose and allows runtime errors TypeScript should prevent.

The `unknown` type is `any`'s type-safe counterpart. It accepts any value like `any`, but requires type narrowing before use.

**Key Pattern**: `any` → `unknown` → type guard → safe access

**Impact**: Prevents runtime errors while maintaining flexibility for truly dynamic data.
</overview>

<workflow>
## Decision Flow

**Step 1: Identify `any` Usage**

When you see `any`, ask:
1. Is this truly unknowable at compile time? (external data, plugin systems)
2. Can I use a more specific type? (union types, generics with constraints)
3. Is this laziness or necessity?

**Step 2: Choose Replacement Strategy**

**Strategy A: Use Specific Types** (preferred)
- Known structure → Use interfaces/types
- Multiple possible types → Use union types
- Shared shape → Use generics with constraints

**Strategy B: Use `unknown`** (when truly dynamic)
- External data with unknown structure
- Plugin/extension systems
- Gradual migration from JavaScript

**Strategy C: Keep `any`** (rare, justified cases)
- Interop with poorly-typed libraries
- Complex type manipulation that TypeScript can't express
- Performance-critical code where type checks are prohibitive

**Step 3: Implement Type Guards**

When using `unknown`, implement type guards:
1. Runtime validation (Zod, io-ts, custom validators)
2. Type predicates for custom guards
3. Built-in guards (typeof, instanceof, in)
</workflow>

<progressive-disclosure>
## Reference Files

For detailed patterns and examples:

- **Type Guard Patterns**: Use the using-type-guards skill for comprehensive type guard implementation
- **Runtime Validation**: Use the using-runtime-checks skill for validating unknown data
- **Generic Constraints**: Use the using-generics skill for constraining generic types
</progressive-disclosure>

<examples>
## Example 1: API Response (External Data)

**❌ Using `any` (unsafe)**

```typescript
async function fetchUser(id: string): Promise<any> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

const user = await fetchUser("123");
console.log(user.name.toUpperCase());
```

**Problem**: If API returns `{ username: string }` instead of `{ name: string }`, this crashes at runtime. TypeScript provides no protection.

**✅ Using `unknown` + validation (safe)**

```typescript
async function fetchUser(id: string): Promise<unknown> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

function isUser(value: unknown): value is { name: string } {
  return (
    typeof value === "object" &&
    value !== null &&
    "name" in value &&
    typeof value.name === "string"
  );
}

const userData = await fetchUser("123");
if (isUser(userData)) {
  console.log(userData.name.toUpperCase());
} else {
  throw new Error("Invalid user data");
}
```

**Better**: Use Zod for complex validation (use the using-runtime-checks skill)

---

## Example 2: Generic Function Defaults

**❌ Using `any` in generic default (unsafe)**

```typescript
interface ApiResponse<T = any> {
  data: T;
  status: number;
}

const response: ApiResponse = { data: "anything", status: 200 };
response.data.nonexistent.property;
```

**Problem**: Generic defaults to `any`, losing all type safety.

**✅ Using `unknown` default (safe)**

```typescript
interface ApiResponse<T = unknown> {
  data: T;
  status: number;
}

const response: ApiResponse = { data: "anything", status: 200 };

if (typeof response.data === "string") {
  console.log(response.data.toUpperCase());
}
```

**Even Better**: Require explicit type parameter

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
}

const response: ApiResponse<User> = await fetchUser();
```

---

## Example 3: Error Handling

**❌ Using `any` for caught errors (unsafe)**

```typescript
try {
  await riskyOperation();
} catch (error: any) {
  console.log(error.message);
}
```

**Problem**: Not all thrown values are Error objects. This crashes if someone throws a string or number.

**✅ Using `unknown` + type guard (safe)**

```typescript
try {
  await riskyOperation();
} catch (error: unknown) {
  if (error instanceof Error) {
    console.log(error.message);
  } else {
    console.log("Unknown error:", String(error));
  }
}
```

---

## Example 4: Validation Function

**❌ Using `any` parameter (unsafe)**

```typescript
function validate(data: any): boolean {
  return data.email && data.password;
}
```

**Problem**: Typos like `data.emial` are not caught. No autocomplete support.

**✅ Using `unknown` + type guard (safe)**

```typescript
interface LoginData {
  email: string;
  password: string;
}

function isLoginData(data: unknown): data is LoginData {
  return (
    typeof data === "object" &&
    data !== null &&
    "email" in data &&
    "password" in data &&
    typeof data.email === "string" &&
    typeof data.password === "string"
  );
}

function validate(data: unknown): data is LoginData {
  if (!isLoginData(data)) {
    return false;
  }

  return data.email.includes("@") && data.password.length >= 8;
}
```
</examples>

<constraints>
**MUST:**

- Use `unknown` for external data (APIs, JSON.parse, user input)
- Use `unknown` for generic defaults when type is truly dynamic
- Implement type guards before accessing `unknown` values
- Use runtime validation libraries (Zod, io-ts) for complex structures

**SHOULD:**

- Prefer specific types (interfaces, unions) over `unknown` when structure is known
- Use type predicates (`value is Type`) for reusable type guards
- Narrow `unknown` progressively (check object → check properties → check types)

**NEVER:**

- Use `any` for external data
- Use `as any` to silence TypeScript errors
- Use `any` in public API surfaces
- Default generics to `any`
- Cast `unknown` to specific types without validation
</constraints>

<validation>
## Validation Checklist

After replacing `any` with `unknown`:

1. **Type Guard Exists**:
   - Every `unknown` value has a corresponding type guard
   - Type guards check structure AND types
   - Guards return early on invalid data

2. **Safe Access Only**:
   - No property access before type narrowing
   - No method calls before type narrowing
   - IDE autocomplete works after narrowing

3. **Error Handling**:
   - Invalid data handled gracefully
   - Clear error messages
   - No silent failures

4. **Compilation**:
   ```bash
   npx tsc --noEmit
   ```
   Should pass without `any` suppressions.
</validation>

<common-patterns>
## When `any` is Actually Justified

**1. Library Interop** (temporary)
```typescript
import poorlyTypedLib from "poorly-typed-lib";
const result = poorlyTypedLib.method() as any;
```

Consider contributing types to DefinitelyTyped or wrapping in typed facade.

**2. Type Manipulation Edge Cases**
```typescript
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

Sometimes TypeScript's type system can't express complex patterns. Document why.

**3. Explicit Opt-Out**
```typescript
const configSchema: any = generateFromSpec();
```

Explicitly choosing to skip type checking for this value. Document decision.
</common-patterns>

<migration-path>
## Migrating Existing `any` Usage

**Phase 1: Audit**
```bash
grep -rn ": any" src/
grep -rn "<any>" src/
grep -rn "= any" src/
```

**Phase 2: Classify**
- External data → `unknown` + validation
- Known structure → specific types
- Generic defaults → remove default or use `unknown`
- Justified `any` → document with comment explaining why

**Phase 3: Replace**
- Start with external boundaries (API layer, JSON parsing)
- Work inward toward core logic
- Add tests to verify runtime behavior unchanged

**Phase 4: Prevent**
- Enable `noImplicitAny` in tsconfig.json
- Add lint rules forbidding `any`
- Use hooks to catch new `any` introduction
</migration-path>
