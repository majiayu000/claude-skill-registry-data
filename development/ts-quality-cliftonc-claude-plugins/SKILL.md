---
name: ts-quality
description: Enforce TypeScript quality standards immediately after writing or modifying .ts/.tsx files. Run type checking and linting on each changed file for instant feedback. Use after creating/editing TypeScript files, or when quality checks, typecheck, lint, or validate are mentioned.
---

# TypeScript Quality Enforcement

This skill helps maintain TypeScript code quality by running instant checks on each file after it's written or modified.

## What This Skill Does

When activated, this skill ensures TypeScript code meets quality standards by:

1. **Type Checking** - Runs `pnpm exec tsc --noEmit <file>` to ensure zero TypeScript type errors
2. **Linting** - Runs `pnpm lint <file>` to enforce code style consistency

Checks run on the SPECIFIC FILE that was just written/modified, not the entire project.

## When to Use This Skill

Activate this skill:

- **Immediately after writing or modifying any .ts or .tsx file**
- After creating new TypeScript files
- After editing existing TypeScript files
- When user mentions: "quality checks", "typecheck", "lint", "validate code"
- Before creating git commits
- During code review processes

## Quality Standards

**ZERO TOLERANCE POLICY**: No lint errors or type errors are acceptable.

### Required Checks (in sequence):

1. **Type Checking** - File-scoped typecheck
   - Must pass with zero errors
   - Validates TypeScript type safety for the specific file

2. **Linting** - File-scoped lint
   - Must pass with zero errors
   - Enforces consistent code formatting and style

## Instructions

When this skill is active, follow these steps:

### 1. Announce Activation

Immediately inform the user that quality checks are running:

```
🔍 Checking {filename}...
```

Replace `{filename}` with the actual file path (e.g., `src/utils/auth.ts`).

### 2. Identify the File to Check

Determine which TypeScript file was just written or modified. This is the file to check.

### 3. Run File-Scoped Quality Checks

Execute checks sequentially on the SPECIFIC FILE ONLY:

```bash
# Type check the specific file
pnpm exec tsc --noEmit path/to/file.ts

# Lint the specific file
pnpm lint path/to/file.ts
```

**Important**:
- Only check the file that was written/modified
- Do NOT run project-wide checks
- Each command must succeed before the next runs

### 4. Report Results

**If all checks pass:**
Report success clearly:
```
✓ {filename}: typecheck and lint passed
```

**If any check fails:**
- Report the specific errors with line numbers
- Format: `✗ {filename}: found N errors`
- Show the actual error messages
- DO NOT proceed to subsequent checks
- DO NOT allow commits with failing checks
- Fix the errors before continuing

## Type Safety Guidelines

### DO:

- Use explicit types for function parameters and return values
- Leverage TypeScript's type inference for simple variable assignments
- Use `unknown` instead of `any` when the type is truly unknown
- Define interfaces for object shapes
- Use type guards for runtime validation of external data
- Document complex types with JSDoc comments

### DO NOT:

- Use `any` without explicit justification in comments
- Ignore TypeScript errors (no `@ts-ignore` without explanation)
- Skip typecheck before committing
- Commit code with lint errors
- Use `@ts-expect-error` to suppress valid errors
- Bypass quality checks "just this once"

## Examples

### Example 1: Creating New TypeScript File

**User**: "Create a new TypeScript component for user authentication"

**Actions**:
1. Create the file with proper types (explicit parameter and return types)
2. Avoid using `any` types
3. After file creation, immediately run quality checks:
   - Announce: `🔍 Checking src/components/Auth.tsx...`
   - Run: `pnpm exec tsc --noEmit src/components/Auth.tsx`
   - Run: `pnpm lint src/components/Auth.tsx`
   - Report: `✓ src/components/Auth.tsx: typecheck and lint passed`
4. Only consider the task complete when checks pass

### Example 2: Modifying Existing Code

**User**: "Update the session processing logic to handle new event types"

**Actions**:
1. Make changes to the file maintaining type safety
2. After saving the file, immediately run quality checks:
   - Announce: `🔍 Checking packages/session/src/processor.ts...`
   - Run: `pnpm exec tsc --noEmit packages/session/src/processor.ts`
   - Run: `pnpm lint packages/session/src/processor.ts`
   - Report results:
     - If passed: `✓ packages/session/src/processor.ts: typecheck and lint passed`
     - If failed: `✗ packages/session/src/processor.ts: found 2 errors` (then show errors)

### Example 3: File with Errors

**User**: Writes a file with type errors

**Actions**:
1. Announce: `🔍 Checking src/utils/helper.ts...`
2. Run typecheck: `pnpm exec tsc --noEmit src/utils/helper.ts`
3. Detect errors and report:
   ```
   ✗ src/utils/helper.ts: found 3 errors

   src/utils/helper.ts:15:5 - error TS2322: Type 'string' is not assignable to type 'number'.
   src/utils/helper.ts:22:10 - error TS2339: Property 'foo' does not exist on type 'User'.
   src/utils/helper.ts:35:3 - error TS2345: Argument of type 'null' is not assignable to parameter of type 'string'.
   ```
4. Do NOT proceed to lint
5. Wait for user to fix errors

## Integration with pnpm Workspaces

This skill works with pnpm workspace monorepos by checking individual files in their packages.

File-scoped checks work across packages without needing to change directories.

## Quick Reference Commands

```bash
# File-scoped typecheck (fast, targeted)
pnpm exec tsc --noEmit path/to/file.ts

# File-scoped lint
pnpm lint path/to/file.ts

# Both checks in sequence
pnpm exec tsc --noEmit path/to/file.ts && pnpm lint path/to/file.ts
```

## Error Handling

When errors occur:

1. **Type Errors**: Show the file, line number, and error message
2. **Lint Errors**: Show the file, line number, rule violated, and how to fix

Always provide actionable information to help fix the errors.

## Best Practices

- **Check after every file write** - Instant feedback prevents accumulating errors
- **Fix errors immediately** - Don't accumulate technical debt
- **Type errors first** - Must be resolved before linting
- **Never commit failing code** - No exceptions
- **File-scoped only** - Don't run project-wide checks
- **Pragmatic quality** - Focus on correctness, not perfection

## Requirements

This skill requires projects to have:

- **pnpm** installed
- **TypeScript** installed and configured
- **Linter** (Biome, ESLint, or similar) configured

The skill uses:
- `pnpm exec tsc --noEmit <file>` for type checking
- `pnpm lint <file>` for linting
