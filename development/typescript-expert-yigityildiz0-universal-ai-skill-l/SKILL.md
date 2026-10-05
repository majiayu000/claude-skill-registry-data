---
name: typescript-expert
description: Deep TypeScript expertise for type-safe application development. Use when writing TypeScript code, designing type systems, implementing generics, handling.
---

# TypeScript Expert

Specialized expertise in TypeScript programming, providing deep guidance on the type system, generics, discriminated unions, advanced type patterns, runtime validation, React component typing, and tooling configuration for building robust, type-safe applications.

## When to Use This Skill

Use this skill for:

- Designing type-safe data models and APIs
- Implementing generics and utility types
- Building discriminated unions with exhaustive checks
- Writing advanced type-level logic (recursive types, variadic tuples, conditional types)
- Integrating runtime validation with Zod
- Typing React components, hooks, and context
- Configuring tsconfig, path aliases, and project references

**Trigger phrases**: "typescript", "ts types", "generics", "discriminated union", "zod schema", "tsconfig", "react typescript", "type guard", "utility type"

## What This Skill Does

Provides TypeScript expertise including:

- **Type System**: Strict mode, literal types, template literals, branded types, const assertions
- **Generics**: Constraints, conditional types, mapped types, infer keyword, utility types
- **Discriminated Unions**: Tagged unions, exhaustive checks, type narrowing, type guards
- **Advanced Patterns**: Recursive types, variadic tuples, declaration merging, module augmentation
- **Runtime Validation**: Zod schemas, safeParse, transforms, refinements, inferred types
- **React Typing**: Component props, hooks, context, event handlers, polymorphic components
- **Tooling**: tsconfig strict flags, path aliases, declaration files, project references

## Instructions

### Step 1: Master Type System Fundamentals

**Strict Mode and Compiler Flags**:

TypeScript's `strict` flag is an umbrella that enables a family of stricter checks. Always enable it in production projects. The individual flags it activates include `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitAny`, `noImplicitThis`, `useUnknownInCatchVariables`, and `alwaysStrict`.

```typescript
// tsconfig.json (strict mode enabled)
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

**Literal Types and Const Assertions**:

Literal types narrow a value to an exact string, number, or boolean rather than the wider primitive type. Use `as const` to tell the compiler to infer the narrowest possible type for an expression.

```typescript
// Literal types
type Direction = "north" | "south" | "east" | "west";
type HttpStatus = 200 | 301 | 404 | 500;
type Toggle = true | false;

function move(direction: Direction): void {
  console.log(`Moving ${direction}`);
}

move("north"); // OK
// move("up"); // Error: Argument of type '"up"' is not assignable

// const assertion - infers the narrowest type
const config = {
  endpoint: "https://api.example.com",
  retries: 3,
  methods: ["GET", "POST"],
} as const;
// Type: { readonly endpoint: "https://api.example.com"; readonly retries: 3; readonly methods: readonly ["GET", "POST"] }

// Without `as const`, methods would be string[] and retries would be number
const looseConfig = {
  endpoint: "https://api.example.com",
  retries: 3,
  methods: ["GET", "POST"],
};
// Type: { endpoint: string; retries: number; methods: string[] }

// Extracting literal union from const array
const ROLES = ["admin", "editor", "viewer"] as const;
type Role = (typeof ROLES)[number]; // "admin" | "editor" | "viewer"
```

**Template Literal Types**:

Template literal types build string types by interpolating other types into template literal positions. They are useful for creating constrained string patterns at the type level.

```typescript
// Basic template literal type
type EventName = `on${string}`;
type ValidEvent = EventName; // any string starting with "on"

// Combining unions in template literals
type Color = "red" | "blue" | "green";
type Shade = "light" | "dark";
type ColorVariant = `${Shade}-${Color}`;
// "light-red" | "light-blue" | "light-green" | "dark-red" | "dark-blue" | "dark-green"

// CSS unit type
type CSSUnit = "px" | "em" | "rem" | "%";
type CSSValue = `${number}${CSSUnit}`;

function setWidth(value: CSSValue): void {
  // ...
}

setWidth("100px");  // OK
setWidth("1.5rem"); // OK
// setWidth("100");  // Error: not assignable to CSSValue

