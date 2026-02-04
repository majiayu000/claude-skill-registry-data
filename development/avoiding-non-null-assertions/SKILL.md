---
name: avoiding-non-null-assertions
description: Avoid non-null assertion operator (!) and use type-safe alternatives instead
---

# Avoiding Non-Null Assertions

The non-null assertion operator (`!`) is deprecated in modern TypeScript because it bypasses type safety and can lead to runtime errors.

## Why Avoid `!`

- **Bypasses type safety**: Tells TypeScript "trust me" without verification
- **Runtime errors**: Can cause `undefined` or `null` errors at runtime
- **Maintenance burden**: Makes refactoring dangerous
- **No protection**: Removes TypeScript's main benefit

## Modern Alternatives

### 1. Optional Chaining (`?.`)

**Bad:**

```typescript
const userName = user!.profile!.name;
```

**Good:**

```typescript
const userName = user?.profile?.name;
```

### 2. Nullish Coalescing (`??`)

**Bad:**

```typescript
const value = config!.timeout;
```

**Good:**

```typescript
const value = config?.timeout ?? 5000;
```

### 3. Type Guards

**Bad:**

```typescript
function processUser(user: User | null) {
  console.log(user!.name);
}
```

**Good:**

```typescript
function processUser(user: User | null) {
  if (user !== null) {
    console.log(user.name);
  }
}
```

### 4. Early Return Pattern

**Bad:**

```typescript
function getUserEmail(userId: number): string {
  const user = findUser(userId);
  return user!.email;
}
```

**Good:**

```typescript
function getUserEmail(userId: number): string | null {
  const user = findUser(userId);
  if (!user) {
    return null;
  }
  return user.email;
}
```

### 5. Custom Type Guards

**Bad:**

```typescript
function handleValue(value: unknown) {
  return (value as User)!.name;
}
```

**Good:**

```typescript
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'name' in value;
}

function handleValue(value: unknown) {
  if (isUser(value)) {
    return value.name;
  }
  throw new Error('Invalid user');
}
```

### 6. Narrowing with `in` Operator

**Bad:**

```typescript
function process(obj: { data?: string }) {
  console.log(obj.data!.toUpperCase());
}
```

**Good:**

```typescript
function process(obj: { data?: string }) {
  if ('data' in obj && obj.data !== undefined) {
    console.log(obj.data.toUpperCase());
  }
}
```

### 7. Array Methods with Type Safety

**Bad:**

```typescript
const users: User[] = getUsers();
const firstUser = users[0]!;
```

**Good:**

```typescript
const users: User[] = getUsers();
const firstUser = users.at(0);
if (firstUser) {
  console.log(firstUser.name);
}
```

### 8. Assertion Functions (TypeScript 3.7+)

**Good:**

```typescript
function assertIsDefined<T>(value: T): asserts value is NonNullable<T> {
  if (value === undefined || value === null) {
    throw new Error('Value must be defined');
  }
}

function process(value: string | null) {
  assertIsDefined(value);
  console.log(value.toUpperCase());
}
```

## DOM Element Access

**Bad:**

```typescript
const button = document.getElementById('submit')!;
button.addEventListener('click', handler);
```

**Good:**

```typescript
const button = document.getElementById('submit');
if (button) {
  button.addEventListener('click', handler);
}
```

**Or with assertion function:**

```typescript
function assertElement<T extends Element>(
  element: T | null,
  selector: string
): asserts element is T {
  if (!element) {
    throw new Error(`Element not found: ${selector}`);
  }
}

const button = document.getElementById('submit');
assertElement(button, '#submit');
button.addEventListener('click', handler);
```

## When Is `!` Acceptable?

Only in very rare cases where:

1. You have exhaustively verified the value exists
2. There's no other way to express it to TypeScript
3. You document WHY it's safe

Even then, prefer assertion functions over `!`.

## Migration Strategy

1. **Search** for all uses of `!` in codebase
2. **Categorize** by pattern (DOM access, array indexing, etc.)
3. **Replace** with appropriate type-safe alternative
4. **Test** thoroughly after each replacement
5. **Enable linting** to prevent future uses

## Compiler Configuration

Enable strict checks:

```json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true
  }
}
```

## Summary

**Never use `!` operator:**

- Use `?.` for optional chaining
- Use `??` for default values
- Use type guards for narrowing
- Use assertion functions when validation is needed
- Let TypeScript protect you from null/undefined errors
