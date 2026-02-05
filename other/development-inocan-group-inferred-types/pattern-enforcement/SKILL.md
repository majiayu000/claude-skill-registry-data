---
name: pattern-enforcement
description: "Enforce architectural patterns with ESLint rules. Block infra imports, enforce object params, prevent server/client leaks."
version: 1.0.0
libraries: ["eslint-plugin-boundaries", "eslint-plugin-prefer-object-params", "eslint-plugin-no-server-imports"]
---

# Enforcing Patterns with ESLint

## Core Principle

Documentation is a ritual. Rules are enforcement. Patterns without rules that fail the build are just suggestions.

## Required ESLint Rules

### 1. Enforce Architectural Boundaries

Domain code must NOT import from infrastructure:

```typescript
// WRONG
import { db } from '../infra/database';

// CORRECT - Inject dependency
async function getUser(args, deps: { db: Database }) {
  return deps.db.findUser(args.userId);
}
```

**Simple approach** - Use `no-restricted-imports`:

```javascript
// eslint.config.mjs
export default {
  rules: {
    "no-restricted-imports": [
      "error",
      {
        patterns: [{
          group: ["**/infra/**"],
          message: "Domain code must not import from infra. Inject dependencies instead.",
        }],
      },
    ],
  },
};
```

**Better approach** - Use `eslint-plugin-boundaries` for directional rules:

```bash
npm install -D eslint-plugin-boundaries
```

```javascript
import boundaries from 'eslint-plugin-boundaries';

export default [{
  plugins: { boundaries },
  settings: {
    'boundaries/elements': [
      { type: 'domain', pattern: 'src/domain/**' },
      { type: 'infra', pattern: 'src/infra/**' },
      { type: 'api', pattern: 'src/api/**' },
    ],
  },
  rules: {
    'boundaries/element-types': ['error', {
      default: 'disallow',
      rules: [
        { from: 'domain', allow: ['domain'] },              // Domain is pure
        { from: 'infra', allow: ['domain', 'infra'] },      // Infra implements domain
        { from: 'api', allow: ['domain', 'infra', 'api'] }, // API wires everything
      ],
    }],
  },
}];
```

### 2. Enforce Function Signatures

Functions should use object parameters, not positional:

```typescript
// WRONG - Positional parameters
function createUser(name: string, email: string, age: number) { }

// CORRECT - Object parameter
function createUser(args: { name: string; email: string; age: number }) { }
```

```bash
npm install -D eslint-plugin-prefer-object-params
```

```javascript
import preferObjectParams from 'eslint-plugin-prefer-object-params';

export default [{
  plugins: { 'prefer-object-params': preferObjectParams },
  rules: {
    'prefer-object-params/prefer-object-params': 'error',
  },
}];
```

Rule ignores single-parameter functions, constructors, and test files by default.

### 3. Enforce Server/Client Boundaries

Prevent server code from leaking to client bundles:

```bash
npm install -D eslint-plugin-no-server-imports
```

```javascript
import noServerImports from 'eslint-plugin-no-server-imports';

export default [{
  plugins: { 'no-server-imports': noServerImports },
  rules: {
    'no-server-imports/no-server-imports': ['error', {
      serverFilePatterns: [
        '**/*.server.ts',
        '**/*.server.tsx',
        '**/server/**',
        '**/api/**',
      ],
    }],
  },
}];
```

Also block Node.js modules in client code:

```javascript
export default [{
  files: ['src/components/**/*.tsx', 'src/hooks/**/*.ts'],
  rules: {
    'import/no-nodejs-modules': ['error', { allow: [] }],
  },
}];
```

## Complete ESLint Config

```javascript
// eslint.config.mjs
import js from '@eslint/js';
import tseslint from '@typescript-eslint/eslint-plugin';
import tsparser from '@typescript-eslint/parser';
import preferObjectParams from 'eslint-plugin-prefer-object-params';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        ecmaVersion: 2022,
        sourceType: 'module',
        project: './tsconfig.json',
      },
      globals: { ...globals.node, ...globals.es2022 },
    },
    plugins: {
      '@typescript-eslint': tseslint,
      'prefer-object-params': preferObjectParams,
    },
    rules: {
      ...tseslint.configs.recommended.rules,

      // Architectural boundaries
      'no-restricted-imports': ['error', {
        patterns: [{
          group: ['**/infra/**'],
          message: 'Domain code must not import from infra.',
        }],
      }],

      // Function signatures
      'prefer-object-params/prefer-object-params': 'error',

      // TypeScript
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',

      // Code quality
      'prefer-const': 'error',
      'no-var': 'error',
      'object-shorthand': 'error',
      'prefer-template': 'error',
    },
  },
  {
    files: ['**/*.test.ts', '**/*.spec.ts'],
    rules: {
      'prefer-object-params/prefer-object-params': 'off',
    },
  },
];
```

## Essential Plugins

| Plugin | Purpose |
|--------|---------|
| `@typescript-eslint/eslint-plugin` | TypeScript-aware rules |
| `eslint-plugin-import` | Broken imports, circular deps |
| `eslint-plugin-unused-imports` | Auto-remove dead imports |
| `eslint-plugin-unicorn` | Modern, safer patterns |
| `eslint-plugin-boundaries` | Architectural boundaries |
| `eslint-plugin-prefer-object-params` | Object parameters |

## Migrating Existing Codebases

The `prefer-object-params` rule currently reports violations but doesn't auto-fix them (the transformation is too complex for safe automation—call sites need updating too).

For large-scale migrations, consider:

1. **Incremental adoption:** Start with `'warn'` and fix violations file-by-file
2. **Codemod scripts:** Use [jscodeshift](https://github.com/facebook/jscodeshift) to automate the transformation:

```javascript
// transform-to-object-params.js (jscodeshift)
export default function transformer(file, api) {
  const j = api.jscodeshift;
  // Transform function declarations with 2+ params to object pattern
  // ... (custom logic for your codebase)
}
```

```bash
npx jscodeshift -t transform-to-object-params.js src/**/*.ts
```

3. **AI-assisted refactoring:** Modern coding agents can batch-refactor functions when given clear rules

The key is that the ESLint rule *catches* violations. The migration strategy is separate from enforcement.

## Why Rules Matter for AI-Generated Code

Prompting is probabilistic - AI might follow patterns, might not.
Rules are deterministic - lint fails, code fails, agent fixes.

> If AI is writing code in your repo, constrain it with the same systems you already trust: linters, types, tests, and CI checks.

## The Rules

1. **Enforce architectural boundaries** - Block domain importing infra
2. **Enforce function signatures** - Require object parameters
3. **Enforce server/client separation** - Block Node.js in client code
4. **Use 'error' not 'warn'** - Violations must fail the build
