---
name: init-javascript-project
description: Initialize a complete JavaScript/TypeScript project with package.json, testing framework, bundler configuration, and documentation. Use when starting.
---

# Initialize JavaScript/TypeScript Project

Create a complete, production-ready JavaScript or TypeScript project with standard structure, configuration files, testing framework, and modern tooling.

## When to Use This Skill

Use this skill when you need to:

- Start a new JavaScript/TypeScript project
- Create Node.js applications or APIs
- Set up React/Vue/Angular frontend projects
- Build npm packages or libraries
- Configure modern build tools (Vite, webpack, esbuild)
- Establish testing with Jest/Vitest

**Trigger phrases**: "init javascript project", "new node project", "create typescript project", "npm init", "javascript boilerplate", "react project setup"

## What This Skill Does

### Project Structure Created

```
project-name/
├── src/                    # Source code
│   ├── index.ts           # Entry point
│   ├── types/             # TypeScript types
│   │   └── index.ts
│   └── utils/             # Utility functions
│       └── index.ts
├── tests/                  # Test files
│   └── index.test.ts
├── dist/                   # Build output (gitignored)
├── .github/               # GitHub workflows
│   └── workflows/
│       └── ci.yml
├── .gitignore             # Git ignore rules
├── .eslintrc.js           # ESLint configuration
├── .prettierrc            # Prettier configuration
├── jest.config.js         # Jest configuration
├── tsconfig.json          # TypeScript configuration
├── package.json           # Project manifest
├── CHANGELOG.md           # Version history
└── README.md              # Documentation
```

## Instructions

### Step 1: Gather Project Requirements

```
Project Details:
- Name: [project-name]
- Description: [one-line summary]
- Type: [Node.js CLI / Express API / React App / npm Package]
- Author: [name and email]
- License: [MIT / Apache-2.0 / ISC]

Dependencies:
- Runtime: [express, axios, lodash]
- Dev: [typescript, jest, eslint]

Features:
- [Key capability 1]
- [Key capability 2]
```

### Step 2: Initialize Package

```bash
# Create project directory
mkdir project-name && cd project-name

# Initialize package.json
npm init -y

# Create directories
mkdir -p src/types src/utils tests .github/workflows
```

### Step 3: Create package.json

```json
{
  "name": "project-name",
  "version": "0.1.0",
  "description": "Project description",
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "tsc",
    "build:watch": "tsc --watch",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src tests --ext .ts,.tsx",
    "lint:fix": "eslint src tests --ext .ts,.tsx --fix",
    "format": "prettier --write \"src/**/*.ts\" \"tests/**/*.ts\"",
    "typecheck": "tsc --noEmit",
    "clean": "rm -rf -- ./dist ./coverage",
    "prepublishOnly": "npm run build"
  },
  "keywords": [
    "typescript",
    "nodejs"
  ],
  "author": "Your Name <your.email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/username/project-name"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "devDependencies": {
    "@types/jest": "^29.5.0",
    "@types/node": "^20.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.45.0",
    "eslint-config-prettier": "^9.0.0",
    "eslint-plugin-prettier": "^5.0.0",
    "jest": "^29.6.0",
    "prettier": "^3.0.0",
    "ts-jest": "^29.1.0",
    "ts-node": "^10.9.0",
    "typescript": "^5.1.0"
  },
  "dependencies": {}
}
```

### Step 4: Create TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    // Language and Environment
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",

    // Output
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Strict Type Checking
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "alwaysStrict": true,

    // Additional Checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,

    // Other
    "skipLibCheck": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

### Step 5: Create ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    project: './tsconfig.json',
  },
  plugins: ['@typescript-eslint', 'prettier'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:prettier/recommended',
  ],
  env: {
    node: true,
    es2022: true,
    jest: true,
  },
  rules: {
    // TypeScript
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/prefer-nullish-coalescing': 'error',
    '@typescript-eslint/prefer-optional-chain': 'error',

    // General
    'no-console': 'warn',
    'no-debugger': 'error',
    'prefer-const': 'error',
    'no-var': 'error',

    // Prettier integration
    'prettier/prettier': 'error',
  },
  ignorePatterns: ['dist/', 'node_modules/', 'coverage/', '*.js'],
};
```

### Step 6: Create Prettier Configuration

```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

