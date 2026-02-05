---
name: code-quality-management
description:
  Implements and enforces code quality gates for TypeScript/React projects. Use
  when setting up Biome/ESLint/TypeScript, configuring pre-commit hooks (Husky),
  fixing lint errors, or running quality checks. Examples - "setup code
  quality", "fix lint errors", "configure Biome", "run quality checks".
---

# Code Quality Management

You enforce code quality standards through automated checks: Biome for
formatting/linting, ESLint for React rules, TypeScript for type safety, Vitest
for unit tests, and Playwright for E2E tests.

## Quality Gates Workflow

Copy this checklist and track your progress:

```
Quality Gates Sequence:
- [ ] Step 1: Format code (Biome)
- [ ] Step 2: Lint code (ESLint + TypeScript)
- [ ] Step 3: Type check (TypeScript)
- [ ] Step 4: Run unit tests (Vitest)
- [ ] Step 5: Run E2E tests (Playwright)
```

**All-in-one quality check:**

```bash
npm run lint && npm run type-check && npm run test
```

## Quick Start

### Install dependencies

```bash
npm install -D @biomejs/biome eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D eslint-plugin-react-hooks eslint-plugin-react-refresh
npm install -D husky lint-staged vitest @playwright/test
```

### Configure package.json scripts

```json
{
  "scripts": {
    "build": "vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "lint:ci": "eslint . --ext ts,tsx --max-warnings 0",
    "format": "biome format --write .",
    "format:check": "biome format --write --dry-run .",
    "type-check": "tsc --noEmit",
    "test": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "prepare": "husky"
  }
}
```

### Setup Biome

Create `biome.json`:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "style": { "useImportType": "error", "useConst": "error" },
      "suspicious": { "noExplicitAny": "warn" },
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error"
      }
    }
  },
  "formatter": { "enabled": true }
}
```

See [BIOME.md](BIOME.md) for advanced configuration and import organization.

### Setup ESLint

Create `.eslintrc.cjs`:

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/no-explicit-any': 'warn',
    'react-hooks/rules-of-hook': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  },
};
```

See [ESLINT.md](ESLINT.md) for React-specific rules and customization.

### Setup TypeScript

Use strict mode in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "types": ["vite/client"]
  },
  "include": ["src"]
}
```

See [TYPESCRIPT.md](TYPESCRIPT.md) for advanced configuration and optimization.

### Setup Pre-commit Hooks

```bash
npx husky init
```

Update `.husky/pre-commit`:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
npm run lint:ci
```

Create `.lintstagedrc.json`:

```json
{
  "*.{ts,tsx}": [
    "biome check --write --no-errors-on-unmatched",
    "eslint --ext .ts,.tsx --fix --no-error-on-unmatched"
  ],
  "*.{js,jsx}": [
    "biome check --write --no-errors-on-unmatched",
    "eslint --fix --no-error-on-unmatched"
  ],
  "*.json": ["biome check --write"],
  "package.json": ["prettier --write"]
}
```

See [PRE-COMMIT.md](PRE-COMMIT.md) for advanced hook configuration and commit
message linting.

### Setup Testing

**Vitest** (`vitest.config.ts`):

```typescript
import { defineConfig } from 'vitest/config';
import path from 'path';
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: { provider: 'v8', reporter: ['text', 'html', 'lcov'] },
  },
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
});
```

**Playwright** (`playwright.config.ts`):

```typescript
import { defineConfig, devices } from '@playwright/test';
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  reporter: 'html',
  use: { baseURL: 'http://localhost:4173', trace: 'on-first-retry' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:4173',
    timeout: 120000,
  },
});
```

See [TESTING.md](TESTING.md) for comprehensive test setup, coverage
configuration, and E2E best practices.

## Daily Workflow

Copy and track this checklist:

```
Daily Development:
- [ ] Format during development: npm run format
- [ ] Fix lint issues: npm run lint:fix
- [ ] Run unit tests: npm run test:watch
- [ ] Before committing: npm run lint:ci && npm run type-check && npm run test
- [ ] Run E2E tests: npm run test:e2e
```

## Fixing Issues

**Quick fixes:**

```bash
npm run format          # Fix formatting
npm run lint:fix        # Fix linting
npm run type-check      # Check types
npm run test            # Run unit tests
npm run test:e2e        # Run E2E tests
```

**Full quality check:**

```bash
npm run lint && npm run type-check && npm run test
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## CI/CD Integration

GitHub Actions workflow (`.github/workflows/quality.yml`):

```yaml
name: Quality Checks
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run format:check
      - run: npm run lint:ci
      - run: npm run type-check
      - run: npm run test:coverage
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
        env: { CI: true }
```

## Quality Standards

**ALWAYS enforce:**

- No `any` types (use `unknown` with type guards)
- Strict TypeScript configuration
- Test coverage > 70%
- Pre-commit validation
- E2E testing for critical flows

**NEVER:**

- Skip quality gates before committing
- Commit with TypeScript/lint errors
- Use `any` type without justification
- Run Prettier on TS/JS files (use Biome instead)

## Reference Files

For detailed configuration, see:

- **[BIOME.md](BIOME.md)** - Advanced Biome configuration, import organization,
  rules
- **[ESLINT.md](ESLINT.md)** - ESLint setup, React rules, customization
- **[TYPESCRIPT.md](TYPESCRIPT.md)** - TypeScript strict mode, advanced options
- **[PRE-COMMIT.md](PRE-COMMIT.md)** - Husky setup, lint-staged, commit hooks
- **[TESTING.md](TESTING.md)** - Vitest and Playwright configuration
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## Common Patterns

### Running Tests

```bash
npm run test              # Unit tests
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report
npm run test:e2e          # E2E tests
npx playwright show-report # View test report
```

### Quality Gate Sequence

```bash
# During development
npm run format && npm run lint:fix

# Before commit
npm run lint:ci && npm run type-check && npm run test

# Full check (includes E2E)
npm run lint && npm run type-check && npm run test && npm run test:e2e
```

Remember: Code quality is not optional. Automated quality gates ensure
consistency and catch errors early.
