---
name: forge-lang-node
description: Node.js development standards including jest/vitest, eslint, and prettier. Use when working with JavaScript files, package.json, or npm/pnpm.
---

# Node.js Development

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
│   ├── index.js
│   └── module.js
├── tests/
│   └── module.test.js
├── package.json
└── README.md
```

## package.json Scripts

```json
{
  "scripts": {
    "test": "jest",
    "lint": "eslint src/",
    "format": "prettier --write .",
    "check": "npm run lint && npm run test"
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
