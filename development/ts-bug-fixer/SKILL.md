---
name: ts-bug-fixer
description: Automatically fix TypeScript compilation errors, type mismatches, and type inference issues. Use when TypeScript compiler shows errors or when type definitions need correction.
version: 1.0.0
---

# TypeScript Bug Fixer

Specialized skill for diagnosing and fixing TypeScript compilation errors, type mismatches, discriminated unions, and complex type inference issues.

## Two Ways to Use This Skill

1. **Direct Fix Mode**: User provides specific code snippet with error message - skill analyzes and proposes solution
2. **Project-Wide Mode**: User asks to fix all TypeScript errors - skill runs compiler and fixes systematically

## When to Use This Skill

Invoke this skill when:
- User provides code with TypeScript errors directly
- User asks to fix specific TypeScript type issues
- User wants to understand why their TypeScript code doesn't compile
- User provides error messages from the TypeScript compiler
- User wants to check and fix all TypeScript errors in the project

## Core Capabilities

1. **Type Error Analysis**: Parse and understand TypeScript error messages
2. **Union Type Fixes**: Handle discriminated unions and conditional types
3. **Type Guards**: Add proper type narrowing and guards
4. **Generic Resolution**: Fix complex generic type inference issues
5. **Null Safety**: Resolve optional chaining and nullability issues

## Workflow

### Mode 1: Fix Specific Code Provided by User

When the user provides code and error message directly:

1. **Analyze the Error**: Read the error message carefully to understand:
   - What TypeScript expects
   - What it found instead
   - The root cause of the mismatch

2. **Understand Context**: Ask clarifying questions if needed:
   - What is the intended behavior?
   - Are there related types or interfaces?
   - What should the function/component accept/return?

3. **Propose Solution**: Explain the fix and provide corrected code with explanations

4. **Apply Fix**: If in a file, use `Edit` tool to apply the fix

### Mode 2: Project-Wide TypeScript Error Fix

When user wants to fix all TypeScript errors in the project:

#### Step 1: Gather TypeScript Errors

Run the TypeScript compiler to collect all errors:

```bash
pnpm ts
# or
npm run type-check
# or
tsc --noEmit
```

Parse the output to extract:
- File paths
- Line numbers
- Error codes (e.g., TS2322, TS2345)
- Error messages

#### Step 2: Categorize Errors

Group errors by type and priority:

**High Priority (blocking):**
- Type mismatches in function returns
- Missing required properties
- Incorrect generic constraints
- Module resolution failures

**Medium Priority:**
- Union type discrimination issues
- Implicit any types
- Unused variables/imports

**Low Priority:**
- Style/convention issues
- Non-critical type narrowing

#### Step 3: Read Affected Files

Use `Read` tool to examine files with errors. Focus on:
- The error location and surrounding context
- Type definitions and interfaces
- Import statements
- Related type dependencies

#### Step 4: Apply Fixes

Use `Edit` tool to fix errors systematically:

**For union type issues:**
- Add discriminant properties
- Use type guards (`typeof`, `instanceof`, `in` operator)
- Split into separate type branches

**For type mismatches:**
- Adjust return types to match implementation
- Fix parameter types to match usage
- Add proper type assertions (sparingly)

**For null/undefined issues:**
- Add optional chaining (`?.`)
- Use nullish coalescing (`??`)
- Add proper null checks
- Update types to reflect actual nullability

**For generic issues:**
- Specify explicit type parameters
- Add constraints to generics
- Fix variance issues (covariance/contravariance)

#### Step 5: Verify Fixes

After each batch of fixes, re-run the TypeScript compiler:

```bash
pnpm ts
```

Continue until all errors are resolved.

## Advanced Patterns

### Discriminated Unions

When dealing with union types that need discrimination:

```typescript
// Problem: Type not narrowed properly
type Result = SuccessResult | ErrorResult;

// Solution: Add discriminant property
type Result =
  | { status: 'success'; data: Data }
  | { status: 'error'; error: Error };

// Use type guards
if (result.status === 'success') {
  // TypeScript knows result.data exists here
}
```

