---
name: avoiding-angle-bracket-assertions
description: Avoid angle-bracket type assertions (<Type>) and use 'as Type' syntax instead
---

# Avoiding Angle-Bracket Type Assertions

The angle-bracket type assertion syntax (`<Type>value`) is deprecated in TypeScript, especially in TSX files where it conflicts with JSX syntax.

## Why Avoid `<Type>` Syntax

- **JSX conflict**: Incompatible with TSX files (React, Preact, etc.)
- **Inconsistent syntax**: Modern TypeScript uses `as Type`
- **Reduced readability**: Looks like generics or JSX
- **Tooling issues**: Some tools don't handle it well

## Modern Alternative: `as Type`

### Basic Replacement

**Deprecated:**
```typescript
const value = <string>someValue;
const num = <number>input;
```

**Modern:**
```typescript
const value = someValue as string;
const num = input as number;
```

### With Complex Types

**Deprecated:**
```typescript
const user = <User>jsonData;
const config = <AppConfig>settings;
```

**Modern:**
```typescript
const user = jsonData as User;
const config = settings as AppConfig;
```

## Better: Avoid Type Assertions Entirely

Type assertions bypass type checking and should be avoided when possible.

### 1. Use Type Guards Instead

**Bad:**
```typescript
function processValue(value: unknown) {
  const str = value as string;
  return str.toUpperCase();
}
```

**Good:**
```typescript
function processValue(value: unknown) {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  throw new Error('Expected string');
}
```

### 2. Use Validation Functions

**Bad:**
```typescript
const user = apiResponse as User;
```

**Good:**
```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    typeof value.id === 'number' &&
    typeof value.name === 'string'
  );
}

const parsed = apiResponse;
if (isUser(parsed)) {
  const user = parsed;
} else {
  throw new Error('Invalid user data');
}
```

### 3. Use Validation Libraries

**Best:**
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;

const user = UserSchema.parse(apiResponse);
```

### 4. Improve Type Inference

**Bad:**
```typescript
const element = document.getElementById('myId') as HTMLButtonElement;
```

**Better:**
```typescript
const element = document.getElementById('myId');
if (element instanceof HTMLButtonElement) {
  element.addEventListener('click', handler);
}
```

**Or use querySelector with type inference:**
```typescript
const element = document.querySelector<HTMLButtonElement>('#myId');
if (element) {
  element.addEventListener('click', handler);
}
```

### 5. Use Discriminated Unions

**Bad:**
```typescript
function handleEvent(event: Event) {
  const mouseEvent = event as MouseEvent;
  console.log(mouseEvent.clientX);
}
```

**Good:**
```typescript
type AppEvent =
  | { type: 'mouse'; clientX: number; clientY: number }
  | { type: 'keyboard'; key: string }
  | { type: 'custom'; data: unknown };

function handleEvent(event: AppEvent) {
  switch (event.type) {
    case 'mouse':
      console.log(event.clientX);
      break;
    case 'keyboard':
      console.log(event.key);
      break;
    case 'custom':
      console.log(event.data);
      break;
  }
}
```

## TSX-Specific Issues

In TSX files, angle-bracket syntax causes syntax errors:

**Will cause syntax error in TSX:**
```tsx
const Component = () => {
  const value = <string>getData();
  return <div>{value}</div>;
};
```

**Must use `as` syntax:**
```tsx
const Component = () => {
  const value = getData() as string;
  return <div>{value}</div>;
};
```

**Even better - validate properly:**
```tsx
const Component = () => {
  const data = getData();
  if (typeof data !== 'string') {
    throw new Error('Expected string');
  }
  return <div>{data}</div>;
};
```

## When Assertions Are Necessary

If you must use assertions (rare cases):

### 1. Use `as const` for Literal Types

```typescript
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
```

### 2. Use `as Type` (Never `<Type>`)

```typescript
const value = unknownValue as SomeType;
```

### 3. Document Why It's Safe

```typescript
const element = document.getElementById('app-root') as HTMLDivElement;
```

## Migration Strategy

1. **Find all angle-bracket assertions:**
   ```bash
   grep -r '<[A-Z][a-zA-Z]*>' --include="*.ts" --include="*.tsx"
   ```

2. **Replace with `as` syntax:**
   - `<Type>value` → `value as Type`

3. **Review each assertion:**
   - Can it be replaced with a type guard?
   - Can validation library be used?
   - Is it truly necessary?

4. **Enable linting:**
   ```json
   {
     "rules": {
       "@typescript-eslint/consistent-type-assertions": [
         "error",
         {
           "assertionStyle": "as",
           "objectLiteralTypeAssertions": "never"
         }
       ]
     }
   }
   ```

## ESLint Configuration

Enforce `as` syntax and discourage assertions:

```json
{
  "rules": {
    "@typescript-eslint/consistent-type-assertions": [
      "error",
      {
        "assertionStyle": "as",
        "objectLiteralTypeAssertions": "never"
      }
    ],
    "@typescript-eslint/no-unnecessary-type-assertion": "error"
  }
}
```

## Summary

**Never use angle-bracket syntax:**
- **Use** `as Type` when assertions are unavoidable
- **Prefer** type guards over assertions
- **Use** validation libraries for external data
- **Validate** at runtime for safety
- **Document** why assertions are necessary
- **Enable** linting to enforce consistency
