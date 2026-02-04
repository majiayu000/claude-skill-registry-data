---
name: typescript-enforcer
description: Enforce strict TypeScript type safety rules including no 'any' types, explicit return types, proper interfaces, and type guards. Use when writing TypeScript code, reviewing code, refactoring, or when user mentions TypeScript, types, interfaces, or type safety.
version: 1.0.0
---

# TypeScript Type Safety Enforcer

Enforce strict TypeScript type safety standards with zero tolerance for shortcuts.

## Core Rule: NEVER Use "any" Type

**This is an immediate fail. No exceptions.**

```typescript
// ❌ ABSOLUTELY FORBIDDEN
const data: any = getData();
function process(input: any): any { }
const items: any[] = [];

// ✅ ALWAYS DO THIS INSTEAD
const data: UserData = getData();
function process(input: UserInput): ProcessedResult { }
const items: string[] = [];
```

## Type Safety Principles

### 1. Always Define Proper Types and Interfaces

**Bad:**
```typescript
function createUser(data) {
  return {
    id: data.id,
    name: data.name,
    email: data.email
  };
}
```

**Good:**
```typescript
interface UserInput {
  id: string;
  name: string;
  email: string;
}

interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

function createUser(data: UserInput): User {
  return {
    id: data.id,
    name: data.name,
    email: data.email,
    createdAt: new Date()
  };
}
```

### 2. Explicit Function Parameters and Return Types

**Bad:**
```typescript
function calculate(a, b) {
  return a + b;
}

async function fetchUser(id) {
  const response = await api.get(`/users/${id}`);
  return response.data;
}
```

**Good:**
```typescript
function calculate(a: number, b: number): number {
  return a + b;
}

async function fetchUser(id: string): Promise<User> {
  const response = await api.get<User>(`/users/${id}`);
  return response.data;
}
```

### 3. Use "unknown" Instead of "any"

When type is truly unknown, use `unknown` and narrow with type guards.

**Bad:**
```typescript
function parseJSON(json: string): any {
  return JSON.parse(json);
}
```

**Good:**
```typescript
function parseJSON(json: string): unknown {
  return JSON.parse(json);
}

// Then use type guard to narrow
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'name' in data &&
    'email' in data
  );
}

const data = parseJSON(jsonString);
if (isUser(data)) {
  // Now TypeScript knows data is User
  console.log(data.name);
}
```

### 4. Prefer Specific Types Over Broad Types

**Bad:**
```typescript
type Status = string;
function setStatus(status: string) { }
```

**Good:**
```typescript
type Status = 'active' | 'inactive' | 'pending';
function setStatus(status: Status) { }

// Or with enums
enum Status {
  Active = 'active',
  Inactive = 'inactive',
  Pending = 'pending'
}
function setStatus(status: Status) { }
```

### 5. Type Guards for Narrowing

**Example:**
```typescript
// Type guard functions
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    typeof (value as any).id === 'string'
  );
}

// Usage
function process(input: unknown) {
  if (isString(input)) {
    // TypeScript knows input is string here
    console.log(input.toUpperCase());
  } else if (isUser(input)) {
    // TypeScript knows input is User here
    console.log(input.name);
  }
}
```

## TypeScript Utility Types

Use built-in utility types instead of "any":

### Partial<T>
```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

// Make all properties optional
function updateUser(id: string, updates: Partial<User>) {
  // updates can have any combination of User properties
}
```

### Required<T>
```typescript
interface UserInput {
  name?: string;
  email?: string;
}

// Make all properties required
function createUser(data: Required<UserInput>) {
  // data.name and data.email are guaranteed to exist
}
```

### Pick<T, K>
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  createdAt: Date;
}

// Pick only specific properties
type PublicUser = Pick<User, 'id' | 'name' | 'email'>;
```

### Omit<T, K>
```typescript
// Exclude specific properties
type UserWithoutPassword = Omit<User, 'password'>;
```

### Record<K, T>
```typescript
// Create object type with specific keys
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>;

const roles: UserRoles = {
  'user1': 'admin',
  'user2': 'user'
};
```

### ReturnType<T>
```typescript
function getUser() {
  return { id: '1', name: 'John' };
}