### Conditional Types Based on Other Properties

```typescript
// Make properties conditional on other properties
type Props =
  | { multiple: true; value: string[]; onChange: (v: string[]) => void }
  | { multiple?: false; value: string; onChange: (v: string) => void };

// Add more discrimination with optional vs required
type PropsWithOptional =
  | { required: true; value: string; onChange: (v: string) => void }
  | { required?: false; value: string | null; onChange: (v: string | null) => void };
```

### Generic Constraints

```typescript
// Problem: Generic type too broad
function process<T>(item: T) {
  return item.id; // Error: Property 'id' does not exist on type 'T'
}

// Solution: Add constraint
function process<T extends { id: string }>(item: T) {
  return item.id; // OK
}
```

## Best Practices

1. **Understand Before Fixing**: Read the error message carefully and understand the root cause
2. **Minimal Changes**: Make the smallest change that fixes the issue
3. **Avoid `any`**: Never use `any` as a quick fix - it defeats TypeScript's purpose
4. **Preserve Intent**: Keep the original type safety intent when fixing
5. **Test Incrementally**: Fix one category of errors at a time
6. **Document Complex Types**: Add comments for non-obvious type decisions

## Common Error Codes

- **TS2322**: Type not assignable - check type compatibility
- **TS2345**: Argument type mismatch - check function call parameters
- **TS2339**: Property does not exist - check object types and optional properties
- **TS2571**: Object is of type 'unknown' - add type guards
- **TS2769**: No overload matches call - check function signatures
- **TS7053**: Element implicitly has 'any' type - add index signature or use Record<>

## Usage Examples

### Mode 1 Usage: User Provides Code Directly

**User says:**
```
I have this TypeScript error:

Type '{ cache: (properties: string[]) => Promise<Feature[]>; }'
is not assignable to type 'DatabaseTileInfo'.
Property 'tiles' is missing in type but required.

My code:
type DatabaseTileInfo = {
  source: 'database';
  tiles: string;
  cache?: Function;
};

const config: DatabaseTileInfo = {
  source: 'database',
  cache: buildFeatures  // Error here
};
```

**Skill response:**
"The issue is that `tiles` is always required in `DatabaseTileInfo`, but you want to use `cache` instead. You need to make these properties mutually exclusive using a discriminated union..."

[Provides solution with explanation]

### Mode 2 Usage: Project-Wide Fix

**User says:**
"Fix all TypeScript errors in the project"

**Skill response:**
[Runs `pnpm ts`, categorizes errors, fixes them systematically]

## Code Fix Examples

### Example 1: Fix Union Type Property Access

**Error:**
```
Type '{ cache: ...; }' is not assignable to type 'TileInfo'.
Property 'tiles' is missing but required.
```

**Fix:**
```typescript
// Split union to make 'tiles' conditional
type DatabaseTileInfo =
  | { source: 'database'; cache: Function; tiles?: string }
  | { source: 'database'; cache?: undefined; tiles: string };
```

### Example 2: Fix Null Safety Issue

**Error:**
```
Object is possibly 'null' or 'undefined'
```

**Fix:**
```typescript
// Add optional chaining
const value = obj?.property?.nested;

// Or add null check
if (obj !== null && obj !== undefined) {
  const value = obj.property;
}
```

### Example 3: Fix Generic Type Inference

**Error:**
```
Type 'Promise<Feature[]>' is not assignable to type 'Promise<Feature>'
```

**Fix:**
```typescript
// Update type definition to match actual return type
type TileInfo = {
  cache?: (properties: string[]) => Promise<Feature[]>; // Add []
};
```

## Output Format

After fixing all errors:

1. Summary of errors fixed
2. Files modified (with line numbers)
3. Any remaining warnings or issues
4. Confirmation that `pnpm ts` passes

## Notes

- Always preserve existing functionality while fixing types
- Consider the broader type system impact of changes
- If a fix seems too complex, discuss with the user first
- Document any non-obvious type decisions in comments