// Intrinsic string manipulation types
type Uppercased = Uppercase<"hello">; // "HELLO"
type Lowercased = Lowercase<"HELLO">; // "hello"
type Capitalized = Capitalize<"hello">; // "Hello"
type Uncapitalized = Uncapitalize<"Hello">; // "hello"
```

**Branded Types**:

Branded types (also called nominal types or opaque types) use an intersection with a unique symbol to prevent accidental mixing of structurally identical types. This is a powerful pattern for domain modelling.

```typescript
// Branded type pattern
type Brand<T, B extends string> = T & { readonly __brand: B };

type USD = Brand<number, "USD">;
type EUR = Brand<number, "EUR">;
type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

// Constructor functions that brand raw values
function usd(amount: number): USD {
  return amount as USD;
}

function eur(amount: number): EUR {
  return amount as EUR;
}

function userId(id: string): UserId {
  return id as UserId;
}

// Type safety prevents mixing currencies or IDs
function chargeUSD(amount: USD): void {
  console.log(`Charging $${amount}`);
}

chargeUSD(usd(19.99));   // OK
// chargeUSD(eur(19.99)); // Error: EUR is not assignable to USD
// chargeUSD(19.99);      // Error: number is not assignable to USD

function getUser(id: UserId): void { /* ... */ }
// getUser("abc");         // Error: string is not assignable to UserId
// getUser(orderId("abc")); // Error: OrderId is not assignable to UserId
```

### Step 2: Generics and Utility Types

**Generic Constraints**:

Generics allow you to write functions and types that work with any type while preserving type information. Constraints (the `extends` keyword) restrict what types a generic parameter can accept.

```typescript
// Basic generic function
function identity<T>(value: T): T {
  return value;
}

const num = identity(42);       // inferred as number
const str = identity("hello");  // inferred as string

// Constrained generic - T must have a length property
function getLength<T extends { length: number }>(item: T): number {
  return item.length;
}

getLength("hello");    // OK - string has length
getLength([1, 2, 3]);  // OK - array has length
// getLength(42);       // Error: number doesn't have length

// Generic with keyof constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30, active: true };
const name = getProperty(user, "name");    // type: string
const age = getProperty(user, "age");      // type: number
// getProperty(user, "email");              // Error: "email" not in keyof typeof user

// Multiple generic parameters with relationships
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

const merged = merge({ name: "Alice" }, { age: 30 });
// type: { name: string } & { age: number }
```

**Conditional Types**:

Conditional types select one of two types based on a condition, using the syntax `T extends U ? X : Y`. They are especially powerful when combined with `infer` to extract types from complex structures.

```typescript
// Basic conditional type
type IsString<T> = T extends string ? true : false;

type A = IsString<"hello">; // true
type B = IsString<42>;      // false

// Distributive conditional types (distributes over unions)
type ToArray<T> = T extends unknown ? T[] : never;
type Result = ToArray<string | number>; // string[] | number[]

// Non-distributive (wrap in tuple to prevent distribution)
type ToArrayNonDist<T> = [T] extends [unknown] ? T[] : never;
type Result2 = ToArrayNonDist<string | number>; // (string | number)[]

// The infer keyword - extract types from structures
type ReturnTypeOf<T> = T extends (...args: unknown[]) => infer R ? R : never;
type FnReturn = ReturnTypeOf<(x: number) => string>; // string

type ElementType<T> = T extends (infer E)[] ? E : T;
type El = ElementType<string[]>;  // string
type El2 = ElementType<number>;   // number (fallback)

// Extract promise value type
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;
type Resolved = Awaited<Promise<Promise<string>>>; // string

// Infer from function parameters
type FirstParam<T> = T extends (first: infer P, ...rest: unknown[]) => unknown ? P : never;
type Param = FirstParam<(x: number, y: string) => void>; // number
```

**Mapped Types**:

Mapped types transform every property of an existing type by iterating over its keys. They are the foundation of many built-in utility types.

```typescript
// Basic mapped type
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

type Optional<T> = {
  [K in keyof T]?: T[K];
};

// Mapped type with key remapping (TypeScript 4.1+)
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Person {
  name: string;
  age: number;
}

type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }

// Filtering keys with mapped types
type FilterByType<T, ValueType> = {
  [K in keyof T as T[K] extends ValueType ? K : never]: T[K];
};

interface Mixed {
  name: string;
  age: number;
  active: boolean;
  email: string;
}

