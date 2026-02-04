---
name: validating-type-assertions
description: Teaches when type assertions are safe versus dangerous in TypeScript. Use when considering using 'as' keyword, type casting, or when working with external data that might use assertions instead of proper validation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
version: 1.0.0
---

<role>
This skill teaches the difference between safe and dangerous type assertions, preventing the common anti-pattern of using `as Type` on unvalidated external data. Based on stress test findings where 50% of agents misused type assertions.
</role>

<when-to-activate>
This skill activates when:

- Code contains `as` keyword or angle bracket syntax `<Type>`
- Working with type assertions or type casting
- Converting between types
- User mentions type assertions, casting, or "as" keyword
- Code uses assertions on external data
</when-to-activate>

<overview>
**Critical Distinction**:

- **Type Guard**: Runtime check that narrows types safely
- **Type Assertion**: Compile-time instruction telling TypeScript to trust you

**Type assertions are TypeScript compiler directives, not runtime operations.**

```typescript
const data = JSON.parse(json) as User;
```

This compiles fine but provides ZERO runtime safety. If JSON is malformed, your code crashes.

**Rule**: Type assertions are safe only when YOU control the data or have already validated it.
</overview>

<workflow>
## Assertion Safety Decision Tree

**Question 1: Where does this data come from?**

- **From your own code** (constants, constructors) → Assertion OK
- **From external source** (API, user input, JSON) → NEVER assert, validate instead

**Question 2: Have you validated the data?**

- **Yes, with runtime validation** → Assertion OK after validation
- **No validation** → NEVER assert

**Question 3: Is this a TypeScript limitation?**

- **Yes** (const assertions, narrowing limitations) → Assertion OK
- **No** (trying to skip validation) → NEVER assert
</workflow>

<examples>
## Example 1: Dangerous Assertions (DO NOT DO)

**❌ Asserting external API data**

```typescript
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json() as User;
  return data;
}
```

**Problem**: If API returns different structure, runtime crash. TypeScript provides no protection.

**✅ Validate instead**

```typescript
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data: unknown = await response.json();

  if (!isUser(data)) {
    throw new Error("Invalid user data from API");
  }

  return data;
}
```

---

**❌ Asserting JSON.parse result**

```typescript
const config = JSON.parse(configString) as Config;
```

**Problem**: If JSON is malformed or wrong shape, crash at runtime.

**✅ Validate with Zod**

```typescript
const data: unknown = JSON.parse(configString);
const config = ConfigSchema.parse(data);
```

---

**❌ Asserting user input**

```typescript
function handleSubmit(formData: FormData) {
  const user = {
    name: formData.get("name"),
    email: formData.get("email")
  } as User;

  saveUser(user);
}
```

**Problem**: FormData can contain anything. No validation.

**✅ Validate form data**

```typescript
function handleSubmit(formData: FormData) {
  const data = {
    name: formData.get("name"),
    email: formData.get("email")
  };

  const user = UserSchema.parse(data);
  saveUser(user);
}
```

---

## Example 2: Safe Assertions (OK to use)

**✅ Const assertions**

```typescript
const routes = [
  { path: "/", component: "Home" },
  { path: "/about", component: "About" }
] as const;

type Route = typeof routes[number];
```

**Safe because**: Data is hardcoded, not external.

---

**✅ After validation**

```typescript
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data: unknown = await response.json();

  const result = UserSchema.safeParse(data);
  if (!result.success) {
    throw new Error("Invalid user data");
  }

  return result.data as User;
}
```

**Safe because**: Data validated before assertion. (Though `result.data` already has correct type, so assertion is redundant.)

---

**✅ Constructor results**

```typescript
class User {
  constructor(
    public id: string,
    public name: string
  ) {}
}

const users = [
  new User("1", "Alice"),
  new User("2", "Bob")
] as User[];
```

**Safe because**: You control construction, types are guaranteed.

---

**✅ Type narrowing limitations**

```typescript
interface Circle { kind: "circle"; radius: number; }
interface Square { kind: "square"; size: number; }
type Shape = Circle | Square;

function getArea(shape: Shape): number {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2;
  }
  return shape.size ** 2;
}
```

**Safe because**: TypeScript narrows to Square after checking for circle. Use `else` to avoid assertion.

---

**✅ Type widening prevention**

```typescript
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000
} as const;
```

**Safe because**: Preventing literal types from widening to general types.

---

**✅ Unknown to specific after validation**

```typescript
function processError(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (typeof error === "string") return error;
  return String(error);
}
```

