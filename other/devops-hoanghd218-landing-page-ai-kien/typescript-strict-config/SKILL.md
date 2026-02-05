---
name: typescript-strict-config
description: Strict TypeScript configuration with all safety flags enabled. Use when initializing TypeScript projects or enforcing type safety.
---

# TypeScript Strict Configuration Skill

This skill defines the strictest possible TypeScript configuration for maximum type safety.

## When to Use

Use this skill when:
- Initializing new TypeScript projects
- Upgrading existing projects to strict mode
- Enforcing zero-tolerance type safety
- Reviewing TypeScript configurations

## Core Principle

**ZERO TOLERANCE FOR `any` TYPES** - Every value must have an explicit, meaningful type.

## tsconfig.json Template

```json
{
  "compilerOptions": {
    // Language & Environment
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",

    // Emit
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "removeComments": false,
    "importHelpers": true,

    // Interop Constraints
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,

    // Type Checking - ALL STRICT FLAGS
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "alwaysStrict": true,

    // Additional Checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "exactOptionalPropertyTypes": true,

    // Completeness
    "skipLibCheck": false,
    "skipDefaultLibCheck": false
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Key Flags Explained

### Mandatory Strict Flags

- **strict: true** - Enables all strict type checking options
- **noImplicitAny: true** - Error on expressions/declarations with implied `any` type
- **strictNullChecks: true** - Null and undefined are not assignable to other types
- **strictFunctionTypes: true** - Function parameters are checked contravariantly
- **strictBindCallApply: true** - Type-check bind, call, and apply methods
- **strictPropertyInitialization: true** - Class properties must be initialized
- **noImplicitThis: true** - Error on `this` expressions with implied `any` type
- **useUnknownInCatchVariables: true** - Catch clause variables are `unknown` (not `any`)

### Additional Safety Flags

- **noUncheckedIndexedAccess: true** - Array/index access returns `T | undefined`
- **noImplicitReturns: true** - Error when not all code paths return a value
- **noFallthroughCasesInSwitch: true** - Error on fallthrough cases in switch statements
- **noUnusedLocals: true** - Error on unused local variables
- **noUnusedParameters: true** - Error on unused function parameters
- **exactOptionalPropertyTypes: true** - Enforce exact optional property types
- **noPropertyAccessFromIndexSignature: true** - Require bracket notation for index signatures

## Package.json Scripts

```json
{
  "scripts": {
    "type-check": "tsc --noEmit",
    "type-check:watch": "tsc --noEmit --watch",
    "build": "tsc",
    "clean": "rm -rf dist"
  }
}
```

## Common Patterns

### Handling Unknown Types

**BAD:**
```typescript
function process(data: any) {  // ❌
  return data.value;
}
```

**GOOD:**
```typescript
function isValidData(value: unknown): value is { value: string } {
  return (
    typeof value === 'object' &&
    value !== null &&
    'value' in value &&
    typeof (value as Record<string, unknown>).value === 'string'
  );
}

function process(data: unknown): string {
  if (!isValidData(data)) {
    throw new Error('Invalid data');
  }
  return data.value;
}
```

### Handling Array Access

With `noUncheckedIndexedAccess: true`, array access returns `T | undefined`:

```typescript
const numbers: number[] = [1, 2, 3];

// ❌ Type error - value is number | undefined
const first: number = numbers[0];

// ✅ Explicit check
const first = numbers[0];
if (first !== undefined) {
  console.log(first.toFixed(2));
}

// ✅ Using optional chaining
console.log(numbers[0]?.toFixed(2));

// ✅ Using assertion (only if guaranteed)
const firstAsserted = numbers[0]!;
```

### Handling Null/Undefined

```typescript
// ❌ Implicit null
let name: string = null;  // Error with strictNullChecks

// ✅ Explicit null
let name: string | null = null;

// ✅ Narrowing
if (name !== null) {
  console.log(name.toUpperCase());
}

// ✅ Optional chaining
console.log(name?.toUpperCase());

// ✅ Nullish coalescing
const displayName = name ?? 'Anonymous';
```

### Catch Clause Variables

With `useUnknownInCatchVariables: true`:

```typescript
// ❌ Old way (error is `any`)
try {
  riskyOperation();
} catch (error) {
  console.log(error.message);  // Unsafe
}

// ✅ New way (error is `unknown`)
try {
  riskyOperation();
} catch (error) {
  if (error instanceof Error) {
    console.log(error.message);
  } else {
    console.log('Unknown error:', error);
  }
}
```

### Function Return Types

```typescript
// ❌ Missing return type
function calculate(x: number) {
  return x * 2;
}

// ✅ Explicit return type
function calculate(x: number): number {
  return x * 2;
}

// ✅ Async function
async function fetchData(id: string): Promise<Data> {
  const response = await fetch(`/api/data/${id}`);
  return response.json() as Promise<Data>;
}
```

## ESLint Integration

Add TypeScript ESLint rules to enforce strict typing:

```typescript
// eslint.config.ts
import tseslint from 'typescript-eslint';

export default tseslint.config(
  ...tseslint.configs.strictTypeChecked,
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',
      '@typescript-eslint/explicit-function-return-type': 'error',
      '@typescript-eslint/explicit-module-boundary-types': 'error',
    },
  },
);
```

## Upgrading Existing Projects

1. Add strict flags incrementally
2. Start with `strict: true`
3. Fix all errors
4. Add additional flags one by one
5. Use `// @ts-expect-error` with justification for unavoidable cases

## Code Review Checklist

- [ ] No `any` types (explicit or implicit)
- [ ] All functions have explicit return types
- [ ] All parameters have explicit types
- [ ] Proper null/undefined handling
- [ ] Array access checked for undefined
- [ ] Catch clauses handle unknown error type
- [ ] No `// @ts-ignore` without justification

## Notes

- Never disable strict flags to make code compile
- Use `unknown` instead of `any` for truly unknown types
- Write type guards for runtime type checking
- All new projects MUST use this configuration
- Zero tolerance for `any` types
