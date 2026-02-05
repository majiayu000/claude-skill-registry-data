---
name: typescript-style
description: Automatic enforcement of TypeScript/JavaScript coding style, ESLint standards, type safety, and modern patterns. Use when writing TypeScript or React code to ensure strict type safety and modern ES2024+ patterns.
---

# TypeScript/JavaScript Style Best Practices Skill

This skill enforces TypeScript strict mode, ESLint standards, and modern patterns for frontend development.

## Core Standards

- **Strict TypeScript**: All strict flags enabled
- **ESLint**: Type-checked rules enabled
- **No `any`**: Use `unknown` or proper types
- **Explicit returns**: All functions typed

## Naming Conventions

```typescript
// Types/Interfaces: PascalCase
interface UserProfile { }

// Functions/variables: camelCase
function calculateTotal() { }
const userName = "john";

// Booleans: is/has/can/should prefix
const isLoading = true;
const hasPermission = false;
```

## Type Definitions

```typescript
// Prefer union types over enums
type Status = "pending" | "active" | "completed";

// Use as const for constant objects
const HttpStatus = {
  Ok: 200,
  NotFound: 404,
} as const;

// Discriminated unions
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };
```

## React Patterns

```typescript
// Typed props
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

// Typed hooks
const [isOpen, setIsOpen] = useState(false);

// Typed event handlers
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {};
```

## Function Length Guidelines

- **< 30 lines**: Ideal
- **30-50 lines**: Review for refactoring
- **> 50 lines**: Must be broken down

## Anti-Patterns to Avoid

- Using `any` type
- Missing return types
- Using `==` instead of `===`
- Unhandled promises
- Magic numbers/strings
- Vague variable/function names
