---
name: using-type-guards
description: Teaches how to write custom type guards with type predicates and use built-in type narrowing in TypeScript. Use when working with unknown types, union types, validating external data, or implementing type-safe runtime checks.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
version: 1.0.0
---

<role>
This skill teaches how to safely narrow types at runtime using type guards, enabling type-safe handling of dynamic data and union types. Critical for validating external data and preventing runtime errors.
</role>

<when-to-activate>
This skill activates when:

- Working with `unknown` or `any` types
- Handling union types that need discrimination
- Validating external data (APIs, user input, JSON)
- Implementing runtime type checks
- User mentions type guards, type narrowing, type predicates, or runtime validation
</when-to-activate>

<overview>
Type guards are runtime checks that inform TypeScript's type system about the actual type of a value. They bridge the gap between compile-time types and runtime values.

**Three Categories**:

1. **Built-in Guards**: `typeof`, `instanceof`, `in`, `Array.isArray()`
2. **Type Predicates**: Custom functions returning `value is Type`
3. **Assertion Functions**: Functions that throw if type check fails

**Key Pattern**: Runtime check → Type narrowing → Safe access
</overview>

<workflow>
## Type Guard Selection Flow

**Step 1: Identify the Type Challenge**

What do you need to narrow?
- Primitive types → Use `typeof`
- Class instances → Use `instanceof`
- Object shapes → Use `in` or custom type predicate
- Array types → Use `Array.isArray()` + element checks
- Complex structures → Use validation library (Zod, io-ts)

**Step 2: Choose Guard Strategy**

**Built-in Guards** (primitives, classes, simple checks)
```typescript
typeof value === "string"
value instanceof Error
"property" in value
Array.isArray(value)
```

**Custom Type Predicates** (object shapes, complex logic)
```typescript
function isUser(value: unknown): value is User {
  return typeof value === "object" &&
         value !== null &&
         "id" in value;
}
```

**Validation Libraries** (nested structures, multiple fields)
```typescript
const UserSchema = z.object({
  id: z.string(),
  email: z.string().email()
});
```

**Step 3: Implement Guard**

1. Check for `null` and `undefined` first
2. Check base type (object, array, primitive)
3. Check structure (properties exist)
4. Check property types
5. Return type predicate or throw
</workflow>

<examples>
## Example 1: Built-in Type Guards

### typeof Guard

```typescript
function processValue(value: unknown): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }

  if (typeof value === "number") {
    return value.toFixed(2);
  }

  if (typeof value === "boolean") {
    return value ? "yes" : "no";
  }

  throw new Error("Unsupported type");
}
```

**typeof Guards Work For**:
- `"string"`, `"number"`, `"boolean"`, `"symbol"`, `"undefined"`
- `"function"`, `"bigint"`
- `"object"` (but also matches `null` - check for `null` first!)

### instanceof Guard

```typescript
function handleError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }

  if (error instanceof CustomError) {
    return `Custom error: ${error.code}`;
  }

  return String(error);
}
```

**instanceof Works For**:
- Class instances
- Built-in classes (Error, Date, Map, Set, etc.)
- DOM elements (HTMLElement, etc.)

### in Guard

```typescript
type Circle = { kind: "circle"; radius: number };
type Square = { kind: "square"; sideLength: number };
type Shape = Circle | Square;

function getArea(shape: Shape): number {
  if ("radius" in shape) {
    return Math.PI * shape.radius ** 2;
  } else {
    return shape.sideLength ** 2;
  }
}
```

**in Guard Best For**:
- Discriminating union types
- Checking optional properties
- Object shape validation

---

## Example 2: Custom Type Predicates

### Basic Type Predicate

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    "email" in value &&
    typeof (value as User).id === "string" &&
    typeof (value as User).name === "string" &&
    typeof (value as User).email === "string"
  );
}

function processUser(data: unknown): void {
  if (isUser(data)) {
    console.log(data.name);
  } else {
    throw new Error("Invalid user data");
  }
}
```

### Array Type Predicate

```typescript
function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every(item => typeof item === "string");
}

