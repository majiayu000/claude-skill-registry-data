---
name: error-fixer
description: Systematic error fixing workflow for Dashboard Link SaaS. Use when user says "fix all errors", "resolve errors", "fix the build", "make it work", "troubleshoot", or when encountering TypeScript errors, lint errors, build failures, test failures, or runtime errors. Provides step-by-step debugging and resolution strategies.
---

# Error Fixer

## Overview

Provides systematic approach to identifying, categorizing, and fixing errors in the Dashboard Link SaaS monorepo, from TypeScript compilation errors to runtime bugs.

## Systematic Error Fixing Process

### Step 1: Identify ALL Errors

Run all checks to get complete picture:

```bash
# Linting errors
pnpm lint 2>&1 | tee lint-errors.txt

# TypeScript errors
pnpm typecheck 2>&1 | tee typecheck-errors.txt

# Build errors
pnpm build 2>&1 | tee build-errors.txt

# Test errors
pnpm test 2>&1 | tee test-errors.txt
```

### Step 2: Categorize Errors

Group errors by type:
- 🔴 **Critical**: Build failures, type errors
- 🟡 **Important**: Lint errors, test failures
- 🟢 **Minor**: Warnings, style issues

### Step 3: Fix in Priority Order

1. **Type errors** (blocks build)
2. **Import errors** (blocks runtime)
3. **Lint errors** (code quality)
4. **Test failures** (functionality issues)
5. **Warnings** (potential issues)

### Step 4: Fix One Error at a Time

```bash
# Fix error
# Verify fix
pnpm typecheck

# If fixed, commit
git add .
git commit -m "fix: resolve [specific error]"

# Move to next error
```

### Step 5: Verify All Fixed

```bash
# Run all checks
pnpm lint && pnpm typecheck && pnpm build && pnpm test

# If all pass, you're done!
```

## Common Error Types & Fixes

### TypeScript Errors

#### 1. "Cannot find module" or "Module not found"

**Cause**: Wrong import path or missing dependency

```typescript
// ❌ Error
import { Worker } from '@dashboard-link/types';
// Module '@dashboard-link/types' not found

// ✅ Fix - Install dependency
pnpm add @dashboard-link/types --filter <current-package>

// ✅ Or fix import path
import { Worker } from './types/workerTypes';
```

#### 2. "Type 'X' is not assignable to type 'Y'"

**Cause**: Type mismatch

```typescript
// ❌ Error
const count: number = "123"; // Type 'string' is not assignable to type 'number'

// ✅ Fix - Convert type
const count: number = parseInt("123");

// ✅ Or fix type annotation
const count: string = "123";
```

#### 3. "Property 'X' does not exist on type 'Y'"

**Cause**: Missing property or wrong type

```typescript
// ❌ Error
const worker: Worker = { name: 'John' };
worker.phone; // Property 'phone' does not exist

// ✅ Fix - Add property
const worker: Worker = { 
  name: 'John',
  phone: '+61412345678' 
};

// ✅ Or make property optional
interface Worker {
  name: string;
  phone?: string; // Optional
}
```

#### 4. "Object is possibly 'undefined'"

**Cause**: Accessing property without null check

```typescript
// ❌ Error
const worker = workers.find(w => w.id === id);
console.log(worker.name); // Object is possibly 'undefined'

// ✅ Fix - Add null check
const worker = workers.find(w => w.id === id);
if (worker) {
  console.log(worker.name);
}

// ✅ Or use optional chaining
console.log(worker?.name);

// ✅ Or throw error
if (!worker) throw new Error('Worker not found');
console.log(worker.name);
```

#### 5. "Argument of type 'X' is not assignable to parameter of type 'Y'"

**Cause**: Function called with wrong type

```typescript
// ❌ Error
function getWorker(id: string) { }
getWorker(123); // Argument of type 'number' is not assignable to parameter of type 'string'

// ✅ Fix - Convert argument
getWorker(String(123));

// ✅ Or update function signature
function getWorker(id: string | number) { }
```

### Lint Errors

#### 1. "Unexpected console statement"

```typescript
// ❌ Error
console.log('Debug info');

// ✅ Fix - Remove
// console.log('Debug info');

// ✅ Or use proper logging
logger.debug('Debug info');
```

#### 2. "Missing return type"

```typescript
// ❌ Error
async function getWorker(id: string) {
  return await db.from('workers').select().eq('id', id);
}

// ✅ Fix - Add return type
async function getWorker(id: string): Promise<Worker | null> {
  return await db.from('workers').select().eq('id', id);
}
```

#### 3. "Unexpected 'any'"

```typescript
// ❌ Error
function processData(data: any) { }

// ✅ Fix - Use specific type
function processData(data: WorkerData) { }

// ✅ Or use unknown
function processData(data: unknown) {
  if (isWorkerData(data)) {
    // Type narrowing
  }
}
```

### Build Errors

#### 1. "Cannot find package '@dashboard-link/X'"

