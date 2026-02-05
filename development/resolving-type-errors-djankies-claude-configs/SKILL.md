---
name: resolving-type-errors
description: Resolve all TypeScript errors using root cause analysis, targeted fixes, and mandatory validation
---

Project configuration:
read tsconfig.json if haven't already
read package.json if haven't already

## 1. Comprehensive Error Discovery

Run type check and collect all errors for the target file:

```bash
pnpm type-check 2>&1 | grep "target-file"
```

Replace `target-file` with the actual file path from the user's request.

List all errors with:

- File path and line numbers
- Error codes (TS####)
- Full error descriptions
- Related information

Prioritize errors by dependency order:

- Base type definition errors first
- Cascading errors after root causes
- Independent errors in parallel

## 2. Root Cause Analysis

Read the target file specified by the user.

For each error, trace to underlying cause:

**Verify type structures from source**:

- Check imported type definitions
- Verify function signatures
- Confirm interface/type shapes
- Validate generic constraints

**Identify root cause categories**:

- Type annotation errors (wrong type specified)
- Type narrowing failures (missing guards)
- Generic constraint violations (needs extends)
- Null/undefined unsafety (missing checks)
- Function signature mismatches (args/return)
- Import/export type issues (wrong imports)

**Consider impact on dependent code**:

- Will fix break other code?
- Are there cascading implications?
- Does this affect public API?

## 3. Resolution Implementation

Apply targeted fixes using Edit tool.

### Type Safety Patterns

**For type narrowing**:

```typescript
if (typeof value === 'string') {
}
if (value !== null && value !== undefined) {
}
if ('property' in object) {
}
if (Array.isArray(value)) {
}
```

**For generic constraints**:

```typescript
function process<T extends SomeType>(value: T): void {}
```

**For union discrimination**:

```typescript
type Result = { success: true; data: Data } | { success: false; error: Error };

if (result.success) {
  result.data;
} else {
  result.error;
}
```

**For null safety**:

```typescript
value?.property;
value ?? defaultValue;
const nonNull = value!;
```

**For unknown types**:

```typescript
function parse(input: unknown): Result {
  if (typeof input !== 'object' || input === null) {
    throw new Error('Invalid input');
  }

  const obj = input as Record<string, unknown>;

  if (typeof obj.property !== 'string') {
    throw new Error('Invalid property');
  }

  return { property: obj.property };
}
```

### Principles

**Minimal changes**:

- Fix only what's broken
- Preserve existing logic
- Maintain code structure

**Address root causes**:

- Don't suppress symptoms
- Fix source of error, not just error site
- Consider why type system caught this

**Maintain consistency**:

- Follow project patterns
- Use existing type definitions
- Match naming conventions

**Prefer interfaces over types** (for objects):

```typescript
interface User {
  id: string;
  name: string;
}
```

**Use type aliases for unions/primitives**:

```typescript
type Status = 'pending' | 'complete' | 'error';
type ID = string;
```

**Use unknown over any**:

```typescript
const data: unknown = JSON.parse(input);
```

## 4. Validation

Run type check after fixes on the target file:

```bash
pnpm type-check 2>&1 | grep "target-file"
```

Replace `target-file` with the actual file path.

**Success criteria**: MUST show zero TypeScript errors

**If errors remain**:

1. Analyze remaining errors
2. Identify if new errors introduced
3. Apply additional fixes
4. Re-run validation
5. Iterate until clean

**NEVER leave file in broken state**

</task>

<constraints>
**Type Safety Requirements:**
- NEVER use `any` type (use `unknown` + guards)
- NEVER use `@ts-ignore` or `@ts-expect-error`
- ALWAYS verify type structures from source
- ALWAYS preserve type safety during fixes
- MUST add type guards for narrowing
- MUST use generic constraints appropriately

**Code Quality Requirements:**

- MUST maintain existing code structure
- MUST follow project naming conventions
- MUST apply minimal changes to resolve errors
- NEVER introduce breaking changes
- NEVER change runtime behavior

**Resolution Requirements:**

- Address root causes, not symptoms
- Fix cascading errors in dependency order
- Iterate until zero errors remain
- Validate after every batch of fixes
  </constraints>

<validation>
**MANDATORY Validation**:

```bash
pnpm type-check 2>&1 | grep "target-file"
```

Replace `target-file` with the actual file path. Must show zero errors or report "No errors found".

**File Integrity**:

- Verify syntactically valid TypeScript
- Ensure imports/exports correct
- Confirm no runtime behavior changes

**Failure Handling**:

- If validation fails, analyze remaining errors
- Apply additional fixes
- Re-run validation until all checks pass
- NEVER mark complete with errors remaining
  </validation>

<output>
Provide clear summary of resolution:

## Resolution Summary

- **Errors resolved**: {count}
- **Changes made**: {summary}
- **Files modified**: {list}

## Changes Applied

For each fix:

### Fix {n}: {error category}

**Location**: `{file}:{line}`

**Original error**:

```
{TypeScript error message}
```

**Change made**:

```typescript
{Code change applied}
```

**Rationale**:
{Why this fix resolves the error}

## Validation Results

```
{Output of type check showing zero errors}
```

✅ All TypeScript errors resolved
✅ Type safety maintained
✅ Zero errors remaining

## Remaining Considerations

- {Any follow-up improvements to consider}
- {Type refactoring opportunities}
- {Long-term type safety enhancements}
  </output>
