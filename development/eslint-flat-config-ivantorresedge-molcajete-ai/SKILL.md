---
name: eslint-flat-config
description: ESLint 9.x flat configuration patterns. Use when setting up ESLint with TypeScript.
---

# ESLint Flat Config Skill

This skill covers ESLint 9.x flat configuration for TypeScript projects.

## When to Use

Use this skill when:
- Setting up ESLint for TypeScript projects
- Migrating from legacy .eslintrc to flat config
- Configuring strict linting rules
- Integrating ESLint with Prettier

## Core Principle

**FLAT CONFIG IS THE FUTURE** - ESLint 9.x uses flat config (`eslint.config.ts`) by default.

## Basic Configuration

### eslint.config.ts

```typescript
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import type { Linter } from 'eslint';

const config: Linter.Config[] = [
  // Ignore patterns
  {
    ignores: ['dist/**', 'node_modules/**', 'coverage/**'],
  },

  // Base JavaScript rules
  js.configs.recommended,

  // TypeScript strict rules
  ...tseslint.configs.strictTypeChecked,

  // Custom rules for TypeScript files
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parserOptions: {
        project: './tsconfig.json',
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      // Type safety
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',
      '@typescript-eslint/no-unsafe-argument': 'error',

      // Code quality
      '@typescript-eslint/explicit-function-return-type': 'error',
      '@typescript-eslint/explicit-module-boundary-types': 'error',
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_' },
      ],

      // Strict boolean expressions
      '@typescript-eslint/strict-boolean-expressions': 'error',

      // No floating promises
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-misused-promises': 'error',
    },
  },
];

export default config;
```

## Installation

```bash
npm install -D eslint @eslint/js typescript-eslint
```

## Package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint --fix ."
  }
}
```

## Key Rules Explained

### Type Safety Rules

```typescript
// @typescript-eslint/no-explicit-any: 'error'
// ❌ Bad
function process(data: any) { }

// ✅ Good
function process(data: unknown) { }
```

```typescript
// @typescript-eslint/explicit-function-return-type: 'error'
// ❌ Bad
function add(a: number, b: number) {
  return a + b;
}

// ✅ Good
function add(a: number, b: number): number {
  return a + b;
}
```

```typescript
// @typescript-eslint/strict-boolean-expressions: 'error'
// ❌ Bad
if (value) { }

// ✅ Good
if (value !== undefined && value !== null) { }
if (typeof value === 'string' && value.length > 0) { }
```

### Promise Handling Rules

```typescript
// @typescript-eslint/no-floating-promises: 'error'
// ❌ Bad - Promise ignored
fetchData();

// ✅ Good - Promise handled
await fetchData();
// or
fetchData().catch(handleError);
// or
void fetchData(); // Explicitly ignored
```

```typescript
// @typescript-eslint/no-misused-promises: 'error'
// ❌ Bad - async function in non-async context
const handlers = {
  onClick: async () => { }, // Error in some contexts
};

// ✅ Good - wrap in non-async handler
const handlers = {
  onClick: () => {
    void handleClick();
  },
};
```

## ESLint with Prettier

### Installation

```bash
npm install -D eslint-config-prettier
```

### Configuration

```typescript
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import prettier from 'eslint-config-prettier';

const config = [
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  prettier, // Must be last to override other formatting rules
  {
    // Custom rules...
  },
];

export default config;
```

## File-Specific Configurations

```typescript
const config = [
  // All TypeScript files
  {
    files: ['**/*.ts', '**/*.tsx'],
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'error',
    },
  },

  // Test files - relaxed rules
  {
    files: ['**/*.test.ts', '**/*.test.tsx', '**/__tests__/**'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
    },
  },

  // Config files - CommonJS allowed
  {
    files: ['*.config.js', '*.config.cjs'],
    rules: {
      '@typescript-eslint/no-var-requires': 'off',
    },
  },
];
```

## Custom Rule Configurations

### Naming Conventions

```typescript
{
  rules: {
    '@typescript-eslint/naming-convention': [
      'error',
      // Variables: camelCase
      {
        selector: 'variable',
        format: ['camelCase', 'UPPER_CASE'],
      },
      // Types: PascalCase
      {
        selector: 'typeLike',
        format: ['PascalCase'],
      },
      // Interfaces: PascalCase, no I prefix
      {
        selector: 'interface',
        format: ['PascalCase'],
        custom: {
          regex: '^I[A-Z]',
          match: false,
        },
      },
      // Private members: underscore prefix
      {
        selector: 'memberLike',
        modifiers: ['private'],
        format: ['camelCase'],
        leadingUnderscore: 'require',
      },
    ],
  },
}
```

### Import Organization

```bash
npm install -D eslint-plugin-import
```

```typescript
import importPlugin from 'eslint-plugin-import';

const config = [
  {
    plugins: {
      import: importPlugin,
    },
    rules: {
      'import/order': [
        'error',
        {
          groups: [
            'builtin',
            'external',
            'internal',
            'parent',
            'sibling',
            'index',
          ],
          'newlines-between': 'always',
          alphabetize: { order: 'asc' },
        },
      ],
      'import/no-duplicates': 'error',
    },
  },
];
```

## Migration from Legacy Config

### Old .eslintrc.json

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

### New eslint.config.ts

```typescript
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
    },
  },
];
```

## Common Issues and Solutions

### "Parsing error: Cannot read file tsconfig.json"

```typescript
// Ensure tsconfigRootDir is set
{
  languageOptions: {
    parserOptions: {
      project: './tsconfig.json',
      tsconfigRootDir: import.meta.dirname,
    },
  },
}
```

### "Definition for rule not found"

```bash
# Ensure all plugins are installed
npm install -D @eslint/js typescript-eslint
```

### Files Not Being Linted

```typescript
// Check ignores pattern
{
  ignores: ['dist/**', 'node_modules/**'],
}

// Ensure files pattern includes your files
{
  files: ['**/*.ts', '**/*.tsx'],
}
```

## IDE Integration

### VS Code Settings

```json
{
  "eslint.useFlatConfig": true,
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

## Best Practices Summary

1. **Use TypeScript for eslint.config.ts**
2. **Enable strictTypeChecked rules**
3. **Put Prettier config last**
4. **Relax rules for test files**
5. **Set tsconfigRootDir properly**
6. **Use file-specific configurations**
7. **Configure VS Code for auto-fix**

## Code Review Checklist

- [ ] eslint.config.ts uses TypeScript
- [ ] strictTypeChecked rules enabled
- [ ] no-explicit-any set to error
- [ ] explicit-function-return-type enabled
- [ ] Prettier config is last
- [ ] Test files have relaxed rules
- [ ] Ignores dist and node_modules
