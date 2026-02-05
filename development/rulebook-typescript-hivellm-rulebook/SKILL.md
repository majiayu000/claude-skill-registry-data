---
name: rulebook-typescript
description: TypeScript development with strict mode, Vitest testing, ESLint linting, and CI/CD best practices. Use when working on TypeScript projects, writing tests, configuring linting, or setting up build pipelines.
version: "1.0.0"
category: languages
author: "HiveLLM"
tags: ["typescript", "javascript", "node", "strict", "testing", "vitest", "eslint"]
dependencies: []
conflicts: []
---

# TypeScript Development Standards

## Quality Check Commands

Run these commands after every implementation:

```bash
npm run type-check        # TypeScript type checking
npm run lint              # ESLint (0 warnings required)
npm run format            # Prettier formatting
npm test                  # Run all tests
npm run test:coverage     # Coverage check (95%+ required)
npm run build             # Build verification
```

## TypeScript Configuration

Use TypeScript 5.3+ with strict mode:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true
  }
}
```

## Code Quality Rules

1. **No `any` type** - Use `unknown` with type guards
2. **Strict null checks** - Handle null/undefined explicitly
3. **Type guards over assertions** - Avoid `as` keyword
4. **95%+ test coverage** - Required for all new code

## Testing with Vitest

```typescript
import { describe, it, expect } from 'vitest';

describe('myFunction', () => {
  it('should handle valid input', () => {
    expect(myFunction('input')).toBe('expected');
  });
});
```

## ESLint Setup

```json
{
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  "parser": "@typescript-eslint/parser",
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/no-explicit-any": "warn"
  }
}
```
