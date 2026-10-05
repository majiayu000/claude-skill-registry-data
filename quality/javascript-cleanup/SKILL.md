---
name: javascript-cleanup
description: Remove unused exports, fix ESLint issues, modernize to ES6+, and clean up JavaScript/TypeScript codebases. Use when cleaning up JS/TS projects, removing.
---

# JavaScript/TypeScript Code Cleanup

Systematically identify and remove dead code, fix ESLint issues, and modernize legacy JavaScript patterns to maintain a clean, modern codebase.

## When to Use This Skill

Use this skill when you need to:

- Remove unused exports and dead code
- Fix ESLint/TSLint issues
- Modernize to ES6+ syntax
- Convert to TypeScript
- Clean up before code review

**Trigger phrases**: "cleanup JavaScript", "cleanup TypeScript", "remove dead code JS", "fix ESLint", "modernize JS", "ES6 migration"

## What This Skill Does

### Cleanup Areas

1. **Dead Code Removal**
   - Unused exports
   - Unreachable code
   - Unused variables/functions
   - Dead imports

2. **Style Compliance**
   - ESLint rules
   - Prettier formatting
   - Naming conventions

3. **TypeScript Migration**
   - Type annotations
   - Interface definitions
   - Strict mode compliance

4. **ES6+ Modernization**
   - Arrow functions
   - Template literals
   - Destructuring
   - async/await

## Instructions

### Step 1: Run Analysis Tools

```bash
# Install tools
npm install --save-dev eslint prettier typescript

# Find issues
npx eslint . --ext .js,.ts,.tsx
npx tsc --noEmit

# Check formatting
npx prettier --check "src/**/*.{js,ts,tsx}"
```

### Step 2: Fix Issues Automatically

```bash
# Fix ESLint issues
npx eslint . --fix

# Format code
npx prettier --write "src/**/*.{js,ts,tsx}"

# Remove unused dependencies
npx depcheck
```

### Step 3: Modernize Patterns

```javascript
// var → const/let
// Before
var name = 'John';
// After
const name = 'John';

// Function → Arrow function
// Before
function add(a, b) { return a + b; }
// After
const add = (a, b) => a + b;

// String concatenation → Template literals
// Before
const msg = 'Hello, ' + name + '!';
// After
const msg = `Hello, ${name}!`;

// Promise.then → async/await
// Before
getData().then(data => process(data)).catch(err => handle(err));
// After
try {
  const data = await getData();
  process(data);
} catch (err) {
  handle(err);
}

// Object property shorthand
// Before
const obj = { name: name, age: age };
// After
const obj = { name, age };

// Destructuring
// Before
const name = user.name;
const age = user.age;
// After
const { name, age } = user;
```

### Step 4: Add TypeScript Types

```typescript
// Before (JavaScript)
function processUser(user) {
  return user.name.toUpperCase();
}

// After (TypeScript)
interface User {
  name: string;
  email: string;
  age: number;
}

function processUser(user: User): string {
  return user.name.toUpperCase();
}
```

## Common Cleanup Targets

| Pattern | Before | After |
|---------|--------|-------|
| Variable declaration | `var x = 1` | `const x = 1` |
| Function | `function f() {}` | `const f = () => {}` |
| String concat | `'a' + b` | `` `a${b}` `` |
| Object method | `{ f: function() {} }` | `{ f() {} }` |
| Null check | `x !== null && x !== undefined` | `x != null` |

## Tools

- **ESLint**: Linting and auto-fix
- **Prettier**: Code formatting
- **TypeScript**: Type checking
- **depcheck**: Find unused dependencies

## Quality Checklist

- [ ] ESLint errors fixed
- [ ] Unused imports removed
- [ ] Modern syntax applied
- [ ] Types added (TypeScript)
- [ ] Formatting consistent
- [ ] Tests still pass

## Related Skills

- `code-review-quality` - Code quality assessment
- `generate-docstrings` - Add JSDoc documentation

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates code_cleanup/javascript_cleanup.md


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