type StringProps = FilterByType<Mixed, string>;
// { name: string; email: string }
```

**Built-in Utility Types**:

TypeScript provides a comprehensive set of utility types that cover the most common type transformations. Knowing these prevents you from reinventing them.

```typescript
// Record - construct an object type with specific keys and value types
type PageInfo = Record<"home" | "about" | "contact", { title: string; url: string }>;

// Pick and Omit - select or remove properties
type UserSummary = Pick<User, "id" | "name">;
type UserWithoutPassword = Omit<User, "password">;

// Extract and Exclude - filter union members
type NumOrStr = Extract<string | number | boolean, string | number>; // string | number
type OnlyBool = Exclude<string | number | boolean, string | number>; // boolean

// Parameters and ReturnType - extract function type info
type Params = Parameters<typeof fetch>; // [input: RequestInfo | URL, init?: RequestInit]
type Return = ReturnType<typeof fetch>;  // Promise<Response>

// NonNullable - remove null and undefined
type MaybeString = string | null | undefined;
type DefiniteString = NonNullable<MaybeString>; // string

// Partial and Required - toggle optionality
interface Config {
  host: string;
  port: number;
  debug?: boolean;
}

type PartialConfig = Partial<Config>;   // all optional
type FullConfig = Required<Config>;     // all required (debug becomes required)

// Readonly at the utility level
type FrozenConfig = Readonly<Config>;
// { readonly host: string; readonly port: number; readonly debug?: boolean }
```

### Step 3: Discriminated Unions and Pattern Matching

**Tagged Unions**:

Discriminated unions (also called tagged unions) use a common literal property (the discriminant) to distinguish between variants. TypeScript narrows the type automatically inside switch or if blocks that check the discriminant.

```typescript
// Define a discriminated union for API responses
type ApiResponse<T> =
  | { status: "success"; data: T; timestamp: number }
  | { status: "error"; error: string; code: number }
  | { status: "loading" };

function handleResponse(response: ApiResponse<User>): void {
  switch (response.status) {
    case "success":
      // TypeScript knows: response.data is User, response.timestamp is number
      console.log(`User: ${response.data.name}`);
      break;
    case "error":
      // TypeScript knows: response.error is string, response.code is number
      console.error(`Error ${response.code}: ${response.error}`);
      break;
    case "loading":
      // TypeScript knows: no other properties
      console.log("Loading...");
      break;
  }
}

// Shape example - classic discriminated union
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return 0.5 * shape.base * shape.height;
  }
}
```

**Exhaustive Checks**:

The `never` type is TypeScript's bottom type (no value is assignable to it). Use it in the default branch of a switch statement to ensure all union variants are handled. If a new variant is added to the union, the code will fail to compile until you handle it.

```typescript
// Exhaustiveness check with never
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(value)}`);
}

function getShapeColor(shape: Shape): string {
  switch (shape.kind) {
    case "circle":
      return "red";
    case "rectangle":
      return "blue";
    case "triangle":
      return "green";
    default:
      return assertNever(shape); // Compile error if a variant is missing
  }
}

// Alternative: satisfies-based exhaustive check
type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "RESET" };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case "INCREMENT":
      return state + action.amount;
    case "DECREMENT":
      return state - action.amount;
    case "RESET":
      return 0;
    default: {
      const _exhaustive: never = action;
      return state;
    }
  }
}
```

**Type Guards and Assertion Functions**:

Type guards are functions that return a type predicate (`param is Type`), allowing TypeScript to narrow the type in the calling scope. Assertion functions (`asserts param is Type`) narrow by throwing on failure rather than returning a boolean.

```typescript
// User-defined type guard
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function processValue(value: unknown): void {
  if (isString(value)) {
    // value is narrowed to string
    console.log(value.toUpperCase());
  }
}

// Type guard for discriminated union members
interface Dog { kind: "dog"; bark(): void }
interface Cat { kind: "cat"; meow(): void }
type Animal = Dog | Cat;

function isDog(animal: Animal): animal is Dog {
  return animal.kind === "dog";
}

// Type guard with in operator
function hasName(obj: unknown): obj is { name: string } {
  return typeof obj === "object" && obj !== null && "name" in obj;
}

// Assertion function - narrows by throwing
function assertDefined<T>(value: T | null | undefined, message?: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? "Value is null or undefined");
  }
}

function processUser(user: User | null): void {
  assertDefined(user, "User must exist");
  // user is narrowed to User (not null)
  console.log(user.name);
}

// Assertion function for custom conditions
function assertIsAdmin(user: User): asserts user is User & { role: "admin" } {
  if (user.role !== "admin") {
    throw new Error("User is not an admin");
  }
}
```