**Cause**: Dependency not installed or not built

```bash
# ✅ Fix - Install dependencies
pnpm install

# ✅ Or build dependency
pnpm --filter @dashboard-link/X build
```

#### 2. "Export 'X' not found in module 'Y'"

**Cause**: Missing export

```typescript
// ❌ Error - workerService.ts
function createWorker() { }

// ✅ Fix - Export function
export function createWorker() { }
```

#### 3. "Circular dependency detected"

**Cause**: Files import each other

```typescript
// ❌ Error
// a.ts imports b.ts
// b.ts imports a.ts

// ✅ Fix - Extract shared code
// Create c.ts with shared code
// a.ts and b.ts both import from c.ts
```

### Runtime Errors

#### 1. "Cannot read property 'X' of undefined"

**Cause**: Accessing property on undefined object

```typescript
// ❌ Error
const name = user.profile.name; // user.profile is undefined

// ✅ Fix - Add null checks
const name = user?.profile?.name;

// ✅ Or validate first
if (!user?.profile) {
  throw new Error('User profile not found');
}
const name = user.profile.name;
```

#### 2. "Network request failed"

**Cause**: API endpoint down or unreachable

```typescript
// ❌ Error
const response = await fetch('/api/workers');

// ✅ Fix - Add error handling
try {
  const response = await fetch('/api/workers');
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const data = await response.json();
} catch (error) {
  console.error('Failed to fetch workers:', error);
  toast.error('Failed to load workers');
}
```

#### 3. "Unexpected token in JSON"

**Cause**: Invalid JSON response

```typescript
// ❌ Error
const data = await response.json(); // Response is HTML, not JSON

// ✅ Fix - Check content type
const contentType = response.headers.get('content-type');
if (contentType?.includes('application/json')) {
  const data = await response.json();
} else {
  const text = await response.text();
  throw new Error(`Unexpected response: ${text}`);
}
```

### Test Errors

#### 1. "Test timeout exceeded"

**Cause**: Async operation not completing

```typescript
// ❌ Error
test('creates worker', async () => {
  await createWorker(data); // Hangs forever
});

// ✅ Fix - Add timeout or mock
test('creates worker', async () => {
  const mock = vi.fn().mockResolvedValue({ id: '123' });
  await createWorker(data);
}, 10000); // 10 second timeout
```

#### 2. "Expected X but received Y"

**Cause**: Assertion mismatch

```typescript
// ❌ Error
expect(worker.status).toBe('active'); // Received 'ACTIVE'

// ✅ Fix - Match expected value
expect(worker.status).toBe('ACTIVE');

// ✅ Or transform before comparing
expect(worker.status.toLowerCase()).toBe('active');
```

## Debugging Workflow

### For "Fix All Errors" Request

1. **Collect all errors**:
   ```bash
   pnpm lint 2>&1 | tee lint-errors.txt
   pnpm typecheck 2>&1 | tee typecheck-errors.txt
   pnpm build 2>&1 | tee build-errors.txt
   ```

2. **Count and categorize**:
   ```bash
   # Count TypeScript errors
   grep -c "error TS" typecheck-errors.txt
   
   # Count lint errors
   grep -c "error" lint-errors.txt
   ```

3. **Fix by category**:
   - Start with TypeScript errors (block everything)
   - Then import errors
   - Then lint errors
   - Finally warnings

4. **Verify after each batch**:
   ```bash
   pnpm typecheck && echo "✅ Types OK"
   pnpm lint && echo "✅ Lint OK"
   pnpm build && echo "✅ Build OK"
   ```

5. **Commit when clean**:
   ```bash
   git add .
   git commit -m "fix: resolve all TypeScript and lint errors"
   ```

### For Specific Error

1. **Read error message carefully**
2. **Identify exact location** (file, line number)
3. **Understand the cause**
4. **Apply smallest fix possible**
5. **Verify fix works**
6. **Check for similar errors elsewhere**

## Error Prevention

### Use TypeScript Strict Mode
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

### Use ESLint Auto-fix
```bash
pnpm lint:fix
```

### Use Pre-commit Hooks
```bash
# Husky runs lint-staged before commit
# Catches errors before they're committed
```

### Add Editor Integration
- VSCode: TypeScript and ESLint plugins
- Auto-fix on save
- Real-time error highlighting

## Resources

- See `references/error-patterns.md` for common error patterns
- See `references/debugging-guide.md` for debugging strategies

## Common Pitfalls

- Fixing errors without understanding the cause
- Ignoring warnings (they become errors later)
- Not testing after fixing
- Fixing same error in multiple places (should extract to function)
- Using `@ts-ignore` instead of fixing properly

## Best Practices

- Fix root cause, not symptoms
- Add types to prevent future errors
- Write tests to prevent regressions
- Use auto-fix tools where appropriate
- Commit after each successful fix
- Group related fixes in one commit
- Document complex fixes with comments
