---
name: typescript-core-development
description: Implement TypeScript code with type safety, generics, utility types, and functional patterns. Use when designing type-safe code, implementing generics, handling errors with Result pattern, or applying functional programming.
---

# TypeScript Core Development Specialist

Specialized in type-safe TypeScript development with advanced type system features and functional programming patterns.

## When to Use This Skill

- Designing type-safe TypeScript code
- Implementing generics and type constraints
- Using utility types (Partial, Pick, Omit, Record, etc.)
- Creating type guards and type predicates
- Implementing functional programming patterns
- Handling errors with Result/Either pattern
- Working with union and intersection types

## Core Principles

- **Type Safety First**: Leverage TypeScript's type system to catch errors at compile time
- **Explicit Over Implicit**: Use explicit type annotations for clarity
- **Immutability**: Prefer `const` and readonly properties
- **Functional Patterns**: Use pure functions and avoid side effects where possible
- **Discriminated Unions**: Use for type-safe state management
- **Type Narrowing**: Use type guards to narrow types safely

## Implementation Guidelines

### Basic Type Definitions

```typescript
// Primitive types
type UserId = string
type Count = number
type IsActive = boolean

// Object types
interface User {
  id: UserId
  email: string
  name: string
  createdAt: Date
  isActive: boolean
}

// Type alias for object
type Order = {
  id: string
  userId: UserId
  items: string[]
  total: number
  status: 'pending' | 'completed' | 'cancelled'
}

// Readonly properties
interface Config {
  readonly apiUrl: string
  readonly timeout: number
  readonly maxRetries: number
}

// Optional properties
interface UserProfile {
  bio?: string
  avatarUrl?: string
  location?: string
}
```

### Union and Intersection Types

```typescript
// Union types
type Status = 'idle' | 'loading' | 'success' | 'error'
type Result = SuccessResult | ErrorResult

// Intersection types
type Timestamped = {
  createdAt: Date
  updatedAt: Date
}

type UserWithTimestamp = User & Timestamped

// Discriminated unions for type-safe state
type RequestState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: User[] }
  | { status: 'error'; error: string }

// WHY: Discriminated union enables exhaustive type checking
function handleRequest(state: RequestState): string {
  switch (state.status) {
    case 'idle':
      return 'Ready to start'
    case 'loading':
      return 'Loading...'
    case 'success':
      return `Loaded ${state.data.length} users`
    case 'error':
      return `Error: ${state.error}`
  }
}
```

### Generics and Constraints

```typescript
// Basic generic function
function identity<T>(value: T): T {
  return value
}

// Generic with constraints
interface HasId {
  id: string
}

function findById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id)
}

// Generic interface
interface Repository<T> {
  findAll(): Promise<T[]>
  findById(id: string): Promise<T | null>
  save(entity: T): Promise<T>
  delete(id: string): Promise<void>
}

// Generic class
class InMemoryRepository<T extends HasId> implements Repository<T> {
  private items: Map<string, T> = new Map()

  async findAll(): Promise<T[]> {
    return Array.from(this.items.values())
  }

  async findById(id: string): Promise<T | null> {
    return this.items.get(id) ?? null
  }

  async save(entity: T): Promise<T> {
    this.items.set(entity.id, entity)
    return entity
  }

  async delete(id: string): Promise<void> {
    this.items.delete(id)
  }
}

// Multiple type parameters
function map<T, U>(items: T[], fn: (item: T) => U): U[] {
  return items.map(fn)
}

// WHY: Constraint ensures we can safely access 'length' property
function logLength<T extends { length: number }>(value: T): void {
  console.log(`Length: ${value.length}`)
}
```

### Utility Types

```typescript
// Partial - make all properties optional
type PartialUser = Partial<User>

function updateUser(id: string, updates: Partial<User>): User {
  // Update only provided fields
  const user = getUserById(id)
  return { ...user, ...updates }
}

// Pick - select specific properties
type UserSummary = Pick<User, 'id' | 'name' | 'email'>

// Omit - exclude specific properties
type UserWithoutId = Omit<User, 'id'>

// Record - create object type with specific keys and value type
type UserMap = Record<UserId, User>
type StatusCount = Record<Status, number>

// Required - make all properties required
type RequiredConfig = Required<Config>

// Readonly - make all properties readonly
type ImmutableUser = Readonly<User>

// ReturnType - extract return type from function
function getUser(): User {
  // ...
}
type UserType = ReturnType<typeof getUser> // User

// Parameters - extract parameter types from function
function createUser(email: string, name: string): User {
  // ...
}
type CreateUserParams = Parameters<typeof createUser> // [string, string]
```

### Type Guards and Type Predicates

```typescript
// Type predicate
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value &&
    'name' in value
  )
}

// Usage
function processValue(value: unknown): void {
  if (isUser(value)) {
    // TypeScript knows value is User here
    console.log(value.email)
  }
}

// Discriminated union type guard
function isErrorResult(result: Result): result is ErrorResult {
  return result.success === false
}

// Assertion function
function assertIsUser(value: unknown): asserts value is User {
  if (!isUser(value)) {
    throw new Error('Value is not a User')
  }
}

// WHY: After assertion, TypeScript knows value is User
function handleUser(value: unknown): void {
  assertIsUser(value)
  console.log(value.email) // No error, value is User
}

// typeof type guard
function processInput(input: string | number): string {
  if (typeof input === 'string') {
    return input.toUpperCase()
  }
  return input.toString()
}

// instanceof type guard
class ValidationError extends Error {
  constructor(
    message: string,
    public field: string
  ) {
    super(message)
  }
}

function handleError(error: unknown): void {
  if (error instanceof ValidationError) {
    console.log(`Validation error on field: ${error.field}`)
  }
}
```