### Step 4: Advanced Type Patterns

**Recursive Types**:

TypeScript supports recursive type aliases, which reference themselves in their definition. These are essential for modelling tree structures, JSON values, and deeply nested data.

```typescript
// JSON type - a classic recursive type
type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

// Deeply nested readonly
type DeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

interface NestedConfig {
  db: { host: string; credentials: { user: string; pass: string } };
  features: string[];
}

type FrozenConfig = DeepReadonly<NestedConfig>;
// All properties at every depth are readonly

// Deep partial
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

// Recursive path type - generates dot-notation paths for an object
type Path<T, Prefix extends string = ""> = T extends object
  ? {
      [K in keyof T & string]: K | `${K}.${Path<T[K], "">}`;
    }[keyof T & string]
  : never;

interface Form {
  user: { name: string; address: { city: string; zip: string } };
  tags: string[];
}

type FormPath = Path<Form>;
// "user" | "user.name" | "user.address" | "user.address.city" | "user.address.zip" | "tags"
```

**Variadic Tuple Types**:

Variadic tuple types (TypeScript 4.0+) allow generic spreading of tuple types, enabling type-safe operations on function arguments and tuple manipulation.

```typescript
// Spread in tuple types
type Concat<A extends unknown[], B extends unknown[]> = [...A, ...B];
type Result = Concat<[1, 2], [3, 4]>; // [1, 2, 3, 4]

// Prepend an element to a tuple
type Prepend<T, Arr extends unknown[]> = [T, ...Arr];
type WithId = Prepend<number, [string, boolean]>; // [number, string, boolean]

// Typed zip function
function zip<A extends unknown[], B extends unknown[]>(
  a: [...A],
  b: [...B],
): { [K in keyof A]: [A[K], K extends keyof B ? B[K] : undefined] } {
  return a.map((val, i) => [val, b[i]]) as never;
}

const zipped = zip([1, "a"] as const, [true, 42] as const);
// type: [[1, true], ["a", 42]]

// Type-safe pipe function using variadic tuples
type Last<T extends unknown[]> = T extends [...unknown[], infer L] ? L : never;

function pipe<T, Fns extends ((arg: never) => unknown)[]>(
  initial: T,
  ...fns: Fns
): ReturnType<Last<Fns> extends (...args: never[]) => infer R ? () => R : never> {
  return fns.reduce((acc, fn) => fn(acc), initial) as never;
}
```

**Declaration Merging and Module Augmentation**:

TypeScript merges declarations with the same name in the same scope. Interfaces merge automatically, and module augmentation lets you extend third-party types without modifying their source.

```typescript
// Interface merging - declarations combine
interface Box {
  width: number;
  height: number;
}

interface Box {
  color: string;
}

// Box now has width, height, and color
const box: Box = { width: 10, height: 20, color: "red" };

// Module augmentation - extend third-party types
// Extend Express Request with custom properties
declare module "express" {
  interface Request {
    userId?: string;
    correlationId: string;
  }
}

// Now TypeScript knows about req.userId and req.correlationId
// in all Express route handlers

// Augmenting a global type
declare global {
  interface Window {
    __APP_CONFIG__: {
      apiUrl: string;
      version: string;
    };
  }
}

// Now window.__APP_CONFIG__ is typed everywhere

// Namespace merging with enums
enum Color {
  Red = "RED",
  Blue = "BLUE",
}

namespace Color {
  export function parse(str: string): Color | undefined {
    return Object.values(Color).find((c) => c === str) as Color | undefined;
  }
}

Color.parse("RED"); // Color.Red
```

**Type-Level Programming**:

TypeScript's type system is Turing-complete, allowing you to encode logic (string parsing, arithmetic, validation) entirely at the type level. Use this sparingly for library APIs where compile-time safety justifies the complexity.

