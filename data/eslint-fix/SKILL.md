---
name: eslint-fix
description: TypeScript/ESLint error fix guide, helps AI quickly locate and fix common lint errors, prioritizing auto-fix commands for formatting issues.
---

## Fix Workflow

### Step 1: Run Lint Command

Before manual fixes, **MUST run project lint command first**:

```bash
pnpm lint
```

These issues are auto-fixed, **no manual action needed**:
- Import order
- Code formatting
- Whitespace/indentation
- Trailing commas

### Step 2: Manually Fix Remaining Errors

## Common Fix Rules

### undefined Replacement

Use `void 0` instead of `undefined`:

```typescript
// bad
const value = undefined

// good
const value = void 0
```

### No End-of-Line Comments

Comments MUST be above statements, **absolutely forbidden** at line end:

```typescript
// bad
const name = 'test' // this is name

// good
// this is name
const name = 'test'
```

### Nullish Coalescing

Prefer `??` over `||`:

```typescript
// bad
const value = input || 'default'

// good
const value = input ?? 'default'
```

## Config Files

**Do NOT modify** `eslint.config.js` or `eslint.config.ts` unless necessary.

If config issues arise, only suggest modifications to user, do not edit config files directly.

## Error Troubleshooting Priority

1. Run `pnpm lint` for auto-fix
2. Check if above rules are violated
3. Read specific error messages to locate issues
4. If config adjustment needed, suggest user to modify manually