// Get return type of function
type UserType = ReturnType<typeof getUser>;
```

## Strict Type Checking Configuration

Ensure tsconfig.json has strict mode enabled:

```json
{
  "compilerOptions": {
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
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Common Patterns

### API Response Typing

**Bad:**
```typescript
async function fetchData(url: string) {
  const response = await fetch(url);
  return response.json();
}
```

**Good:**
```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  return response.json();
}

// Usage
const userResponse = await fetchData<User>('/api/user');
console.log(userResponse.data.name); // Fully typed
```

### Event Handlers

**Bad:**
```typescript
function handleClick(e) {
  console.log(e.target.value);
}
```

**Good:**
```typescript
function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
  console.log(e.currentTarget.value);
}

function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value);
}
```

### State Management

**Bad:**
```typescript
const [data, setData] = useState(null);
```

**Good:**
```typescript
const [data, setData] = useState<User | null>(null);

// Or with initial value
const [users, setUsers] = useState<User[]>([]);
```

### Props in React

**Bad:**
```typescript
function UserCard(props) {
  return <div>{props.name}</div>;
}
```

**Good:**
```typescript
interface UserCardProps {
  user: User;
  onClick?: (id: string) => void;
  className?: string;
}

function UserCard({ user, onClick, className }: UserCardProps) {
  return (
    <div className={className} onClick={() => onClick?.(user.id)}>
      {user.name}
    </div>
  );
}
```

## Error Handling with Types

**Bad:**
```typescript
try {
  const data = await fetchUser();
} catch (error) {
  console.log(error.message);
}
```

**Good:**
```typescript
try {
  const data = await fetchUser();
} catch (error) {
  if (error instanceof Error) {
    console.log(error.message);
  } else {
    console.log('Unknown error:', error);
  }
}

// Or create custom error types
class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public response?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

try {
  const data = await fetchUser();
} catch (error) {
  if (error instanceof ApiError) {
    console.log(`API Error ${error.statusCode}: ${error.message}`);
  } else if (error instanceof Error) {
    console.log('Error:', error.message);
  }
}
```

## Validation Checklist

Before committing TypeScript code:

- [ ] No "any" types anywhere
- [ ] All function parameters have explicit types
- [ ] All function return types are explicit
- [ ] Interfaces defined for all objects
- [ ] Proper null/undefined handling with `?` or union types
- [ ] Type guards used when narrowing unknown types
- [ ] Utility types used instead of "any"
- [ ] Strict mode enabled in tsconfig.json
- [ ] No implicit any errors
- [ ] All React props properly typed

## When to Use Each Approach

### Use Interfaces for:
- Object shapes
- API contracts
- Props definitions
- Extending types

```typescript
interface User {
  id: string;
  name: string;
}

interface AdminUser extends User {
  permissions: string[];
}
```

### Use Types for:
- Unions
- Intersections
- Primitives
- Tuples

```typescript
type Status = 'active' | 'inactive';
type ID = string | number;
type Point = [number, number];
type UserWithTimestamp = User & { timestamp: Date };
```

### Use Enums for:
- Fixed set of constants
- When you need reverse mapping

```typescript
enum UserRole {
  Admin = 'admin',
  User = 'user',
  Guest = 'guest'
}
```

## Rejection Criteria

**Reject pull requests that contain:**

- ❌ Any usage of `any` type without absolute justification
- ❌ Implicit any from missing type annotations
- ❌ Functions without return type declarations
- ❌ Untyped parameters
- ❌ Disabled TypeScript checks with `@ts-ignore` or `@ts-nocheck`
- ❌ Type assertions with `as any`

**Only accept `any` if:**
- Working with truly dynamic third-party library with no types
- Legacy code migration (temporary, must be documented)
- Extremely complex generic type that's impossible to express (rare)

**Even then, prefer:**
```typescript
// Instead of any
const data: unknown = thirdPartyLib.getData();

// Or create minimal interface
interface ThirdPartyData {
  [key: string]: unknown;
}
```

## Summary: Type Safety is Non-Negotiable

**Golden Rules:**
1. Never use "any" - use "unknown" and type guards
2. Always type function parameters and returns explicitly
3. Define interfaces for all data structures
4. Use utility types (Partial, Pick, Omit, etc.)
5. Enable strict mode in tsconfig.json
6. Type guards for narrowing unknown types
7. Specific types over broad types
8. Reject code with "any" types

**Remember:** Type safety catches bugs at compile time, not runtime. It's not optional—it's essential for maintainable code.