```typescript
// Type-level string parsing
type Split<S extends string, D extends string> = S extends `${infer Head}${D}${infer Tail}`
  ? [Head, ...Split<Tail, D>]
  : [S];

type Parts = Split<"a.b.c", ".">; // ["a", "b", "c"]

// Type-level builder pattern
interface QueryBuilder<Selected extends string = never> {
  select<Col extends string>(
    column: Col,
  ): QueryBuilder<Selected | Col>;
  where(column: Selected, value: unknown): QueryBuilder<Selected>;
  execute(): Promise<Record<Selected, unknown>[]>;
}

// Usage ensures you can only filter on selected columns
declare const qb: QueryBuilder;
const query = qb
  .select("name")
  .select("age")
  .where("name", "Alice") // OK - "name" is selected
  // .where("email", "x")  // Error - "email" is not in Selected

// Compile-time route parameter extraction
type ExtractParams<T extends string> = T extends `${string}:${infer Param}/${infer Rest}`
  ? Param | ExtractParams<Rest>
  : T extends `${string}:${infer Param}`
    ? Param
    : never;

type RouteParams = ExtractParams<"/users/:userId/posts/:postId">;
// "userId" | "postId"

type ParamMap<T extends string> = Record<ExtractParams<T>, string>;
// For the route above: { userId: string; postId: string }
```

### Step 5: Runtime Validation with Zod

**Schema Definition**:

TypeScript types are erased at compile time and provide no runtime safety. Zod bridges this gap by defining schemas that validate data at runtime and infer static types from the same source of truth.

```typescript
import { z } from "zod";

// Primitive schemas
const nameSchema = z.string().min(1).max(100);
const ageSchema = z.number().int().positive().max(150);
const emailSchema = z.string().email();

// Object schema
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  role: z.enum(["admin", "editor", "viewer"]),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

// Infer the TypeScript type from the schema
type User = z.infer<typeof UserSchema>;
// { id: string; name: string; email: string; age: number; role: "admin" | "editor" | "viewer"; metadata?: Record<string, unknown> }

// Nested and composed schemas
const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  country: z.string().length(2), // ISO country code
  zip: z.string().regex(/^\d{5}(-\d{4})?$/),
});

const UserWithAddressSchema = UserSchema.extend({
  address: AddressSchema,
  tags: z.array(z.string()).default([]),
});
```

**safeParse and Error Handling**:

Always prefer `safeParse` over `parse` in application code. While `parse` throws on invalid input, `safeParse` returns a discriminated union that forces you to handle both success and failure paths explicitly.

```typescript
// safeParse returns a discriminated union
const result = UserSchema.safeParse(unknownData);

if (result.success) {
  // result.data is fully typed as User
  console.log(result.data.name);
} else {
  // result.error contains detailed validation errors
  const formatted = result.error.format();
  console.error(formatted);

  // Iterate individual issues
  for (const issue of result.error.issues) {
    console.error(`${issue.path.join(".")}: ${issue.message}`);
  }
}

// In an Express route handler
app.post("/users", (req, res) => {
  const parsed = UserSchema.safeParse(req.body);

  if (!parsed.success) {
    return res.status(400).json({
      errors: parsed.error.issues.map((i) => ({
        field: i.path.join("."),
        message: i.message,
      })),
    });
  }

  // parsed.data is User - fully validated and typed
  createUser(parsed.data);
  return res.status(201).json(parsed.data);
});
```

**Transforms and Refinements**:

Transforms change the output type of a schema (for example, coercing a date string into a `Date` object). Refinements add custom validation logic without changing the type.

```typescript
// Transform: change the output type
const DateStringSchema = z
  .string()
  .datetime()
  .transform((str) => new Date(str));

type DateOutput = z.infer<typeof DateStringSchema>; // Date (not string)

// Coercion helpers
const CoercedNumber = z.coerce.number(); // "42" -> 42
const CoercedBoolean = z.coerce.boolean(); // "true" -> true

// Refinement: custom validation without changing the type
const PasswordSchema = z
  .string()
  .min(8)
  .refine((pw) => /[A-Z]/.test(pw), "Must contain an uppercase letter")
  .refine((pw) => /[0-9]/.test(pw), "Must contain a digit")
  .refine((pw) => /[^A-Za-z0-9]/.test(pw), "Must contain a special character");

// Superrefine for cross-field validation
const SignupSchema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.confirmPassword) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Passwords do not match",
        path: ["confirmPassword"],
      });
    }
  });

// Discriminated union schema
const EventSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
  z.object({ type: z.literal("keypress"), key: z.string() }),
  z.object({ type: z.literal("scroll"), delta: z.number() }),
]);

type AppEvent = z.infer<typeof EventSchema>;
```

