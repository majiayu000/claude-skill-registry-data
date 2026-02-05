---
name: post-prompt-finetune
description: Run automatically after completing any code changes. Validates TypeScript build, auto-fixes prettier and linting, then manually fixes any remaining issues.
---

# Post-Prompt Fine-Tune

Runs automatically after editing code.

## Purpose

This skill ensures code quality by automatically validating changes after every modification.

## When to Use

**AUTOMATICALLY after:**

- Creating new TypeScript files
- Modifying existing TypeScript files
- Refactoring code
- Adding features
- Fixing bugs

**Do NOT run for:**

- Reading files only
- Answering questions
- Documentation changes (unless they affect code)

## Steps

## Workflow

### Step 1: Build

```bash
npm run build
```

**If build fails:**

1. Read the TypeScript error messages carefully
2. Identify the file and line number
3. Understand what the error means
4. Fix the actual code issue (don't just add `// @ts-ignore`)
5. Re-run build
6. Repeat until build succeeds

**Common TypeScript Errors:**

- See `references/common-fixes.md` for solutions

This auto-fixes formatting. No manual action needed.

### Step 2: Lint Check

```bash
npm run lint
```

**If linting fails:**

1. Read each ESLint error carefully
2. Understand WHY the rule exists (see `references/eslint-rules.md`)
3. Fix the code properly (don't disable rules)
4. Run `npm run lint:fix` to auto-fix what's possible
5. Re-run `npm run lint`
6. Repeat until no errors remain

**Never:**

- Add `// eslint-disable` without understanding why
- Skip fixing errors
- Leave code in failing state
- Use `any` type

### Step 3: Auto-Format

```bash
npm run prettier:fix
```

### Step 4: Report

Report validation status clearly:

- ✅ What passed
- ❌ What failed and how you fixed it
- 📝 Summary of changes made

## Examples

### Example 1: Unused Variable

```
Error: 'user' is assigned a value but never used
```

**Bad Fix:**

```typescript
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const user = getUser();
```

**Good Fix:**

```typescript
// Remove if truly unused
// OR use it if it should be used
const user = getUser();
return user.name;
```

### Example 2: Missing Return Type

```
Error: Missing return type on function
```

**Fix:**

```typescript
// Before
function getUser() {
    return { name: 'John' };
}

// After
function getUser(): { name: string } {
    return { name: 'John' };
}
```

That's it.