function processNames(data: unknown): string {
  if (isStringArray(data)) {
    return data.join(", ");
  }
  throw new Error("Expected array of strings");
}
```

### Nested Type Predicate

For complex nested structures, compose guards from simpler guards. See `references/nested-validation.md` for detailed examples.

---

## Example 3: Discriminated Unions

### Using Literal Type Discrimination

```typescript
type Success = {
  status: "success";
  data: string;
};

type Failure = {
  status: "error";
  error: string;
};

type Result = Success | Failure;

function handleResult(result: Result): void {
  if (result.status === "success") {
    console.log("Data:", result.data);
  } else {
    console.error("Error:", result.error);
  }
}
```

### Runtime Validation of Discriminated Union

```typescript
function isSuccess(value: unknown): value is Success {
  return (
    typeof value === "object" &&
    value !== null &&
    "status" in value &&
    value.status === "success" &&
    "data" in value &&
    typeof (value as Success).data === "string"
  );
}

function isFailure(value: unknown): value is Failure {
  return (
    typeof value === "object" &&
    value !== null &&
    "status" in value &&
    value.status === "error" &&
    "error" in value &&
    typeof (value as Failure).error === "string"
  );
}

function isResult(value: unknown): value is Result {
  return isSuccess(value) || isFailure(value);
}
```

---

## Example 4: Assertion Functions

```typescript
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error(`Expected string, got ${typeof value}`);
  }
}

function assertIsUser(value: unknown): asserts value is User {
  if (!isUser(value)) {
    throw new Error("Invalid user data");
  }
}

function processData(data: unknown): void {
  assertIsUser(data);

  console.log(data.name);
}
```

**Assertion Functions**:
- Throw error if check fails
- Narrow type for remainder of scope
- Use `asserts value is Type` return type
- Good for precondition checks
</examples>

<progressive-disclosure>
## Reference Files

**Local References** (in `references/` directory):
- `advanced-patterns.md` - Optional properties, arrays, tuples, records, enums
- `nested-validation.md` - Complex nested object validation patterns
- `testing-guide.md` - Complete unit testing guide with examples

**Related Skills**:
- **Runtime Validation Libraries**: Use the using-runtime-checks skill for Zod/io-ts patterns
- **Unknown Type Handling**: Use the avoiding-any-types skill for when to use type guards
- **Error Type Guards**: Error-specific type guard patterns can be found in error handling documentation
</progressive-disclosure>

<constraints>
**MUST:**

- Check for `null` and `undefined` before property access
- Check object base type before using `in` operator
- Use type predicates (`value is Type`) for reusable guards
- Validate all required properties exist
- Validate property types, not just existence

**SHOULD:**

- Compose simple guards into complex guards
- Use discriminated unions for known variants
- Prefer built-in guards over custom when possible
- Name guard functions `isType` or `assertIsType`

**NEVER:**

- Access properties before type guard
- Forget to check for `null` (typeof null === "object"!)
- Use type assertions instead of type guards for external data
- Assume property exists after checking with `in`
- Skip validating nested object types
</constraints>

<patterns>
## Common Patterns

**Basic Patterns** (covered in examples above):
- Built-in guards: typeof, instanceof, in, Array.isArray()
- Custom type predicates for object shapes
- Discriminated union narrowing
- Assertion functions

**Advanced Patterns** (see `references/advanced-patterns.md`):
- Optional property validation
- Array element guards with generics
- Tuple guards
- Record guards
- Enum guards
</patterns>

<validation>
## Type Guard Quality Checklist

1. **Null Safety**:
   - [ ] Checks for `null` before using `in` or property access
   - [ ] Checks for `undefined` for optional values

2. **Complete Validation**:
   - [ ] Validates all required properties exist
   - [ ] Validates property types, not just existence
   - [ ] Validates nested objects recursively

3. **Type Predicate**:
   - [ ] Returns `value is Type` for reusable guards
   - [ ] Or uses `asserts value is Type` for assertion functions

4. **Edge Cases**:
   - [ ] Handles arrays correctly
   - [ ] Handles empty objects
   - [ ] Handles inherited properties if relevant

5. **Composition**:
   - [ ] Complex guards built from simpler guards
   - [ ] Guards are unit testable
</validation>

<testing-guards>
## Unit Testing Type Guards

Test all edge cases: valid inputs, missing properties, wrong types, null, undefined, and non-objects.

See `references/testing-guide.md` for complete testing strategies and examples.
</testing-guards>