### Step 6: React with TypeScript

**Component Typing**:

Type React components using function declarations with explicit prop types. Avoid `React.FC` because it implicitly includes `children` in the props and obscures the return type.

```typescript
// Basic component with typed props
interface ButtonProps {
  label: string;
  variant?: "primary" | "secondary" | "danger";
  disabled?: boolean;
  onClick: () => void;
}

function Button({ label, variant = "primary", disabled = false, onClick }: ButtonProps): React.ReactElement {
  return (
    <button className={`btn btn-${variant}`} disabled={disabled} onClick={onClick}>
      {label}
    </button>
  );
}

// Children prop - be explicit about what children you accept
interface CardProps {
  title: string;
  children: React.ReactNode; // Accepts anything renderable
}

function Card({ title, children }: CardProps): React.ReactElement {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="card-body">{children}</div>
    </div>
  );
}

// Render prop pattern
interface DataFetcherProps<T> {
  url: string;
  render: (data: T, loading: boolean) => React.ReactNode;
}

function DataFetcher<T>({ url, render }: DataFetcherProps<T>): React.ReactElement {
  const [data, setData] = React.useState<T | null>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then((json: T) => { setData(json); setLoading(false); });
  }, [url]);

  return <>{data !== null ? render(data, loading) : null}</>;
}
```

**Hooks Typing**:

When TypeScript cannot infer the type of a hook's state (for example, when the initial value is `null` or an empty array), provide an explicit generic argument. For `useRef`, distinguish between refs to DOM elements and refs to mutable values.

```typescript
// useState with explicit type
const [user, setUser] = React.useState<User | null>(null);
const [items, setItems] = React.useState<Item[]>([]);

// useReducer with typed state and actions
interface CounterState {
  count: number;
}

type CounterAction =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "RESET" };

function counterReducer(state: CounterState, action: CounterAction): CounterState {
  switch (action.type) {
    case "INCREMENT":
      return { count: state.count + action.amount };
    case "DECREMENT":
      return { count: state.count - action.amount };
    case "RESET":
      return { count: 0 };
  }
}

function Counter(): React.ReactElement {
  const [state, dispatch] = React.useReducer(counterReducer, { count: 0 });

  return (
    <div>
      <span>{state.count}</span>
      <button onClick={() => dispatch({ type: "INCREMENT", amount: 1 })}>+</button>
    </div>
  );
}

// useRef for DOM elements vs mutable values
function TextInput(): React.ReactElement {
  // DOM ref - pass null, TypeScript knows it may be null until attached
  const inputRef = React.useRef<HTMLInputElement>(null);

  // Mutable ref - for storing values that do not trigger re-renders
  const renderCount = React.useRef<number>(0);

  React.useEffect(() => {
    renderCount.current += 1;
  });

  function focusInput(): void {
    inputRef.current?.focus();
  }

  return <input ref={inputRef} />;
}

// Custom hook with typed return
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [stored, setStored] = React.useState<T>(() => {
    const item = window.localStorage.getItem(key);
    return item !== null ? (JSON.parse(item) as T) : initialValue;
  });

  function setValue(value: T): void {
    setStored(value);
    window.localStorage.setItem(key, JSON.stringify(value));
  }

  return [stored, setValue];
}
```

**Context Typing and Event Handlers**:

Create typed context with a factory pattern that avoids the need for a default value while keeping the API ergonomic. For event handlers, use React's built-in event types rather than the DOM ones directly.

```typescript
// Typed context - factory pattern (no awkward default value)
interface AuthContext {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = React.createContext<AuthContext | null>(null);

function useAuth(): AuthContext {
  const context = React.useContext(AuthContext);
  if (context === null) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

function AuthProvider({ children }: { children: React.ReactNode }): React.ReactElement {
  const [user, setUser] = React.useState<User | null>(null);

  const login = async (credentials: Credentials): Promise<void> => {
    const user = await api.login(credentials);
    setUser(user);
  };

  const logout = (): void => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Event handler typing
function Form(): React.ReactElement {
  function handleSubmit(event: React.FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    // Process form...
  }

  function handleChange(event: React.ChangeEvent<HTMLInputElement>): void {
    console.log(event.target.value);
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>): void {
    if (event.key === "Enter") {
      // Submit...
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} onKeyDown={handleKeyDown} />
    </form>
  );
}
```

