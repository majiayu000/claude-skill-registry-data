---
name: forge-lang-typescript
description: TypeScript development standards including type checking, jest/vitest, eslint, and prettier. Use when working with TypeScript files, tsconfig.json, or .ts/.tsx files.
---

# TypeScript Development

## Type Checking

```bash
# Check types without emitting
npx tsc --noEmit

# Watch mode
npx tsc --noEmit --watch
```

## Testing

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific test
npm test -- --testPathPattern=module.test
```

## Linting

```bash
# Run eslint
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix

# Type-aware linting (if configured)
npx eslint --ext .ts,.tsx src/
```

## Formatting

```bash
# Format with prettier
npm run format

# Check without changing
npx prettier --check .
```

## Project Structure

```
project/
├── src/
│   ├── index.ts
│   ├── types.ts
│   └── module.ts
├── tests/
│   └── module.test.ts
├── package.json
├── tsconfig.json
└── README.md
```

## tsconfig.json Template

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## package.json Scripts

```json
{
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit",
    "check": "npm run typecheck && npm run lint && npm run test"
  }
}
```

## TDD Cycle Commands

```bash
# RED: Write test, run to see it fail
npm test -- --testPathPattern=new_feature

# GREEN: Implement, run to see it pass
npm test -- --testPathPattern=new_feature

# REFACTOR: Clean up, ensure tests still pass
npm run check
```