### Step 7: Create Jest Configuration

```javascript
// jest.config.js
/** @type {import('jest').Config} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests', '<rootDir>/src'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  transform: {
    '^.+\\.tsx?$': [
      'ts-jest',
      {
        tsconfig: 'tsconfig.json',
      },
    ],
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/types/**/*',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  verbose: true,
};
```

### Step 8: Create Source Files

```typescript
// src/index.ts
/**
 * Project Name - Main Entry Point
 *
 * @packageDocumentation
 */

export { greet, VERSION } from './utils';
export type { GreetOptions } from './types';

/**
 * Main function
 */
export function main(): void {
  console.log('Project Name v0.1.0');
  console.log('='.repeat(50));
  console.log('Project initialized successfully!');
}

// Run if executed directly
if (require.main === module) {
  main();
}
```

```typescript
// src/types/index.ts
/**
 * Type definitions for Project Name
 */

export interface GreetOptions {
  name: string;
  greeting?: string;
}

export interface Config {
  debug: boolean;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
}
```

```typescript
// src/utils/index.ts
/**
 * Utility functions
 */

import type { GreetOptions } from '../types';

export const VERSION = '0.1.0';

/**
 * Generate a greeting message
 */
export function greet(options: GreetOptions): string {
  const { name, greeting = 'Hello' } = options;
  return `${greeting}, ${name}!`;
}

/**
 * Check if value is defined
 */
export function isDefined<T>(value: T | undefined | null): value is T {
  return value !== undefined && value !== null;
}
```

### Step 9: Create Tests

```typescript
// tests/index.test.ts
import { greet, VERSION } from '../src';

describe('greet', () => {
  it('should return greeting with default message', () => {
    const result = greet({ name: 'World' });
    expect(result).toBe('Hello, World!');
  });

  it('should return greeting with custom message', () => {
    const result = greet({ name: 'World', greeting: 'Hi' });
    expect(result).toBe('Hi, World!');
  });
});

describe('VERSION', () => {
  it('should be defined', () => {
    expect(VERSION).toBeDefined();
    expect(typeof VERSION).toBe('string');
  });
});
```

### Step 10: Create .gitignore

```
# Dependencies
node_modules/

# Build output
dist/
build/
*.tsbuildinfo

# Test coverage
coverage/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Logs
logs/
*.log
npm-debug.log*

# Cache
.npm/
.eslintcache
```

### Step 11: Create CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run typecheck

      - name: Test
        run: npm run test:coverage

      - name: Build
        run: npm run build
```

### Step 12: Install and Verify

```bash
# Install dependencies
npm install

# Run linting
npm run lint

# Run type check
npm run typecheck

# Run tests
npm test

# Build
npm run build

# Run application
npm start
```

## Project Type Variations

### Express API

```json
// Additional dependencies
{
  "dependencies": {
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "morgan": "^1.10.0",
    "dotenv": "^16.0.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.0",
    "@types/cors": "^2.8.0",
    "@types/morgan": "^1.9.0",
    "supertest": "^6.3.0",
    "@types/supertest": "^2.0.0"
  }
}
```

### React Application

```bash
# Use Vite for React
npm create vite@latest project-name -- --template react-ts
```

### npm Package

```json
// package.json additions
{
  "main": "dist/cjs/index.js",
  "module": "dist/esm/index.js",
  "types": "dist/types/index.d.ts",
  "exports": {
    ".": {
      "require": "./dist/cjs/index.js",
      "import": "./dist/esm/index.js",
      "types": "./dist/types/index.d.ts"
    }
  },
  "sideEffects": false
}
```

## Quality Checklist

- [ ] package.json configured
- [ ] TypeScript compiles without errors
- [ ] ESLint passes
- [ ] Prettier formatting applied
- [ ] Tests pass with coverage
- [ ] CI workflow configured
- [ ] Documentation complete
- [ ] Git initialized
- [ ] README accurate

## Related Skills

- `test-structure` - Set up comprehensive testing
- `javascript-cleanup` - Code cleanup
- `api-documentation` - Document APIs
- `code-commit-workflow` - Git workflow

---

**Version**: 1.0.0
**Last Updated**: December 2025


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