**Polymorphic Components**:

A polymorphic component accepts an `as` prop that controls which HTML element (or React component) it renders. This pattern is common in design system libraries and requires careful typing to ensure that the resulting props match the chosen element.

```typescript
// Polymorphic component - renders as any HTML element
type PolymorphicProps<E extends React.ElementType, P = object> = P &
  Omit<React.ComponentPropsWithoutRef<E>, keyof P | "as"> & {
    as?: E;
  };

type TextProps<E extends React.ElementType = "span"> = PolymorphicProps<E, {
  size?: "sm" | "md" | "lg";
  weight?: "normal" | "bold";
}>;

function Text<E extends React.ElementType = "span">({
  as,
  size = "md",
  weight = "normal",
  children,
  ...rest
}: TextProps<E> & { children?: React.ReactNode }): React.ReactElement {
  const Component = as ?? "span";
  return (
    <Component className={`text-${size} font-${weight}`} {...rest}>
      {children}
    </Component>
  );
}

// Usage - props are validated against the chosen element
<Text>Default span</Text>
<Text as="h1" size="lg">Heading</Text>
<Text as="a" href="/about" size="sm">Link</Text>
// <Text as="a" disabled>Error</Text>  // Error: 'disabled' does not exist on anchor
```

### Step 7: Configuration and Tooling

**tsconfig Strict Flags**:

A production-grade tsconfig should enable every strictness flag available. Each flag catches a distinct class of bugs. Here is a recommended configuration with explanations.

```jsonc
{
  "compilerOptions": {
    // Strict family (all enabled by "strict": true)
    "strict": true,

    // Additional strictness beyond the "strict" umbrella
    "noUncheckedIndexedAccess": true,    // arr[0] is T | undefined, not T
    "exactOptionalPropertyTypes": true,  // { x?: string } does not accept undefined assignment
    "noPropertyAccessFromIndexSignature": true, // force bracket notation for index signatures
    "noFallthroughCasesInSwitch": true,  // switch cases must break or return

    // Module resolution
    "module": "ESNext",
    "moduleResolution": "bundler",       // modern resolution for Vite, esbuild, etc.
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "isolatedModules": true,             // required for esbuild, swc, and similar transpilers

    // Output
    "target": "ES2022",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "dist",

    // Path aliases
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules", "dist"]
}
```

**Path Aliases**:

Path aliases replace long relative imports with clean, absolute-looking paths. You must configure them in both tsconfig (for the compiler) and your bundler (for runtime resolution).

```typescript
// Without path aliases
import { Button } from "../../../components/ui/Button";
import { formatDate } from "../../../../utils/date";

// With path aliases
import { Button } from "@components/ui/Button";
import { formatDate } from "@utils/date";
```

```typescript
// Vite configuration for path aliases
// vite.config.ts
import { defineConfig } from "vite";
import path from "path";

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      "@components": path.resolve(__dirname, "src/components"),
      "@utils": path.resolve(__dirname, "src/utils"),
    },
  },
});
```

**Declaration Files**:

Declaration files (`.d.ts`) describe the types of JavaScript code that has no TypeScript source. Use them for untyped third-party modules, global ambient declarations, and when publishing a library.

```typescript
// Declare types for an untyped module
// types/untyped-lib.d.ts
declare module "untyped-lib" {
  export function doSomething(input: string): number;
  export interface Config {
    verbose: boolean;
    output: string;
  }
  export default function init(config: Config): void;
}

// Declare global ambient types available everywhere
// types/global.d.ts
declare global {
  // Extend NodeJS process.env with known variables
  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: "development" | "production" | "test";
      DATABASE_URL: string;
      API_KEY: string;
    }
  }
}

export {}; // Makes this file a module so `declare global` works

// Type-only imports and exports (erased at runtime)
import type { User } from "./models";
export type { User };

// Import type inline (TypeScript 4.5+)
function processUser(user: import("./models").User): void {
  // ...
}
```

**Project References**:

Project references split a large codebase into smaller TypeScript projects that can be compiled independently. This improves editor responsiveness and build times through incremental compilation.