### Functional Programming Patterns

```typescript
// Pure functions
function add(a: number, b: number): number {
  return a + b
}

// Higher-order functions
function compose<A, B, C>(
  f: (b: B) => C,
  g: (a: A) => B
): (a: A) => C {
  return (a: A) => f(g(a))
}

const toUpperCase = (s: string): string => s.toUpperCase()
const addExclamation = (s: string): string => `${s}!`
const shout = compose(addExclamation, toUpperCase)

// Immutable operations
interface State {
  readonly count: number
  readonly items: readonly string[]
}

// WHY: Return new object instead of mutating
function increment(state: State): State {
  return {
    ...state,
    count: state.count + 1,
  }
}

function addItem(state: State, item: string): State {
  return {
    ...state,
    items: [...state.items, item],
  }
}

// Currying
function multiply(a: number): (b: number) => number {
  return (b: number) => a * b
}

const double = multiply(2)
const triple = multiply(3)

// Pipe function
function pipe<T>(...fns: Array<(arg: T) => T>): (value: T) => T {
  return (value: T) => fns.reduce((acc, fn) => fn(acc), value)
}

const transform = pipe(
  (s: string) => s.trim(),
  (s: string) => s.toLowerCase(),
  (s: string) => s.replace(/\s+/g, '-')
)
```

### Result/Either Pattern for Error Handling

```typescript
// Result type
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E }

// Helper functions
function success<T>(value: T): Result<T, never> {
  return { success: true, value }
}

function failure<E>(error: E): Result<never, E> {
  return { success: false, error }
}

// Usage in functions
function parseJSON<T>(json: string): Result<T, string> {
  try {
    const value = JSON.parse(json) as T
    return success(value)
  } catch (error) {
    return failure('Invalid JSON')
  }
}

// Pattern matching with Result
function handleResult<T, E>(
  result: Result<T, E>,
  handlers: {
    success: (value: T) => void
    failure: (error: E) => void
  }
): void {
  if (result.success) {
    handlers.success(result.value)
  } else {
    handlers.failure(result.error)
  }
}

// Usage
const result = parseJSON<User>('{"id": "1", "email": "user@example.com"}')
handleResult(result, {
  success: user => console.log('Parsed user:', user),
  failure: error => console.error('Parse error:', error),
})

// Result helpers
function map<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  return result.success ? success(fn(result.value)) : result
}

function flatMap<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  return result.success ? fn(result.value) : result
}

// WHY: Chain operations with automatic error propagation
function processUser(json: string): Result<string, string> {
  return pipe(
    parseJSON<User>(json),
    result => map(result, user => user.email),
    result => map(result, email => email.toUpperCase())
  )
}
```

## Tools to Use

- `Read`: Read existing TypeScript files
- `Write`: Create new TypeScript modules
- `Edit`: Modify existing code
- `Bash`: Run TypeScript compiler, tests, and linters

### Bash Commands

```bash
# Type checking
tsc --noEmit

# Watch mode
tsc --watch

# Linting
eslint src/ --ext .ts,.tsx

# Formatting
prettier --write "src/**/*.{ts,tsx}"

# Run tests
vitest
vitest --coverage
```

## Workflow

1. **Understand Requirements**: Clarify what needs to be implemented
2. **Write Tests First**: Use `vitest-react-testing` skill
3. **Verify Tests Fail**: Confirm tests fail correctly (Red)
4. **Define Types**: Start with type definitions and interfaces
5. **Implement Logic**: Write implementation with type safety
6. **Run Type Checker**: Ensure no type errors (`tsc --noEmit`)
7. **Run Tests**: Ensure tests pass (Green)
8. **Run Linter**: Clean up code style (`eslint`)
9. **Refactor**: Improve code quality while maintaining types
10. **Commit**: Create atomic commit

## Related Skills

- `react-component-development`: For React component implementation
- `vitest-react-testing`: For writing tests
- `react-state-management`: For state management patterns

## Coding Standards

See [TypeScript Coding Standards](../_shared/typescript-coding-standards.md)

## TDD Workflow

Follow [Frontend TDD Workflow](../_shared/frontend-tdd-workflow.md)

## Key Reminders

- Always use explicit type annotations for function parameters and return types
- Leverage utility types (Partial, Pick, Omit, Record) to avoid repetition
- Use discriminated unions for type-safe state management
- Implement type guards for runtime type checking
- Prefer `const` and `readonly` for immutability
- Use generics to create reusable, type-safe abstractions
- Consider Result/Either pattern instead of throwing exceptions
- Use functional programming patterns for predictable code
- Run `tsc --noEmit` to catch type errors before runtime
- Write comments explaining WHY, not WHAT
- Follow TDD workflow: Red → Green → Refactor