**Safe because**: Type guards narrow before use without assertions.

---

## Example 3: Double Assertion Anti-Pattern

**❌ Double assertion to bypass safety**

```typescript
const value = "not a number" as unknown as number;
```

**Problem**: Intentionally bypassing type system. Defeats TypeScript's purpose.

**✅ Fix the types properly**

```typescript
const value: unknown = "not a number";

if (typeof value === "number") {
  console.log(value.toFixed(2));
}
```

---

## Example 4: Non-null Assertion

**❌ Non-null assertion on external data**

```typescript
const user = await fetchUser(id);
console.log(user!.name);
```

**Problem**: If `fetchUser` can return `null`, this crashes.

**✅ Check explicitly**

```typescript
const user = await fetchUser(id);

if (user) {
  console.log(user.name);
} else {
  console.log("User not found");
}
```

---

**✅ Non-null assertion after explicit check**

```typescript
const element = document.getElementById("root");

if (!element) {
  throw new Error("Root element not found");
}

element.appendChild(child);
```

**Safe because**: Checked for null and threw. TypeScript narrows automatically, no assertion needed.

---

## Example 5: Assertion Functions vs Assertions

**❌ Assertion to avoid validation**

```typescript
function getUser(data: unknown): User {
  return data as User;
}
```

**✅ Assertion function with validation**

```typescript
function assertIsUser(data: unknown): asserts data is User {
  if (!isUser(data)) {
    throw new Error("Invalid user data");
  }
}

function getUser(data: unknown): User {
  assertIsUser(data);
  return data;
}
```
</examples>

<progressive-disclosure>
## Reference Files

For related patterns:

- **Runtime Validation**: Use the using-runtime-checks skill for proper validation with Zod
- **Type Guards**: Use the using-type-guards skill for safe type narrowing
- **Unknown Type**: Use the avoiding-any-types skill for handling unknown data safely
</progressive-disclosure>

<constraints>
**MUST:**

- Validate external data with type guards or validation libraries
- Use assertion functions (`asserts value is Type`) over direct assertions
- Check for null/undefined before non-null assertions (`!`)
- Document WHY assertion is safe when used

**SHOULD:**

- Prefer type guards over assertions
- Use `as const` for literal type inference
- Limit assertions to known-safe scenarios
- Consider if assertion indicates missing validation

**NEVER:**

- Assert on external data without validation (APIs, JSON, user input)
- Use double assertions (`as unknown as Type`)
- Use non-null assertion (`!`) without prior check
- Assert to silence compiler errors (fix the types instead)
- Trust that data "will be correct"
</constraints>

<safe-assertion-checklist>
## When Assertions Are Safe

Type assertion is safe when ALL of these are true:

- [ ] Data source is internal/controlled (not external)
- [ ] OR data has been validated with runtime checks
- [ ] You understand what the assertion does (compiler directive, not runtime check)
- [ ] Assertion is documented with reason
- [ ] No double assertions being used

If ANY checkbox is false, use validation instead.
</safe-assertion-checklist>

<common-patterns>
## Pattern Library

### Pattern 1: Validated Assertion

```typescript
function parseUser(data: unknown): User {
  const result = UserSchema.safeParse(data);

  if (!result.success) {
    throw new ValidationError("Invalid user", result.error);
  }

  return result.data;
}
```

### Pattern 2: Const Assertion for Config

```typescript
const API_ENDPOINTS = {
  users: "/api/users",
  posts: "/api/posts",
  comments: "/api/comments"
} as const;

type Endpoint = typeof API_ENDPOINTS[keyof typeof API_ENDPOINTS];
```

### Pattern 3: Assertion Function

```typescript
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}

function handleShape(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.size ** 2;
    default:
      assertNever(shape);
  }
}
```

### Pattern 4: Type Predicate Instead of Assertion

```typescript
function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

const values = [1, null, 2, undefined, 3];
const defined = values.filter(isDefined);
```
</common-patterns>

<migration>
## Removing Unsafe Assertions

**Find assertions**: `grep -rn " as " src/` and `grep -rn "!" src/ | grep -v "!=="`

**Classify each**: External data → add validation; After validation → verify; Const assertion → keep; Bypassing types → fix types

**Replace pattern**:
```typescript
const data = JSON.parse(json) as User;
```
Becomes:
```typescript
const data: unknown = JSON.parse(json);
const user = UserSchema.parse(data);
```

**Enable strict mode**: Set `"strict": true` and `"noImplicitAny": true` in tsconfig.json
</migration>