```jsonc
// Root tsconfig.json
{
  "files": [],
  "references": [
    { "path": "packages/shared" },
    { "path": "packages/client" },
    { "path": "packages/server" }
  ]
}

// packages/shared/tsconfig.json
{
  "compilerOptions": {
    "composite": true,       // required for project references
    "declaration": true,     // required for composite projects
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src/**/*.ts"]
}

// packages/client/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "references": [
    { "path": "../shared" }  // client depends on shared
  ],
  "include": ["src/**/*.ts", "src/**/*.tsx"]
}
```

```bash
# Build all referenced projects in dependency order
tsc --build

# Build incrementally (only changed projects)
tsc --build --incremental

# Clean all build outputs
tsc --build --clean
```

## Best Practices

- **Enable strict mode** - Never ship a project with `strict: false`; fix the underlying type issues instead
- **Avoid any** - Use `unknown` and narrow with type guards; `any` disables the compiler's safety net
- **Infer where obvious, annotate where not** - Let TypeScript infer local variables; always annotate exported function signatures
- **Prefer type aliases over interfaces for data** - Use interfaces only when you need declaration merging or extension points
- **Validate at the boundary** - Use Zod (or a similar library) where data enters your system (API routes, form submissions, storage reads)
- **Use discriminated unions over type flags** - A `kind` or `type` discriminant is safer and more ergonomic than `if (obj.isError)`
- **Branded types for domain IDs** - Prevent accidental mixing of `UserId` and `OrderId` even though both are strings
- **Keep generics simple** - If a type requires more than three generic parameters, consider restructuring

## Common Patterns

### Pattern 1: Type-Safe Event Emitter

```typescript
type EventMap = {
  userCreated: { userId: string; email: string };
  orderPlaced: { orderId: string; total: number };
  error: { message: string; code: number };
};

class TypedEmitter<Events extends Record<string, unknown>> {
  private handlers = new Map<keyof Events, Set<(data: never) => void>>();

  on<K extends keyof Events>(event: K, handler: (data: Events[K]) => void): void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler as (data: never) => void);
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.handlers.get(event)?.forEach((handler) => handler(data as never));
  }
}

const emitter = new TypedEmitter<EventMap>();
emitter.on("userCreated", (data) => {
  // data is { userId: string; email: string }
  console.log(data.userId);
});
// emitter.emit("userCreated", { orderId: "123" }); // Error: missing userId
```

### Pattern 2: Type-Safe API Client

```typescript
// Define route map as a type
interface ApiRoutes {
  "GET /users": { response: User[]; query: { page?: number } };
  "GET /users/:id": { response: User; params: { id: string } };
  "POST /users": { response: User; body: CreateUserDto };
  "PUT /users/:id": { response: User; params: { id: string }; body: UpdateUserDto };
  "DELETE /users/:id": { response: void; params: { id: string } };
}

type Method = "GET" | "POST" | "PUT" | "DELETE";

type RoutesForMethod<M extends Method> = {
  [K in keyof ApiRoutes]: K extends `${M} ${string}` ? K : never;
}[keyof ApiRoutes];

// The client enforces correct params, body, and query for each route
async function apiClient<K extends keyof ApiRoutes>(
  route: K,
  options: Omit<ApiRoutes[K], "response">,
): Promise<ApiRoutes[K]["response"]> {
  // Implementation: parse method and path from route key, substitute params, fetch...
  throw new Error("Not implemented");
}

// Usage - fully type-checked
const users = await apiClient("GET /users", { query: { page: 1 } });
const user = await apiClient("POST /users", { body: { name: "Alice", email: "a@b.com" } });
```

## Quality Checklist

- [ ] `strict: true` enabled in tsconfig with `noUncheckedIndexedAccess`
- [ ] No uses of `any` (search codebase, replace with `unknown` and narrow)
- [ ] All exported functions have explicit return types
- [ ] Discriminated unions use exhaustive checks (`assertNever`)
- [ ] API boundaries validated with Zod (or equivalent runtime validator)
- [ ] React components typed without `React.FC`
- [ ] Custom hooks return explicitly typed tuples or objects
- [ ] Path aliases configured in both tsconfig and bundler
- [ ] Declaration files provided for untyped dependencies

## Related Skills

- `react-specialist` - React architecture and patterns
- `code-quality` - TypeScript code standards
- `cicd-architect` - TypeScript CI/CD pipelines
- `api-designer` - Type-safe API design
- `performance-testing` - TypeScript build optimization

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: TypeScript Handbook, Effective TypeScript, awesome-claude-code-subagents patterns


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
